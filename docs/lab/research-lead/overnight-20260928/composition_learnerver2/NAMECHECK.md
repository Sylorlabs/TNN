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

## Provenance (completed after implementation)

- lv2_base.zag: byte-identical copy (cmp-verified) of
  composition_learnerver/lvcomp_base.zag (itself cc_base.zag +
  un_patch.zag). Never edited; ev_query untouched.
- lv2_patch.zag (347 lines): first 320 lines byte-identical
  (cmp-verified head) to composition_learnerver/lvcomp_patch.zag
  (compose_lv, lv_dfs, lv_setup, lv_predict, lv_pred_resolve,
  lv_observe, lv_verify_chain); plus a new 27-line section defining
  ev_cquery, the CONSTRUCT-goal query entry point (RETRIEVE/CONSTRUCT
  contract distinction, no flag, no ev_query change).
- lv2_driver.zag (455 lines): new battery driver. World builders
  (T1/T2A/T2B/T3/T4 train, couse, zfacts, gap) body-identical to
  composition_unified/un_driver.zag (diff-checked function by function;
  only episode comment lines were re-added to match verbatim); evidence
  helper adapted from composition_learnerver/lvcomp_driver.zag,
  parametrized by cycle count.
- Build: cat lv2_base.zag lv2_patch.zag lv2_driver.zag > lv2_full.zag
  (2899 lines); compiled with pinned znc (exit 0, A0102 warnings only,
  same class as H-COMPVER-1); 3 runs, SHA-256
  fc054b5e3bfb3ef8fcb2e4ad5d94dd0f52e5c65dc7de3b9e6ea8e282d2f8942f,
  3/3 byte-identical.
- Prereg commit-order self-check: PREREG.md committed alone in
  6081afa94 before any implementation file existed; this results
  commit strictly follows it.

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
