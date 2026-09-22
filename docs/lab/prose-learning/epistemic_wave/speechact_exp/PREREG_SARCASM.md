# WHY-SARCASM WAVE — Preregistration (RDTDT: Review → Debate → Test)

**Date:** 2026-09-22
**Question (Micah):** "why does TNN struggle with sarcasm more?"
**Observation:** speech-act experiment (commit fabb003e263c). With speech-act
knowledge installed, weird-English scores by family: counterfactual 9/10,
hypothetical 5/10, poetry 5/10, implicature 5/10, sarcasm 3/10, analogy 3/10.
Facts are easy (12/12 falsehoods held). Sarcasm is the hardest thing TNN does.
**Volume data (early, VOLUME_CURVE.md):** sarcasm's learned profile peaks at
2 examples (6/10) then DISSOLVES — 0/10 by 16 examples. Counterfactual stays
at ceiling once reached; hypothetical saturates at 1. Sarcasm saturates LOWER
and then collapses. This wave explains why.

**Method law:** same deliberation machinery across conditions; only the tested
factor varies. Pure Zag, zero RNG, deterministic, 3 byte-identical reps per
cell, SHA256-verified. Answer-key-free items (ID + utterance only; context/
speaker fields are INPUTS to deliberate over, not answer keys).

---

## H1 — LAYERING

**Steelman:** Sarcasm forces three simultaneous readings — the literal meaning,
the intended (opposite) meaning, and the speaker's attitude. A deliberation
that resolves to a single ENDORSE/WITHHOLD status cannot hold all three; the
layers interfere, and the literal reading (plausible, endorsable) wins ties.

**Test:** `layered` mode computes the three layers explicitly (LITerality,
ATTitude, SITuation valence) and withholds on layer mismatch, vs `base`
single-status deliberation, on the same 10 bare-sarcasm items (s_bare.txt).

**KILL BAR:** H1 survives iff `layered` beats `base` on s_bare by ≥3 items
(i.e. ≥6/10 vs the 3/10 baseline). If the improvement is <2 items, the layers
were never interfering — H1 is KILLED.

## H2 — TRUTH-MACHINERY CONFLICT

**Steelman:** TNN's falsehood machinery is strong (12/12) and it fires FIRST
(step 1 of deliberation, before sarcasm markers are weighed). On sarcastic
items with false literals it withholds for the WRONG reason, so the system
appears to handle sarcasm without ever learning it; the strength becomes the
obstacle. On plausible-literal sarcasm the machinery contributes nothing and
the weak markers decide alone.

**Tests:** (a) `notruth` mode (known-false/absurdity/known-true checks
disabled) vs `base` on s_bare.txt. (b) `base` on s_litfalse.txt — 10 sarcastic
items whose literals are ALSO known falsehoods — with instrumented reason
codes (which step decided?).

**KILL BAR:** H2's "fires first and blocks" claim is KILLED iff `notruth`
changes s_bare accuracy by <2 items AND <50% of s_litfalse withholds carry
reason F. It SURVIVES as a mechanism (not a block) iff ≥50% of s_litfalse
withholds are decided by the truth-machinery step — the system doing sarcasm's
work for the wrong reason.

## H3 — MISSING CUES

**Steelman:** In text, sarcasm leans on prosody and shared context; its
markers are pragmatic and weak. Hypothetical ("what if", "suppose") and
counterfactual ("if I had", "would have") have DEDICATED LEXICAL FRAMES —
that is why hypothetical saturates at 1 example and counterfactual never
dissolves. Sarcasm has no dedicated frame; "great" also praises genuinely.

**Tests:** (a) `marked` mode adds explicit lexical sarcasm markers ("yeah
right", "as if", "oh please", "give me a break", "sure, sure", "not!") and
runs on s_marked.txt (10 NEW sarcastic items built on those markers) vs
`base` on the same items. (b) `ctx` mode: the same utterances WITH the
situational context supplied as a third field (s_ctx.txt) vs without
(s_ctx_utt.txt).

**KILL BAR:** H3 is KILLED iff explicit markers do NOT reach ≥8/10 on
s_marked (improvement <2 items over base) AND context improves s_ctx by
<2 items. H3 SURVIVES iff either intervention reaches its bar (markers
≥8/10, or context improves ≥3 items).

## H4 — NO SPEAKER MODEL

**Steelman:** Sarcasm requires modeling the speaker's attitude (contempt,
frustration, playfulness) — theory of mind. TNN judges utterances; it has no
model of the utterer. "Wonderful, my flight is delayed" is sarcastic from
ALIX (who hates delays) and genuine from BRAM (who finds silver linings) —
the utterance alone cannot decide.

