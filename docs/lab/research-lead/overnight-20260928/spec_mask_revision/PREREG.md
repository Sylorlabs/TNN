# PREREG: Specialize Mask Revision (SHIFT)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/spec_mask_revision/` only.
Worker: Specialize Mask Revision Worker (subagent, 2026-10-02).
Parent mandate: test revision of SPECIALIZE masks when the world changes.

## 1. What is being tested

Whether a learner that learned per-kind informative slot masks
(SPECIALIZE, from L2-L3-SPEC-COMPLETE: MASK_K1=48, MASK_K2=12) can
REVISE those masks when the world changes and the informative slots
move. The prior build froze mask learning to a single post-phase-0
call (x_learn_masks). Open question: is the mask structure revisable
from new experience, or is it stuck with the old world's structure?

Concrete scenario (SHIFT):
- Phase 0/1 (old world, as in ORCHARD): masks learned 48/12;
  kind 1 signal pair (d,e), kind 2 signal pair (b,c); hidden rule
  TRUE1: PICK iff the kind's signal pair sums >= 10. M = [ADD R0,R1]
  constructed; phase-1 Z = 4/4. Masks work initially.
- Phase 2 (world change): the informative slots MOVE. Kind 1's
  signal pair is now (b,c) [slots 2,3]; kind 2's signal pair is now
  (d,e) [slots 4,5]. Hidden rule TRUE2: PICK iff (k==1 and b+c >= 10)
  or (k==2 and d+e >= 10). The old slots go quiet (zeros).
- The question: with stale masks the specialized replay delivers
  (0,0) and the pipeline breaks; after learner-side mask revision
  the replay canonicalizes the new signal pair into (R0,R1) again
  and performance is restored with the SAME invented M.

## 2. Frozen learner machinery (disclosed)

Generic machinery plus learned state. No episode data, no hidden
world rules, no reduction solution in the learner source. Adapted
from `l2_l3_spec/learner.zag` with disclosed deltas: (a) X store
grown to 32 episodes; (b) state offsets shifted accordingly;
(c) x_learn_masks replaced by x_revise_masks, a consolidation
function with a consolidation pointer REV_PTR: it recomputes the
per-kind variance masks over episodes with index in [REV_PTR, XN),
overwrites a kind's mask iff the window contains at least one
episode of that kind (no-data kinds keep the old mask), then sets
REV_PTR = XN. The driver schedules consolidation calls (the
frozen-timing precedent from l2_l3_spec): after phase-0 (initial
learn), after phase-1 (stability check), and, in the REVISE arm
only, after phase-2 training (revision). "Learning" vs "revision"
is timing, not mechanism: one generic re-consolidation function.

- State: one u8 buffer, 2048 bytes. Offsets: 0 XN, 1 LN, 2 YN,
  3 YT_SET, 4 REPLAY_LEN, 5 ADAPT_ON (driver-set causal control,
  never written by the learner). 8..231: X slots, 32 x 7 bytes
  [id,tag,s0..s4], 255 = empty. 232..295: labels, 32 x 2 bytes.
  296..299: Y threshold i32. 300..331: M slot, 32 bytes [n,gen,sup,
  pad,threshold i32,24 program bytes at 308..331]. 332..363: Mprev
  reserved. 364..395: Y scalar observations, 16 x 2 bytes.
  396..399: spec_count i32. 400..403: recall_calls i32.
  404: MASK_K1, 405: MASK_K2. 406..409: REV_PTR i32.
  410..2047: scratch.
- x_teach: stores id + 6 readings (unfilled = 255); 32-episode cap.
- x_learn_len: REPLAY_LEN = longest prefix filled in every taught
  episode. Learned from experience.
- x_revise_masks (the revision mechanism under test): as specified
  above. Variance criterion unchanged from l2_l3_spec: bit i
  (i in 1..5) set iff slot i takes at least two distinct values
  across window episodes of that kind.
- x_recall: the L2 SPECIALIZE standing rule, unchanged in mechanism:
  iff ADAPT_ON==1, reads the kind tag and replays exactly the
  learned mask's slots in ascending order when the mask is nonzero;
  otherwise the general fixed replay of slots 0..L-1.
