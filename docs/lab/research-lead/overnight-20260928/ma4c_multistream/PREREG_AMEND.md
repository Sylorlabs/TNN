# PREREG_AMEND: MA4C-MULTISTREAM -- stream-definition correction (frozen)

## 0. Standing

This amendment is committed BEFORE any tile-shuffle implementation.
It transparently corrects the stream definition in PREREG.md (committed
as a6a32a83c). No bar is weakened; the correction strengthens the
test. The original design's Bernoulli-seed streams are disclosed as
vacuous below and superseded for the margin question.

## 1. What was found (evidence, no new mechanism)

After building ms_w6/ms_s1..ms_s4 per PREREG.md and running 3x each
(all 3/3 byte-identical; ms_w6 audit-neutral vs frozen ma4c run1.txt),
the four "new streams" returned BIT-IDENTICAL proxy tallies to W6:

- MS E735: NUM=157731 DEN=53600 PCT=294 on W6, S1, S2, S3, S4.
- MS E795: NUM=7585 DEN=2220 PCT=341 on W6, S1, S2, S3, S4.
- TRIGW/PROXYC/REDSEEDW/DECLW identical; run files differ ONLY in the
  banner line and the printed EW (examples-to-criterion) values.

Root cause (code inspection): the W Bernoulli trials feed ONLY
`etc_ep` -> `t`, stored to eoff which is write-only and never read
back by any decision. The closed-loop dynamics (winners, errors,
scores, triggers, reseeds, xerr/xcnt/wpart/wpsm) are functions of the
TILE VALUES only. Varying the Bernoulli seed varies nothing the
proxy measures. The S1..S4 streams are therefore vacuous for the
margin question: five copies of one trajectory, not five streams.

The S1..S4 artifacts are kept (toolchain-validation value only:
they confirm determinism and audit-neutrality replicate) and
SUPERSEDED for all margin/discriminination verdicts.

## 2. Amended stream definition (frozen)

Five W streams: W6 (frozen baseline, no change) and T1..T4.
T1..T4 = ms_w6.zag PLUS a per-stream re-shuffle of the four W tile
sets (t9w 73-81, t9wb 46-54, t9c 78-86, t9d 46-54) inserted in gen()
after the frozen shuffles: `s64(G,0,TSEED)` then Fisher-Yates
re-permutation of each set (same swap pattern as the frozen code).
TSEED: T1=20261027, T2=20261028, T3=20261029, T4=20261030.

What this preserves / varies:
- Preserved: designed bands (same value sets per block), X/Y/Z/D
  tiles and seeds (re-shuffle is s64-scoped to W sets only;
  downstream s64 resets contain the rnd consumption), mechanism
  logic, K=3, MS audit, probes.
- Varied: the per-episode W tile SEQUENCE within each band, which
  is what actually drives winners, errors, tallies, triggers, and
  the proxy ratios. These are genuine distinct realizations of the
  designed scenario.

Control prediction: E14 (D block, tiles frozen) must show identical
MS (PCT=460, K3=0) on all five streams; E735/E795 tallies must now
DIFFER across streams (else the re-shuffle is itself inert and the
amendment fails its own check).

## 3. Bars (unchanged in logic; "stream" now reads T1..T4)

B1 COMMIT-ORDER: this amendment committed strictly before any
ms_t*.zag. (Original B1 still holds for PREREG.md vs ms_w6/ms_s*.)
B2 TOOLCHAIN, B3 DETERMINISM (3/3 per T stream), B4 AUDIT-NEUTRALITY
(already PASS on ms_w6; T streams inherit the identical audit code),
B5 SCENARIO-VALIDITY, B6 K3-DISCRIMINATION (PRIMARY), B7 OPAQUE-IDS
(re-run on ms_t*.zag), B8 MARGIN-QUANTIFICATION, B9 K3-STABILITY:
all as PREREG.md section 4, with S1..S4 replaced by T1..T4.

Headline verdicts (K3-ROBUST / MARGIN-FRAGILE / K-VARIES implication)
as PREREG.md section 4.

## 4. Honest boundaries (added)

- The Bernoulli-seed incident is a design error caught by the
  experiment's own audit before any verdict: reported, not hidden.
- Tile-shuffle streams test margin stability under tile-sequence
  resampling within the frozen designed bands; they do not test
  other band designs (separate experiment).
- Four new streams remains a small sample.

## 5. Artifacts planned (added)

- `ms_t1.zag` .. `ms_t4.zag`, four binaries, 12 run files
  (sha256 recorded); this amendment; REPORT.md (covering both the
  vacuity finding and the T-stream verdicts).
