# REPORT: Learner-Owned Verification of Composition via World Execution (H-LVNAV-1)

**Verdict: LEARNER-VERIFICATION-COMPLETE.**
Agreement vs harness: learner-vs-HV (value key) 3/4 (75%); learner-vs-HT
(trace key) 2/4 (50%). Both divergences preregistered and characterized.

## What was built

A standalone pure-Zag experiment in
docs/lab/research-lead/overnight-20260928/learner_verification/nav_world/
(a subdirectory; the parent learner_verification/ lane holds C181, COMPLETE,
and is untouched). An 8x8 grid navigation world with two variants (OPEN;
LAVA with lava cells at (3,0),(4,0),(5,0)). The learner induces displacement
contracts for three movement MAPs from probe executions (X=(7,0), Y=(0,7),
Xb=(3,0)), composes MAPs by chaining freshly copied node lists into new
persistent structures (H2-style), commits to the composed MAP with a
predicted final cell (status=PENDING logged before any execution), the
driver executes exactly the committed MAP in the world, and the learner
judges the consequence from world state alone (final cell, burned flag)
under the frozen rule PASS iff final==goal AND burned==0 AND
final==predicted. The harness side (driver only) holds two researcher keys:
HV expected final cell 63, HT expected canonical trace. The learner path
never consults either key.

## Kill bars (all frozen in PREREG.md, commit 514e4ef6a)

- K1 (prereg order): PASS. PREREG.md committed alone as 514e4ef6a before any
  .zag file existed; implementation commits follow it in git log order.
- K2 (determinism): PASS. 3/3 byte-identical runs; sha256
  4052759b0b7787be9723aa3193a0c5f6f3627be5aa45b8117f8d55fe59ef4a77 for
  run1/2/3 (cmp clean).
- K3 (boundary audit): PASS. harness-key tokens: 0 in lv_mech.zag, 3 in
  lv_main.zag (driver/harness block only). Direct world-state writes: only
  inside world_reset/world_place/world_step in lv_mech.zag; 0 in the driver.
- K4 (commit before execution): PASS. Transcript line numbers: T1 COMMIT 7
  < EXEC 8 < CONSEQUENCE 9 < LEARNER-VERDICT 10; same ordering for T2
  (14<15<16<17), T3 (21<22<23<24), T4 (28<29<30<31). status=PENDING logged
  at every commit.
- K5 (preregistered verdicts): PASS, exact match.
  T1 (L=PASS, HV=PASS, HT=PASS); T2 (FAIL,FAIL,FAIL);
  T3 (FAIL,PASS,PASS); T4 (PASS,PASS,FAIL); CTRL T3 = PASS.
- K6 (agreement measured and explained): PASS. learner-vs-HV 3/4;
  learner-vs-HT 2/4; both divergences are the preregistered D1/D2; no
  unpreregistered divergence occurred.
- K7 (toolchain): PASS. build.sh guard confirms python3/python absent from
  the safebin PATH; safebin recorded in NAMECHECK.md Step 0; zero forbidden
  invocations.
- K8 (governance): PASS. 0 modes/bridges/handlers (grep 0); paper
  untouched; nothing pushed (local commits only); zero em/en dashes
  (byte-verified); explicit pathspecs on every git add/commit.

## Agreement analysis

| trial | world | compose | learner | HV | HT | agree-HV | agree-HT |
| T1 | OPEN | X;Y | PASS | PASS | PASS | yes | yes |
| T2 | OPEN | Xb;Y | FAIL | FAIL | FAIL | yes | yes |
| T3 | LAVA | X;Y | FAIL | PASS | PASS | NO (D1) | NO (D1) |
| T4 | OPEN | Y;X | PASS | PASS | FAIL | yes | NO (D2) |

- D1 (T3, preregistered): the lava variant. The composed MAP reaches the
  goal cell, so both harness keys pass it, but the agent crossed lava
  (burned=1). Neither key can express the "arrive unburned" constraint, so
  both are blind to the violation. The learner's world-state observation
  catches it and fails the composition. The harness keys under-specify the
  task; learner-owned verification is strictly more informative here.
- D2 (T4, preregistered): the alternative route Y;X reaches the goal cleanly
  (final=63, burned=0), so the learner and the value key pass it, but the
  trace key fails it because the executed cell sequence differs from the
  canonical X;Y path. The trace key over-specifies: it rejects a valid
  alternative derivation. Learner-owned verification accepts any
  goal-reaching legal execution.
- CTRL arm (prediction-only, no world read): T1 PASS, T2 FAIL, T3 PASS
  (spurious), T4 PASS. Without world execution the learner would have
  passed T3, missing the lava violation exactly as the harness keys do.
  World observation is load-bearing for D1.

## Honest limits

- The verdict rule (goal + unburned + prediction-consistent), the world law,
  probe starts, and per-trial composition choice are researcher scaffold,
  labeled as such in the prereg. Learner-owned: the composed structures,
  induced contract values, prediction values, world-state observation, and
  the verdict computed from that observation.
- Chain-family compositions only; one fixed task (reach (7,7)); the LAVA
  world is a single hand-designed variant, not an adversarial battery.
- This lane tests the verification loop, not composition discovery: the
  learner does not choose which MAPs to compose per trial.
- The harness keys compared against are the status-quo style keys (expected
  value, expected trace); the result does not claim all possible harness
  designs would diverge the same way.

## Artifacts

- lv_mech.zag (mechanism), lv_main.zag (driver/harness), lv_full.zag
  (concatenated build input), build.sh, compile.txt
- lv_bin (sha256 2b94bbda180f0a734570be4cd38d5fe81f932edb9eabc491c8adb9dd89347f32)
- run1.txt, run2.txt, run3.txt, sha256sums.txt
- PREREG.md (frozen, commit 514e4ef6a), NAMECHECK.md, REPORT.md (this file)

**Verdict: LEARNER-VERIFICATION-COMPLETE** with agreement 3/4 vs the harness
value key and 2/4 vs the harness trace key; divergences D1 (keys miss the
unburned constraint) and D2 (trace key rejects a valid alternative route)
characterized as preregistered.
