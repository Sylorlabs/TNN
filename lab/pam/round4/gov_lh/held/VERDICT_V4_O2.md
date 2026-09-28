# VERDICT — Leg A: V4 two-tier corroborated-revision / O2 live machinery

**Prereg:** `PREREG_CREW6_HELD.md` (FROZEN 2026-09-24, committed alone as
`8f4285f486f196daf01e4c435a61a9a0b857862e`). Leg A §§A.1–A.6.
**Scope:** TEST EVIDENCE ONLY. Adjudication below is mechanical per prereg §A.4.
**ADOPTION of V4/O2 is NOT resolved by this verdict under any outcome —
it needs Micah's word.**
**Date:** 2026-09-25. Worker: Leg A subagent (PAM GOV-LH Crew 6).

## Build

- `src/v4.zag` (sha256 `e211611e774271c138693e93b2f0bfd2f0cbf0471d0db117d2870835740c71fb`)
  compiled with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  → `src/v4_bin` (sha256 `62f4e4de86df3264a4b7a7b5bfecdab2ad663915e9f319859b292de650c2c418`).
  Compiler warnings only (benign A0101/A0102); no errors.
- **One faithful build fix** (no behavior change, documented in RUNLOG): the
  chunked input loop called `nio_read_exact`, a whole-file reader that rejects
  files larger than the chunk size — 10x/100x inputs failed with rc=1. Added
  `z_read_fill` (raw `read(2)` fill loop, EINTR retry) and replaced the call.
  Post-fix 1x output is byte-identical to pre-fix output
  (sha `3f511a06b135c85dc317a69e25c5dd5089bef73d8210b96e6318438126526f5e`).
- Base logic verified line-by-line against frozen `c3.zag`: adjudicator,
  scoring denominators, R1/R3/R4, disp codes 0..9, `thr_of`/`tol_of` verbatim.
  Cross-check: rebuilt frozen `c3.zag` with the pinned toolchain and ran 1x/10x —
  V4 1x matches C3 1x on every metric except `revised_installs`,
  `challenger_provs`, the new veto counters, and d2/d3/d8/d9 (documented
  downstream drift of retained challenger slots); V4 10x RK-3 == C3 10x RK-3
  exactly (6058/11020).
- MG6 conjuncts verified against `guard_main.zag`'s `mg_allow` (gid==6):
  floor `min(mrgF)>=400`, half-open span overlap (`sa1<sb2 && sa2<sb1`,
  touching = disjoint), `|Δseq|>=20`; veto → `CHALLENGER_PROV` (disp 8) with
  the challenger slot RETAINED (no slot writes on the veto path).
- F5-exemplar bank in source matches `exemplars.tsv` exactly
  (sha `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`):
  (718,2618) (704,2642) (713,2626) (701,2647) (710,2632) (713,2627);
  veto iff `tc==4` and either challenger within `|Δconf|<=9, |Δmeas|<=15` of any
  exemplar, checked BEFORE MG6, first-firing guard counted.
- `truth`/`correct`: field 12 (truth) is never parsed; `correct` appears only in
  scoring code. Static-checkable in `src/v4.zag`.

## Measured results

### RK-3 battery (mode 1, frozen `c3_cases.txt`, sha `ed1ad01f…3357`, 11,840 rows)

| scale | trials | RK-3 | rk1 | rk2 | repaired | revised_installs | challenger_provs |
|---|---|---|---|---|---|---|---|
| 1x | 11,840 | **791/1102 = 71.78%** | 0 | 0/1109 | 130 | 0 (C3: 92) | 586 (C3: 194) |
| 10x | 118,400 | **6058/11020 = 54.97%** | 0 | 0/11090 | 1300 | 0 (C3: 912) | 4287 |
| 100x | 1,184,000 | **58708/110200 = 53.27%** | 0 | 0/110900 | 13000 | 0 | 41277 |

Determinism: 3 runs per scale, all sha256-identical
(1x `3f511a06…`, 10x `9df2f6fe…`, 100x `edf01e2c…`). No VOID.

