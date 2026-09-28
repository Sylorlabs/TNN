# PREREG — DECLINE INVESTIGATION: why does more hurt?

**Date:** 2026-09-22 · **Branch:** `tnn-native-lab` · **Engine lineage:** `delib_vol.zag`
**Question (Micah):** the volume curve peaked at 2 examples/concept (76%) then declined
to 50% at 32 examples. His standing intuition: more examples should help or plateau,
NEVER hurt. "Are they good examples? Examples shouldn't be the same thing — they should
all be different in their own ways."

This prereg is frozen BEFORE any new result. The volume curve (VOLUME_CURVE.md,
commit 291bbf75785b) is the prior; nothing below re-tunes against it.

## Hypotheses and kill bars

### H-D1 — the decline is a BAR ARTIFACT (fixed absolute bar × normalized prevalence)
VOLUME_CURVE.md §6 names the suspect: SCORE_BAR=500 is fixed while per-feature weight
w = prev·disc/1000 shrinks as prev = 1000·df_c/N_c normalizes by N. Test: replace the
weight rule with a volume-relative COUNT rule — WITHHOLD iff ≥3 matched features each
have distinctiveness ≥ 750 (no prevalence term at all). Same engine, same examples,
same 70 items, same deliberation order.
- **KILL BAR:** H-D1 is KILLED if the count-rule variant still shows a significant
  decline from r2 to r32 (McNemar paired test on the same 70 items, p < 0.05 in the
  declining direction). If the count rule restores a non-decreasing curve r2→r32,
  H-D1 SURVIVES and the lead's monotonic intuition is vindicated.

### H-D2 — the decline is an EXAMPLE-QUALITY artifact (template redundancy)
The 224 example utterances were spot-checked for naturalness and test-overlap, never
for quality or diversity. Micah's charge: good examples are "all different in their
own ways." Test BOTH directions at fixed N with the ORIGINAL engine and bar:
- O-diverse: examples ordered by greedy max-novelty (each next example maximizes
  new unigram/bigram features vs all previous).
- O-redundant: examples ordered by greedy min-novelty (most template-similar first).
- O-proto ("best-first"): prototypicality = mean pairwise feature-overlap with all
  other same-concept examples, descending. O-outlier ("worst-first"): ascending.
  Prototypicality is computed WITHOUT touching test items (answer-key-free).
- **KILL BAR:** H-D2 is KILLED if O-diverse shows an equal-or-steeper decline than
  O-redundant from r2 to r32 AND O-diverse's peak ≤ O-redundant's peak. If O-diverse
  removes or substantially shrinks the decline, H-D2 SURVIVES.

### H-D3 — the decline is DISTINCTIVENESS DILUTION (DISC_BAR=750 fails as profiles overlap)
As all 7 profiles grow with N, inter-concept feature overlap grows and
disc = 1000·df_c/(df_c+df_o) falls; the DISC_BAR≥750 gate starves. Ablations:
- B2: SCORE-only rule (drop the DISC_BAR gate; WITHHOLD iff score ≥ 500).
- B3: DISC-only rule (drop SCORE_BAR; WITHHOLD iff bestd ≥ 750).
- **KILL BAR:** H-D3 is KILLED if B2 shows the same decline shape as baseline
  (r2→r32 significant decline). Mechanism attribution: if B3 restores monotonicity
  and B2 does not, the SCORE_BAR×prevalence interaction (H-D1's suspect) is the
  mechanism; if B2 restores it and B3 does not, distinctiveness dilution (H-D3) is.

### H-D4 — implicature is a REPRESENTATION failure (front-end can't see indirectness)
Implicature peaked at 3/10 at every volume. Suspect: unigrams/bigrams share surface
form between indirect requests and plain statements. Test richer front-ends on the
SAME engine skeleton, same bar, same examples:
- F1: current front-end (control — reproduces the 3/10).
- F2: F1 + closed-class pragmatic frame features (fixed TYPES, counts learned from
  examples — like tokenization, not hand-specified knowledge): subject pronoun class
  (i/you/he/she/it/they/we), stative-duration frames (has/have been, still, again,
  since), negation/problem frames (n't/not/no/never, out of, empty), second-person
  reference (you/your), it-is-locative frames.
- F3: F2 + slot-abstracted frames (e.g. "it is ADJ", "your NOUN" with the content
  word abstracted to its slot — tests whether frame transfer beats lexical overlap).
- **KILL BAR:** H-D4 is KILLED if NO richer front-end lifts the implicature family
  above 5/10 (strictly above the 3/10 baseline by ≥3 items). If killed, the report
  says so honestly: the failure is deeper than representation. If a front-end lifts
  it, the report names exactly which frame features transferred (evidence, not story).

## Audit (preregistered metrics, computed before the ordering experiments)

Per concept file: distinct-unigram ratio, distinct-bigram ratio, template-adherence
fraction (sarcasm: praise-word + [—:.] + misfortune; others: crew-defined after
reading), marginal feature-novelty curve (new features contributed by example k at
the moment it is added), cross-concept shared-vocabulary growth with N. The audit
is analysis (Python, like analysis_twin.py) — not part of the mechanism.

## Method (Micah's laws)

- Same 70-item c70 set, same b12 false/true control legs. Pure Zag, zero RNG.
- 3/3 byte-identical reruns per cell, SHA256 per file (scored_evidence/).
- Answer-key-free: example orderings and front-end types are fixed WITHOUT using
  test items. The true/falsehood legs must hold (12/12) in every variant — any
  variant that breaks them is reported as broken, not as a win.
- When in doubt, test both: diverse AND redundant, absolute AND relative bars.
- The corrected curve (if the artifact account wins) is presented as the curve
  under good diverse examples + a sane bar — not as a replacement of the honest
  original, which stands as what the original bar measured.
