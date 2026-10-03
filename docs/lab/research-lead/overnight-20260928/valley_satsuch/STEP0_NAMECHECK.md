STEP 0 NAME-CHECK (Valley Satisfiability Searcher, 2026-09-30)

The four standing-rules sections at the top of LOOP_STATE.md and how this task honors them:
1. Standing owner rules (2026-09-23): PURE ZAG ONLY applies fully. The bounded search, the V3 oracle invocation,
   all harness glue, analysis, and byte checks will be pure Zag or shell. No Python anywhere, including scratch.
2. Standing owner rule: fork testing (2026-09-23) is a wave-level rule and does not direct this task; I will not
   disturb fork-battery state or claim anything about forks.
3. Standing ruling: pure-Zag red line scope (2026-09-23) applies: fixture provisioning counts as loop work, so the
   bounded search's candidate enumeration and any input generation are Zag-only.
4. Standing rule: shell-only byte checks (2026-09-30) applies: dash checks use
   docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh only, never python3.

Additional task-scoped governance: prereg strictly precedes implementation (merge-base verified); owned pathspec
commits only (docs/lab/research-lead/overnight-20260928/valley_satsuch/); never touch the contaminated research
paper; never remove a live .git/index.lock (wait and retry); the frozen V3 checker is an unmodified oracle.
