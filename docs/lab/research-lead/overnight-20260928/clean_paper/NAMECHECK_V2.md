# NAMECHECK (second paper regeneration cycle)

Worker: Clean-Paper Regeneration Worker (second cycle).
Step 0 per the standing-rules block at the top of LOOP_STATE.md.

Applicable standing rules and how they will be honored:
1. PURE ZAG ONLY (2026-09-23): this task is pure markdown authorship; no
   code is written, no analysis is run, no Python will be used at any
   step. All hash/commit verification uses git and sha256sum/md5sum.
2. Shell-only byte checks (2026-09-30): em/en dash checks will use only
   docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
   No python3 for byte checks.
3. The contaminated internal log
   docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
   will never be edited, staged, or committed; zero diff verified at the end.
4. Provenance caution (2026-09-30 wave): shared-branch index races caused
   crossed commits. Every git add and git commit uses explicit pathspecs;
   git status --porcelain is inspected before each commit; a live
   .git/index.lock is waited on, never removed.
