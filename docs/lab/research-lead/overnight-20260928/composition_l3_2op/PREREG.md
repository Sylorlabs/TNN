# PREREG: Composition L3 Two-Op First Creation (LEDGER)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/composition_l3_2op/` only.
Worker: Composition L3 2-Op First-Creation Worker (subagent, 2026-10-02).
Parent mandate: test L3 invention requiring a 2-operation intermediate
from scratch. FORAGE built `ADD R0,R2` (1 op) in first creation, then
extended to 2 ops on revision. RELAY built `SUB R0,R1` (1 op), then
extended to 2 ops on revision. Open: can the learner invent a 2-op
intermediate in the FIRST creation, not via later revision?

## 1. What is being tested

Whether the SAME learner mechanism that built 1-op intermediates on
FORAGE and RELAY, run UNMODIFIED, constructs a 2-OPERATION intermediate
in its first fresh construction on a world where NO single op from
{CPY,ADD,SUB,MAX,MIN} suffices.

Concrete scenario (LEDGER), disjoint from FORAGE and RELAY:
- X: episode recall. Given an episode id, X replays the 4 sensor
  readings observed in that episode. X outputs a SEQUENCE.
- Y: threshold decide. Given a scalar s, Y outputs CLEAR(1) iff s >= t
  else HOLD(0). The threshold t is learned from direct scalar
  experience. Y consumes a SCALAR.
- Z: on new episodes, decide CLEAR/HOLD correctly. X alone cannot
  decide (no decision procedure; type gap: sequence vs scalar). Y alone
  cannot decide (no perceptual input). The bridge is a learned reduction
  seq -> scalar that the source never defines.

The LEDGER hidden rules are credit-minus-debit shaped. Phase 1: clear
iff e0+e1-e2 >= 6. The correct intermediate is the 2-op program
[ADD R0,R1, SUB R0,R2] (R0 = e0+e1-e2). No single instruction reaches
perfect classification on the phase-1 train set: the best 1-op scores
7/8. The learner must therefore compose TWO ops in first creation.

## 2. Frozen learner machinery (disclosed, UNMODIFIED)

`learner.zag` is copied byte-identical from
`docs/lab/research-lead/overnight-20260928/composition_l3/learner.zag`
(sha256 9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b).
No episode data, no hidden world rules, no aggregation solution live in
it. Falsifier F-LEARNER-MODIFIED fires if the copy's sha256 differs.

State, op basis {0=CPY, 1=ADD, 2=SUB, 3=MAX, 4=MIN}, register machine
(R0..R3 preloaded, output R0), greedy construct() (80 candidates per
round, strictly positive gain, first-max ties, 8-instruction cap),
refit_threshold(), adapt() codes 0/1/2/3, decide() with -1 NO_DECISION:
all exactly as documented in the FORAGE prereg section 2. Nothing is
re-disclosed here because nothing changes.

Note on candidate semantics (used in the hand derivation): a candidate
with d != 0 leaves R0 untouched, so it always scores exactly the round
baseline (gain 0, never selected). The 20 distinct d=0 candidates are
the effective search space per round.

## 3. Frozen world (LEDGER; environment, hidden from learner)

The world defines episodes and the hidden labeling rules. The learner
sees only sequences (via X teaching) and labels (as observed outcomes).
The driver generates labels from these rules; the learner source never
calls them.

- Y prior scalar experience (teaches that Y exists and consumes
  scalars; identical generic teaching as FORAGE/RELAY):
  (12,clear),(15,clear),(11,clear),(8,hold),(5,hold),(9,hold).
  Y threshold from this data: t=10 (first-max ascending; 6/6).
- TRUE1 (phase 1): clear iff e0+e1-e2 >= 6.
- TRUE2 (phase 2): clear iff e0+e1-e2 >= 9 (stricter margin).
- TRUE3 (phase 3): clear iff e0+e1-e2+e3 >= 9 (third channel assists).

Frozen episode tables (id: [e0,e1,e2,e3], label under the phase rule):

Phase 1 train (labels from TRUE1):
1: [2,9,5,0] clear   2: [9,1,4,8] clear
3: [7,6,7,2] clear   4: [5,4,2,3] clear
5: [9,5,9,4] hold    6: [8,0,3,5] hold
7: [1,7,6,6] hold    8: [3,2,1,7] hold
Phase 1 test:
9: [8,4,5,1] clear   10: [3,3,6,9] hold
11: [6,7,6,0] clear  12: [1,2,4,5] hold

