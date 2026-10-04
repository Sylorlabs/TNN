# Step 0 Name-Check: Learner-State ACT Prereg Architect

Date: 2026-09-30. Worker: Learner-State ACT Prereg Architect (subagent).
Task: preregister the design for ACT as a generic operation that
consults learner-created state (the architectural answer to Cluster D,
no agentic action machinery), and freeze PREREG_ACT.md before any
implementation.

Standing rules from the top of repo-root LOOP_STATE.md, and how
they are honored:

1. PURE ZAG ONLY (literal red line). This task is architecture
   design: pure markdown documents only. No code is written, no
   compiler or interpreter is invoked, no Python is used for any
   purpose at any step. No Python, C, JavaScript, Rust, or any
   other language implements any research logic; shell exists
   only to sequence file operations and git.

2. Shell-only byte checks. The dash check on the prereg documents
   runs via a shell-only byte grep. python3 is never invoked.

3. Fork testing and the image-judge rule are not applicable to
   architecture design; no forks are created and no image work
   is performed.

4. Commits stay local on branch tnn-native-lab. Owned path only:
   docs/lab/research-lead/overnight-20260928/learner_act/.
   Explicit pathspecs on add and commit. git status inspected
   before staging. The contaminated paper
   (docs/lab/research-lead/overnight-20260928/
   TNN_RESEARCH_PAPER_20260929.md) is never opened, staged, or
   modified. If a live .git/index.lock is encountered, wait and
   retry; never remove it.

This name-check was written down before any design work began.
