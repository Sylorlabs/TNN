# PREREG: L2-L3 Truncate Combination (STUBBLE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_l3_trunc/` only.
Worker: L2-L3 Truncate Worker (subagent, 2026-10-02).
Parent mandate: demonstrate L2 adaptation AND L3 novel intermediate
creation in a SINGLE problem, where the L2 adaptation is TRUNCATE
(not EXTEND).

## 1. What is being tested

Whether one learner, on one problem, BOTH adapts an old structure
that is too long (L2: TRUNCATE the recall procedure to the filled
prefix on structural preconditions) AND invents a novel intermediate
(L3: constructs the sequence to scalar reduction through experience,
its final form not enumerated in source). Prior waves demonstrated
L2 EXTEND + L3 (MEADOW, builder-designed; RELAY, adversarial). Open:
does L2+L3 work when the adaptation is TRUNCATE?

Concrete scenario (STUBBLE):
- X: episode recall. X was consolidated on old 6-reading episodes, so
  its standing replay length is L=6. New episodes carry 4 readings.
  X alone replays 6 slots, including 2 phantom (255) slots.
- L2 adaptation (TRUNCATE): a standing rule inside recall. If slots
  within 0..L-1 are unfilled (255) in the queried episode's store
  entry, replay stops at the first unfilled slot. Fires on structural
  preconditions computed from learner state (slot fill pattern),
  never selected per problem by the researcher. Adapted X' replays
  4 readings.
- Consumer: a fixed 4-register recency window. The reduction machine
  loads the last up to 4 replayed readings (R0 = 4th-from-last,
  R3 = last; fewer than 4 replayed leaves leading registers 0). When
  X over-replays (6 slots), the phantom 255s occupy the recency
  positions and displace the informative early readings e0,e1. After
  TRUNCATE (4 slots), the window holds the true [e0,e1,e2,e3].
- Y: threshold decide. Given a scalar s, Y outputs KEEP(1) iff s >= t
  else DROP(0). Y consumes a SCALAR. Threshold t=12 learned from
  prior scalar experience.
- Hidden world rule: KEEP iff e1+e2 >= 12. The decisive readings e1
  (slot 1) is displaced from the recency window without TRUNCATE.
- L3 invention: the bridge between X' (4-reading sequence in the
  window) and Y (scalar) is a reduction program M constructed by
  greedy search over the frozen generic op basis {CPY,ADD,SUB,MAX,MIN}
  on 4 registers, guided only by labeled episode experience. M is not
  selected from a menu of reductions. The frozen expectation is
  M = [CPY R0,R1, ADD R0,R2], the same CPY-then-ADD shape as MEADOW
  but over different registers and a different threshold.

The problem requires both: without TRUNCATE, e1 is displaced from
the window so no reduction can reach the true signal; without the
invented M, the truncated window contents cannot drive Y's scalar
decision.

## 2. Frozen learner machinery (disclosed)

Generic machinery plus learned state. No episode data, no hidden world
rule, no reduction solution in the learner source. Adapted from
`l2_l3_combo/learner.zag`, with two disclosed deltas: (a) the L2
standing rule is TRUNCATE (not EXTEND); (b) the reduction machine has
4 registers with recency-window (keep-last) loading instead of 6
registers with first-6 loading. The greedy construction policy, the
op basis, and the decide pipeline are unchanged in mechanism.

- State: one u8 buffer. Offsets: 0 XN, 1 LN, 2 YN, 3 YT_SET,
  4 REPLAY_LEN (learned), 5 ADAPT_ON (causal-control flag, set by the
  driver per arm, never written by the learner; the composition_l2
  adapt_on precedent). X slots: 16 episodes x 7 bytes
  [id,e0,e1,e2,e3,e4,e5] at 8..119 (unfilled slot = 255). Label slots:
  16 x 2 bytes at 120..151. Y threshold i32 at 152..155. M slot 32
  bytes at 156..187 [n,gen,sup,pad,threshold i32,24 program bytes].
  ADAPT-STAT: trunc_count i32 at 252..255, recall_calls i32 at
  256..259. Y scalar observations 16 x 2 bytes at 220..251.
