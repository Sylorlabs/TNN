# PREREG: Cross-Domain Grammar to Program L3 Novel Intermediate (COMPILE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/xdomain_l3/` only.
Worker: Cross-Domain L3 Worker (subagent, 2026-10-02).
Parent mandate: test L3 novel intermediate on grammar to program
(Micah priority 2026-10-02 #4: "grammar to program requiring new
intermediate").

## 1. What is being tested

Whether the SAME generic learner machinery that constructed a novel
intermediate for sequence to scalar (composition_l3 FORAGE:
`learner.zag`, reused here VERBATIM) constructs a DIFFERENT novel
intermediate M for a NEW cross-domain pair, grammar to program, where
grammar X and program Y are jointly insufficient for the goal Z.

Design decision (disclosed): `learner.zag` is a byte-identical copy of
`composition_l3/learner.zag` (sha256 recorded in NAMECHECK.md; the file
is not modified). The only new artifacts are the world (grammar
productions, program fuel rules) and the driver (arms, phases, checks).
This is the experiment, not a shortcut: the discriminating prediction
is that the frozen machinery invents M = [ADD R1,R3] here versus
[ADD R0,R2] in FORAGE. If the intermediate's form were baked into the
machinery, it could not differ across worlds. A different invented form
from the same frozen source is the cross-domain L3 evidence.

Concrete scenario (COMPILE):
- X: grammar production recall. Given a rule id, X replays the rule's
  licensed 4-symbol production (opcode weights). X outputs a SEQUENCE.
- Y: program fuel gate. Given a scalar fuel s, Y runs the s-fueled
  canonical program: RUN-OK(1) iff s >= t else FAIL(0). The threshold t
  is learned from direct scalar fuel experience. Y consumes a SCALAR.
- Z: on new grammar rules, decide RUN-OK/FAIL correctly. X alone cannot
  decide (no program procedure; type gap: sequence vs scalar). Y alone
  cannot decide (no grammar input). The bridge is a learned reduction
  seq -> scalar that the source never defines.

The learner must DISCOVER the reduction by constructing a program from
generic primitives, guided only by labeled rule experience. It may not
select it from a menu of reductions. Grammar to program L2
(xdomain_grammar_l2) adapted a licensed length parameter; here no
parameter adaptation can bridge the gap because X's output type and Y's
input type do not meet. A new intermediate is required.

## 2. Frozen learner machinery (disclosed, reused verbatim)

Identical to composition_l3, section 2 of its PREREG (state layout,
X store, label store, Y scalar observations and threshold, M slot and
Mprev slot, register machine with R0..R3 preloaded, frozen op basis
{0=CPY, 1=ADD, 2=SUB, 3=MAX, 4=MIN}, construct() greedy search with
80 candidates per round and strictly positive first-max gain,
refit_threshold(), adapt() with codes 0/1/2/3, decide() with
NO_DECISION=-1). No production data, no hidden world rules, and no
reduction solution live in the learner source. The op basis is the same
disclosed residual researcher footprint as FORAGE and is NOT expandable
to rescue a failed build.

## 3. Frozen world (environment, hidden from the learner)

The world defines grammar productions and the hidden program-run rules.
The learner sees only productions (via X teaching) and outcomes (as
observed labels). The driver generates labels from these rules; the
learner source never calls them.

- Y prior fuel experience (teaches that Y exists and consumes scalars):
  (12,1),(15,1),(11,1),(8,0),(5,0),(9,0).
  Y threshold from this data: t=10 (first-max ascending; 6/6).
- TRUE1 (phase 1): RUN-OK iff e1+e3 >= 10.
- TRUE2 (phase 2): RUN-OK iff e1+e3 >= 14 (stricter fuel criterion).
- TRUE3 (phase 3): RUN-OK iff e1+e2+e3 >= 16 (world change).

Frozen production tables (rule id: [e0,e1,e2,e3], outcome under the
phase rule):

Phase 1 train (labels from TRUE1):
1: [3,7,1,5] ok    2: [9,4,8,6] ok    3: [1,9,2,3] ok
4: [6,2,9,8] ok    5: [8,6,0,3] fail  6: [4,9,7,0] fail
7: [2,1,5,4] fail  8: [7,3,6,5] fail
Phase 1 test:
9: [5,6,2,4] ok   10: [8,1,7,2] fail   11: [0,9,9,5] ok
12: [4,4,4,4] fail

Phase 2 refit (labels from TRUE2):
21: [3,8,1,7] ok  22: [9,5,2,9] ok  23: [6,9,4,4] fail
24: [2,2,8,8] fail
Phase 2 held-out:
25: [1,7,3,8] ok  26: [9,2,6,3] fail

Phase 3 train (labels from TRUE3):
31: [7,6,5,5] ok  32: [2,9,4,5] ok  33: [8,2,3,4] fail
34: [1,9,8,2] ok  35: [5,5,5,5] fail 36: [9,1,7,7] fail
37: [3,3,3,9] fail 38: [6,4,6,6] ok
Phase 3 test:
39: [5,7,5,4] ok  40: [9,1,1,1] fail  41: [2,8,4,5] ok
42: [7,2,2,3] fail

Frozen hand-derived expectations (the implementation must reproduce
them; any deviation is a falsifier, not a tuning opportunity):
- Phase 1 construction from empty: round 1 evaluates 80 candidates;
  baseline score 5/8 (best threshold on R0=e0); ADD R1,R3 (op=1,d=1,
  s=3) is the unique 8/8 candidate (gain 3 over baseline); round 2 finds
  no positive gain; M = [ADD R1,R3] (1 instruction: program bytes
  1,1,3), threshold t=10, train 8/8.
- Menu controls (experiment controls in the world file, NOT learner
  machinery), thresholds fit on phase-1 train (first-max ascending):
  SUM t=25, MAX t=9, MIN t=1, FIRST t=9, LAST t=5. Each misclassifies
  at least one phase-1 test production (SUM on 9, MAX on 9, MIN on
  10, FIRST on 9, LAST on 9).
- Phase 2 adapt: M+t=10 scores 2/4 on refit; threshold refit reaches
  4/4 at t=14; adapt code 1; M structural bytes unchanged; held-out
  2/2.
- Phase 3 adapt: M+t=14 scores 5/8 on train; threshold refit maxes at
  7/8 (t=11); extension finds ADD R0,R2 as the first positive-gain
  append (gain 1); adapt code 2; M' = [ADD R1,R3, ADD R0,R2], t=16,
  test 4/4; old M in Mprev with superseded=1.

## 4. Frozen arms

- ARM-FULL: X taught (rules 1..12), Y taught (prior + phase-1 fit),
  M constructed from train 1..8. Z on test 9..12. Expect 4/4.
- ARM-X-ONLY: X taught, Y absent, M absent. Z on test 9..12. Expect
  0/4 (all NO_DECISION).
- ARM-Y-ONLY: Y taught, X absent. Z on test 9..12. Expect 0/4.
- ARM-MENU (5 controls): X+Y taught; driver applies each menu
  reduction with its train-fit threshold on test 9..12. Expect each
  <= 3/4.
- ARM-NO-M: ARM-FULL state with the M slot wiped before Z. Expect 0/4.

## 5. Kill bars

- K-XD-1 (insufficiency): ARM-X-ONLY == 0/4 AND ARM-Y-ONLY == 0/4 AND
  ARM-FULL == 4/4. X and Y exist and each alone fails Z.
- K-XD-2 (no enumerated solution): frozen grep audit on `learner.zag`
  returns zero hits for every pattern in section 6.
- K-XD-3 (creation trace): the run log shows construction with at
  least one positive-gain round, the final program is non-empty, and
  it scores 8/8 on phase-1 train. The program bytes are printed from
  learner state and must be (1,1,3).
- K-XD-4 (causal necessity): ARM-FULL == 4/4 AND ARM-NO-M == 0/4.
  Removing M restores the X/Y type gap and Z fails.
- K-XD-5 (persistence): the 28 structural bytes of the M slot
  (n@232, gen@233, sup@234, pad@235, program@240..263) dumped after
  phase 1 are byte-identical after phase 2. The threshold field at
  236..239 is Y's adaptive decision parameter (it also lives in Y's
  own slot at 228..231) and is expected to change 10 -> 14 on refit;
  it is excluded from this bar (precedent: composition_l3 ERRATUM-1).
