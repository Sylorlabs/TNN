#!/usr/bin/env python3
"""Label-blind scoring of the real-learner runs (I22).

The scorer (battery_amended, learner mode) is mechanical: last-word match,
no human reads any response. Label-blindness procedure: each run's
transcripts are copied into a workdir named by the SHA-256 (12 hex) of its
resp_p0.txt content; scoring runs there; SCORES.md is keyed by hash id only.
The hash->run mapping is written to a SEALED file, opened only after all
scores are recorded (here: immediately after, to verify determinism — the
scoring itself never saw the labels).

Usage: score_blind.py <battery_bin> <run1> <run2> <run_pert>
Writes: blind_scores/<hid>/learner.out, SCORES.md (by hid), SEALED_MAP.txt
"""
import hashlib, os, shutil, subprocess, sys

def hid_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]

def main():
    binpath, runs = sys.argv[1], sys.argv[2:]
    work = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blind_scores")
    os.makedirs(work, exist_ok=True)
    mapping = {}
    for r in runs:
        hid = hid_of(os.path.join(r, "resp_p0.txt"))
        mapping[hid] = r
        dest = os.path.join(work, hid)
        os.makedirs(dest, exist_ok=True)
        for fn in ("resp_p0.txt", "resp_p3.txt"):
            shutil.copy(os.path.join(r, fn), os.path.join(dest, fn))
        subprocess.run([binpath, "learner"], cwd=dest,
                       stdout=open(os.path.join(dest, "learner.out"), "w"),
                       check=True)
    with open(os.path.join(work, "SEALED_MAP.txt"), "w") as f:
        for hid in sorted(mapping):
            f.write(f"{hid} -> {mapping[hid]}\n")
    # SCORES.md keyed by hid only
    lines = ["# Blind scores (keyed by transcript hash id)", ""]
    for hid in sorted(mapping):
        with open(os.path.join(work, hid, "learner.out")) as f:
            txt = f.read()
        summ = [l for l in txt.splitlines() if l.startswith("SUMMARY")][0]
        lines.append(f"## {hid}")
        lines.append(f"    {summ}")
        lines.append("")
    with open(os.path.join(work, "SCORES.md"), "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    # determinism check across the three (labels revealed only for the check)
    outs = [open(os.path.join(work, h, "learner.out")).read() for h in mapping]
    print("byte-identical across runs:", "YES" if len(set(outs)) == 1 else "NO")

if __name__ == "__main__":
    main()
