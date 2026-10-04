# Preregistration: H-EXP8 Red Team (X-E8-1..X-E8-4)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
attack fixture is written, any build is run, or any attack
code is executed. No Python at any stage.

## Mission

Independently attack the H-EXP8 repair claim (causal/adv/
EXP8_RESULT.md, H-EXP8 SURVIVES 5/5). Assume it is false.
H-EXP8's repair claim, quoted from EXP8_RESULT.md:

1. "the clamp-artifactual from-bucket is flagged and its raw
   from-values are shown" (closes X-E7-1).
2. "the attempt-conditioned rate is visible; the two
   materially different realities no longer render
   identically" (closes X-E7-2).
3. "the clamp-rendered self-loop is explicitly flagged"
   (closes X-E7-3).

Causal interpretation under test: "a planner that reads the
annotations as documented can no longer mistake a clamp
artifact for a from-state observation, mistake an
outcome-conditioned rate for an attempt-conditioned one, or
mistake a clamp-rendered self-loop for a maintained state."

Documented honest limits (PREREG_EXP8.md, frozen): the raw
tag is a per-bucket observed range, not per-episode and not
a distribution ("two buckets with the same range may hide
different distributions"); from-att does not condition on
other variables or episode order and is not a success
probability under intervention; the `*` flag is deductive.

## Attack fixtures (all S1-based, action 0, temp variable)

S1 = causal/cum_B.txt (11 episodes). All attack fixtures
append the listed episodes to S1 verbatim. Fixture format:
`T <t> <p> <l> | <a> | <nt> <npr> <nl>`.

### X-E8-1a: raw-range distribution hiding

- D1 = S1 + 9x `T 5 0 0 | 0 | 2 0 0` (raw 5->2, artifactual
  from-2) + 1x `T 2 0 0 | 0 | 3 0 0` (raw 2->3, genuine
  from-2 change; clamped 2->2).
- D2 = S1 + 1x `T 5 0 0 | 0 | 2 0 0` + 9x
  `T 2 0 0 | 0 | 3 0 0`.

Both put 10 change episodes in cell (a=0,v=temp,o=2,x=2).
D1 is 90% artifactual; D2 is 10% artifactual. Frozen
expectation: both render the from-bucket identically as
`2:10*(raw:2..5)` (rmin=2, rmax=5 in both; rdiff 9 vs 1,
both >0 so the tag renders; the count c=10 and the range
2..5 are identical).

Kill criterion: DOWNGRADED if D1 and D2 render the bucket
identically AND a planner reading the annotations as
documented would draw a materially wrong conclusion about
the reliability of from-2 evidence that the frozen
documentation does not warn against. If the identical
rendering matches the documented limit ("two buckets with
the same range may hide different distributions") and no
further planner harm is demonstrated, this attack FAILS
and the limit is recorded as an empirically CONFIRMED
BOUNDARY.

### X-E8-1b: raw to-value invisibility

- D3 = S1 + 1x `T 5 0 0 | 0 | 9 0 0` (raw 5->9; clamped
  2->2).
- Control C1 (frozen H-EXP7 fixture) = S1 + 1x
  `T 5 0 0 | 0 | 2 0 0` (raw 5->2; clamped 2->2).

Frozen expectation: both render cell (0,temp,2,2) as
`2->2:1*` / bucket `2:1*(raw:5..5)`. The raw OUTCOME (9 vs
2) is recorded nowhere: rmin/rmax/rdiff track raw
from-values only.

Kill criterion: DOWNGRADED if the indistinguishability
falsifies a repair claim. The repair claims only raw
FROM-values; the to-value clamp is outside the frozen
claim, so the expected finding is a NEW HONEST LIMIT
(boundary), not a downgrade, unless the evidence shows a
planner misreading that the documentation affirmatively
invites. This attack is primarily boundary-mapping; it
FAILs as a kill and the boundary is recorded.

### X-E8-2a: raw attempt-profile invisibility

- E1 = S1 + 1x `T 2 0 0 | 0 | 0 0 0` (raw 2->0 change) +
  10x `T 2 0 0 | 0 | 2 0 0` (raw 2->2 no-ops).
- E2 = S1 + 1x `T 2 0 0 | 0 | 0 0 0` +
  10x `T 5 0 0 | 0 | 5 0 0` (raw 5->5 no-ops; clamped
  from 2).

Frozen expectation: E1 and E2 render byte-identically.
The 10 no-ops differ in raw from-value (2 vs 5) but both
clamp to from-bucket 2; rmin/rmax/rdiff record change
episodes only, so the no-ops' raw profile is invisible;
from-att counts clamped from-values (12 in bucket 2 for
both, counting the S1 base `T 2 0 0 | 0 | 2 0 0`).

Kill criterion: DOWNGRADED if E1 and E2 render
byte-identically AND the 10/11-vs-1/11 genuine-from-2
attempt composition is material to a planner in a way the
documentation does not cover. The documentation states
from-att counts clamped from-values; raw attempt profiles
are outside the claim. Expected: identical rendering,
recorded as CONFIRMED BOUNDARY, attack FAILS as a kill.

### X-E8-2b: episode-order invisibility

- F1 = S1 + 1x `T 0 0 0 | 0 | 2 0 0` then 10x
  `T 0 0 0 | 0 | 0 0 0` (change first).
- F2 = S1 + 10x `T 0 0 0 | 0 | 0 0 0` then 1x
  `T 0 0 0 | 0 | 2 0 0` (change last).

Frozen expectation: byte-identical rendering. The honest
limit documents "does not condition on ... episode
order". Expected: CONFIRMED BOUNDARY, attack FAILS as a
kill. DOWNGRADED only if order-sensitivity is shown to be
planner-material beyond the documented limit.

### X-E8-3a: self-loop flag audit (deductive claim)

- G1 = S1 + `T 2 0 0 | 0 | 3 0 0` (raw 2->3) +
  `T 2 0 0 | 0 | 5 0 0` (raw 2->5) +
  `T 2 0 0 | 0 | 9 0 0` (raw 2->9) +
  `T 5 0 0 | 0 | 2 0 0` (raw 5->2) +
  `T 5 0 0 | 0 | 6 0 0` (raw 5->6) +
  `T 3 0 0 | 0 | 4 0 0` (raw 3->4).

All six are genuine raw changes with clamped (o=2,x=2).
Frozen expectation: TRANSITION TABLE contains `2->2:6*`
(the S1 base has no genuine (2,2) temp change by action 0;
J1/C1 are separate fixtures, not included); every `*` in
the table and in from-buckets sits on a genuine raw
change; no o==x cell lacks `*`.

Kill criterion: KILL the deductive claim (downgrade
H-EXP8) if any `*` appears on a cell that is not a
genuine raw change, or any o==x cell is rendered without
`*`. This attack FAILS (defense holds) if the audit is
clean.

### X-E8-3b: non-change exclusion

- H1 = S1 + `T 2 0 0 | 0 | 2 0 0` (raw 2->2: not a change) +
  `T 5 0 0 | 0 | 5 0 0` (raw 5->5: not a change).

Frozen expectation: no `2->2` cell appears in the
TRANSITION TABLE for action 0 temp (the change predicate
is raw ns != raw os; S1 base has no genuine (2,2)
change). The added episodes must affect only from-att
counts, never trans cells.

Kill criterion: KILL/DOWNGRADE if a trans cell is created
for a raw non-change (ns == raw os). FAILS (defense
holds) if no such cell appears.

### X-E8-4: regression

Rebuild the committed exp_invent8.zag unmodified with
znc 2026.07.0-dev (edition 2026); run all 11 frozen
fixtures (S1,S2,S0,A1,F1,G1,H1,J1,R1,C1,r1_e8_ctrl) 3x;
byte-compare against the committed evidence files
(causal/adv/evidence/exp8_*.txt).

Kill criterion: any byte mismatch vs the committed raw on
any fixture, or any non-determinism across the 3 runs, is
a KILL pending investigation (a silent behavior change
invalidates the 5/5 claim).

## Verdict rules (frozen)

- H-EXP8 is KILLED or DOWNGRADED if any attack meets its
  kill criterion with the planner-harm demonstrated.
- Attacks that confirm documented honest limits are
  recorded as CONFIRMED BOUNDARIES, not kills.
- All 5/5 frozen H-EXP8 bars are assumed intact unless
  X-E8-4 or a new attack breaks one; this red team does
  not re-litigate K-E8-1..K-E8-5 except via X-E8-4.
- Pure Zag throughout: hand-written fixtures, znc builds
  in /tmp only (never committed), cmp/md5sum/grep/diff
  for comparison. No Python at any stage.

## Deliverable

EXP8_ADV_RESULT.md + attack fixtures (d1,e1,e2,f1,f2,g1,
h1,d3 as d3_e8_adv.txt etc.) + raw evidence, committed to
tnn-native-lab under causal/adv/. Only adversary-owned
paths staged.
