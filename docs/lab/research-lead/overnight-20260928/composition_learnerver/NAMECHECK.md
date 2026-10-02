# NAMECHECK: H-COMPVER-1 Learner-Verified Composition

## Step 0: Worker toolchain guard (mandatory, recorded before any work)
- Ran the safebin setup block at session start (2026-10-02 ~07:34 PDT):
  linked git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack into $HOME/safebin.
- `export PATH="$HOME/safebin"` active for all commands in this session.
- `which python3 python` under safebin PATH returned NOTHING
  (output was empty before "guard-check-done"). No python3/python resolves.
- All computation in this task is pure Zag via the pinned znc binary
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1). Shell used only to
  invoke znc, run binaries, and do file/git operations.
- If any forbidden executable is invoked, this wave is PROCESS-FAIL.

## Provenance
- Base cognition: copies (never edits) of frozen
  composition_C/cc_base.zag and composition_unified/un_patch.zag,
  concatenated as lvcomp_base.zag. Verified byte-identical to the first
  2097 lines of composition_unified/un_full.zag via cmp.
- Prediction machinery: ported from learner_verification/lv_base.zag
  (ev_predict, pred_record, pred_resolve, ev_observe-with-resolution),
  renamed with lv_ prefix to avoid collisions; logic preserved.
- lv_setup / verify structure: adapted from learner_verification/lv_patch.zag.
- DFS: un_dfs from composition_unified/un_patch.zag with the
  expected-answer termination replaced by learner-prediction termination.
- World builders in the driver: copied verbatim from
  composition_unified/un_driver.zag (t1_train, t1_couse, cmp_gap,
  t1_zfacts, counters), renamed with lvc_ prefix where needed.

## Constraints honored
- Unfrozen variant only. Frozen sources read only (copies made with cp).
- Pure Zag. Zero Python invocations (guard above).
- Zero em/en dashes in all documentation (byte-verified with grep).
- Research paper untouched. Nothing pushed to GitHub (local commits only).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- The verifier must not smuggle expected answers: compose_lv and lv_dfs
  take no expected parameter; grep audit recorded in REPORT.md.
- Git commits use EXPLICIT pathspecs only.