Phase 2 refit (labels from TRUE2):
21: [9,8,7,0] clear  22: [8,9,6,1] clear
23: [9,5,8,2] hold   24: [7,6,7,3] hold
Phase 2 held-out:
25: [9,9,8,4] clear  26: [5,4,5,5] hold

Phase 3 train (labels from TRUE3):
31: [9,6,6,0] clear  32: [8,7,8,4] clear
33: [5,9,4,1] clear  34: [7,3,5,6] clear
35: [9,2,3,0] hold   36: [0,0,9,9] hold
37: [4,4,4,1] hold   38: [1,1,8,8] hold
Phase 3 test:
39: [9,3,2,2] clear  40: [5,5,5,5] clear
41: [8,4,6,1] hold   42: [2,2,2,8] clear

Frozen hand-derived expectations (verified by independent awk
re-implementation of the learner's scoring semantics before this
commit; the implementation must reproduce them; any deviation is a
falsifier, not a tuning opportunity):
- Phase 1 construction from empty: baseline (empty program, R0=e0)
  scores 5/8 at t=2. Round 1 evaluates 80 candidates; ADD R0,R1
  (op=1,d=0,s=1) is the UNIQUE 7/8 candidate (gain 2, first-max
  threshold t=9). The five earlier-in-order candidates (CPY R0,R0..R3
  at 5/8, ADD R0,R0 at 5/8) all score strictly less; the fourteen later
  d=0 candidates score at most 7/8 (SUB R0,R3 6/8 t=0, MIN R0,R2 6/8
  t=2, rest at most 5/8); every d != 0 candidate scores the 5/8
  baseline. No single instruction reaches 8/8. Round 2 from
  [ADD R0,R1]: SUB R0,R2 (op=2,d=0,s=2) is the UNIQUE 8/8 candidate
  (gain 1, first-max threshold t=6); all earlier candidates score at
  most 7/8 (MAX R0,Rs 7/8 t=9); every d != 0 candidate scores the 7/8
  baseline. Round 3 finds no positive gain and stops.
  M = [ADD R0,R1, SUB R0,R2] (2 instructions: bytes 1,0,1,2,0,2),
  threshold t=6, train 8/8.
- Rejected 1-op alternatives probed by the driver on phase-1 train:
  ADD-R0-R1 7/8 t=9 (round-1 winner, imperfect), SUB-R0-R2 5/8 t=3,
  SUB-R0-R3 6/8 t=0, MIN-R0-R2 6/8 t=2, ADD-R0-R3 5/8 t=14,
  CPY-R0-R0 5/8 t=2. The FORAGE program [ADD R0,R2] scores 5/8 here
  and the RELAY program [SUB R0,R1] scores 4/8: neither transfers.
- Menu controls (experiment controls in the world file, NOT learner
  machinery), thresholds fit on phase-1 train (first-max ascending):
  SUM 5/8 t=14, MAX 5/8 t=9, MIN 5/8 t=2, FIRST 5/8 t=2, LAST 5/8 t=8.
  On phase-1 test: SUM 3/4, MAX 1/4, MIN 1/4, FIRST 3/4, LAST 1/4.
  Each misclassifies at least one test episode.
- Phase 2 adapt: M+t=6 scores 2/4 on refit; threshold refit reaches 4/4
  at t=7; adapt code 1; M structural bytes unchanged; held-out 2/2
  at t=7.
- Phase 3 adapt: M(v)+t=7 scores 6/8 on train; threshold refit best is
  7/8 (t=5); extension round 1 from [ADD R0,R1, SUB R0,R2]: baseline
  7/8, ADD R0,R3 (op=1,d=0,s=3) is the UNIQUE 8/8 append (gain 1,
  t=9); all earlier candidates score at most 7/8 (CPY R0,R0 7/8 t=5,
  CPY R0,R1 7/8 t=3, ADD R0,R0/R1/R2 7/8); round 2 stops; adapt code 2;
  M' = [ADD R0,R1, SUB R0,R2, ADD R0,R3] (bytes 1,0,1,2,0,2,1,0,3),
  t=9, test 4/4; old M in Mprev with superseded=1.

## 4. Frozen arms

- ARM-FULL: X taught (episodes 1..12), Y taught (prior + phase-1 fit),
  M constructed from train 1..8. Z on test 9..12. Expect 4/4.
- ARM-X-ONLY: X taught, Y absent, M absent. Z on test 9..12. Expect 0/4
  (all NO_DECISION).
- ARM-Y-ONLY: Y taught, X absent. Z on test 9..12. Expect 0/4.
- ARM-MENU (5 controls): X+Y taught; driver applies each menu
  aggregation with its train-fit threshold on test 9..12. Expect each
  <= 3/4.