- x_teach: stores id + 6 readings (unfilled = 255).
- x_learn_len: REPLAY_LEN = max k in 0..6 such that every taught
  episode has slots 0..k-1 filled. Learned from experience, not set
  by hand. FROZEN TIMING: called once, after phase-0 teaching
  (consolidation). It is not re-run after phase-1; L=6 is X's
  standing structure, and TRUNCATE is the recall-time adaptation
  under test. Re-running it would rebuild L instead of adapting the
  replay, which is exactly what this experiment does not do.
- x_recall (contains the L2 TRUNCATE standing rule): replays slots
  0..L-1; but iff ADAPT_ON==1, stops at the first slot holding 255
  (structural precondition from learner state). Returns readings
  replayed (0 = episode unknown). Trailing out slots are zeroed.
  Increments recall_calls always and trunc_count when the replay was
  actually shortened (limit < L). The rule is evaluated on every
  recall; the researcher never picks it per problem.
- y_teach / y_fit / y_decide: threshold sweep t=0..40 ascending,
  first-max (as in the combo build).
- Recency window: 4 registers R0..R3. Loading takes the last up to 4
  replayed readings (R0 = 4th-from-last, R3 = last; leading registers
  0 when fewer than 4 replayed). Frozen generic machinery: a fixed
  capacity recency-ordered working memory, not a per-problem choice.
- Reduction program: up to 8 instructions of (op,d,s), d,s in 0..3.
  Output is R0. Frozen op basis: 0=CPY, 1=ADD, 2=SUB, 3=MAX, 4=MIN.
  Not expandable (F-OP-EXPAND voids the build).
- construct(): greedy search from a given program. Each round
  evaluates every (op,d,s) append (5*16=80 candidates) by
  best-threshold classification score on the labeled episodes;
  applies the single append with the largest strictly positive gain;
  ties broken by candidate order (op 0..4, d 0..3, s 0..3,
  first-max). Stops at no positive gain or 8 instructions. Threshold
  sweep t=0..40 ascending, first-max.
- decide(ep_id): recall via X (TRUNCATE applies per the standing
  rule); if recall finds nothing, or M absent (n==0), or Y threshold
  unset, return -1 (NO_DECISION). Else s=exec(M, window); return
  Y(s). -1 never counts as correct.

## 3. Frozen world (environment, hidden from learner)

The driver generates labels from these rules; the learner source
never calls them.

- Phase 0 (old world, teaches the 6-reading replay length):
  O1 id=51: [1,2,3,4,5,6]; O2 id=52: [6,5,4,3,2,1]. Stored fully
  filled. x_learn_len -> L=6.
- Y prior scalar experience: (14,keep),(15,keep),(13,keep),
  (11,drop),(8,drop),(10,drop). Y threshold t=12 (first-max; 6/6).
- TRUE (phase 1): KEEP iff e1+e2 >= 12.

Frozen episode tables (id: [e0,e1,e2,e3], label under TRUE).
e0 alternates 3,7 (non-informative by design); (e2,e3) pairs repeat
across the label split (load-bearing for the L3-only pairing proof).

Phase 1 train (labels from TRUE):
1: [3,7,6,1] keep    2: [7,1,6,1] drop
3: [3,8,5,2] keep    4: [7,2,5,2] drop
5: [3,6,7,3] keep    6: [7,0,7,3] drop
7: [3,9,4,4] keep    8: [7,7,4,4] drop
(Note id 8: e1=7 collides with keep-episode e1 values, so e1 alone
reaches only 7/8; the e1+e2 sum is needed for 8/8.)
Phase 1 test:
9: [3,7,6,5] keep   10: [7,8,5,6] keep
11: [3,2,5,7] drop  12: [7,1,6,8] drop

Digit-string encodings (world.zag): old "123456654321"; train
"37617161385272523673707339447744"; test "3765785632577168".

Frozen hand-derived expectations (the implementation must reproduce
them; any deviation is a falsifier, not a tuning opportunity):

