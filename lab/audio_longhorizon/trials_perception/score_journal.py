#!/usr/bin/env python3
"""Score a session_run_pr4 journal: extract PR4 bits lines in EP order,
compare to a labels JSON {clipkey: 'b2b1b0'}. Clip key = basename of the
session line without .wav (for pr4: 'pr4:0000'). Prints agreement stats.
Usage: score_journal.py <journal> <session.txt> <labels.json>
"""
import json, re, sys

journal, sess, labf = sys.argv[1:4]
labels = json.load(open(labf))
sess_lines = [l.strip() for l in open(sess) if l.strip() and not l.startswith('#')]
bits = re.findall(r'^PR4 bits=([01]{3})$', open(journal).read(), re.M)
assert len(bits) == len(sess_lines), 'bits=%d clips=%d' % (len(bits), len(sess_lines))
tot = hit = 0
per = []
for b, s in zip(bits, sess_lines):
    key = s.rsplit('/', 1)[-1]
    if key.endswith('.wav'): key = key[:-4]
    lab = labels[key]
    a = sum(1 for x, y in zip(b, lab) if x == y) / 3.0
    per.append((key, b, lab, a))
    tot += 3; hit += sum(1 for x, y in zip(b, lab) if x == y)
print('clips=%d bits=%d agree=%d mean_agreement=%.4f' % (len(bits), tot, hit, hit / tot))
b2 = sum(1 for k, b, l, a in per if b[0] == l[0]); b1 = sum(1 for k, b, l, a in per if b[1] == l[1]); b0 = sum(1 for k, b, l, a in per if b[2] == l[2])
n = len(per)
print('per-bit agreement: frac_static=%.3f hnr=%.3f prosody=%.3f' % (b2/n, b1/n, b0/n))
for k, b, l, a in per:
    if a < 1.0:
        print('  MISS', k, 'organ=%s label=%s' % (b, l))
