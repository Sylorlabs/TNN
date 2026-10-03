# PREREG_DEVANG3 (fresh): Segmentation-Dependent Statistics as a Design Requirement

**Status:** DRAFT. Not yet frozen. The coordinator commits this file ALONE
before any .zag implementation exists in the lane.
**Date:** 2026-10-01.
**Wave:** wave-20261001-2021pdt.
**Lane:** DEVANG3.
**Owned path:** `docs/lab/rsi/runs/wave-20261001-2021pdt/DEVANG3/`

## Disambiguation

An earlier artifact with the same lane name exists:
`docs/lab/research-lead/overnight-20260928/devang3/` (overnight DEVANG3,
two-pass TP segmentation plus lexicon-reuse repair, BUILD-FAIL close at
16/20 against a 17/20 bar, prereg commit `b2ceb6b38`). This document is a
separate, fresh prereg for the current wave. It does not adopt that
machinery, its bars, or its verdict history. References below to
"DEVANG2" mean the wave-20261001-1721pdt retry lane
(`docs/lab/rsi/runs/wave-20261001-1721pdt/DEVANG2/`, triply determined
BUILD-FAIL, red-team review EVIDENCE HOLDS) unless stated otherwise.

## 1. Standing failures this prereg answers

1. DEVANG1 (`docs/lab/research-lead/overnight-20260928/devlang/`,
   prereg commit `e23627a40`): the training loop crashed with "slice
   index out of bounds" (8-byte lexicon string field versus 9+ character
   segments; `lex_add` wrote past the field and corrupted the length
   byte; the 24-byte layout expansion introduced new out-of-bounds
   accesses). Root cause never isolated. No output, no kill bar
   measurable. Verdict: BUILD-FAIL.
2. DEVANG2 retry (wave-20261001-1721pdt): crash fix plus exactly one
   mechanism change (cold-start tie-break: single-character segments
   while total bigram observations equal zero). Triply determined
   BUILD-FAIL: K1 3/10 vs 8/10, K8 learner 13/20 vs best control 17/20
   (gap -20pp vs required +15pp), sub-bars 3/7 vs 4. Crash-regression
   gate PASS, determinism 3/3 byte-identical PASS. The cold-start
   hypothesis is falsified.
3. The adopted deeper cause (independent red-team review of DEVANG2,
   residual note 1): bigram learning read raw utterance bytes and was
   segmentation-independent by construction. The DP's only inputs were
   those bigram counts, so segmentations at t>=1 were identical between
   the cold-start and no-cold-start variants, and the repair was
   architecturally incapable of moving K1, not merely empirically inert.
   No t=0-only segmentation change could ever move K1, because the
   statistics that drive the DP never depended on segmentation.

Queue item for this wave: DEVANG3 with segmentation-dependent statistics
as a design requirement, not just a scoring-function fix. Both prior
failures inform this prereg: the crash (memory layout frozen before
coding, section 3) and the inert repair (information-flow constraint,
section 2).

## 2. The design requirement (frozen)

One door for bytes. The segmentation front-end is the only consumer of
raw utterance bytes. All statistics (bigram, unigram, and any
higher-order tables the learner keeps) are updated exclusively from
segmenter output: segment identities, intra-segment character pairs, and
segment-to-segment transitions. No statistics update function may read
raw utterance bytes. The cold-start path is part of the segmenter: its
declared t=0 output feeds the same statistics update as every later
episode, never a bypass around it. The consequence that must hold, and
that the kill bars verify, is that perturbing the segmenter measurably
perturbs the statistics.

Why this is a design requirement and not a scoring-function fix: the
DEVANG2 failure was information-flow, not scoring. The statistics table
never depended on segmentation, so any repair confined to segmentation
behavior (the cold-start tie-break) or to DP scoring (boundary cost,
length averaging, TP thresholds) leaves the information source unchanged
and is architecturally incapable of moving lexicon discovery. A
scoring-function fix changes how candidate boundaries are ranked; it
does not change what the statistics know. The DEVANG2 trap was exactly
this: a repair that fired correctly at t=0 and was byte-identical
downstream by necessity, because `learn_update` counted bigrams from
`ep[48+k]` and `ep[48+k+1]` (raw utterance bytes), never from the
segmentation. This prereg therefore constrains the architecture's
information flow, and the kill bars verify the constraint structurally
(K_AUD code audit), causally (K_ABL ablation), and differentially
(K_C0 control comparison), rather than trusting a repair's intent.

