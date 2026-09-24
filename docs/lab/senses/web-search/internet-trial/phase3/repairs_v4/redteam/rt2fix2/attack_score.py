#!/usr/bin/env python3
"""Attacked-direction scorer. RT-A hits: oracle in {0,2} but got 1 (install invalid).
RT-B hits: oracle==2 got!=2, or oracle==1 got!=1 (reject/withhold valid)."""
import sys

def load(path, is_log):
    r = {}
    with open(path) as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if is_log:
                sp = line.rstrip('\n').split()
                if len(sp) >= 3:
                    r[sp[0]] = (sp[1], sp[2])
            else:
                if len(parts) >= 4:
                    r[parts[0]] = (parts[-1].strip(), parts[1])
    return r

def score(corpus, log, which):
    o = load(corpus, False)
    r = load(log, True)
    hits = []
    for i, (oracle, claim) in o.items():
        got, reason = r.get(i, ('?', '?'))
        if which == 'A':
            if oracle in ('0', '2') and got == '1':
                hits.append((i, oracle, got, reason, claim))
        else:
            if (oracle == '2' and got != '2') or (oracle == '1' and got != '1'):
                hits.append((i, oracle, got, reason, claim))
    print(f"RT-{which}: {len(hits)}/{len(o)} attacked-direction hits")
    for i, oracle, got, reason, claim in hits:
        print(f"  {i}: oracle={oracle} got={got}({reason}) | {claim[:60]}")
    return hits

if __name__ == '__main__':
    score(sys.argv[1], sys.argv[2], sys.argv[3])
