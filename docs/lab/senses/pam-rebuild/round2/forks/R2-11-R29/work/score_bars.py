#!/usr/bin/env python3
"""Score R2-11 mechanical bars from completed battery runs.

Usage: score_bars.py <forkA_run_base> <forkB_run_base>
Merges both shards, joins percepts.tsv with trials.tsv truth.
Trial ids repeat across tasks -> key = (trial_id, task, fixture).

Bars:
  B1: primary accuracy on the 370 harness-primary trials (>=60% pass)
  B5: false permanent installs / all trials (<=3% pass)
  B3: mean percept ops, mean render ops (B), mean artifact bytes/percept
  KB-E2: bad selection rows, empty artifacts
"""
import sys, os, glob

def load_percepts(base):
    rows = []
    for tsv in sorted(glob.glob(base + '_sh?/percepts.tsv')):
        lines = open(tsv).read().splitlines()
        assert lines[0].startswith('trial\ttask'), lines[0][:40]
        rows += [l.split('\t') for l in lines[1:]]
    return rows

def main():
    baseA, baseB = sys.argv[1], sys.argv[2]
    trials = [l.rstrip('\n').split('\t') for l in open('trials.tsv')][1:]
    truth = {(r[0], r[1], r[4]): r[5] for r in trials}
    fam = {(r[0], r[1], r[4]): r[3] for r in trials}
    print(f"truth trials: {len(truth)}")

    for fork, base in (('A', baseA), ('B', baseB)):
        P = load_percepts(base)
        if not P:
            print(f"--- fork {fork}: NO DATA ---")
            continue
        def key(r): return (r[0], r[1], r[2])
        have = {key(r) for r in P}
        missing = [k for k in truth if k not in have]
        nf = sum(max(0, len(open(t).read().splitlines()) - 1)
                 for t in glob.glob(base + '_sh?/failed.tsv'))
        prim = [r for r in P if fam[key(r)] == 'harness-primary']
        b1 = sum(1 for r in prim if r[3] == truth[key(r)]) / 370
        n_inst = sum(1 for r in P if r[5] == 'INSTALL')
        n_false = sum(1 for r in P if r[5] == 'INSTALL' and r[3] != truth[key(r)])
        b5 = n_false / len(truth)
        ops = [int(r[6]) for r in P]
        rops = []
        for t in sorted(glob.glob(base + '_sh?/render_ops.tsv')):
            rops += [int(l.split('\t')[1]) for l in open(t).read().splitlines()[1:]]
        nbytes = nart = 0
        for d in sorted(glob.glob(base + '_sh?/artifacts')):
            for e in os.listdir(d):
                nbytes += os.path.getsize(os.path.join(d, e))
                nart += 1
        bad_sel = sum(1 for r in P if int(r[7]) != len(r[8].split(';') if r[8] else []))
        empty_art = 0
        for d in sorted(glob.glob(base + '_sh?/artifacts')):
            for e in os.listdir(d):
                if os.path.getsize(os.path.join(d, e)) == 0:
                    empty_art += 1
        print(f"--- fork {fork} ---")
        print(f"percepts={len(P)} failed={nf} missing={len(missing)} installed={n_inst}")
        print(f"B1 primary: {len(prim)} trials, acc={b1:.4f} ({'PASS' if b1 >= 0.60 else 'FAIL'})")
        print(f"B2 delta vs Approach A (0.726): {b1 - 0.726:+.4f}")
        print(f"B5 false installs: {n_false}/{len(truth)} = {b5:.4f} ({'PASS' if b5 <= 0.03 else 'FAIL'})")
        print(f"B3 percept ops: mean={sum(ops)/len(ops):,.0f} max={max(ops):,}")
        if rops:
            print(f"B3 render ops: mean={sum(rops)/len(rops):,.0f} max={max(rops):,}")
        print(f"B3 artifact bytes: total={nbytes:,} per_percept={nbytes/len(P):,.0f} (nart={nart})")
        print(f"KB-E2: bad_sel_rows={bad_sel} empty_artifacts={empty_art}")

main()
