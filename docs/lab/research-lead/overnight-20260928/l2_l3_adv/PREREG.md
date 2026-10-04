# PREREG: L2-L3 Adversarial World (RELAY)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_l3_adv/` only.
Worker: Adversarial L2-L3 Worker (subagent, 2026-10-02).
Parent mandate: test whether the L2+L3 combination generalizes to an
adversary-designed world family, different from MEADOW.

## 1. What is being tested

Whether one learner, on one independently designed problem, BOTH
adapts an old structure (L2: EXTEND the recall procedure past its
learned length on structural preconditions) AND invents a novel
intermediate (L3: constructs the sequence to scalar reduction through
experience, its final form not enumerated in source). The MEADOW wave
demonstrated this for one builder-designed world (hidden rule
e2+e4 >= 10, invented M = [CPY R0,R4, ADD R0,R2]). Open: does the
combination generalize to a world the builder did not design?

Concrete scenario (RELAY), designed by this worker independently of
the MEADOW builder:
- X: episode recall. X was trained on 4-reading episodes from an old
  4-reading-per-day protocol, so its learned replay length is L=4. New
  episodes carry 6 hourly signal-strength readings from a relay
  station. X alone replays only the first 4.
- L2 adaptation (EXTEND): the same standing rule inside recall as in
  the MEADOW build (learner.zag is reused byte-identical). If
  continuation slots past L are filled in the queried episode's store
  entry, replay continues greedily up to 2 extra slots. Fires on
  structural preconditions computed from learner state (slot fill
  pattern), never selected per problem by the researcher. Adapted X'
  replays 6 readings.
- Y: threshold decide. Given a scalar s, Y outputs STABLE(1) iff
  s >= t else UNSTABLE(0). Y consumes a SCALAR. Threshold t=5 learned
  from prior scalar experience.
- Hidden world rule: STABLE iff e5-e1 >= 5. The signal at hour 5 must
  exceed the signal at hour 1 by at least 5 (an overnight climb). The
  decisive reading e5 sits in slot 5, unreachable without the L2
  extension.
- L3 invention: the bridge between X' (6-reading sequence) and Y
  (scalar) is a reduction program M constructed by greedy search over
  the frozen generic op basis {CPY,ADD,SUB,MAX,MIN} on 6 registers,
  guided only by labeled episode experience. M is not selected from a
  menu of reductions. The frozen expectation is M = [CPY R0,R5,
  SUB R0,R1], a SUB-based difference program, structurally distinct
  from MEADOW's ADD-based sum.

The problem requires both: without EXTEND, e5 is unreachable so no
reduction can succeed; without the invented M, the extended sequence
cannot drive Y's scalar decision. A trap episode (id 8: high e5 yet
UNSTABLE because e1 is also high) forces the second instruction: e5
alone reaches only 7/8, and the SUB correction is needed for 8/8.

## 2. Frozen learner machinery (disclosed, reused unmodified)

Generic machinery plus learned state. No episode data, no hidden
world rule, no reduction solution in the learner source. The file
`l2_l3_adv/learner.zag` is a byte-identical copy of
`l2_l3_combo/learner.zag` (sha256
338c462287661c13ea02e06fc0b8f57dda2f567c4db68c5ebc3d0b2b89117c6b);
it is not modified, extended, or re-derived. Frozen summary:

- State: one u8 buffer. Offsets: 0 XN, 1 LN, 2 YN, 3 YT_SET,
  4 REPLAY_LEN (learned), 5 ADAPT_ON (causal-control flag, set by the
  driver per arm, never written by the learner). X slots: 16 episodes
  x 7 bytes [id,e0,e1,e2,e3,e4,e5] at 8..119 (unfilled slot = 255).
  Label slots: 16 x 2 bytes at 120..151. Y threshold i32 at 152..155.
  M slot 32 bytes at 156..187 [n,gen,sup,pad,threshold i32,24 program
  bytes]. ADAPT-STAT: ext_count i32 at 252..255, recall_calls i32 at
  256..259. Y scalar observations 16 x 2 bytes at 220..251.
- x_teach: stores id + 6 readings (unfilled = 255).
- x_learn_len: REPLAY_LEN = max k in 0..6 such that every taught
  episode has slots 0..k-1 filled. Learned from experience.
- x_recall (contains the L2 EXTEND standing rule): replays slots
  0..L-1; then, iff ADAPT_ON==1, continues while the next slot is
  filled and fewer than 2 extra slots were added. Returns readings
  replayed (0 = episode unknown). Increments recall_calls always and
  ext_count when at least one extra slot was replayed.
- y_teach / y_fit / y_decide: threshold sweep t=0..40 ascending,
  first-max.
- Reduction program: up to 8 instructions of (op,d,s), d,s in 0..5,
  registers R0..R5 auto-loaded with replayed readings (unreplayed =
  0). Output is R0. Frozen op basis: 0=CPY, 1=ADD, 2=SUB, 3=MAX,
  4=MIN. Not expandable (F-OP-EXPAND voids the build).
