# T3-FELT re-trial — RUNLOG (replacement run)

**Worker:** resume replacement (predecessor errored 2026-09-24 17:24 UTC, daemon restart drain).
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 verified `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` before use.
**Constraints honored:** scratch workspace only (`~/workspace/scratch-crossref/T3/T3-FELT/newrun/`); no RNG; no commits or pushes to `sylorlabs/TNN`; prereg adoption stays draft/provisional (no signature solicited or recorded).

## Inherited state (verified, not blindly trusted)

- `PREREG_RETRIAL.orig.md` (409 lines, mtime 15:50 UTC) — frozen design source; old-SHA pointers neutralized.
- `PREREG_FELT_NEW.md` (349 lines, mtime **16:03 UTC**) — the replacement prereg draft. sha256 `7b7d30183415b86892726ba4c2688c813cce8195d30b11c62d6fca7fa564696c` (recorded by resume worker; no prior freeze record existed).
- `code/{decides,develop,phase_e}/` — predecessor's first battery generation (outputs mtime 15:53–15:56 UTC, i.e. **before** the prereg file existed): 12 decides metric records (raw outputs in /tmp — LOST), 12 develop outputs, 42 phase_e outputs, plus `DECIDES_RESULTS.md`, `DEVELOP_RESULTS.md`, `PHASE_E_RESULTS.md`.
- `work/wave8/felt-retrial/{phase_e,develop,decides}/` — predecessor's second (post-freeze) generation: full sources, runner scripts with static gates, and phase_e 13/21 cells complete (log ends 17:23 UTC, one cell's a-file partial).
- `prereg_commit.json` / `results_commit.json` — describe ONLY the old commits `6a030212284846bb4964dc9fbc57e67bde2704d8` (prereg, blob `9747366c9f0b62c1cf76e9f9efe56ab9126a908c`) and `5b1213eaee441e41751050a50069599792c7c526` (results); not treated as new commits.

## Actions (resume worker)

1. Verified toolchain SHA-256 prefix `498abcb5ab346f8c` (full match recorded above).
2. Verified predecessor's phase_e state: 13 `CELL_OK` in `run_phase_e.log`, 14 `out_*_a.txt` (last one partial, no `FELT_DONE`) → deleted the partial `out_F_H5_1_a.txt`.
3. Compared post-freeze generation vs pilot generation: `cmp` clean on all 27 phase_e+develop output pairs (`code/` vs `work/`); specifically `code/phase_e/out_F_H1_0_a.txt` ≡ `work/wave8/felt-retrial/phase_e/out_F_H1_0_a.txt`.
4. Wrote `work/wave8/felt-retrial/run_resume_all.sh` and launched it in background: remaining 8 phase_e cells → develop T0–T2, C0–C2 → decides D/X × 3 variants.
   - Phase E resume: 8/8 `CELL_OK` (F_H5_1, F_H5_2, N_H1_0, N_H1_1, N_H1_2, N_H5_0, N_H5_1, N_H5_2). Log: `work/wave8/felt-retrial/resume_all.log`.
   - The background session died silently after phase_e+develop completed (session handle lost; no failure lines in log). Decides had only a partial `out_D0_a.txt`.
   - Re-ran the full phase_e integrity-bar validation (curriculum totals, `r_zone_entries=0`, replay rc=0, recompute_bad=0, histogram overflows=0, F4a/b/c) over all 21 workdir cells: **fail=0**.
   - Verified all 21 phase_e a/b pairs byte-identical and all end `FELT_DONE`.
5. Relaunched the decides battery. The first relaunch's wrapper died when its binary was killed during a cleanup (`RUNNER_FAIL,run D0 a` — the wrapper's death rattle, harmless); then ran `run_decides_parallel.sh` (2-way parallel: D0+X0, D1+X1, D2+X2), each cell with a-run, b-run, byte-compare, `FELT_DONE` check, and integrity checks (replay rc=0, recompute_bad=0). **Completed: 6/6 `CELL_OK` + `INTEGRITY_OK`, `DECIDES_PARALLEL_OK`.** All 6 a/b pairs byte-identical; D chose H1 in all 3 variants × both windows (`DEC_CHOSEN,1` / `DEC_CHOSEN2,1`); `n_commits=2` per D run (at the ≤2 anti-shopping limit); `r_vup(D)=r_vup(X)=100` in every variant — reproducing the recorded `DECIDES_RESULTS.md` findings exactly.
6. Static gates observed passing in all three runners: W7-source `cmp` (felt.zag, st_memory_core.zag, substrate), no-RNG `grep`, bare-`@import` checks, frozen constants (12/20/25 corroborate/contradict/trainer-mark), frozen curriculum formulas.
7. Spot-verified `PHASE_E_RESULTS.md` against raw outputs (F-H1 v0 `FELT_METRIC` lines match the recorded table).
8. Confirmed D1 empirically: `out_F_H1_0_a.txt` has `auc_pn_n,0` and `auc_p_den,0` (proven-negative reads = 0, denominator 0) — `AUC_proven` structurally unevaluable in Phase E, exactly as the prereg's known-defect note states.
9. Wrote `VERDICT.md` (sibling). Updated the F-INT-6 bullet after finding the develop arm computes populated `ph_auc_p` (denominators nonzero) with `AUC_proven=1000ppt` in all phases — D1 is Phase-E-specific.

## Prereg chronology defect (recorded, undisguised)

The pilot generation (`code/`, 15:53–15:56 UTC) ran **before** the replacement prereg file was written (16:03 UTC). It is therefore a pre-freeze pilot, not a prereg-compliant run; the `work/` generation (16:11 UTC onward) is the prereg-compliant run. Byte-identity between the generations (27/27) means no result is affected, but the "frozen before any compile/run" header claim is not literally true of the pilot. No `RUNLOG.md` freeze record existed before this resume; the sha256 above is the freeze record.

## Anomalies

- Two transient exec-session issues: one metadata-registration timeout (retried fine) and one background session that vanished mid-decides (recovered by relaunch; log-monitored, not handle-monitored).
- `/tmp` loss: predecessor's decides raw outputs were written to `/tmp` and are unrecoverable (shared 512MB tmpfs). The re-run regenerates them in-workspace.

## Open item

- None. All three batteries are complete and verified. The decides re-run reproduced the recorded `DECIDES_RESULTS.md` findings exactly (D→H1 in all variants, D≡X numerically, 2 commits per D run).