## 3. Crash-resistance (frozen design rules, from the DEVANG1 diagnosis)

1. The full learner memory layout is computed and documented before
   coding and is never changed mid-implementation.
2. Lexicon entries are fixed at 24 bytes (16-byte string field, length
   at offset 16, count at offset 20, 3 bytes padding); `lex_add`
   rejects any segment longer than 16 bytes.
3. Every buffer access is bounds-checked against documented sizes.
4. K1 is measured from an in-loop lexicon snapshot at t=60 (end of
   phase 1); the DEVANG1 timing deviation stays corrected.
5. Crash-regression input (KR0): the exact DEVANG1 crash input, seeded
   episode generator, seed `123456789`, 100 strictly-online training
   episodes followed by 20 frozen test episodes.

## 4. Learner and world (inherited from the frozen DEVANG1 design)

Family A (base, comparability) is the frozen DEVANG1 world verbatim:
objects (3 per episode; color red/blu/grn, shape ball/cube/tri, size
smal/big), vocabulary (tak, not, red, blu, grn, bal, sph, cub, tri,
big, biger, smal; variable word lengths 3, 4, 5; big/biger morphology;
bal/sph synonymy), episode templates (DIRECT, NEG, REL, SIZE), phases
(60 phase-1, 40 phase-2, 20 test with the same explicit hold-outs:
grn+cub, blu+tri, grn+sph, not+grn, biger+tri, smal+tri,
big+grn+bal), seeded LCG scene generation with seed `123456789`
(same generator; same scenes for learner and controls).

Online protocol: episode t is segmented using only state derived from
episodes 0..t-1; bigram/lexicon/grounding/negator/comparative
statistics are updated after episode t is segmented and interpreted,
using only episode t's data; test episodes perform no updates.

Grounding: `primary(s)` is the argmax over the 8 feature-values of the
grounding table, valid only if the lexicon count for s is >= 2.
Negator detection stays the generic statistical test (adjacent pair
counts, violation ratio), not hardcoded to any word. Comparative
detection stays the generic statistical test (shape-conditioned size
comparisons), not hardcoded to any word. Interpretation passes follow
DEVANG1 section 4.7 (action-marker skip, negator/comparative token
rules, object scoring, max score with lowest-index tie-break).

Controls C1 (whole-utterance memorization), C2 (fixed-width-3
segmentation), C3 (literal substring memory) run the same scenes.

Mechanism freedom: within sections 2, 3, and 8, the builder may redesign
the segmenter and the statistics tables freely, including replacing the
raw-byte bigram[26][26] table with segmentation-derived tables, as long
as every kill bar, the audit, and the architecture accounting hold.

## 5. Seal protocol (frozen)

1. After this prereg is committed, the wave coordinator spawns an
   independent adversary worker (not the builder; no shared
   implementation notes beyond this prereg).
2. The adversary designs and commits the sealed world package before
   the builder's sealed-evaluation run. The package contains: (a) the
   Family B generator, sealed inputs, and ground-truth boundaries;
   (b) the Family C generator, sealed inputs, and answer key. The
   commit records the sha256 of every sealed file.
