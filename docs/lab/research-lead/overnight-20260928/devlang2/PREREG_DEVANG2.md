# PREREG_DEVANG2: Developmental Semantic Language Retry

**Status:** FROZEN. Committed before any implementation.
**Date:** 2026-09-30.
**Worker:** DEVANG2 (Developmental Semantic Language Retry).
**Owned path:** `docs/lab/research-lead/overnight-20260928/devlang2/`

## 1. Mission

Retry of DEVANG1 (BUILD-FAIL, d0817af17). The DEVANG1 design is sound;
the implementation had memory-safety defects. This wave re-freezes the
same research design with a corrected implementation.

**Reference:** DEVANG1 prereg (`docs/lab/research-lead/overnight-20260928/devlang/PREREG_DEVANG1.md`,
commit e23627a40) defines the full world design, learner, controls, and
kill bars K1-K12. This prereg incorporates that document by reference.
All sections 1-8 of PREREG_DEVANG1 apply unchanged, EXCEPT for the
implementation fixes listed in section 2 below.

**Do NOT create SEG10.** SEG is mature infrastructure.

## 2. Implementation fixes (vs DEVANG1)

The DEVANG1 BUILD-FAIL root causes were:

1. **Lexicon string field overflow.** 8-byte string field vs 9-12 char
   segments. `lex_add` wrote past the field, corrupting the length byte
   and causing `lex_find` mismatches. Fix: 24-byte lexicon entries
   (16 bytes string, 1 byte len at offset 16, 3 bytes pad, 4 bytes
   count at offset 20). Max segment length capped at 16 (the utterance
   buffer size). Bounds check: `lex_add` rejects len > 16.

2. **Suspected memory corruption from layout changes.** Fix: single
   clean layout computed before coding; no mid-implementation layout
   changes. All buffer accesses bounds-checked against documented sizes.

3. **K1 timing.** Prereg requires K1 measured at end of phase 1 (t=60).
   DEVANG1 measured after all 100 episodes. Fix: snapshot lexicon at
   t=60 and evaluate K1 from the snapshot.

The segmentation scoring deviation (length-averaged vs sum-of-logs)
disclosed in DEVANG1 is RETAINED. It is a mechanism bug fix, not a bar
change. Kill bars unchanged.

## 3. Memory layout (fixed before coding)

Learner W buffer:
- 0..2704: bigram[26][26] i32 (2704 bytes)
- 2704..2720: nlex (i32 at 2704), padding to 2720
- 2720..4256: lexicon 64 x 24B (16 str, len at +16, count at +20)
- 4256..6304: ground 64 x 8 x i32 (2048 bytes)
- 6304..6560: neg_viol[64] i32, neg_tot[64] i32 (512 bytes)
- 6560..6816: cmp_ok[64] i32, cmp_tot[64] i32 (512 bytes)
- 6816..6880: k1 snapshot (10 x i32 hit flags, 40 bytes), padding
Total: 6880 bytes.

Lexicon entry li: base=2720+li*24. String bytes 0..15, len at 16,
count (i32) at 20. Invariant: 0 <= len <= 16.

Episode buffer: 64 bytes per episode (unchanged from DEVANG1):
- 0..36: objects (9 x i32)
- 36..40: ulen (i32)
- 40..44: target (i32)
- 44..48: template (i32)
- 48..64: utt bytes (16)

## 4. Kill bars (unchanged from DEVANG1)

- K1 (lexicon discovery): >= 8 of the 10 phase-1 true words present as
  exact lexicon entries at end of phase 1 (t=60, from snapshot).
- K2 (DIRECT novel): >= 5/6 correct.
- K3 (NEG novel): >= 2/3 correct.
- K4 (REL novel): >= 2/3 correct.
- K5 (SYN novel): >= 2/3 correct.
- K6 (SIZE novel): >= 2/3 correct.
- K7 (3-WAY novel): >= 1/2 correct.
- K8 (beats controls): learner test accuracy exceeds best control by
  >= 15 percentage points.
- K9 (new vocab acquisition): >= 7/10 correct on last 10 phase-2
  training episodes.
- K10 (true online, governance): code audit confirms strictly sequential
  processing; no structure built from future data.
- K11 (no future leakage in segmentation, governance): bigram counts
  used to segment episode t exclude episode t.
- K12 (determinism): 3/3 byte-identical outputs.

**Verdict rule:** BUILD-PASS requires K1, K8, K10, K11, K12 plus at
least 4 of {K2..K7, K9}. Otherwise BUILD-FAIL.

## 5. Expected classification

Developmental L2 structural learning (pipeline integration). NOT L3.
The composition skeleton is researcher-designed; segment meanings,
negator flag, and comparative flag are learned.

## 6. Determinism and purity

- Seeded LCG; no wall-clock; no ASLR-dependent output.
- Pure Zag only. No Python at any stage.
- No em dashes in documentation.
- 3/3 byte-identical runs required (K12).

## 7. Commits

- This prereg committed ALONE before any .zag implementation.
- Implementation + raw + result committed separately.
- Owned paths only (`docs/lab/research-lead/overnight-20260928/devlang2/`).
- Local commits only.
