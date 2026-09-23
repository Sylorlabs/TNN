# P4 (indexed KB recall) promotion — run record

Frozen prereg: `coding/reflection/speed_intel/PROMOTION_PREREG.md` (commit f5154e8c6c7c050388d03b3580f9d17cd6f2858b).
Date: 2026-09-22. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Baseline (pre-port, flat mainline) — 3 reruns

Battery: `kb/tests/specs.txt` 24 GEN + 6 GATE via `kb/bin/run_recall.py`.
Runs: `baseline_flat_run1.log` (56.5s), `baseline_flat_run2.log` (60.6s),
`baseline_flat_run3.log` (59.1s) — 3 runs byte-identical console logs.

| spec | family | pass | spec | family | pass |
|---|---|---|---|---|---|
| r1 | E-STRREV | PASS | o1 | E-SORT | PASS |
| r2 | E-STRREV | PASS | o2 | E-STRREV | FAIL (output mismatch — frozen quirk) |
| r3 | E-STRREV | PASS | o3 | E-SORT | PASS |
| c1 | E-STRCOUNT | PASS | h1 | E-HASH | PASS |
| c2 | E-STRCOUNT | PASS | h2 | E-HASH | PASS |
| c3 | E-STRCOUNT | PASS | h3 | E-HASH | PASS |
| s1 | E-ARRAYSUM | PASS | w1 | E-FILEWRITE | PASS |
| s2 | E-ARRAYSUM | PASS | w2 | E-FILEWRITE | PASS |
| s3 | E-ARRAYSUM | PASS | w3 | E-FILEWRITE | PASS |
| m1 | E-ARRAYMAP | PASS | f1 | E-FILEREAD | PASS |
| m2 | E-ARRAYMAP | PASS | f2 | E-FILEREAD | PASS |
| m3 | E-ARRAYMAP | PASS | f3 | E-FILEREAD | PASS |

Compile 24/24 · test pass 23/24 · gate 6/6 PASS.
kb.dat sha256 (baseline): `1531fda8108d867eb81c758227bab0dcff99adf4ea4f5a4af9cbcdb65a9e9a2f`
(see `baseline_kbdat.sha256`).

## Baseline probes (SI-flat reference binary, selections proven identical)

`probes_flat_ported.log` is the ported binary in flat mode; the SI reference
gave the same numbers: 69 entries scored/spec, 348.00 probes/query (flat).

## Post-port (default = indexed auto) — 3 reruns

Runs: `indexed_run1.log` (69.6s), `indexed_run2.log` (64.9s),
`indexed_run3.log` (57.9s) — 3 runs byte-identical; compare vs baseline:
`compare_runs.py` → **24/24 family selections byte-identical, pass/fail
identical (23/24, same o2 FAIL), gates 6/6 identical. PASS.**

Install line now also prints:
`KB-INDEX terms=251 assoc=348 bytes=8253 buildops=39870`
kb.dat sha256 post-port: `1531fda8108d867eb81c758227bab0dcff99adf4ea4f5a4af9cbcdb65a9e9a2f`
— byte-identical to baseline (`cmp` verified).

## Probes/query (ported binary, plan mode, 24 GEN specs)

| mode | scored/query | probes/query | tprobes/query | total/query |
|---|---|---|---|---|
| flat (escape hatch) | 69.00 | 348.00 | 0.00 | 348.00 |
| indexed auto (default) | 5.33 | 27.50 | 251.00 | 278.50 |
| Δ (indexed − flat) | −63.67 | − | − | **−69.50** |

Matches frozen Arm-2a evidence (−63.67 entries/spec, −69.5 probes/spec).

## Index build cost / break-even

One-time build: 39,870 term comparisons (`buildops=39870`), index 8,253
bytes (251 terms, 348 term→entry associations). Break-even vs flat:
39870 / 69.5 ≈ **573.8 → 574 queries** (matches frozen honest break-even).

## Wall-clock (end-to-end battery, single-threaded)

