# PREREG: Autonomous Change Detection (ADETECT)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/autonomous_detect/` only.
Worker: Autonomous Change Detection Worker (subagent, 2026-10-02).
Parent mandate: test AUTONOMOUS change detection (learner detects the
world change on its own and triggers mask revision itself).

## 1. What is being tested

SPEC-MASK-REVISION-COMPLETE showed a learner CAN revise stale
SPECIALIZE masks from new experience via x_revise_masks, but the
trigger was driver-scheduled re-consolidation (disclosed control).
Boundary: "autonomous change detection explicitly not tested". Open
question: can the learner DETECT that the world changed and TRIGGER
the revision itself?

Operationalization. The learner has no labels in phase 2, so it
cannot measure accuracy. What it CAN observe is its own decision
stream: the exec(M) decision scores s it produces on every decide().
Under a stable world those scores follow the learned distribution;
after the slot move, the stale masks replay (0,0) and every score
collapses to s=0, a value never seen in baseline. The learner runs
a generic surprise monitor on its own score stream and requests
revision when surprise persists. The claim under test: the
learner-side monitor detects the change from its own observable
stream and the learner-side x_maybe_revise triggers the generic
re-consolidation without the driver deciding to revise.

Disclosed boundary of "autonomous": the driver still supplies the
standing opportunity (it calls x_maybe_revise after each batch, like
a heartbeat) and schedules baseline recording (x_record_baseline).
The DECISION to revise (DET_REVISE_REQ written only by learner
monitor logic) and the revision itself (x_revise_masks on learner
state) are the learner's. What this build does NOT claim: the
learner choosing when to record baselines, or detecting a change
that leaves its score distribution unchanged.

## 2. Frozen learner machinery (disclosed)

Adapted from `spec_mask_revision/learner.zag` with disclosed deltas:
(a) new detection monitor state at offsets 410..431; (b) decide()
pushes every real decision score to a 4-slot ring and runs the
surprise monitor; (c) x_record_baseline freezes baseline stats from
the ring; (d) x_maybe_revise revises iff DET_REVISE_REQ==1. All other
machinery (X store, SPECIALIZE replay, x_revise_masks, construct,
Y threshold, 2-register machine, op basis {CPY,ADD,SUB,MAX,MIN})
unchanged.

- State: one u8 buffer, 2048 bytes. Offsets 0..409 as in
  spec_mask_revision (XN, LN, YN, YT_SET, REPLAY_LEN, ADAPT_ON,
  X slots 8..231, labels 232..295, Y threshold 296..299, M slot
  300..331, Mprev 332..363, Y scalars 364..395, ADAPT-STAT
  396..403, MASK_K1 404, MASK_K2 405, REV_PTR 406..409).
  New detection state:
  410..413: DET_BASE_MEAN i32 (baseline mean of decision scores)
  414..417: DET_BASE_SPREAD i32 (baseline max abs deviation)
  418: DET_BASE_SET (1 = baseline recorded)
  419: DET_SURP_RUN (consecutive surprising decisions)
  420: DET_REVISE_REQ (1 = learner requests revision; written ONLY
       by the monitor inside decide(), never by the driver)
  421..424: DET_REV_COUNT i32 (autonomous revisions performed)
  425..428: DET_RING, 4 bytes, last 4 decision scores (u8 each)
  429: DET_RING_N (slots filled, 0..4)
  430: DET_RING_POS (next write position, 0..3)
  431: DET_LAST_SURP (surprise flag of the last decision, trace)
  432..2047: scratch.
- decide(): unchanged path (X recall, exec M, Y decide), plus: when
  a real score s is produced (replay found, M present, Y set), s
  is pushed to DET_RING; iff DET_BASE_SET==1, the score is
  surprising iff |s - DET_BASE_MEAN| > DET_BASE_SPREAD (strict);
  surprising increments DET_SURP_RUN else resets it to 0; if
  DET_SURP_RUN >= 3 then DET_REVISE_REQ = 1. DET_LAST_SURP records
  the flag for the trace. The trigger threshold 3 is a frozen
  generic parameter, not tuned to any world.
- x_record_baseline(st): iff DET_RING_N==4: DET_BASE_MEAN =
  sum/4 (integer division); DET_BASE_SPREAD = max |ring[i] - mean|;
  DET_BASE_SET=1; DET_SURP_RUN=0. Driver-scheduled (disclosed).
- x_maybe_revise(st): iff DET_REVISE_REQ==1: calls x_revise_masks
  (the unchanged generic re-consolidation over [REV_PTR, XN));
  DET_REVISE_REQ=0; DET_SURP_RUN=0; DET_REV_COUNT++. Returns 1 if
  it revised, else 0. The driver calls this after every batch; the
  learner decides whether to revise.
- x_revise_masks, x_recall/SPECIALIZE, construct, y_fit/y_decide,
  p_exec: unchanged from spec_mask_revision.

## 3. Frozen world (environment, hidden from learner)

Phase 0/1/2 tables and hidden rules TRUE1/TRUE2 are verbatim from
spec_mask_revision/world.zag. New: phase 5, a STABLE-world batch
(same distribution as phase 1, new ids), for the no-false-trigger
arm.

