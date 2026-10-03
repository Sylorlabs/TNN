# PREREG: Composition L3 Adversarial World (RELAY)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/composition_l3_adv/` only.
Worker: Composition L3 Red-Team Worker (subagent, 2026-10-02, independent
adversary relative to the FORAGE builder).
Parent mandate: red-team the L3 novel intermediate claim with an
independent adversary-designed world. The FORAGE result
(COMPOSITION-L3-COMPLETE) left C0-C open: its hidden rules were
builder-designed. This prereg seals an adversarial world family designed
by the red-team worker, and freezes the bars the unmodified L3 mechanism
must meet on it.

## 1. What is being tested

Whether the SAME learner mechanism that built `ADD R0,R2` on FORAGE,
run UNMODIFIED, constructs a DIFFERENT novel intermediate on a world
whose hidden rule demands a different structure, and avoids reusing the
FORAGE-specific solution.

Concrete scenario (RELAY), disjoint from FORAGE:
- X: episode recall. Given an episode id, X replays the 4 sensor
  readings observed in that episode. X outputs a SEQUENCE.
- Y: threshold decide. Given a scalar s, Y outputs OPEN(1) iff s >= t
  else CLOSED(0). The threshold t is learned from direct scalar
  experience. Y consumes a SCALAR.
- Z: on new episodes, decide OPEN/CLOSED correctly. X alone cannot
  decide (no decision procedure; type gap: sequence vs scalar). Y alone
  cannot decide (no perceptual input). The bridge is a learned reduction
  seq -> scalar that the source never defines.

The RELAY hidden rules are difference-based, not sum-based. Phase 1:
open iff e0 - e1 >= 4. The FORAGE intermediate (`ADD R0,R2`, i.e.
e0 + e2) is the wrong shape for this world: it must fail here, and the
learner must discover `SUB R0,R1` instead.

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

## 3. Frozen world (RELAY; environment, hidden from learner)

The world defines episodes and the hidden labeling rules. The learner
sees only sequences (via X teaching) and labels (as observed outcomes).
The driver generates labels from these rules; the learner source never
calls them. The adversary (this worker) designed the rules and tables;
the FORAGE builder had no input.

- Y prior scalar experience (teaches that Y exists and consumes
  scalars; identical generic teaching as FORAGE):
  (12,open),(15,open),(11,open),(8,closed),(5,closed),(9,closed).
  Y threshold from this data: t=10 (first-max ascending; 6/6).
- TRUE1 (phase 1): open iff e0 - e1 >= 4.
- TRUE2 (phase 2): open iff e0 - e1 >= 6 (stricter margin).
- TRUE3 (phase 3): open iff e0 - e1 + e3 >= 8 (third channel assists).

Frozen episode tables (id: [e0,e1,e2,e3], label under the phase rule):

Phase 1 train (labels from TRUE1):
1: [5,0,9,9] open    2: [6,1,2,2] open    3: [4,0,7,3] open
4: [8,3,1,1] open    5: [9,7,0,5] closed  6: [7,6,4,4] closed
7: [3,5,8,8] closed  8: [2,1,6,6] closed
Phase 1 test:
9: [7,2,5,0] open   10: [9,8,1,9] closed
11: [5,0,3,7] open  12: [6,4,2,2] closed

Phase 2 refit (labels from TRUE2):
21: [8,1,4,2] open  22: [9,3,0,5] open
23: [7,3,8,1] closed  24: [5,5,2,9] closed
Phase 2 held-out:
25: [9,2,6,3] open  26: [4,3,1,1] closed

Phase 3 train (labels from TRUE3):
31: [9,1,0,2] open  32: [7,0,5,3] open  33: [6,2,1,5] open
34: [8,3,4,4] open  35: [9,2,0,0] closed  36: [8,3,1,1] closed
37: [4,0,9,2] closed  38: [5,4,2,5] closed
Phase 3 test:
39: [9,2,0,3] open  40: [5,1,7,1] closed
41: [8,4,2,5] open  42: [6,5,3,4] closed

Frozen hand-derived expectations (verified by independent shell
arithmetic before this commit; the implementation must reproduce them;
any deviation is a falsifier, not a tuning opportunity):
- Phase 1 construction from empty: round 1 evaluates 80 candidates;
  baseline (empty program, R0=e0) scores 6/8 at t=4; SUB R0,R1
  (op=2,d=0,s=1) is the UNIQUE 8/8 candidate (gain 2, first-max
  threshold t=3); round 2 finds no positive gain; M = [SUB R0,R1]
  (1 instruction: bytes 2,0,1), threshold t=3, train 8/8.
- Rejected alternatives probed by the driver on phase-1 train:
  FORAGE-ADD-R0-R2 5/8 t=12, SUB-R0-R3 5/8 t=0, MAX-R0-R3 4/8 t=0,
  MIN-R0-R2 5/8 t=1, ADD-R0-R3 4/8 t=0, CPY-R0-R1 4/8 t=0.
  The FORAGE solution scores 5/8 here: it does not transfer.
- Menu controls (experiment controls in the world file, NOT learner
  machinery), thresholds fit on phase-1 train (first-max ascending):
  SUM 4/8 t=0, MAX 4/8 t=0, MIN 4/8 t=0, FIRST 6/8 t=4, LAST 5/8 t=9.
  On phase-1 test: SUM 2/4, MAX 2/4, MIN 2/4, FIRST 2/4, LAST 1/4.
  Each misclassifies at least one test episode.
