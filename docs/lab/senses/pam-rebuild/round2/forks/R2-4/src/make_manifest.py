#!/usr/bin/env python3
"""Generate MANIFEST.sha256 covering every fixture byte used.

Covers, in deterministic sorted order, no timestamps:
  1) all generated *.r24 and *.r24.truth in ../fixtures/
  2) all frozen harness fixture/truth bytes referenced by the trial manifest
Format: <sha256>  <path> per line (like sha256sum).
Also writes a summary line with total count and a manifest-of-manifest hash.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "..", "fixtures")
OUT = os.path.join(HERE, "..", "evidence", "MANIFEST.sha256")
LAB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
HARN = os.path.join(LAB, "senses", "rebuild", "harness", "fixtures")
TRIALS = os.path.join(HERE, "..", "evidence", "_evalwork_r24", "trials.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    lines = []
    # 1) Generated R2A fixtures
    for f in sorted(os.listdir(FIX)):
        if f.endswith(".r24") or f.endswith(".r24.truth"):
            lines.append("%s  fixtures/%s\n" % (sha(os.path.join(FIX, f)), f))
    # 2) Frozen harness fixtures referenced in trial manifest
    trials = json.load(open(TRIALS))
    harn_basenames = sorted(set(
        tr["path"] for tr in trials if tr["src"] == "harness"
    ))
    for p in harn_basenames:
        # p is absolute path; record relative to HARN
        rel = os.path.relpath(p, HARN)
        if os.path.exists(p):
            lines.append("%s  harness/%s\n" % (sha(p), rel))
        # truth file: try .truth and .r24.truth
        for tp in (p + ".truth",):
            if os.path.exists(tp):
                trel = os.path.relpath(tp, HARN)
                lines.append("%s  harness/%s\n" % (sha(tp), trel))
    lines.sort()
    body = "".join(lines)
    mom = hashlib.sha256(body.encode()).hexdigest()
    with open(OUT, "w") as fh:
        fh.write("# R2-4 fixture manifest (generated + frozen harness)\n")
        fh.write("# files: %d\n" % len(lines))
        fh.write("# manifest-sha256: %s\n" % mom)
        fh.write(body)
    print("wrote %s: %d files, manifest-sha256=%s" % (OUT, len(lines), mom))


if __name__ == "__main__":
    main()
