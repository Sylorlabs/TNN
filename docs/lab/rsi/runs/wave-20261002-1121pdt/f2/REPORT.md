# REPORT: F2 v6 3x SEALED EVALUATION (wave-20261002-1121pdt, lane F2)

Task: queue item 10. Re-run the frozen F2 v6 sealed evaluation
(PREREG_F2V6.md, frozen 2026-10-02, wave-20261002-0521pdt) that went
PARTIAL under CPU contention. Measure K6-R4 (convergence + two
revisions + wave-3 goal achievement) under serialized, clean-as-possible
CPU conditions. Pure Zag throughout.

## Provenance (inherited, not re-authored)

- Prereg: docs/lab/rsi/runs/wave-20261002-0521pdt/F2/PREREG_F2V6.md
  (frozen commit 8f99040b3; NC5 amendment 3c69d53cb).
- Implementation: .../0521pdt/F2/f2v6_learner.zag @50693d022
  (206 changed lines vs v5 base; sha256
  e041d4f6bfcdccf851a05167ace6d492b76d7ac60f6a8f4ad0e61ee9e8404d87).
- Prior sealed record: .../0521pdt/F2/SEALED_EVAL.md (PARTIAL).
- This lane modifies NO source and NO sealed world. Rebuild only.

## Seal verification (before any run)

World hashes recomputed and matched against the prereg freeze record:

- shift2: 05e26e0854427b07fa3b0971f46d22cdec368f9d84bad1b6a057d05f730ca054 MATCH
- shift1: c0986c12fd3ad22366b37eb943927c1df7ba482557b18a75ccbae5f075dc6f5c MATCH
- osc:    2fb92115015f385649fbab78f40fcc8b815d9c3db725d2ad4b7db005f74a0470 MATCH

Seal holds. Worlds frozen (committed) before all runs below.

## Kill bars applied (frozen, unmoved)

K6-R1..R8 per PREREG_F2V6.md section 8. Negative controls NC1..NC5 per
section 9 (NC5 per the 2026-10-02 amendment). BUILD-PASS requires all
eight bars; any FAIL is BUILD-FAIL.

## Run conditions

- Toolchain: safebin znc (/home/hatch/safebin/znc); python3/python
  resolve to nothing (NAMECHECK.md Step 0).
- Sealed binary: /tmp/f2v6_shift2, sha256
  196c889361dfae6968318b132b054f481a23037ef059756578b69beca559a545
  (built from frozen sources via lane build.sh; hash reproduced
  byte-identically after a machine reboot + rebuild).
- Serialization: one sealed run at a time; no compiles in parallel
  with measurement; live scaling binaries (s5f_bin, s10000_bin_fixed)
  not disturbed.
- Byte-identical check: sha256sum + cmp over the binary's stdout
  (run metadata kept in separate .meta files, not in the compared log).

## Environmental incident (not scientific)

At ~2026-10-02 21:58 UTC the VM rebooted (uptime reset; all processes
lost, /tmp wiped). Run 1 was at ~2h45m wall, in the wave-3 11-action
planning phase (log intact through S2_VERIFY_RESULT 3, 1240 lines;
archived as eval_logs/shift2_r1_reboot_partial.log). The partial run
does not count toward K6-R7. The binary was rebuilt from the frozen
sources; sha256 reproduced exactly
(196c889361dfae6968318b132b054f481a23037ef059756578b69beca559a545),
confirming build determinism. Run 1 restarted from scratch at
~22:00 UTC. CPU contention from other lanes' restarted binaries
continues; documented per run.

## SHIFT2 sealed runs (the 11-action planning gap)

Run 1 (restarted after VM reboot at ~21:58 UTC; prior partial archived):

- Wave 1: SURVIVORS [46], S2_VERIFY_RESULT 1 (Regime 1). PLAN_C2
  [SX,SJ,SK,W,SX,W,SX] (7 actions). GOAL_REAL_C2 0 (failed as designed).
  PRED_VS_ACTUAL mismatch logged. REVISION_TRIGGER wave=1 -> wave=2.
  Byte-identical to 0521pdt wave 1.
- Wave 2: SURVIVORS [82], S2_VERIFY_RESULT 2 (Regime 2). PLAN_C2
  [SX,SJ,SK,W,SX,W,SX,W,SX] (9 actions). GOAL_REAL_C2 0 (failed).
  PRED_VS_ACTUAL mismatch logged. REVISION_TRIGGER wave=2 -> wave=3.
  Byte-identical to 0521pdt wave 2.
