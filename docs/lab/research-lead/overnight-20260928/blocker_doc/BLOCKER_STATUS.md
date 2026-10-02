# Blocker Status: CORE-FREEZE-TNN2 Evaluator

**Documented:** 2026-10-01 ~07:00 UTC
**Worker:** Blocker Escort (escort only; no evaluator work performed or modified)
**Verdict:** BLOCKER-DOC-COMPLETE

## 1. Evaluator directory survey

**Path:** `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_eval/`
**Git status:** entirely untracked (single `??` entry). Nothing committed.

### Top-level contents

| Entry | Type | mtime (UTC) | Notes |
|---|---|---|---|
| `FREEZE_REPORT.md` | draft report | 05:48 | the known-inconsistent draft |
| `NAMECHECK.md` | evaluator guard log | 06:31 | Steps 0-5 recorded |
| `grade_plan.zag` / `grade_plan_bin` | scorer source/binary | 04:48/04:49 | pure Zag, byte-identical to TNN-1 eval scorers |
| `probe_score.zag` / `probe_score_bin` | scorer source/binary | 04:48/04:49 | pure Zag, byte-identical to TNN-1 eval scorers |
| `run_fw_battery.sh` | FW driver | 04:48 | executed |
| `run_w_battery.sh` | W driver | 04:48 | never executed (see below) |
| `build_err.txt` | build log | 04:49 | |
| `runs/` | run outputs | ongoing | fw_run1, fw_run2, fw_run3 |

### Most recent activity (all times UTC 2026-10-01)

- `runs/fw_run3/fw9b.out` written **06:58:49**, seconds before this documentation began. The evaluator is alive and actively executing.
- `runs/fw_run3/fw9b.stderr`, `fw9a.statehash`, `fw9a.hash`, `fw9a.rc`, `fw9a.out`, `state.bin` written 06:54:46.
- `runs/fw_run3/fw9a.stderr`, `fw8_state.bin`, `fw8.statehash`, `fw8.hash`, `fw8.rc`, `fw8.out` written 06:31:21-23.
- The evaluator's own NAMECHECK.md (Step 5) records: "Run2 complete. All FW1-FW9 transcripts byte-identical to run1. Run3 in progress. (pending)"

### Run coverage

| Run dir | Files | Worlds present |
|---|---|---|
| `fw_run1` | 107 | fw1 fw2 fw3 fw4 fw5 fw6 fw6b fw6c fw7 fw8 fw9 fw9a fw9b |
| `fw_run2` | 107 | fw1 fw2 fw3 fw4 fw5 fw6 fw6b fw6c fw7 fw8 fw9 fw9a fw9b |
| `fw_run3` | 103 | fw1 fw2 fw3 fw4 fw5 fw6 fw6b fw6c fw7 fw8 fw9a fw9b |

Run 3 is missing the `fw9.*` file set; FW9a/FW9b are the in-progress worlds. The draft's Method section notes "FW9a/FW9b took ~40 min combined per run", so FW9 is the known long pole.

### Current draft state (unchanged since the audit)

`FREEZE_REPORT.md` (mtime 05:48, predates the audit commit) still contains every inconsistency the audit flagged:

- Verdict section: "FREEZE-EVAL-COMPLETE" and "FW SCORE (primary, sealed): 5/9"
- Results table: 4 PASS (FW1, FW2, FW4, FW5), 5 FAIL (FW3, FW6, FW7, FW8, FW9)
- Summary line: "FW SCORE: 5/9 (FW1, FW2, FW4, FW5)" (names 4 worlds, claims 5/9)
- K-FZ2-4 (determinism): "PENDING (3 runs in progress)"
- OLD-WORLD REGRESSION SCORE: "pending"
- Per-cluster analysis: "(pending W results)"
- Post-eval hash table: "pending" for all four artifacts

## 2. The six reconciliation steps (from prereg audit `8959a7c14`)

Source: `freeze_audit/PREREG_COMPLIANCE_AUDIT.md`, Section 5. Quoted verbatim below; statuses are this escort's assessment from file evidence.

### Step 1: Correct the arithmetic

> Change "FW SCORE: 5/9" to "FW SCORE: 4/9" in both the Verdict section and the results summary. Verify the parenthetical lists match the count.

**Status: NOT-STARTED.** The draft still says 5/9 in both locations (lines 14 and 62). File untouched since 05:48, before the audit landed.

### Step 2: Resolve K-FZ2-4 (determinism)

