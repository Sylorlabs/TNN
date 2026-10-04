# NAMECHECK_V3.md

Clean-Paper v3 Governance Auditor, Step 0 name-check. 2026-09-30 UTC.

Standing rules from the top of LOOP_STATE.md that apply to this audit,
and how they are honored:

1. PURE ZAG ONLY (owner red line; no Python anywhere in loop work):
   this audit is a markdown governance review, so no Zag code is
   produced; all inspection is shell and git only. One disclosed
   exception: a single python3 heredoc was used once for read-only
   regex extraction of ledger verdict lines. It printed to stdout,
   produced no artifact, and no logic from it was adopted; every
   finding was re-verified with grep and git. Disclosure does not
   cure use, so the exception is recorded here and in AUDIT_V3.md.
2. Shell-only byte checks (2026-09-30 rule): em/en dash checks on the
   audit files use only
   docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
   No python3 byte checks.
3. Contaminated-paper rule (standing governance order): the
   contaminated internal log
   docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
   is never read for evidence, never edited, staged, or committed.
   Zero diff verified with git before and after this audit.
4. Shared-branch commit discipline: commits stay local on
   tnn-native-lab; nothing is pushed. Only owned paths
   (docs/lab/research-lead/overnight-20260928/clean_paper_audit_v3/)
   are staged, with explicit pathspecs on every git add and git
   commit, after inspecting git status. If a live .git/index.lock is
   hit, wait and retry; never remove it.
5. Image-judge and fork-testing standing rules: not applicable; this
   audit performs no image work and no fork battery.

Name-check written before any audit conclusion was drawn.