- y_teach / y_fit / y_decide: threshold sweep t=0..40 ascending,
  first-max.
- Register machine: 2 registers, first-2 loading (the disclosed
  consumer-side constraint from l2_l3_spec).
- Reduction program: up to 8 instructions of (op,d,s); output R0.
  Frozen op basis {CPY,ADD,SUB,MAX,MIN}. Not expandable
  (F-OP-EXPAND voids the build).
- construct(): greedy search, 20 candidates/round, first-max
  tie-breaking, stops at no strictly positive gain or 8
  instructions. Threshold sweep t=0..40 ascending, first-max.
- decide(ep_id): recall via X; -1 (NO_DECISION) if recall finds
  nothing, M absent (n==0), or Y unset. Else s=exec(M); Y(s).

TRIGGER DISCLOSURE: the revision trigger is driver-scheduled
re-consolidation (experimental control, same precedent as the
original frozen timing). The claim under test is that the learner
CAN revise masks from new experience via the generic mechanism,
not that it autonomously detects the world change. Autonomous
change detection is open future work.

## 3. Frozen world (environment, hidden from learner)

Phase 0 and phase 1 are the ORCHARD tables verbatim (amendment A1
form). Phase 2 is new.

- Phase 0 old episodes (id: [k,a,b,c,d,e]):
  O1 id=51: [1,0,0,0,3,7]; O2 id=52: [1,0,0,0,8,2];
  O3 id=53: [2,0,5,1,0,0]; O4 id=54: [2,0,2,6,0,0].
  Digit strings: "100037","100082","205100","202600".
  x_learn_len -> L=6. First consolidation (REV_PTR 0 -> 4):
  kind 1 varies slots 4,5 -> MASK_K1 = 48; kind 2 varies slots
  2,3 -> MASK_K2 = 12.
- Y prior scalar experience: (7,pick),(8,pick),(9,pick),
  (3,skip),(4,skip),(5,skip). y_fit -> t=6 (first-max, 6/6).
- TRUE1 (phase 1): PICK iff (k==1 and d+e >= 10) or (k==2 and
  b+c >= 10).
- Phase 1 train (id: [k,a,b,c,d,e], label under TRUE1):
  1: [1,0,0,0,4,9] pick    2: [1,0,0,0,9,4] pick
  3: [1,0,0,0,4,1] skip    4: [1,0,0,0,1,4] skip
  5: [2,0,4,9,0,0] pick    6: [2,0,9,4,0,0] pick
  7: [2,0,4,1,0,0] skip    8: [2,0,1,4,0,0] skip
  Digit strings: "100049","100094","100041","100014",
  "204900","209400","204100","201400".
- Phase 1 test:
  9: [1,0,0,0,5,8] pick   10: [1,0,0,0,3,2] skip
  11: [2,0,7,6,0,0] pick  12: [2,0,2,3,0,0] skip
  Digit strings: "100058","100032","207600","202300".
- TRUE2 (phase 2, the world change): PICK iff (k==1 and b+c >= 10)
  or (k==2 and d+e >= 10). The informative slots move: kind 1 now
  (b,c), kind 2 now (d,e); old slots are zero.
- Phase 2 train (id: [k,a,b,c,d,e], label under TRUE2):
  21: [1,0,4,9,0,0] pick   22: [1,0,9,4,0,0] pick
  23: [1,0,4,1,0,0] skip   24: [1,0,1,4,0,0] skip
  25: [2,0,0,0,4,9] pick   26: [2,0,0,0,9,4] pick
  27: [2,0,0,0,4,1] skip   28: [2,0,0,0,1,4] skip
  Digit strings: "104900","109400","104100","101400",
  "200049","200094","200041","200014".
- Phase 2 test:
  29: [1,0,5,8,0,0] pick   30: [1,0,3,2,0,0] skip
  31: [2,0,0,0,7,6] pick   32: [2,0,0,0,2,3] skip
  Digit strings: "105800","103200","200076","200023".

Frozen hand-derived expectations (the implementation must
reproduce them; any deviation is a falsifier):