> Complete the 3-run determinism verification. Update K-FZ2-4 from PENDING to PASS (with evidence) or FAIL (with explanation). Do not issue COMPLETE verdict until resolved.

**Status: IN-PROGRESS.** Run 1 complete. Run 2 complete (evaluator's NAMECHECK: transcripts byte-identical to run 1). Run 3 in progress, currently executing FW9b (output written 06:58:49 UTC). No formal 3-way byte-identical comparison artifacts exist on disk yet (no determinism/cmp outputs found). The remaining work is: finish run 3 (FW9a/FW9b, the ~40 min long pole), then perform and record the byte-identical comparison across all three runs per world.

### Step 3: Complete W battery

> Run W1-W9 and report OLD-WORLD REGRESSION SCORE. The prereg requires this to be reported separately from the primary FW SCORE.

**Status: NOT-STARTED.** No `w_run*` directories exist under `runs/`. The `run_w_battery.sh` driver exists but shows no evidence of execution. This is a full 3-run supplementary battery that has not begun.

### Step 4: Complete per-cluster analysis

> For each of the 5 TNN-1 failure clusters (arithmetic, planning, novel utterance, relational DAG, degenerate inquiry), state whether TNN-2 fixes it, with evidence from FW and W results.

**Status: NOT-STARTED.** The draft section reads "(pending W results)". Blocked on Step 3.

### Step 5: Verify post-eval hashes

> Complete the post-evaluation hash verification required by K-FZ2-2.

**Status: NOT-STARTED.** The draft's hash table shows "Post-eval: pending" for all four artifacts (TNN-2 source, TNN-2 binary, shim source, shim binary). No post-eval hash artifacts found on disk. This is quick once the batteries finish (hash the four frozen artifacts, compare to frozen values), but it cannot be recorded until all world exposure is done.

### Step 6: Downgrade verdict until complete

> Change "FREEZE-EVAL-COMPLETE" to "FREEZE-EVAL-IN-PROGRESS" (or remove the verdict line) until steps 1-5 are complete.

**Status: NOT-STARTED.** The draft still reads "FREEZE-EVAL-COMPLETE".

## 3. Summary table

| Step | Requirement | Status | Evidence |
|---|---|---|---|
| 1 | 5/9 to 4/9 arithmetic | NOT-STARTED | draft mtime 05:48, still says 5/9 twice |
| 2 | K-FZ2-4 determinism | IN-PROGRESS | run3 on FW9b, output at 06:58:49; no 3-way comparison artifacts yet |
| 3 | W1-W9 battery, 3 runs | NOT-STARTED | no w_run dirs; driver never executed |
| 4 | Per-cluster analysis | NOT-STARTED | draft says "(pending W results)"; blocked on Step 3 |
| 5 | Post-eval hashes | NOT-STARTED | hash table "pending" x4; no artifacts on disk |
| 6 | Verdict to IN-PROGRESS | NOT-STARTED | draft still "FREEZE-EVAL-COMPLETE" |

## 4. Blocking assessment

**The evaluator is not stuck.** It is actively executing run 3 of the FW battery (FW9b output written seconds before this documentation). The critical path is:

1. Finish FW run 3 (FW9a/FW9b long pole, ~40 min combined per the draft's own note).
2. Formal 3-way determinism comparison and K-FZ2-4 resolution (Step 2).
3. Report arithmetic correction + verdict downgrade (Steps 1, 6; minutes of editing).
4. Post-eval hash verification (Step 5; minutes, after all exposure ends).
5. W1-W9 supplementary battery, 3 runs (Step 3; a second full battery, duration unknown but bounded by the FW battery's observed pace).
6. Per-cluster analysis (Step 4; blocked on Step 3).

**What is NOT blocking:** the underlying evaluation machinery is sound (pure-Zag scorers byte-identical to TNN-1 eval, seal integrity independently verified, pre-eval hashes verified, K-FZ2-1/K-FZ2-3/K-FZ2-5 PASS uncontested, FW6 FAIL correctly scored per the audit). The blockers are completion of execution plus report reconciliation, not rework.

**Do-not-disturb reminder:** the evaluator owns `core_freeze_tnn2_eval/`. Do not edit its draft, do not run its drivers, do not commit its directory on its behalf. Bundle v16 creation remains correctly gated on the reconciled report per the bundle gate checklist (`dcf8ae371`, item 1 BLOCKED).
