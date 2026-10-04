# PREREG: L2-L3 Combination (MEADOW)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_l3_combo/` only.
Worker: L2-L3 Combination Worker (subagent, 2026-10-02).
Parent mandate: demonstrate L2 adaptation AND L3 novel intermediate
creation in a SINGLE problem.

## 1. What is being tested

Whether one learner, on one problem, BOTH adapts an old structure
(L2: EXTEND the recall procedure past its learned length on structural
preconditions) AND invents a novel intermediate (L3: constructs the
sequence to scalar reduction through experience, its final form not
enumerated in source). Prior waves demonstrated L2 adaptation
(composition_l2: EXTEND/TRUNCATE/SPECIALIZE) and L3 invention
(composition_l3 FORAGE: M = [ADD R0,R2]) separately. Open: can TNN do
both in one composition?

Concrete scenario (MEADOW):
- X: episode recall. X was trained on 4-reading episodes, so its learned
  replay length is L=4. New episodes carry 6 readings. X alone replays
  only the first 4.
- L2 adaptation (EXTEND): a standing rule inside recall. If continuation
  slots past L are filled in the queried episode's store entry, replay
  continues greedily up to 2 extra slots. Fires on structural
  preconditions computed from learner state (slot fill pattern), never
  selected per problem by the researcher. Adapted X' replays 6 readings.
- Y: threshold decide. Given a scalar s, Y outputs STAY(1) iff s >= t
  else LEAVE(0). Y consumes a SCALAR. Threshold t=10 learned from prior
  scalar experience.
- Hidden world rule: rich iff e2+e4 >= 10. The decisive reading e4 sits
  in slot 4, unreachable without the L2 extension.
- L3 invention: the bridge between X' (6-reading sequence) and Y
  (scalar) is a reduction program M constructed by greedy search over
  the frozen generic op basis {CPY,ADD,SUB,MAX,MIN} on 6 registers,
  guided only by labeled episode experience. M is not selected from a
  menu of reductions.

The problem requires both: without EXTEND, e4 is unreachable so no
reduction can succeed; without the invented M, the extended sequence
cannot drive Y's scalar decision.

## 2. Frozen learner machinery (disclosed)

Generic machinery plus learned state. No episode data, no hidden world
rule, no reduction solution in the learner source. Frozen for this
build:

- State: one u8 buffer. Offsets: 0 XN, 1 LN, 2 YN, 3 YT_SET,
  4 REPLAY_LEN (learned), 5 ADAPT_ON (causal-control flag, set by the
  driver per arm, never written by the learner; the composition_l2
  adapt_on precedent). X slots: 16 episodes x 7 bytes
  [id,e0,e1,e2,e3,e4,e5] at 8..119 (unfilled slot = 255). Label slots:
  16 x 2 bytes at 120..151. Y threshold i32 at 152..155. M slot 32 bytes
  at 156..187 [n,gen,sup,pad,threshold i32,24 program bytes].
  ADAPT-STAT: ext_count i32 at 252..255, recall_calls i32 at 256..259.
  Y scalar observations 16 x 2 bytes at 220..251.
- x_teach: stores id + 6 readings (unfilled = 255).
- x_learn_len: REPLAY_LEN = max k in 0..6 such that every taught episode
  has slots 0..k-1 filled. Learned from experience, not set by hand.
- x_recall (contains the L2 EXTEND standing rule): replays slots
  0..L-1; then, iff ADAPT_ON==1, continues while the next slot is
  filled and fewer than 2 extra slots were added. Returns readings
  replayed (0 = episode unknown). Increments recall_calls always and
  ext_count when at least one extra slot was replayed. The rule is
  evaluated on every recall; the researcher never picks it per problem.
- y_teach / y_fit / y_decide: as in FORAGE. Threshold sweep t=0..40
  ascending, first-max.
- Reduction program: up to 8 instructions of (op,d,s), d,s in 0..5,
  registers R0..R5 auto-loaded with replayed readings (unreplayed = 0).
  Output is R0. Frozen op basis: 0=CPY, 1=ADD, 2=SUB, 3=MAX, 4=MIN.
  Not expandable (F-OP-EXPAND voids the build).
- construct(): greedy search from a given program. Each round evaluates
  every (op,d,s) append (5*36=180 candidates) by best-threshold
  classification score on the labeled episodes; applies the single
  append with the largest strictly positive gain; ties broken by
  candidate order (op 0..4, d 0..5, s 0..5, first-max). Stops at no
  positive gain or 8 instructions. Threshold sweep t=0..40 ascending,
  first-max.
