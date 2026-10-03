# M2W2R_RUN_LOG.md: M2-W2 fresh-state re-run under frozen amendment (wave-20261001-2021pdt, lane BATTERY)

Date: 2026-10-02. Worker: BATTERY-M2W2RERUN. Implements frozen amendment
AMENDMENT_M2W2.md (c3a753abe) section 3 only. No em-dashes in this file.

## 0. Governance evidence

- Safebin: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
  Pinned znc resolves from safebin. `which python3` prints NOTHING
  (exit 1); `which python` prints NOTHING (exit 1).
- Pure Zag only: no new Zag code authored or compiled; all tools are the
  frozen prebuilt binaries; shell used only for transport, byte checks,
  and hash manifests. No forbidden executable invoked.
- Commit-order self-check: amendment c3a753abe committed alone at
  2026-10-02 04:06:35 UTC, touching only AMENDMENT_M2W2.md and
  NAMECHECK_M2W2FIX.md. Prereg freeze d43fe32c5 precedes it. All M2W2R_
  files are untracked new files with filesystem mtimes 04:08:55 UTC and
  later (NAMECHECK_M2W2RERUN.md 04:08:55, run artifacts 04:09:07+), so the
  amendment commit strictly precedes every re-run artifact. UNVERIFIABLE
  ORDERING does not apply.
- World file unchanged: `m2w2v2_world.txt` hashes to
  `6ccc1d242e2e0b66f75cea559c4e6fc408b93eee6fef56f62e960c5d44b7e3f6`,
  matching WORLD_MANIFEST_V2.sha256 exactly.
- Frozen binaries: `freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  before and after the re-run; `tnn2.zag` hashes to
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`;
  `git status` shows zero modifications under the frozen cognition
  paths. Shim exit code 0 on every invocation.

## 1. Protocol execution (frozen amendment section 3)

For R in 1, 2, 3:

- Step 1 (fresh state A): `./run_m2w1.sh R m2w1v2_envelope_runR.txt
  M2W2R_w1_world_R.txt M2W2R_w1_trans_R.txt M2W2R_w1_log_R.txt
  M2W2R_stateA_R.bin` (template plus envelope_r, driver log saved,
  exactly as in the v2 validation; 49 steps each run). State A persists.
- Step 2 (fresh state B): `rm -f M2W2R_stateB_R.bin`;
  `freeze_shim2_bin m2w2v2_world.txt M2W2R_stateB_R.bin >
  M2W2R_w2_trans_R.txt` (exit 0). State B never chained from state A.
- Step 3 (continue state A): `freeze_shim2_bin m2w3v2_world.txt
  M2W2R_stateA_R.bin > M2W2R_w3_trans_R.txt` (persistent chain W1 -> W3).

## 2. Measurements

N (fresh-state baseline ACT, CHOICE[0] of the step-2 transcript): **0**.
Guide-free by construction: fresh state B, baseline ACT occurs after a
hit with no guide in state, before the first miss of the run.

Transcript CHOICE sequence (all 3 runs): 0, 30, 30.

- N = 0 (baseline, measured)
- pre-resolution ACT = 30 (guide-driven)
- post-resolution ACT = 30 (stale guide action)

