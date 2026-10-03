# NAMECHECK: LIFETIME-METALEARN-3 (cross-family lifetime learning)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- All scientific computation in this lane is pure Zag (znc-compiled binaries).
  Shell is used only for: file staging, znc invocation, binary execution,
  hashing, git operations.
- Zero invocations of python3, python, or any other forbidden executable.
  No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/lifetime_metalearn/`
on branch `tnn-native-lab`. Commits stay local with explicit pathspecs.
Commit order: the first commit contains ONLY PREREG.md and NAMECHECK.md
(Step 0 + this design record). The Zag source, binary, run logs, and
REPORT.md come in later commits, all strictly postdating the prereg
commit. Pushing to origin is authorized per Micah's 2026-10-03 PAT
authorization; push promptly, exclude build artifacts.

## Design record (pre-prereg, no frozen implementation run)

LM3 fills the Priority #8 gap (no active workers on lifetime/
meta-learning) and goes beyond lifetime_meta/2 (which tested
meta-learning WITHIN one bias-learning family): LM3 tests a continuing
learner across FIVE task families with conflict episodes, retention
probes, and an ablation control.

Pre-prereg design-phase work (all in /tmp and ~/workspace/scratch_lm3,
never in the lane; no frozen experiment executed):
- Pilot v1 (mechanism with histogram-fingerprint regime selection):
  revealed (a) an fm-string literal misalignment bug (families assigned
  to wrong episodes; caught by trial trace), (b) fingerprint merges
  causing silent regime pollution (compare merged into map regime),
  (c) evidence-based probe selection fragile under incomplete slot
  coverage.
- Pilot v2 (slot-evidence-only selection, first-encounter slot
  creation, min 64 trials): clean separation, 100% T probe accuracy,
  0 splits (backstop unneeded), 0 evictions. Meta-learning visible in
  fixed-episode errors (E03=19 -> E12=6), not in etc (first-encounter
  slots neutralize the prior for etc; disclosed in PREREG sec 7).
- Thresholds set from pilot with margins (PREREG sec 5). The frozen
  binary uses identical seeds/mechanism, so pilot values are the
  expected frozen values. This is power analysis, not seed selection:
  one frozen seed, reported honestly.

## Build record

(to be filled post-prereg)
