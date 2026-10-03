# JUDGE_BRIEF.md - F1-REPAIR2 S-prime confirmation and repair-time policy

Provenance:
- RENDER_SHA: 466bcee03 (sealed evaluation commit; prereg b4dfa3f32,
  implementation 6bc6483c3, fixtures fed95fc76, all on branch
  tnn-native-lab, local only)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: F1 BUILD-FAIL, F1-FOLLOWUP Part 2 NOT-FOUND,
  F1-BUFFER BUFFER-NOT-PREDICTIVE, F1-REPAIR
  GREEDY-CONFIRMED-with-nuance
- NEW_KNOWLEDGE_CLAIM: The relaxed repair signature S-prime
  (later to-zero burst, any buffer size) is confirmed on 24 fresh
  sealed worlds with zero misclassifications on degenerate-path
  seeds, and the repair-time policy (a later burst completes iff
  its first construct is a feature-doubling that discards the
  degenerate accumulator) meets its frozen bar with its two
  violations, both on non-degenerate seeds, precisely bounding
  its scope.

## Verdict: REPAIR2-CONFIRMED (per the frozen decision rule)

Governing bars (frozen in PREREG_REPAIR2.md, committed alone at
b4dfa3f32 before any probe was built, any fresh fixture was
generated, or any fresh run executed; binary under test is the
frozen F1 impl/f1_learn, sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before runs):

- 24 fresh sealed 7300-series sum2 worlds; 3/3 byte-identical
  reruns on all 48 invocations; zero NOTRIG, zero parse failures.
- Overfit rate 4/24 = 17 percent (seeds 18, 20, 21 at 0/30;
  seed 19 at 3/30; all 20 correct seeds at 30/30). Three of the
  four overfits are degenerate-path seeds; seed 19 is a
  non-degenerate overfit.
- Part A (conditioned on D): D = 7 seeds (2, 6, 14, 18, 20, 21,
  23) >= 6. S'=1 on seeds 2, 6, 14, 23 (all CORRECT); S'=0 on
  seeds 18, 20, 21 (all OVERFIT). misc_D = 0 <= 2: PASS.
  S-prime now holds on 27/27 degenerate-path seeds across
  three series (9/9 5100, 11/11 6100, 7/7 7300).
- Part B (all 24 seeds): POLICY-R mispredicted on 2 seeds
  (11, 19), misc_B = 2 <= 4: PASS. 12/14 fresh later bursts
  satisfy the policy; both violations are on non-degenerate
  seeds and bound the policy's scope (seed 11: clean inherited
  accumulator completes without a doubling; seed 19: a
  doubling-first burst stalls when the post-reset buffer
  favors the degenerate second move).
- K-C0A: PASS (zero semantic markers in new lane code; probes
  are external trace readers; frozen binary unmodified).
- Commit-order self-check: prereg (b4dfa3f32) precedes
  implementation (6bc6483c3), which precedes fixtures
  (fed95fc76), which precede sealed runs and evaluation (this
  commit). No bar moved after freezing.

## What was decided and what was not

Decided: S-prime is confirmed as the repair signature on fresh
worlds; POLICY-R characterizes typical degenerate-path repair
dynamics within its stated boundary. Not decided: no fix is
proposed for the F1 line; POLICY-R is a mechanism
characterization, not a repair patch. Open threads for the next
experiment: the post-doubling second-move competition as a
function of buffer composition, and the non-degenerate
overfit class (seed 19), which the first-trigger-only D
definition does not capture.

## Evidence

All under docs/lab/rsi/runs/wave-20261001-2321pdt/F1-REPAIR2/:
PREREG_REPAIR2.md, SEALED_EVAL_REPAIR2.md,
dev/CALIBRATION_5100_6100_POLICY.md, dev/r2sig.zag,
dev/r2apply.zag (+ compiled binaries), dev/f1_learn,
dev/f1_wgen, dev/f1_score (read-only copies, hash-verified),
sealed5/ (fixtures, gen5.sh, run_repair2.sh,
FIXTURE_SHA256.txt), runs5/ (3 repetitions,
DETERMINISM_SHA256.txt, fresh_table.txt, fresh_scores.txt,
fresh_sigs.txt, verdict.txt).
