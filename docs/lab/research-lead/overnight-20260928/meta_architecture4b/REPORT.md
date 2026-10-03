# REPORT: MA4b -- Current-regime tripwire on the MA4 adversarial stream

## Frozen verdict: TRIPWIRE-FIXED

Per the frozen verdict mapping, B10b (ADVKILL2=1 with
PAIR2 VC=1 at E735 and VC=3 at E795) PASSES. B5a (kill bar)
PASSED (R_X=7) and B9 PASSED (REDSEEDW=2 >= 2, BADRED=0),
with B1, B2, B3, B5b, B5c, B5d, B5e, B5f, B6, B7, B8 all
PASS. Nothing was weakened or reinterpreted; no amendment
was made.

The current-regime tripwire fires exactly on the red-team
kill (the E795 conflation of the B4 and R bands) and stays
silent on the genuine redundancy at E735. The old lifetime
tripwire (B10/ADVKILL=0) reproduces C460's blindness on the
same run, confirming the new detector is tested against the
same stream that defeated its predecessor.

## What was built (pure Zag, safebin-only)

- `ma4b.zag`: MA4's architecture UNCHANGED (cell selection,
  EMA scoring, absorption, consec>=3 trigger, prot(),
  redun(), victim rule (a)/(b)/(c), RDDM=10 all frozen;
  verified by diff against MA4's source: 147 added lines,
  all harness-side; the only removed lines are header
  comments and the "MA4 SEEDB" banner string). W6 stream,
  X/Y/Z, seeds all frozen as MA4.
- New harness-side (write-only, no cell-state feedback):
  `wblkc[20]` post-reseed per-cell per-block winner tallies
  (zeroed for cell v on every reseed of v, W only);
  `curdom()` argmax over post-reseed tallies (ties -> lower
  index); `advpair2()` (advpair with curdom for both cells);
  `advkill2` counter; `pair2log` per-R-path-reseed audit.
