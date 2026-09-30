# NAMECHECK: OpScope Behavioral-Validation Redesign Builder

**Date:** 2026-09-30 (PDT)

Standing rules from the top of `LOOP_STATE.md` and how this worker honors them:

1. **PURE ZAG ONLY (2026-09-23 owner red line):** All implementation, analysis, verification, and scratch work will be pure Zag plus shell builtins only. No Python anywhere, including no python3 heredoc placeholders and no Python byte checks. All analysis via grep/awk/sort/sha256sum.
2. **Shell-only byte checks (2026-09-30 standing rule):** Documents are checked for em/en dash bytes with `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh` only. The 2026-09-30 governance audit found most K4 violations were python3 byte checks; disclosure does not cure use, so I will not use python3 at all.
3. **Fork testing (2026-09-23 owner rule):** Not directly in scope for this builder (no new forks created); I keep commits local, never push, and keep my owned path isolated so the fork battery wave worker can test the tree cleanly.
4. **Pure-Zag red-line scope (2026-09-23 debate ruling):** Fixture provisioning and all loop work are Zag-only; any world-generation for test families is authored in Zag, never provisioned via other languages.

Additional loop disciplines: prereg committed ALONE before any implementation (strict `git merge-base --is-ancestor` check); explicit pathspecs on every `git add`/`git commit`; `git status --porcelain` inspected before each commit on this shared branch; never touch `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` (contaminated internal log, frozen); if a live `.git/index.lock` is hit, wait and retry, never remove it. Compiler rule: u8-backed cells only, never `as *i32` + `q[0..n]` slice construction inside functions (pinned znc miscompiles; see `~/AGENTS.md`).
