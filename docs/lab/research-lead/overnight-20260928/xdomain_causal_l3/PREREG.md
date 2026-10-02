# PREREG: Cross-Domain Causal to Intervention L3 Novel Intermediate (INTERVENE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/xdomain_causal_l3/` only.
Worker: Causal L3 Worker (subagent, 2026-10-02).
Parent mandate: test L3 novel intermediate on causal to intervention
(Micah priority 2026-10-02 #4: "causal to intervention requiring
adaptation"). Prior L3 demonstrations: sequence to scalar (FORAGE,
composition_l3), grammar to program (COMPILE, xdomain_l3). Open: does
the same frozen machinery invent a novel intermediate for a
causal to intervention pair?

## 1. What is being tested

Whether the SAME generic learner machinery that constructed a novel
intermediate for sequence to scalar (composition_l3 FORAGE:
`learner.zag`) and for grammar to program (xdomain_l3 COMPILE, same
file reused verbatim) constructs a DIFFERENT novel intermediate M for
a NEW cross-domain pair, causal observation to intervention, where a
causal model X and an intervention gate Y are jointly insufficient
for the goal Z.

Design decision (disclosed): `learner.zag` will be a byte-identical
copy of `composition_l3/learner.zag` (sha256 recorded in NAMECHECK.md;
the file is not modified). The only new artifacts are the world
(causal observation scenarios, intervention outcome rules) and the
driver (arms, phases, checks). This is the experiment, not a
shortcut: the discriminating prediction is that the frozen machinery
invents M = [ADD R0,R1] here versus [ADD R0,R2] in FORAGE and
[ADD R0,R3] in COMPILE. If the intermediate's form were baked into the
machinery, it could not differ across worlds. A third distinct
invented form from the same frozen source is the cross-domain L3
evidence.

Concrete scenario (INTERVENE):
- X: causal observation recall. Given a scenario id, X replays the 4
  readings observed in that scenario: two causal-antecedent readings
  (e0, e1) and two downstream readings (e2, e3). X outputs a SEQUENCE.
- Y: intervention gate. Given an intervention strength scalar s, Y
  outputs ACT(1) iff s >= t else SKIP(0). The threshold t is learned
  from direct scalar strength experience. Y consumes a SCALAR.
- Z: on new causal scenarios, decide ACT/SKIP correctly. X alone
  cannot decide (no decision procedure; type gap: sequence vs
  scalar). Y alone cannot decide (no causal observations). The bridge
  is a learned reduction seq -> scalar that the source never defines.

The learner must DISCOVER the reduction by constructing a program
from generic primitives, guided only by labeled scenario experience.
It may not select it from a menu of reductions.

## 2. Frozen learner machinery (disclosed, reused verbatim)

Identical to composition_l3, section 2 of its PREREG (state layout,
X store, label store, Y scalar observations and threshold, M slot and
Mprev slot, register machine with R0..R3 preloaded and R0 as output,
frozen op basis {0=CPY, 1=ADD, 2=SUB, 3=MAX, 4=MIN}, construct()
greedy search with 80 candidates per round and strictly positive
first-max gain, refit_threshold(), adapt() with codes 0/1/2/3,
decide() with NO_DECISION=-1). No scenario data, no hidden world
rules, and no reduction solution live in the learner source. The op
basis is the same disclosed residual researcher footprint as FORAGE
and COMPILE and is NOT expandable to rescue a failed build.

## 3. Frozen world (environment, hidden from the learner)

The world defines causal observation scenarios and the hidden
intervention outcome rules. The learner sees only scenarios (via X
teaching) and outcomes (as observed labels). The driver generates
labels from these rules; the learner source never calls them.

- Y prior strength experience (teaches that Y exists and consumes
  scalars): (12,1),(15,1),(11,1),(8,0),(5,0),(9,0).
  Y threshold from this data: t=10 (first-max ascending; 6/6).
- TRUE1 (phase 1): ACT iff e0+e1 >= 12 (the two causal antecedents
  jointly warrant intervention).
