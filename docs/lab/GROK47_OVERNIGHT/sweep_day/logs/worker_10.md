# Worker 10 sweep log — 2026-09-22 (chunk_10, 50 rows)

Scope: LH-7 toolchain (hello probes, r34v3 quarantine set) + LH-P3
(RESULT.md, R33 substrate, ZAG_PLAYBOOK.md, hello probes, r34v3 md,
8 lh_* campaign harnesses). Method: sha256 all files (all present,
sizes match manifest), byte-compare for dups, full read of md files,
grep sweeps for randomness + the znc miscompile patterns (ZNC-007
consecutive same-size `as []i32`/`[]u32`/`[]u16`, ZNC-004 annotated
slice-let off local struct value, `slice as *u8`, chained
`s.field.subfield` through pointer-in-struct, stray `};`, 8-arg
`_zag_raw_syscall`, `(x as i64)*512`, >32MB slice allocs, 5-deep
else nesting), structural-isolation import check, and `znc check`
spot-compiles with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

No grok-4.7 calls used — native review was conclusive on every row.

## Findings (4)

1. **Seeded LCG in `r34_learner_core.zag` confirmed tainted.** Line 15:
   `fn r34v3_rng(s:*R34V3State)i32 {let v:i32=r34v3_mod(s.*.rng*997+7919,1000003);...}`
   drives the explore flip at line 38:
   `if(explore_enabled==1 && r34v3_mod(r34v3_rng(s),5)==0){obj=1-obj;ex=1;}`
   — exactly the 1-in-5 explore-flip contamination from the known
   outcomes (Micah's REMEDIATE ruling). This file is the quarantined,
   pre-remediation version; it must not be cited as a no-RNG exemplar.
2. **LCG still present in the LH-P3 cores (context, not in chunk).**
   `r34_p3_learner_core.zag` line 49 still coins explores via
   `r34v3_mod(r34v3_rng(s),s.*.period)`; `r34_p1_learner_core.zag` line 108
   via `p1_mod(p1_rng(s),5)`. This matches RESULT.md's own contamination
   notice — no new violation, but it means the P3 adaptive mechanism rides
   on the tainted coin, and the quarantine stands until the clean baseline
   re-run happens.
3. **Stale claim flagged:** `WORKLOG_20260916.md` says the learner core
   contains "deterministic RNG" — stale since the 2026-09-20 remediation
   (LCG removed, state-driven explore installed). Quarantine caveat noted
   in the verdict.
4. **Playbook toolchain SHA verified:** `ZAG_PLAYBOOK.md` claims
   `498abcb5...1373137e58ef` for the pinned znc binary — recomputed on
   this VM, byte-identical. Its §6 R34 v3 runtime proofs document the
   pre-remediation apparatus only; no science claims contradict the
   known quarantine.

## Per-file verdicts

### LH-7/toolchain/hello (10 rows) — all PASS
`add, diag, diagd, diagf, diago, diago2, diags, hello, rawprobe, sysprobe`
— substrate smoke probes (syscalls, cstr helpers, open-flag matrix).
`znc check` OK on hello/add/diago2/sysprobe (diago2: 3 non-fatal analyzer
warnings). No randomness, no decision paths, no miscompile patterns.
`*u8 -> []u8` only ever via `p[0..n]` — the legal direction.

### LH-7/toolchain/r34v3 (8 rows)
- `CLOSURE_20260917.md` — review: bars (8/16, 16/16, 48 updates,
  refusals 2005/2001) match the prereg; pre-remediation evidence on the
  tainted lineage, quarantine caveat applies.
- `PREREGISTRATION.md` — review: isolation prereg coherent; verified by
  inspection that the learner imports only `observation.zag`.
- `README.md` — review: module-split description accurate per inspection.
- `WORKLOG_20260916.md` — review: stale "deterministic RNG" claim (see
  finding 3); pre-freeze witness figures match prereg bars.
- `r34_continuing_harness_v3.zag` — review: quarantined v3 harness;
  pattern sweep clean (no bad casts, no chained field access, no stray
  `};` beyond struct-literal initializers, 7-arg syscalls only).
- `r34_learner_core.zag` — review: the tainted LCG version (finding 1);
  `znc check` OK; isolation gate satisfied; no miscompile patterns. Note:
  `r34v3_decode` whole-assigns a 23-field flat struct (`s.*=t`) —
  ZNC-009-adjacent latent risk, not a fail.
- `r34_lh7_harness.zag` — review: seeds documented (learner 55223 /
  world 353); `znc check` OK; drives the tainted core, quarantined.
- `wb_whitebox_tests.zag` — review: `znc check` OK (10 non-fatal
  warnings); includes `rng_seed_sensitive` asserting seeded-RNG behavior —
  self-consistent with pre-remediation code only.

### LH-P3 (11 non-dup rows)
- `RESULT.md` — PASS: carries its own 2026-09-20 contamination notice
  quarantining all P3-vs-R34 comparisons pending a clean baseline re-run
  — matches known outcomes exactly. P3 core sha
  `4aa6d6b6...704f14bc1e` verified identical to the on-disk file.
  C1/C2/C3 numbers, the mixed C3 verdict, and the do-not-promote-P1-on-
  clean-protocol reading are prereg-following judgments; no kill bar is
  tripped by this document. The struct-by-value `stream` footgun it
  documents is already fixed (`&stream`) in the lh_p1 sources.
- `R33_CONTINUING_LIFE_V1/{checkpoint,common,observation,storage,world}.zag`
  — PASS: `znc check` OK on io/sha256/observation/world; pattern sweep
  clean; no RNG.
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` — PASS: `znc check`
  OK; no issues.
- `ZAG_PLAYBOOK.md` — PASS: SHA verified (finding 4); honest
  compile/runtime/historical separation; §9 not-proven list present;
  §11 "Zag only, no Python" standing rule noted.

### Duplicates (15 rows) — all byte-identical to canonical LH-7 paths
LH-P3 `hello/` ×10, `r34v3/{CLOSURE,PREREGISTRATION,README,WORKLOG}` ×4,
and `r34_continuing_harness_v3.zag` ×1 are all byte-for-byte dups of the
LH-7 versions reviewed above.

### LH-P3/toolchain/r34v3/lh_* harnesses (8 rows) — all review
`lh_c1_fixed` (`znc check` OK), `lh_p1_baseline` (OK), `lh_p3_c2` (OK),
`lh_c1_p3`, `lh_fixed_c3`, `lh_p1_trial`, `lh_p3_c3`, `lh_p3_checkpoint`
(pattern sweep clean; 3 of 8 spot-compiled). All import their
lineage-appropriate cores and belong to the quarantined LH-P3 campaign;
no miscompile patterns found in any of them.

## Kill bars
None of the 50 rows references a preregistered kill bar whose condition
is tripped. RESULT.md's prereg falsification readings were already made
by the authoring agent and are judgments, not live bar trips. The
contamination notices are quarantine statuses, handled mechanically by
marking the affected rows `review:` rather than PASS.

## Rows not evaluable
None — all 50 files present and readable; all manifest sizes match
(`stat` check, zero mismatches). The imported-but-unchunked cores
`r34_p3_learner_core.zag` / `r34_p1_learner_core.zag` were verified for
RNG state as context only (not swept as rows).

## Summary
- Rows done: 50/50. Findings: 4. Rows not evaluable: 0.
- 19 PASS (10 LH-7 hello probes, RESULT.md, 5 R33 modules, 2 native
  substrates, ZAG_PLAYBOOK.md).
- 16 review (8 LH-7 r34v3 docs+code, 8 LH-P3 lh_* harnesses).
- 15 dup (LH-P3 copies of LH-7 files).
- No new randomness violations beyond the known, quarantined LCG
  lineage. No znc miscompile patterns in any of the 40 zag files.
  No grok-4.7 calls consumed.
