# NAMECHECK: MA4b (current-regime tripwire)

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
- Toolchain smoke test: compiled and ran a trivial Zag program
  (`/tmp/ma4b/toolcheck/t.zag`) under safebin PATH; output `ok`,
  exit 0 (2026-10-03).
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, cmp/diff/grep audits,
  git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/meta_architecture4b/`
on branch `lane-ma4b-20261003` (worktree `/home/hatch/workspace/tnn-rsi`).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: the first commit contains ONLY PREREG.md
(frozen) and NAMECHECK.md (Step 0 + this design record). The Zag
source, binary, run logs, and REPORT.md come in later commits, all
strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

MA4b answers the C460 recommendation: replace MA4's lifetime
dominant-block tripwire with a current-regime (post-reseed)
tripwire and test it on the same W6 adversarial stream.

Architecture: MA4's UNCHANGED (not a redesign). Learner logic
(selection, EMA scoring, absorption, consec>=3 trigger, prot,
redun, victim rule, RDDM=10) frozen; W6 stream, X/Y/Z, seeds
all frozen. Only harness-side audit code changes.

New harness state (write-only, no cell-state feedback):
- `wblkc[20]` at 3682260: post-reseed per-cell per-block winner
  tallies, same layout as wblk; incremented with wblk (W only);
  zeroed for cell v on every reseed of v (W only).
- `curdom(G,v)`: argmax over wblkc, ties -> lower index.
- `advpair2(G,cb,v,j,vcur)`: advpair with curdom for both cells.
- `advkill2` at 3682340; `pair2n` at 3682344; `pair2log[32]`
  at 3682348 (28 bytes/entry: ep, v, vcur, a0..a3).
- Old ADVKILL/domblk/advpair kept as the blind diagnostic.

Predicted: TRIGW n=3 (E14 U, E735 R, E795 R); ADVKILL=0;
PAIR2 E735: VC=1 A3=2 (no fire, genuine R/R redundancy);
PAIR2 E795: VC=3 A3=2 (fire, B4 victim via R anchor);
ADVKILL2=1 -> B10b PASS. X/Y/Z byte-identical to MA4's
run1.txt (cmp). WBLKC predicted: cell0 `9 0 0 0 0`,
cell1 `1 0 60 0 48`, cell2 `0 0 0 37 12`, cell3 `0 458 0 23 0`.

B7: the 29-word list grep must return empty in ma4b.zag; new
comments use "band" phrasing, never "regime" (and avoid
"rate"-containing substrings such as "separate"/"iterate"/
"demonstrated").

## Build record (post-prereg implementation, 2026-10-03)

- Implemented `ma4b.zag` strictly after prereg commit
  154e9fdd3 (no implementation file predates it).
- Changes vs MA4's `ma4.zag` (verified by diff): 147 added
  lines, all harness-side (wblkc tallies + zeroing on
  reseed, curdom/advpair2 helpers, advkill2 counter,
  pair2log audit, ADVKILL2/WBLKC/PAIR2/B10B output); the
  only removed lines are header comments and the output
  banner string ("MA4 SEEDB" -> "MA4b SEEDB"). Learner
  logic (selection, scoring, absorption, trigger, prot,
  redun, victim rule) byte-identical to MA4.
- B7: 29-word grep clean (0 hits).
- Compiled with safebin znc (one A0101 warning on
  `etc_ep`, known false-positive class); ran 3x,
  byte-identical, sha256
  `9d4f069dacfbdfe4c752e150875cc2dc3b3220d728a8f63dc3cd1412ea688934`.
- X/Y/Z episode sections, W episode lines, and all SNAP*
  snapshots byte-identical to MA4's run1.txt (cmp clean):
  the learner trajectory is provably unchanged.
- Result: B10b PASS (ADVKILL2=1; PAIR2 E735 VC=1 no fire,
  PAIR2 E795 VC=3 fire via A3=2). B10 stays 0, reproducing
  C460's lifetime-tripwire blindness on the same run.
- Two audit-string predictions missed (disclosed in
  REPORT.md, bars unaffected): PAIR2 E735 A3=0 (not 2;
  advpair2 logs only {1,3}-pairing anchors) and WBLKC2
  `0 0 0 0 12` (not `0 0 0 37 12`; the E795 reseed zeroes
  the victim's post-reseed tallies after the tripwire
  reads them).