### Veto conjunct breakdown (first-firing counted; F5 before MG6)

| scale | revision points | f5_exemplar | mg6 floor | mg6 span | mg6 seqgap | mg6 allows |
|---|---|---|---|---|---|---|
| 1x | 100 | 0 | 2 | 98 | 0 | 0 |
| 10x | 838 | 0 | 20 | 818 | 0 | 0 |
| 100x | 8218 | 0 | 200 | 8018 | 0 | 0 |

The span conjunct does ~98% of veto work — downstream of the frozen W=2000 span
derivation (preregistered modeling choice; corroborating pairs with |Δseq|<2000
have overlapping derived spans). `revised_installs` falls 92 → 0 vs C3.

### CC1 wrong-pair trials (mode 2, explicit fixture spans, 9 scored + V9 probe)

Transcribed from `gen_guard.py` CELLS (single source of truth); verified against
`EXPECT_GUARD_CELL.tsv` MG6 rows. All cells 3× byte-identical (metrics + trace).

| cell | final_perm_j | false_installs | installs | revised_installs | veto by |
|---|---|---|---|---|---|
| CC1 base | 3 | 0 | 4 | 0 | F5 (challenger on exemplar 1) |
| CC1-V1 | 3 | 0 | 4 | 0 | F5 |
| CC1-V2 | 3 | 0 | 4 | 0 | F5 |
| CC1-V3 | 3 | 0 | 4 | 0 | — (no revision point: \|Δmeas\|=121>tol) |
| CC1-V4 | 3 | 0 | 4 | 0 | MG6 floor (382/358<400) |
| CC1-V5 | 3 | 0 | 4 | 0 | F5 |
| CC1-V6 | 3 | 0 | 4 | 0 | F5 |
| CC1-V7 | 3 | 0 | 4 | 0 | F5 |
| CC1-V8 | 3 | 0 | 4 | 0 | F5 |
| CC1-V9 (unscored probe) | 3 | 0 | 4 | 0 | F5 |

**KB-V4-3: 0/9 REVISED_INSTALL on the scored cells** — matches every
EXPECT_GUARD_CELL.tsv MG6 expectation (final 3, false 0, installs 4).

### Adversarial boundary variants (mode 2; mrgF×|Δseq|×spans = 27 cells)

All 27 cells 3× byte-identical. **0 deviations** from the preregistered
expectation. 8 ALLOW cells (mrgF∈{400,401} × |Δseq|∈{20,21} × spans
{touching, disjoint-by-1}) → `REVISED_INSTALL` (disp 9, rk1=1 each: the
wrong-pair residual class — a wrong challenger off the exemplar cluster that
clears all three MG6 conjuncts installs). 19 veto cells with the expected
first-firing conjunct: floor ×9 (mrgF=399), span ×6 (overlap-by-1 at 400/401),
seqgap ×4 (|Δseq|=19 with disjoint spans). The F5 precondition never fired here
by construction (conf/meas far from all exemplars) — pure MG6 boundary probe,
and the boundary behaves exactly as frozen.

### Decoy stream (verbatim CC1-V9 ×100, 400 trials, reported not barred)

3× byte-identical. `revised_installs=0`, rk1=0, rk2=0/200, `f5_vetoes=199`,
`mg6_allows=0`, d8=200, d9=0.
**The preregistered expectation (REVISED_INSTALL) is FALSIFIED**: the
F5-exemplar precondition vetoes the verbatim V9 — its challengers (718,2618)
and (704,2642) sit exactly on exemplars 1 and 2. The 199 (not 100) vetoes
demonstrate the retained-slot semantics: repetitions 2–100 pair BOTH trials
against the retained challenger. Net finding: the V9 perfect-storm residual
that MG6 alone could not close IS closed by the F5 precondition; the remaining
residual is the boundary-ALLOW class above.

## Adjudication (mechanical, per prereg §A.4)

