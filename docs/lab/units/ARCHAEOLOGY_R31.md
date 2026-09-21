# ARCHAEOLOGY VERDICT SHEET — R31 endogenous chunking

**Date:** 2026-09-21
**Verdict: RESURRECT** — the mechanism is fully recoverable and was never falsified.
**Status:** findings only; no prereg changes made. All numeric bars below remain PROPOSED for Micah's sign-off.

## Provenance

Micah's memory ("no chunking hurt it, so TNN choosing its own chunking is best") is confirmed
and now precisely specified. The work is **R31 "endogenous chunking"** (Adaptive Motif lineage,
frozen 2026-08-22/23), born from his 2026-08-21 correction of R30: *"R30's `token accuracy`
framing is wrong for TNN. TNN should choose its own chunking… should not drift toward
transformer/token/BPE assumptions."*

It was never superseded. Promotion was **denied by the native gate** (no `znc` compiler in that
runtime), not by evidence. H-02/H-03 remain PROVISIONAL; MATRIX.md marks the line
"Retained (shadow)." No document anywhere marks it abandoned. The wave-11 dead list does not
include chunking. The 2026-09-20 drop (`0fc255a3`) killed the R32 segmental *classifier*
machinery, not the chunking core. R32_HANDOFF: *"R31 should not be restarted. Its central
architecture decision is supported: raw episodic route + endogenous reversible chunks + active
grounded evidence."*

The Python originals were purged from the repo (`9da6e30b`, 19,457 deletions). They survive in
the Drive shadow archive, downloaded read-only (Drive authorization stayed read-only throughout)
to `/tmp/oldcode/shadow_tar/`. Recovered artifacts are preserved beside this sheet in
`archaeology_r31/` (shadow tarball, checksums, cleanroom contract, tournament/ablation/dose
evidence JSONs, the 1,148-line Zag spec, generation logs).

## The mechanism, precisely enough to reimplement

**Inputs:** raw microstate integer streams (alphabet 32) plus grounded consequence labels from
the learner's own experience. No VAD, phoneme, word, tokenizer, BPE, transcript, or next-token
objective. The hardcoding ledger pins: "Chunk boundaries: learned, TNN-recruited spans; no
VAD/word/phoneme boundaries supplied."

**Boundary signals (two, deliberately non-human):**
1. **Description-length recurrence** — `r31_compression_gain(n,seen) = (n-1)*seen-(n+3)`
   (verified verbatim in the recovered Zag source). Every span of length 2–8 is enumerated at
   every position, hashed, counted.
2. **Grounded consequence consistency** — spans gain utility when their historical consequences
   are predictively consistent; "no language/category name is supplied." Compression is
   deliberately down-weighted: *"compression is admissible but cannot dominate grounding."*

**Promotion rule** (recovered Python `ChunkBank.promote`): a span becomes a chunk iff
`seen ≥ 5 AND purity ≥ 0.34 AND utility > 0`, where
`utility = gain*0.02 + max(0, purity−0.2)*log1p(seen)*len(sp)`.
Candidates ranked by utility, capped at 700 chunks, stored longest-first.

**Segmentation:** greedy longest-match over recruited chunks; unmatched microstates fall back to
single-symbol literals (negative IDs), so *"information is not destroyed merely because the
current chunk vocabulary is weak."* Exact round-trip preserved.

**Dynamics** (recovered Zag source): split fires when
`use_count ≥ 3 AND conflict ≥ learned_conflict AND utility ≤ learned_utility_floor`;
merge fires when `pair_seen ≥ learned_pair_seen AND joint_gain − separate_regret ≥ learned_gain`.
*"Chunk boundaries are mutable hypotheses."* Support-gap recruitment: the teacher supplies only a
grounded whole experience; the learner recruits the largest unsupported raw span if it meets
learned min-support and beats the runner-up by a learned margin, else abstains (−1). Delayed
regret revises utilities; recurrent adjacent pairs propose a hierarchy layer.

**The anti-harm architecture:** a dual route — raw high-fidelity evidence runs alongside the
chunked route, trust weights shift by delayed downstream evidence. *"Chunking is never allowed
to erase evidence merely because it compresses well."*