- TRUE2 (phase 2): ACT iff e0+e1 >= 16 (stricter intervention
  criterion).
- TRUE3 (phase 3): ACT iff e0+e1+e2 >= 18 (world change: the
  downstream reading e2 now contributes to the outcome).

Frozen scenario tables (scenario id: [e0,e1,e2,e3], outcome under the
phase rule):

Phase 1 train (labels from TRUE1):
1: [7,6,1,2] act    2: [6,7,9,0] act    3: [8,5,0,8] act
4: [9,4,9,1] act    5: [9,0,0,1] skip   6: [0,9,1,0] skip
7: [5,5,2,3] skip   8: [4,4,9,9] skip
Phase 1 test:
9: [7,0,0,6] skip  10: [9,9,0,0] act  11: [3,3,8,8] skip
12: [4,9,4,4] act

Phase 2 refit (labels from TRUE2):
21: [9,8,1,2] act  22: [8,9,0,5] act  23: [9,6,5,1] skip
24: [6,6,6,6] skip
Phase 2 held-out:
25: [8,0,0,9] skip  26: [9,9,4,4] act

Phase 3 train (labels from TRUE3):
31: [7,6,6,2] act  32: [6,7,6,0] act  33: [8,5,6,8] act
34: [9,4,6,1] act  35: [9,8,0,6] skip 36: [8,9,0,0] skip
37: [0,1,2,3] skip 38: [9,0,8,1] skip
Phase 3 test:
39: [6,6,6,6] act  40: [9,8,0,0] skip  41: [5,5,8,4] act
42: [7,7,2,1] skip

Frozen hand-derived expectations (the implementation must reproduce
them; any deviation is a falsifier, not a tuning opportunity):
- Phase 1 construction from empty: round 1 evaluates 80 candidates;
  baseline score 7/8 (empty program, R0=e0, best threshold t=6);
  ADD R0,R1 (op=1,d=0,s=1) is the unique 8/8 candidate (gain 1 over
  baseline; nearest rivals ADD R0,R0, MIN R0,R0, MAX R0,R0 reach 7/8,
  gain 0); round 2 finds no positive gain; M = [ADD R0,R1]
  (1 instruction: program bytes 1,0,1), threshold t=11, train 8/8.
- Menu controls (experiment controls in the world file, NOT learner
  machinery), thresholds fit on phase-1 train (first-max ascending):
  SUM t=16, MAX t=6, MIN t=0, FIRST t=6, LAST t=0. Each misclassifies
  at least one phase-1 test scenario (SUM on 11, MAX on 9 and 11,
  MIN on 9 and 11, FIRST on 9 and 12, LAST on 9 and 11).
- Phase 2 adapt: M+t=11 scores 2/4 on refit; threshold refit reaches
  4/4 at t=16; adapt code 1; M structural bytes unchanged; held-out
  2/2.
- Phase 3 adapt: M+t=16 scores 2/8 on train; threshold refit maxes at
  6/8 (t=10); extension finds ADD R0,R2 as the strict first-max
  winner (gain 2; nearest rivals CPY R0,R2 and MIN R0,R2 reach 7/8,
  gain 1); adapt code 2; M' = [ADD R0,R1, ADD R0,R2], t=18, test 4/4;
  old M in Mprev with superseded=1.

## 4. Frozen arms

- ARM-FULL: X taught (scenarios 1..12), Y taught (prior + phase-1
  fit), M constructed from train 1..8. Z on test 9..12. Expect 4/4.
- ARM-X-ONLY: X taught, Y absent, M absent. Z on test 9..12. Expect
  0/4 (all NO_DECISION).
- ARM-Y-ONLY: Y taught, X absent. Z on test 9..12. Expect 0/4.
- ARM-MENU (5 controls): X+Y taught; driver applies each menu
  reduction with its train-fit threshold on test 9..12. Expect each
  <= 3/4.