- construct(): greedy search from a given program. Each round
  evaluates every (op,d,s) append (5*36=180 candidates) by
  best-threshold classification score on the labeled episodes;
  applies the single append with the largest strictly positive gain;
  ties broken by candidate order (op 0..4, d 0..5, s 0..5,
  first-max). Stops at no positive gain or 8 instructions. Threshold
  sweep t=0..40 ascending, first-max.
- decide(ep_id): recall via X (EXTEND applies per the standing rule);
  if recall finds nothing, or M absent (n==0), or Y threshold unset,
  return -1 (NO_DECISION). Else s=exec(M,readings); return Y(s).
  -1 never counts as correct.

## 3. Frozen world (environment, hidden from learner)

The driver generates labels from these rules; the learner source
never calls them. This world was designed by the adversarial worker,
not by the MEADOW builder.

- Phase 0 (old world, teaches the 4-reading replay length):
  O1 id=51: [3,1,4,2]; O2 id=52: [0,5,2,6]. Stored with slots 4,5 =
  255. x_learn_len -> L=4.
- Y prior scalar experience: (7,stable),(8,stable),(6,stable),
  (5,stable),(4,poor),(3,poor). Y threshold t=5 (first-max; 6/6).
- TRUE (phase 1): STABLE iff e5-e1 >= 5.

Frozen episode tables (id: [e0,e1,e2,e3,e4,e5], label under TRUE).
All episodes carry e0=0 and e4=0; only e1,e2,e3,e5 vary.

Phase 1 train (labels from TRUE):
1: [0,2,1,3,0,8] stable    2: [0,1,5,2,0,7] stable
3: [0,4,0,6,0,9] stable    4: [0,4,3,1,0,9] stable
5: [0,2,1,3,0,2] unstable  6: [0,1,5,2,0,3] unstable
7: [0,4,0,6,0,4] unstable  8: [0,4,3,1,0,8] unstable
(Trap: id 8 has high e5=8 yet is UNSTABLE because e1=4 gives
8-4=4 < 5.)
Phase 1 test:
9: [0,1,2,4,0,8] stable   10: [0,3,0,1,0,9] stable
11: [0,2,5,3,0,4] unstable 12: [0,6,1,2,0,8] unstable

Digit-string encodings (world.zag): old "31420526"; train
"021308015207040609043109021302015203040604043108"; test
"012408030109025304061208".

Frozen hand-derived expectations (the implementation must reproduce
them; any deviation is a falsifier, not a tuning opportunity):

- Phase-0 teaching then x_learn_len gives L=4; after phase-1 teaching
  L is still 4 (old episodes still constrain the common prefix).
- ARM-FULL construction on train ids 1..8 (recall extends to 6, so
  registers hold [0,e1,e2,e3,0,e5]):
  - Empty baseline: R0=e0=0 for all 8; every t scores exactly 4/8;
    first-max t=0.
  - Round 1 (180 candidates): d!=0 appends leave R0=e0=0 (4/8).
    Among (op,0,s): R0 is a function of the single reading e_s
    (e0=0). e0..e3 projections are pairwise label-identical
    (train pairs share slots 0..3), so s=0..3 give 4/8; s=4 gives
    e4=0 for all (4/8). CPY R0,R5 (op=0,d=0,s=5): R0=e5, stable e5
    {8,7,9,9} vs unstable {2,3,4,8}; t=5 gives 4+3=7/8, first t
    reaching 7 (t=4 gives 4+2=6). No other single instruction
    exceeds 7/8: every d=0 single-instruction output is a function
    of one reading (SUB R0,R5 = -e5 reaches only 4/8; MIN gives 0;
    MAX R0,R5 = e5 ties at 7/8 but is later in candidate order).
    Gain 3 > 0. Adopt [CPY R0,R5], t=5.
  - Round 2: base 7/8. op=0 appends: R0=e_s (max 7/8) or R0=e5
    (d!=0, 7/8). op=1: (1,0,1) e5+e1 reaches at most 6/8 (the
    (8,8) and (13,13) value collisions force exactly 1 correct per
    colliding pair); (1,0,2) e5+e2 at most 7/8 (t=9); (1,0,3)
    e5+e3 at most 6/8; (1,0,4) = e5; (1,0,5) = 2*e5 (7/8). (2,0,0)
    = e5 (7/8). (2,0,1) [SUB R0,R1]: R0 = e5-e1 = stable
    {6,6,5,5} vs unstable {0,2,0,4}: t=5 gives 8/8 (first t with
    8; t=4 gives 4+3=7). First candidate with positive gain.
    Gain 1 > 0. Adopt [CPY R0,R5, SUB R0,R1], t=5, score 8/8.
  - Round 3: base 8/8; no strictly positive gain possible; stop.
  - M-BUILT n=2 t=5 score=8/8. M slot program bytes:
    [0,0,5, 2,0,1, 0,0,0, ...].