**Test:** `speaker` mode installs a speaker-attitude knowledge file
(speakers.txt: each speaker's known dislikes) and gates the sarcasm inference
on speaker–utterance mismatch. Items s_spk.txt (ID|speaker|utterance): 5
sarcastic-from-ALIX (WITHHOLD) + 5 genuine-from-BRAM (ENDORSE). Control:
`base` on the same 10 utterances without speaker fields (s_spk_utt.txt).

**KILL BAR:** H4 is KILLED iff `speaker` improves over the `base` control by
<2 items. H4 SURVIVES iff `speaker` wins by ≥3 items (≥8/10 while base stays
≤5/10) — the speaker model is doing work the utterance alone cannot.

## H5 — INVERSION OPACITY

**Steelman:** Sarcastic "X" means not-X. The mapping from utterance to
intended meaning passes through an extra inversion step no other speech act
needs — and no surface-feature learner can learn not-X from X-shaped
features. This predicts the volume collapse: sarcastic and genuine utterances
SHARE surface features ("great", "flat tire"), so more examples dilute
distinctiveness until the profile dissolves (r16: 0/10). Counterfactuals have
dedicated frames and never dissolve.

**Tests:** (a) Discrimination: `base` on s_bare.txt (10 sarcastic, WITHHOLD)
vs s_genuine.txt (10 genuine positive-about-negative, ENDORSE) — can any
surface marker separate them? (b) `marked` on both sets. (c) `inv` mode
reports the inferred speaker attitude (POS/NEG) alongside the verdict;
attitude accuracy scored on s_marked (all NEG) and s_genuine (all POS).

**KILL BAR:** H5 is KILLED iff some marker set scores ≥8/10 on the sarcastic
set AND ≥8/10 on the genuine set simultaneously — surface features suffice
for detection and attitude. H5 SURVIVES iff no marker set achieves this: the
distinguishing information is not in the utterance's surface features, so the
inversion has nothing to work from. The volume-collapse data (sarcasm
dissolves, counterfactual doesn't) counts as supporting evidence either way
and is cited, not double-counted.

---

## Test matrix

| # | Mode | Items | N | Decides |
|---|---|---|---|---|
| 1 | base | c70.txt (reproduction) | 70 | engine correctness: must match PoC arm2 byte-identically |
| 2 | base | s_bare.txt | 10 | baseline (expect 3/10) |
| 3 | notruth | s_bare.txt | 10 | H2a |
| 4 | base | s_litfalse.txt | 10 | H2b (reason codes) |
| 5 | layered | s_bare.txt | 10 | H1 |
| 6 | layered | s_genuine.txt | 10 | H1/H5 (over-fire check) |
| 7 | base | s_genuine.txt | 10 | H5a (discrimination) |
| 8 | marked | s_marked.txt | 10 | H3a |
| 9 | base | s_marked.txt | 10 | H3a control |
| 10 | marked | s_genuine.txt | 10 | H5b |
| 11 | speaker | s_spk.txt (+speakers.txt) | 10 | H4 |
| 12 | base | s_spk_utt.txt | 10 | H4 control |
| 13 | ctx | s_ctx.txt | 10 | H3b/H5 (verdict + attitude) |
| 14 | base | s_ctx_utt.txt | 10 | H3b/H5 control |
| 15 | inv | s_marked.txt | 10 | H5c (attitude) |
| 16 | inv | s_genuine.txt | 10 | H5c (attitude) |

3 reps per cell. Correct: sarcastic → WITHHOLD; genuine → ENDORSE;
attitude: sarcastic → NEG, genuine → POS.

## Second debate (RDTDT)

After results: re-debate. Hypotheses that survive are refined against each
other (e.g. H3 vs H5: are weak cues and inversion opacity the same problem?
H2's "blocking" vs "doing the work" distinction). Killed hypotheses stay
killed. Final ranking + the concrete answer: why is sarcasm harder, and what
would fix it → WHY_SARCASM.md.