- Phase 2 adapt: M+t=3 scores 3/4 on refit; threshold refit reaches 4/4
  at t=5; adapt code 1; M program bytes unchanged; held-out 2/2 at t=5.
- Phase 3 adapt: M+t=5 scores 5/8 on train; threshold refit best is 5/8
  (t=2); extension round 1 from [SUB R0,R1]: baseline 5/8, ADD R0,R3
  (op=1,d=0,s=3) is the UNIQUE 8/8 append (gain 3, t=8); round 2 stops;
  adapt code 2; M' = [SUB R0,R1, ADD R0,R3] (bytes 2,0,1,1,0,3), t=8,
  test 4/4; old M in Mprev with superseded=1.

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
- ARM-FORAGE-PROBE: driver evaluates the FORAGE intermediate
  [ADD R0,R2] on RELAY phase-1 train with best threshold. Expect < 8/8
  (frozen: 5/8). This is the anti-transfer check.

## 5. Kill bars

- K-ADV-1 (insufficiency): ARM-X-ONLY == 0/4 AND ARM-Y-ONLY == 0/4 AND
  ARM-FULL == 4/4. X and Y exist and each alone fails Z.
- K-ADV-2 (no enumerated solution): frozen grep audit on the copied
  `learner.zag` returns zero hits for every pattern in section 6, AND
  sha256 matches the frozen FORAGE learner hash (F-LEARNER-MODIFIED
  otherwise).
- K-ADV-3 (creation trace): the run log shows construction with at
  least one positive-gain round, the final program is non-empty, is NOT
  the FORAGE program bytes (1,0,2), and scores 8/8 on phase-1 train.
  The program bytes are printed from learner state.
- K-ADV-4 (causal necessity): ARM-FULL == 4/4 AND ARM-NO-M == 0/4.
  Removing M restores the X/Y type gap and Z fails.
- K-ADV-5 (persistence): the 28 structural bytes of the M slot
  (n, gen, sup, pad, 24 program bytes; threshold field excluded per the
  FORAGE ERRATUM-1 rationale, which carries over unchanged) dumped
  after phase 1 are byte-identical after phase 2.
- K-ADV-6 (reuse): phase-2 adapt returns code 1 (threshold-only, M
  untouched) AND held-out decisions == 2/2.
- K-ADV-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict COMPOSITION-L3-ADV-COMPLETE requires all seven PASS with no
falsifier firing.

## 6. Frozen K-ADV-2 grep audit spec (run on the copied learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e0-e1` (the phase-1 solution expression; also covers e0-e1+e3)
2. `SUB R0,R1` (the phase-1 solution instruction)
3. `ADD R0,R3` (the phase-3 revision instruction)
4. `5,0,9,9` (episode data must not live in the learner)
5. `set32(st,236,3)` (no hardcoded phase-1 M threshold)
6. `set32(st,228,3)` (no hardcoded Y threshold of 3)
7. `_MODE` (zero modes allowed)
8. `bridge` (case-insensitive; never used in code at all)

## 7. Frozen falsifiers

- F-NO-CREATE: construction yields an empty program, the FORAGE program
  bytes (1,0,2), or < 8/8 on train.
- F-MENU-WIN: any menu control reaches 4/4 on phase-1 test.
- F-ABLATE-FAIL: ARM-X-ONLY or ARM-Y-ONLY scores >= 1/4.
- F-NOT-NECESSARY: ARM-NO-M scores >= 1/4.
- F-NO-PERSIST: M structural bytes differ between phase 1 and phase 2.
- F-NO-REUSE: phase-2 adapt code != 1 or held-out < 2/2.
- F-NO-REVISE: phase-3 adapt code != 2 or phase-3 test < 4/4.
- F-FORAGE-REUSE: the FORAGE probe reaches 8/8 on RELAY phase-1 train.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN} for
  any reason. This voids the build.
- F-LEARNER-MODIFIED: the copied learner.zag sha256 differs from
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b.
  This voids the build.
- F-AUDIT: any K-ADV-2 pattern matches in the copied learner.zag.
- F-NONDET: the three runs differ by even one byte.
- F-PYTHON: any python/python3 invocation in the worker process tree.

Any falsifier firing voids the corresponding claim; F-NO-CREATE,
F-AUDIT, F-NONDET, F-PYTHON, F-OP-EXPAND, F-LEARNER-MODIFIED void the
whole build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer and
one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN} and the register machine are
  researcher-supplied generic machinery, frozen here and byte-identical
  to the FORAGE build. The L3 claim here is about the intermediate's
  form being source-underdetermined and history-determined, not about
  the basis.
- The hidden world rules were designed by the red-team worker
  (independent adversary relative to the FORAGE builder), sealed in this
  prereg before any implementation existed. This addresses the FORAGE
  honest boundary (builder-designed rules, C0-C open) for one
  additional world family. One adversarial family does not establish
  broad generality.
- One world family (relay gating). No generality claim beyond the
  demonstrated phases.
- The driver and world files are new experiment-side code for RELAY;
  only learner.zag is the frozen mechanism under test.

## 10. Standing non-claims (unchanged from FORAGE)

- This build targets the seven composition-L3 bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
