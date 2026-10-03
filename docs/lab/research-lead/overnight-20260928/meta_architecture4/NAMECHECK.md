# NAMECHECK: MA4 (adversarial close-regimes red-team)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- Safebin contents: coreutils, git, awk, sed, grep, cmp, diff, sha256sum,
  znc, ...; no python3/python/perl/ruby/node.
- Toolchain smoke test: compiled and ran a trivial Zag program
  (`/tmp/ma4red/toolcheck/t.zag`) under safebin PATH; output `ok`,
  exit 0 (2026-10-03).
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, git operations, diff/grep
  audits.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/meta_architecture4/`
on branch `lane-ma4rt-fix-20261003` (worktree `/home/hatch/workspace/tnn-rsi`;
the original `lane-ma4redteam-20261003` was co-opted by other
workers and the worktree branch was externally switched to
`lane-ledgerreconcile-20261003` mid-task, so the implementation
was re-committed as b024ae99c on a clean branch cut from the
prereg commit 22cf677a4 to preserve B1 commit order).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: the first commit contains ONLY PREREG.md
(frozen) and NAMECHECK.md (Step 0 + this design record). The Zag
source, binary, run logs, and REPORT.md come in later commits, all
strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

MA4 answers the parent task: adversarial close-regimes red-team
of MA3's RDDM=10 redundancy proxy, the exact attack MA3's prereg
named as future work ("Distinct regimes closer than RDDM would
be conflated").

Architecture: MA3's UNCHANGED (prot, redun, victim rule,
RDDM=10 all frozen; not a redesign). Only the W stream changes
(W5 -> W6, adversarial): D identical; R={73..81} (mean 77);
B2={46..54} (mean 50); B4={78..86} (mean 82); B5={46..54}
(return). The R and B4 regimes are genuinely distinct by
construction, temporal separation (B2 intervenes), independent
demonstration (200+ / 50+ winner episodes each, both
protected), and disjoint histories, yet |77-82|=5 <= 10 so
the proxy conflates them. X/Y/Z replicate MA3 exactly
(expected byte-identical outputs, verified by cmp).

New harness-side tripwire (write-only, no learner feedback):
per-cell per-block winner tallies for W; at each W
redundancy-path reseed, ADVKILL increments iff the
victim/anchor dominant-block pair is {R, B4}. Predicted:
TRIGW n=4 (E14 U, E675 R, E735 U-or-R, E795 R); the E795
trigger reseeds the R-regime cell via the 82-cell anchor
(ADVKILL=1); BADRED=0 and PROTDEST=0 hold simultaneously,
separating "implementation correct" from "proxy wrong".

Predicted headline: INFORMATIVE-FAIL (proxy). If ADVKILL=0
with apparatus bars passing, the headline is PROXY-SURVIVES
with a diagnosis of why the adversarial event did not fire.

## Build record (post-prereg implementation, 2026-10-03)

- Implemented `ma4.zag` strictly after prereg commit
  22cf677a4 (no implementation file predates it).
- Changes vs MA3's `ma3.zag` (verified by diff): W-only
  tile changes (t9w={73..81} R, t9wb={46..54} B2,
  t9c={78..86} B4, t9d={46..54} B5), W value loop, W flip
  seed 20261026; new write-only harness code (wblk
  tallies, domblk/advpair helpers, ADVKILL); W metric
  targets (RWB2->50, RWB4->82, RWB5->50); MARG bands;
  B5f redefined (X/Y/Z + W-D-block); B9 >= 2; new B10;
  output (ADVKILL, B10, WBLK). Learner logic (selection,
  scoring, absorption, trigger, prot, redun, victim
  rule) byte-identical to MA3.
- B7: 29-word grep clean (0 hits; "regime"/"counts"/
  "learner" comment substrings found and reworded
  before compilation).
- Compiled with safebin znc (one A0101 warning on
  `etc_ep`, known false-positive class); ran 3x,
  byte-identical, sha256
  `c05f7924c6670e8e7038797e33f84a9d22e815793e3cd71a1165ec0a545b3812`.
- X/Y/Z sections and snapshots byte-identical to MA3's
  (cmp clean).
- Result: B10 FAIL (ADVKILL=0); audit confirms the
  proxy conflated the B4 and R regimes at the E795
  trigger (victim cell2, B4-model mean 83.4, via anchor
  cell3, R-model mean 78.3; unique B4 model destroyed).
  Tripwire flaw: lifetime dominant blocks misclassify
  the reseeded victim. Reported as B10-FAIL with
  positive red-team finding; bar not redefined.
  Recommended follow-up: MA4b with current-regime
  tripwire.
