# CORE-FREEZE-TNN1 Evaluation: NAMECHECK

Date: 2026-09-30. Worker: CORE-FREEZE-TNN1 Evaluator (subagent).
Task: sealed CORE-FREEZE-TNN1 evaluation per frozen prereg 60f1ff0bf.

## Step 0: Toolchain guard (safebin)

- Ran the mandatory safebin setup: linked 17 tools into $HOME/safebin
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- Exported PATH="$HOME/safebin:$PATH" for all subsequent work.
- Verified: `which python3 python` returns nothing (no output before
  guard-check-done). Forbidden interpreters do not resolve.
- All research computation uses the pinned znc or safebin shell tools.
  No Python, C/C++, JavaScript, or Rust anywhere in this wave.

## Step 1: Prereg and ordering (K-FZ1, K-FZ5)

- Frozen prereg: 60f1ff0bf (CORE-FREEZE-TNN1-PREREG-FROZEN).
- Driver shim: 58d2268e7 (SHIM-BUILD-PASS).
- K1 ordering verified: `git merge-base --is-ancestor 60f1ff0bf HEAD`
  passes (exit 0). Prereg strictly precedes shim, shim precedes
  evaluation. K-FZ1 PASS.

## Step 2: Frozen artifact verification (K-FZ2)

All four hashes verified with sha256sum before any world exposure:

| Artifact | Expected | Observed | Match |
|---|---|---|---|
| TNN-1 source (tnn1_act.zag) | d3895083c9f8b5b0f82ac1c74b11eb2c90341059fcf9e37be30b9c085de0cc6b | d3895083c9f8b5b0f82ac1c74b11eb2c90341059fcf9e37be30b9c085de0cc6b | YES |
| TNN-1 binary (tnn1_act_bin) | efa36ecd0604a8e3f650e0fef715a25c2383f271f20349c6e26a8f91116507a1 | efa36ecd0604a8e3f650e0fef715a25c2383f271f20349c6e26a8f91116507a1 | YES |
| Shim source (freeze_shim.zag) | 167f4fd3ba3febc5e260dc1c84c8cb7b6ae82cad634c64e41b498130609ce8f9 | 167f4fd3ba3febc5e260dc1c84c8cb7b6ae82cad634c64e41b498130609ce8f9 | YES |
| Shim binary (freeze_shim_bin) | 9007e084e93b81cc508f6b5e73200080b70454e84201f0d3e7c3baa4f35c64e0 | 9007e084e93b81cc508f6b5e73200080b70454e84201f0d3e7c3baa4f35c64e0 | YES |

K-FZ2 pre-evaluation: PASS. No F-FZ2 trigger.

## Step 3: Seal integrity (K-FZ5)

- FW1-FW9 sealed assets: freeze_worlds_v2, seal commit 396895595.
- FW world-file sha256 seals verified against SEAL.md before running.
- FW blindness audit: 6f0eae9f2 (PASS, prior).
- Anti-smuggling re-scan: the new TNN-1 source (tnn1_act.zag,
  d3895083...) scanned for FW-range integer tokens [30000,39999]
  and for the W1-W9 id ranges from the original A5 audit. Results
  recorded in FREEZE_REPORT.md.
- Sealed world files are fed to the shim binary mechanically. No
  world contents inspected, tuned to, or exposed in reports.
- K-FZ5: PASS (pending scan results recorded in the report).

## Step 4: Evaluation method (authorized process)

- Same mechanism as the original freeze (run_phase/run_world.sh):
  per-world binary-hash check, sequential execution with persistent
  state carried across worlds, stdout/stderr/rc/timing/statehash
  captured per world.
- Pure-Zag scorer (probe_score.zag) and pure-Zag plan grader
  (grade_plan.zag), built with the pinned znc, committed in this
  directory before any scoring.
- FW6/W6 two-stage responder contracts implemented mechanically
  in shell per the sealed design docs (exact-line matching only).
- Determinism: full battery run 3 times from fresh state;
  per-world stdout compared byte-identical (K-FZ4).

## Standing rules observed

- Owned path only: core_freeze_tnn1_eval/.
- No TNN-1 or shim source edits. No new opcodes.
- No em dashes in loop documentation.
- Contaminated paper untouched (zero-diff verified at commit).
- Explicit git pathspecs for the final commit.

## Step 5: Battery Execution (2026-10-01)
- FW battery: 3 runs, all byte-identical (K-FZ4 PASS)
- W battery: 3 runs, all byte-identical (K-FZ4 PASS)
- FW5-B0: 10/10 from S4 (gate PASS)
- K-FZ2 re-verified post-battery: all hashes intact
- FW SCORE: 4/9. OLD-WORLD REGRESSION: 4/9.
- Verdict: FREEZE-EVAL-COMPLETE
