# NAMECHECK: H-GOALINF-1 Goal-Type Inference

## Step 0: Worker toolchain guard (mandatory, recorded before any work)

- Ran the safebin setup block at session start (2026-10-02 ~07:57 PDT):
  linked git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack into
  $HOME/safebin.
- `export PATH="$HOME/safebin"` active for all commands in this session.
- `which python3 python` under safebin PATH returned NOTHING (empty
  output before "guard-check-done"). No python3/python resolves.
- All computation in this task is pure Zag via the pinned znc binary
  (reached through $HOME/safebin/znc). Shell used only to invoke znc,
  run binaries, assemble with cat, and do file/git operations.
- If any forbidden executable is invoked, this wave is PROCESS-FAIL.

## Provenance (completed after implementation)

- gi_base.zag (2444 lines): byte-identical concatenation (cmp-verified
  against head -n 2444 of lv2_full.zag) of H-COMPVER-2's lv2_base.zag
  (2097 lines) + lv2_patch.zag (347 lines). Never edited; ev_query,
  compose_lv, ev_cquery untouched (frozen read-only, copied).
- gi_patch.zag (226 lines): new code. gi_factscan (FACT scan mirroring
  lv_predict ordering), gi_probe (target-free greedy structural walk via
  un_candidates/un_satisfy, read-only), gi_supersede (native type-3
  self-edge, the same primitive lv_observe uses on contradiction),
  gi_compose (compose_lv's body with caller-supplied pred/rel; the
  reliability gate unchanged), ev_iquery (the inference entry; route
  codes 0=RETRIEVE, 1=CONSTRUCT, 2=CONSTRUCT-CONFLICT, 3=WITHHOLD in
  st[12]; probe execs accumulated in st[8]).
- gi_driver.zag (272 lines): instrumentation, T1 world builders
  (t1_train, t1_couse, t1_zfacts, t1_world, cmp_gap), and the
  lv2_evidence helper copied verbatim (sed-extracted) from
  H-COMPVER-2's lv2_driver.zag; plus new gi_confirm helper (predict +
  resolve cycles that never write a FACT, so a taught FACT earns its
  own score), gi_cost_construct, the 5-test battery, and main.
- Build: cat gi_base.zag gi_patch.zag gi_driver.zag > gi_full.zag
  (2942 lines); compiled with pinned znc (exit 0, A0102 warnings only,
  same class as H-COMPVER-2); 3 runs, SHA-256
  abc1afdb0f796a1625edf7f121893e1b57f83c3ebf897abd92b46db215687291,
  3/3 byte-identical.
- Prereg commit-order self-check: PREREG.md committed alone in
  5fd4988d8 before any implementation file existed; this results
  commit strictly follows it.

## Constraints honored

- Unfrozen variant only. Frozen sources read-only (copies made with cp
  and cat; cmp-verified).
- Pure Zag. Zero Python invocations (guard above).
- Zero em/en dashes in all documentation (byte-verified with grep).
- Research paper untouched. Nothing pushed to GitHub (local commits only).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- No researcher goal flag and no researcher target in the learner path:
  ev_iquery takes (W,s,r,masked,st); the token `expected` occurs 0
  times in gi_patch.zag (grep-verified); the -999999 sentinel passed to
  ev_query on the RETRIEVE arm is inert on the activate path.
- Git commits use EXPLICIT pathspecs only.
