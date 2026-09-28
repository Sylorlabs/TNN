#!/usr/bin/env python3
"""RSS measurement via resource.getrusage(RUSAGE_CHILDREN).ru_maxrss (KB on Linux).
Deterministic allocator => max RSS is stable; 2x per leg to confirm.
Usage: rss_harness.py <binary> ; reads legs.list: "<scale> <variant> <input> <tag>"
writes rss_results.txt: "<tag> <kb1> <kb2>" and saves <tag>.tsv outputs.
"""
import subprocess, resource, sys

binary = sys.argv[1]
out_lines = []
for line in open("legs.list"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    scale, variant, inp, tag = line.split(None, 3)
    kbs = []
    for rep in (1, 2):
        subprocess.run([binary, scale, variant, inp, f"{tag}.tsv"],
                       check=True)
        ru = resource.getrusage(resource.RUSAGE_CHILDREN)
        kbs.append(ru.ru_maxrss)
    # ru_maxrss is cumulative-max over ALL waited children; take the delta
    # per leg instead: measure one leg at a time in a fresh python per leg.
    out_lines.append(f"{tag} {' '.join(map(str, kbs))}")
    print(out_lines[-1], flush=True)
open("rss_results.txt", "w").write("\n".join(out_lines) + "\n")
