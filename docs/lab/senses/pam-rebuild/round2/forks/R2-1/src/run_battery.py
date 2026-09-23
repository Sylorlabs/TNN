#!/usr/bin/env python3
"""R2-1 battery runner: 10,000 full + 10,000 ablated, hash-chained.

Usage: run_battery.py <trial_index.csv> <out_dir> <mode>
  mode: full | ablated
Writes: <out_dir>/<mode>_results.csv, <out_dir>/<mode>_chain.txt
"""
import os, sys, csv, subprocess, hashlib

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sense_bin")

def parse_output(out):
    """Parse sense binary output into dict."""
    d = {}
    for line in out.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def main():
    index_csv, out_dir, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    assert mode in ("full", "ablated")
    os.makedirs(out_dir, exist_ok=True)
    trials = list(csv.DictReader(open(index_csv)))
    print("mode=%s trials=%d" % (mode, len(trials)), flush=True)
    res_path = os.path.join(out_dir, "%s_results.csv" % mode)
    chain_path = os.path.join(out_dir, "%s_chain.txt" % mode)
    start_idx = 0
    prev_hash = "00" * 32
    if os.path.exists(res_path) and os.path.exists(chain_path):
        with open(chain_path) as cf:
            clines = [l.strip() for l in cf if l.strip()]
        if clines:
            last = clines[-1].split()
            start_idx = int(last[0]) + 1
            prev_hash = last[2]
            print("resuming %s from trial %d" % (mode, start_idx), flush=True)
    wmode = "a" if start_idx > 0 else "w"
    cmode = "a" if start_idx > 0 else "w"
    with open(res_path, wmode, newline="") as rf, open(chain_path, cmode) as cf:
        w = csv.writer(rf)
        if start_idx == 0:
            w.writerow(["trial_idx", "fixture_id", "fixture_path", "task", "truth", "stratum",
                        "judgment", "confidence", "measure", "operations",
                        "percept_bytes", "program", "tests", "decision", "chain_hash"])
        for t in trials:
            idx = t["trial_idx"]
            if int(idx) < start_idx:
                continue
            fid = t["fixture_id"]
            fx = t["fixture_path"]
            p = subprocess.run(
                [BIN, fx, mode, prev_hash, idx, fid],
                capture_output=True, text=True, timeout=60)
            if p.returncode != 0:
                print("FAIL trial %s rc=%d stderr=%s" % (idx, p.returncode, p.stderr[:200]),
                      flush=True)
                d = {}
            else:
                d = parse_output(p.stdout)
            ch = d.get("chain", "")
            w.writerow([idx, fid, fx, t["task"], t["truth"], t["stratum"],
                        d.get("judgment", ""), d.get("conf", ""),
                        d.get("measure", ""), d.get("ops", ""),
                        d.get("percept_bytes", ""), d.get("program", ""),
                        d.get("tests", ""), d.get("decision", ""), ch])
            cf.write("%s %s %s\n" % (idx, fid, ch))
            if ch:
                prev_hash = ch
            if int(idx) % 1000 == 0:
                print("  %s: %s done" % (mode, idx), flush=True)
    print("mode=%s complete" % mode, flush=True)

if __name__ == "__main__":
    main()
