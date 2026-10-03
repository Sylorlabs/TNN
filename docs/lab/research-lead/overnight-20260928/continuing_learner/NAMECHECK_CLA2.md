# Step 0 Name-Check: LORG-to-CLA-1 Consolidation Architect

Date: 2026-09-30. Worker: LORG-to-CLA-1 Consolidation Architect (subagent).
Task: fold the LORG memory substrate ideas into the CLA-1 continuing
learner architecture as one consolidated prereg (CLA-2). Prereg only;
no implementation. Verdict label target: LORG-CONSOLIDATION-PREREG-COMPLETE.

Standing rules from the top of repo-root LOOP_STATE.md, and how
they are honored:

1. PURE ZAG ONLY (literal red line, per the 2026-09-30 tooling
   ruling). This task is architecture design: pure markdown
   documents only. No code is written, no compiler or interpreter
   is invoked, no Python/C/JS/Rust is used for any purpose at any
   step. Shell is used only for git operations, file moves, and
   the byte-level dash check.

2. Shell-only byte checks. The dash check on the prereg documents
   runs via the shell-only
   worker_snippets/check_no_dash.sh snippet. No scripting
   language is invoked.

3. Fork testing and the image-judge rule are not applicable to
   architecture design; no forks are created and no image work
   is performed.

4. Owned path only:
   docs/lab/research-lead/overnight-20260928/continuing_learner/.
   The contlearn2 files (PREREG_CONTLEARN2.md, contlearn2.zag,
   contlearn2_bin, CL2_*, build.err, run*.err) belong to another
   worker and are not opened, staged, or modified. Explicit
   pathspecs on add and commit. git status inspected before
   staging. The contaminated paper
   (docs/lab/research-lead/overnight-20260928/
   TNN_RESEARCH_PAPER_20260929.md) is never opened, staged, or
   modified; zero-diff is verified at commit time. If a live
   .git/index.lock is encountered, wait and retry; never remove it.

5. Micah's 2026-09-30 consolidation ruling governs the design:
   LORG must not become a separate permanent memory subsystem;
   CLA-1 is the primary architecture; utility evidence,
   dependency links, protection relationships, and regret/history
   enter as learned structural state in the generic
   learner-owned workspace, not as a separate memory engine.
   Q1/Q2/Q3 are addressed explicitly with falsifiable
   predictions in the prereg.

This name-check was written down before the consolidation prereg
was drafted.
