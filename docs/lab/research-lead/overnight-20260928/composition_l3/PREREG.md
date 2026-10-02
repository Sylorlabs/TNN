# PREREG: Composition L3 Novel Intermediate (FORAGE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/composition_l3/` only.
Worker: Composition L3 Novel Intermediate Worker (subagent, 2026-10-02).
Parent mandate: demonstrate L3 novel intermediate structure creation for
composition. L1 exact reuse is demonstrated; stop spending cycles there.

## 1. What is being tested

Whether a learner, given two learned structures X and Y that are each
insufficient for a goal Z, constructs through experience a NOVEL
INTERMEDIATE M that bridges them, where M's final form is not enumerated
in source, then persists M, reuses M on a new problem, and revises M when
the world changes.

Concrete scenario (FORAGE):
- X: episode recall. Given an episode id, X replays the 4 sensor readings
  observed in that episode. X outputs a SEQUENCE.
- Y: threshold decide. Given a scalar s, Y outputs STAY(1) iff s >= t else
  LEAVE(0). The threshold t is learned from direct scalar experience. Y
  consumes a SCALAR.
- Z: on new episodes, decide STAY/LEAVE correctly. X alone cannot decide
  (no decision procedure; type gap: sequence vs scalar). Y alone cannot
  decide (no perceptual input). The bridge is a learned aggregation
  seq -> scalar that the source never defines.

The learner must DISCOVER the aggregation by constructing a reduction
program from generic primitives, guided only by labeled episode
experience. It may not select it from a menu of aggregations.

## 2. Frozen learner machinery (disclosed)

The learner is generic machinery plus learned state. No episode data, no
hidden world rules, and no aggregation solution live in the learner
source. Frozen for this build:

- State: one u8 buffer. X store (32 episode slots: id + 4 readings).
  Label store (32 slots: id + rich/poor). Y scalar observations (16
  slots) and Y threshold (i32, -1 = unset). M slot (32 bytes: n_instr,
  generation, superseded flag, threshold i32, up to 8 instructions of
  3 bytes). Mprev slot (32 bytes, revision history).
- Reduction program: sequence of up to 8 instructions. Registers R0..R3
  auto-loaded with the 4 readings. Output is R0. Instruction = (op, d, s)
  with d,s in 0..3. Frozen op basis (residual researcher footprint,
  disclosed in section 9; NOT expandable to rescue a failed build):
  0=CPY (Rd=Rs), 1=ADD (Rd+=Rs), 2=SUB (Rd-=Rs), 3=MAX (Rd=max(Rd,Rs)),
  4=MIN (Rd=min(Rd,Rs)).
- construct(): greedy search. Start from a given program (empty for fresh
  construction). Each round evaluates every (op,d,s) append (5*16=80
  candidates) by best-threshold classification score on the labeled
  episodes; applies the single append with the largest strictly positive
  gain; ties broken by candidate order (op 0..4, d 0..3, s 0..3,
  first-max). Stops at no positive gain or 8 instructions. Threshold
  sweep is t=0..40 ascending, first-max. Returns the program, its
  threshold, and its score.
- refit_threshold(): re-sweeps t=0..40 for the current M on new labeled
  episodes; adopts the new t iff it reaches perfect classification.
- adapt(): generic adaptation policy, no modes. (1) Evaluate current M+t
  on new labeled episodes; if perfect, keep (code 0). (2) Else refit the
  threshold; if perfect, keep M with new t (code 1). (3) Else extend M via
  construct() starting from M; if perfect, retire old M to Mprev
  (superseded=1) and adopt M' (code 2). (4) Else HONESTFAIL (code 3).
- decide(ep_id): recall sequence via X; if X misses, or M is absent, or Y
  threshold unset, return -1 (NO_DECISION). Else s=exec(M,seq); return
  Y(s). -1 never counts as correct.

## 3. Frozen world (environment, hidden from learner)

The world defines episodes and the hidden labeling rules. The learner
sees only sequences (via X teaching) and labels (as observed outcomes).
The driver generates labels from these rules; the learner source never
calls them.

- Y prior scalar experience (teaches that Y exists and consumes scalars):
  (12,rich),(15,rich),(11,rich),(8,poor),(5,poor),(9,poor).
  Y threshold from this data: t=10 (first-max ascending; 6/6).
