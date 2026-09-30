# PREREG: F3 REVISE OOD Test (Pipeline Step 7)

Status: FROZEN. This prereg is committed alone before any OOD world
file, build script, binary, or run exists. No OOD world file existed
at freeze time.

Parent chain: design ca157c743, builder prereg c197e7cd8, builder
result 7009d711c (REVISE-PASS), sealed prereg 8cdf0992a, sealed
result 1df8addec (REVISE-SEALED-PASS), repro 7407dd4a7
(REVISE-REPRO-PASS), baseline prereg 4786633c5 plus amendment
db585360a, baseline result c810d5f55 (REVISE-BASELINE-PASS), attack
prereg 12da75511, attack result bbdb65c99 (REVISE-ATTACK-SURVIVES).
This is pipeline step 7 (OOD test) only.

## 1. Frozen learner

The OOD runs use the frozen learner byte-for-byte:
`revise_attack/f3_revise_frozen.zag`, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
(verified before any run; verified again at build time). The learner
is concatenated with each OOD world exactly as in the sealed runs.
No learner modification of any kind.

## 2. OOD axes

Two distribution-shift axes, both outside every world the learner
has seen (builder worlds, sealed S-CONJ2/S-NEG2, attack S-RK):

Axis A (S-OOD-D3): delay shift WITHIN the frozen delay currency.
Sealed truth Y(t) = X(t-2) AND NOT Z(t-2) becomes
Y(t) = X(t-3) AND NOT Z(t-3). Passive: env SETs X at t=1,7;
Y=1 at t=4,10. Goal setup: Z=1 inhibitor at t=0 (as in S-NEG2).
Vars: X(0,ctrl), Z(1,ctrl), Y(2). w_plan_maxd=8. Goal mode 0.

Axis B (S-OOD-D6): delay shift BEYOND the frozen delay currency
(dcur=4, literal inventory delays 1..4). Sealed truth becomes
Y(t) = X(t-6). Passive: env SETs X at t=3,9; Y=1 at t=9 (t=15 is
outside the 0..11 passive trace). Goal setup: all zero. Vars:
X(0,ctrl), Z(1,ctrl), Y(2). w_plan_maxd=8. Goal mode 0.

Both worlds are new files authored AFTER this prereg freezes.
Diff discipline: each world is written fresh in the sealed-world
style (same ws layout, same harness fns); no sealed world text is
copied except the structural template.

## 3. Frozen predictions

### 3.1 S-OOD-D3 (predicted: D1 revision succeeds at delay 3)

Mechanism analysis (frozen learner source):
- OP-PROP scans delays 1..4. Candidates for Y: [X@3] only
  (ok=2 at t=1,7; every other (c,pol,d) refutes: Z never pulsed,
  X at other delays misaligns).
- Trial [SX,W,W,W,OY] on the fresh world: Y(3)=X(0) AND NOT Z(0)=1.
  RULE_CONFIRMED.
- Goal attempt 1: planner enumerates d=1..8; first sim-valid plan is
  [SX,W,W,W] (SET X at t=0, advance to t=3). Real world: Z(0)=1, so
  Y(3)=X(0) AND NOT Z(0)=0. GOAL_REAL 0.
- D1 fires: GOAL_FAIL_GROW_ATTEMPT. Grow search at t_ref=3 over
  (c,pol,d) FALSE at t_ref and TRUE at all passive true positives:
  first accepted is (Z,0,3), i.e. !Z@3. (c=X variants fail
  condition (b); (Z,0,1) and (Z,0,2) are TRUE at t_ref, failing
  condition (a).)
- Goal attempt 2: first sim-valid plan for [X@3 & !Z@3] is
  [SX,CZ,W,W,W] (clear the inhibitor at t=0, advance to t=3).
  Real world: Y(3)=X(0) AND NOT Z(0)=1. GOAL_REAL 1.
- FINALRULE V=Y rule=0 [X@3 & !Z@3].

Frozen bar OOD-D3-PASS (all must hold on all 3 runs):
- (a) line "F3P3 GOAL_REAL 0 (attempt 1)" present.
- (b) line "F3P3 GOAL_FAIL_GROW_ATTEMPT" present.
- (c) line "F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@3" present.
- (d) line "F3P3 GOAL_REAL 1 (attempt 2)" present.
- (e) line "F3P3 FINALRULE V=Y rule=0 [X@3 & !Z@3]" present.
- (f) 3/3 byte-identical stdout, exit 0, zero stderr bytes.

Note on the RESULT line: the frozen learner's verdict conjunction
is (goal_ok && drill_ok && split_ok && cost_ok && search_ok). The
sealed evaluator disclosed that the embedded REFUTE-DRILL is
world-calibrated so drill_ok=0 on these worlds (step-6 attack
confirmed the drill is behaviorally inert on every mechanism
line). The RESULT line is therefore predicted to read
"F3P3 RESULT REVISE-FAIL" and is EXCLUDED from the verdict by this
prereg. The verdict rests on (a)-(f) only.

### 3.2 S-OOD-D6 (predicted: honest graceful failure, no hallucination)

Mechanism analysis:
- OP-PROP scans delays 1..4. Y=1 only at t=9 in the passive trace.
  [X@d] for d in 1..4: X=1 at t=3 needs Y(3+d)=1, but 3+d in 4..7
  where Y=0, so ref fires. pol=0 variants ref at t=0. No candidate
  for Y; no candidate for X (backwards) or Z. ne=0.
- L_run emits "F3P3 NE 0" then "F3P3 RESULT PHASE3-FAIL
  no-effect-vars" and returns 1 before the validation loop, the
  drills, and the goal phase.

Frozen bar OOD-D6-PASS (all must hold on all 3 runs):
- (a) line "F3P3 RESULT PHASE3-FAIL no-effect-vars" present.
- (b) NO line containing "GOAL_REAL" anywhere (goal phase never runs).
- (c) line "SEALED DONE mask=1" present.
- (d) 3/3 byte-identical stdout, exit 0, zero stderr bytes.

This is a predicted boundary failure, not a mechanism defect: the
mechanism must not invent a rule, must not crash, and must halt
with the disclosed no-effect-vars stop.

## 4. Verdict rule (frozen)

REVISE-OOD-PASS iff OOD-D3-PASS and OOD-D6-PASS both hold.
Otherwise REVISE-OOD-FAIL. Any crash, hang, non-determinism across
the 3 runs, or nonzero stderr bytes on any run forces
REVISE-OOD-FAIL regardless of the trace lines. The RESULT line
plays no role in the verdict (see 3.1 note).

## 5. Kill bars

- K1: this prereg is committed alone before any OOD world file,
  build script, binary, or run exists (verified by commit ancestry).
- K2: both OOD worlds run 3x each against the frozen learner with
  committed raw logs.
- K3: pure Zag. Shell, znc, git, grep, diff, md5sum, sha256sum
  only. Zero Python at every stage. Shell-only dash check clean.
  No em/en dash bytes in any new file.

## 6. Honest scope (pre-registered)

This tests two OOD axes: delay-parameter generalization within the
frozen currency, and graceful degradation beyond it. It does not
test multi-inhibitor worlds, the 3-literal cap boundary, delays
beyond 6, disjunctive truths, or transfer/reuse. A PASS keeps
REVISE at bounded L2 and advances the pipeline past step 7 only.