- After phase-0 consolidation: MASK_K1=48, MASK_K2=12, REV_PTR=4.
- Phase-1 consolidation (window = episodes 4..15, i.e. phase-1
  train+test; kind 1 varies slots 4,5, kind 2 varies slots 2,3):
  masks UNCHANGED 48/12, REV_PTR=16. Stability control: revision
  does not spuriously change masks when the world is stable.
- M1 construction on phase-1 train ids 1..8 (ADAPT_ON=1, masks
  48/12; R0=[4,9,4,1,4,9,4,1], R1=[9,4,1,4,9,4,1,4], labels
  [1,1,0,0,1,1,0,0]): identical values to the l2_l3_spec hand
  derivation, so C-ROUND 1 base=6 eval=20 win=1,0,1 gain=2
  score=8 t=6; C-ROUND 2 base=8 eval=20 stop. M1 n=1, t=6,
  prog=[1,0,1,0,0,0,...]. Y prior t=6 agrees (T-AGREE y=6 m=6).
- Z-PHASE1 on test 9..12 (specialized replay [d,e]/[b,c], s=S0+S1,
  Y t=6): 9: s=13 -> 1 ok; 10: s=5 -> 0 ok; 11: s=13 -> 1 ok;
  12: s=5 -> 0 ok. Z-PHASE1 4/4.
- ARM-STALE-KEEP (no revision; M1 reused; stale masks 48/12):
  29 kind 1 -> replay [d,e]=(0,0), s=0 < 6 -> dec 0, true 1,
  wrong. 30 -> dec 0, true 0, right. 31 kind 2 -> replay
  [b,c]=(0,0) -> dec 0, true 1, wrong. 32 -> dec 0, true 0,
  right. Z-STALE-KEEP exactly 2/4 (both picks missed; the
  always-skip baseline).
- ARM-STALE-REBUILD (no revision; construction re-run on phase-2
  train ids 21..28 with stale masks): every train episode replays
  (0,0): kind 1 replays slots {4,5} = (0,0); kind 2 replays slots
  {2,3} = (0,0). Empty baseline R0=0: t=0 -> 4/8 (all pick),
  t>=1 -> 4/8 (all skip); first-max t=0, 4/8. Round 1: all 20
  candidates evaluate on constant (0,0) -> 4/8; no strictly
  positive gain; stop with n=0. Trace: `C-ROUND 1 base=4 eval=20
  stop`. decide -> -1 on all 4 (M absent). Z-STALE-REBUILD 0/4.
  This is the information-starvation proof: the break is at the
  mask level, not in M.
- ARM-REVISE (x_revise_masks after phase-2 train teaching, before
  phase-2 test teaching; window = episodes 16..23 = ids 21..28):
  kind 1 (ids 21..24) varies slots 2,3 only -> MASK_K1 = bits
  {2,3} = 12; kind 2 (ids 25..28) varies slots 4,5 only ->
  MASK_K2 = bits {4,5} = 48; REV_PTR=24. Masks SWAP 48<->12.
  M1 reused (M slot still n=1, prog [1,0,1,...], t=6).
  Z on test 29..32: 29 -> replay [5,8], s=13 -> 1, true 1, ok.
  30 -> [3,2], s=5 -> 0, true 0, ok. 31 -> [7,6], s=13 -> 1,
  true 1, ok. 32 -> [2,3], s=5 -> 0, true 0, ok. Z-REVISE 4/4.

## 4. Frozen arms (each an independent learner state, ADAPT_ON=1)

- ARM-BASE: phase-0 teach + consolidation; Y prior; phase-1
  teach+labels; phase-1 consolidation; construct M1; Z on phase-1
  test 9..12. Expect Z-PHASE1 4/4, M1 n=1 prog [1,0,1,...] t=6.
- ARM-STALE-KEEP: ARM-BASE pipeline, then phase-2 train+labels and
  phase-2 test teach, NO revision call, M1 reused; Z on phase-2
  test 29..32. Expect exactly 2/4.
- ARM-STALE-REBUILD: ARM-BASE pipeline, then phase-2 train+labels,
  construction re-run on phase-2 train ids 21..28 (stale masks),
  phase-2 test teach; Z on phase-2 test. Expect M n=0 and Z 0/4.
- ARM-REVISE: ARM-BASE pipeline, then phase-2 train+labels,
  x_revise_masks (driver-scheduled), phase-2 test teach, M1
  reused; Z on phase-2 test. Expect masks 12/48, REV_PTR=24,
  Z-REVISE 4/4.

