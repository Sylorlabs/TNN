#!/usr/bin/env python3
"""sense_run.py — run the pure-Zag Approach-A motion sense on every .vid window.

Usage: sense_run.py [windows_dir] [out_jsonl]
For each <video_id>_w<idx>.vid: runs
    <sense_bin> motiondir <path>
and parses stdout key=value lines into a percept record:
    {video_id, window_idx, window_path, judgment, confidence, ops, dx, dy, mag}
Deterministic: the sense binary is pure-Zag (no RNG, no wall-clock); identical
.vid bytes always give identical records (proven by rerun test).
Sense binary location is a parameter default, not baked-in state.
"""
import json, os, re, subprocess, sys

WORK = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SENSE = os.path.join(WORK, "yt_sense", "sense_t1")  # rematch-T4 fitted (t=1)
FALLBACK_SENSE = os.path.expanduser(
    "~/workspace/tnn-lab/senses/rebuild/a_raw/sense")

def parse(stdout):
    rec = {}
    for line in stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            rec[k.strip()] = v.strip()
    return rec

def main():
    windows = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "windows")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(WORK, "percepts.jsonl")
    sense = os.environ.get("SENSE_BIN", DEFAULT_SENSE)
    files = sorted(f for f in os.listdir(windows) if f.endswith(".vid"))
    n = 0
    with open(out, "w") as fo:
        for fn in files:
            m = re.match(r"^(.+)_w(\d+)\.vid$", fn)
            if not m:
                continue
            vid, idx = m.group(1), int(m.group(2))
            path = os.path.join(windows, fn)
            r = subprocess.run([sense, "motiondir", path],
                               capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                print("ERROR sense rc=%d on %s: %s" % (r.returncode, fn, r.stdout.strip()))
                continue
            kv = parse(r.stdout)
            dbg = kv.get("debug_vec", "")
            def dnum(key):
                m2 = re.search(key + r"=(-?\d+)", dbg)
                return int(m2.group(1)) if m2 else None
            rec = {
                "video_id": vid,
                "window_idx": idx,
                "window_path": fn,
                "judgment": kv.get("judgment"),
                "confidence": int(kv.get("confidence", -1)),
                "ops": int(kv.get("ops", -1)),
                "dx": dnum("dx"),
                "dy": dnum("dy"),
                "mag": dnum("mag"),
            }
            fo.write(json.dumps(rec, sort_keys=True) + "\n")
            n += 1
    print("percepts written: %d -> %s" % (n, out))

if __name__ == "__main__":
    sys.exit(main())