- Wave 3: SURVIVORS [82], S2_VERIFY_RESULT 3 (Regime 3). Convergence
  byte-identical to 0521pdt wave 3 (same line count, same survivor).
  11-action planning IN PROGRESS at report time (binary alive, 21:51
  CPU, exhaustive search in d=11 region). Not yet complete.

Runs 2-3: not started (serialized; run 1 must complete first).

K6-R1: NHYP 54/216/216 across waves (all >= 2). PASS (from completed waves).
K6-R2: source audit clean (IMPLEMENTATION.md). PASS.
K6-R3: ledger complete, zero world calls in search, REVISION_TRIGGERs
  cite PRED_VS_ACTUAL mismatches. PASS (from completed waves).
K6-R4: conv 1/2/3 YES; exactly 2 revisions YES; wave-3 plan found and
  GOAL_REAL_C2=1 UNMEASURED (planning incomplete). UNMEASURED.
K6-R5: wave-3 GOAL_REAL_C2 UNMEASURED; random control not yet run. UNMEASURED.
K6-R6: OBS_USED 20/21 in waves 1-2 (well under 110 budget). Partial.
K6-R7: 3/3 byte-identical runs NOT completed. UNMET.
K6-R8: regression not re-run this wave (binary byte-identical to 0521pdt
  build; 0521pdt regression PASS). Inherited.

## K6-R4 adjudication (mechanical, from logs)

K6-R4 requires: wave-1 conv=1 AND wave-1 plan fails for real with logged
contradiction AND exactly two revisions AND wave-2 conv=2 AND wave-2 plan
fails with contradiction AND wave-3 conv=3 AND wave-3 plan achieves goal.

Measured: conv 1/2/3 confirmed (S2_VERIFY_RESULT 1/2/3, single survivors
46/82/82). Two revisions confirmed (REVISION_TRIGGER wave=1, wave=2,
both gated on PRED_VS_ACTUAL mismatch). Wave-3 goal achievement
UNMEASURED: the 11-action exhaustive planning had not completed at
report time (binary in d=11 search, 21:51 CPU, no PLAN_C2 emitted).

K6-R4: UNMEASURED (not killed; the bar was not tested to completion).

## Negative controls

NC1: random control runs with wave 3 (not yet reached). Pending.
NC2: not re-run (0521pdt: NC2_RESULT 0, PASS). Inherited.
NC3: not re-run (0521pdt: v5-base PROGRAM_FAIL, VOID CONDITION SATISFIED). Inherited.
NC4: not re-run (0521pdt: v6 on SHIFT1, nrev=1, PASS). Inherited.
NC5: not re-run (0521pdt: v6 on OSC, nrev=1, PASS). Inherited.

## Regression (K6-R8)

Not re-run this wave. The binary was rebuilt from the identical frozen
source and is sha256-identical to the 0521pdt build
(196c889361dfae6968318b132b054f481a23037ef059756578b69beca559a545),
under which 0521pdt regression passed (A-prime and C2-prime,
PROGRAM_ALL_BARS_PASS, mask 63, nrev=0).

## Red team

### RT1: Is the 11-action gap a planning failure or a harness artifact?

The planner (L_plan_c2) is provably complete: exhaustive
iterative-deepening lexicographic search over the 7-symbol primitive
alphabet to maxd=12. It cannot "fail to plan" in the algorithmic sense;
given sufficient CPU it must return the shortest valid plan or prove
none exists within maxd. The wave-3 world model is correct
(S2_VERIFY_RESULT 3, single survivor hyp82, byte-identical across two
independent builds). A length-11 plan exists by design (prereg section
5.1) and was independently reconstructed by this worker
([SX,SJ,SK,W,SX,W,SX,W,SX,W,SX], valid under the v5-tightened
soundness check). The observed incompleteness is therefore a
COMPUTE-TIME artifact: the binary received 12-18% CPU on a 2-core VM
with 5+ competing heavy processes (other lanes' scaling binaries,
which were not disturbed), plus a mid-run VM reboot. It is NOT a
horizon artifact either: maxd=12 exceeds the length-11 solution, so
the solution lies within the disclosed horizon.

### RT2: Does the failure mode match a genuine planning deficit?

