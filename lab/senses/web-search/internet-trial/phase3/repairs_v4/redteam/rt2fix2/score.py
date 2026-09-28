#!/usr/bin/env python3
"""Score r12 run logs against oracles. Usage: score.py <corpus.tsv> <run.log>
Corpus: id \t claim \t title \t evidence \t oracle(0/1/2). Log: id tag reason."""
import sys

def load_oracle(path):
    o = {}
    with open(path) as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 4:
                o[parts[0]] = parts[-1].strip()
    return o

def load_log(path):
    r = {}
    with open(path) as f:
        for line in f:
            parts = line.rstrip('\n').split()
            if len(parts) >= 3:
                r[parts[0]] = (parts[1], parts[2])
    return r

def main(corpus, log):
    o = load_oracle(corpus)
    r = load_log(log)
    hits = []
    for i, oracle in o.items():
        tag, reason = r.get(i, ('?', '?'))
        if tag != oracle:
            hits.append((i, oracle, tag, reason))
    n = len(o)
    print(f"{corpus} vs {log}: {n - len(hits)}/{n} correct, {len(hits)} mismatches")
    for i, oracle, tag, reason in hits:
        print(f"  {i}: oracle={oracle} got={tag}({reason})")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
