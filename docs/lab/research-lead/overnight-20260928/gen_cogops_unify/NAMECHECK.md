# NAMECHECK: GEN-COGOPS-UNIFY (COMPRESSION-AUDIT candidate #2, C418)

Worker: GEN-COGOPS-UNIFY. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/gen_cogops_unify/`
Task: investigate whether GEN's composer can subsume COGOPS composition
(one composer for domain and cognitive structures). Analysis +
proof-of-concept; prereg-ready design if feasible.

## Step 0: toolchain guard (safebin mandatory)

- Safebin setup script run: `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  was executed in a prior session; this worker re-verified rather than
  re-ran it.
- `export PATH="$HOME/safebin"` is set for every command in this lane.
- Verification (2026-10-03, this worker, before any build):
  `which python3` -> empty (no result)
  `which python`  -> empty (no result)
  `which znc`     -> /home/hatch/safebin/znc (pinned compiler)
- All research computation in this lane is pure Zag, compiled with the
  pinned safebin znc. Shell is used only for znc/binary/git/assembly/
  byte-verification (diff, cmp, sha256sum, grep).
- If any forbidden executable is invoked, the wave is PROCESS-FAIL per
  standing governance.

## Step 1: frozen source inventory (read-only references)

- GEN composer: `gen_statefix/gsf_gen.zag` (post-GEN-STATEFIX GEN, no
  main) and `gen_generality/ref_gg_base.zag` (frozen base). Both live in
  sibling lanes; copied regions are byte-verified by the build script.
- COGOPS procedures: `cogops_compose/cc_learn.zag` (learner-owned
  ret_spec/vfy_spec bodies, coverage, specialize_*) and
  `cogops_compose/cc_base.zag` (ret_gen/vfy_gen). Lifted regions are
  byte-verified by the build script.
- Compression audit: `compression_audit/COMPRESSION_AUDIT_MECHANISMS.md`
  (candidate #2 spec, section 3).

## Step 2: lane file plan

- `gu_base.zag`  -- adapted base (documented GU-DELTA marks only)
- `gu_learn.zag` -- verbatim-lifted learner procedure bodies
- `gu_glue.zag`  -- new: goal-handle buffers, cognitive MAP classes
- `gu_gen.zag`   -- gsf_gen.zag minus nothing (no main) + 1-token
  garity delta (documented, diff-audited)
- `gu_main.zag`  -- driver: worlds, episodes, teach, queries
- `gu_build.sh`  -- assemble + verify regions + compile + run 3x
- `ANALYSIS.md`  -- feasibility analysis (Q1, Q2, honest negatives)
- `PREREG_DESIGN.md` -- prereg-ready design for the full test
- `poc_run1/2/3.txt` -- PoC outputs
