# SEALED_EVAL_ADV: adversarial battery against the unified `satisfy`

Wave: wave-20261002-1121pdt. Lane: COMP. Worker: lane-comp-20261002-1121pdt.
Prereg: PREREG_ADV.md frozen alone at d516c1da6 (2026-10-02 19:15:22 UTC).
Implementation committed at 21b881c9e (2026-10-02 19:23:25 UTC); KB6
commit-order self-check HOLDS (prereg strictly precedes implementation).
Mechanism: 0521pdt patch_d.zag, byte-identical (SHA df1d0faa...); zero
mechanism edits. Pure Zag, safebin PATH, no Python anywhere.

## Build and determinism record

- KB2: full_adv.zag lines 1..2027 (substrate + patch_d + shim region)
  SHA256 = 627ff98a691b0bd02e26d16b99d4b61fc064750eead9b3e6c1f45f7ca873ba81,
  byte-identical to 0521 full_d.zag lines 1..2027. patch_d.zag SHA =
  df1d0faa1802a8dc11c1b59f1b8277664308a0f699a3f7f479284a623a80fe82
  (matches the frozen 0521 value). Zero "compose" code occurrences in
  the mechanism region (grep; 3 comment hits explaining the absence
  only). Pipeline source-verified: activate -> satisfy -> trial ->
  bootstrap.
- KB1: 3x builds byte-identical (bin_adv SHA
  441bc63ad539c22be2b017b455ef38163cc6f297099bc941a6970d789155e828;
  bin_timed SHA b886131df6aae21737b80971d7b0bb8720aedc08d2b90656d91075097d5140cb).
  3x runs byte-identical (run_adv SHA
  af24011a7ddeec9d262fc45441ab10198e4014b6740b2543e4b69330d3de1e4c;
  run_timed SHA a5ab6ef96cf1962f04a817bbc30327e49f70455b35364e8589dc3550c6183346).
  KB1 HOLDS.
- Stdout byte-verified: intact markers, plausible integers, no dropped
  literals (per the 2026-10-02 _zag_print toolchain lesson; all output
  goes through the single-syscall emit path).

## Result matrix (run 1; runs 2/3 byte-identical)

(g) = SAT-SEGS/SAT-FIX marker confirms the satisfy mechanism produced
the answer. (t) = trial path produced the answer (B4 only, by design).
(i) = informational, unscored.

| test | result | marker | answer | mechanism note |
|------|--------|--------|--------|----------------|
| TPF1 | PASS (g) | SAT-SEGS n=5 | 112 | 11-edge goal; relseq 11-match; trial max reach 4 edges |
| TPF2 | PASS (g) | SAT-SEGS n=5 | 112 | TPF1 + 40 distractor facts |
| TPF3 | PASS (g) | SAT-FIX n=5 term=112 | 112 | unsupervised; no expected exists to leak |
| B1 | PASS (g) | SAT-SEGS n=2 | 105 | 9-edge distractor walked to depth exhaustion, backtracked |
| B2 | PASS (g) | SAT-SEGS n=2 | 105 | cycle 101-1->102-1->103-1->101 terminated by visited guard |
| B3S | PASS (g) | SAT-SEGS n=2 | 106 | distractor grounding tried first, backtracking recovered |
| B3U | FAIL (g) | SAT-FIX n=2 term=914 | 914 | PREDICTED FAIL: greedy fixpoint committed to distractor |
| B4 | PASS (t) | none; type14edges=0 | 105 | satisfy could not fire; trial answered; markers honest |
| B4U | INFO (i) | SAT-FIX n=1 term=103 | 103 | unsupervised promotes partial composite when stuck |
| B5 | PASS | none | -2 | no facts: no hallucination, no markers |
| B6 | PASS (g) | SAT-SEGS n=2 | 105 | 0521 ADV-A verbatim rerun: reproduces sealed result |
| B7 | PASS (g) | SAT-SEGS n=2 | 105 | 40 eight-edge distractor subtrees exhausted, no stall |
| B8 | PASS (g) | SAT-SEGS n=2 | 105 | k0=4 overshoot abandoned; prefix [1,1] of X used |
| PM1A | PASS (g) | SAT-SEGS n=2 | 105 | expected=105 selects the 105 completion |
| PM1B | PASS (g) | SAT-SEGS n=2 | 205 | expected=205 selects the 205 completion |
| PF1A | PASS (g) | SAT-SEGS n=3 | 105 | diamond DAG, first branch correct |
| PF1B | PASS (g) | SAT-SEGS n=3 | 105 | diamond DAG, dead branch tried first, backtracked |
| PF1C | INFO (i) | SAT-FIX n=2 term=106 | 106 | greedy commits to dead branch in DAG |