- ARM-NO-M: ARM-FULL state with the M slot wiped before Z. Expect 0/4.

## 5. Kill bars

- K-2OP-1 (insufficiency): ARM-X-ONLY == 0/4 AND ARM-Y-ONLY == 0/4 AND
  ARM-FULL == 4/4 (X/Y type gap), AND the construction trace shows the
  best single-instruction candidate scoring 7/8 < 8/8 (no 1-op
  suffices).
- K-2OP-2 (novelty): frozen grep audit on the copied `learner.zag`
  returns zero hits for every pattern in section 6, AND sha256 matches
  the frozen FORAGE learner hash (F-LEARNER-MODIFIED otherwise). The
  2-op form [ADD R0,R1, SUB R0,R2] is not in source.
- K-2OP-3 (creation + necessity): the run log shows construction with
  exactly two positive-gain rounds, the final program has exactly 2
  instructions, is the byte sequence 1,0,1,2,0,2, and scores 8/8 on
  phase-1 train (first creation, not revision); AND ARM-FULL == 4/4
  AND ARM-NO-M == 0/4 (M is causally necessary).
- K-2OP-4 (persistence): phase-2 adapt returns code 1 (threshold-only,
  M untouched), the 28 structural bytes of the M slot (n, gen, sup,
  pad, 24 program bytes; threshold field excluded per the FORAGE
  ERRATUM-1 rationale, which carries over unchanged) dumped after
  phase 1 are byte-identical after phase 2, AND held-out == 2/2.
- K-2OP-5 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict COMPOSITION-L3-2OP-COMPLETE requires all five PASS with no
falsifier firing.

## 6. Frozen K-2OP-2 grep audit spec (run on the copied learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e0+e1-e2` (the phase-1 solution expression)
2. `ADD R0,R1` (the round-1 instruction)
3. `SUB R0,R2` (the round-2 instruction)
4. `2,9,5,0` (episode data must not live in the learner)
5. `set32(st,236,6)` (no hardcoded phase-1 M threshold)
6. `set32(st,228,6)` (no hardcoded Y threshold of 6)
7. `_MODE` (zero modes allowed)
8. `bridge` (case-insensitive; never used in code at all)

## 7. Frozen falsifiers

- F-ONEOP: construction yields fewer than 2 instructions, the round-1
  winner reaches 8/8, or the final program scores < 8/8 on train.
  (Any of these means 1 op sufficed or 2-op invention failed.)
- F-MENU-WIN: any menu control reaches 4/4 on phase-1 test.
- F-ABLATE-FAIL: ARM-X-ONLY or ARM-Y-ONLY scores >= 1/4.
- F-NOT-NECESSARY: ARM-NO-M scores >= 1/4.
- F-NO-PERSIST: M structural bytes differ between phase 1 and phase 2.
- F-NO-REUSE: phase-2 adapt code != 1 or held-out < 2/2.
- F-NO-REVISE: phase-3 adapt code != 2 or phase-3 test < 4/4.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN} for
  any reason. This voids the build.
- F-LEARNER-MODIFIED: the copied learner.zag sha256 differs from
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b.
  This voids the build.
- F-AUDIT: any K-2OP-2 pattern matches in the copied learner.zag.
- F-NONDET: the three runs differ by even one byte.
- F-PYTHON: any python/python3 invocation in the worker process tree.

Any falsifier firing voids the corresponding claim; F-ONEOP,
F-AUDIT, F-NONDET, F-PYTHON, F-OP-EXPAND, F-LEARNER-MODIFIED void the
whole build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer and
one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN} and the register machine are
  researcher-supplied generic machinery, frozen here and byte-identical
  to the FORAGE and RELAY builds. The L3 claim here is about the
  intermediate's form being source-underdetermined and
  history-determined (now at 2-op complexity in first creation), not
  about the basis.
- The hidden world rules were designed by this worker (the 2-op
  builder), sealed in this prereg before any implementation existed.
  Like RELAY, this addresses builder-designed rules for one additional
  world family; it does not establish broad generality and does not
  claim Micah's full 12-criterion L3 bar.
- One world family (ledger settlement). No generality claim beyond the
  demonstrated phases.
- The driver and world files are new experiment-side code for LEDGER;
  only learner.zag is the frozen mechanism under test.

## 10. Standing non-claims (unchanged from FORAGE/RELAY)

- This build targets the five composition-L3-2OP bars above. It does
  not claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
