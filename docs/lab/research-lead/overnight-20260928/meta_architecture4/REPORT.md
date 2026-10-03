# REPORT: MA4 -- Adversarial close-regimes red-team of the RDDM=10 proxy

## Frozen verdict: B10 FAILS AS OPERATIONALIZED; PROXY BREAKS ON AUDIT

Per the frozen verdict mapping, B10 (ADVKILL=1) FAILS: ADVKILL=0.
B5a (kill bar) PASSED (R_X=7) and B9 PASSED (REDSEEDW=2 >= 2,
BADRED=0), with B1, B2, B3, B5b, B5c, B5d, B5e, B5f, B6, B7, B8
all PASS. Nothing was weakened or reinterpreted; no amendment
was made.

The frozen mapping's PROXY-SURVIVES headline for B10-FAIL does
not apply: audit of the trigger log, cell snapshots, and
per-block winner tallies shows the RDDM=10 proxy DID conflate
two genuinely distinct regimes at the E795 trigger, destroying
the unique B4 model. The frozen ADVKILL tripwire missed it
because its lifetime-dominant-block operationalization
misclassifies a reseeded cell (details below). The honest
verdict is therefore: **the proxy breaks under adversarial
close regimes (audit-confirmed); the preregistered B10
detector was insufficient to capture it.** This is reported
as a B10-FAIL with a positive red-team finding, not as a
B10-PASS: the bar is not retroactively redefined.

## What was built (pure Zag, safebin-only)

- `ma4.zag`: MA3's architecture UNCHANGED (cell selection,
  EMA scoring, absorption, consec>=3 trigger, prot(),
  redun(), victim rule (a)/(b)/(c), RDDM=10 all frozen;
  verified by diff against MA3's source: only the W
  stream, new harness-side audit code, metric targets,
  and output changed). New harness-side (write-only, no
  cell-state feedback): per-cell per-block winner tallies
  (wblk) for W and the ADVKILL tripwire (domblk/advpair
  helpers).
- W6 (852 episodes): D identical to MA3; R={73..81}
  (mean 77); B2={46..54} (mean 50); B4={78..86}
  (mean 82); B5={46..54} (return). |77-82|=5 <= 10.
  X/Y/Z replicate MA3 exactly (same tiles, same seeds).