- TRUE1 (phase 1): rich iff e0+e2 >= 10.
- TRUE2 (phase 2): rich iff e0+e2 >= 14 (stricter stay criterion).
- TRUE3 (phase 3): rich iff e0+e2+e3 >= 16 (world change).

Frozen episode tables (id: [e0,e1,e2,e3], label under the phase rule):

Phase 1 train (labels from TRUE1):
1: [7,1,5,2] rich    2: [2,9,9,0] rich    3: [8,0,4,8] rich
4: [1,2,9,9] rich    5: [9,0,0,1] poor    6: [8,8,1,0] poor
7: [0,1,2,3] poor    8: [5,5,4,1] poor
Phase 1 test:
9: [6,0,6,0] rich   10: [9,9,0,0] poor   11: [3,3,8,8] rich
12: [4,4,4,4] poor

Phase 2 refit (labels from TRUE2):
21: [7,1,7,2] rich  22: [9,0,5,0] rich  23: [8,2,5,1] poor
24: [6,6,6,6] poor
Phase 2 held-out:
25: [5,0,9,0] rich  26: [9,9,4,4] poor

Phase 3 train (labels from TRUE3):
31: [7,1,5,6] rich  32: [2,9,9,7] rich  33: [8,0,4,8] rich
34: [6,2,9,1] rich  35: [9,0,0,6] poor  36: [8,8,1,0] poor
37: [0,1,2,3] poor  38: [5,5,9,1] poor
Phase 3 test:
39: [6,0,6,6] rich  40: [9,9,0,0] poor  41: [5,5,7,4] rich
42: [7,7,7,1] poor

Frozen hand-derived expectations (the implementation must reproduce them;
any deviation is a falsifier, not a tuning opportunity):
- Phase 1 construction from empty: round 1 evaluates 80 candidates;
  ADD R0,R2 is the unique 8/8 candidate (gain 3 over the empty-program
  baseline 5/8); round 2 finds no positive gain; M = [ADD R0,R2]
  (1 instruction: op=1,d=0,s=2), threshold t=10, train 8/8.
- Menu controls (experiment controls in the world file, NOT learner
  machinery), thresholds fit on phase-1 train (first-max ascending):
  SUM t=19, MAX t=6, MIN t=1, FIRST t=1, LAST t=2. Each misclassifies at
  least one phase-1 test episode (SUM on 9, MAX on 10, MIN on 9, FIRST on
  10, LAST on 9).
- Phase 2 adapt: M+t=10 scores 2/4 on refit; threshold refit reaches 4/4
  at t=14; adapt code 1; M bytes unchanged; held-out 2/2.
- Phase 3 adapt: M+t=14 scores 4/8 on train; threshold refit maxes at 7/8
  (t=10); extension finds ADD R0,R3 as the unique 8/8 append (gain 1);
  adapt code 2; M' = [ADD R0,R2, ADD R0,R3], t=16, test 4/4; old M in
  Mprev with superseded=1.

## 4. Frozen arms

- ARM-FULL: X taught (episodes 1..12), Y taught (prior + phase-1 fit),
  M constructed from train 1..8. Z on test 9..12. Expect 4/4.
- ARM-X-ONLY: X taught, Y absent, M absent. Z on test 9..12. Expect 0/4
  (all NO_DECISION).
- ARM-Y-ONLY: Y taught, X absent. Z on test 9..12. Expect 0/4.
- ARM-MENU (5 controls): X+Y taught; driver applies each menu aggregation
  with its train-fit threshold on test 9..12. Expect each <= 3/4.
- ARM-NO-M: ARM-FULL state with the M slot wiped before Z. Expect 0/4.

## 5. Kill bars

- K-L3-1 (insufficiency): ARM-X-ONLY == 0/4 AND ARM-Y-ONLY == 0/4 AND
  ARM-FULL == 4/4. X and Y exist and each alone fails Z.
- K-L3-2 (no enumerated solution): frozen grep audit on `learner.zag`
  returns zero hits for every pattern in section 6.
- K-L3-3 (creation trace): the run log shows construction with at least
  one positive-gain round, the final program is non-empty, and it scores
  8/8 on phase-1 train. The program bytes are printed from learner state.
- K-L3-4 (causal necessity): ARM-FULL == 4/4 AND ARM-NO-M == 0/4.
  Removing M restores the X/Y type gap and Z fails.
