# PREREG: MA4b -- Current-regime tripwire for the MA4 adversarial stream

## 0. Standing

MA4-REDTEAM (C460) proved the RDDM=10 mean-distance proxy breaks:
close bands (tile means 77/82, distance 5 <= 10) get conflated, and
the unique B4-model (cell2, mean 83.4, 37 post-reseed wins) was
destroyed at the E795 trigger by a redundancy-path reseed anchored
on the R-model (cell3, mean 78.3). The frozen B10 tripwire missed
the kill (ADVKILL=0) because it operationalized a cell's band as
its LIFETIME dominant winner block: victim cell2's lifetime
tallies (R=202, B4=37) classify it as band 1, but its CURRENT band
at the trigger was B4, learned after its T3' reseed. The red-team
verdict was reported honestly as B10-FAIL with a positive
audit finding, and the recommended follow-up is a current-regime
tripwire. This prereg freezes that follow-up.

MA4b changes NOTHING about the learner or the stream: MA4's
architecture (cell selection, EMA scoring, absorption,
consec>=3 trigger, prot(), redun(), victim rule (a)/(b)/(c),
RDDM=10) and the W6 adversarial stream (D, R={73..81}, B2={46..54},
B4={78..86}, B5={46..54}; SEED_W6=20261026) and X/Y/Z are all
frozen exactly as in MA4. Only the harness-side tripwire changes:
lifetime dominant block -> current (post-reseed) dominant block.

Nothing in this prereg weakens any frozen bar. All thresholds
below are frozen before implementation.

## 1. Current-regime tripwire design (frozen, harness-side only)

