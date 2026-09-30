# Step 0: standing-rules name-check (2026-09-30, Law-Revert Adaptive Intervention Builder)

Read the standing-rules block at the top of LOOP_STATE.md before any work.

Rules applying to this task and how they will be honored:

1. PURE ZAG ONLY (owner red line): every artifact in this task (design doc,
implementation, build/run/verify scripts, case data) is pure Zag or POSIX
shell. No Python is authored, executed, or used for analysis at any step,
including byte checks. Fixture/case authoring is Zag-only.
2. Shell-only byte checks: em/en dash checks use
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
only, never python3.
3. Fork testing is a wave-level rule; this experiment runs on the shared
tnn-native-lab branch. I honor the shared-branch discipline with
owned-pathspec commits only
(docs/lab/research-lead/overnight-20260928/ddes_revert/), inspecting
git status before every commit, never staging other workers' files, never
touching the contaminated research paper
(TNN_RESEARCH_PAPER_20260929.md), and waiting/retrying on a live
.git/index.lock instead of removing it.
4. Image-judge rule: not applicable (no sensory work).

Name-check complete. Proceeding to prereg.