M (learner's miss response, first inquiry-phase miss in state-A M2-W1):
**-2** (ANSWER 45111 45600 -2, verified in M2W2R_w1_trans_1.txt).

## 3. Determinism

- Step 2 (fresh-state M2-W2), 3 executions: transcripts byte-identical.
  sha256: `71e9af3d2a279a6c0670b712b1e8f9628af6355615d1489b518132527e624b0a`
  for M2W2R_w2_trans_1/2/3.txt. PASS (amended K-S2v2 extension).
- Step 1: M2-W1 run-1 re-executed immediately with its envelope; transcript
  and driver log byte-identical to the recorded run (cmp clean). PASS
  (v2 per-run reproducibility rule).
- Step 3 (fixed W3 on W1 -> W3 chain): transcripts byte-identical across
  runs. sha256: `6efa79f5588ba6eb6d2d58ba736d14fb2eeb7ad7606eaeeee6897a1cb236006a`
  for M2W2R_w3_trans_1/2/3.txt. PASS.
- State files: M2W2R_stateB_R.bin identical across runs
  (4b07f739f5dcb89e1932ced33689c26d83c1a142394f4a30500f3d1bfd36aac4);
  M2W2R_stateA_R.bin identical across runs
  (5b02eddd4df5ed51b93f50925b53b54ec94a28b84ce26685aeeeb2ccb6b90ebf),
  confirming state B independence and state A reproducibility.

## 4. Calibration gates (fresh-state configuration, BEFORE any mechanism verdict)

Controls run once per policy (deterministic programs) on m2w2v2_world.txt,
scored with `v2_sealed_score_bin ... BAR=M2W2`:

| Control | CHOICEs | N | validity (pre != N) | Bar | Gate | Result |
|---------|---------|---|---------------------|-----|------|--------|
| D1 constant 77 | 77 77 77 | 77 | FAIL WORLD-INVALID | FAIL | must not pass | HOLD |
| D2 stale-action | 0 30 30 | 0 | PASS | FAIL | must FAIL | HOLD |
| C miss/hit | 0 30 0 | 0 | PASS | PASS | must PASS | HOLD |

All gates hold. The amended M2-W2 is NOT void as a battery defect.
Transcripts: M2W2R_ctl_D1_trans.txt, M2W2R_ctl_D2_trans.txt,
M2W2R_ctl_C_trans.txt.

## 5. Amended K-S9v2 verdict (frozen mechanisms, fresh state)

Scored with `v2_sealed_score_bin m2w2v2_world.txt M2W2R_w2_trans_R.txt
BAR=M2W2`, all 3 runs identical:

- NULL_ACTION 0, PRERES_ACTION 30, POSTRES_ACTION 30
- Validity: pre (30) != N (0): PASS. The world is engaged; not WORLD-INVALID.
- Bar: post (30) == N (0)? No. **K-S9v2 FAIL.**
- The FAIL matches the amendment's predicted signature exactly
  (N=0, pre=30, post=30 stale). This corroborates the v1 M2 kill (constant
  inquiry action, no uncertainty-resolution transition) through a
  calibrated bar.
- Unexpected-PASS rule: not triggered. The mechanism did not pass; no
  battery-defect void, no reopened v1 evidence beyond what section 7 of
  the prereg specifies.

## 6. Collateral-probe restatements (applied exactly as specified)

- M2-W2's two collateral probes (QUERY 45101 45600 45201,
  QUERY 45102 45600 45202): both returned -2 on fresh state B, equal to
  the mechanism's miss response M. Engagement probes: PASS as engagement.
  Retention claim WITHDRAWN.
- M2-W3's 44111 collateral (QUERY 44111 44601 44901 on the W1 -> W3
  chain): returned -2, equal to M. Engagement probe only; retention
  claim WITHDRAWN (W2's teaches never occurred on this chain).
- M2-W3's 45103 collateral: hit, PASS (from state A).
- K-S14v2 denominator stays 12; the four restated probes are scored as
  engagement, granting no PASS anywhere.

## 7. M2-W3 under carried N (step 4 of the amendment)

Scored with `v2_sealed_score_bin m2w3v2_world.txt M2W2R_w3_trans_R.txt
"BAR=M2W3:M=-2:N=0"`, all 3 runs identical:

- EPISODE_ACTIONS 30 30 30; distinct=0, nonnull=1 (each differs from N=0)
- Validity: 3x M=-2: PASS
- **K-S10v2 FAIL** (constant action three times). Same verdict as the
  validation run; the contaminated in-chain N=30 is replaced by the
  measured N=0, and the bar still fails on non-distinctness.

## 8. Overall battery validation status

The v2 validation recorded 8/9 worlds validated with M2-W2 WORLD-INVALID
as a prereg design defect. This amended re-run executes exactly the
amendment's fresh-state protocol:

- K-S9v2 amended: FAIL with the predicted stale-guide signature,
  validity holds, all calibration gates hold, 3/3 determinism.
- No battery-defect void on M2-W2 under the amended design.
- Result: **9/9 validated** (expected outcome achieved).

The v1 M2 kills stand, corroborated: K-S8v2 FAIL (unchanged from v2
validation), amended K-S9v2 FAIL, K-S10v2 FAIL with N carried from the
fresh-state baseline.

## 9. Artifact manifest (all in this lane directory)

- NAMECHECK_M2W2RERUN.md (this re-run's Step 0)
- M2W2R_RUN_LOG.md (this file)
- M2W2R_w1_world_R.txt, M2W2R_w1_trans_R.txt, M2W2R_w1_log_R.txt (R=1..3)
- M2W2R_stateA_R.bin (post-W1 persistent state), M2W2R_stateB_R.bin
  (fresh-state M2-W2 state)
- M2W2R_w2_trans_R.txt (fresh-state M2-W2 transcripts, byte-identical)
- M2W2R_w3_trans_R.txt (W1 -> W3 chain transcripts, byte-identical)
- M2W2R_ctl_D1_trans.txt, M2W2R_ctl_D2_trans.txt, M2W2R_ctl_C_trans.txt
  (calibration control transcripts)

No existing lane file was modified. No commits were made by this worker.
