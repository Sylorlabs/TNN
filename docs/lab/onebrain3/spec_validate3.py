#!/usr/bin/env python3
"""Spec-validate v6.tsv against single-mode output run_single_v6.txt.
Checks per item:
  - >=2 readings with ev=1 (spec: >=2 surviving evidence-bearing readings)
  - fork-likely by construction: nread>=2 AND top-two fired-bid SCORE margin<=12
  - readings column references valid reading hids present in actual output
  - expected_bid in 13..24, no duplicate ids/queries, rows parse (5 cols)
Item count is dynamic (not hardcoded). Prints a per-item table + summary.
Exits nonzero on any SPEC failure.
"""
import re, sys

tsv = open('v6.tsv').read().splitlines()
assert tsv[0].split('\t') == ['id','query','expected_bid','readings','rationale'], "header"
rows = [l.split('\t') for l in tsv[1:]]
assert all(len(r) == 5 for r in rows), "all rows must have 5 tab columns"
n = len(rows)
ids = [r[0] for r in rows]
queries = [r[1] for r in rows]
assert len(set(ids)) == len(ids), "duplicate ids"
assert len(set(queries)) == len(queries), "duplicate queries"
exp = {r[0]: int(r[2]) for r in rows}
assert all(13 <= v <= 24 for v in exp.values()), "expected_bid range"

# parse run output: blocks are "<trace lines>\nVERDICT id=..."
blocks = {}
cur = []
for line in open('run_single_v6.txt'):
    line = line.rstrip('\n')
    cur.append(line)
    if line.startswith('VERDICT'):
        m = re.search(r'id=(\S+)', line)
        blocks[m.group(1)] = (cur, line)
        cur = []
assert set(blocks) == set(ids), f"block/id mismatch: {set(ids)^set(blocks)}"

fails = []
print(f"{'id':5} {'exp':3} {'win':3} {'ok?':3} {'nread':5} {'fired bids (hid:score)':38} {'margin':6} {'fork?':5}")
tot_correct = 0
fork_likely = 0
for r in rows:
    iid, query = r[0], r[1]
    lines, verdict = blocks[iid]
    reads = {}
    for l in lines:
        m = re.match(r'READ hid=(\d+) rd=(\S+) ev=(\d+)', l)
        if m: reads[int(m.group(1))] = (m.group(2), int(m.group(3)))
    fired = []
    winner = None
    for l in lines:
        m = re.match(r'BID hid=(\d+) act=(\S+) fire=(\d+) base=(\d+) bonus=(\d+) score=(\d+)', l)
        if m:
            h, fire, score = int(m.group(1)), int(m.group(3)), int(m.group(6))
            if fire == 1: fired.append((h, score))
    m = re.search(r'winner=(\d+)', verdict)
    winner = int(m.group(1))
    ev1 = sorted(h for h, (nm, ev) in reads.items() if ev == 1)
    nread = len(ev1)
    fired.sort(key=lambda x: -x[1])
    margin = fired[0][1] - fired[1][1] if len(fired) >= 2 else None
    fork = (nread >= 2 and margin is not None and margin <= 12)
    ok = 'Y' if winner == exp[iid] else 'n'
    if ok == 'Y': tot_correct += 1
    if fork: fork_likely += 1
    # spec checks
    spec = []
    if nread < 2: spec.append(f"SPEC-FAIL nread={nread}")
    col_hids = sorted(set(int(x) for x in r[3].split('/')))
    if not set(col_hids) <= set(range(10)): spec.append("SPEC-FAIL bad hid in readings col")
    missing = [h for h in col_hids if h not in ev1]
    if missing: spec.append(f"READINGS-COL-MISMATCH col={col_hids} actual_ev1={ev1}")
    if spec: fails.append((iid, '; '.join(spec)))
    fb = ' '.join(f"{h}:{s}" for h, s in fired)
    print(f"{iid:5} {exp[iid]:3} {winner:3} {ok:3} {nread:5} {fb:38} {str(margin):6} {'Y' if fork else 'n':5}")

print()
print(f"items: {n}")
print(f"single-mode accuracy: {tot_correct}/{n} = {tot_correct/n*100:.1f}% (target <70%)")
print(f"fork-likely (>=2 ev1 readings AND top-two fired score margin<=12): {fork_likely}/{n} (target >=30)")
print()
if fails:
    print("FAILURES:")
    for iid, s in fails: print(f"  {iid}: {s}")
    sys.exit(1)
print("ALL SPEC CHECKS PASSED")