Genuine planning-deficit signatures would be: convergence to wrong
laws, a planner bug that misses existing plans, or a found plan that
fails for real. Observed: correct convergence in all three waves
(1/2/3), a correct exhaustive planner, and an incomplete search.
The failure mode (wall-clock timeout under contention) does not match
a planning deficit.

### RT3: Is exhaustive search itself an intelligence limitation?

Yes, and worth recording: the learner brute-forces up to 2e9
candidates instead of exploiting structural insight (e.g., extending
the wave-1/wave-2 pulse-train pattern, which a more intelligent
planner would generalize). This is a legitimate intelligence critique
of the mechanism, but it is out of scope for the frozen K6 bars: the
prereg explicitly discloses "The Regime-3 plan needs an 11-action
exhaustive search; wall-clock cost is reported, not hidden." It does
not constitute a bar failure.

### RT4: Soundness of the v5 tightening

The v5 soundness tightening (3-consecutive-goal-step window at exactly
[nwait,nwait+2]) is SUFFIX-sound: it matches the real observation
times. The independently reconstructed length-11 plan satisfies it.
No evidence the tightening renders the problem unsatisfiable.

### RT5: Tuning / world-learner collusion

Sealed worlds hash-verified against the prereg freeze record (all
three match). NC3 (pristine v5-base must PROGRAM_FAIL on SHIFT2)
guards against a world tuned for v6; it passed in 0521pdt. The
learner contains no shift-specific content (source audit in
IMPLEMENTATION.md: no S2_* references, w_* interface only). The
double-shift structure defeats the one-revision v5 mechanism
structurally, not by a depth gap.

### RT6: Determinism status

Waves 1-2 and wave-3 convergence are byte-identical across two
independent builds (pre-reboot and post-reboot binaries, sha256-identical).
This is strong evidence for K6-R7, but the bar requires 3/3 complete
runs cmp-verified, which is pending run completion.

## VERDICT: PARTIAL

BUILD-PASS requires all eight frozen bars (K6-R1..R8). Status:

- K6-R1 (passive ambiguity): PASS (NHYP 54/216/216, all >= 2).
- K6-R2 (construction, not enumeration): PASS (source audit clean).
- K6-R3 (sequential justification): PASS (ledger complete, contradictions logged).
- K6-R4 (convergence + two revisions): UNMEASURED (conv 1/2/3 and 2 revisions confirmed; wave-3 goal achievement pending planning completion).
- K6-R5 (model to goal): UNMEASURED (wave-3 execution pending).
- K6-R6 (observation economy): PARTIAL (waves 1-2 within budget; wave-3 pending).
- K6-R7 (determinism and purity): UNMET (3/3 complete runs not finished; strong partial evidence: waves byte-identical across two independent builds).
- K6-R8 (no regression): INHERITED PASS (binary sha256-identical to 0521pdt build; 0521pdt regression PASS).

The v6 evidence-driven revision loop is validated as far as the runs
progressed: two revisions triggered by logged prediction-vs-observation
contradictions, re-convergence under each new regime (1/2/3), no
spurious revision, no fixed-point stop. The 11-action planning gap is
a COMPUTE-TIME artifact (exhaustive search under 12-18% CPU share plus
a mid-run VM reboot), not a planning failure: the planner is provably
complete, the wave-3 model is correct, and a valid length-11 plan
exists by construction. This matches and strengthens the 0521pdt
PARTIAL verdict.

Commit IDs (lane-f2-20261002-1121pdt, pathspec-limited to lane dir):
- f256d1128: NAMECHECK Step 0 (safebin guard PASS, seal discipline, provenance) + lane build.sh.
- 20b44ea24: REPORT skeleton.
- aa6eb51e2: VM reboot incident record, binary rebuilt byte-identical, run 1 restarted.
- c09d89907: red-team analysis (RT1-RT6).
- (this commit): full REPORT with VERDICT.

Queued next for the parent:
1. Complete run 1 (in progress, PID 2183) to measure K6-R4/R5.
2. Runs 2-3 for K6-R7 (3/3 byte-identical).
3. Consider: the 11-action exhaustive planning is the bottleneck. A future mechanism could prune via structural generalization (e.g., extend the wave-1/wave-2 pulse-train pattern) rather than brute force. Out of scope for v6 (frozen), but noted as intelligence limitation (RT3).
