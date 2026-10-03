#!/usr/bin/env python3
"""Regenerate cleanroom_train.tsv and cleanroom_heldout_blind.tsv from corpus/corpus.tsv.
Split rule (prereg section 4): held-out iff numeric_id mod 10 in {0,1,2}."""
import sys
def main():
    rows = []
    with open('corpus/corpus.tsv') as f:
        header = f.readline()
        for line in f:
            rows.append(line.rstrip('\n').split('\t'))
    train, held = [], []
    for p in rows:
        num = int(''.join(c for c in p[0] if c.isdigit()))
        (held if num % 10 in (0, 1, 2) else train).append(p)
    with open('cleanroom_train.tsv', 'w') as f:
        f.write('id\ttext\tclass\tprovenance\n')
        for p in train:
            f.write('\t'.join(p) + '\n')
    with open('cleanroom_heldout_blind.tsv', 'w') as f:
        f.write('id\ttext\n')
        for p in held:
            f.write(p[0] + '\t' + p[1] + '\n')
    print(f"train={len(train)} held={len(held)}")
if __name__ == '__main__':
    main()
