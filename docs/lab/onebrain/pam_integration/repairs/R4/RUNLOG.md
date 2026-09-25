# RUNLOG — R4 fourth resume (fifth crew, 2026-09-24/25)

## Inherited state (verified live before any change)

1. **Smoke VALID — not rerun from scratch:** `build/artifacts/smoke/run{1,2,3}.out`
   3/3 byte-identical, SHA-256 `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`,
   each ending `OB_FAILURES,0`, zero stderr. Reused for staging.
2. **Red-team artifacts INCOHERENT — rerun clean 3x required:** `redteam/artifacts/run1.out`
   (8879 B, Sep 25 00:01), `run2.out` (9661 B, Sep 24 23:40), `run3.out`
   (9266 B, Sep 25 00:02) — different sizes, different binary generations;
   `.sha256` files stale (from earlier runs).
3. **Implementation exists:** `M_REVISE=113` (overseer-only, N-AUTH, append-only
   revision rows, effective store rewrites superseded `|EXT` → inert `|SUP`)
   in `build/src/sp_gate.zag` and `redteam/src/sp_gate.zag` + `ob_test_redteam.zag`.
4. **Remaining law violation:** `build/src/sp_gate.zag:135` `const SP_REV_CAP:i32=64`
   — arbitrary hard limit vs the no-stupid-limits standing law.
5. **Staging empty except prereg:** `~/workspace/tnn-lab/onebrain/pam_integration/repairs/R4/`
   contains only `PREREG_R4.md`.
6. Three `sp_gate.zag` copies byte-identical at `6648fb970f6e43aa608f308120fad991e475bb6ee700d4ad2f11c61403e4984e`.

## Workdir verification (this crew)

- All three trees present with src/, build scripts, artifacts. Pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` present and used.
- `G_REV`/`G_REV_N`/`SP_REV_CAP` referenced ONLY inside `sp_gate.zag` (plus
  `.zag-cache` semantic records, not committed). No other src file touches the
  revision region → edit localized to one file per tree.
- All shared src files byte-identical across the three trees (each SHA ×3);
  only per-tree drivers differ (`ob_test_integration.zag`, `ob_lh_bal.zag`,
  `ob_lh_int.zag`, `ob_test_redteam.zag`, `corpus_probe.zag`).
- Redteam battery baseline: ran the PRE-CHANGE `ob_redteam_bin` (built Sep 24
  23:58 from `SP_REV_CAP=64` sources) once to `/tmp/rt_baseline.out` for the
  K6 pre-revision-section comparison.

## Change made (the no-stupid-limits repair)

`SP_REV_CAP=64` DELETED. Revision rows moved to physically-chunked,
logically-unbounded storage, same shape as the committed R2 repair
(`docs/lab/onebrain/pam_integration/repairs/R2/build/src/sp_gate.zag` on
branch `tnn-native-lab`, studied 2026-09-25):

- Layout: `G_REV_HEAD` (i64 head-chunk ptr, 0 = none), `G_REV_N` (i32 total
  rows); `G_STATE_SZ` 108908 → 107892. Old `G_REV` 64×16 region gone.
- `SP_REV_ROWS=65536` rows/chunk, 16 B/row → chunk `8+65536*16 = 1,048,584 B`
  < 33,554,432 (znc 2^25 slice ceiling — the load-bearing limit).
- New fns (all in `sp_gate.zag`): `sp_rev_g64`/`sp_rev_s64` (i64 word
  accessors), `sp_rev_chunk` (slice view; null ptr = loud stop on physical
  exhaustion, never silent), `sp_rev_get` (row/field read),
  `sp_rev_append` (on-demand chunk allocation, never drops),
  rewritten `sp_rev_newest` (same newest-row semantics via `sp_rev_get`).
- `sp_rev_cycle`: bound changed from `hops<=SP_REV_CAP` to `hops<=n`
  (n = live row count) — data-derived, not arbitrary: n+1 hops among n rows
  force a repeated row by pigeonhole → periodic walk → fail closed.
- `sp_revise_one`: the `n>=SP_REV_CAP` refusal (reason `SP_R_REV_CAP`) is
  gone; apply = `sp_rev_append` + `SP_L_REVISE` ledger row. `SP_R_REV_CAP=15`
  kept as a reserved ledger code (comment notes it is now unused).
- Semantics preserved: append order = row index order → latest-revision-wins,
  `chain_prev` audit chain, effective-store `|SUP` rewrite, all 7 warrant
  checks in prereg order — unchanged.
- `redteam/src/ob_test_redteam.zag`: two mechanical line updates in
  `rt_r4_revise` Gate B (`ob_g32(g2,G_REV+1*16+4)` → `sp_rev_get(g2,1,1)`,
  `ob_g32(g2,G_REV+1*16+12)` → `sp_rev_get(g2,1,3)` — identical row/field
  reads through the new accessor); new probe `rt_r4_uncapped` (100
  revisions past the old cap, read-back, supersession, effective store,
  end-to-end INSTALL + falsehood WITHHOLD), called from `main` after
  `rt_r4_revise`. The prereg's "existing attack functions byte-untouched"
  is bent ONLY for these two accessor lines (forced by the parent-directed
  storage change); all check names/values/expectations unchanged.
- Edited `sp_gate.zag` SHA-256 `0fa841f7b9ec4904b04ec424ff047ef188e69c3b797eaa4f9756ff5cd9d14a06`,
  byte-identical in `build/src`, `longhorizon/src`, `redteam/src`.

## Builds (pinned znc; old binaries removed first per the writer quirk)

- `redteam/ob_redteam_bin` rebuilt 2026-09-25 (analyzer warnings only, as before).
- `build/ob_integration_bin` rebuilt 2026-09-25.
- `longhorizon/ob_lh_bal_bin`, `ob_lh_int_bin` rebuilt 2026-09-25.

## Battery results

### Smoke (`build/run_smoke.sh`, 3x)
- 3/3 byte-identical, SHA `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
  — EXACTLY the inherited SHA. Change is behavior-preserving on the smoke path.
  Each ends `OB_FAILURES,0`, zero stderr.

