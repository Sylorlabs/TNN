# NAMECHECK: MA2 (dormant-cell protection)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- `which git` returns `/home/hatch/safebin/git` (verified 2026-10-03).
- Safebin contents: coreutils, git, awk, sed, grep, cmp, diff, sha256sum,
  znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, git operations, diff/grep
  audits.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/meta_architecture2/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. Commit order: the first
commit contains ONLY PREREG.md (frozen) and NAMECHECK.md (Step 0 +
this design record). The Zag source, binary, run logs, and REPORT.md
come in later commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

MA2 answers the parent task: protect dormant cells with low
failure-score and a record of activity from MA1's naive victim rule,
without blocking legitimate reallocation.

Mechanism (frozen, PREREG.md Section 1): each cell adds (wpart, wpsm):
winner-episodes and summed prediction error over those episodes, both
from revealed values only. Protected iff wpart >= 5 and
wpsm/wpart <= 10 (PACT/PERR margins: distractor cell at T1 has
wpart = 9, mean win-error ~= 2; atypical spares have wpart <= 3).
Deliberately not recency-weighted: recency would unprotect dormant
cells during long blocks, which is exactly what the mechanism must
not do. Victim = highest score (ties: highest index) among
non-active, non-winner, unprotected cells. If none exists, the
reseed is declined (logged, consec reset); score selection then
reuses the dormant cell. Cell selection, EMA scoring, absorption,
and the consec>=3 trigger are unchanged from MA1.

Experiment: X/Y/Z replicate MA1 (same seeds 20261020..23, same
blocks); W adds D(12)+R(660)+B2(60)+R3(60) = 852 episodes, R3
reusing the Block-R tile (the 80 block returns), SEED_W=20261024.
X and W share block values over episodes 0..731, so their cell
trajectories are identical through E731 by construction.

Frozen predictions: T1 (X/W E14) victim = cell 3 (unprotected
atypical spare); distractor cell 0 protected and survives; R_X in
[4,64]. T2 (X/W E675) victim = an unprotected cell (predicted cell
1); protected 80-cells survive; R_XB2/R_WB2 <= 13; DECLX = 0. T3 (W
E735): case A (cell 2 earned protection) -> decline, DECLW >= 1,
dormant 80-cell reused; case B (cell 2 below bar) -> victim =
cell 2, TRIGW = 3. Both give R_W <= 15 and PROTDEST = 0. Kill bars:
B5a (1 <= R_X <= 99) and B8 (PROTDEST = 0).

Pre-prereg design-phase work (no frozen experiment executed): all
bounds and victim identities above were derived by hand from the
frozen update rules on MA1's disclosed streams (no code run); the
case-A/case-B branch is stream-dependent and both branches are
preregistered as bar-satisfying. No calibration Monte Carlo was run;
the bounds are mechanism-derived, not fitted.

## Build record

- 2026-10-03: `ma2.zag` written after the frozen prereg commit
  (1aebf8f). MA1's learner unchanged (selection, EMA 3/4 scoring,
  winner-absorbs, consec>=3 trigger) plus: per-cell (wpart, wpsm)
  tallies updated on winner absorbs from revealed values only;
  `prot()` predicate (wpart >= 5 and wpsm/wpart <= 10); victim =
  highest score (ties: highest index) among non-active, non-winner,
  unprotected cells; decline path (logged episode, victim marker,
  protection bitmask; consec reset) when no unprotected candidate
  exists; reseed resets wpart/wpsm. W condition: 852 episodes
  (D+R+B2+R3, R3 reusing the R tile), SEED_W=20261024. B7 audit:
  case-insensitive grep for the frozen 29-word list initially hit 2
  substrings ("demonstrated", "calibrated" contain "rate"); both
  comments reworded before compilation; final grep returns empty.
  Compiled with pinned safebin znc -> `ma2_bin`; one A0101 analyzer
  warning, the known false-positive class (max index
  fbase+e*1200+1199, in bounds).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `dfdd1e47a8fa7e5e9a1ec7211d0feb2910a90985ac4bef85cfcff80be4e54ea7`
  (run1/2/3.txt). Results: RX=7 RY=2 RZ=624 RXF=3 RXB2=4 RWB2=4
  RW=8 COSTXY=1022 COSTXZ=-3936; TRIGX n=2 (E14:3U F=1, E675:1U
  F=13), TRIGY n=0, TRIGW n=3 (E14:3U F=1, E675:1U F=13, E735:D
  F=15); DECLX=0 DECLY=0 DECLW=1; PROTDEST=0. All bars PASS
  (B5a..B5g, B8, DISTINCTD, PARID, XDISJ, MARG, GENFAIL). White-box:
  T1 victim cell 3 (unprotected spare), distractor cell (WP=9, mean
  win-error 5.33) survives; T2 victim cell 1 (unprotected), both
  80-cells survive, dormant distractor cell wins B2 episodes
  (N0 9->50); T3 declined (all 4 protected, F=15), dormant 80-cell
  reused at R3k=4, RW=8. X Block-R byte-identical to MA1; Y/Z
  byte-identical to MA1. Case A occurred as preregistered; case B
  did not arise.
- Commit order self-check: prereg (1aebf8f, PREREG.md + NAMECHECK.md
  Step 0 only) strictly predates this implementation commit. PASS
  (B1).

(pending: none)
