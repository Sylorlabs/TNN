#!/usr/bin/env python3
"""Commit the STEP English championship box to tnn-native-lab.

Walks step/, excludes binaries/.zagd/.zag-cache/__pycache__/logs-tmp,
writes a file list, then commits via commit_big_files.py (handles >96KB
blobs via gh-api). Target: branch tnn-native-lab,
docs/lab/wave12/championship/english/step/.

Usage: python3 commit_step.py [--dry]   (dry prints the file list only)
"""
import os
import subprocess
import sys

STEP = "/home/hatch/workspace/tnn-lab/wave12/championship-english/step"
SKIP_DIRS = {".zag-cache", "__pycache__"}
# NB: step/build/*.py (reproducibility scripts) MUST be included; only the
# per-leg native build dirs (legs/tnn/legX/build) are excluded.
SKIP_SUFFIX = (".zagd", ".zagd.semantic-ready")
SKIP_NAMES = set()

def collect():
    out = []
    for dirpath, dirnames, fns in os.walk(STEP):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not (d == "build" and "/legs/" in dirpath)]
        for fn in sorted(fns):
            if fn.endswith(SKIP_SUFFIX) or fn in SKIP_NAMES:
                continue
            p = os.path.join(dirpath, fn)
            # skip compiled binaries (no extension, executable) in leg build dirs
            if "/build/" in p and "." not in os.path.basename(p):
                continue
            # skip evidence run*.log intermediates (only final .log kept)
            if ".run" in fn and fn.endswith(".log"):
                continue
            out.append(p)
    return out

files = collect()
print(f"{len(files)} files")
big = [f for f in files if os.path.getsize(f) > 96*1024]
print(f"{len(big)} files >96KB: {[os.path.basename(f) for f in big]}")
if "--dry" in sys.argv:
    for f in files:
        print(f"  {os.path.relpath(f, STEP)} ({os.path.getsize(f)}B)")
    sys.exit(0)

msg = ("STEP championship English box (step-3.7-flash:free): frozen corpus, "
       "Track-5 D2 leg, §B.7 direct + teacher legs, verdict")
msg_file = "/tmp/step_commit_msg.txt"
open(msg_file, "w").write(msg + "\n")
r = subprocess.run(
    ["python3", os.path.expanduser("~/workspace/commit_big_files.py"),
     "tnn-native-lab", msg_file] + files,
    capture_output=True, text=True)
print(r.stdout[-2000:])
print(r.stderr[-1000:], file=sys.stderr)
