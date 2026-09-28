#!/usr/bin/env python3
"""Verify the A2/K-AT1 bars for learned attitudes (delib_att.zag).
A2: no static dislike list anywhere in the build (no find_speaker_blob,
    no ';'-separated dislike blob format, none of the old dislike words
    as speaker knowledge).
K-AT1: every attitude count cites >=1 episode line in attitude_history.txt;
    no episode utterance equals any test utterance; the attitude math
    (ALIX 5/6 sarc -> NEG, BRAM 1/6 sarc -> POS) is recomputed independently.
Exits nonzero on any failure.
"""
import sys

D = "/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp/"
src = open(D + "delib_att.zag").read()
# strip comment lines: mentions documenting the removal are fine; only
# functional remnants (definitions/calls) count.
code = "\n".join(ln for ln in src.split("\n") if not ln.lstrip().startswith("//"))
fails = []

# A2: simulated dislike-list remnants
for pat in ["find_speaker_blob", "dislike", "blob"]:
    if pat in code:
        fails.append(f"A2: simulated-input remnant in source: {pat!r}")
# old speakers.txt blob lines must not be loadable: no ';' parsing anywhere
if '";"' in src or "';'" in src:
    fails.append("A2: semicolon-blob parsing present")

# parse history
eps = []
for ln in open(D + "attitude_history.txt"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"):
        continue
    parts = ln.split("|")
    assert parts[0] == "EP" and len(parts) == 5, ln
    eps.append(parts)

counts = {}
for _, spk, sit, utt, aft in eps:
    s, g = counts.get(spk, (0, 0))
    if aft == "sarcastic":
        s += 1
    else:
        g += 1
    counts[spk] = (s, g)

def att(s, g):
    n = s + g
    if n < 4:
        return "UNK"
    if s * 10 >= n * 6:
        return "NEG"
    if s * 10 <= n * 4:
        return "POS"
    return "UNK"

print("attitude audit (each count cites episode lines):")
for spk, (s, g) in sorted(counts.items()):
    a = att(s, g)
    cites = [e[0] + "/" + e[3][:30] for e in eps if e[1] == spk]
    print(f"  {spk}: sarc={s} gen={g} -> {a}  ({len(cites)} episodes)")
    if len(cites) < 4:
        fails.append(f"K-AT1: {spk} has <4 episodes")

if att(*counts.get("ALIX", (0, 0))) != "NEG":
    fails.append("K-AT1: ALIX attitude is not NEG")
if att(*counts.get("BRAM", (0, 0))) != "POS":
    fails.append("K-AT1: BRAM attitude is not POS")

# K-AT1: no episode utterance equals any test utterance
tests = set()
for f in ["s_spk.txt", "s_spk_utt.txt"]:
    for ln in open(D + f):
        ln = ln.rstrip("\n")
        if ln and not ln.startswith("#"):
            tests.add(ln.split("|")[-1].strip())
for _, spk, sit, utt, aft in eps:
    if utt.strip() in tests:
        fails.append(f"K-AT1: history utterance shared with test battery: {utt[:40]}")

if fails:
    print("FAIL")
    for f in fails:
        print(" ", f)
    sys.exit(1)
print("OK A2 (no simulation) + K-AT1 (audit/leakage)")
