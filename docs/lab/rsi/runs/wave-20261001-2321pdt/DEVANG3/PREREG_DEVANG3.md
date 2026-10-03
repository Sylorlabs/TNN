# PREREG_DEVANG3 (fresh): Linear Novel-Length Penalty as the Segmentation Fix

**Status:** FROZEN on commit. The coordinator commits this file ALONE
before any .zag implementation exists in the lane.
**Date:** 2026-10-01.
**Wave:** wave-20261001-2321pdt.
**Lane:** DEVANG3.
**Owned path:** `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/`

## Disambiguation

Two earlier artifacts share the lane name:
`docs/lab/research-lead/overnight-20260928/devang3/` (overnight DEVANG3,
BUILD-FAIL 16/20 vs 17/20, prereg commit `b2ceb6b38`) and
`docs/lab/rsi/runs/wave-20261001-2021pdt/DEVANG3/` (wave-20261001-2021pdt,
BUILD-FAIL: K_SEG 8/12 vs 9/12, K_SEAL 11/20 vs 12/20). This document is a
separate, fresh prereg for the current wave. It adopts the 2021pdt
information-flow architecture (segmentation-dependent statistics, K_AUD
design requirement) but replaces the segmenter scoring. The 2021pdt sealed
worlds are REGRESSION ONLY for this wave, not kill-bar inputs.

## 1. Standing failure this prereg answers

Wave-20261001-2021pdt DEVANG3 BUILD-FAIL (SEALED_EVAL.md, adversary):
K_SEG 8/12 (need >= 9/12), K_SEAL 11/20 (need >= 12/20). K_AUD PASS
confirmed the result is segmentation-dependent (mechanism result, not
architectural recurrence): the fix needed is segmenter quality, not a new
mechanism. The four K_SEG failures were all merges of a novel word with an
adjacent known word, plus one exact tie resolved the wrong way:
- probe 6 `blumalagrn`: got `[blu][malagrn]`, key `[blu][mala][grn]`.
- probe 8 `grnsalabal`: got `[grnsala][bal]`, key `[grn][sala][bal]`.
- probe 9 `takbigerkala`: got `[tak][big][erkala]` (tie), key `[tak][biger][kala]`.
- probe 12 `nottemagrn`: got `[not][temagrn]`, key `[not][tema][grn]`.

## 2. Root cause (frozen diagnosis)

The 2021pdt segmenter scored a novel (unseen) segment of length L as
`-50 + ilog(L+1)*5`: a fixed cost plus a LENGTH BONUS. The length bonus
made longer novel segments score HIGHER, so merging a novel word with an
adjacent known word (one long novel segment) beat isolating the novel word
(two shorter pieces, one of which pays the fixed cost again). Concretely,
for probe 8: `[grnsala]` scored `-35` while `[grn][sala]` scored
`0 + -40 = -40`; the merge won by 5 points on the length bonus alone.
For probe 9 the two analyses tied exactly and the tie-break (first
max wins) chose the wrong one. The length term had the wrong sign:
under any character-level generative story, a longer novel string should
cost MORE (each character is additional evidence against the analysis),
not less. The fix is to flip the length bonus to a length penalty.
This is a scoring correction inside the same generic mechanism (DP over
lexicon-frequency statistics), not a new mechanism and not a semantic case.

## 3. Frozen segmenter design

The segmenter is the 2021pdt `seg_dp` (DP over lexicon-frequency scores,
cold-start 3-char chunks while nlex < 10, all statistics updated
exclusively from segmenter output) with EXACTLY ONE scoring change:

- Novel segment (count 0), length L: `score = -50 - 1*L`.
  (Was: `-50 + ilog(L+1)*5`.)
- Seen segment (count c >= 1), length L: unchanged:
  `score = ilog(c)*10 - 30 + ilog(L+1)*5`, minus 40 if L == 1.
- Tie-break: unchanged (strictly greater wins; first max kept).
- Cold start: unchanged (3-char chunks while nlex < 10).
- No new tables, no new modes, no new semantic cases. The C0 control
  (`seg_dp_raw`, raw-bigram DP) is unchanged.