- decide(ep_id): recall via X (EXTEND applies per the standing rule);
  if recall finds nothing, or M absent (n==0), or Y threshold unset,
  return -1 (NO_DECISION). Else s=exec(M,readings); return Y(s).
  -1 never counts as correct.

## 3. Frozen world (environment, hidden from learner)

The driver generates labels from these rules; the learner source never
calls them.

- Phase 0 (old world, teaches the 4-reading replay length):
  O1 id=51: [4,2,6,1]; O2 id=52: [7,0,3,5]. Stored with slots 4,5 = 255.
  x_learn_len -> L=4.
- Y prior scalar experience: (12,rich),(15,rich),(11,rich),
  (8,poor),(5,poor),(9,poor). Y threshold t=10 (first-max; 6/6).
- TRUE (phase 1): rich iff e2+e4 >= 10.

Frozen episode tables (id: [e0,e1,e2,e3,e4,e5], label under TRUE):

Phase 1 train (labels from TRUE):
1: [1,0,7,0,5,0] rich    2: [0,9,3,0,8,0] rich
3: [8,0,9,8,1,0] rich    4: [3,2,2,0,9,9] rich
5: [1,0,7,0,0,1] poor    6: [0,9,3,0,0,0] poor
7: [8,0,9,8,0,3] poor    8: [3,2,2,0,1,0] poor
Phase 1 test:
9: [2,1,6,0,5,0] rich   10: [9,9,1,1,9,0] rich
11: [7,7,8,0,1,0] poor  12: [4,4,0,4,2,8] poor

Frozen hand-derived expectations (the implementation must reproduce
them; any deviation is a falsifier, not a tuning opportunity):

- Phase-0 teaching then x_learn_len gives L=4; after phase-1 teaching
  L is still 4 (old episodes still constrain the common prefix).
- ARM-FULL construction on train ids 1..8 (recall extends to 6):
  - Empty baseline: R0=e0; rich e0 {1,0,8,3} equals poor e0 {1,0,8,3}
    as multisets, so every t scores exactly 4/8; first-max t=0.
  - Round 1 (180 candidates): d!=0 appends leave R0=e0 (4/8). Among
    d=0 appends the max is 7/8, reached first by CPY R0,R4
    (op=0,d=0,s=4): e4 rich {5,8,1,9} vs poor {0,0,0,1}, best t=1
    (4+3). Nearest rivals ADD R0,R4 and MAX R0,R4 also 7/8 but later
    in candidate order. Gain 3 > 0. Adopt [CPY R0,R4], t=1.
  - Round 2: base 7/8. op=0 appends max 7/8. op=1: (1,0,0) e4+e0 7/8,
    (1,0,1) e4+e1 6/8, (1,0,2) e4+e2 = {12,11,10,11} vs {7,3,9,3}:
    t=10 gives 8/8 (first t with all poor < t, since poor has 9).
    First 8/8 in order. Gain 1 > 0. Adopt [CPY R0,R4, ADD R0,R2],
    t=10, score 8/8.
  - Round 3: base 8/8; no strictly positive gain possible; stop.
  - M-BUILT n=2 t=10 score=8/8. M slot program bytes:
    [0,0,4, 1,0,2, 0,0,0, ...].
- ARM-FULL Z on test 9..12 (recall extends to 6, s=e4+e2, Y t=10):
  9: s=11>=10 -> 1, true rich -> ok.
  10: s=10>=10 -> 1, true rich -> ok.
  11: s=9<10 -> 0, true poor -> ok.
  12: s=2<10 -> 0, true poor -> ok. Z-FULL 4/4.
- ARM-L2-ONLY (adapt on, construction skipped): X' replays 6 readings
  (ext fires; Z lines show 6-reading seqs), M slot n=0, decide -1 on
  all 4. Z-L2ONLY 0/4. Adaptation happened but Z still fails.
- ARM-L3-ONLY (adapt off, construction on): recall replays 4 readings
  (R4=R5=0). Train projections pair up: rich [1,0,7,0],[0,9,3,0],
  [8,0,9,8],[3,2,2,0] are byte-identical to poor [1,0,7,0],[0,9,3,0],
  [8,0,9,8],[3,2,2,0]. Any deterministic program on (e0..e3) gives
  identical outputs within each rich/poor pair, so no candidate
  exceeds 4/8 = the empty baseline; round 1 finds no positive gain;
  construction stops with M n=0. decide -1 on all 4. Z-L3ONLY 0/4.
  (Pairing proof; no candidate enumeration needed.)
