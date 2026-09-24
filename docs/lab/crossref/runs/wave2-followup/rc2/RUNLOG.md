# RC2 10x-leg follow-up — RUNLOG

**Worker:** resume replacement (predecessor errored 2026-09-24 17:24 UTC, daemon restart drain).
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 verified `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` before use.
**Constraints honored:** scratch workspace only; no RNG; no commits or pushes to `sylorlabs/TNN`.

## Inherited state (verified, not re-run)

- `work/clean/wave7/reasoning-control/trial/` — predecessor's 10× build at 2026-09-24 17:05 UTC: `rc2_trial.zag` (19,172 bytes), `rc2_bin`, `run1.stdout`, `run2.stdout`, `committed_run1.stdout`, `compile.stderr` (0 bytes), `run1.stderr`/`run2.stderr` (0 bytes).
  - Verified: `cmp run1.stdout run2.stdout` clean; `cmp run1.stdout committed_run1.stdout` clean; tail shows `RC2_STAT,final,E=2,W=24,stage=4`, `RC2_FAILURES,0`, `TRIAL PASSED`.
- `work/oldrun2/wave7/reasoning-control/trial/` — predecessor's side-by-side: new-source runs (`RC2_FAILURES,0`, `TRIAL PASSED`) and old-source runs (`old_run1.stdout`, `RC2_FAILURES,8`); `rc2_bin` and `rc2old_bin` binaries.
- `work/old/rc2_trial_old.zag` — the 2026-09-22 committed RC2 source.
- `work/rc2_trial.zag` — predecessor working copy (not used for the final clean run).
- `T3-RC1-RUNLOG.branch.md` — predecessor's RC1 replication notes, containing the RC2 status record ("RC2 proper DID RUN … RC2_FAILURES,8 … The 10× scale leg … did NOT run") that this leg supersedes.
- `src/wave7/reasoning-control/trial/` — mirror of the wave-7 trial dir (rc2_trial.zag, run_rc2.sh).

## Actions (resume worker, 2026-09-24 ~17:40–18:00 UTC)

1. Compared `work/oldrun2/.../rc2_trial.zag` vs `work/clean/.../rc2_trial.zag` — differ at char 15441, line 479 (comment rewording + probe reorder; see VERDICT.md). Outputs (`run1.stdout`) byte-identical across both dirs.
2. Rebuilt the 10× binary: `znc rc2_trial.zag --no-zagd --no-analyze --no-foreground-cache -o rc2_bin_rebuild` → SHA-256 `60bb048a31bfcb9541101988aff16c7dffe1d61db9797d05147fa13551ec124d`, **byte-identical to predecessor's `rc2_bin`** (same SHA in both `work/clean/` and `work/oldrun2/`).
3. Third run: `./rc2_bin_rebuild > run3.stdout` → exit 0, **byte-identical to run1.stdout** (58 lines, `RC2_FAILURES,0`, `TRIAL PASSED`).
4. No-RNG gate: `grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc'` over new source, old source, and `il_core.zag` → zero hits; bare `@import` present in new source.
5. Reconstruction of `RC2_FAILURES,8`: mirrored the required import layout at `work/reconstruct/wave7/reasoning-control/trial/` + `work/reconstruct/wave4/integrity-ledger/` (clean `il_core.zag` + substrate copies), compiled `rc2_trial_old.zag` with pinned znc → `rc2old_bin` SHA-256 `f3cd57d082228d46e480a9d44af6838845f234ca2b677a97e46e5eaf621b3a32`, **byte-identical to predecessor's `rc2old_bin`**; ran it → exit 8, `old_recon_run1.stdout` **byte-identical to historical `old_run1.stdout`**, `RC2_FAILURES,8`, same 8 failing `CL_CHECK` lines.
6. Diffed old vs new trial sources: the fix is probe reordering (cherry probe moved before the lying probe) plus a new cherry2 boundary probe and amendment-prototype checks; root cause of the 8 recorded in VERDICT.md.
7. Wrote `VERDICT.md` (this log's sibling).

## Notes / anomalies

- One transient exec-session registration timeout ("timed out after 15s registering session metadata") during the old-binary run; retried foreground and succeeded. No data lost.
- `work/clean/.../committed_run1.stdout` is a local staging copy of the new run's output, not a committed record; nothing was committed or pushed per task constraints.
- No open items: the 10× leg is complete and verified; the `RC2_FAILURES,8` record is reconstructed and root-caused.
