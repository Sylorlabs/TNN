# Sweep log — worker_20 (chunk_20)

- **Date:** 2026-09-22
- **Input:** `GROK47_OVERNIGHT/sweep_day/chunks/chunk_20.tsv` (50 data rows)
- **Output:** `fragments/worker_20.tsv` (all 50 rows, `status=done`)
- **Scope:** `wave8/felt-retrial/*` (19 rows), `wave8/rc2/*` (8 rows), `wave9/integration/*` (23 rows)

## Duplicate map (repo-wide by SHA-256)

| File in chunk (×3 each) | Canonical |
|---|---|
| `felt-retrial/{decides,develop,phase_e}/felt.zag` | `wave7/felt-intensity/felt.zag` |
| `felt-retrial/{decides,develop,phase_e}/substrate/R33_NATIVE_IO_V1.zag` | `toolchain/R33_NATIVE_IO_V1.zag` |
| `felt-retrial/{decides,develop,phase_e}/substrate/R33_NATIVE_SHA256_V2.zag` | `toolchain/R33_NATIVE_SHA256_V2.zag` |
| `felt-retrial/{decides,develop,phase_e}/substrate/cl/common.zag` | `toolchain/R33_CONTINUING_LIFE_V1/common.zag` |

The 12 duplicate rows inherit the canonical inspection. All byte-identical (SHA-256).

## Per-file notes

### wave8/felt-retrial

- `decides/decides_trial.zag` — PASS. Spot-compiled cleanly with the pinned znc
  (`znc_linux_x86_64_abed8aa1`); no `as []i32/u32/u16` casts, no `slice as *u8`,
  zero RNG-like tokens in comment-stripped code. Noteworthy: line 1214 carries the
  exact candidate ZNC-004 pattern (`let tjn2:[]u8=w.traj_n;`, annotated slice-let
  off a local struct value) and the build SUCCEEDED on this toolchain — the
  documented failure appears type- or build-context-specific, not universal.
- `develop/develop.zag` — PASS. No forbidden casts, no RNG-like tokens
  (comment-stripped). The only chained-dot grep hit was a comment line; `&`-local
  uses are the normal `st_add`/`st_snap` out-param idiom; `w.*.field` derefs go
  through pointer params (not `&local`), so ZNC-010 does not apply.
- `phase_e/felt_phase_e.zag` — PASS. Same clean scan.
- `decides/felt.zag` (canonical reviewed) — PASS. Pure function of audited
  observation counts; reads nothing from strength/judgments; no RNG, no casts.
- `develop/DEVELOP_RESULTS.md` — review. Deterministic gates hold, but R never
  changed and the G3 path never triggered, so the feeling was NOT stress-tested
  by an actual R change; perfect AUC admitted as constructionally easy.
