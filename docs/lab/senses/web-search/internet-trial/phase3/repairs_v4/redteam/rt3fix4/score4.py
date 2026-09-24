#!/usr/bin/env python3
# score4.py — score a run4 output against a corpus oracle.
# Usage: score4.py <corpus.tsv> <run.txt> [--codes] [--items]
import sys

def load_corpus(p):
    items = {}
    with open(p) as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) < 4:
                continue
            # Oracle is the last column (corpora vary: 4 or 5 columns).
            oracle = parts[-1].strip().upper()
            if oracle not in ('JOKE', 'JOKING', 'NONJOKE', 'UNCERTAIN'):
                continue
            items[parts[0]] = (parts[1], oracle)
    return items

def load_run(p):
    out = {}
    with open(p) as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            out[parts[0]] = (parts[1], parts[2] if len(parts) > 2 else '')
    return out

def main():
    corp = load_corpus(sys.argv[1])
    run = load_run(sys.argv[2])
    show_codes = '--codes' in sys.argv
    show_items = '--items' in sys.argv
    inst, miss = [], []
    code_inst = {}
    for i, (claim, oracle) in corp.items():
        if i not in run:
            print('MISSING', i); continue
        v, codes = run[i]
        installed = v in ('JOKING', 'SATIRE')
        if oracle in ('NONJOKE', 'UNCERTAIN') and installed:
            inst.append(i)
            for c in codes.split('+'):
                code_inst[c] = code_inst.get(c, 0) + 1
        if oracle in ('JOKE', 'JOKING') and v == 'UNCERTAIN':
            miss.append(i)
    n = len(corp)
    print(f'items={n} deadpan_installs={len(inst)} joke_misses={len(miss)}')
    if show_codes:
        print('install codes:', sorted(code_inst.items(), key=lambda x: -x[1]))
    if show_items:
        for i in inst:
            print(' INST', i, run[i][1], corp[i][0][:90])
        for i in miss:
            print(' MISS', i, run[i][1], corp[i][0][:90])

main()