- Commit order honored: prereg (154e9fdd3, PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates
  implementation. This commit adds implementation + runs +
  report.
- Toolchain: PATH="$HOME/safebin" throughout;
  python3/python/perl/ruby/node all unresolvable; zero
  forbidden invocations. One znc analyzer warning
  (A0101 on `etc_ep`, the known false-positive class from
  MA1/MA2/MA3/MA4; max index is fbase+e*1200+1199,
  in bounds).
- Determinism: 3/3 runs byte-identical, sha256
  `9d4f069dacfbdfe4c752e150875cc2dc3b3220d728a8f63dc3cd1412ea688934`.
- Learner trajectory provably unchanged: X/Y/Z episode
  sections, W episode lines, and all SNAP* snapshots are
  byte-identical to MA4's run1.txt (verified by cmp).

## Results (frozen binary output, 3/3 identical)

```
TRIGW n=3 E14:3U F=1 E735:2R F=15 E795:2R F=15
PAIR2 n=2
PAIR2 E735:2R VC=1 A0=0 A1=0 A2=0 A3=0
PAIR2 E795:2R VC=3 A0=0 A1=0 A2=0 A3=2
REDSEEDX n=0 REDSEEDY n=0 REDSEEDW n=2 BADRED=0 ADVKILL=0 ADVKILL2=1
PROTDEST=0
WBLK0 9 0 0 0 0
WBLK1 1 0 60 0 48
WBLK2 1 202 0 37 12
WBLK3 1 458 0 23 0
WBLKC0 9 0 0 0 0
WBLKC1 1 0 60 0 48
WBLKC2 0 0 0 0 12
WBLKC3 0 458 0 23 0
RX=7 RY=2 RZ=624 RXF=3 RXB2=4 RWB2=6 RWB4=5 RWB5=9 COSTXY=1022 COSTXZ=-3936
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1 B8=1 B9=1 B10=0 B10B=1
DISTINCTD=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
```

Bar scorecard: B1 COMMIT-ORDER PASS; B2 TOOLCHAIN PASS;
B3 DETERMINISM PASS; B4 NOVELTY PASS (W tiles unchanged from
MA4); B5a PRIMARY PASS (1 <= 7 <= 99); B5b PASS (624 >= 500);
B5c PASS (1022 < 4690); B5d PASS (1 <= 4 <= 30); B5e PASS
(GENFAIL=0, apparatus unchanged); B5f PASS (PARID=1,
XDISJ=1); B5g PASS (b5gok=3); B6 PASS (learner fns
byte-identical to MA4 by diff; wblkc/curdom/advpair2/
advkill2/pair2log are write-only harness hooks; 29-word
grep clean); B7 PASS; B8 PASS (PROTDEST=0); B9 PASS
(2 >= 2, BADRED=0); B10 diagnostic 0 (reproduces C460);
B10b PRIMARY PASS (ADVKILL2=1, PAIR2 VC=1 at E735,
VC=3 at E795).

## Reading of the result

The key question was whether a current-regime tripwire
correctly identifies the red-team kill. It does, on both
sides:

FIRE (E795): victim cell2's post-reseed tallies are 37 B4
wins (its B4 model, built after the E735 reseed) -> VC=3;
anchor cell3's post-reseed tallies are R=458 vs B4=23 ->
curdom 1 -> A3=2. The {3,1} pair fires ADVKILL2. The
tripwire reads the tallies BEFORE the reseed zeroes them,
so the destroyed B4 model's current band is captured.

NO FIRE (E735): victim cell2 was never reseeded; its
post-reseed tallies are its lifetime tallies, R-dominant
(202 R wins, 0 B4) -> VC=1. Anchor cell3 (reseeded at E14)
is post-reseed R-dominant -> no {1,3} pair -> A3=0, no
fire. The genuine R/R redundancy is correctly passed over.

The old lifetime tripwire stays blind on the identical
trajectory (ADVKILL=0): victim cell2's lifetime tallies
(R=202, B4=37) still classify it as band 1. Same stream,
same kill, one detector sees it and the other does not.

## Honest boundaries

- Two preregistered AUDIT STRING predictions were wrong;
  neither touches a frozen bar, and both are disclosed
  rather than amended:
  (1) PAIR2 E735 was predicted `A3=2`, observed `A3=0`:
  advpair2 logs only anchors forming a {1,3} current-band
  pair; at E735 the anchor's current band is R (pair
  {1,1}), so no adversarial anchor is logged. The
  prereg's own prose ("Pair {1,1}: no fire") matches the
  observation; the predicted string was the error.
  (2) WBLKC2 was predicted `0 0 0 37 12`, observed
  `0 0 0 0 12`: the E795 reseed zeroes the victim's
  post-reseed tallies after the tripwire fires, so the
  run-end tally holds only the 12 B5 wins; the 37 B4
  wins are the destroyed model's pre-reseed history,
  which is exactly the knowledge the proxy destroyed.
- B10b's frozen conditions (ADVKILL2=1, VC(E735)=1,
  VC(E795)=3) are met exactly as predicted; no bar was
  reinterpreted to accommodate the audit-string slips.
- This lane repairs the DETECTOR, not the proxy: RDDM=10
  remains researcher-supplied, and the architecture still
  destroys the B4 model. The kill is now visible to a
  frozen bar.
- One W6 scenario, one frozen seed set; X/Y/Z seeds reused
  for direct comparability (byte-identical control
  verified).
- curdom's never-reseeded-cells-use-lifetime rule and the
  twice-reseeded-in-one-block boundary are disclosed in
  the prereg; W6 exercises only the former.

## Artifacts in this lane

- `ma4b.zag`: frozen implementation (B6/B7 audited; learner
  logic byte-identical to MA4's ma4.zag by diff).
- `ma4b_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  outputs (sha256
  `9d4f069dacfbdfe4c752e150875cc2dc3b3220d728a8f63dc3cd1412ea688934`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record (Step 0 + build record).
