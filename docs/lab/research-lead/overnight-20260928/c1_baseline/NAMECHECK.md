# Step 0 name-check: C1 Simple Baseline Worker

Date: 2026-09-30 UTC

The standing rules from LOOP_STATE.md that apply to this task:

1. PURE ZAG ONLY. No Python anywhere: not glue, not analysis, not
verifiers, not harnesses. All three baselines (MEM, FREQ, RAND) are
implemented in Zag and compiled with the pinned znc; the shell only
sequences processes and runs byte checks. Fixture provisioning counts
as loop work, so world reuse is by git blob extraction, not Python.
2. Shell-only byte checks. Dash checks via
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh;
never python3 for byte checks.
3. Fork testing and the image-judge rule are not applicable to this
baseline-comparison task (no image work, no new forks created).

Governance I will honor: prereg committed alone before any
implementation (K1); frozen worlds reused byte-identical
(e0a30377f) and never modified (K2); commits local with explicit
pathspecs confined to
docs/lab/research-lead/overnight-20260928/c1_baseline/; git status
inspected before every commit; contaminated paper
TNN_RESEARCH_PAPER_20260929.md untouched; live .git/index.lock never
removed (wait and retry). New Zag code uses u8-backed cells with the
st32/ld32 little-endian idiom; no `as *i32` slice construction inside
functions (pinned znc aliasing workaround per AGENTS.md).

This name-check was written before any baseline implementation.
