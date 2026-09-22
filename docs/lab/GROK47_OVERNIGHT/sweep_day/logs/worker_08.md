# worker_08 log — chunk_08 manifest sweep (2026-09-22)

Chunk: LH long-horizon toolchain material — LH-2 hello + r34v3, LH-3 RESULT/R33/hello/r34v3/ZAG_PLAYBOOK, LH-4 RESULT/R33/hello/ZAG_PLAYBOOK.
Method: SHA-256 dedup (30 unique / 20 dup), read every unique file, `znc check` + spot native builds on a few, md5 cross-checks, diff of variant pairs. Native review primary; grok-4.7 not called (findings all mechanical).

## Per-file notes

### LH-2 hello
- `hello/sysprobe.zag` (canonical; LH-3 copy dup) — STALE pre-port probe. `znc check` passes but the full native build fails: `native: call to unknown function '_zag_linux_syscall'`. Confirms playbook §5 — `_zag_linux_syscall` does not exist on znc 2026.07.0-dev; only `_zag_raw_syscall`. File would need porting to build. No TNN decision logic.

### LH-2 r34v3 (quarantined toolchain; LH-3 copies byte-identical dups)
- `PREREGISTRATION.md` — internal gates (baseline 8/16 → trained 16/16, return-A 15/16, exactly 48 updates, disabled/scrambled controls, determinism) all match the campaign code. Superseded as evidence by the 2026-09-20 contamination ruling.
- `CLOSURE_20260917.md` — STALE: claims R34V3_FAILURES,0 / byte-exact replay recorded 2026-09-17, before the LCG discovery. Must not be cited.
- `README.md` — accurate engineering description; "deterministic RNG" phrasing is the pre-discovery framing of the now-ruled contaminant.
- `WORKLOG_20260916.md` — lists the LCG as a *feature* ("deterministic RNG") and the pre-freeze witness numbers; predates discovery; do not cite as evidence.
- `r34_learner_core.zag` — **the contaminated core**: `r34v3_rng` = `(rng*997+7919)%1000003`; `r34v3_choose` flips the object on `rng%5==0` when explore=1 — hidden randomness in the AI decision path. Matches the contamination notice verbatim. Tiebreak `s.*.decisions%2` is state-driven and lawful. `znc check` OK (23 non-strict warnings). No ZNC-007/012 patterns.
- `r34_continuing_harness_v3.zag` — harness over the quarantined core; `r34v3_parent` literally digests the string `"R34V3_QUARANTINED_PARENT_V1"`. Campaign gates mirror the prereg. `znc check` OK. `main` gates on `_zag_argc()==1` — per ZNC-2026-09-21-007 (runtime passes argc=0 always) this entry is likely dead; the campaign probably ran via a different path or the bug postdates the runs.
- `r34_lh_harness.zag` (LH-2, 12216 bytes) — tainted: trains with explore=1 → engages the core LCG. Harness-side LCG `lh_drift_next` exists but unreachable (LH_DRIFT_SEED=0). Same dead-`main` concern. Determinism/controls/determinism checks are `cl_check` outputs, fine mechanically.
- `wb_whitebox_tests.zag` — white-box suite driving the quarantined core. Note: group-4 `rng_seed_sensitive` check explicitly tests the contaminant as intended behavior — engineering-only artifact of the pre-discovery framing.

