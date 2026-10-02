# PREREG: L2-L3 Specialize Combination (ORCHARD)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_l3_spec/` only.
Worker: L2-L3 Specialize Worker (subagent, 2026-10-02).
Parent mandate: demonstrate L2 adaptation AND L3 novel intermediate
creation in a SINGLE problem, where the L2 adaptation is SPECIALIZE
(not EXTEND, not TRUNCATE).

## 1. What is being tested

Whether one learner, on one problem, BOTH adapts an old structure
that is too general (L2: SPECIALIZE the recall procedure to the
queried episode's kind on structural preconditions) AND invents a
novel intermediate (L3: constructs the sequence to scalar reduction
through experience, its final form not enumerated in source). Prior
waves demonstrated L2 EXTEND + L3 (MEADOW, builder-designed; RELAY,
adversarial) and L2 TRUNCATE + L3 (STUBBLE, builder-designed). Open:
does L2+L3 work when the adaptation is SPECIALIZE?

Concrete scenario (ORCHARD):
- X: episode recall. X's standing replay is the general fixed replay:
  all 6 stored readings [k,a,b,c,d,e], where k (slot 0) is a kind
  tag (1 or 2) and a..e are data readings. The consumer is a
  fixed-capacity 2-register machine loading the first 2 replayed
  readings. The kind tag and the first data reading saturate it, so
  the kind-specific signal pair never reaches the registers. X alone
  is too general: one replay shape for every kind.
- L2 adaptation (SPECIALIZE): a standing rule inside recall. From old
  episodes X has learned per-kind informative slot masks: for each
  kind tag value, the slots (tag slot excluded) that vary across old
  episodes of that kind. On recall, iff ADAPT_ON==1, the replay is
  specialized to the queried episode's kind: only the kind's
  informative slots are replayed, in ascending slot order. Fires on
  structural preconditions computed from learner state (kind tag +
  learned masks), never selected per problem by the researcher.
  Adapted X' canonicalizes the view: kind 1 replays [d,e], kind 2
  replays [a,b]; in both cases (R0,R1) holds the signal pair.
- Y: threshold decide. Given a scalar s, Y outputs PICK(1) iff s >= t
  else SKIP(0). Y consumes a SCALAR. Threshold t=6 learned from prior
  scalar experience (first-max, 6/6).
- Hidden world rule: PICK iff the kind's signal pair sums >= 10.
  Kind 1 uses (d,e); kind 2 uses (a,b).
- L3 invention: the bridge between X' (2-reading canonical sequence)
  and Y (scalar) is a reduction program M constructed by greedy search
  over the frozen generic op basis {CPY,ADD,SUB,MAX,MIN} on 2
  registers, guided only by labeled episode experience. M is not
  selected from a menu of reductions. The frozen expectation is
  M = [ADD R0,R1]: specialization canonicalizes the signal pair into
  (R0,R1), so the invented intermediate is minimal.

The problem requires both: without SPECIALIZE the signal pair never
reaches the registers (the fixed replay is provably uninformative:
pairing proof, section 3); without the invented M the canonical
2-reading sequence cannot drive Y's scalar decision.

## 2. Frozen learner machinery (disclosed)

Generic machinery plus learned state. No episode data, no hidden world
rule, no reduction solution in the learner source. Adapted from
`l2_l3_combo/learner.zag`, with two disclosed deltas: (a) the L2
standing rule is SPECIALIZE (not EXTEND); (b) the reduction machine
has 2 registers with first-2 loading instead of 6 registers with
first-6 loading. The greedy construction policy, the op basis, the
label store, and the decide pipeline are unchanged in mechanism.

- State: one u8 buffer. Offsets: 0 XN, 1 LN, 2 YN, 3 YT_SET,
  4 REPLAY_LEN (learned), 5 ADAPT_ON (causal-control flag, set by the
  driver per arm, never written by the learner; the composition_l2
  adapt_on precedent). X slots: 16 episodes x 7 bytes
  [k,a,b,c,d,e] at 8..119 (unfilled slot = 255). Label slots:
  16 x 2 bytes at 120..151. Y threshold i32 at 152..155. M slot 32
  bytes at 156..187 [n,gen,sup,pad,threshold i32,24 program bytes].
  ADAPT-STAT: spec_count i32 at 252..255, recall_calls i32 at
  256..259. Y scalar observations 16 x 2 bytes at 220..251.
  MASK_K1 u8 at 260, MASK_K2 u8 at 261 (bit i = slot i informative
  for that kind; tag slot 0 never set).
- x_teach: stores id + 6 readings (unfilled = 255).
- x_learn_len: REPLAY_LEN = max k in 0..6 such that every taught
  episode has slots 0..k-1 filled. Learned from experience, not set
  by hand.
- x_learn_masks (new; the L2 learning step): for kind tag value v in
  {1,2}, over taught episodes whose slot 0 == v, MASK_Kv gets bit i
  (i in 1..5) iff slot i takes at least two distinct values across
  those episodes. FROZEN TIMING: called once, after phase-0 teaching
  (consolidation). It is not re-run after phase-1; the masks are X's
  standing per-kind structure, and SPECIALIZE is the recall-time
  adaptation under test.
- x_recall (contains the L2 SPECIALIZE standing rule): finds the
  episode by id (0 = unknown). Iff ADAPT_ON==1, reads the kind tag
  (slot 0) and the learned mask for that kind; if the mask is nonzero,
  replays exactly the masked slots in ascending order. Otherwise
  replays slots 0..L-1 (the general fixed replay). Returns readings
  replayed. Trailing out slots are zeroed. Increments recall_calls
  always and spec_count when the specialized replay was used. The rule
  is evaluated on every recall; the researcher never picks it per
  problem.
- y_teach / y_fit / y_decide: threshold sweep t=0..40 ascending,
  first-max (as in the combo build).
- Register machine: 2 registers R0,R1. Loading takes the first up to
  2 replayed readings (R0 = first, R1 = second; missing = 0). Frozen
  generic machinery: a fixed-capacity working memory, not a
  per-problem choice. It is the disclosed consumer-side constraint
  that makes X's over-general full replay saturate the registers with
  the tag and first data reading, which is what SPECIALIZE repairs.
- Reduction program: up to 8 instructions of (op,d,s), d,s in 0..1.
  Output is R0. Frozen op basis: 0=CPY, 1=ADD, 2=SUB, 3=MAX, 4=MIN.
  Not expandable (F-OP-EXPAND voids the build).
- construct(): greedy search from a given program. Each round
  evaluates every (op,d,s) append (5*4=20 candidates) by
  best-threshold classification score on the labeled episodes;
  applies the single append with the largest strictly positive gain;
  ties broken by candidate order (op 0..4, d 0..1, s 0..1,
  first-max). Stops at no positive gain or 8 instructions. Threshold
  sweep t=0..40 ascending, first-max.
- decide(ep_id): recall via X (SPECIALIZE applies per the standing
  rule); if recall finds nothing, or M absent (n==0), or Y threshold
  unset, return -1 (NO_DECISION). Else s=exec(M, registers); return
  Y(s). -1 never counts as correct.

## 3. Frozen world (environment, hidden from learner)

The driver generates labels from these rules; the learner source never
calls them.

- Phase 0 (old world, teaches the standing replay and the masks).
  Old episodes (id: [k,a,b,c,d,e]):
  O1 id=51: [1,0,0,0,3,7]; O2 id=52: [1,0,0,0,8,2];
  O3 id=53: [2,5,1,0,0,0]; O4 id=54: [2,2,6,0,0,0].
  Stored fully filled. x_learn_len -> L=6. x_learn_masks: kind 1
  episodes vary only in slots 4,5 -> MASK_K1 = bits {4,5} = 48;
  kind 2 episodes vary only in slots 1,2 -> MASK_K2 = bits {1,2} = 6.
- Y prior scalar experience: (7,pick),(8,pick),(9,pick),
  (3,skip),(4,skip),(5,skip). Y threshold t=6 (first-max; 6/6:
  t=5 gives 5/6).
- TRUE (phase 1): PICK iff (k==1 and d+e >= 10) or (k==2 and
  a+b >= 10).

Frozen episode tables (id: [k,a,b,c,d,e], label under TRUE):

Phase 1 train (labels from TRUE):
1: [1,0,0,0,4,9] pick    2: [1,0,0,0,9,4] pick
3: [1,0,0,0,4,1] skip    4: [1,0,0,0,1,4] skip
5: [2,4,9,0,0,0] pick    6: [2,9,4,0,0,0] pick
7: [2,4,1,0,0,0] skip    8: [2,1,4,0,0,0] skip
Phase 1 test:
9: [1,0,0,0,5,8] pick   10: [1,0,0,0,3,2] skip
11: [2,7,6,0,0,0] pick  12: [2,2,3,0,0,0] skip

Digit-string encodings (world.zag): old "100037","100082","251000",
"226000"; train "100049","100094","100041","100014","249000",
"294000","241000","214000"; test "100058","100032","276000","223000".

Frozen hand-derived expectations (the implementation must reproduce
them; any deviation is a falsifier, not a tuning opportunity):

- Phase-0 teaching then x_learn_len gives L=6; x_learn_masks gives
  MASK_K1=48, MASK_K2=6. After phase-1 teaching L is still 6.
- ARM-FULL construction on train ids 1..8 (ADAPT_ON=1; specialized
  replay: kind 1 -> [d,e], kind 2 -> [a,b]; hence R0=S0, R1=S1 with
  S0=[4,9,4,1,4,9,4,1], S1=[9,4,1,4,9,4,1,4], labels [1,1,0,0,1,1,0,0]):
  - Empty baseline: R0=S0. t sweep: t=0: 4/8; t=1: 4/8; t=2..9: 6/8;
    t>=10: 4/8. First-max: 6/8 at t=2. (Each single reading overlaps
    across the label split by design: S0 values 4 carry labels
    {1,0,1,0}.)
  - Round 1 (20 candidates, order op 0..4, d 0..1, s 0..1):
    (0,0,0): 6/8. (0,0,1) [CPY R0,R1]: R0=S1, values 9->{1,1},
    4->{1,0,1,0}, 1->{0,0}: max 6/8. (0,1,0),(0,1,1): 6/8.
    (1,0,0) [ADD R0,R0]: 2*S0, monotone in S0: 6/8.
    (1,0,1) [ADD R0,R1]: R0=S0+S1=[13,13,5,5,13,13,5,5]:
    t=6 is the first t with 8/8 (t<=5: 4/8). Gain 2 > 0. It is the
    FIRST 8/8 in candidate order. Adopt [ADD R0,R1], score=8, t=6.
    Later 8/8s lose the tie-break: (3,0,1) [MAX R0,R1] -> 8/8 at
    t=5; (4,0,1) [MIN R0,R1] -> 8/8 at t=2. (2,0,1) [SUB R0,R1]:
    max 6/8 (t=4..5). All others <= 6/8.
  - Round 2: base 8/8. Appends reach at most 8/8 (e.g. (1,0,0):
    R0=26/10, 8/8 at t=11; (3,0,1): MAX(13/5,S1), 8/8);
    no strictly positive gain; stop.
  - M-BUILT n=1 t=6 score=8/8. M slot program bytes:
    [1,0,1, 0,0,0, ...].
- ARM-FULL Z on test 9..12 (specialized replay; s=S0+S1; Y t=6 after
  T-AGREE, which genuinely agrees with the prior t=6):
  9: replay [5,8], s=13>=6 -> 1, true pick -> ok.
  10: replay [3,2], s=5<6 -> 0, true skip -> ok.
  11: replay [7,6], s=13>=6 -> 1, true pick -> ok.
  12: replay [2,3], s=5<6 -> 0, true skip -> ok. Z-FULL 4/4.
- ARM-L2-ONLY (specialization on, construction skipped): X' replays
  2 readings (spec fires; Z lines show 2-reading seqs), M slot n=0,
  decide -1 on all 4. Z-L2ONLY 0/4. Adaptation happened but Z still
  fails.
- ARM-L3-ONLY (specialization off, construction on): generic replay
  [k,a,b,c,d,e]; 2-register first-2 loading gives (R0,R1)=(k,a).
  Train (k,a) groups: (1,0): ids 1,2,3,4 labels 1,1,0,0; (2,4):
  ids 5,7 labels 1,0; (2,9): ids 6,8 labels 1,0. Any deterministic
  program on (k,a) is constant on each group, hence correct on
  exactly half of each group: 4/8 = the empty baseline (R0=k:
  t=0..1: 4/8; t=2: 4/8). Round 1 finds no positive gain;
  construction stops with M n=0. decide -1 on all 4. Z-L3ONLY 0/4.
  (Pairing proof; no candidate enumeration needed.)
- ARM-FRESH (nothing taught): x_recall finds nothing; Z-FRESH 0/4.

## 4. Frozen arms

- ARM-FULL: ADAPT_ON=1; phase-0 teach + x_learn_len + x_learn_masks
  (once each); Y prior; phase-1 teach+labels (masks not re-learned);
  construct M; Z on test 9..12. Expect 4/4, spec_count >= 1, M n=1
  with program [1,0,1,0,0,0,...], t=6.
- ARM-L2-ONLY: ADAPT_ON=1; same teaching; construction skipped
  (M slot stays n=0); Z on test. Expect 0/4 with spec_count >= 1.
- ARM-L3-ONLY: ADAPT_ON=0; same teaching; construct M; Z on test.
  Expect construction to yield n=0 and Z 0/4 with spec_count == 0.
- ARM-FRESH: ADAPT_ON=0; no teaching at all; Z on test. Expect 0/4.

## 5. Kill bars

- K-CB-1 (both required): ARM-L2-ONLY == 0/4 AND ARM-L3-ONLY == 0/4
  AND ARM-FULL == 4/4. The problem is unsolvable by either level
  alone and solvable by both together.
- K-CB-2 (L2-only fails): ARM-L2-ONLY == 0/4 with spec_count >= 1
  (adaptation genuinely fired but is insufficient without M).
- K-CB-3 (L3-only fails): ARM-L3-ONLY == 0/4 with spec_count == 0
  and constructed M n == 0 (no adaptation, and construction provably
  cannot reach the needed information: the pairing proof).
- K-CB-4 (combined succeeds with provenance): ARM-FULL == 4/4 AND
  ADAPT-STAT spec_count >= 1 AND the run log prints the M program
  bytes [1,0,1,0,0,0,...] with n=1 from learner state AND every Z
  line shows a 2-reading replayed sequence (adapted X' in the trace).
- K-CB-5 (M not in source): frozen grep audit on `learner.zag`
  returns zero hits for every pattern in section 6.
- K-CB-6 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L2-L3-SPEC-COMPLETE requires all six PASS with no falsifier
firing.

## 6. Frozen K-CB-5 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `d+e` (hidden rule fragment for kind 1)
2. `a+b` (hidden rule fragment for kind 2)
3. `ADD R0,R1` (the constructed instruction)
4. `1,0,1` (the constructed program triple)
5. `100049` (train episode 1 digit string; no episode data in learner)
6. `1,0,0,0,4,9` (train episode 1 literal)
7. `orchard` (no world concept in the learner)
8. `threshold.*=.*6` (no hardcoded threshold; thresholds come only
   from sweeps over experience)
9. `_MODE` (zero modes allowed)
10. `bridge` (case-insensitive; nothing in code is a bridge handler)

## 7. Frozen falsifiers

- F-NO-CREATE: ARM-FULL construction yields n=0 or train score < 8/8.
- F-NO-SPEC: ARM-FULL ADAPT-STAT spec_count == 0.
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

- The op basis {CPY,ADD,SUB,MAX,MIN}, the 2-register first-2 loading
  machine, the greedy construction policy, the per-kind variance mask
  learning, and the SPECIALIZE standing rule are researcher-supplied
  generic machinery, frozen here. The L2 claim is that SPECIALIZE
  fires on structural preconditions (kind tag + learned masks)
  without per-problem researcher selection; the L3 claim is that M's
  final form ([ADD R0,R1]) is source-underdetermined and
  history-determined, not that the basis is.
- Design note (disclosed): with a 6-register first-6 loading, the
  generic full replay would expose every reading to the greedy
  search, so SPECIALIZE could not be load-bearing. The
  fixed-capacity 2-register consumer is the disclosed constraint that
  makes X's over-general replay saturate the registers with the tag
  and first data reading, which is what SPECIALIZE repairs by
  canonicalizing the kind's signal pair into (R0,R1).
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner. It enables the
  lesion comparison; it is not a runtime mode.
- The x_learn_masks frozen timing (called once after phase-0, not
  re-run) is experimental control: it holds X's standing per-kind
  structure fixed so the lesion (SPECIALIZE on/off) is interpretable.
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