- Phase-0 teaching then x_learn_len gives L=6. x_learn_len is not
  re-run after phase-1 (frozen timing, section 2).
- ARM-FULL construction on train ids 1..8 (TRUNCATE fires; window
  holds [e0,e1,e2,e3]):
  - Empty baseline: R0=e0={3,7,3,7,3,7,3,7}, labels alternate, so
    every t scores exactly 4/8; first-max t=0.
  - Round 1 (80 candidates): d!=0 appends leave R0=e0 (4/8). Among
    (op,0,s): s=0 gives e0 (4/8); s=2 gives e2, paired values
    {6,6,5,5,7,7,4,4} (4/8); s=3 gives e3, paired (4/8).
    (0,0,1) [CPY R0,R1]: R0=e1={7,1,8,2,6,0,9,7}; keep e1
    {7,8,6,9} vs drop {1,2,0,7}; 7 appears in both labels so the max
    is 7/8, first reached at t=3 (t=0:4/8, t=1:5/8, t=2:6/8). No
    other round-1 candidate exceeds 7/8: (1,0,1) e0+e1 reaches 6/8;
    (4,0,1) MIN R0,R1 ties 7/8 but is later in candidate order;
    SUB/MAX variants score lower (negatives unusable under t>=0
    sweep; MAX R0,R1 reaches 6/8). Gain 3 > 0. Adopt [CPY R0,R1],
    t=3.
  - Round 2: base 7/8. op=0 appends max 7/8. op=1: (1,0,0) e1+e0
    6/8, (1,0,1) 2*e1 7/8, (1,0,2) [ADD R0,R2]: R0=e1+e2 =
    {13,7,13,7,13,7,13,11} vs labels {1,0,1,0,1,0,1,0}: t=12 gives
    8/8 (first t with 8; t=11 gives 7/8 because id 8 has 11).
    First 8/8 in candidate order (op=0 all <=7/8 precedes it).
    Gain 1 > 0. Adopt [CPY R0,R1, ADD R0,R2], t=12, score 8/8.
  - Round 3: base 8/8; no strictly positive gain possible; stop.
  - M-BUILT n=2 t=12 score=8/8. M slot program bytes:
    [0,0,1, 1,0,2, 0,0,0, ...].
- ARM-FULL Z on test 9..12 (TRUNCATE fires; s=e1+e2; Y t=12):
  9: s=13>=12 -> 1, true keep -> ok.
  10: s=13>=12 -> 1, true keep -> ok.
  11: s=7<12 -> 0, true drop -> ok.
  12: s=7<12 -> 0, true drop -> ok. Z-FULL 4/4.
- ARM-L2-ONLY (truncation on, construction skipped): X' replays 4
  readings (trunc fires; Z lines show 4-reading seqs), M slot n=0,
  decide -1 on all 4. Z-L2ONLY 0/4. Adaptation happened but Z still
  fails.
- ARM-L3-ONLY (truncation off, construction on): replay is 6 slots
  [e0,e1,e2,e3,255,255]; recency window holds [e2,e3,255,255]. Train
  (e2,e3) pairs are byte-identical across the label split: keep
  [3,7,6,1],[3,8,5,2],[3,6,7,3],[3,9,4,4] share (e2,e3) with drop
  [7,1,6,1],[7,2,5,2],[7,0,7,3],[7,7,4,4] respectively. Any
  deterministic program on (e2,e3,255,255) gives identical outputs
  within each keep/drop pair, so every candidate in every round
  scores at most 4/8 = the empty baseline; round 1 finds no positive
  gain; construction stops with M n=0. decide -1 on all 4. Z-L3ONLY
  0/4. (Pairing proof; no candidate enumeration needed.)
- ARM-FRESH (nothing taught): x_recall finds nothing; Z-FRESH 0/4.

## 4. Frozen arms

- ARM-FULL: ADAPT_ON=1; phase-0 teach + x_learn_len (once); Y prior;
  phase-1 teach+labels (no x_learn_len re-run); construct M; Z on
  test 9..12. Expect 4/4, trunc_count >= 1, M n=2 with program
  [0,0,1,1,0,2,...].
