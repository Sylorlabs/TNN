# Sweep worker_02 log — chunk_02 (50 rows)

Date: 2026-09-22. Worker: cb4ba97b label, native review primary. grok-4.7 calls: 0 (nothing needed LLM judgment beyond native reading).
Method: read each file per kind; grep all 27 zag files for (a) rand|random|lcg|seed|entropy tokens in decision paths, (b) ZNC-007/004/002/012 miscompile patterns; spot-compiled hello.zag (ran OK), t1.zag (FAIL), pdec.zag (OK) with pinned `znc_linux_x86_64_abed8aa1`; self-ran readback_mdl.py and bt1_scorecards.py on smoke inputs; byte-compared 3 substrate dups. Stray compile binaries cleaned up.

## Findings (actionable)

1. **r34v3 = quarantined contaminated set (7 rows: 4 md + 3 zag).** The contamination notices (dated 2026-09-20) on all four docs match the known LH outcome exactly: `r34v3_rng` = `(rng*997+7919) mod 1000003` in `r34_learner_core.zag` driving 1-in-5 explore flips at `r34v3_choose:38` (verified by reading the source line). The harness passes `explore=1` through `r34v3_begin_episode`. This is law-violating randomness in a TNN decision path — already quarantined, do not revive or cite. `wave1/README.md` and `toolchain/ZAG_PLAYBOOK.md` §6 both cite the campaign numbers with matching dated notices — no stale un-annotated claims found.
2. **`scratch_w7/imp/t1.zag` does not compile.** Importing `delib.zag` + `tb_types.zag` together pulls two vendored copies of `R33_NATIVE_IO_V1.zag` (one under `units/teachers/learner/`, one under `units/teachers/battery/substrate/`), each defining `nio_metric` → znc aborts with "duplicate fn definition 'nio_metric'". Double-vendored IO substrate; the probe is unusable as written. (Note: this is a diagnostic scratch probe, not a shipped component.)
3. **`wave10/int-c7s100/work/src0/CURRICULUM_NOTES.md` is stale.** Claims 640 episodes/stage (3,840 total) and DC-3 organs O1+O2+O3+O5; CHECK_REPORT §3/§4 (same chunk, independently verified) documents the true code values: DC-0 800 / DC-1 880 / DC-2 1440 / DC-3 2400 / DC-4 2000 / DC-5 1400 = 8,920 total, DC-3 organs=27 (O1+O2+O4+O5, no O3). The checker's doc flags this; CURRICULUM_NOTES itself is not amended. Code is authoritative.
4. **`scratch_w7/imp2/pdec.zag` verified clean and compiling.** It probes `p_decode` wire parsing (ZNC-2026-09-21-011 context: draft vs frozen §P layout); spot-compiled OK with the pinned toolchain.

## Kill-bar applications

- **Debate-norecord (PREREG §4/§5 → RESULTS):** FA tripwire (≥5/6 TRUE picks with margin2>0) got 0/6, all abstain → NOT FALSIFIED (survives). FB tripwire (≥5/6 TRUE picks) got 0/6 FALSE picks → NOT FALSIFIED (survives). Applied mechanically as written. Zero-RNG + byte-identical bars asserted in results; flagged for Micah retroactive review.
- **Felt V3 (AMEND1 A7):** K4 harm fired on all three disjuncts (ER_vup 0.0405 vs 0.1554; F_wbs 0.9595 vs 0; R_wbs 0/117); K3′ restatement fired (naive count-policy replay in-band); K1 did NOT fire (not equivalent — worse); K2 clean. → RETIRE wholesale per A7; no further feeling trials without Micah's re-approval. _EXP5_SKELETONS Branch B matches the executed outcome; A/C unused by design.
- **C7 redesign:** skeleton is DRAFT / not approved / not binding; §5 FAIL stands; S100 stays gated. Direction 3+1 is proposed, not adopted — the flip is Micah's explicit call (no-rescue discipline).
- **INT-1 battery (CHECK_REPORT):** AGREE-BLOCKED — C3/C4/C5/C7 instruments defective (not the bars), P7 temporal excluded, P2/Q2/P1-retention never wired into the driver, DC-5 gate narrower than prereg letter, analysis-driver source deleted (limits recomputation), quoted hash prefixes absent from logs. S100 must not run until repairs + dated amendment.

## Non-findings (checked, nothing to flag)