- Commit order honored: prereg (22cf677a4, PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates
  implementation. This commit adds implementation +
  runs + report.
- Toolchain: PATH="$HOME/safebin" throughout;
  python3/python/perl/ruby/node all unresolvable; zero
  forbidden invocations. One znc analyzer warning
  (A0101 on `etc_ep`, the known false-positive class
  from MA1/MA2/MA3; max index is fbase+e*1200+1199,
  in bounds).
- Determinism: 3/3 runs byte-identical, sha256
  `c05f7924c6670e8e7038797e33f84a9d22e815793e3cd71a1165ec0a545b3812`.
- X/Y/Z sections and snapshots byte-identical to MA3's
  (verified by cmp): the mechanism is unchanged and the
  control holds.

## Results (frozen binary output, 3/3 identical)

```
RX=7 RY=2 RZ=624 RXF=3 RXB2=4 RWB2=6 RWB4=5 RWB5=9 COSTXY=1022 COSTXZ=-3936
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1 B8=1 B9=1 B10=0
DISTINCTD=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
TRIGW n=3 E14:3U F=1 E735:2R F=15 E795:2R F=15
DECLX n=0 DECLY n=0 DECLW n=0
REDSEEDX n=0 REDSEEDY n=0 REDSEEDW n=2 BADRED=0 ADVKILL=0
PROTDEST=0
WBLK0 9 0 0 0 0
WBLK1 1 0 60 0 48
WBLK2 1 202 0 37 12
WBLK3 1 458 0 23 0
SNAPWR S0=180 N0=9 C0=56 WP0=9 WQ0=48 S1=40 N1=1 C1=36 WP1=1 WQ1=10
       S2=14989 N2=203 C2=3 WP2=203 WQ2=268 S3=35962 N3=459 C3=1 WP3=458 WQ3=745
SNAPWB4 S0=180 N0=9 C0=59 WP0=9 WQ0=48 S1=3045 N1=61 C1=30 WP1=61 WQ1=167
       S2=3171 N2=38 C2=1 WP2=37 WQ2=60 S3=37790 N3=482 C3=2 WP3=481 WQ3=779
SNAPWB5 S0=180 N0=9 C0=28 WP0=9 WQ0=48 S1=5484 N1=109 C1=1 WP1=109 WQ1=265
       S2=604 N2=13 C2=2 WP2=12 WQ2=6 S3=37790 N3=482 C3=27 WP3=481 WQ3=779
```

Bar scorecard: B1 COMMIT-ORDER PASS; B2 TOOLCHAIN PASS;
B3 DETERMINISM PASS; B4 NOVELTY PASS; B5a PRIMARY PASS
(1 <= 7 <= 99); B5b PASS (624 >= 500); B5c PASS
(1022 < 4690); B5d PASS (1 <= 4 <= 30); B5e PASS; B5f PASS
(PARID=1 over X/Y/Z + W-D-block, XDISJ=1 over X/Y/Z);
B5g PASS (b5gok=3); B6 PASS (learner fns unchanged; wblk/
advkill/domblk are write-only harness code with no
feedback into cell state; 29-word grep clean); B7 PASS;
B8 PASS (PROTDEST=0); B9 PASS (2 >= 2, BADRED=0);
B10 FAIL (ADVKILL=0).

## Reading of the result

Three triggers, not the preregistered four. The B2-onset
trigger (predicted T2') did NOT fire: at 0-indexed e=674
the active R-absorber (mean 73) met a B2 value of 53,
error exactly 20, which is not > 20, resetting the consec
counter. The R absorbers (means 73.8, 78.3) sit only
~20-32 from B2 values, so the strict >20 trigger
threshold makes B2-onset triggering knife-edge. This is
a design deviation (documented, not hidden): the B2 block
was meant to separate R and B4 in time and supply the
50-model, and it did both (cell1 organically became the
50-model with 60 B2 wins, no reseed needed).

T1 (log E14): U-path, victim=cell3, as preregistered.
During R, the v14-split produced absorbers at 73.8
(cell2, 203 wins) and 78.3 (cell3, 458 wins), both
protected, matching the preregistered -3/+1.5 pattern.

T3' (log E735, B4 onset): R-path, victim=cell2 (the 73.8
absorber), redundant via cell3 (|73.8-78.3|=4.5 <= 10).
A correct proxy call: genuine R-duplicate reseeded as
the 82-model. During B4, cell2 became the B4 model
(mean 83.4, 37 wins, mean win-error 1.6, protected).

T4' (log E795, B5 onset): **the adversarial event.**
Active at trigger = cell3 (R model, mean 78.3; its score
undercut cell2's during the first two B5 episodes).
Winner = cell1 (50-model, err ~4). Candidates = {cell0
(D, mean 20), cell2 (B4 model, mean 83.4)}. cell2 is
redundant SOLELY via the cell3 anchor:
|83.4 - 78.3| = 5.1 <= RDDM=10. cell0 is unique
(nearest protected mean 50, distance 30). Victim =
cell2 -> reseeds as a second 50-model (SNAPWB5:
mean 46.5). **The unique B4-regime model is destroyed.**
After T4', no cell models {78..86}: cell0=D,
cell1=50-model, cell2=fresh 50-model, cell3=R-model.

The two conflated regimes are genuinely distinct by the
preregistered criteria: different generative tiles
({73..81} vs {78..86}), independent shuffles, temporal
separation by B2, independent demonstration (cell3: 458
R wins; cell2: 37 B4 wins, both protected with mean
win-error <= 10), disjoint demonstrated histories, and
no block labels reaching the cells. The proxy used only
mean distance (5.1 <= 10) and ignored all of it.
BADRED=0 and PROTDEST=0 hold simultaneously: the
implementation is correct; the proxy design is wrong.
This is exactly the failure mode MA3's prereg named.

## Why B10 missed it (tripwire flaw, disclosed)

The frozen ADVKILL operationalized "regime" as lifetime
argmax of per-block winner tallies. Victim cell2's
lifetime tallies are R=202, B4=37 (WBLK2), so its
dominant block is R(1); anchor cell3's is R(1); {1,1}
!= {1,3} -> no increment. But cell2's CURRENT regime
at the trigger was B4 (mean 83.4, learned from 37 B4
wins after its T3' reseed; its 202 R wins are
pre-reseed history). Lifetime tallies misclassify
reseeded cells. The {R,B4} pairing B10 was built to
detect DID occur (R-anchor cell3, B4-victim cell2);
the detector's regime operationalization was
insufficient. This flaw is in the tripwire, not the
proxy finding.

## Honest boundaries

- B10 FAILS as frozen; the INFORMATIVE-FAIL headline is
  NOT claimed via B10. The proxy-break finding rests on
  the trigger-log/snapshot/WBLK audit above, reported
  transparently as B10-FAIL-with-positive-finding rather
  than a retroactive bar redefinition.
- The T2' non-trigger is a design deviation: B2's
  {46..54} values sit at the trigger threshold's edge
  for R-absorber means. A follow-up should use a B2
  tile farther from R (or a longer separation) so the
  predicted four-trigger trajectory materializes.
- The adversarial event fired in the reverse direction
  from the preregistered prediction (B4-victim via
  R-anchor, not R-victim via B4-anchor); the proxy
  conflates symmetrically, as expected from a pure
  mean-distance measure.
- One W6 scenario, one frozen seed set; X/Y/Z seeds
  reused for comparability (byte-identical control
  verified).
- What is learned are cell means (L1/L2-ish), as
  MA1-3. RDDM=10 remains researcher-supplied; the
  red team attacked the proxy design, not the learner.

## Recommendation

MA4b follow-up with a re-frozen prereg: (1) current-
regime tripwire (post-reseed winner tallies, or
mean-nearest-block at trigger time) instead of lifetime
dominant block; (2) B2 tile moved farther from R so the
B2-onset trigger fires deterministically; (3) keep the
R/B4 close pair (|77-82|=5). The present run already
demonstrates the proxy breaks; MA4b would confirm it
under a frozen bar.

## Artifacts in this lane

- `ma4.zag`: frozen implementation (B6/B7 audited).
- `ma4_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  outputs (sha256
  `c05f7924c6670e8e7038797e33f84a9d22e815793e3cd71a1165ec0a545b3812`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record (Step 0 + build record).