- K-XD-6 (reuse): phase-2 adapt returns code 1 (threshold-only, M
  untouched) AND held-out decisions == 2/2.
- K-XD-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict XDOMAIN-L3-COMPLETE requires all seven PASS with no falsifier
firing.

## 6. Frozen K-XD-2 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e1+e3` (the solution expression)
2. `ADD R1,R3`
3. `3,7,1,5` (production data must not live in the learner)
4. `odd` (no positional concept in the learner)
5. `threshold.*=.*10` (no hardcoded threshold; thresholds come only
   from sweeps over experience)
6. `_MODE` (zero modes allowed)
7. `bridge` (case-insensitive; the intermediate is never a bridge
   handler/mode; conceptual term only, and not used in code at all)

## 7. Frozen falsifiers

- F-NO-CREATE: construction yields an empty program or < 8/8 on train.
- F-MENU-WIN: any menu control reaches 4/4 on phase-1 test.
- F-ABLATE-FAIL: ARM-X-ONLY or ARM-Y-ONLY scores >= 1/4.
- F-NOT-NECESSARY: ARM-NO-M scores >= 1/4.
- F-NO-PERSIST: M structural bytes differ between phase 1 and phase 2.
- F-NO-REUSE: phase-2 adapt code != 1 or held-out < 2/2.
- F-NO-REVISE: phase-3 adapt code != 2 or phase-3 test < 4/4.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN}
  for any reason. This voids the build.
- F-AUDIT: any K-XD-2 pattern matches in learner.zag.
- F-NONDET: the three runs differ by even one byte.
- F-PYTHON: any python/python3 invocation in the worker process tree.

Any falsifier firing voids the corresponding claim; F-NO-CREATE,
F-AUDIT, F-NONDET, F-PYTHON, F-OP-EXPAND void the whole build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer and
one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the register machine, the greedy
  search, and the adapt() policy are researcher-supplied generic
  machinery, frozen here, identical to composition_l3. The L3 claim
  here is about the INTERMEDIATE's form being source-underdetermined
  and history-determined for a new domain pair, not about the basis.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality (Micah C0-C) is
  open future work.
- One world family (grammar production to program fuel). No generality
  claim beyond the demonstrated phases.
- The cross-domain comparison (FORAGE [ADD R0,R2] vs COMPILE
  [ADD R1,R3] from the same frozen learner) is evidence, not a bar.

## 10. Standing non-claims (unchanged)

- This build targets the seven xdomain-L3 bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
