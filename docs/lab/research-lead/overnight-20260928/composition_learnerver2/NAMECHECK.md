# NAMECHECK: H-COMPVER-2 Learner-Verified Composition Extension

## Step 0: Worker toolchain guard (mandatory, recorded before any work)

- Ran the safebin setup block at session start (2026-10-02 ~07:46 PDT):
  linked git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack into
  $HOME/safebin.
- `export PATH="$HOME/safebin"` active for all commands in this session.
- `which python3 python` under safebin PATH returned NOTHING (empty
  output before "guard-check-done"). No python3/python resolves.
- All computation in this task is pure Zag via the pinned znc binary
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1, reached through
  $HOME/safebin/znc). Shell used only to invoke znc, run binaries, and
  do file/git operations.
- If any forbidden executable is invoked, this wave is PROCESS-FAIL.

## Provenance (to be completed after implementation)

- lv2_base.zag: byte-identical copy of
  composition_learnerver/lvcomp_base.zag (itself cc_base.zag +
  un_patch.zag). Verified with cmp.
- lv2_patch.zag: verbatim copy of
  composition_learnerver/lvcomp_patch.zag (320 lines) plus the new
  ev_cquery section (CONSTRUCT-goal query entry point).
- lv2_driver.zag: new battery driver. World builders ported verbatim
  from composition_unified/un_driver.zag; evidence helper adapted from
  composition_learnerver/lvcomp_driver.zag (parametrized cycles).
- Build: cat lv2_base.zag lv2_patch.zag lv2_driver.zag > lv2_full.zag;
  compiled with pinned znc; 3 runs; SHA-256 recorded in REPORT.md.

## Constraints honored

- Unfrozen variant only. Frozen sources read-only (copies made with cp).
- Pure Zag. Zero Python invocations (guard above).
- Zero em/en dashes in all documentation (byte-verified with grep).
- Research paper untouched. Nothing pushed to GitHub (local commits only).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- No researcher answer parameter anywhere in the learner path:
  compose_lv, lv_dfs, ev_cquery take no target parameter; grep audit in
  REPORT.md.
- Git commits use EXPLICIT pathspecs only.
