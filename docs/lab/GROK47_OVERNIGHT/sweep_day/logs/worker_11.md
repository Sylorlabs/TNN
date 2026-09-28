# Sweep worker_11 log — chunk_11 (50 rows), 2026-09-22 ~07:15 PDT

Scope: `wave2/longhorizon` (r34v3 toolchain), `wave2/posttable` (CTX design/prereg/trial), `wave2/ruleslab` (P2/P3 learning rules). 50 rows → 27 unique files reviewed in depth, 23 exact byte-duplicates marked `dup:<first chunk occurrence>`. No commits, no manifest edits, no cron jobs, no external contact, no spend. grok-4.7 not needed — native review covered everything (0 of ~5 calls used).

## Method

- SHA-256 over all 50 rows → 27 distinct hashes. Canonical for dup verdicts = first occurrence in chunk order (within-chunk dedup only; cross-chunk dups belong to other workers).
- Pattern scans across all zag files: LCG constants (997/7919/1000003), `as []i32|u32|u16` consecutive casts (ZNC-007), `slice as *u8` (ZNC-002), annotated slice-let off local struct value (ZNC-004), `s.field.subfield` chains through pointer-in-struct (ZNC-012), nested shift in `&`-test (ZNC-008), `}else{` depth (ZNC-013).
- Spot builds with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (5 builds, all clean, `--no-analyze --no-zagd`): `wb_whitebox_tests.zag` (ran: WB_FAILURES,0), `trial_ht1.zag` (ran twice: byte-identical, HT1_FAILURES,0), `baseline/trial.zag` (ran twice: byte-identical), `p2_twospeed/trial.zag`, `p3_adaptive_eps/trial.zag` (each ran twice: byte-identical).

## Per-file findings

### r34v3 toolchain (QUARANTINED — the known LCG taint)
- `r34_learner_core.zag`: hidden LCG `r34v3_rng` (`(rng*997+7919)%1000003`) engaged in `r34v3_choose` under `explore_enabled==1` (`rng%5==0` → flip). Exactly the taint described in the contamination notices. Struct-literal inits are plain scalars (no ZNC-012 literal-init-with-pointer); no ZNC-007/004/008/012 patterns.
- `r34_p1_learner_core.zag`: same LCG (`p1_rng`) in choose; P1 struct-promote mechanics (ACCEPTED/CANDIDATE tables, E51AJ per-arm gate) otherwise sound. Note its doc references `wave2/ruleslab/PREREG_P1_STRUCT_PROMOTE.md` — not in this chunk; flag to coordinator that the P1 prereg should be sweep-checked where it lives.
- `r34_p3_learner_core.zag`: same LCG in choose (period-modulated: `rng%period==0`); wire v4 layout (168 bytes) as documented.
- `wb_whitebox_tests.zag`: builds and runs, WB_FAILURES,0 (roundtrip incl. rng field, corrupt-refused, ledger consistency/orphan/mismatch). LCG presence here is apparatus (seed-sensitivity test), not a decision-path violation.

### posttable (CTX) — PASS
- `CTX_DESIGN.md`, `POST_TABLE.md`, `PREREG_HT1.md`, `TRIAL_RESULTS_HT1.md`: all carry the dated 2026-09-20 LH-5 contamination note; claims consistent with known outcomes (MA1, 357-switch storm, HT1 11/11). No stale claims found.
- `ctx_core.zag`: zero randomness in the decision path. `CTX_SWITCH` corroboration (target maj-pos AND active maj-neg from recorded evidence, else REFUSED_UNVERIFIED) is structural, as claimed. Audit invariants (clean refusals, replay-from-genesis, verified-switch scan) verified by reading; `nio_alloc` arenas hand-zeroed per playbook §12; `nio_free` only of `nio_alloc` results (no ZNC-006 nested-free).
- `toy_core.zag`: byte-copy of the quarantined r34v3 core, but used as the expected-negative control with `explore_enabled=0` — the LCG is never engaged in `choose` on this path. My rerun confirms the 357-switch storm reproduces with exploration OFF, which directly supports the contamination note's claim of independent reproduction. PASS as apparatus.
- `trial_ht1.zag`: the harness LCG (`ht_next`, same constants) is a seeded *environment* stream (regime flips, 15% evidence noise) — not the learner's decision path; both arms see identical curriculum by construction. CTX arm decisions are rng-free. Rerun byte-identical: HT1_TRUE_FLIPS,10 / HT1_CTX_SWITCHES,11 / HT1_CTX_REFUSALS_UNVERIFIED,0 / HT1_CTX_COLLAPSED_BLOCKS,0 / HT1_CTX_END_R0,16 / HT1_CTX_END_R1,16 / HT1_TOY_SWITCHES,357 / HT1_TOY_COLLAPSED_BLOCKS,2 / HT1_TOY_END_R0,16 / HT1_TOY_END_R1,0 — matching TRIAL_RESULTS_HT1.md's table cell-for-cell.