- ARM-FULL Z on test 9..12 (recall extends to 6, s=e5-e1, Y t=5):
  9: s=7>=5 -> 1, true stable -> ok.
  10: s=6>=5 -> 1, true stable -> ok.
  11: s=2<5 -> 0, true unstable -> ok.
  12: s=2<5 -> 0, true unstable -> ok. Z-FULL 4/4.
- ARM-L2-ONLY (adapt on, construction skipped): X' replays 6 readings
  (ext fires; Z lines show 6-reading seqs), M slot n=0, decide -1 on
  all 4. Z-L2ONLY 0/4. Adaptation happened but Z still fails.
- ARM-L3-ONLY (adapt off, construction on): recall replays 4 readings
  (R4=R5=0). Train projections pair up: stable [0,2,1,3],[0,1,5,2],
  [0,4,0,6],[0,4,3,1] are byte-identical to unstable [0,2,1,3],
  [0,1,5,2],[0,4,0,6],[0,4,3,1]. Any deterministic program on
  (e0..e3) gives identical outputs within each stable/unstable pair,
  so every candidate and every threshold scores exactly 4/8 = the
  empty baseline; round 1 finds no positive gain; construction stops
  with M n=0. decide -1 on all 4. Z-L3ONLY 0/4. (Pairing proof; no
  candidate enumeration needed.)
- ARM-FRESH (nothing taught): x_recall finds nothing; Z-FRESH 0/4.

## 4. Frozen arms

- ARM-FULL: ADAPT_ON=1; phase-0 teach; Y prior; phase-1 teach+labels;
  construct M; Z on test 9..12. Expect 4/4, ext_count >= 1, M n=2
  with program [0,0,5,2,0,1,...].
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
  ADAPT-STAT ext_count >= 1 AND the run log prints the M program
  bytes [0,0,5,2,0,1,...] with n=2 from learner state AND every Z
  line shows a 6-reading replayed sequence (adapted X' in the trace).
- K-CB-5 (M not in source): frozen grep audit on `learner.zag`
  returns zero hits for every pattern in section 6. (learner.zag is
  byte-identical to the MEADOW build's learner; the audit is
  re-run here because the invented M differs.)
- K-CB-6 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L2-L3-ADV-COMPLETE requires all six PASS with no falsifier
firing.

## 6. Frozen K-CB-5 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e5-e1` (the hidden rule expression)
2. `CPY R0,R5` (the constructed first instruction)
3. `SUB R0,R1` (the constructed second instruction)
4. `0,0,5` (the first instruction triple)
5. `2,0,1` (the second instruction triple)
6. `021308` (train episode 1 digit string; no episode data in learner)
7. `0,2,1,3,0,8` (train episode 1 literal)
8. `relay` (no world concept in the learner)
9. `threshold.*=.*5` (no hardcoded threshold; thresholds come only
   from sweeps over experience)
10. `_MODE` (zero modes allowed)
11. `bridge` (case-insensitive; nothing in code is a bridge handler)

All eleven were verified zero-hit on learner.zag during design
(before this freeze).

## 7. Frozen falsifiers

- F-NO-CREATE: ARM-FULL construction yields n=0 or train score < 8/8.
- F-NO-EXTEND: ARM-FULL ADAPT-STAT ext_count == 0.
- F-L2-SUFFICIENT: ARM-L2-ONLY scores >= 1/4.
- F-L3-SUFFICIENT: ARM-L3-ONLY scores >= 1/4 or its M has n > 0.
- F-FRESH-PASS: ARM-FRESH scores >= 1/4.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN}
  for any reason. Voids the build.
- F-AUDIT: any K-CB-5 pattern matches in learner.zag. Voids the
  build.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer
and one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the 6-register machine, the
  greedy construction policy, and the EXTEND standing rule are
  researcher-supplied generic machinery, reused byte-identical from
  the MEADOW build. The L2 claim is that EXTEND fires on structural
  preconditions without per-problem researcher selection; the L3
  claim is that M's final form ([CPY R0,R5, SUB R0,R1]) is
  source-underdetermined and history-determined, not that the basis
  is.
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner. It enables the
  lesion comparison; it is not a runtime mode.
- The hidden world rule was designed by this adversarial worker,
  independently of the MEADOW builder, and is sealed from the
  learner (driver side only). It is not a trivial MEADOW variant:
  the hidden rule is a temporal difference (e5-e1 >= 5) rather than a
  static sum, and the invented program is SUB-based rather than
  ADD-based, over different registers.
- One world family (RELAY signal stability). No generality claim
  beyond the four demonstrated arms.
- This build targets the six combo bars above. It does not claim
  Micah's full 12-criterion L3 bar.

## 10. Standing non-claims

- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. learner.zag is reused
  byte-identical, never modified. The frozen TNN core is not used
  here; this is a standalone learner-mechanism experiment.
