# NAMECHECK: TNN-2 Build

Date: 2026-09-30/10-01. Builder: TNN-2 Builder (retry; prior worker errored on
infrastructure before producing output; no partial work existed; started clean).
Prereg: `7c1e30522` (TNN2-PREREG-FROZEN). Root-cause basis: `ed38121d4`.
Toolchain: pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## Step 0: Toolchain guard (mandatory)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  equivalent: created `$HOME/safebin` with symlinks to allowed tools only
  (git, znc -> pinned abed8aa1, sh, bash, ls, cp, mv, rm, mkdir, cat, grep,
  sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack, plus
  coreutils present from the prior setup).
- Exported `PATH="$HOME/safebin"` before all work; every exec call in this
  build re-exports it.
- Verified `which python3` returns nothing (exit 127) under the restricted
  PATH. `python` likewise absent.
- All computation in Zag via pinned znc. Shell used only to invoke znc, run
  binaries, do git operations, and move/copy files. File reads/writes via
  file tools.
- Zero Python/C/C++/JS/Rust invocations in this wave.

## K-T2-1: prereg ordering (K1)

- Pre-implementation check (before any tnn2.zag edit):
  `git merge-base --is-ancestor 7c1e30522 HEAD` -> true (exit 0).
  HEAD was `7c1e30522` itself at build start.
- Post-build re-verification recorded at commit time (see build report).

## Frozen sources used (read-only)

- Base: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed_build/tnn1_act.zag`
  (1328 lines; ACT-remediated TNN-1).
- Trial loop reference: `docs/lab/research-lead/overnight-20260928/mul_rungb_build/mul1b.zag`
  (commit `a2223cc11`; propose/execute/verify/promote, odometer search,
  genuine-rejection counting).
- Inquiry reference: `docs/lab/research-lead/overnight-20260928/inquiry_refreeze/inquire.zag`
  (commit `18ed3331c`; Piece A reify_admission, Piece B construct_guides,
  CHOICE 30 inquiry act).
- Root-cause analysis: commit `ed38121d4`.

## K-T2-2 evidence (single executor; code inspection)

- `exec_plan` (the separate step-kind 1-6 executor) is deleted. Verified:
  `grep -n "exec_plan" tnn2.zag` returns zero hits after the edit.
- `execute` (4-op ISA: MOVE/BRANCHEQ/INC/DEC, tags 101-104) is the only
  remaining graph executor. All trial candidates, the revision verifier,
  and tests t_c6/t_c7 route through it.
- No other function walks a cell graph. `seq_nx` is a shared edge follower,
  not an executor.

## K-T2-3 evidence (no fixed templates; code inspection)

- Deleted: `plan_new`, `step_new`, `plan_c2`, `plan_g`, `plan_it`,
  `plan_ext`, `plan_c2c`, `clone_st`, `ch_out`, `mp_gather_k`, `mp_build`,
  `mp_compose`, `verify_plan`, `exact_lu` (only caller was `exec_plan`).
  Verified zero hits for each name in tnn2.zag after the edit.
- Deleted constants: `T_PLAN`, `T_STEP`, `TM_C2`, `TM_G`, `TM_IT`,
  `TM_COMP`, `SK_READ`, `SK_MOVE`, `SK_BEQ`, `SK_INC`, `SK_EMIT`,
  `SK_APPLY` (the removed plan vocabulary).
- Every miss-path executable structure is now assembled at runtime by
  `t2_asm_chain` / `t2_asm_sum` / `t2_asm_count` from primitive 4-op cells
  (tags 101-104), driven by `t2_trial` search over gathered observations.
  No complete graph exists in source; cell count, op per cell, operands,
  and branch targets are chosen by the search and fixed only by
  execution-verified success.
- Anti-theater evidence: new test `t_t2_chain4` solves a 4-hop chain that
  no removed template could express (old ceiling was 3-hop via
  compose-by-cloning); `t_t2_trial_reject` asserts genuine rejections>0
  before the winning candidate on the t_p4 fact pattern.

## K-T2-4 evidence (inquiry integration)

- `miss_inquire` is called from `ev_query`'s cognition path on the true
  -2 miss (after the trial loop and P-INV bootstrap both fail). No test
  scaffolding involved.
- It creates a T_UNCERT node (type 30, existing): field20=miss subject,
  field24=miss relation, field28=2 (ignorance marker, per inquiry build
  vocabulary). Field4=-4 (non-role) so the uncertainty node itself can
  never match the act-role check in `ev_act` (adaptation note: the inquiry
  build's ref0=key moves to payload because TNN-1 field4 is the act role).
- It ensures a T_GROUP POLICY_ROOT (type 2, existing) via `pol_set`.
- It constructs a guide (TNN-1 act pattern from t_a2: type 1, field4=role
  =miss subject, field20=choice=30 the validated inquiry act), links
  G->U via ET_DEP and POLICY_ROOT->G via ET_MEM. Existing node and edge
  types only. No new modes.
- Test `t_t2_inquire` drives this through `ev_teach`/`ev_query` only and
  asserts the UNCERTAINTY node and the POLICY_ROOT-linked guide exist.

## K-T2-5 evidence (act path live)

- Test `t_t2_actlive`: miss on (9002,77) via public `ev_query`, then
  `ctx_push(W,9002)` + `ev_act(W)` returns 30 (the learner-constructed
  inquiry guide's choice), not the hardcoded 0 fallback. No `r_mk_guide`
  / `r_mk_uncert` scaffolding calls in this test.

## K-T2-6 evidence (revision operator)

- `revise_on_contradict` is called from `ev_observe`'s contradiction
  branch (cognition path, not a test).
- `t2_revise_graph`: locates the stale SETREG cell via its ET_DEP
  provenance edge to the contradicted fact, removes that step, inserts a
  corrected step (new cell nodes, SEQ edges rewired), re-executes the
  restructured graph via `execute`, and only on verification success
  updates the promoted answer fact.
- Test `t_t2_revise`: promotes a 2-hop chain graph answering 201,
  contradicts the licensing fact via public `ev_observe`, and asserts
  (a) the restructured graph executes to 999, (b) the stale cell is
  tombstoned and a new cell wired in (topology change), (c)
  `map_standing` is unchanged (no demotion; revision is not standing
  change), (d) the follow-up query returns 999.

## K-T2-7 (determinism)

- All tests pass 3/3 byte-identical; SHA-256 recorded in build report.

## K-T2-8 (toolchain)

- Pure Zag; safebin; zero Python. See Step 0.

## Falsifier checks

- F-T2-1: `execute` is byte-identical to the frozen base (no ISA change);
  no new opcode/mode/bridge/handler/semantic case. `grep` for new
  tag constants: none.
- F-T2-2: `exec_plan` deleted; single executor (see K-T2-2).
- F-T2-3: trial loop is search+verify, not a menu (see K-T2-3).
- F-T2-4: POLICY_ROOT populated by `miss_inquire` from the miss path;
  no test-scaffolding call populates it in the new tests.

## Regression

- All 41 prior tests (35 TNN-1 + 6 ACT-remediation groups / 24 ACT
  assertions) copied with assertions verbatim; only the init call was
  renamed `tnn1_init` -> `tnn2_init`. All pass.