- No RNG tokens in any decision path of: R33_CONTINUING_LIFE_V1 (world.zag's Park-Miller `(seed*48271)%2^31-1` is environment-side state evolution in a module the header marks "NEVER imported by the learner" — deterministic given seed), debate_nr.zag / il_core.zag (`db_seed` is provenance seeding, not RNG), hello probes, scratch probes (except the quarantined r34v3).
- No ZNC-007 (`as []i32/u32/u16` casts), ZNC-004 (annotated slice-let off local struct), ZNC-002 (`slice as *u8`), or ZNC-012 (chained `s.field.subfield`) patterns in any chunk file. il_core/debate_nr correctly use the []u8-arena + explicit get/set idiom and local-slice-copy idiom. `_zag_slice_ptr` (not the broken cast) is used for syscall paths; `_zag_malloc … as *u8` / `as *i64` pointer casts (not slice casts) in diago2/mkcstr/cl_usage are fine.
- 3 substrate files byte-identical → dup verdicts: wave10/debate-norecord/substrate/R33_NATIVE_IO_V1.zag, …/R33_NATIVE_SHA256_V2.zag, …/cl/common.zag.
- B-T1 docs: closeout readback 12/12 + 6/6 probes hold; repair doc preserves the binding FAIL and re-measures repaired module FAIL (7/11) — no verdict reinterpretation; py files self-ran OK.

## Per-file verdicts

| path | verdict |
|---|---|
| scratch/b_t1_closeout/stage/bt1_scorecards.py | PASS: deterministic scorecards; self-test OK |
| scratch/b_t1_closeout/stage/logs/READBACK.md | PASS: 12/12 readbacks hold; consistent w/ B-T1 FAIL |
| scratch/b_t1_closeout/stage/logs/READBACK_CLOSEOUT.md | PASS: 6/6 closeout probes; no-RNG canary clean |
| scratch/b_t1_closeout/stage/readback_mdl.py | PASS: independent reimplementation; self-test OK |
| scratch/b_t1_repair/REPAIR.md | PASS: FAIL verdict preserved; repaired module also FAIL; 2^25 audit done |
| scratch_w7/imp/t1.zag | **review: does not compile** (double-vendored nio_metric) |
| scratch_w7/imp2/pdec.zag | PASS: compiles clean; ZNC-011 wire probe |
| toolchain/R33_CONTINUING_LIFE_V1/checkpoint.zag | PASS |
| toolchain/R33_CONTINUING_LIFE_V1/common.zag | PASS |
| toolchain/R33_CONTINUING_LIFE_V1/observation.zag | PASS |
| toolchain/R33_CONTINUING_LIFE_V1/storage.zag | PASS: Darwin→Linux port map documented |
| toolchain/R33_CONTINUING_LIFE_V1/world.zag | PASS: world-only Park-Miller seed; never learner-imported |
| toolchain/R33_NATIVE_IO_V1.zag | PASS |
| toolchain/R33_NATIVE_SHA256_V2.zag | PASS |
| toolchain/ZAG_PLAYBOOK.md | PASS: §6 claims covered by contamination notice |
| toolchain/hello/*.zag (10 files) | PASS: benign diagnostic probes; hello.zag ran OK |
| toolchain/r34v3/CLOSURE_20260917.md | **review: QUARANTINED** (notice present, matches LH finding) |
| toolchain/r34v3/PREREGISTRATION.md | **review: QUARANTINED** |
| toolchain/r34v3/README.md | **review: QUARANTINED** |
| toolchain/r34v3/WORKLOG_20260916.md | **review: QUARANTINED** |
| toolchain/r34v3/r34_continuing_harness_v3.zag | **review: QUARANTINED** |
| toolchain/r34v3/r34_learner_core.zag | **review: QUARANTINED — contains the LCG (r34v3_rng, r34v3_choose:38)** |
| toolchain/r34v3/wb_whitebox_tests.zag | **review: QUARANTINED** |
| wave1/README.md | PASS: R34 citation carries contamination notice |
| wave10/debate-norecord/PREREG_DEBATE_NORECORD.md | PASS: frozen prereg, mechanical bars, retro-review flag |
| wave10/debate-norecord/TRIAL_RESULTS_NORECORD.md | PASS: FA/FB tripwires NOT fired (correctly applied) |
| wave10/debate-norecord/debate_nr.zag | PASS: zero RNG; ZNC-safe idioms |
| wave10/debate-norecord/il_core.zag | PASS: zero-RNG ledger; ZNC-safe idioms |
| wave10/debate-norecord/substrate/R33_NATIVE_IO_V1.zag | dup:toolchain/R33_NATIVE_IO_V1.zag |
| wave10/debate-norecord/substrate/R33_NATIVE_SHA256_V2.zag | dup:toolchain/R33_NATIVE_SHA256_V2.zag |
| wave10/debate-norecord/substrate/cl/common.zag | dup:toolchain/R33_CONTINUING_LIFE_V1/common.zag |
| wave10/felt-followup/FELT_RETIRE_ANALYSIS.md | PASS: K4+K3′ fired → RETIRE per A7 |
| wave10/felt-followup/_EXP5_SKELETONS.md | PASS: Branch B executed; A/C unused; no commit |
| wave10/int-c7s100/C7_REDESIGN_ASSESSMENT.md | PASS: design-only; flip is Micah's call |
| wave10/int-c7s100/PREREG_C7_REDESIGN_SKELETON.md | PASS: DRAFT not binding; S100 stays gated |
| wave10/int-c7s100/VERIFICATION_REPORT.md | PASS: claims (a)(b)(c) CONFIRMED; AGREE-BLOCKED |
| wave10/int-c7s100/work/METRIC_NOTE.md | PASS: double-count derived; 880≠897 shown |
| wave10/int-c7s100/work/instrument.py | PASS: print-only instrumentation; read OK |
| wave10/int-c7s100/work/link_chains.py | PASS: strict-key linkage + A1–A8 checks; read OK |
| wave10/int-c7s100/work/src0/CHECK_REPORT.md | PASS: AGREE-BLOCKED; disputes (A)–(D) honest |
| wave10/int-c7s100/work/src0/CURRICULUM_NOTES.md | **review: STALE (640/stage budgets, DC-3 organs)** |

Tally: 50 rows done — 38 PASS, 3 dup, 9 review (7 quarantine + 1 compile-fail + 1 stale). Zero rows unevaluable.