Marker totals: SAT-SEGS x14, SAT-FIX x4, matching the predicted
attribution exactly. B4/B5 sections contain zero SAT markers (grep).

## Timing (KB4a bars)

bin_timed (B1 + B2 + B7, same frozen mechanism): 16.4 s wall total
(2.36 s user). Bars: B1 < 120 s, B2 < 60 s, B7 < 300 s. All three
PASS with large margins. The exhaustive-grounding axis 0521 left
untested for A (A stalled 50+ min on 40 single-fact distractors):
D's DFS, guided by MAP-applicability, exhausts 40 eight-edge
distractor subtrees (each walked to depth exhaustion with k0=1
unwind) in seconds. Genuine measured robustness difference.

## Trial-path-free argument (KB3)

t2_trial's chain reach is k = 2..4 edges from the query subject.
TPF-1/2/3 goals are 11 edges from 101; every 2..4-edge taught path
from 101 terminates at 102..105 (TPF-2 adds dead-end 9100+i values),
never 112. Sum fallback: subsets of {102} (TPF-1/3) or
{102, 9100+i} (TPF-2) cannot sum to 112. Count fallback yields small
ints. The mechanical criteria additionally require the SAT marker
plus an exact 11-entry relseq match plus terminal 112, so a trial
rescue could not be miscounted as a satisfy win. TPF-3 has no
expected value at all: nothing can leak through supervision.

## KB scoring

- KB1 determinism: HOLD (3x builds, 3x runs byte-identical).
- KB2 mechanism freeze: HOLD (SHAs match; zero compose code hits).
- KB3 trial-path-free battery: HOLD (TPF-1/2/3 all PASS per 2.1).
- KB4a supervised breakers: HOLD (B1, B2, B3S, B6, B7, B8 all PASS;
  timing bars met with margin).
- KB4b attribution honesty: HOLD (B4: ans=105 via trial, no SAT-SEGS,
  zero type-14 edges on the rel-70 MAP; B5: ans=-2, no markers).
- KB4c unsupervised bounds: characterization. B3U FAILS as predicted
  (greedy trap wins; terminal 914, relseq [1,1,1,1]). B4U INFO:
  partial composite (terminal 103, relseq [1,1]) when no MAP covers
  the remainder. PF-1c INFO: dead-branch commit in DAG (terminal 106).
- KB5a source audit: HOLD (zero test-value literals in patch_d.zag
  code; the only `101` hits are SET-cell node-tag comparisons in the
  graph encoding; zero compose code occurrences).
- KB5b probe-menu: PM-1a AND PM-1b PASS. Expected value selects among
  fully MAP-licensed completions. Recorded as BOUND: satisfy carries
  no intrinsic preference between multiple valid compositions; the
  goal disambiguates. (Counter to full probe-menu equivalence:
  TPF-3/0521-NOSUP compose with no expected value at all.)
- KB6 commit order: HOLD (d516c1da6 19:15:22 strictly before
  21b881c9e 19:23:25).
- KB7: SURVIVES-ADV-A. KB1, KB2, KB3, KB4a, KB4b, KB5a all hold;
  PF-1a/PF-1b PASS, so no downgrade to SURVIVES-SEALED-ONLY.
  No breaker produced a wrong-answer promotion or a hang.

## Prediction calibration (not kill bars)

17/17 correct: every PASS/FAIL/INFO prediction in PREREG_ADV section 4
matched, including B3U FAIL (terminal 914 exactly as predicted),
B4U INFO (terminal 103), PF-1c INFO (terminal 106).