- ARM-NO-M: ARM-FULL state with the M slot wiped before Z. Expect
  0/4.

## 5. Kill bars

- K-XC-1 (insufficiency): ARM-X-ONLY == 0/4 AND ARM-Y-ONLY == 0/4 AND
  ARM-FULL == 4/4. X and Y exist and each alone fails Z.
- K-XC-2 (novelty, no enumerated solution): frozen grep audit on
  `learner.zag` returns zero hits for every pattern in section 6.
- K-XC-3 (creation trace): the run log shows construction with at
  least one positive-gain round, the final program is non-empty,
  it scores 8/8 on phase-1 train, and the program bytes printed from
  learner state are (1,0,1).
- K-XC-4 (necessity): ARM-FULL == 4/4 AND ARM-NO-M == 0/4. Removing
  M restores the X/Y type gap and Z fails.
- K-XC-5 (persistence): the 28 structural bytes of the M slot
  (n@232, gen@233, sup@234, pad@235, program@240..263) dumped after
  phase 1 are byte-identical after phase 2. The threshold field at
  236..239 is Y's adaptive decision parameter (it also lives in Y's
  own slot at 228..231) and is expected to change 11 -> 16 on refit;
  it is excluded from this bar (precedent: composition_l3 ERRATUM-1).
- K-XC-6 (reuse): phase-2 adapt returns code 1 (threshold-only, M
  untouched) AND held-out decisions == 2/2.
- K-XC-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict XDOMAIN-CAUSAL-L3-COMPLETE requires all seven PASS with no
falsifier firing.

## 6. Frozen K-XC-2 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e0+e1` (the solution expression)
2. `ADD R0,R1`
3. `76626760` (scenario table data must not live in the learner)
4. `causal` (no causal concept in the learner)
5. `intervention` (no intervention concept in the learner)
6. `threshold.*=.*10` (no hardcoded threshold; thresholds come only
   from sweeps over experience)
7. `_MODE` (zero modes allowed)
8. `bridge` (case-insensitive; the intermediate is never a bridge
   handler/mode; conceptual term only, and not used in code at all)

## 7. Frozen falsifiers

- F-NO-CREATE: construction yields an empty program or < 8/8 on
  train, or program bytes differ from (1,0,1).
- F-MENU-WIN: any menu control reaches 4/4 on phase-1 test.
- F-ABLATE-FAIL: ARM-X-ONLY or ARM-Y-ONLY scores >= 1/4.
- F-NOT-NECESSARY: ARM-NO-M scores >= 1/4.
- F-NO-PERSIST: M structural bytes differ between phase 1 and
  phase 2.
- F-NO-REUSE: phase-2 adapt code != 1 or held-out < 2/2.
- F-NO-REVISE: phase-3 adapt code != 2 or phase-3 test < 4/4.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN}
  for any reason. This voids the build.
- F-AUDIT: any K-XC-2 pattern matches in learner.zag.
- F-NONDET: the three runs differ by even one byte.
- F-PYTHON: any python/python3 invocation in the worker process tree.

Any falsifier firing voids the corresponding claim; F-NO-CREATE,
F-AUDIT, F-NONDET, F-PYTHON, F-OP-EXPAND void the whole build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer
and one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the register machine, the
  greedy search, and the adapt() policy are researcher-supplied
  generic machinery, frozen here, identical to composition_l3 and
  xdomain_l3. The L3 claim here is about the INTERMEDIATE's form
  being source-underdetermined and history-determined for a third
  domain pair, not about the basis.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality (Micah C0-C) is
  open future work.
- One world family (causal observation to intervention strength). No
  generality claim beyond the demonstrated phases.
- The cross-domain comparison (FORAGE [ADD R0,R2] vs COMPILE
  [ADD R0,R3] vs INTERVENE [ADD R0,R1] from the same frozen learner)
  is evidence, not a bar.

## 10. Standing non-claims (unchanged)

- This build targets the seven xdomain-causal-L3 bars above. It does
  not claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