| condition | runs | wall-clock (s) |
|---|---|---|
| baseline flat | 3 | 56.5, 60.6, 59.1 |
| indexed default | 3 | 69.6, 64.9, 57.9 |
| flat escape hatch (post-port) | 1 | 55.5 |

No realized wall-clock saving at the 24-query battery scale: recall scoring
is milliseconds either way; battery time is dominated by 72 znc
compile+run invocations (~2s/spec). Per the frozen prereg the mechanism pays
back after 574 queries. Reported honestly per prereg §7 (no save AND extra
surface would kill — here the surface is small and the break-even is
frozen evidence, so promotion proceeds).

## Escape hatch proof

`flat_hatch_run1.log` (`--flat`): `compare_runs.py` vs baseline → **24/24
byte-identical selections, identical pass/fail, gates. PASS.**
Missing/corrupt index fallback verified manually: auto mode with a
truncated `<kbdat>.idx` falls back to flat, same family selected
(scored=69, probes=348, no tprobes line).

## Files changed (NOT committed — parent commits)

1. `coding/reflection/kb/src/kb_install.zag` — appended inverted-index build
   (verbatim from `speed_intel/work_a2/kb_install_si.zag`); argv[3] defaults
   to `<kbdat>.idx` when absent; kb.dat output byte-identical.
2. `coding/reflection/kb/src/kb_main.zag` — ported indexed-recall machinery
   (verbatim from `speed_intel/work_a2/kb_main_si.zag`: `entry_score` probe
   accounting, `do_plan` over cached scores, `pre_score`, `idx_reachable`);
   new default: argv[4] absent/anything-but-"flat" → auto-load
   `<kbpath>.idx` (or argv[5]), use index only if magic `KBIDX1` + bounds
   validate, else flat fallback; `"flat"` → escape hatch. New `idx_try_load`
   (defensive bounds checks; returns 0 → flat on any failure).
3. `coding/reflection/kb/bin/run_recall.py` — installs with index (default
   `<kbdat>.idx`), recalls in default auto mode; new `--flat` flag forces
   the escape hatch; results JSON named `recall_results_flat.json` in flat
   mode; `flat_mode` recorded in JSON.

New files (all under `coding/reflection/speed_intel/work_promo_kb/`,
uncommitted): run logs (`baseline_flat_run{1,2,3}.log`, `indexed_run{1,2,3}.log`,
`flat_hatch_run1.log`), `probes_flat_ported.log`, `probes_indexed_ported.log`,
`compare_runs.py`, `probes_sweep.py`, `baseline_kbdat.sha256`,
`results_baseline_flat.json`, `results_indexed_default.json`,
`results_flat_hatch.json`, this file.

Reference (uncommitted, helper only): `work_promo_kb/ref_install`,
`work_promo_kb/ref_main` (SI binaries for baseline probes), `ref_kb.dat`,
`ref_kb.dat.idx`.

## Deviations from prereg

None material. Two judgment calls, both additive/defensive:
- kb_install argv[3] defaults to `<kbdat>.idx` (prereg lists this exact
  default).
- kb_main auto mode validates the full 7-byte magic `KBIDX1` plus bounds
  checks (SI checked 3 bytes); any validation failure → silent flat fallback
  (proven results-identical). `plan` mode output gains the SI `PLAN
  scored=/probes=/tprobes=` accounting line; `gen` output (the battery path)
  is byte-identical to old mainline in both modes.
- Zero RNG in the promotion path (grep verified); pure Zag, Python glue only.

## Verdict recommendation

**PROMOTE P4.** Kill criteria not triggered: quality tables identical
(24/24 selections byte-identical, same 23/24 pass, same gates), 3 reruns
byte-identical per condition, kb.dat byte-identical, no RNG. Wall-clock
neutral at battery scale with frozen honest break-even of 574 queries.
Rollback: `kb_main ... flat`; code revert via `git revert` of the promotion
commit (parent to commit).
