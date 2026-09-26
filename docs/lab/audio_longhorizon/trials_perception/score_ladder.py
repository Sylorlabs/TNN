#!/usr/bin/env python3
"""Score a ladder journal: extract PR4 bits per EP, map EP->clip via session file,
compare to labels_all.json. Reports overall + per-bit + per-class agreement.
Usage: score_ladder.py <journal.txt> <session.txt> <labels_all.json>
"""
import json, sys, re

jpath, spath, lpath = sys.argv[1], sys.argv[2], sys.argv[3]
sess = [l.strip() for l in open(spath) if l.strip()]
labels = json.load(open(lpath))

bits = []
for line in open(jpath):
    m = re.match(r'PR4 bits=([01]{3})', line.strip())
    if m:
        bits.append(m.group(1))
assert len(bits) == len(sess), '%d bits vs %d sess' % (len(bits), len(sess))

tot = b0 = b1 = b2 = 0
cls_tot = {}
cls_ok = {}
for ep, (clip, ob) in enumerate(zip(sess, bits)):
    cid = clip.rsplit('/', 1)[-1][:-4]
    lab = labels[cid]['bits']
    cls = labels[cid]['cls']
    cls_tot[cls] = cls_tot.get(cls, 0) + 3
    ok = 0
    for i in range(3):
        tot += 1
        if ob[i] == lab[i]:
            if i == 0: b0 += 1
            if i == 1: b1 += 1
            if i == 2: b2 += 1
            ok += 1
    cls_ok[cls] = cls_ok.get(cls, 0) + ok

print('n=%d clips, agreement=%.4f' % (len(sess), (b0 + b1 + b2) / tot))
print('per-bit: frac_static=%.3f hnr=%.3f prosody=%.3f' % (b0 / (tot / 3), b1 / (tot / 3), b2 / (tot / 3)))
for c in sorted(cls_tot):
    print('  class %-8s %.3f (%d bits)' % (c, cls_ok[c] / cls_tot[c], cls_tot[c]))