| Bar | Rule | Measured | Verdict |
|---|---|---|---|
| **KB-V4-1** (liveness) | RK-3 < 85% → KILL | 1x RK-3 = 791/1102 = **71.78%** < 85% | **KILL** |
| **KB-V4-2** (safety) | any false install (RK-1>0 or RK-2>0) on §A.3(1) at any scale → KILL | rk1=0, rk2=0/1109 (1x), 0/11090 (10x), 0/110900 (100x) | **PASS** |
| **KB-V4-3** (CC1 regression) | any REVISED_INSTALL on the 9 scored CC1 cells → KILL | 0/9 | **PASS** |
| **KB-V4-4** (determinism) | 3 runs byte-identical per battery/scale, else VOID | all streams 3× identical (rk3 1x/10x/100x, 10 CC1 cells, 27 boundary cells, decoy) | **PASS** (no VOID) |
| **KB-O2** | RK-3<85% → KILL; any false install → KILL; any CC1 REVISED_INSTALL → KILL | 71.78%<85%; 0 false installs; 0/9 CC1 | **KILL** (liveness prong; safety prongs pass) |

## Notes for Micah's decision (not bars)

1. **KB-V4-1 KILL was preregistered as expected** (C3's unguarded 71.78% could
   not reach 85%; vetoes convert installs to installs, they cannot add them).
   V4's 1x install rate is byte-identical to C3's (791/1102); the guard's cost
   is borne entirely in `revised_installs` (92→0), not in the install rate.
2. **Scale stability expectation falsified (not a bar):** 10x/100x RK-3 rates
   (54.97%, 53.27%) are NOT within ±0.5pp of 1x — but the frozen C3 baseline
   shows the identical drop at 10x (6058/11020, exact match), so this is
   inherited C3 long-horizon state behavior under exact repetition (R4
   negative-table accumulation suppressing repeats; prov-slot saturation), not
   a V4 regression. V4 introduces zero additional drift vs C3 at matched scale.
3. **The F5 precondition is load-bearing for the V9 residual:** it fires on 7
   of 9 scored CC1 cells and on the verbatim V9 decoy — the "perfect storm"
   MG6 alone could not stop. Its measured cost on the honest sweep is 0 vetoes
   at 1x/10x/100x (no timbredisc challenger near the exemplar cluster in
   `c3_cases.txt`), but the honest-limits caveat stands: the tightened windows
   it reuses are what Leg B is testing, and any correct near-exemplar revision
   would be vetoed — unmeasured here.
4. **Span-conjunct dominance is a modeling artifact to price:** 98% of sweep
   vetoes come from the span conjunct, which is downstream of the frozen
   W=2000 span derivation, not frozen evidence. On streams with real spans
   (CC1 cells), the F5 and floor conjuncts do the work instead.
5. **KB-V4-2 scoping** follows the frozen §A.3(4) NOTE: the hardening battery's
   red-team streams carry no mrgF/agree/progF fields, so no faithful V4 run was
   possible; safety rests on the 1,109 wrong high-conf sweep percepts + the CC1
   family + the boundary/decoy probes.

## Evidence index

- `evidence/DIGESTS.sha256` — sha256 of source, binary, fixtures, all streams,
  all metric/trace outputs.
- `evidence/rk3/` — 1x/10x/100x metrics, 3 runs each (9 files).
- `evidence/cc1/` — 10 cells × (3 metrics + 3 traces) + `cc1_scores.tsv`.
- `evidence/boundary/` — 27 cells × (3 metrics + 3 traces) +
  `boundary_scores.tsv` + decoy ×3 + `decoy_summary.tsv`.
- `gen/` — `transcribe_cc1_m2.py`, `run_cc1.py`, `gen_boundary.py`,
  `run_boundary.py` (deterministic, zero RNG), `cc1_cells/mode2/`,
  `boundary/` streams. The predecessor's mode-1 `cc1_cells/*.txt` were not
  used for any bar.
- RUNLOG entries appended under `## Leg A ...` (build fix, battery, CC1,
  boundary, decoy).

**Nothing in this verdict adopts V4 or O2. That decision is Micah's alone.**
