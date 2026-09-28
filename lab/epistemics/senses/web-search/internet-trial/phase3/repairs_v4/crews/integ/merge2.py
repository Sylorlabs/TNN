#!/usr/bin/env python3
"""Final assembly: mechanical sections + custom merged functions -> r12_v4.zag"""
import hashlib

# Re-run merge1's assembly logic by exec'ing it (paths already absolute)
ns = {}
exec(open('/home/hatch/workspace/scratch-hellhole/crews/integ/merge1.py').read().split('print("mechanical')[0], ns)
out = ns['out']

D = '/home/hatch/workspace/scratch-hellhole/crews/integ/'
out.append(open(D + 'custom_scan_text.zag.txt').read())
out.append(open('/tmp/v4_r12.txt').read())
out.append(open(D + 'custom_tail.zag.txt').read())

full = "\n".join(out) + "\n"
p = D + 'r12_v4.zag'
open(p, 'w').write(full)
print("wrote", p)
print("bytes:", len(full))
print("sha256:", hashlib.sha256(full.encode()).hexdigest())

# sanity: no duplicate fn definitions
import re
names = re.findall(r'^fn (\w+)\(', full, re.M)
dups = sorted(set(n for n in names if names.count(n) > 1))
print("fn count:", len(names), "duplicates:", dups)
# sanity: balanced braces overall
print("braces:", full.count('{') - full.count('}'))