### Red-team (clean 3x, `redteam/run_redteam.sh`, 2026-09-25)
- 3/3 byte-identical, SHA `e419318e54f5f0be521257b72b1e50ca60e2b3e3093507b0daa2330490413b97`
  (15987 B each). `RT_FAILURES,0`, `RT_K3_HITS,0`, zero stderr, 504 OB_CHECKs,
  zero mismatches.
- `rt_r4_revise`: all 60 `r4v_` checks pass (K1–K5 preserved).
- `rt_r4_uncapped` (new): 220/220 `r4u_` checks pass — 100 revisions applied
  past the old cap, read-back exact (rows 64/99), supersession holds,
  effective store `|SUP`/`|EXT` correct, end-to-end INSTALL + falsehood WITHHOLD.
- K6: pre-revision section (218 lines) of the new output byte-identical to
  the pre-change binary's section (which was itself byte-identical to the
  Sep-24 run2.out section).
- Environment note: two background battery runs were killed mid-output with
  no stderr while two heavy batteries ran concurrently (sessions reaped);
  partial outputs showed zero check mismatches in every completed section
  (all 60 r4v_ + 220 r4u_ green before the redteam kill, which landed in the
  revision-untouched `rt_exhaust` R2 section). Sequential reruns all completed
  cleanly. LH/smoke drivers never touch revision machinery (grep: 0 refs),
  so the LH int run2 kill is provably unrelated to this change.

### Long-horizon (`longhorizon/run_lh.sh` equivalent, 3x each + frozen-ref compare)
- `ob_lh_bal`: 3/3 byte-identical, SHA `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`
  (frozen ref) — K7 PASS.
- `ob_lh_int`: 3/3 byte-identical, SHA `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`
  (frozen ref) — K7 PASS. (One backgrounded run2 was killed mid-output as
  noted above; rerun sequentially → clean.)
- All end `OB_FAILURES,0`, zero stderr.

### RNG scan (K8)
- `grep -rniE "rand|srand|random|lcg|entropy|_zag_random"` over all three
  `src/` trees (minus `.zag-cache`): ZERO hits. Batteries 3x byte-identical
  (smoke, redteam, LH bal+int) — the empirical backstop.

## Staging / commit
- (pending batteries) Stage per-tree `src/`, `evidence/{smoke,redteam,longhorizon}`
  (3x outputs + SHA-256 each), reports (`BUILD_REPORT.md`, `INTEGRATION_SPEC.md`,
  `RNG_SCAN.md`, `ATTACK_LOG.md`, `RESULTS.md`, `LONGHORIZON_REPORT.md`,
  `VERDICT_R4.md`), never binaries/`.zagd`/`.zag-cache`/`probe/`.