3. Families:
   - Family A (base, comparability): the frozen DEVANG1 world,
     unsealed, seed `123456789`. Used for KR0, K1, K2..K9, K8, K10,
     K11, K12, K_ABL (Family A part), K_C0.
   - Family B (held-out segmentation ambiguity, sealed): at least 12
     utterances; word lengths 2 to 6; at least 3 word pairs sharing a
     prefix of length >= 2; at least 3 word pairs sharing a suffix of
     length >= 2; ground-truth boundaries committed by the adversary.
     Used for K_SEG and K_ABL (Family B part).
   - Family C (post-freeze adversarial, sealed): at least 20 novel
     test episodes; new surface vocabulary (no Family A word forms);
     word lengths 2 to 6; boundary statistics materially different
     from Family A (attested in the adversary's sealed notes);
     designed after freeze, never a trivial Family A variant. Used
     for K_SEAL, with C0, C1, C2, C3 reported for comparison.
4. Non-circumvention: the builder must not open or inspect sealed
   input files before the sealed run. Any evidence of pre-run
   inspection voids the sealed evaluation (governance VOID, not
   BUILD-PASS). The sealed run executes the frozen binary against the
   sealed files as opaque inputs; the builder records the run, not
   the inputs.
5. Commit order: the adversary's sealed package commit strictly
   precedes the sealed-evaluation run. The coordinator verifies this
   from git history before accepting any sealed result.

## 6. Frozen kill bars (exact numeric thresholds)

- **KR0 (crash regression, hard gate):** Family A, 3/3 runs complete,
  exit code 0, zero stderr bytes each, no panic or trap. Violation =
  BUILD-FAIL regardless of all other bars.
- **K1 (lexicon discovery):** >= 8 of the 10 phase-1 true words
  (tak, not, red, blu, bal, sph, cub, big, biger, smal) present as
  exact lexicon entries in the t=60 snapshot.
- **K_SEG (segmentation quality):** >= 9/12 sealed Family B
  utterances segmented with exact true boundaries (no missing,
  extra, or shifted boundaries).
- **K_SEAL (post-freeze adversarial):** learner accuracy >= 12/20 on
  sealed Family C test episodes. C0, C1, C2, C3 accuracies on
  Family C are reported alongside for comparison.
- **K_AUD (segmentation-dependence audit, governance):** independent
  code inspection PASS on all three claims: (a) every statistics
  table is updated only from segmenter output; (b) no code path reads
  raw utterance bytes into any statistics table; (c) the cold-start
  path is inside the segmenter and its output feeds the same
  statistics update as later episodes. Any violation = BUILD-FAIL,
  classified as DEVANG2-mode recurrence.
- **K_ABL (ablation, load-bearing front-end):** the ablation variant
  (frozen learner source with only the segmenter replaced by
  fixed-width-3 chunking; statistics machinery, lexicon, grounding,
  negator/comparative detection, and interpretation identical) must
  FAIL K1 (< 8/10 on Family A) AND FAIL K_SEG (<= 5/12 on Family B).
  If the ablation passes either bar, the front-end is not
  load-bearing = BUILD-FAIL.
- **K_C0 (trap exclusion, no architecture-independent rescue):**
  control C0 (frozen learner source with only the statistics input
  switched from segmenter output to raw utterance bytes, i.e. the
  DEVANG2 failure-mode architecture; segmenter, lexicon, grounding,
  negator/comparative detection, interpretation, seeds, and worlds
  identical) must trail the learner by >= 15 percentage points on
  Family A test accuracy AND by >= 3 words on K1. If C0 matches the
  learner within those margins, the win does not come from
  segmentation-dependent statistics = BUILD-FAIL.
- **K2 (DIRECT novel):** >= 5/6 correct on tak+grn+cub and tak+blu+tri.
- **K3 (NEG novel):** >= 2/3 correct on tak+not+grn.
- **K4 (REL novel):** >= 2/3 correct on tak+biger+tri.
- **K5 (SYN novel):** >= 2/3 correct on tak+grn+sph.
- **K6 (SIZE novel):** >= 2/3 correct on tak+smal+tri.
- **K7 (3-WAY novel):** >= 1/2 correct on tak+big+grn+bal.
- **K9 (new vocab acquisition):** >= 7/10 correct on the last 10
  phase-2 training episodes.
- **K8 (beats controls):** Family A learner test accuracy (20 items)
  exceeds the best of C1/C2/C3 by >= 15 percentage points.
- **K10 (true online, governance):** code audit PASS: strictly
  sequential processing; updates for episode t occur after episode t
  is segmented and interpreted; no structure is built from future
  data.
- **K11 (no future leakage in segmentation, governance):** code audit
  PASS: the statistics used to segment episode t exclude episode t.
- **K12 (determinism):** 3/3 byte-identical outputs on every family
  and every variant (learner, C0, ablation); sha256 recorded per run.

**Verdict rule:** BUILD-PASS requires KR0, K1, K_SEG, K_SEAL, K_AUD,
K_ABL, K_C0, K8, K10, K11, K12, plus at least 4 of
{K2, K3, K4, K5, K6, K7, K9}. Otherwise BUILD-FAIL. No bar may be
altered after results are observed. A bar may not be weakened to force
a pass.

## 7. Negative controls (what constitutes BUILD-FAIL)

1. Any required bar missed under the verdict rule in section 6.
2. KR0 violated: any panic, trap, nonzero exit, or nonzero stderr on
   any of the 3/3 runs.
3. K_AUD, K_ABL, or K_C0 failed: classified as recurrence of the
   DEVANG2 segmentation-independent failure mode (repair that is
   architecturally inert). The result must name which of the three
   failed and quote the numbers.
4. A t=0-only or scoring-only repair that leaves the statistics
   input unchanged: excluded by design (K_AUD claim (b) and (c));
   submitting one is a governance fail.
5. Any new mode, bridge, router, task-specific handler, or hardcoded
   semantic case found in the implementation: governance fail, cannot
   BUILD-PASS regardless of scores. (No SUB, DIV, PARITY,
   two-threshold COND, or equivalents; negator and comparative
   detection stay the generic statistical tests.)
6. Cognition source lines added versus the DEVANG2 baseline (1065-line
   devang2.zag at commit `153e2af8e`) reaching 120 or more
   new/changed lines: governance fail. Target is zero or negative.
7. Python or any forbidden executable invoked at any stage:
   automatic PROCESS-FAIL for the wave.
8. Any implementation file predating the prereg freeze commit, or
   unverifiable commit ordering: this prereg is VOID.
9. Sealed inputs inspected before the sealed run: the sealed
   evaluation is VOID.
10. Any frozen bar weakened after results are observed: the verdict
    is VOID.

## 8. Architecture accounting (frozen expectations; builder fills actuals)

| Field | Frozen expectation | Actual (builder fills at implementation) |
|-------|-------------------|------------------------------------------|
| Cognition source lines added vs DEVANG2 baseline | target <= 0 (zero or negative); hard cap < 120 new/changed lines | |
| New hardcoded semantic cases | 0 | |
| New modes / bridges / routers / handlers | 0 | |
| Learner-state structures created | net 0 new persistent structures; segmentation-derived statistics tables replace the raw-byte bigram table rather than adding parallel tables | |
| Protected-core / ISA boundary | no new protected operations; frozen ISA respected; no benchmark-specific opcodes | |

Any nonzero entry in the semantic-case, mode, bridge, router, or
handler rows invalidates the verdict regardless of scores.

## 9. Honest boundaries

**What a BUILD-PASS would establish:** crash-free execution under the
frozen world; segmentation-dependent statistics as a working design
(segmenter errors propagate into statistics by audit, the front-end
is load-bearing by ablation, and the win is not an
architecture-independent rescue by control comparison); lexicon
discovery >= 8/10 strictly online; exact segmentation >= 9/12 on
sealed held-out ambiguity cases; >= 12/20 on a post-freeze adversarial
family; beating no-segmentation, fixed-width, and substring-memory
controls by >= 15pp. This is developmental L2 structural-learning
evidence (the learner discovers segmentations and parameterizes a
researcher-designed interpretation skeleton), not representational
invention.

**What a BUILD-PASS would NOT establish:** no L3 claim (no C0 clause
is attempted: semantics remain learned parameters of a
researcher-designed skeleton, not learner-defined runtime semantics).
No generality claim: three families over one base world; per the
standing ruling, regression-style success must not be overclaimed,
and the post-freeze sealed battery is the important generality test,
not a generality proof. No claim that this segmentation design
transfers to other modalities or languages.

**What a BUILD-FAIL would establish:** if KR0 fails, the
memory-safety defect class survives the layout rules (report the
panic location and input). If K_AUD, K_ABL, or K_C0 fail, the
segmentation-independent failure mode recurs despite the design
requirement, which is evidence the information-flow constraint was
not actually implemented. If K1 or K_SEG fail while the
segmentation-dependence bars pass, the design requirement holds but
the segmenter quality is insufficient, and the failure is a mechanism
result, not an architectural-recurrence result.

## 10. Purity, determinism, commits

- Pure Zag only: implementation, compilation (pinned znc), execution,
  and analysis. No Python, C, or other languages at any stage.
- Seeded LCG; no wall-clock; no ASLR-dependent behavior in output.
- No em dashes in source or documentation.
- This prereg is committed ALONE before any .zag implementation
  exists in the lane. Implementation plus raw outputs plus result are
  committed separately. The builder records file creation order in
  BUILD-LOG.md at implementation time.
- Owned path only
  (`docs/lab/rsi/runs/wave-20261001-2021pdt/DEVANG3/`). Local commits
  only; nothing is pushed. No git reset, no rebase.