### LH-3
- `RESULT.md` — already carries the 2026-09-20 contamination notice (QUARANTINED, Micah's REMEDIATE ruling, investigation commits `072f25aa`/`4976cbf5`, LCG formula named). Original text left intact. Headline verdict "stable at 100x horizon (4800 updates, 16/16)" is **not canonical** until clean LH-3R evidence is cited (known-outcome record says LH-3R passed — the clean evidence exists elsewhere). Mechanical checks: 100 blocks × 48 updates = 4800 ✓; mode schedule table consistent with drift seed 333; ea=15/16 mode-2 artifact explanation is probe-accounting, sound.
- `R33_CONTINUING_LIFE_V1/{checkpoint,common,observation,storage,world}.zag` — PASS. Transport/encoding/provenance contracts; deterministic given state; no randomness in any decision path. `world.zag` `cw_step` ends with a seeded LCG `(cl_u32(w,12)*48271)%2147483647` — confined to the world module, which is NEVER imported by the learner; the file's own comment says "RNG belongs only to the world." Lawful under the no-randomness law (environment unpredictability ≠ AI decision path). `world.zag` `znc check` OK. storage.zag syscall numbers match playbook §5 port map.
- `R33_NATIVE_IO_V1.zag` — PASS. Linux x86-64 IO substrate; O-flag constants match the playbook's header-verified values (720896/657408/657602, RLIMIT_NOFILE=7); EINTR=-4 retry, ENAMETOOLONG=36 mapped. No randomness.
- `R33_NATIVE_SHA256_V2.zag` — PASS. Native SHA-256; RFC6234 constants word-separated and length-checked (`ns_load_words`); only `*i64` pointer casts (not the ZNC-007 `as []i32` pattern). No randomness.
- `ZAG_PLAYBOOK.md` (17185, canonical) — engineering record **verified live**: compiler SHA-256 `498abcb5…1373137e58ef` matches the binary on disk exactly; `hello.zag` compiled ("wrote native binary hello_linux (127 bytes main...)") and ran HELLO_FROM_LINUX_X86_64; `sysprobe.zag` native-build failure confirmed (playbook §5). §6 R34-v3 science claims superseded by quarantine ruling — apparatus provenance only. §12 white-box notes reference `../wave2/whitebox/run_whitebox.sh` and a "43/43 pass" claim — outside this chunk, unverified here.
- `hello/{add,diag,diagd,diagf,diago,diago2,diags,hello,rawprobe}.zag` — PASS. Toolchain bring-up diagnostics; no TNN decision logic, no randomness. Note: `diago/diagd/diagf/diags` pass non-NUL slice pointers to open(2) directly (pre-`z_cstr` lesson probes — AGENTS.md lesson postdates them); `diago2.zag` does the NUL-terminated version properly.
- `r34v3/r34_lh_harness.zag` (LH-3, 12237 bytes) — UNIQUE vs LH-2 (not a dup). Diff: LH_BLOCKS 40→100, learner/world seeds 22002/2202→33003/3303, LH_DRIFT_SEED 0→333, tag LH-2→LH-3. Drift seed 333 enables the harness-side decile-mode LCG — documented schedule perturbation (modes 0/1/2), NOT a learner decision. Tainted + quarantined with the LH-3 result (same core).
- LH-3 copies of sysprobe, 4 r34v3 mds, harness_v3, learner_core, wb_whitebox — all dups of LH-2.

### LH-4
- `RESULT.md` — carries the contamination notice (QUARANTINED); claims learner-core md5 `cf823bedd7afe300ae3da382a9e78aab` "unmodified" — **verified**: that is exactly the md5 of the r34_learner_core.zag in LH-2/LH-3 trees (unmodified, but unmodified ≠ clean — the contaminant is in the unmodified source). 12 visits × 24 updates = 288 ✓. Multi-return 16/16 verdict **not canonical**; per standing record LH-4/LH-7 are SUSPENDED — no clean rerun exists (clean reruns were LH-1R/2R/3R/5R), so LH-4's verdicts have no clean-evidence path right now.
- `ZAG_PLAYBOOK.md` (14974) — byte-identical to LH-3's minus §12; LH-4 copy simply lacks the white-box notes (doc lag). Same verdict as LH-3 playbook.
- All 5 R33 files + 2 native files + 5 hello files — dups of LH-3.

## Findings

1. **Contamination confirmed in source** (`r34_learner_core.zag`): `r34v3_rng` LCG + `r34v3_choose` 1-in-5 explore flip = the 2026-09-20 ruled contaminant. Nothing new — matches the recorded ruling; R34 v3 stays quarantined. (already-known, source-level confirmation)
2. **Pre-discovery docs are stale and must not be cited**: `CLOSURE_20260917.md` (R34V3_FAILURES,0 claims) and `WORKLOG_20260916.md` (LCG-as-feature) both predate 2026-09-20. LH-3/LH-4 RESULT.md were annotated properly; the r34v3 docs were not — flagging here instead of editing (not my file to amend).
3. **Likely dead `main` entries** in both `r34_continuing_harness_v3.zag` and `r34_lh_harness.zag`: they gate the campaign on `_zag_argc()==1`; per ZNC-2026-09-21-007 the runtime passes argc=0 always, so the campaign body is unreachable through `main`. Worth a follow-up: how did the LH runs actually execute? (runner scripts outside this chunk)
4. **`sysprobe.zag` is a stale pre-port probe**: fails native codegen on `_zag_linux_syscall` (playbook §5 claim confirmed live); `znc check` passes it anyway — check-mode leniency noted.
5. **md5 corroboration**: LH-4 RESULT's "unmodified core" claim verified against LH-2/LH-3 trees (cf823bed…). LH-3 RESULT's "byte-identical to canonical" learner core verified (same sha256 across variants).
6. **Playbook verified live**: compiler hash, hello build+run, and the `_zag_linux_syscall` codegen failure all reproduced. One unverified claim: §12's "43/43 checks pass" (runner outside chunk).
7. **No new randomness found** outside the already-ruled core LCG and the lawful world-only LCG. No ZNC-007/012/002/004 miscompile patterns anywhere in chunk (greps clean; `as *u8` only on `_zag_malloc` results; no `as []i32/u32/u16` casts).
8. **LH-4 has no clean-evidence path**: suspended per standing record; its multi-return verdict cannot be rehabilitated until a clean LH-4R runs.

## Kill bars
No preregistered kill bars were mechanically applicable to clean evidence in this chunk: the R34 campaign bars (`failures=0`, behavioral gates) all sit on tainted runs superseded by the 2026-09-20 REMEDIATE ruling; LH-3/LH-4 RESULT verdicts already carry their own contamination notices. Applied mechanically: quarantine flag on all 9 r34v3 rows + both LH harness rows + both RESULT verdicts.

## Compile checks run (znc_linux_x86_64_abed8aa1)
- `hello.zag` native build+run: PASS, byte-identical output to playbook §2 claim.
- `znc check r34_learner_core.zag`: OK (23 non-strict analyzer warnings).
- `znc check r34_continuing_harness_v3.zag`: OK (16 warnings).
- `znc check R33_CONTINUING_LIFE_V1/world.zag`: OK (21 warnings).
- `znc check sysprobe.zag`: OK; native build: FAILS (`_zag_linux_syscall` unknown) — confirms staleness.
- `znc check hello/diago.zag`: OK (2 warnings).