Why this fixes the four probes (verified by hand arithmetic on the
post-training lexicon counts, and confirmed on the 2021pdt sealed set as
regression: 12/12):
- Probes 6, 8, 12: the correct and wrong analyses contain the SAME number
  of novel segments (one), so the fixed -50 cancels; the linear penalty
  makes the shorter novel piece win by `3*1 = 3` points.
- Probe 9: `[biger][kala]` beats `[big][erkala]` by `2*1 = 2` points
  (novel `kala` is 2 chars shorter than novel `erkala`); the tie is gone.

Why Family A learning still works (K1): early in training the known piece
in a novel-word formation event has a WEAK score (e.g. `s(big)` approx -10
when `biger` first forms), so the novel whole still beats the split;
the penalty only bites once the lexicon is mature. No schedule is needed.

## 4. Learner and world (inherited from the frozen 2021pdt design)

Family A is the frozen DEVANG1 world verbatim (same episodes, seed
`123456789`, same phases, same hold-outs). Online protocol, grounding,
negator/comparative detection, and interpretation are unchanged from the
2021pdt implementation. Controls C1 (whole-utterance memorization), C2
(fixed-width-3), C3 (literal substring memory), and C0 (raw-byte
statistics, the DEVANG2 failure-mode architecture) run the same scenes.

## 5. Seal protocol (frozen)

1. After this prereg is committed, the builder implements the one-line
   scoring change plus the sealed-evaluation interface (same interface as
   2021pdt: `segb`, `segb-abl`, `sealc`, `sealc-fresh`).
2. The builder then writes two deterministic pure-Zag generators for the
   FRESH sealed families (new vocabulary and new episode selections; the
   2021pdt sealed files are not reused). Generator designs:
   - Family B: 12 utterances; word lengths 3 to 4; at least 3 word pairs
     sharing a prefix of length >= 2; at least 3 word pairs sharing a
     suffix of length >= 2; Family A anchor words plus novel words;
     ground-truth boundaries recorded by the generator.
   - Family C: 60 train + 20 test episodes; new surface vocabulary (no
     Family A word forms); word lengths 3 to 4 (3-char content words,
     4-char negator/comparative in fixed positions); boundary positions
     materially different from Family A (attested in sealed notes);
     every test word occurs >= 8 times in training; test episodes use
     novel combinations of trained words.
3. The sealed files and their sha256 hashes are committed (SEALED_B.md,
   SEALED_C.md) BEFORE any sealed run. The builder does not inspect the
   sealed file contents between generation and the sealed run; the
   generator is written from the class spec above without observing its
   outputs.
4. The sealed run executes the frozen binary against the sealed files as
   opaque inputs. Each sealed command is run 3/3 with byte-identical
   stdout required.
5. Note on independence: this wave has no separate adversary worker
   (single worker does builder and sealed generation). The mitigation is
   the blind-generation discipline in step 3 plus fresh vocabulary and
   fresh episode selections. This limitation is recorded here and in
   JUDGE_BRIEF.md.

## 6. Frozen kill bars (exact numeric thresholds)

- **KR0 (crash regression, hard gate):** Family A, 3/3 runs complete,
  exit code 0, zero stderr bytes each. Violation = BUILD-FAIL.
- **K1 (lexicon discovery):** >= 8 of the 10 phase-1 true words present
  as exact lexicon entries in the t=60 snapshot.
- **K_SEG (segmentation quality):** >= 9/12 FRESH sealed Family B
  utterances segmented with exact true boundaries.
- **K_SEAL (post-freeze adversarial):** learner accuracy >= 12/20 on
  FRESH sealed Family C test episodes (`sealc-fresh`, learner variant).
  C0, C1, C2, C3 accuracies on Family C are reported for comparison.
- **K_AUD (segmentation-dependence audit):** code inspection PASS on the
  three 2021pdt claims: (a) every statistics table updated only from
  segmenter output; (b) no raw-byte path into statistics on the learner
  path; (c) cold start inside the segmenter feeding the same update.
  Any violation = BUILD-FAIL (DEVANG2-mode recurrence).
- **K_ABL (ablation):** fixed-width-3 ablation scores <= 5/12 on FRESH
  sealed Family B (and < 9/12). If the ablation reaches 9/12, the
  front-end is not load-bearing = BUILD-FAIL.
