#!/usr/bin/env python3
"""Single-leg RSS: runs the binary once, prints children's ru_maxrss (KB, Linux).
One leg per invocation (RUSAGE_CHILDREN max is cumulative per process).
Usage: rss_one.py <binary> <scale> <variant> <input> <out.tsv>
"""
import subprocess, resource, sys

binary, scale, variant, inp, out = sys.argv[1:6]
subprocess.run([binary, scale, variant, inp, out], check=True)
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print(ru.ru_maxrss)