### ruleslab (P2/P3) — mixed, quarantine notices accurate
- `PREREG_P2_TWOSPEED.md`: outcome REJECTED recorded honestly with mechanism of failure (slow-table tie-break drag, 25%/8ep decay, 4000 margin never fires) and explicit "do not rerun as parameterized". Contamination notice present and factually accurate (P2 explores identically to baseline by construction).
- `PREREG_P3_ADAPTIVE_EPS.md`: outcome ACCEPTED 3/3 recorded with the richer-worlds caveat. Contamination notice present and accurate (P3 = preregistered mechanism under test; recorded-but-uncertified pending clean baseline).
- `RULES_SURVEY.md`: mechanics verified against source; the "never wired in" qualification-stage substrates (curiosity v1, memory-lifecycle v1, hypothesis-state v1, self-model v1) are described accurately. Contamination notice present.
- `TRIAL_RESULTS.md`: all seed-7331 baseline/P2/P3 rows reproduced byte-identically by rerun (trainA 35/31/37; trainB 33/30/35; returnA 15/16; explores 5/5/3 + 11/11/7). Contamination notice accurate: the trial driver runs train phases with explore=1, so baseline and P2 exploratory episodes come from the tainted LCG stream.
- `baseline/learner_core.zag`: QUARANTINED (LCG in `trl_choose`). `baseline/episode.zag`: PASS (shared machinery; explore flag passed through; world rng is the seeded cw world, deterministic).
- `baseline/trial.zag`: PASS — reproduced the published seed-7331 row exactly; byte-identical across runs.
- `p2_twospeed/learner_core.zag`: QUARANTINED (same LCG); rerun reproduced published numbers.
- `p3_adaptive_eps/learner_core.zag`: QUARANTINED-ish (LCG stream, period-modulated — the preregistered mechanism under test); byte-identical reruns; numbers match published table.
- `sweep_baseline_12345/trial.zag`, `sweep_baseline_999/trial.zag`: PASS — substantive (not dups): byte-identical to baseline/trial.zag except the learner seed constant (7331→12345 / →999, single-line diff each).

### substrate (5 files, canonical in posttable/ctx/substrate; ruleslab copies byte-identical)
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`, `cl/common.zag`, `cl/observation.zag`, `cl/world.zag`: PASS. `as *u8` occurs only on `_zag_malloc` results (not slice-as-*u8). `cl_u32` returns i64 (unsigned); callers sign-extend explicitly (e.g. `cl_pcm_at`). `world.zag`'s Park-Miller stream in `cw_step` is the seeded environment, not a learner decision path. No ZNC-004/007/008/012/013 patterns.

## Known znc miscompile patterns: NONE FOUND in this chunk
No consecutive same-size `as []i32|u32|u16` casts, no slice-as-*u8, no annotated slice-lets off local struct values, no `s.field.subfield` chains through pointer-in-struct, no nested shift-in-`&`-test, no 5-deep else nesting. (Stray `};` check: none found.)

## Kill bars applied
- HT1 criteria 1–5 + toy-control (PREREG_HT1.md): my byte-identical rerun gives HT1_FAILURES,0 — all five CTX criteria hold (0 collapsed blocks, 11 ≤ 2×10 switches, 16/16 both regimes, audit-clean + replay + verified-scan pass, 2 distinct labels) and the toy control shows the curriculum stresses the table (357 switches, 2 collapsed blocks, R1 0/16). PASS mechanically.
- P2 falsification (returnA ≤ baseline on any seed → reject): doc records REJECTED; verdict stands.
- P3 falsification (exploratory count not dropping → reject): doc records ACCEPTED 3/3; verdict stands (recorded-but-uncertified per contamination note).

## Findings / flags for the parent
1. Confirmed by rerun: the 357-switch storm reproduces with the toy's exploration disabled (`explore_enabled=0`, LCG never engaged in choose) — the contamination notes' "independently reproduced under explore-disabled conditions" claim is true on the artifact.
2. `r34_p1_learner_core.zag` references `wave2/ruleslab/PREREG_P1_STRUCT_PROMOTE.md`, which is not in chunk_11 — ensure the owning worker sweep-checks it.
3. All 23 dups are within-chunk; canonical = first chunk occurrence. If other chunks contain the same byte content (likely: sweep dirs were copied), cross-chunk dedup will need a global pass before final manifest freeze.
4. Note: `sweep_p3_adaptive_eps_999/` exists on disk but was not in chunk_11 (chunk ends at `sweep_p3_adaptive_eps_12345/learner_core.zag`) — chunking boundary, not an omission by this worker.

## Tally
- 50/50 rows evaluated, status=done, verdicts filled.
- PASS or PASS-as-apparatus: 20 unique + 2 near-dup sweep trials (22) plus 23 dup rows.
- QUARANTINED: 7 unique rows (r34v3 core, p1, p3, baseline learner core, p2 learner core, p3 ruleslab learner core, toy_core is PASS-as-apparatus not quarantined).
- Rows not evaluable: 0.