- ARM-L2-ONLY: ADAPT_ON=1; same teaching; construction skipped
  (M slot stays n=0); Z on test. Expect 0/4 with trunc_count >= 1.
- ARM-L3-ONLY: ADAPT_ON=0; same teaching; construct M; Z on test.
  Expect construction to yield n=0 and Z 0/4 with trunc_count == 0.
- ARM-FRESH: ADAPT_ON=0; no teaching at all; Z on test. Expect 0/4.

## 5. Kill bars

- K-CB-1 (both required): ARM-L2-ONLY == 0/4 AND ARM-L3-ONLY == 0/4
  AND ARM-FULL == 4/4. The problem is unsolvable by either level
  alone and solvable by both together.
- K-CB-2 (L2-only fails): ARM-L2-ONLY == 0/4 with trunc_count >= 1
  (adaptation genuinely fired but is insufficient without M).
- K-CB-3 (L3-only fails): ARM-L3-ONLY == 0/4 with trunc_count == 0
  and constructed M n == 0 (no adaptation, and construction provably
  cannot reach the needed information: the pairing proof).
- K-CB-4 (combined succeeds with provenance): ARM-FULL == 4/4 AND
  ADAPT-STAT trunc_count >= 1 AND the run log prints the M program
  bytes [0,0,1,1,0,2,...] with n=2 from learner state AND every Z
  line shows a 4-reading replayed sequence (adapted X' in the trace).
- K-CB-5 (M not in source): frozen grep audit on `learner.zag`
  returns zero hits for every pattern in section 6.
- K-CB-6 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L2-L3-TRUNC-COMPLETE requires all six PASS with no falsifier
firing.

## 6. Frozen K-CB-5 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `e1+e2` (the hidden rule expression)
2. `CPY R0,R1` (the constructed first instruction)
3. `ADD R0,R2` (the constructed second instruction)
4. `0,0,1,1,0,2` (the constructed program prefix)
5. `3761` (train episode 1 digit string; no episode data in learner)
6. `3,7,6,1` (train episode 1 literal)
7. `stubble` (no world concept in the learner)
8. `threshold.*=.*12` (no hardcoded threshold; thresholds come only
   from sweeps over experience)
9. `_MODE` (zero modes allowed)
10. `bridge` (case-insensitive; nothing in code is a bridge handler)

## 7. Frozen falsifiers

- F-NO-CREATE: ARM-FULL construction yields n=0 or train score < 8/8.
- F-NO-TRUNC: ARM-FULL ADAPT-STAT trunc_count == 0.
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

- The op basis {CPY,ADD,SUB,MAX,MIN}, the 4-register recency window,
  the greedy construction policy, and the TRUNCATE standing rule are
  researcher-supplied generic machinery, frozen here. The L2 claim is
  that TRUNCATE fires on structural preconditions without per-problem
  researcher selection; the L3 claim is that M's final form
  ([CPY R0,R1, ADD R0,R2]) is source-underdetermined and
  history-determined, not that the basis is.
- Design note (disclosed): with a first-6 register loading, trailing
  constant slots (255 vs 0) are provably ignorable by the greedy
  search, so TRUNCATE could not be load-bearing. The fixed-capacity
  recency window is the disclosed consumer-side constraint that makes
  X's over-long replay displace informative readings, which is what
  TRUNCATE repairs. This is frozen machinery, not a per-problem fix.
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner. It enables the
  lesion comparison; it is not a runtime mode.
- The x_learn_len frozen timing (called once after phase-0, not
  re-run) is experimental control: it holds X's standing structure
  fixed so the lesion (TRUNCATE on/off) is interpretable. Re-running
  it would rebuild L rather than adapt the replay.
- The hidden world rule was designed by the builder, not an
  independent adversary. Sealed-adversary generality is open future
  work.
- One world family. No generality claim beyond the demonstrated arms.
- This build targets the six combo bars above. It does not claim
  Micah's full 12-criterion L3 bar.

## 10. Standing non-claims

- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. The frozen TNN core is not
  used here; this is a standalone learner-mechanism experiment.
