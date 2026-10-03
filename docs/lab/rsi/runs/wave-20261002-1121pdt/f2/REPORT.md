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

(to be filled)

## K6-R4 adjudication (mechanical, from logs)

(to be filled)

## Negative controls

(to be filled)

## Regression (K6-R8)

(to be filled)

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

## VERDICT

(to be filled)
