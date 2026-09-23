#!/usr/bin/env python3
"""Byte-exact mirror of dialogue.zag's keyword pipeline for WE-09 analysis.

Mirrors: tokenize (alnum runs, lowercase), is_stop, stem_inplace
(first-match-wins, single pass), keyword extraction (dedup + insertion sort
by interned id -- order irrelevant for Jaccard), jscore cross-multiplied
Jaccard, retrieve (best fid, tie -> lower fid).
"""
import sys

STOP = """the an of in is are was were be been what which that this these those
it its do does did have has had there and or to for with at by from as on
how many much when where s""".split()

def ends_with(b, suf):
    return len(b) >= len(suf) and b.endswith(suf)

def stem_inplace(w):
    b = w
    n = len(b)
    if ends_with(b, "ies"):
        return b[:-3] + "y"
    if ends_with(b, "ication"):
        return b[:-7] + "ish"
    if ends_with(b, "ished"):
        return b[:-5] + "ish"
    if ends_with(b, "ic") and n > 5:
        return b[:-2]
    if ends_with(b, "ed") and n > 4:
        return b[:-2]
    if ends_with(b, "ches"):
        return b[:-2]
    if ends_with(b, "shes"):
        return b[:-2]
    if ends_with(b, "sses"):
        return b[:-2]
    if ends_with(b, "xes"):
        return b[:-2]
    if ends_with(b, "zes"):
        return b[:-2]
    if ends_with(b, "s") and n > 3 and not ends_with(b, "ss"):
        return b[:-1]
    return b

def tokenize(s):
    toks, cur = [], []
    for ch in s.lower():
        if ch.isalnum():
            cur.append(ch)
        else:
            if cur:
                toks.append("".join(cur)); cur = []
    if cur:
        toks.append("".join(cur))
    return toks

def digit_val(t):
    # digit_val: pure digit runs; mirror keeps it simple (values aren't keywords)
    return int(t) if t.isdigit() else -1

NUMWORDS = {}  # number-words aren't keywords either (cls=2 -> value only)

def keywords(sentence):
    kids = []
    seen = set()
    for t in tokenize(sentence):
        if digit_val(t) >= 0:
            continue
        if t in NUMWORDS:
            continue
        if t in STOP:
            continue
        s = stem_inplace(t)
        if s not in seen:
            seen.add(s)
            kids.append(s)
    return sorted(kids)

def jscore(q, f):
    qs, fs = set(q), set(f)
    inter = len(qs & fs)
    union = len(qs | fs)
    return inter, union

def main():
    kb = []
    with open(sys.argv[1]) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            fid = int(parts[0])
            text = parts[-1]
            kb.append((fid, text, keywords(text)))
    queries = sys.argv[2:]
    for q in queries:
        qk = keywords(q)
        print(f"Q: {q}")
        print(f"  kw: {qk}")
        scored = []
        for fid, text, fk in kb:
            inter, union = jscore(qk, fk)
            scored.append((fid, text, fk, inter, union))
        scored.sort(key=lambda r: (-(r[3] / r[4] if r[4] else 0), r[0]))
        for fid, text, fk, inter, union in scored[:6]:
            mark = " <-- WINNER" if fid == scored[0][0] else ""
            print(f"  fid {fid}: {inter}/{union} = {inter/union if union else 0:.4f} :: {text}{mark}")
            print(f"           kw: {fk}")
        print()

if __name__ == "__main__":
    main()
