# PREREG_DEVANG2 (wave-20261001-1421pdt): DEVANG1 Crash-Fix Retry with Cold-Start Repair

**Status:** DRAFT. Not yet frozen. The coordinator commits this file ALONE
before any .zag implementation exists.
**Date:** 2026-10-01.
**Wave:** wave-20261001-1421pdt.
**Owned path:** `docs/lab/rsi/runs/wave-20261001-1421pdt/devang2/`

## Disambiguation

An earlier artifact with the same name exists:
`docs/lab/research-lead/overnight-20260928/devlang2/` (DEVANG2-overnight,
frozen commit `402e53d32`, implementation commit `153e2af8e`). That
artifact was a crash-fix-only retry of DEVANG1 and BUILD-FAIL'd on
mechanism (13/20 vs C2 fixed-width 17/20). Commit-order independently
verified via git: the prereg commit (402e53d32, "frozen before
implementation", 2026-09-30 05:15 UTC) is an ancestor of the
implementation commit (153e2af8e); prereg-order governance PASS for that
artifact. This document defines a
separate, narrower retry in the current wave: the DEVANG1 crash fix plus
exactly ONE mechanism change (cold-start segmentation repair, section 4).
It does NOT adopt the DEVANG3 two-pass redesign (V3 TP segmentation plus
lexicon-reuse repair, `docs/lab/research-lead/overnight-20260928/devang3/`,
BUILD-FAIL close at 16/20); that redesign line continues separately.

## 1. Frozen diagnosis of the DEVANG1 crash (one paragraph, cited)

DEVANG1 (`docs/lab/research-lead/overnight-20260928/devlang/PREREG_DEVANG1.md`,
frozen commit `e23627a40`; result `RESULT_DEVANG1.md`) never produced
output: the training loop panicked with "slice index out of bounds" at
points varying with code edits (during learner state allocation, at t=0
after segmentation and lexicon insertion during `interpret`/`learn_update`,
and at t=31 in an earlier version). The documented chain was an 8-byte
lexicon string field versus 9+ character segments, so `lex_add` wrote past
the field, corrupted the length byte, broke `lex_find` matching
(`nlex` grew to 31 after 31 episodes instead of ~8), and the subsequent
layout expansion to 24-byte entries introduced new out-of-bounds
accesses; the root cause was never isolated (suspected memory corruption
from the lexicon layout changes or a buffer overflow in the
segmentation/grounding code), the K1-timing deviation (measured after
100 training episodes instead of at t=60) was disclosed but unfixed, and
the build was therefore not salvageable without rework. Verdict:
**BUILD-FAIL** (no kill bar measurable).

## 2. Retry hypothesis

The DEVANG1 research design (raw unsegmented character stream, strictly
online bigram DP segmentation, grounded lexicon, learned negator and
comparative flags, fixed 100-train/20-test seeded world, controls
C1/C2/C3) is sound; only the implementation was memory-unsafe, and the
mechanism has one documented initialization flaw: with zero bigram counts
at t=0 every segmentation scores equally and the DP defaults to a single
whole-utterance segment, poisoning the lexicon with 9-character
pseudo-words (DEVANG2-overnight observed `nseg=1` early and K1 3/10;
the segmentation redesign validated the cold-start fix "single
characters at t=0, no lexicon poisoning"). Hypothesis: fixing the crash
and adding a minimal cold-start tie-break (single-character segments
while total bigram observations equal zero, section 4) is sufficient for
the frozen DEVANG1 kill bars to become measurable and for word discovery
(K1) to recover. A BUILD-FAIL on mechanism after this fix would be
informative: it would corroborate that the bottleneck is the scoring
function itself rather than initialization, consistent with the
DEVANG3 TP-redesign line.

## 3. Design (inherited from DEVANG1, unchanged except section 4)

World design, vocabulary, episode templates, phases (60 phase-1, 40
phase-2, 20 test with the same explicit hold-outs), seeded LCG scene
generation (seed `123456789`, same generator as DEVANG1 and
DEVANG2-overnight), online protocol (episode t segmented and interpreted
using only state from episodes 0..t-1; bigram/lexicon/grounding updates
AFTER segmentation/interpretation; test episodes frozen), grounding
(`primary` via argmax over 8 feature-values, valid only if lexicon count
>= 2), generic negator detection (4.5 of DEVANG1 prereg, not hardcoded to
"not"), generic comparative detection (4.6 of DEVANG1 prereg, not
hardcoded to "biger"), interpretation passes, and controls C1 (whole
utterance memorization), C2 (fixed-width-3 segmentation), C3 (substring
memory) are identical to the frozen DEVANG1 prereg. The scoring deviation
disclosed in DEVANG1 (length-averaged log bigram score minus boundary
cost, versus the prereg's sum formulation) is RETAINED as the baseline
to avoid a second mechanism change; it is a disclosed implementation
choice, not a bar change. K1 is measured at t=60 via an in-loop lexicon
snapshot (the DEVANG1 measurement deviation is corrected; bars unchanged).

## 4. Changes relative to DEVANG1 (crash fix plus ONE mechanism change)

### 4.1 Crash-fix bundle (implementation corrections, no bar changes)

1. Lexicon entries are fixed at 24 bytes (16-byte string field, length
   byte at offset 16, 4-byte count at offset 20, 3 bytes padding); the
   full learner memory layout (bigram 676 x i32, nlex, lexicon 64 x 24B,
   ground 64 x 8 x i32, neg_viol/neg_tot, cmp_ok/cmp_tot, K1 snapshot) is
   computed once before coding and is never changed mid-implementation.
2. `lex_add` rejects any segment with length > 16 (bounds check);
   every buffer access is bounds-checked against documented sizes.
3. K1 is measured from a lexicon snapshot taken at t=60 (end of phase 1),
   per the frozen DEVANG1 requirement.

### 4.2 The single mechanism change: cold-start tie-break

Before segmenting episode t, compute `bigram_total` as the sum of all
676 bigram counts (episodes 0..t-1 only, so t=0 sees total 0). If
`bigram_total == 0`, segmentation returns single-character segments
(each utterance byte its own segment) and the DP is not called.
Otherwise the unchanged DEVANG1 `seg_dp` runs. Rationale: this is exactly
the validated cold-start fix from the segmentation redesign (single
characters at t=0, no lexicon poisoning); it adds no persistent learner
state (the check reads the existing bigram buffer), preserves strict
online purity (episode t's counts are added after its segmentation per
K10/K11), and is the narrowest change that addresses the documented
whole-utterance default. In practice the branch fires at t=0 only
(episode 0's update makes the total nonzero); sparse-count behavior in
later early episodes remains the bigram DP's and is unchanged.

### 4.3 Explicitly NOT changed

No new semantic cases (no SUB, DIV, PARITY, two-threshold COND, or
equivalents; negator and comparative detection remain the generic
statistical tests of DEVANG1 prereg 4.5/4.6). No new modes, bridges,
routers, or task-specific handlers. No segmentation redesign beyond
section 4.2 (the DEVANG3 two-pass machinery is a separate line). No
changes to kill-bar thresholds, verdict rule structure, world design,
controls, or seeds.

## 5. Architecture accounting (frozen expectations; builder fills actuals)

| Field | Frozen expectation | Actual (builder fills at implementation) |
|-------|-------------------|------------------------------------------|
| Cognition source lines added | Small delta only: lexicon layout/bounds checks plus the cold-start branch; no new cognitive subsystem, no new module (cap: < 120 new/changed lines vs a faithful DEVANG1 port) | |
| New hardcoded semantic cases | 0 (no SUB, DIV, PARITY, two-threshold COND, or equivalents; no word-specific detectors) | |
| New modes / bridges / routers / handlers | 0 | |
| Learner-state structures created | 0 new persistent structures beyond DEVANG1's bigram[26][26], lexicon, ground[64][8], neg_viol/neg_tot, cmp_ok/cmp_tot, K1 snapshot (the cold-start check reads the existing bigram buffer) | |

Any implementation that adds a semantic case, mode, bridge, router, or
handler fails governance and cannot BUILD-PASS regardless of scores.

## 6. Frozen kill bars (exact numeric thresholds)

- **KR0 (crash regression, hard gate):** the exact DEVANG1 crash input
  (seeded episode generator, seed `123456789`, 100 training episodes
  processed strictly online followed by 20 frozen test episodes) must
  execute to completion with no panic, trap, or non-zero stderr on 3/3
  runs. Violation = BUILD-FAIL regardless of all other bars.
- **K1 (lexicon discovery):** >= 8 of the 10 phase-1 true words
  (tak, not, red, blu, bal, sph, cub, big, biger, smal) present as exact
  lexicon entries at end of phase 1, measured from the t=60 snapshot.
- **K2 (DIRECT novel):** >= 5/6 correct on tak+grn+cub and tak+blu+tri.
- **K3 (NEG novel):** >= 2/3 correct on tak+not+grn.
- **K4 (REL novel):** >= 2/3 correct on tak+biger+tri.
- **K5 (SYN novel):** >= 2/3 correct on tak+grn+sph.
- **K6 (SIZE novel):** >= 2/3 correct on tak+smal+tri.
- **K7 (3-WAY novel):** >= 1/2 correct on tak+big+grn+bal.
- **K8 (beats controls):** learner test accuracy (20 items) exceeds the
  best control (C1/C2/C3) by >= 15 percentage points.
- **K9 (new vocab acquisition):** >= 7/10 correct on the last 10 phase-2
  training episodes.
- **K10 (true online, governance):** code audit confirms strictly
  sequential processing; no structure is built from future data; updates
  for episode t occur after episode t is segmented and interpreted.
- **K11 (no future leakage in segmentation, governance):** the bigram
  counts used to segment episode t exclude episode t (verified by update
  ordering in code; the cold-start branch reads totals from 0..t-1 only).
- **K12 (determinism):** 3/3 byte-identical outputs; sha256 of each run
  recorded in the result.

**Verdict rule:** BUILD-PASS requires KR0, K1, K8, K10, K11, K12 plus at
least 4 of {K2..K7, K9}. Otherwise BUILD-FAIL. No bar may be altered
after results are observed. A bar may not be weakened to force a pass.

## 7. Frozen evaluation protocol

1. Implement in pure Zag (section 8) in the owned path only.
2. Run 3/3 with the frozen seed; record sha256 per run and assert
   byte-identical outputs (K12) and completion with zero stderr (KR0).
3. Report every bar K1..K12 plus KR0 in a table with threshold, result,
   and PASS/FAIL; report train accuracy (100) and test accuracy (20)
   for the learner and for C1, C2, C3 for comparability with
   DEVANG2-overnight (13/20) and DEVANG3 (16/20).
4. K10/K11 are verified by code inspection against the update ordering
   (segmentation of t precedes learn_update of t; test episodes perform
   no updates).
5. Report the architecture accounting actuals (section 5); any nonzero
   semantic case / mode / bridge / handler entry invalidates the verdict.

## 8. Honest boundaries

**What a BUILD-PASS would establish:** the DEVANG1 design can execute
crash-free under the frozen world; the cold-start tie-break avoids
lexicon poisoning; bigram DP segmentation can discover >= 8/10 phase-1
words online; learned segmentation, grounding, and generic
negator/comparative flags beat no-segmentation, fixed-width, and
substring-memory controls by >= 15pp on novel compositions. This is
developmental L2 structural-learning evidence (learner discovers
segmentations and parameterizes a researcher-designed interpretation
skeleton), not representational invention.

**What a BUILD-PASS would NOT establish:** no L3 claim (no C0 clause is
attempted: C0-A fails because semantics are learned parameters of a
researcher-designed skeleton, not learner-defined runtime semantics;
C0-B fails because the composition form is researcher-enumerated, not
open and incremental; C0-C fails because evaluation is one designed
world, not sealed unforeseen worlds; C0-D fails because no transfer or
cognitive-reuse test is run). No generality claim (one seeded world; per
the standing ruling, regression-battery style success must not be
overclaimed). No claim that cold-start repair fixes segmentation in
general; the DEVANG3 redesign line remains the candidate for deeper
segmentation work.

**What a BUILD-FAIL would establish:** if KR0 fails, the memory-safety
defect class survives the layout fix (report the panic location and
input). If mechanism bars fail (e.g., K1 < 8/10 or K8 missed), the
cold-start hypothesis is falsified: initialization was not the
bottleneck, corroborating that the scoring function is, and the
DEVANG3 redesign line is the correct next step.

## 9. Purity, determinism, commits

- Pure Zag only: implementation, compilation (pinned znc), execution,
  and analysis. No Python, C, or other languages at any stage.
- Seeded LCG; no wall-clock; no ASLR-dependent behavior in output.
- No em dashes in source or documentation.
- This prereg is committed ALONE before any .zag implementation.
  Implementation plus raw outputs plus result are committed separately.
- Owned paths only (`docs/lab/rsi/runs/wave-20261001-1421pdt/devang2/`).
  Local commits only; nothing is pushed.