- Phase 5 stable episodes (id: [k,a,b,c,d,e]), labels under TRUE1:
  41: [1,0,0,0,4,9] pick   42: [1,0,0,0,1,4] skip
  43: [2,0,4,9,0,0] pick   44: [2,0,1,4,0,0] skip
  Digit strings: "100049","100014","204900","201400".
- Frozen test labels: phase 1 test ids 9..12: 1,0,1,0; phase 2 test
  ids 29..32: 1,0,1,0; phase 5 ids 41..44: 1,0,1,0; phase 2 train
  ids 21..28: 1,1,0,0,1,1,0,0.

Frozen hand-derived expectations (the implementation must
reproduce them; any deviation is a falsifier):

- Phase-1 test decisions (masks 48/12, M1 [ADD R0,R1], t=6):
  9 -> replay [5,8], s=13 -> 1, true 1, ok; 10 -> [3,2], s=5 -> 0,
  true 0, ok; 11 -> [7,6], s=13 -> 1, true 1, ok; 12 -> [2,3],
  s=5 -> 0, true 0, ok. Z-PHASE1 4/4. Ring = [13,5,13,5].
- x_record_baseline: mean = 36/4 = 9; spread = max(4,4,4,4) = 4;
  DET_BASE_SET=1, DET_SURP_RUN=0, DET_REVISE_REQ=0.
- ARM-STABLE phase-5 decisions: 41 -> s=13, d=|13-9|=4, not > 4,
  not surprising; 42 -> s=5, d=4, not surprising; 43 -> s=13;
  44 -> s=5. Z-STABLE 4/4. DET_SURP_RUN stays 0, DET_REVISE_REQ
  stays 0, DET_REV_COUNT stays 0. x_maybe_revise returns 0.
  Masks stay 48/12, REV_PTR stays 16.
- ARM-CHANGE / ARM-NOREVISE phase-2 train evaluation (stale masks
  48/12; every replay is (0,0)): decisions on ids 21..28 all s=0,
  dec=0. Labels 1,1,0,0,1,1,0,0 -> correct on 23,24,27,28 only:
  Z-TRAIN-EVAL 4/8 (the always-skip baseline; externally measured
  performance drop from 4/4). Monitor: d=|0-9|=9 > 4, surprising,
  every decision; DET_SURP_RUN reaches 3 at the 3rd decision ->
  DET_REVISE_REQ=1 (learner-set; the driver never writes offset
  420). Ring = [0,0,0,0].
- ARM-CHANGE x_maybe_revise: DET_REVISE_REQ==1 -> x_revise_masks
  over window [16,24) = phase-2 train episodes 21..28: kind 1
  varies slots 2,3 only -> MASK_K1=12; kind 2 varies slots 4,5
  only -> MASK_K2=48; REV_PTR=24; DET_REVISE_REQ=0;
  DET_SURP_RUN=0; DET_REV_COUNT=1. Returns 1.
- ARM-CHANGE phase-2 test (revised masks 12/48, M1 reused):
  29 -> replay [5,8], s=13 -> 1, true 1, ok; 30 -> [3,2], s=5 ->
  0, true 0, ok; 31 -> [7,6], s=13 -> 1, true 1, ok; 32 -> [2,3],
  s=5 -> 0, true 0, ok. Z-CHANGE 4/4. Post-revision d=4 each:
  no surprise, no second trigger.
- ARM-NOREVISE (driver withholds x_maybe_revise after train
  evaluation): DET_REVISE_REQ stays 1, masks stay 48/12,
  REV_PTR stays 16, DET_REV_COUNT stays 0. Phase-2 test: replays
  (0,0), s=0, dec=0 -> correct on 30,32 only: Z-NOREVISE 2/4.
  (Note: during this test the monitor keeps firing; that is
  expected and reported, not a bar.)

## 4. Frozen arms (each an independent learner state, ADAPT_ON=1)

- ARM-STABLE: phase-0 teach + consolidation (masks 48/12);
  Y prior; phase-1 train + test teach; consolidation-1 (stability:
  masks unchanged 48/12, REV_PTR=16); construct M1; x_maybe_revise
  (no-op); Z on phase-1 test 9..12 (fills ring); x_record_baseline;
  phase-5 teach; Z-STABLE on 41..44; x_maybe_revise (no-op).
  Expect: Z-STABLE 4/4, REVISE_REQ 0, REV_COUNT 0, masks 48/12.
- ARM-CHANGE: as ARM-STABLE through x_record_baseline, then
  phase-2 train teach; Z-TRAIN-EVAL on 21..28 (driver-scored
  against taught labels; monitor live); x_maybe_revise
  (AUTONOMOUS revision); phase-2 test teach; Z-CHANGE on 29..32.
  Expect: Z-TRAIN-EVAL 4/8, REVISE_REQ set by learner during
  evaluation, REV_COUNT 1, masks 12/48, REV_PTR 24,
  Z-CHANGE 4/4 with M1 reused.
