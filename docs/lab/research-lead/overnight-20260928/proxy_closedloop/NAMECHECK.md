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

## Step 2: Build record (2026-10-03)

- Safebin PATH active; `which python3` returns nothing.
- Implementation: 5 files cl_w6.zag, cl_t1..t4.zag copied from
  proxy_redesign pr_*.zag; the ONLY functional changes (verified
  by diff) are: (1) victim path (b) uses redun3(G,cb,vi,e);
  (2)/(3) badred/protdest consistency checks use redun3(G,cb,v,e);
  (4) banner PROXY=redun3-CL. Header/comment wording updated.
  No new identifiers, functions, arena regions, or tallies.
- Built 5 binaries with safebin znc:
  - cl_w6.zag -> cl_w6_bin (194787 bytes)
  - cl_t1.zag -> cl_t1_bin (198898 bytes)
  - cl_t2.zag -> cl_t2_bin (198898 bytes)
  - cl_t3.zag -> cl_t3_bin (198898 bytes)
  - cl_t4.zag -> cl_t4_bin (198898 bytes)
- 3/3 runs byte-identical per stream (C3 PASS); sha256 recorded
  in REPORT.md.
- C4/C5/C6(i) PASS: E735 PX kind=0 shows P0=2,P1=0,P2=4,P3=0 and
  TRIGW shows E735:0R on all 5 streams, exactly as preregistered.
- C6(ii) PASS: BADRED=0 on all streams; no active-cell proxy kill.
- C7/C8/C9 PASS: REDUN3-CLOSEDLOOP-DISCRIMINATES.