- `phase_e/PHASE_E_RESULTS.md` — review. 42 cells, paired-deterministic; F-INT-1
  UNEVALUABLE (zero proven-negative reads — prereg defect, needs Micah's ruling);
  F-INT-2 holds as written but is VACUOUS (mass REFUSED_FULL collapses the
  denominator; ER_vup ≈ 14.6% median). F and N arms outcome-identical under every
  harness; the harness, not the feeling, drives all outcome differences.
- `phase_e/analyze_phase_e.py` — review. The generator of PHASE_E_RESULTS.md.
  Its header string wrongly claimed "54 runs" (real count 42 = 7 arms × 3 × 2;
  the prereg's 54 counts D/X arms outside this scope). Its module-level code
  asserts paired a==b byte-identity for all 21 cells and completed without
  assertion errors — that assertion passing is itself evidence of paired
  determinism. See **worker incident** below for a side-effect and its repair.

### wave8/rc2

- `RC2_RESULTS.md` — PASS. 40/40 PASS, paired byte-identical reruns, zero RNG,
  capacity-equivalence evidence present; claims verified against evidence dirs.
- `il_core_rc2.zag` — PASS. Exact diff against `wave4/integrity-ledger/il_core.zag`
  shows ONLY the documented IL_CAP 128→1024 change with the Micah-approved
  2026-09-20 amendment citation. Packed `[]u8`, explicitly initialized memory.
- `rc2_trial.zag` — PASS. Spot-compiled cleanly; RC_SMAX=1500, defect constants
  parameterized, expected S_b=370; no known znc hazard.
- `rc2_mini.zag` — review. Not standalone-evaluable: it imports the
  runner-generated `il_core_mini.zag`, which exists only while `run_equiv.sh`
  runs (committed equivalence evidence shows both cap builds compiled and
  passed). This is a build-context constraint, not a defect.
- `AMENDMENT_IL_CAP_PROPOSED.md` — review. Internal stale contradiction: top
  quote says approved/frozen by Micah and folded into the prereg; title/body
  repeatedly say "PROPOSED, NOT APPROVED."
- `PREREG_RC2_DRAFT.md` — review. Filename historical; top amendment
  approves/freezes it, including the IL_CAP leg sizing.
- `COUNCIL_VERDICT.md` — PASS (pre-run advisory council; consistent with the
  later approved amendment and outcomes). `SURVEY_NOTES.md` — PASS (pre-run
  implementation survey; historical).

### wave9/integration

Outcome-sequence chain (verified against each other): `RESULTS_S10.md` BLOCKED
→ battery repaired → `RESULTS_S10_REPAIR.md` (superseded) → C5 redesign
`RESULTS_S10_C5REDESIGN.md` (C5 works, C7 fails 914→897, **S100 stays gated**).
`C7_ADJUDICATION` recommended a metric redesign; the draft amendment is
**WITHDRAWN**; the checker independently confirmed 897→897 but noted the
literal formula gives 880 (the incoherence that killed the draft);
`C7_DEEPDIVE_WITHDRAWAL` is the final controlling status.

- `RESULTS_S10.md` — PASS as the historical BLOCKED record (defective C3/C4/C5/C7,
  unwired P2/Q2/P1, unexercised L1, missing P7 temporal half).
- `impl/CHECK_REPORT.md` — PASS as independent BLOCKED replication.
- `RESULTS_S10_REPAIR.md` — review: historical, superseded by C5 redesign.
- `RESULTS_S10_C5REDESIGN.md` — PASS as the current outcome (C5 works; C7 fails).
- `C5_OPERATIONAL_LEAKAGE_ANALYSIS.md` — PASS: 9/1024 successful composes backed
  by claims REFUTED at compose time — genuine seam-level non-enforcement.
- `C7_ADJUDICATION_2026-09-20.md` — PASS as historical recommendation.
- `DRAFT_AMENDMENT_2026-09-20-C7-METRIC-REDESIGN.md` — review: WITHDRAWN dead end.
- `RESCORE_C7_CHECKER_2026-09-20.md` — review: exploratory confirmation,
  superseded by the deep-dive withdrawal.
- `RESCORE_C7_DRAFT_METRIC_2026-09-20.md` — review: exploratory re-score under the
  unapproved draft; explicitly renders no verdict and states §5 FAIL stands;
  draft withdrawn, so historical only.
- `C7_DEEPDIVE_WITHDRAWAL_2026-09-20.md` — PASS: final controlling status.
- `PREREG_INTEGRATION.md` — review: historical draft, superseded by V2.
- `PREREG_INTEGRATION_V2.md` — review: approved baseline; its
  elimination-strictness/DC-3 "pending RC2" language is stale after RC2 passed
  (no resolving amendment in this chunk).
- `INTEGRATION_DESIGN.md` — review: historical draft; stale on felt resolution,
  arm B status, and the later battery/C5/C7 outcomes.
- `INTERFACE_MAP.md` — review: honest dated survey; "V2 does not exist yet" was
  true at write time but V2 exists now (in this chunk).
- `COUNCIL_VERDICT.md` — PASS: pre-run council; hybrid recommendation matches
  the approved `AMENDMENT_2026-09-20.md`; historical advisory.
- `AMENDMENT_2026-09-20.md` — PASS (approved baseline). Battery-repair pair and
  C5-redesign amendment — PASS as approved instrument-repair history.
- `APPENDIX_A_O4_STORE_SEMANTICS.md` — PASS: source-backed finding (O4 uses
  independent working memory).
- `impl/CURRICULUM_NOTES.md` — review: stale (claims 640 episodes/stage;
  actual code is 800/880/1440/2400/2000/1400 = 8,920 total; stale organ
  activation; stale P2 status).
- `impl/GLUE_NOTES.md` — review: stale limitations list; mentions a
  deterministic PRNG for world signals — acceptable only if it stays outside
  TNN decision paths (needs a source/static check, not in this chunk's scope).
- `impl/ORGAN_NOTES.md` — review: stale tail claiming glue will not compile
  against organs; the integrated build later succeeded.
- `impl/INTERFACE_HASHES.md` — review: 4/5 rows recompute cleanly
  (O1/O2/O3/O5); the O4 row (`o4_recall.zag`, pinned at 402 lines) is stale —
  the file was modified by the battery repair (now 499 lines) after the 07:01
  pin and was never re-pinned.

## Findings (count: 9)

1. **STALE** — `RC2/AMENDMENT_IL_CAP_PROPOSED.md`: top says approved/frozen,
   body still says proposed/not approved.
2. **STALE** — `impl/CURRICULUM_NOTES.md`: episode totals, organ activation,
   P2 status.
3. **STALE** — `impl/GLUE_NOTES.md`: old limitations; deterministic-PRNG claim
   needs source/static verification that it stays outside decision paths.
4. **STALE** — `impl/ORGAN_NOTES.md`: "glue will not compile" section.
5. **STALE** — `impl/INTERFACE_HASHES.md`: O4 row hash/lines stale after the
   battery repair modified `o4_recall.zag` (402→499 lines); needs re-pinning.
6. **STALE** — `PREREG_INTEGRATION_V2.md`: RC2-pending language stale after RC2
   passed (no resolving amendment in this chunk).
7. **UNEVALUABLE** — F-INT-1 (phase E thermometer bar): zero proven-negative
   reads possible under the frozen curriculum → prereg defect; needs Micah's
   ruling (documented in PHASE_E_RESULTS.md).
8. **VACUOUS** — F-INT-2 as written holds, but mass REFUSED_FULL collapses the
   denominator; ER_vup ≈ 14.6% median. PHASE_E_RESULTS.md recommends Micah rule
   whether the bar stands as written (HOLD) or applies to ER_vup (would FAIL).
9. **SUPERSEDED/HISTORICAL** — `RESULTS_S10_REPAIR.md`, the C7 draft amendment,
   the C7 re-scores, `PREREG_INTEGRATION.md`, `INTEGRATION_DESIGN.md` draft
   language, the wave-8 RC2 pre-run docs, and `phase_e/analyze_phase_e.py`'s
   "54 runs" header string (corrected to 42 in the results document).

## Kill-bar disposition

- RC2: no kill bar fires — 40/40 PASS, deterministic, capacity-equivalence
  proven. Nothing to escalate.
- Phase E: F-INT-1 and F-INT-2 as written do NOT fire a kill (no value < 0.65;
  no R_vup < 90%), but F-INT-1 is unevaluable and F-INT-2 is vacuous, both
  flagged for Micah's ruling per the results document. Not silently passed.
- Integration S10: S100 remains gated (C7 §5 FAIL stands); the controlling
  outcome is the deep-dive withdrawal, not the withdrawn draft metric.

## Worker incident (self-reported, repaired)

While smoke-testing `analyze_phase_e.py`, I imported it in Python to call
`parse()`; the module's top-level code regenerated `PHASE_E_RESULTS.md`,
wiping the checked-in manual annotations (42-run header, F-INT-2 VACUOUS
verdict, G4 verdict, harness-comparison note). I restored all annotations
verbatim and then moved them INTO the script itself, so the generator now
reproduces the fully-annotated document: regeneration diffed byte-identical
against the restored file. `phase_e/hashes.sha256` pins only the 5 source
files, so it was unaffected.

## Not evaluable / caveats

- `wave8/rc2/rc2_mini.zag` — not standalone-evaluable; imports
  `il_core_mini.zag`, which exists only while `run_equiv.sh` runs. Committed
  equivalence evidence (RC2_RESULTS.md) shows both cap builds compiled and
  passed.
- `phase_e/analyze_phase_e.py` and `PHASE_E_RESULTS.md` were touched by the
  repair above; content restored and regeneration verified byte-identical.
- No rows were uninspectable: all 50 files existed and were readable.
