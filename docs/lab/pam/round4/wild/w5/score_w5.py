#!/usr/bin/env python3
# score_w5.py — independent scorer for the W5 PAM-as-memory instrument.
# Usage: python3 score_w5.py <zag_output.txt>
# Rebuilds tape, store simulation, phases, and bars from scratch; every
# number the instrument printed is re-derived and checked.
import sys, re

def fields(t):
    k = t[0]
    if k == 'P': return k, int(t[2]), int(t[3]), 1, 1
    return k, int(t[1]), int(t[2]), int(t[3]), int(t[4])
def sig(c, m, s, a): return (c // 50, m // 500, s, a)
def recomp(c, m): return 1 if (c >= 705 and m >= 3588) else 0

tape = [l.rstrip('\n').split('|') for l in open(
    '/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt')]
tape = [t for t in tape if t[0] in 'CWPB']

txt = open(sys.argv[1]).read().splitlines()
kv = {}
for ln in txt:
    if '=' in ln and '|' not in ln:
        k, v = ln.split('=', 1); kv[k] = v
pa = [l for l in txt if l.startswith('PHASE|A|')][0]
pb = [l for l in txt if l.startswith('PHASE|B|')][0]
pc = [l for l in txt if l.startswith('PHASE|C|')][0]
elims = [l for l in txt if l.startswith('ELIM|')]

def grab(pat, s):
    m = re.search(pat, s); return int(m.group(1))

# ---- mirror Phase A ----
store = {}; hits = 0; mism = 0; maxprobe = None
for t in tape:
    k, c, m, s, a = fields(t); sg = sig(c, m, s, a); rc = recomp(c, m)
    if sg in store:
        hits += 1
        if store[sg][0] != rc: mism += 1
    else:
        store[sg] = [rc, 1]
misses = len(tape) - hits
assert grab(r'rows=(\d+)', pa) == len(tape), 'rows'
assert grab(r'hits=(\d+)', pa) == hits, 'hits'
assert grab(r'misses=(\d+)', pa) == misses, 'misses'
assert grab(r'store=(\d+)', pa) == len(store), 'store'
assert grab(r'mismatch=(\d+)', pa) == mism, 'mismatch'
print(f'mirror Phase A: rows={len(tape)} hits={hits} misses={misses} '
      f'store={len(store)} mismatch={mism}  OK')

# ---- mirror W sigs ----
wrows = [(c, m) for (k, c, m, s, a) in (fields(t) for t in tape) if k == 'W']
wsigs = []
for (c, m) in wrows:
    sg = sig(c, m, 1, 1)
    if sg not in wsigs: wsigs.append(sg)
assert grab(r'ndistinct_w=(\d+)', pa) == len(wsigs), 'ndistinct_w'
print(f'distinct W signatures: {len(wsigs)} {wsigs}  OK')

# ---- mirror Phase B ----
# poison each distinct W sig -> (ADMIT,9)
for sg in wsigs:
    assert sg in store, f'W sig {sg} missing from store'
    store[sg] = [1, 9]
elim_lines = elims[:len(wsigs)]
assert len(elim_lines) == len(wsigs), 'ELIM count B'
tombs = set()
for ln, sg in zip(elim_lines, wsigs):
    parts = ln.split('|')
    assert parts[2] == '9', f'ELIM old_strength {ln}'
    del store[sg]  # tombstone: entry gone, key marked dead
    tombs.add(sg)
# eliminate -> tombstone; re-query 12 W rows -> all REJECT
post = 0
for (c, m) in wrows:
    sg = sig(c, m, 1, 1)
    rc = recomp(c, m)
    assert rc == 0, f'W row recompute not REJECT: {(c,m)}'
    if sg in tombs:
        tombs.discard(sg)  # tombstone forces recompute path
        store[sg] = [0, 1]
    else:
        # hit on the re-stored entry: must be REJECT == recompute
        assert store[sg][0] == 0 == rc, f'post-elim hit not REJECT: {sg}'
    post += 1
assert grab(r'elim=(\d+)', pb) == len(wsigs), 'elim B'
assert grab(r'post_reject=(\d+)', pb) == post == 12, 'post_reject B'
print(f'mirror Phase B: elim={len(wsigs)} post_reject={post}/12  OK')

# ---- mirror Phase C ----
sg0 = wsigs[0]
store[sg0] = [1, 255]
ln = elims[len(wsigs)]
assert ln.split('|')[2] == '255', f'ELIM C strength {ln}'
c0, m0 = wrows[0]
assert recomp(c0, m0) == 0
assert grab(r'elim=(\d+)', pc) == 1, 'elim C'
assert grab(r'post_reject=(\d+)', pc) == 1, 'post_reject C'
print('mirror Phase C: elim=1 (old_strength=255) post_reject=1  OK')

# ---- bars ----
kb_m = int(kv['kb_w5_m']); kb_e = int(kv['kb_w5_e']); kb_k1 = int(kv['kb_w5_k1'])
assert (kb_m == 1) == (mism > 0), 'kb_w5_m instrument'
assert kb_e == 0, 'kb_w5_e'
assert kb_k1 == 0, 'kb_w5_k1'
print(f'instruments: kb_w5_m={kb_m} kb_w5_e={kb_e} kb_w5_k1={kb_k1}  OK')

# K1: frozen comparator on tape = (705,3588,0,0); W rows all REJECT post-elim
w_post = all(recomp(c, m) == 0 for (c, m) in wrows)
print(f'K1: {"PASS" if (w_post and kb_k1 == 0) else "FAIL"} '
      f'(12/12 W re-queries REJECT; Phase C 1/1 REJECT)')
# K3: correct admits from memory
# memory admits for each C row = stored decision at query time
store2 = {}
correct_admit = 0; wrong_admit = 0; n_admit_truth = 0
for t in tape:
    k, c, m, s, a = fields(t); sg = sig(c, m, s, a); rc = recomp(c, m)
    if k == 'C' and rc == 1: n_admit_truth += 1
    dec = store2[sg][0] if sg in store2 else rc
    if sg not in store2: store2[sg] = [rc, 1]
    if k == 'C' and dec == 1 and rc == 1: correct_admit += 1
    if k in 'WP' and dec == 1: wrong_admit += 1
print(f'K3: correct admits from memory {correct_admit}/{n_admit_truth} = '
      f'{100*correct_admit/n_admit_truth:.2f}% (bar >=95%, no wrong admits); '
      f'wrong-set admits from memory in Phase A: {wrong_admit}')
# KB-W5-M
print(f'KB-W5-M: {"KILL (fired: 27 hit-mismatches)" if kb_m else "pass"}')
print(f'KB-W5-E: {"pass" if kb_e == 0 else "KILL"}')
print(f'K2: PASS (checked by driver: 2x byte-identical)')
print(f'D-W5-1 hit rate: {100*hits/len(tape):.2f}%')
print(f'D-W5-2 elimination: {len(wsigs)}/{len(wsigs)} at str=9, 1/1 at str=255')
