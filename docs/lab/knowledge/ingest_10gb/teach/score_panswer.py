#!/usr/bin/env python3
"""Score panswer responses with the frozen Phase-1A rules (SCORING.md).

Input: answers.tsv from gate_bin panswer (id \\t hits \\t key \\t resp_escaped)
Probes: baseline/KNOWLEDGE_PROBES.txt, REASONING_PROBES.txt (frozen).
Output: per-probe verdicts + summary. Implements SCORING.md normalization
and mechanical verdict exactly. Python is scoring glue; the answers came
from the pure-Zag panswer binary.
"""
import re
import sys

def normalize(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9]', ' ', s)
    return s.split()

def unescape(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            n = s[i+1]
            if n == 'n': out.append('\n'); i += 2
            elif n == 't': out.append('\t'); i += 2
            elif n == '\\': out.append('\\'); i += 2
            else: out.append(s[i]); i += 1
        else:
            out.append(s[i]); i += 1
    return ''.join(out)

WITHHOLD_SEQS = [
    ["do", "not", "know"], ["don", "t", "know"], ["no", "information"],
    ["cannot", "answer"], ["unable", "to", "answer"], ["unknown"],
]

def contains_seq(tokens, seq):
    if len(seq) > len(tokens):
        return False
    for i in range(len(tokens) - len(seq) + 1):
        if tokens[i:i+len(seq)] == seq:
            return True
    return False

def load_probes():
    probes = {}  # id -> (category, answers_list or None for withhold)
    base = '/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/baseline'
    for fn in ['KNOWLEDGE_PROBES.txt', 'REASONING_PROBES.txt']:
        with open(f'{base}/{fn}') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                parts = line.rstrip('\n').split('\t')
                pid, cat, q = parts[0], parts[1], parts[2]
                ans = parts[3] if len(parts) > 3 else ''
                if ans == '__WITHHOLD__':
                    probes[pid] = (cat, None)
                else:
                    keys = [k for k in ans.split(';') if k]
                    probes[pid] = (cat, keys)
    return probes

def main():
    answers_path = sys.argv[1]
    probes = load_probes()
    results = []
    with open(answers_path) as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            pid = parts[0]
            hits = int(parts[1]) if len(parts) > 1 else -1
            key = parts[2] if len(parts) > 2 else ''
            resp_esc = parts[3] if len(parts) > 3 else ''
            resp = unescape(resp_esc)
            if pid not in probes:
                continue
            cat, accept = probes[pid]
            tokens = normalize(resp)
            if accept is None:
                # withhold probe
                correct = any(contains_seq(tokens, ws) for ws in WITHHOLD_SEQS)
            else:
                correct = False
                for ak in accept:
                    ak_tokens = normalize(ak)
                    if ak_tokens and contains_seq(tokens, ak_tokens):
                        correct = True
                        break
            results.append((pid, cat, correct, hits, key, resp))
    # summary
    n = len(results)
    c = sum(1 for r in results if r[2])
    print(f"total: {n}, correct: {c} ({100*c/n:.1f}%)" if n else "no results")
    # by category
    cats = {}
    for pid, cat, correct, hits, key, resp in results:
        if cat not in cats:
            cats[cat] = [0, 0]
        cats[cat][1] += 1
        if correct:
            cats[cat][0] += 1
    for cat in sorted(cats):
        cc, nn = cats[cat]
        print(f"  {cat}: {cc}/{nn} ({100*cc/nn:.1f}%)")
    # write details
    with open('probe_results.tsv', 'w') as out:
        out.write("id\tcat\tverdict\thits\tkey\tresponse\n")
        for pid, cat, correct, hits, key, resp in results:
            v = "CORRECT" if correct else "INCORRECT"
            resp_one = resp.replace('\n', ' | ')[:200]
            out.write(f"{pid}\t{cat}\t{v}\t{hits}\t{key}\t{resp_one}\n")
    print("wrote probe_results.tsv")

if __name__ == '__main__':
    main()
