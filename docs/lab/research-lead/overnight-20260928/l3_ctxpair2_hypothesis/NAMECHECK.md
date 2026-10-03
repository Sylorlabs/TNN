# NAMECHECK: L3-CTXPAIR-2-HYPOTHESIS worker

**Worker:** L3-CTXPAIR-2-HYPOTHESIS (subagent, depth 2/2)
**Date:** 2026-10-03
**Task:** hypothesis generation only (H-CTXPAIR-2 prereg) as a competing
hypothesis to H-CTXPAIR-1 for the ctx-blind used-pair set finding from
L3-SUF-1-SCALING REPORT.md finding (a). Non-ledger task (claim minting
paused). No implementation exists or is authorized.

## Step 0: toolchain guard verification

- No research logic was executed in this lane: no builds, no binaries,
  no scripts run. Shell was used only for read-only discovery
  (`ls`, `sed -n`/`grep` page reads, `git` status/log) and for creating
  the lane directory.
- `which python3` / `which python` were never invoked; no interpreter
  of any kind was invoked. There is nothing to PROCESS-FAIL: the
  forbidden-interpreter rule is vacuously satisfied (no execution).
- If a future builder wave is spawned under this prereg, it must run
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`,
  `export PATH="$HOME/safebin"`, verify `which python3` returns nothing,
  and record it in its own NAMECHECK.md Step 0.

## Step 1: frozen-source integrity

- Frozen L3-SUF-1 src/ (`l3_suf_intermediate/src/`) was READ ONLY
  (read/grep for mechanism grounding: `l_probe_phase` stages (a)/(b),
  `l_predict2` fab semantics, `l_form_new`/`l_form_add`/`l_form_find`
  kind0/kind1/kind2 behavior, `l_do_test` logging, `l_guard_reexpand` /
  `l_union_reexpand` repair paths, the single `l_probe_phase` call site
  in `l_escalate`). No writes, no copies, no links.
- The adversary's sealed worlds and KEY.md were NOT inspected
  (l3_suf_adversary/ was never opened).
- The scaling worker's worlds (`l3_suf_scaling/scale_world.zag`,
  `scale_main.zag`) and REPORT.md were READ ONLY (grep/sed for A/D/U
  training semantics, truth functions, stakes construction).

## Step 2: prereg discipline

- PREREG.md frozen and committed BEFORE any implementation exists.
  There is no implementation in this lane and there never will be
  under this prereg: the lane is hypothesis-only by tasking.
- Commit-order self-check: the freeze commit contains ONLY PREREG.md
  and NAMECHECK.md under l3_ctxpair2_hypothesis/.
- Meta-preregistration (section 0 of PREREG.md): the six criteria for
  a good hypothesis (H2-CRIT-1..6) were frozen before the hypothesis
  content (sections 1-8); the self-check table holds the hypothesis
  against them.

## Step 3: determinism

- Not applicable: no runs were performed. The future builder's
  determinism bar is H2-K8 (3/3 byte-identical per run, sha256 digests),
  preregistered in PREREG.md section 6 (T3).
