# NAMECHECK: MA3 (redundancy-aware victim choice)

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

Lane: `docs/lab/research-lead/overnight-20260928/meta_architecture3/`
on branch `tnn-native-lab` (worktree `/home/hatch/workspace/tnn-rsi-gpi3`).
Nothing is pushed to GitHub; commits stay local with explicit
pathspecs. Commit order: the first commit contains ONLY PREREG.md
(frozen) and NAMECHECK.md (Step 0 + this design record). The Zag
source, binary, run logs, and REPORT.md come in later commits, all
strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

MA3 answers the parent task: redundancy-aware victim choice. When
all candidates at a trigger are protected, the architecture must
distinguish redundant from unique knowledge instead of declining
indefinitely (MA2's honest boundary).

Mechanism (frozen, PREREG.md Section 1): dup(i,j) iff both cells
protected and |mean_i - mean_j| <= RDDM (RDDM=10, researcher
constant); cell i is REDUNDANT iff protected with a protected
duplicator (anchor may be any protected cell except i; must be
protected because a fresh cell's mean is one revealed value, not
demonstrated knowledge). Victim rule: (a) unprotected candidate
exists -> highest score, ties highest index (MA2's rule,
unchanged); (b) else redundant candidate exists -> lowest wpart,
ties highest score, ties highest index (keep the stronger
demonstration, reseed the weaker duplicate); (c) else decline
(MA2's rule, unchanged). Cell selection, EMA scoring, absorption,
trigger, and protection predicate unchanged from MA2.

Experiment: X/Y/Z replicate MA2 exactly (same seeds/blocks; new
rule never fires there; trajectories byte-identical by
construction). W replaced by W5: D(12) + R(660, {76..84}) +
B2(60, {16..24}) + B4(60, NEW {46..54}) + B5(60, NEW {91..99}) =
852 episodes, five distinct blocks, SEED_W5=20261025. W5's D/R/B2
tiles are drawn from the SEED_B stream in MA2's exact order, so
W5's values over 0..731 (and cell trajectory) match MA2's W
through E731.

Frozen predictions: T1 (X/W5 E14) U-path victim cell 3; T2
(X/W5 E675) U-path victim cell 1; T3 (W5 E734, B4 onset)
R-path: winner cell 2, candidates {1,3} both redundant, victim
cell 1 (WP ~19 < ~437); T4 (W5 E794, B5 onset) R-path: winner
cell 3, candidates {0 unique, 2 redundant}, victim cell 2 (the
discriminating case: redundant 80-duplicate chosen over the
unique distractor cell). REDSEEDW=2, BADRED=0, PROTDEST=0,
DECLW=0, R_WB4/R_WB5 <= 15. Kill bars: B5a (1 <= RX <= 99) and
B9 (REDSEEDW=2 AND BADRED=0).

Pre-prereg design-phase work (no frozen experiment executed): all
bounds, winner identities, and victim identities above were
derived by hand from the frozen update rules on MA2's disclosed
streams (no code run). No calibration Monte Carlo was run; the
bounds are mechanism-derived, not fitted.

## Build record

- 2026-10-03: `ma3.zag` written after the frozen prereg commit
  (7be552ca4). MA2's learner unchanged (selection, EMA 3/4 scoring,
  winner-absorbs, consec>=3 trigger, prot() predicate) plus: new
  `redun()` predicate (protected cell with a protected duplicator
  within RDDM=10 of its mean, from revealed values only); victim
  rule gains the redundancy sub-path (no unprotected candidate ->
  redundant candidate with lowest wpart, ties highest score, ties
  highest index; else decline as in MA2); trigger log path markers
  U/R/D/X; new tallies REDSEEDW (redundancy reseeds) and BADRED
  (in-binary tripwire: redundancy victim failing the predicate);
  PROTDEST now counts only protected-UNIQUE victims. W5 condition:
  852 episodes (D+R+B2+B4+B5; B4 = NEW tiled {46..54}, B5 = NEW
  tiled {91..99}), SEED_W5=20261025; D/R/B2 tiles drawn from the
  SEED_B stream in MA2's exact order so W5 values over 0..731 match
  MA2's W and X. B7 audit: case-insensitive grep for the frozen
  29-word list in ma3.zag returns empty (no hits at all). B6 audit:
  e==/cond== hooks are write-only snapshots (snap/b5gok) with no
  feedback into cell state; learner logic reads only revealed
  values and derived tallies. Compiled with pinned safebin znc ->
  `ma3_bin`; one A0101 analyzer warning, the known false-positive
  class (max index fbase+e*1200+1199, in bounds).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `5217cb95af51b7c656df1581e8720109fc811717c5297cc58005515e90d4dec8`
  (run1/2/3.txt). Results: RX=7 RY=2 RZ=624 RXF=3 RXB2=4 RWB2=4
  RWB4=5 RWB5=6 COSTXY=1022 COSTXZ=-3936; TRIGX n=2 (E14:3U F=1,
  E675:1U F=13), TRIGY n=0, TRIGW n=4 (E14:3U F=1, E675:1U F=13,
  E735:1R F=15, E795:2R F=15); DECLX=0 DECLY=0 DECLW=0;
  REDSEEDX=0 REDSEEDY=0 REDSEEDW=2; BADRED=0; PROTDEST=0. All bars
  PASS (B5a..B5g, B8, B9, DISTINCTD, PARID, XDISJ, MARG, GENFAIL).
  White-box: T3 victim cell 1 (redundant via cell 0, |17-21|=4;
  lowest wpart 19 < 437); T4 victim cell 2 (redundant via cell 3,
  |76-81|=5; unique cell 0, nearest protected mean 28 away,
  survived). X/Y/Z outputs byte-identical to MA2's (cmp
  verified). Label note: prereg T3/T4 labels E734/E794 were
  0-indexed episode numbers; the log prints 1-indexed (E735/E795);
  both denote the mechanism-derived trigger points (B4k=3/B5k=3).
- Commit order self-check: prereg (7be552ca4, PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates this implementation
  commit. PASS (B1).

(pending: none)

## Commit order self-check

PASS (B1): prereg commit 7be552ca4 contains only PREREG.md and
NAMECHECK.md (Step 0 + design record) and strictly predates the
implementation commit below.
