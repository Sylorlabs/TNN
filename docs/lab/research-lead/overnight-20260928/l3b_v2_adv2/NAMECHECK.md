# Name-check: L3B v2 Independent Adversary (Step 0)

Standing rules read from the top of LOOP_STATE.md (four sections):

1. **Standing owner rules (2026-09-23): PURE ZAG ONLY.** No Python anywhere in loop work: not glue, not analysis, not verifiers, not harnesses. I will implement the attack, worlds, diagnostics, and analysis in pure Zag plus shell utilities only. The IMAGE JUDGE clause is inapplicable (no image work).
2. **Standing owner rule: fork testing (2026-09-23).** Inapplicable in scope: this is a mechanism-level adversarial attack, not a wave with fork-testing duties. I will not enumerate forks.
3. **Standing ruling: pure-Zag red line scope (debate 2026-09-23).** Fixture provisioning counts as loop work, so all sealed-world fixtures and attack evidence are produced by Zag code, never Python.
4. **Standing rule: shell-only byte checks (2026-09-30).** Dash byte checks use the shell-only snippet docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh; never python3 for byte checks.

Additional rules from the task brief honored here: prereg committed ALONE before any attack implementation (K1, merge-base verified); explicit pathspecs on every git add/commit after git status inspection; no touch of docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md; live .git/index.lock is waited on, never removed; no em dashes in documentation; 3/3 byte-identical runs (K2/K3).
