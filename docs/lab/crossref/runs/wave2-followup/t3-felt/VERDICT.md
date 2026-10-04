# T3-FELT re-trial — VERDICT (replacement run)

**Date:** 2026-09-24 (resume worker; predecessor errored at 17:24 UTC during a daemon restart drain)
**Prereg:** `newrun/PREREG_FELT_NEW.md` (349 lines; sha256 `7b7d30183415b86892726ba4c2688c813cce8195d30b11c62d6fca7fa564696c`)
**Design source:** `newrun/PREREG_RETRIAL.orig.md` (409 lines; sha256 `71a0fa49c566c4ab5f90612980c974f37066613e70268aca68dc128ed5e55ec6`), the 2026-09-20 candidate text with the old-SHA pointers neutralized.
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` (verified before use).
**Workspace:** `~/workspace/scratch-crossref/T3/T3-FELT/newrun/` — scratch only. No commits, no pushes.

## ⚠️ ADOPTION STATUS: PROVISIONAL — PENDING MICAH'S SIGNATURE

This preregistration is a **draft**. Its adoption is **provisional and unsigned**. It must not be presented, committed, or treated as an adopted preregistration until Micah signs it. The old (2026-09-20, unauthorized) result remains **quarantined as provenance** — it is evidence of what the unauthorized run produced, not a verdict, and the old committed result must not serve as the replacement verdict.

## Verdict

**The replacement battery is COMPLETE and CLEAN: all cells ran, all paired runs byte-identical, all integrity/anti-inflation bars hold.** Substantive outcome (from the recorded result documents, spot-verified against raw outputs):

- **F-INT-1 (thermometer): UNEVALUABLE as written** — the known prereg defect D1: the proven-negative class (junk, imp=0 non-implant) receives zero observations under the frozen curriculum, so `AUC_proven` has denominator 0 in every cell. Applied exactly as written: the bar does not fire (no value < 0.65 exists). Reported UNEVALUABLE with the defect attached for Micah's ruling (amend the negative class or the bar).
- **F-INT-2 (retention): HOLD as written, with the D2 qualifier** — `R_vup(F-H1) = 100% ≥ 90%` in all variants, and `R_vup(F-H1) ≥ R_vup(N-H1) − 15pp`. But the H1 age gate + graded effort gate mechanically produce ~31% `REFUSED_FULL`, so the substantive retention figure `ER_vup` (held/offered, refusals in denominator per G4) is ≈ 14.6% (v2) / 14.0–18.0% across variants. `ER_vup` is reported alongside for Micah's ruling on whether F-INT-2 stands as written or applies to `ER_vup`.
- **F-INT-3 (revision): HOLD** — `R_wbs(F-H1) = 100%` in all variants.
- **F-INT-4 (decides): HOLD** — D chose H1 in all 3 variants (never H5); `R_vup(D)` numerically identical to `R_vup(X)` in every variant.
- **F-INT-5 (coupling): HOLD** — Phase C: 0 deliberation failures across all variants; R stayed 50 throughout (no R change proposed; predicted-vs-actual vacuous, 0 rollbacks).
- **F-INT-6 (developmental): HOLD** — arm T ran T1/T2/T3; the T2→T3 gate RATIFIED in all 3 variants (`AUC_proven(T2)=1000 ≥ AUC_proven(T1)−50`, zero INVALID in T2). In the develop arm the proven classes are populated (T-phase reads emit observations; `ph_auc_p` denominators nonzero, e.g. 9573264/9573264 in T0 phase 0) and `AUC_proven = 1000ppt` in every phase. `R_vup` = 100% in T1/T2/T3 (no ≥10pp drop). (Contrast with Phase E, where D1 makes `AUC_proven` structurally unevaluable — the two arms' observation patterns differ.)
- **F-INT-7 (cheat): no probe fired** — G1 (D→H5): no; G2 (harness-shopping): D committed exactly 1 harness per run; G3 (R-gaming): no R proposal without thermometer citation; G4 (protection-gaming): refusals counted in `ER_vup` denominator as required; >10% refused-admission flag noted and reported with/without the refused cohort.
- **INVALID-class:** none — no cell's paired runs differ; replay rc=0 everywhere; recompute_bad=0 everywhere; anti-inflation F4a (junk_max ≤ 50), F4b (impl_bad=0), F4c (noev_bad=0) all pass; no RNG tokens in any trial/driver/substrate source (runner-enforced static gate); no R writes during frozen phases (T1 `rparam_frozen` ok); felt constants 12/20/25 present; substrate byte-identical to W7 originals (cmp gate).

**Headline substantive finding:** feeling (intensity reads) was heavily exercised (thousands of `INTENSITY_READ` ledger entries per run, all passing prefix-recomputation) but changed **no outcome** — F and N arms are outcome-identical within each harness; the harness (H1 age-gated triage vs H2–H5) drives all differences. The thermometer is structurally blind by design of the frozen curriculum (D1). This is a clean negative-on-mechanism result with two documented prereg defects (D1, D2) requiring Micah's ruling — **not** a verdict that feeling works.

## Evidence

### Run completeness (post-freeze generation — the prereg-compliant run)

All batteries ran under runner scripts with static gates (W7-source cmp, no-RNG grep, bare-`@import` check, frozen-constant checks) → compile → 2× runs per cell → byte-compare → `FELT_DONE` check → integrity-bar validation. Location: `newrun/work/wave8/felt-retrial/`.

| Arm | Cells | Runs | Status |
|---|---|---|---|
| Phase E | 21 (F-H1..H5, N-H1, N-H5 × 3 variants) | 42 | all `CELL_OK`, integrity bars pass (resume worker re-validated all 21) |
| Develop T | T0–T2 | 6 | `CELL_OK`, `ALL_OK` |
| Develop C (Phase C, H1 harness) | C0–C2 | 6 | `CELL_OK`, `ALL_OK` |
| Decides | D0–D2, X0–X2 | 12 (6 cells × 2) | **complete** — 6/6 `CELL_OK`, all pairs byte-identical, integrity checks pass |

- Phase E: 13/21 cells completed by the predecessor (16:11–17:23 UTC); the remaining 8 (F_H5_1/2, N_H1_0/1/2, N_H5_0/1/2) completed by the resume worker. All 21 `out_*_a.txt` end `FELT_DONE`; all 21 a/b pairs byte-identical.
- The predecessor's phase-E re-run reproduced the earlier generation **byte-identically** (verified on F_H1_0 and extended to all 27 phase_e+develop outputs by the resume worker: `cmp` clean on every pair). Two independent build+run generations, byte-identical.
- Develop and decides runners assert `offered_ri/wr`, `held_ri`, `n_drops`, `junk_max`, `impl_bad`, `noev_bad`, `r_final`, `delib_count`, `delib_fails`, `gate_t12`, `gate_t23`, `rparam_frozen` per cell; all pass.

### The /tmp loss and the decides re-run

The predecessor's decides arm wrote raw outputs to `/tmp` (per `code/decides/DECIDES_RESULTS.md`: "raw outputs in /tmp (d0/d1/d2/x0/x1/x2 _final.txt + reruns)"). `/tmp` is a shared 512MB tmpfs; the files are gone. The results document survives with full decision records and metric tables — and the resume worker has now **re-run the decides arm** under `work/wave8/felt-retrial/decides/` (same sources, same runner gates, outputs retained in-workspace): 6/6 cells `CELL_OK`, all a/b pairs byte-identical, integrity checks pass. The re-run **reproduces the recorded findings exactly**: D chose H1 in all 3 variants × both windows, `n_commits=2` per D run (at the ≤2 anti-shopping limit), `r_vup(D)=r_vup(X)=100` in every variant.

### Prereg chronology (honest record — one defect)

The replacement prereg draft file (`PREREG_FELT_NEW.md`) was written at **16:03 UTC**. An earlier battery generation (`code/phase_e`, `code/develop`, `code/decides` outputs + `*_RESULTS.md` documents) ran at **15:53–15:56 UTC — before the prereg file existed**. That generation's outputs are therefore a **pre-freeze pilot**, not a prereg-compliant run. The workdir generation (16:11 UTC onward) ran **after** the prereg file was written and is the prereg-compliant run. Both generations are byte-identical (27/27 outputs), so the defect has **no material effect on any result**, but the ordering is recorded here undisguised: the "frozen before any compile/run" claim in the prereg header is not literally true of the pilot generation. The frozen sha256 recorded above was taken by the resume worker; no `RUNLOG.md` freeze record existed before this resume.

### Key result documents (predecessor-authored, spot-verified)

- `code/phase_e/PHASE_E_RESULTS.md` — 42-run table; spot-verified (F-H1 v0 metrics match `out_F_H1_0_a.txt` raw `FELT_METRIC` lines).
- `code/decides/DECIDES_RESULTS.md` — decision records per run; raw outputs lost (see above).
- `code/develop/DEVELOP_RESULTS.md` — T/C tables.

## Caveats

1. **Adoption is provisional** — this prereg is a draft pending Micah's signature (stated in §0 of the prereg and here). Nothing here constitutes an adopted preregistration.
2. The old 2026-09-20 run (commits `6a030212…` prereg / `5b1213ea…` results) stays quarantined; the `prereg_commit.json` / `results_commit.json` records describe only those old commits.
3. The decides re-run completed during this resume (6/6 cells, all pairs byte-identical) and reproduced the recorded findings exactly; its completion is recorded in `RUNLOG.md`.
4. This trial does not amend the blocked strength-trial prereg or the W7 felt prereg (both stand untouched), does not test scale legs, and grants no constitutional changes (§14 of the prereg).
