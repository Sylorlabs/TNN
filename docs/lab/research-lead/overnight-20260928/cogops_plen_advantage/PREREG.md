# PREREG: COGOPS-PLEN-ADVANTAGE

Frozen 2026-10-03. This prereg strictly precedes implementation
(commit-order self-check applies). Non-ledger task (claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/cogops_plen_advantage/`,
branch `tnn-native-lab`.

## Question

COGOPS-PLEN-GRANULARITY (verdict INCOMPLETE, negative on bars)
reported a sign reversal against the original K4 hypothesis:
lower revise-phase plen (PADAPT 0->1) cost less than or equal to
fixed plen=3 in 24/24 matched arms, strictly less in pairs 3, 6, 7
at every granularity (deltas at g=2: [0,0,0,-1,0,0,-84,-216];
sign test on 3/3 non-tied favoring PA: p=0.125, suggestive not
significant). It also found the PA-vs-P3 gap is driven by plen=0
itself, not the 0->1 thermostat step (thermostat fired in only
7/24 arms; PA diverged from P3 in 24/24).

This lane tests the reversed hypothesis directly: **adaptive
(lower) revise-phase PLEN is beneficial vs fixed PLEN=3** --
lower revise cost, not higher -- and discriminates whether any
benefit comes from the adaptive ramp or merely from the lower
plen level.

## Design

`adv.zag` ports `cogops_plen_granularity/gran.zag`
(tnn-native-lab, sha256
`8b5cd1da7c761543ce51cbc8a5f4bd4b3560fde95f54646f1778a41bca8a2740`)
with targeted edits only. The revise driver, worlds, operators,
adopt rule (`best > cur+150`), 850 raw passer bar, 30-generation
revise, matched-RNG record/check protocol, and the three replay
scorers are unchanged.

### Arms (per pair, per rg)

- P1 (plenmode 1): pmode 3, cell 2370=1; plen_adapt returns
  early (2370!=0). Fixed plen=1. Records the RNG state.
- P0 (plenmode 5, NEW): pmode 3, cell 2370=0, cell 2405=1
  (plen_hold). plen_adapt early-returns on 2405==1, so plen
  stays 0 for the whole revise. Fixed plen=0. This is the
  level-control that discriminates adaptivity from level:
  PA minus P0 is exactly the adaptive 0->1 step.
- PA (plenmode 4): pmode 3, cell 2370=0, plen_adapt live.
  Adaptive 0->1 (the true adaptive revise state).
- P3 (plenmode 3): pmode 2. Fixed plen=3.

P0, PA, P3 check the RNG state recorded by P1 (binary-enforced
matched-RNG; graded_replay consumes no RNG).

### Pairs

k2 = 0..15. k2 < 8: the original 8 pair seeds, byte-identical
to the RNG/granularity lanes
(env `123456789+k*104729`, learn `987654321+k*7919`).
k2 >= 8: 8 FRESH seeds, same family, disjoint constants
(env `555555555+(k-8)*104729`, learn `333333333+(k-8)*7919`;
verified disjoint from the original ranges).

### Granularities

rg = 0 (quantized control) and rg = 2 (fine, where the plen
coefficient bites). rg = 1 skipped to bound runtime; the
PA-vs-P3 cost edge was consistent across all g in the
granularity lane.

128 revise searches per binary run (16 pairs x 4 arms x 2 rg).
Expected RNG-MATCH: 96 per run (3 checks x 16 pairs x 2 rg).

### Reporting (per arm)

- `REVISE-RESULT`: unchanged format (trials, best, adopted).
  Cost = trials if adopted else 369 (granularity-lane
  convention).
- `GEN`: unchanged (sumlen, bestraw, fixcount per generation).
- `FLIP`: extended with `inv=` (cell 2372 inversion count).
- `QUALITY` (new): bestlen (best passer length, -1 if none),
  inv, adj (PLEN-ADJ fire count, cell 2371).

### Code edits (all reporting or the hold cell unless noted)

E1 header comment; E2 fresh-seed branch in
pair_env_seed/pair_learn_seed (k<8 unchanged);
E3 setup_run zeroes cell 2405;
E4 plen_adapt early-returns when cell 2405==1 (behavioral
only for the new P0 arm; P1/PA arms have 2405=0);
E5 inversion-diagnostic gate widened from pmode==3 to
pmode>0 (reporting only; cell 2372 is write-only);
E6 revise_arm: plenmode 5 branch, FLIP gains inv=, new
QUALITY emit;
E7 main: rgi loop over rg {0,2}, k2 0..15, arms
P1(record), P0, PA, P3 (check).

## Frozen kill bars

- AH1 CONTROL REPLICATION: rg in {0,2}, original 8 pairs,
  arms P1/P3/PA: GEN sequences byte-identical to
  gran_run1.txt (48/48 arms). PASS required to license any
  inference.
- AH2 FRESH-SEED ADVANTAGE: rg=2, 8 fresh pairs:
  cost(PA) <= cost(P3) in 8/8 pairs AND cost(PA) < cost(P3)
  in >=2/8 pairs. Tests whether the never-worse /
  sporadically-better shape replicates on independent seeds.
- AH3 COMBINED SIGNIFICANCE: rg=2, all 16 pairs: one-sided
  sign test on cost(PA) vs cost(P3), ties dropped, p < 0.05
  per the frozen critical-k table below (n non-tied pairs
  -> minimum strict PA wins k):
  5->5, 6->6, 7->7, 8->7, 9->8, 10->9, 11->9, 12->10,
  13->10, 14->11, 15->12, 16->12. (n<=4 cannot reach
  p<0.05.)
- AH4 LEVEL-vs-ADAPTIVITY (interpretation; evaluated only
  if AH3 passes): rg=2, 16 pairs, cost(PA) vs cost(P0).
  - AH4a: cost(PA) == cost(P0) in >=13/16 pairs ->
    the benefit is the LEVEL (plen ~0), the adaptive ramp
    adds nothing in revise.
  - AH4b: cost(PA) < cost(P0) in >=5/16 pairs AND
    cost(PA) > cost(P0) in <=2/16 pairs -> the adaptive
    ramp adds value beyond fixed low plen.
- AH5 DOSE-RESPONSE (informative): rg=2, 16 pairs: mean
  costs P0/PA/P1/P3; count of pairs with monotone
  P0<=PA<=P1<=P3 ordering; success (adopt) rates per arm.
- AH6 MECHANISM (informative): rg=2, 16 pairs:
  (a) inversion counts: expect
  inv(P3) > inv(P1) >= inv(PA) >= inv(P0)=0 -- pressure
  discarding higher-raw longer members;
  (b) bestlen: expect mean bestlen(P0/PA) >= mean
  bestlen(P3) -- lower plen retains longer variants;
  (c) early bestraw: GEN bestraw at g=5, expect
  PA/P0 >= P3 -- low plen keeps higher-raw candidates
  from the start.
- AH7 DETERMINISM: 3/3 byte-identical runs (sha256
  recorded, cmp-checked).
- AH8 GUARDS: build.sh enforces safebin-only PATH,
  python3/python do not resolve, no `python` token,
  no `as *i32`, no `_MODE`, opcode dispatch exactly 1..8,
  no `while.*!(`, exactly one `fn main(`.

## Predictions (not bars)

AH1 PASS (port is near-verbatim). AH2 PASS (the never-worse
shape held in 24/24 arms; expect it to replicate). AH3 lean
FAIL: with mostly ties and ~3-6 strict wins expected, the
one-sided sign test likely lands above 0.05. AH4a (PA ~= P0):
the granularity lane attributed the gap to plen=0 itself.
Overall lean: INCOMPLETE (suggestive) or COMPLETE
(reframed) -- the "rescued as adaptivity" outcome is not
expected.

## Verdict mapping (frozen)

- AH1 FAIL -> INCOMPLETE (port broken; no inference
  licensed).
- AH1 PASS, AH2 FAIL -> INCOMPLETE (negative): the PA cost
  edge does not replicate on fresh seeds; best explanation
  is RNG/history artifact, and the granularity lane's sign
  reversal does not generalize.
- AH1+AH2 PASS, AH3 FAIL -> INCOMPLETE (suggestive, not
  significant): the never-worse / sporadically-better shape
  replicates but does not reach p<0.05. The adaptive concept
  is not rescued as a robust optimizer; "lower plen helps or
  is neutral" stands as a weak effect.
- AH1+AH2+AH3 PASS -> COMPLETE, with the interpretation
  fixed by AH4:
  - AH4a -> COMPLETE (reframed): lower revise-phase plen is
    robustly beneficial vs plen=3, but the benefit is the
    LEVEL, not the adaptive ramp. The adaptive PLEN concept
    as adaptivity is NOT rescued; what survives is "no/low
    length pressure during revise beats plen=3".
  - AH4b -> COMPLETE (rescued): the adaptive 0->1 ramp
    adds value beyond fixed low plen.
  - neither AH4a nor AH4b -> COMPLETE (advantage confirmed;
    adaptivity contribution indeterminate -- report the
    thermostat-firing stratification).

## Honesty notes (preregistered)

- 16 pairs is small; the sign test is exact but low-powered,
  and ties dominate the expected outcome. A FAIL on AH3 is
  informative, not a design flaw.
- The P0 hold arm is a researcher-owned ablation, not
  learner behavior; it isolates the level, nothing more.
- "Adaptive" here is the revise-phase 0->1 thermostat only,
  not the full create-phase 0->1->2 ramp of the parent lane.
- Cost conflates speed-to-adopt with success; adopt rates
  and best-raw quality are reported separately (AH5/AH6).
- Fresh seeds are the same generator family with new
  constants: independent draws from the same distribution,
  not a new distribution.
- If the thermostat never fires on fresh seeds, PA is
  plen-0-fixed there; AH4a then measures exactly that.