- ARM-NOREVISE: as ARM-CHANGE through Z-TRAIN-EVAL, but the driver
  never calls x_maybe_revise; phase-2 test teach; Z-NOREVISE on
  29..32. Expect: REVISE_REQ 1 (detection fired), masks 48/12,
  REV_COUNT 0, Z-NOREVISE 2/4. Causal control: detection without
  the revision action does not recover performance.

## 5. Kill bars

- K-AD-1 (baseline recorded): post-x_record_baseline in ARM-CHANGE:
  DET_BASE_SET == 1 AND DET_BASE_MEAN == 9 AND DET_BASE_SPREAD == 4
  AND DET_REVISE_REQ == 0.
- K-AD-2 (stable world, no trigger): ARM-STABLE: Z-STABLE == 4/4
  AND DET_REVISE_REQ == 0 AND DET_REV_COUNT == 0 AND MASK_K1 == 48
  AND MASK_K2 == 12 (after the final x_maybe_revise).
- K-AD-3 (world change: performance drops, learner detects):
  ARM-NOREVISE: Z-TRAIN-EVAL == 4/8 (external performance drop)
  AND DET_REVISE_REQ == 1 (learner-set detection) AND MASK_K1 == 48
  AND MASK_K2 == 12 AND DET_REV_COUNT == 0 AND Z-NOREVISE == 2/4.
- K-AD-4 (autonomous trigger + revision): ARM-CHANGE: after
  x_maybe_revise, DET_REV_COUNT == 1 AND DET_REVISE_REQ == 0 AND
  MASK_K1 == 12 AND MASK_K2 == 48 AND REV_PTR == 24.
- K-AD-5 (recovery): ARM-CHANGE: Z-CHANGE == 4/4 with M1 reused
  (M slot n == 1, prog bytes [1,0,1,0,0,0,...], t == 6) AND every
  Z-CHANGE line shows a 2-reading replayed sequence.
- K-AD-6 (provenance): phase-1 consolidation leaves masks 48/12
  (no spurious revision when stable) AND ADAPT-STAT spec >= 1 in
  ARM-CHANGE AND the frozen grep audit on learner.zag returns zero
  hits for every pattern in section 6.
- K-AD-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict AUTONOMOUS-DETECT-COMPLETE requires all seven PASS with no
falsifier firing.

## 6. Frozen K-AD-6 grep audit spec (run on learner.zag)

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
14. `w_true` (no world-rule access from the learner)

## 7. Frozen falsifiers

- F-NO-BASE: post-baseline DET_BASE_SET != 1 or mean != 9 or
  spread != 4 or REVISE_REQ != 0.
- F-FALSE-TRIGGER: ARM-STABLE REVISE_REQ == 1 or REV_COUNT > 0 or
  either mask != (48,12) after the final x_maybe_revise.
- F-NO-DROP: ARM-NOREVISE Z-TRAIN-EVAL != 4/8.
- F-NO-DETECT: ARM-NOREVISE DET_REVISE_REQ == 0 after train
  evaluation.
- F-NO-REVISE: ARM-CHANGE post-maybe_revise masks != (12,48) or
  REV_PTR != 24 or REV_COUNT != 1.
- F-NO-RECOVER: ARM-CHANGE Z-CHANGE != 4/4.
- F-CONTROL-BROKEN: ARM-NOREVISE Z-NOREVISE != 2/4 (the control
  must show detection without revision stays broken).
- F-SPURIOUS: phase-1 consolidation changes either mask.
- F-OP-EXPAND: the op basis is extended beyond {CPY,ADD,SUB,MAX,MIN}
  for any reason. Voids the build.
- F-AUDIT: any K-AD-6 pattern matches in learner.zag. Voids the
  build.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the build.

## 8. Determinism spec

No RNG. Fixed candidate order, first-max tie-breaking everywhere,
ascending threshold sweeps, ascending monitor logic. Output via a
single preallocated buffer and one raw syscall write. 3/3
byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The op basis, 2-register machine, greedy construction, variance
  mask criterion, consolidation pointer, SPECIALIZE standing rule,
  driver-scheduled consolidation timing, driver-scheduled baseline
  recording, the standing x_maybe_revise heartbeat call, and the
  trigger threshold 3 are researcher-supplied generic machinery,
  frozen here. The claim is that the learner's monitor detects the
  world change from its own score stream and the learner's
  x_maybe_revise triggers the generic re-consolidation, with no
  world knowledge in the learner and no driver decision to revise.
- ADAPT_ON is a driver-set causal-control flag, never written by
  the learner. It is not a runtime mode.
- Detection uses distributional surprise in exec(M) scores, the
  learner-observable proxy for a world change; the driver measures
  the true accuracy drop (4/4 -> 4/8) externally. A world change
  that leaves the learner's score distribution unchanged would not
  be detected; that is disclosed, not hidden.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality is open future
  work.
- One world family (kind-tagged aggregation with a slot move). No
  generality claim beyond the three demonstrated arms.
- This build targets the seven detection bars above. It does not
  claim Micah's full 12-criterion L3 bar.

## 10. Standing non-claims

- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. The frozen TNN core is
  not used here; this is a standalone learner-mechanism experiment.