- ARM-FRESH (nothing taught): x_recall finds nothing; Z-FRESH 0/4.

## 4. Frozen arms

- ARM-FULL: ADAPT_ON=1; phase-0 teach; Y prior; phase-1 teach+labels;
  construct M; Z on test 9..12. Expect 4/4, ext_count >= 1, M n=2
  with program [0,0,4,1,0,2,...].
- ARM-L2-ONLY: ADAPT_ON=1; same teaching; construction skipped
  (M slot stays n=0); Z on test. Expect 0/4 with ext_count >= 1.
- ARM-L3-ONLY: ADAPT_ON=0; same teaching; construct M; Z on test.
  Expect construction to yield n=0 and Z 0/4 with ext_count == 0.
- ARM-FRESH: ADAPT_ON=0; no teaching at all; Z on test. Expect 0/4.

## 5. Kill bars

- K-CB-1 (both required): ARM-L2-ONLY == 0/4 AND ARM-L3-ONLY == 0/4
  AND ARM-FULL == 4/4. The problem is unsolvable by either level
  alone and solvable by both together.
- K-CB-2 (L2-only fails): ARM-L2-ONLY == 0/4 with ext_count >= 1
  (adaptation genuinely fired but is insufficient without M).
- K-CB-3 (L3-only fails): ARM-L3-ONLY == 0/4 with ext_count == 0 and
  constructed M n == 0 (no adaptation, and construction provably
  cannot reach the needed information).
- K-CB-4 (combined succeeds with provenance): ARM-FULL == 4/4 AND
  ADAPT-STAT ext_count >= 1 AND the run log prints the M program bytes
  [0,0,4,1,0,2,...] with n=2 from learner state AND every Z line shows
  a 6-reading replayed sequence (adapted X' in the trace).
- K-CB-5 (M not in source): frozen grep audit on `learner.zag`
  returns zero hits for every pattern in section 6.
- K-CB-6 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L2-L3-COMBO-COMPLETE requires all six PASS with no falsifier
firing.

## 6. Frozen K-CB-5 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e2+e4` (the hidden rule expression)
2. `CPY R0,R4` (the constructed first instruction)
3. `ADD R0,R2` (the constructed second instruction)
4. `0,0,4` (the first instruction triple)
5. `1,0,2` (the second instruction triple)
6. `107050` (train episode 1 digit string; no episode data in learner)
7. `1,0,7,0,5,0` (train episode 1 literal)
8. `even` (no positional concept in the learner)
9. `threshold.*=.*10` (no hardcoded threshold; thresholds come only
   from sweeps over experience)
10. `_MODE` (zero modes allowed)
11. `bridge` (case-insensitive; nothing in code is a bridge handler)

## 7. Frozen falsifiers

- F-NO-CREATE: ARM-FULL construction yields n=0 or train score < 8/8.
- F-NO-EXTEND: ARM-FULL ADAPT-STAT ext_count == 0.
- F-L2-SUFFICIENT: ARM-L2-ONLY scores >= 1/4.
- F-L3-SUFFICIENT: ARM-L3-ONLY scores >= 1/4 or its M has n > 0.
- F-FRESH-PASS: ARM-FRESH scores >= 1/4.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN}
  for any reason. Voids the build.
- F-AUDIT: any K-CB-5 pattern matches in learner.zag. Voids the build.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer and
one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the 6-register machine, the
  greedy construction policy, and the EXTEND standing rule are
  researcher-supplied generic machinery, frozen here. The L2 claim is
  that EXTEND fires on structural preconditions without per-problem
  researcher selection; the L3 claim is that M's final form
  ([CPY R0,R4, ADD R0,R2]) is source-underdetermined and
  history-determined, not that the basis is.
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner. It enables the
  lesion comparison; it is not a runtime mode.
- The hidden world rule was designed by the builder, not an independent
  adversary. Sealed-adversary generality is open future work.
- One world family. No generality claim beyond the demonstrated arms.
- This build targets the six combo bars above. It does not claim
  Micah's full 12-criterion L3 bar.

## 10. Standing non-claims

- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. The frozen TNN core is not
  used here; this is a standalone learner-mechanism experiment.