New write-only harness state (no feedback into cell state, same
status as MA4's wblk/snapshots):

- `wblkc[20]`: per-cell per-block POST-RESEED winner tallies
  (cell-major, same 5-block layout as wblk: 0=D,1=R,2=B2,3=B4,4=B5).
  Incremented on exactly the same events as wblk (W winner of
  episode e in block blk). ZEROED for cell v whenever v is reseeded
  (U-path and R-path alike; any reseed starts a new current band),
  alongside the existing cell-state reset.
- `curdom(G,v)`: argmax over wblkc, ties -> lower index. A cell's
  current band is the block it has won most SINCE ITS LAST RESEED.
  Never-reseeded cells use lifetime tallies (identical to wblk
  until the first reseed), which is correct: with no reseed
  boundary, the whole history is the current band. Protection
  implies wpart >= 5 since the last reseed, so curdom is always
  well-defined for victims and anchors.
- `advpair2(G,cb,v,j,vcur)`: identical to MA4's advpair except
  both victim and anchor bands come from curdom (post-reseed)
  instead of domblk (lifetime).
- `advkill2`: incremented at each W redundancy-path reseed iff
  the CURRENT-band pair {vcur, anchor curdom} is {1, 3}.
- `pair2log`: per-W-R-path-reseed audit record (episode e+1,
  victim v, vcur, and per-anchor j its curdom+1, 0 if j is not a
  qualifying anchor), printed as PAIR2 lines.

The old tripwire (ADVKILL/B10, lifetime) is KEPT as a diagnostic:
it must reproduce MA4's result (ADVKILL=0), proving the new
tripwire is tested against the same blind detector that failed.

## 2. Experimental protocol (frozen harness)

X/Y/Z: MA4 exactly (same tiles, same seeds). Expected
byte-identical to MA4's run outputs (verified by cmp).

W6: MA4 exactly (same tiles, same order, SEED_W6=20261026).
The learner trajectory must be identical to MA4's: the only
new arena writes are harness-side.

## 3. Frozen metrics

All MA4 metrics carried over unchanged (RX, RY, RZ, RXF, RXB2,
RWB2/RWB4/RWB5, COSTXY, COSTXZ, TRIGX/Y/W, DECLX/Y/W,
REDSEEDX/Y/W, BADRED, PROTDEST, ADVKILL, WBLK, SNAP*, B5A..B10,
DISTINCTD, PARID, XDISJ, MARG, GENFAIL), plus:

- ADVKILL2 (advkill2 counter).
- PAIR2 audit lines, one per W redundancy-path reseed:
  `PAIR2 E<ep>:<v>R VC=<vcur> A0=<a0> A1=<a1> A2=<a2> A3=<a3>`
  (A<j> = anchor j's curdom+1, 0 if j not a qualifying anchor).
- WBLKC lines (post-reseed tallies at run end, 4 cells x 5 blocks).
- B10B bar bit (computed in-binary from advkill2).

## 4. Mechanism-derived predictions (frozen)

Trajectory identical to MA4 (mechanism unchanged):

- TRIGW n=3: E14 (U-path, v=3), E735 (R-path, v=2), E795
  (R-path, v=2). REDSEEDW=2, BADRED=0, PROTDEST=0, DECLW=0.
- ADVKILL=0 (old lifetime tripwire still blind; reproduces C460).
- PAIR2 at E735: victim cell2 was never reseeded; its
  post-reseed tallies are its lifetime tallies, R-dominant
  (202 R wins, 0 B4 wins at that point) -> VC=1. Anchor cell3
  was reseeded at E14; post-reseed: ~458 R wins vs ~2-3 B4
  wins -> curdom 1 -> A3=2. Pair {1,1}: no fire (correct: the
  E735 reseed paired two genuine R duplicates).
- PAIR2 at E795: victim cell2 was reseeded at E735; post-reseed
  tallies: 37 B4 wins, 0 B5 wins at trigger -> VC=3. Anchor
  cell3 post-reseed (since E14): R=458 vs B4=23 -> curdom 1 ->
  A3=2. Pair {3,1}: FIRE -> ADVKILL2=1.
- WBLKC at run end (predicted): cell0 `9 0 0 0 0` (never
  reseeded); cell1 `1 0 60 0 48` (never reseeded); cell2
  `0 0 0 37 12` (reseeded at E735); cell3 `0 458 0 23 0`
  (reseeded at E14).
- X/Y/Z sections and snapshots byte-identical to MA4's
  run1.txt (cmp).

## 5. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates every
  implementation commit.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout,
  Step 0 recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical
  (sha256 recorded).
- B4 NOVELTY: PASS iff MA4's bands hold (W tiles unchanged;
  same ones-fraction bands as MA4).
- B5a RECOVERY (kill bar): PASS iff 1 <= R_X <= 99.
- B5b BASELINE-REPLICATION: PASS iff R_Z >= 500.
- B5c COST: PASS iff COST_XY < 4690.
- B5d SHIFT-BACK: PASS iff 1 <= R_XB2 <= 30.
- B5e APPARATUS: PASS iff max etc <= 1200 and genfail=0.
- B5f STREAM-VALIDITY: PASS iff PARID=1 over X/Y/Z and
  W-vs-X over the D block (e<12), and XDISJ=1 over X/Y/Z
  (as MA4).
- B5g MANIPULATION: PASS iff b5gok=3.
- B6 NO-RESEARCHER-RULE: PASS iff learner fns read only
  revealed values and derived tallies; wblkc/curdom/
  advpair2/advkill2/pair2log are write-only harness hooks
  with no feedback into cell state (audit by diff vs
  MA4's ma4.zag: learner logic byte-identical; grep).
- B7 OPAQUE-IDS: PASS iff episode labels are E0001.. and
  case-insensitive grep for the frozen 29-word list
  (coin, bias, heads, tails, shrink, prior, learn, meta,
  cluster, outlier, typical, atypical, general, poisson,
  rate, lambda, gauss, count, event, slot, family,
  distractor, shift, phase, regime, original, interference,
  recover) in ma4b.zag returns empty.
- B8 NO-UNIQUE-DESTRUCTION: PASS iff PROTDEST=0.
- B9 REDUNDANCY-PATH (kill bar): PASS iff REDSEEDW >= 2
  AND BADRED=0.
- B10 ADVERSARIAL-KILL-LIFETIME (diagnostic, carried): expected
  0, reproducing C460's B10-FAIL. NOT the headline bar.
- B10b ADVERSARIAL-KILL-CURRENT (PRIMARY, kill bar): PASS iff
  ADVKILL2=1 AND the PAIR2 audit shows VC=1 (no fire) at the
  E735 reseed AND VC=3 (fire) at the E795 reseed.

Headline verdict: TRIPWIRE-FIXED iff B10b PASS with B5a PASS,
B9 PASS, and B1, B2, B3, B5b, B5c, B5d, B5e, B5f, B6, B7, B8
all PASS: the current-regime tripwire correctly identifies
the red-team kill (E795 conflation of the B4 and R bands)
that the lifetime tripwire missed, while correctly staying
silent on the genuine redundancy at E735.

If B10b FAILS with the apparatus bars PASS, the headline is
TRIPWIRE-INSUFFICIENT: the report must diagnose which
preregistered prediction broke (wrong trajectory, VC
misclassification, or pair logic) and must NOT reinterpret
the bar.

## 6. Honest boundaries (frozen)

- What is learned are cell means (L1/L2-ish), as MA1-4. Not
  strategy invention, not L3. RDDM=10 remains
  researcher-supplied; this lane repairs the DETECTOR, not
  the proxy.
- The E735/E795 trigger identities and PAIR2 values are
  predicted from MA4's observed trajectory; the mechanism is
  unchanged, so any deviation is a finding about the
  implementation, not the stream.
- One W6 scenario, one frozen seed set; X/Y/Z seeds reused
  for direct comparability (byte-identical control).
- curdom uses winner tallies since the last reseed; a cell
  reseeded twice within one block accumulates both
  sub-histories. In W6 no cell is reseeded twice, so this
  boundary is disclosed but untested.

## 7. Artifacts planned

- `ma4b.zag`: frozen implementation (B6/B7 audited; learner
  logic byte-identical to MA4's ma4.zag by diff).
- `ma4b_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  outputs.
- `REPORT.md`: results and frozen verdict.
- `NAMECHECK.md`: build record (Step 0 + build record).
