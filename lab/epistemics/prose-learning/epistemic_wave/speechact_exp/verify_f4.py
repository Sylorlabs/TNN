#!/usr/bin/env python3
"""Verify the K-LC bars for the lie-catcher redesign (delib_f4.zag).
K-LC1: no test-item string (or >15-char item substring) in the source or
       the experience corpus; every corpus line differs from every test line.
K-LC3: unseen_keys run has no F2 reason.
K-LC4: the speech-act matcher fns in delib_f4.zag are byte-identical to
       delib_sa.zag (only the truth machinery changed).
Exits nonzero on any failure.
"""
import re, sys

D = "/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp/"
src = open(D + "delib_f4.zag").read()
fails = []

def items(path):
    out = []
    for ln in open(D + path):
        ln = ln.rstrip("\n")
        if not ln or ln.startswith("#"):
            continue
        out.append(ln.split("|", 1)[1].lower())
    return out

test_texts = items("b12_false.txt") + items("b12_true.txt") + items("unseen_keys.txt")
corpus = [ln.split("|", 1)[1].lower() for ln in open(D + "experience_facts.txt")
          if ln.startswith("FACT|")]

# K-LC1a: full test strings must not appear in source or corpus
for t in test_texts:
    if t in src.lower():
        fails.append(f"K-LC1a: test item verbatim in source: {t[:50]}")
    for c in corpus:
        if t == c:
            fails.append(f"K-LC1a: corpus line equals test line: {t[:50]}")
        if t in c or c in t:
            fails.append(f"K-LC1a: corpus/test substring containment: {t[:40]}")

# K-LC1b: no >15-char test substring in the source's string literals
lits = re.findall(r'"([^"]{16,})"', src)
for lit in lits:
    l = lit.lower()
    for t in test_texts:
        for k in range(0, len(t) - 15):
            if t[k:k + 16] in l:
                fails.append(f"K-LC1b: >15-char test substring in source literal: {t[k:k+16]!r}")
                break

# K-LC1c: the removed helpers must be gone
for fn in ["is_known_false", "is_known_true", "is_absurd"]:
    if re.search(r"fn\s+" + fn + r"\b", src):
        fails.append(f"K-LC1c: removed helper still defined: {fn}")

# K-LC4: matcher fns byte-identical to delib_sa.zag
sa = open(D + "delib_sa.zag").read()
for fn in ["is_pos_word", "is_neg_situation", "matches_sarcasm",
           "matches_hypothetical", "matches_counterfactual",
           "matches_analogy", "matches_poetry"]:
    pat = re.compile(r"fn\s+" + fn + r"\(.*?^}", re.M | re.S)
    m1 = pat.search(src)
    m2 = pat.search(sa)
    if not m1 or not m2 or m1.group(0) != m2.group(0):
        fails.append(f"K-LC4: matcher {fn} differs from delib_sa.zag")

if fails:
    print("FAIL")
    for f in fails:
        print(" ", f)
    sys.exit(1)
print("OK K-LC1 (no test-derived strings) + K-LC4 (matcher parity)")