- K-L3-5 (persistence): the M slot bytes dumped after phase 1 are
  byte-identical after phase 2 (memcmp in the driver).
- K-L3-6 (reuse): phase-2 adapt returns code 1 (threshold-only, M
  untouched) AND held-out decisions == 2/2.
- K-L3-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict COMPOSITION-L3-COMPLETE requires all seven PASS with no
falsifier firing.

## 6. Frozen K-L3-2 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e0+e2` (the solution expression)
2. `e\[0\].*e\[2\]`
3. `ADD R0,R2`
4. `7,1,5,2` (episode data must not live in the learner)
5. `even` (no positional concept in the learner)
6. `threshold.*=.*10` (no hardcoded threshold; thresholds come only from
   sweeps over experience)
7. `_MODE` (zero modes allowed)
8. `bridge` (case-insensitive; the intermediate is never a bridge
   handler/mode; conceptual term only, and not used in code at all)

## 7. Frozen falsifiers

- F-NO-CREATE: construction yields an empty program or < 8/8 on train.
- F-MENU-WIN: any menu control reaches 4/4 on phase-1 test.
- F-ABLATE-FAIL: ARM-X-ONLY or ARM-Y-ONLY scores >= 1/4.
- F-NOT-NECESSARY: ARM-NO-M scores >= 1/4.
- F-NO-PERSIST: M bytes differ between phase 1 and phase 2.
- F-NO-REUSE: phase-2 adapt code != 1 or held-out < 2/2.
- F-NO-REVISE: phase-3 adapt code != 2 or phase-3 test < 4/4.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN} for
  any reason. This voids the build.
- F-AUDIT: any K-L3-2 pattern matches in learner.zag.
- F-NONDET: the three runs differ by even one byte.
- F-PYTHON: any python/python3 invocation in the worker process tree.

Any falsifier firing voids the corresponding claim; F-NO-CREATE,
F-AUDIT, F-NONDET, F-PYTHON, F-OP-EXPAND void the whole build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer and
one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN} and the register machine are
  researcher-supplied generic machinery, frozen here. This is the same
  class of footprint as the operator vocabulary in the L3 bridge work.
  The L3 claim here is about the INTERMEDIATE's form being
  source-underdetermined and history-determined, not about the basis.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality (Micah C0-C) is
  open future work.
- One world family (foraging aggregation). No generality claim beyond
  the demonstrated phases.
## 10. Amendments (transparent, re-frozen before implementation commit)

ERRATUM-1 (K-L3-5 scope, internal contradiction resolved): section 3
requires phase-2 threshold refit to reach 4/4 at t=14 (adapt code 1),
while K-L3-5 as written requires full 32-byte M-slot identity. The M
slot's threshold field (bytes 236..239) is Y's adaptive decision
parameter, recorded per M generation for revision history; it must
change 10 to 14 in phase 2. The intermediate M's structural identity is
its program: bytes n@232, gen@233, sup@234, pad@235, prog@240..263
(28 bytes). K-L3-5 is clarified to: the 28 structural bytes of the M
slot dumped after phase 1 are byte-identical after phase 2. The driver
check compares exactly those bytes. Rationale for the split: the
threshold is Y's parameter (it also lives in Y's own slot at 228..231);
the novel intermediate is the reduction program. The frozen phase-2
expectation (adapt code 1, threshold-only update, M program untouched)
is unchanged.

ERRATUM-2 (menu-fit detail): the SUM train-fit threshold is t=18, not
t=19 as hand-computed in section 3. Cause: builder arithmetic slip
(P4=[5,5,4,1] sums to 15, not 18; with rich sums {15,20,20,21} and poor
sums {10,17,6,15}, t=18 is the first ascending threshold reaching 7/8).
The frozen episode tables are unchanged and the derived value is
correct. No kill bar depends on this value; F-MENU-WIN is evaluated on
the test episodes.

Both errata are builder-side corrections documented here before the
implementation commit. The learner (learner.zag) is untouched by
ERRATUM-1; only the driver's persistence check scope is refined to match
the clarified bar. No threshold, episode, rule, or machinery was altered
to rescue a result.

## 11. Standing non-claims (unchanged)

- This build targets the seven composition-L3 bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
