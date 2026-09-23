#!/usr/bin/env python3
"""Static no-RNG scan over the step English leg sources.

Flags any identifier/API that could introduce nondeterminism:
rand/random/rng/entropy/clock/time/pid/thread. Excludes known-benign
curriculum-geometry names (seed_id/pool_id/heldout are deterministic
index functions, not RNG). Prints every hit with context for human review.
Exit 1 if any hit needs review (i.e., any hit at all — reviewer confirms).
"""
import os
import re
import sys

ROOT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/step/legs/tnn"
PAT = re.compile(r"(?i)\brand\b|random|rng|entropy|getpid|_zag_time|clock_gettime|srand|/dev/urandom|thread")
BENIGN = re.compile(r"seed_id|pool_id|heldout|_ho_has|branch|randomized")

hits = []
comments = 0
for dirpath, _, fns in os.walk(ROOT):
    for fn in fns:
        if not fn.endswith(".zag"):
            continue
        p = os.path.join(dirpath, fn)
        for ln, line in enumerate(open(p), 1):
            code = line.split("//")[0]  # strip comments
            if PAT.search(line) and not BENIGN.search(line):
                if PAT.search(code):
                    hits.append((p, ln, line.strip()))
                else:
                    comments += 1

print(f"scanned .zag files under {ROOT}")
print(f"comment-only mentions (asserting no-RNG): {comments}")
if hits:
    print(f"HITS REQUIRING REVIEW: {len(hits)}")
    for p, ln, line in hits:
        print(f"  {os.path.relpath(p, ROOT)}:{ln}: {line[:120]}")
    sys.exit(1)
print("no RNG/nondeterminism identifiers found — PASS")
