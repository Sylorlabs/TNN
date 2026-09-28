#!/usr/bin/env python3
"""Verify the I/K-IM bars for implicature context (delib_impl2.zag).
I1: >= 10/12 on impl_ctx.txt (expected: odd=REQUEST with right target,
    even=LITERAL).
I2: all 6 same-utterance pairs resolve DIFFERENTLY via the context model.
K-IM1: no battery utterance string (or >12-char substring) in
    delib_impl2.zag; every REQUEST cites the matched situation slot + goal.
K-IM2 is the runner's determinism check.
Exits nonzero on any failure.
"""
import re, sys

D = "/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp/"
src = open(D + "delib_impl2.zag").read()
fails = []

items = {}
for ln in open(D + "impl_ctx.txt"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"):
        continue
    i, spk, sit, goal, utt = ln.split("|")
    items[i] = (spk, sit, goal, utt)

# expected resolutions (frozen in the prereg)
exp = {
    "I01": ("REQUEST", "salt"), "I02": ("LITERAL", None),
    "I03": ("REQUEST", "heater"), "I04": ("LITERAL", None),
    "I05": ("REQUEST", "trash"), "I06": ("LITERAL", None),
    "I07": ("REQUEST", "meeting"), "I08": ("LITERAL", None),
    "I09": ("REQUEST", "package"), "I10": ("LITERAL", None),
    "I11": ("REQUEST", "baby"), "I12": ("LITERAL", None),
}

out = {}
for ln in open(D + "scored_evidence/impl_ctx_rep1.txt"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("SUMMARY") or ln.startswith("#"):
        continue
    p = ln.split("|")
    out[p[0]] = p

score = 0
for i, (ekind, etarget) in exp.items():
    p = out.get(i)
    if not p:
        fails.append(f"I1: no output for {i}")
        continue
    okind, otarget = p[1], (p[2] if len(p) > 2 else None)
    good = (okind == ekind) and (ekind == "LITERAL" or otarget == etarget)
    if good:
        score += 1
    else:
        fails.append(f"I1: {i} got {'|'.join(p[1:3])}, expected {ekind}/{etarget}")
    # every REQUEST must cite slot + goal
    if okind == "REQUEST" and (len(p) < 5 or ":" not in p[3]):
        fails.append(f"K-IM1: {i} REQUEST lacks slot citation")

if score < 10:
    fails.append(f"I1: score {score}/12 < 10")

# I2: same-utterance pairs resolve differently
pairs = [("I01", "I02"), ("I03", "I04"), ("I05", "I06"),
         ("I07", "I08"), ("I09", "I10"), ("I11", "I12")]
for a, b in pairs:
    if items[a][3] != items[b][3]:
        fails.append(f"I2: {a}/{b} are not the same utterance")
    ka, kb = out[a][1], out[b][1]
    if ka == kb:
        fails.append(f"I2: pair {a}/{b} resolved the same ({ka}) — pattern matching?")

# K-IM1: no utterance strings in the binary source
lits = re.findall(r'"([^"]+)"', src)
for i, (spk, sit, goal, utt) in items.items():
    u = utt
    if u in src:
        fails.append(f"K-IM1: full utterance of {i} in source")
    for k in range(0, len(u) - 12):
        sub = u[k:k + 13]
        for lit in lits:
            if sub.lower() in lit.lower():
                fails.append(f"K-IM1: >12-char utterance substring in source literal: {sub!r}")
                break

if fails:
    print("FAIL")
    for f in fails:
        print(" ", f)
    sys.exit(1)
print(f"OK I1 ({score}/12) + I2 (6/6 pairs discriminate) + K-IM1 (no hardcode)")