## 5. Kill bars

- K-RV-1 (masks learned): post-phase-0 MASK_K1 == 48 AND
  MASK_K2 == 12 (from ARM-BASE state).
- K-RV-2 (work initially): Z-PHASE1 == 4/4 AND M1 n == 1 with
  program bytes [1,0,1,0,0,0,...] and t == 6 from learner state.
- K-RV-3 (world change breaks them): Z-STALE-KEEP == 2/4 exactly
  AND STALE-REBUILD construction yields n == 0 (trace shows
  `C-ROUND 1 base=4 eval=20 stop`) AND Z-STALE-REBUILD == 0/4.
- K-RV-4 (learner revises masks): post-revision MASK_K1 == 12 AND
  MASK_K2 == 48 AND REV_PTR == 24 in ARM-REVISE state.
- K-RV-5 (revised work): Z-REVISE == 4/4 with M1 reused (M slot
  still n == 1, prog [1,0,1,0,0,0,...], t == 6) AND every Z line
  shows a 2-reading replayed sequence.
- K-RV-6 (provenance): phase-1 consolidation leaves masks 48/12
  (stability: no spurious revision when the world is stable) AND
  ADAPT-STAT spec >= 1 in ARM-REVISE (specialization fired in the
  trace) AND the frozen grep audit on learner.zag returns zero
  hits for every pattern in section 6.
- K-RV-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict SPEC-MASK-REVISION-COMPLETE requires all seven PASS with
no falsifier firing.

## 6. Frozen K-RV-6 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `d+e` (hidden rule fragment)
2. `b+c` (hidden rule fragment)
3. `ADD R0,R1` (the constructed instruction)
4. `1,0,1` (the constructed program triple)
5. `100049` (phase-1 train episode 1 digit string)
6. `104900` (phase-2 train episode 21 digit string)
7. `200049` (phase-2 train episode 25 digit string)
8. `1,0,0,0,4,9` (phase-1 train episode 1 literal)
9. `1,0,4,9,0,0` (phase-2 train episode 21 literal)
10. `orchard` (no world concept in the learner)
11. `threshold.*=.*6` (no hardcoded threshold; thresholds come only
    from sweeps over experience)
12. `_MODE` (zero modes allowed)
13. `bridge` (case-insensitive; nothing in code is a bridge handler)

## 7. Frozen falsifiers

- F-NO-LEARN: post-phase-0 masks != (48,12).
- F-NO-BASE: Z-PHASE1 != 4/4 or M1 n != 1.
- F-NO-BREAK: Z-STALE-KEEP != 2/4, or STALE-REBUILD n > 0, or
  Z-STALE-REBUILD > 0.
- F-NO-REVISE: post-revision masks != (12,48) or REV_PTR != 24.
- F-NO-RECOVER: Z-REVISE != 4/4.
- F-SPURIOUS: phase-1 consolidation changes either mask.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN}
  for any reason. Voids the build.
- F-AUDIT: any K-RV-6 pattern matches in learner.zag. Voids the
  build.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps. Output via a single preallocated buffer
and one raw syscall write. 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the 2-register first-2 loading
  machine, the greedy construction policy, the variance mask
  criterion, the consolidation pointer, the SPECIALIZE standing
  rule, and the driver-scheduled consolidation timing are
  researcher-supplied generic machinery, frozen here. The claim is
  that x_revise_masks recomputes per-kind informative masks from
  post-change experience through the generic window mechanism,
  with no world knowledge in the learner.
- ADAPT_ON is a driver-set causal-control flag (the
  composition_l2 adapt_on precedent), never written by the
  learner. It is not a runtime mode.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality is open future
  work.
- One world family (kind-tagged aggregation with a slot move). No
  generality claim beyond the four demonstrated arms.
- This build targets the seven revision bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- Autonomous change detection (the learner deciding WHEN to
  revise) is explicitly NOT tested here; the trigger is
  driver-scheduled. This is disclosed, not hidden.

## 10. Standing non-claims

- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. The frozen TNN core is
  not used here; this is a standalone learner-mechanism experiment.
