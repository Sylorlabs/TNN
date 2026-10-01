# Timeline Estimate: CORE-FREEZE-TNN2 Evaluator Completion

**Estimated:** 2026-10-01 07:01 UTC
**Basis:** live mtime evidence from `core_freeze_tnn2_eval/runs/` plus the blocker doc (commit `008e08ab8`) and prereg audit (commit `8959a7c14`).
**Status of evaluator at estimate time:** alive, mid-execution of FW run 3 (FW9b partial output, 466 of 1248 final bytes).

## Observed FW battery pace (measured, not guessed)

| Run | Start | FW1-FW8 done | FW9a done | FW9b done | Total |
|---|---|---|---|---|---|
| run1 | 05:00:36 | 05:00:43 (~7 s) | 05:17:06 (~16.4 min) | 05:44:34 (~27.5 min) | ~44 min |
| run2 | 05:44:39 | 05:44:45 (~6 s) | 06:01:03 (~16.3 min) | 06:29:14 (~28.2 min) | ~44.6 min |
| run3 | 06:31:17 | 06:31:23 (~6 s) | 06:54:46 (~23.4 min) | in progress | - |

FW1-FW8 consistently take under 10 seconds. FW9a/FW9b are the entire long pole (~44 of 44 minutes). Run3 FW9a was slower than runs 1-2 (23.4 vs ~16.3 min), consistent with machine load from concurrent workers.

## Phase estimates

### 1. Finish FW run 3 (FW9b) + determinism check + FW report edits + post-eval hashes

- FW9b remaining: runs 1-2 took ~28 min from FW9a completion; run3 FW9b started ~06:54:46. Allowing for the observed run3 slowdown: done **07:20-07:35 UTC**.
- K-FZ2-4 determinism (Step 2): 3-way byte-identical `cmp` across runs is seconds of compute; recording evidence in the report: **15-30 min**.
- Arithmetic correction + verdict downgrade (Steps 1, 6): minutes of editing: **10-15 min**.
- Post-eval hash verification (Step 5): `sha256sum` on 4 frozen artifacts is seconds; recording: **5-10 min**.
- Phase 1 complete: **~07:50-08:20 UTC**.

### 2. W1-W9 supplementary battery, 3 runs (Step 3)

- The W worlds are the old TNN-1 freeze worlds (`core_freeze/worlds_prefreeze/`, `core_freeze/worlds_adversary/`). All world files are small (60-2428 bytes), comparable to FW1-FW8 files that execute in ~1 s each. No W-side long pole is evidenced anywhere; the ~40 min pole belongs specifically to the new sealed FW9a/FW9b.
- Estimate per W run: **3-7 min** (9 small worlds, responder contract on W6, per-world hash verification). Three runs: **10-20 min** plus scoring.
- Phase 2 complete: **~08:05-08:40 UTC**.

### 3. Per-cluster analysis (Step 4)

- Report writing, not compute: 5 TNN-1 failure clusters assessed against FW + W results. Bracketed from this session's observed report-writing pace: **30-60 min**.
- Phase 3 complete: **~08:35-09:40 UTC**.

### 4. Final reconciled report commit

- `git add` + commit of the evaluator directory (~330 files, 4.3 MB): **5-10 min**.

## Total

**Reconciled report committed: ~08:40-09:50 UTC (01:40-02:50 PDT), i.e., roughly 1.5 to 3 hours from 07:01 UTC.**

Central estimate: **~09:00 UTC**.

## What could move the estimate

- Earlier: FW9b finishes on the fast side of runs 1-2; W battery runs clean with no responder-contract hiccups; per-cluster analysis is concise.
- Later: continued machine-load slowdown (run3 FW9a was 43 percent slower than runs 1-2); the evaluator discovers a scoring discrepancy needing investigation; W6 responder contract needs re-runs; the evaluator writes a long per-cluster analysis.
- The machinery is sound (pure-Zag scorers, verified seal, verified pre-eval hashes), so the risk is pace, not rework. The one genuine unknown is W-world runtime, but small file sizes and the FW1-FW8 precedent bound it tightly.

## Gating note

Bundle v16 creation stays gated on this report (bundle gate item 1, commit `dcf8ae371`). The three other pending worker dirs (`tnn2_boundary/` now committed as `8d763d766`; `tnn2_transfer/`; `h2_trapworlds/` now committed as `86389b108`) are independent of this timeline.
