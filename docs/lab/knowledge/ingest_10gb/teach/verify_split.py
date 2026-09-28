#!/usr/bin/env python3
"""Verify split page files for a stem: contiguity + well-formed tail.
Usage: verify_split.py <outbase> <stem>
Prints: N_GOOD <highest contiguous good index> (resume index), and lists bad files.
A file is good iff its name parses as <stem>_n<8d>.xml and its last 13 bytes are b"</mediawiki>\n".
Zero RNG. Deterministic."""
import os, re, sys
outbase, stem = sys.argv[1], sys.argv[2]
pat = re.compile(rf"^{re.escape(stem)}_n(\d{{8}})\.xml$")
seen = {}
bad = []
for root, _, files in os.walk(outbase):
    for fn in files:
        m = pat.match(fn)
        if not m:
            continue
        idx = int(m.group(1))
        p = os.path.join(root, fn)
        try:
            with open(p, "rb") as f:
                f.seek(-13, 2)
                tail = f.read()
            good = tail == b"</mediawiki>\n"
        except OSError:
            good = False
        if good:
            seen[idx] = p
        else:
            bad.append((idx, p))
# highest contiguous run from 0
n = 0
while n in seen:
    n += 1
print(f"contiguous_good=0..{n-1} count={n}")
if bad:
    print(f"bad_files={len(bad)}")
    for idx, p in sorted(bad)[:20]:
        print(f"  BAD {idx} {p}")
    # any bad below n means a hole inside the contiguous run
    holes = [i for i, _ in bad if i < n]
    if holes:
        print(f"holes_in_run={holes[:10]}")
else:
    print("bad_files=0")
print(f"resume_index={n}")