**The winning cut signal:** `predictive_surprise` — boundaries at the 82nd percentile of the
learner's own sensory prediction error (transition surprise), 256-entry inventory.

## What the tests actually proved (all REFERENCE_ONLY — Python shadow, never natively executed)

- **Tournament** (8 arms, 5 seeds, 3,200 training units, 700 hidden tests × 8 conditions):
  predictive_surprise **0.7376** ≫ random_chunks 0.4988 ≈ fixed_window_4 0.4928 >
  MDL variants ~0.4715–0.4731 > **raw_micro (no chunking) 0.4489 — dead last**.
  This is the "no chunking hurt it" result Micah remembers. Honest nuance: the learner's own
  MDL chunkers did *not* beat fixed windows or random chunks, and the surprise winner won
  partly via giant spans (mean len 32.3) — a compression exploit the docs themselves
  **rejected** as a criterion.
- **Causal ablation** (3 learners × 9,000 episodes, 1,300 trials × 9 conditions, 6 seeds):
  raw_active hard grounding **0.9213** vs chunk_active **0.7533** vs dual_active **0.9209** —
  adding chunks cost nothing and gained ~85% compression; chunk-*only* hurt and was
  **rejected** ("compresses strongly, loses hidden grounding"). Dual also improved near-twin
  discrimination (0.8363 vs 0.8186).
- **Support-gap recruitment:** ~0.89–0.92 on the hard battery across seeds and 1–16 exposures.
  **Dose curve:** flat ~0.36–0.40 from 250 → 8000 — no dose effect, no degradation.
- **Adaptive Motif lineage:** 33,450 raw units → 2,789 motifs with exact round-trip; motifs
  crossed word boundaries, only ~14–30% aligned to known surface values — "not a hidden
  fixed tokenizer."

**Recorded verdict** (R31_FINAL_REPORT): *"Self-chunking is retained as a compression/indexing/
grounded-construction/memory route, but it must not erase or replace raw episodic evidence."*

## Why RESURRECT rather than SUPERSEDED

1. **Complete to reimplementation grade** — runnable Python plus the Zag spec with exact integer
   logic; cleanroom source contract passes (`no_transformer_tokenizer`, `endogenous_chunking`,
   `split_merge`, `support_gap`, `dual_route`).
2. **Never falsified.** Denied by infrastructure, not evidence.
3. **Nothing replaced it.** R32/R33 moved to other topics.
4. It directly instantiates this program's arm D (self-cut byte span + stable ID) and the
   predictive-surprise arm — with the giant-span exploit explicitly barred in prereg.

## Qualifications the prereg must carry

1. **Substrate gap:** the old work ran on synthetic 32-symbol acoustic microstate streams; this
   program needs byte streams of text/code. The mechanism generalizes (spans over discrete
   streams), but the promotion rule's *purity* term needs grounded consequence labels — the
   prereg must operationally define "grounded consequence" for text/code (e.g., recall success,
   downstream discrimination). Design gap, not a blocker.
2. **Old numbers don't transfer.** All evidence is REFERENCE_ONLY; native quantitative
   validation never happened. Re-run natively at 1x/10x — which is the plan anyway.
3. **Preregister the DUAL route, not chunk-only.** The old verdict already rejected chunk-only;
   raw matched dual on hard grounding, so chunks must earn their place as compression/indexing
   with the raw route intact.
4. **Bonus thread for the vocabulary arms:** R23 Python-era teaching experiments
   (`english_apprenticeship_inversion_experiment`, master-taught vs TNN-taught with "no English
   dictionary installed into child") are a direct ancestor of the taught-vocabulary arm. One
   Google Doc (`ghost#1`) matched "vocabulary" but needs the Docs skill to read — flagged,
   not blocking.

## Recommended next step

Proceed to preregistration with two resurrected arms: (a) the R31 dual-route endogenous
chunker (self-cut spans + stable IDs + literal fallback + split/merge + support-gap), and (b)
the predictive-surprise cut signal — both re-run natively on byte streams with "grounded
consequence" operationally defined for text/code, and the giant-span compression exploit
explicitly barred. Awaiting Micah's sign-off alongside the catalog's open items (numeric bars,
judgment-held vs force-pinned for taught words, V fairness checklist, frozen judgment
parameters).
