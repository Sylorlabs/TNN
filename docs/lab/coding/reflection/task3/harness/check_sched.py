#!/usr/bin/env python3
"""Scheduler bars (frozen 2026-09-22). Reads program stdout on stdin.
PASS: byte-identical to frozen expected AND skew<=1 AND min>=1."""
import sys

EXPECTED = "".join(f"task {i}: 100\n" for i in range(8)) \
    + "SEQ 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7\n"

got = sys.stdin.read()
fails = []
if got != EXPECTED:
    fails.append("stdout not byte-identical to frozen expected")
    # still parse what we can
counts = []
for line in got.splitlines():
    if line.startswith("task "):
        try:
            counts.append(int(line.split(":")[1]))
        except Exception:
            pass
seq_ok = "SEQ 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7" in got
if len(counts) != 8:
    fails.append(f"want 8 task lines, got {len(counts)}")
else:
    skew = max(counts) - min(counts)
    print(f"counts={counts} skew={skew} min={min(counts)}")
    if skew > 1:
        fails.append(f"skew {skew} > 1")
    if min(counts) < 1:
        fails.append("starvation: a task has count < 1")
if not seq_ok:
    fails.append("SEQ line missing/wrong (cyclic order not proven)")
if fails:
    for f in fails:
        print("FAIL:", f)
    print("RESULT: FAIL")
    sys.exit(1)
print("RESULT: PASS (byte-identical, skew<=1, no starvation)")
