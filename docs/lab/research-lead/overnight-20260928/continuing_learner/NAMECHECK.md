# Step 0 Name-Check: Continuing Learner Architect

Date: 2026-09-30. Worker: Continuing Learner Architect (subagent).
Task: design the ONE continuing learner architecture and freeze
PREREG_CLA1.md before any implementation.

Standing rules from the top of repo-root LOOP_STATE.md, and how
they are honored:

1. PURE ZAG ONLY (literal red line). This task is architecture
   design: pure markdown documents only. No code is written, no
   compiler or interpreter is invoked, no Python is used for any
   purpose at any step.

2. Shell-only byte checks. The dash check on the prereg documents
   runs via the shell-only
   worker_snippets/check_no_dash.sh snippet. python3 is never
   invoked.

3. Fork testing and the image-judge rule are not applicable to
   architecture design; no forks are created and no image work
   is performed.

4. Commits stay local on branch tnn-native-lab. Owned path only:
   docs/lab/research-lead/overnight-20260928/continuing_learner/.
   Explicit pathspecs on add and commit. git status inspected
   before staging. The contaminated paper
   (docs/lab/research-lead/overnight-20260928/
   TNN_RESEARCH_PAPER_20260929.md) is never opened, staged, or
   modified. If a live .git/index.lock is encountered, wait and
   retry; never remove it.

This name-check was written down before any design work began.