- **K_C0 (trap exclusion):** C0 (raw-byte statistics) trails the learner
  by >= 15 percentage points on Family A test accuracy AND by >= 3 words
  on K1. Otherwise = BUILD-FAIL.
- **K8 (beats controls):** Family A learner test accuracy exceeds the
  best of C1/C2/C3 by >= 15 percentage points.
- **K2..K7, K9 (sub-bars):** at least 4 of {K2 >= 5/6, K3 >= 2/3,
  K4 >= 2/3, K5 >= 2/3, K6 >= 2/3, K7 >= 1/2, K9 >= 7/10}.
- **K10 (true online):** code audit PASS (strictly sequential; updates
  for episode t after episode t is segmented and interpreted).
- **K11 (no future leakage in segmentation):** code audit PASS
  (statistics used for episode t exclude episode t).
- **K12 (determinism):** 3/3 byte-identical outputs on every family and
  every variant; sha256 recorded per run.

**Regression bars (2021pdt worlds, not kill bars):** the tuned segmenter
must not regress on the 2021pdt sealed sets: Family B >= 8/12 (was 8/12),
Family C >= 11/20 (was 11/20). A regression is reported as a negative
result but does not by itself flip the verdict.

**Verdict rule:** BUILD-PASS requires KR0, K1, K_SEG, K_SEAL, K_AUD,
K_ABL, K_C0, K8, K10, K11, K12, plus at least 4 of
{K2, K3, K4, K5, K6, K7, K9}. Otherwise BUILD-FAIL. No bar may be
altered after results are observed.

## 7. Negative controls (what constitutes BUILD-FAIL)

1. Any required bar missed under the verdict rule in section 6.
2. KR0 violated.
3. K_AUD, K_ABL, or K_C0 failed: DEVANG2-mode recurrence.
4. Any new mode, bridge, router, task-specific handler, or hardcoded
   semantic case in the implementation: governance fail.
5. Cognition source lines added versus the 2021pdt baseline reaching 120
   or more new/changed lines: governance fail. (Expected: under 10.)
6. Python or any forbidden executable invoked: PROCESS-FAIL.
7. Any implementation file predating the prereg freeze commit, or
   unverifiable commit ordering: prereg VOID.
8. Sealed inputs inspected before the sealed run: sealed evaluation VOID.
9. Any frozen bar weakened after results: verdict VOID.

## 8. Architecture accounting (frozen expectations)

| Field | Frozen expectation |
|-------|-------------------|
| Cognition source lines added vs 2021pdt | under 10 (one scoring line plus comment updates) |
| New hardcoded semantic cases | 0 |
| New modes / bridges / routers / handlers | 0 |
| Learner-state structures created | 0 (no new tables; scoring constants only) |
| Protected-core / ISA boundary | no new protected operations |

## 9. Honest boundaries

**What a BUILD-PASS would establish:** the length-penalty scoring fixes
the merge pathology on held-out ambiguity probes (>= 9/12) and supports
post-freeze adversarial generalization (>= 12/20), with the
segmentation-dependence architecture intact (K_AUD, K_ABL, K_C0).
Developmental L2 evidence only, not representational invention.

**What a BUILD-PASS would NOT establish:** no L3 claim. No generality
beyond the three families. No claim about 2-char words (the 3-char
cold-start bootstrap cannot seed them; documented limitation) or about
5+ char words in variable positions (fragile under this segmenter).

**What a BUILD-FAIL would establish:** if K_SEG fails, the linear penalty
is insufficient for the fresh ambiguity classes. If K_SEAL fails while
K_SEG passes, segmentation improved but did not transfer to the
adversarial family. If K_AUD/K_ABL/K_C0 fail, DEVANG2-mode recurrence.

## 10. Purity, determinism, commits

- Pure Zag only: implementation, compilation (pinned znc), execution.
  No Python, C, or other languages at any stage.
- Seeded LCG; no wall-clock; no ASLR-dependent behavior in output.
- No em dashes in source or documentation.
- This prereg is committed ALONE before any .zag implementation exists
  in the lane. Implementation, sealed generators, sealed files, raw
  outputs, and results are committed separately, in order.
- Owned path only
  (`docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/`). Local commits
  only; nothing is pushed. No git reset, no rebase.
