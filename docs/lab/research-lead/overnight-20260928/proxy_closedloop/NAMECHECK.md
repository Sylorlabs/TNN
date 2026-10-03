# NAMECHECK: PROXY-CLOSEDLOOP (redun3 drives the closed loop)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- `which git` returns `/home/hatch/safebin/git`; git write ops invoked via
  the resolved `/usr/bin/git` path (the safebin git symlink has a known
  EPERM failure mode on object/index writes per the 2026-10-03 workspace
  lesson; same tool, resolved path).
- `which awk` returns `/home/hatch/safebin/awk` (used only for reading
  printed integers out of audit lines; no scientific computation).
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, cmp/diff/grep audits,
  git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/proxy_closedloop/`
on branch `tnn-native-lab` (worktree `/home/hatch/workspace/tnn-rsi-gpi3`).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: the prereg commit contains ONLY PREREG.md
and NAMECHECK.md (Step 0 + Step 1 + design record). The
implementation (cl_*.zag) strictly postdates it. No frozen kill bar
is evaluated before its prereg commit.

## Design record (pre-prereg; basis disclosed in PREREG.md)

PROXY-REDESIGN's frozen run files show redun3 firing on TWO cells at
the E735 trigger (kind=0, pre-reseed) on all 5 streams: P0=2 (cell 0,
anchor cell 1) and P2=4 (cell 2, anchor cell 3); P1=P3=0. K=3 fired
only on cell 2. The closed-loop victim-selection rule (path b:
lowest wpart among eligible firing cells) therefore selects cell 0
(wpart 9 < wpart ~200; cell 0 is never the anticipated cell or the
winner in the B4 block, so it is eligible), not K=3's cell 2. The
prereg freezes this predicted feedback-induced behavior change
(E735:0R on all streams) alongside the discrimination bars.

## Build record

(recorded after the prereg commit; implementation has not begun)
