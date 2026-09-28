#!/usr/bin/env python3
"""Build-script: flatten frozen tp_data.json into a pipe-delimited text file
for the pure-Zag oracle. No decision logic here — just field extraction.
Usage: prep_flat.py [evidence_dir] [out_file]"""
import json, sys
ev = sys.argv[1] if len(sys.argv) > 1 else '.'
outp = sys.argv[2] if len(sys.argv) > 2 else 'tp_flat.txt'
data = json.load(open(ev + '/tp_data.json'))
idm = json.load(open(ev + '/idmaps.json'))
aid = {v: int(k) for k, v in idm['ans'].items()}
out = []
for q in sorted(data.keys()):
    v = data[q]
    rel = -1 if v['rel'] in (None, 'None') else int(round(float(v['rel']) * 1000))
    rows = v['rows']
    assert len(rows) == 4, q
    out.append(f"ENV|{q}|{v['block']}|{rel}|{len(rows)}")
    for d, a, y in rows:
        out.append(f"ROW|{d}|{a}|{aid[a]}|{y}")
open(outp, 'w').write("\n".join(out) + "\n")
print("envelopes:", len(data), "lines:", len(out), "->", outp)
