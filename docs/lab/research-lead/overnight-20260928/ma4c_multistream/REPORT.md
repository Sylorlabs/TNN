# REPORT: MA4C-MULTISTREAM -- multi-stream validation of the K=3 proxy

## 0. Verdict

**MARGIN-FRAGILE**, with the preregistered **K-VARIES** implication.
K=3 discriminates the genuine/adversarial cases on W6 only. On all
four new tile-shuffle streams the discrimination breaks: T1/T2/T3 go
silent on the genuine B4-boundary case (ratios 3.21/3.02/3.18, all
above 3; the genuine redundancy is never consolidated), and T4 fires
on the adversarial B5-boundary case (ratio 2.57, below 3) and commits
a real kill (ADVKILL2=1, PAIR2 VC=3, the B4 model destroyed). No
integer K in 1..5 separates on all streams; on three streams NO K
separates at all (genuine and adversarial ratios identical); on the
fourth the ordering inverts. A frozen universal integer K is
disclaimed per the preregistered implication.

This does not overturn MA4c's PROXY-LEARNER-DRIVEN, which was scoped
to W6 with the explicit honest boundary that multi-stream validation
was required. This lane is that validation, and it returns negative.

## 1. The Bernoulli-seed incident (transparent disclosure)

The original PREREG.md defined streams by W Bernoulli seed
(20261026 -> 20261027..30). After building and running S1..S4 (all
3/3 byte-identical; ms_w6 audit-neutral vs frozen ma4c run1.txt), all
four returned BIT-IDENTICAL proxy tallies to W6 (E735: NUM=157731
DEN=53600 PCT=294; E795: NUM=7585 DEN=2220 PCT=341 on all five).
Root cause: the Bernoulli trials feed only etc_ep -> t, stored to a
write-only region never read by any decision; closed-loop dynamics
are functions of tile values only. The Bernoulli seed is causally
inert. S1..S4 are therefore vacuous for the margin question (five
copies of one trajectory) and are SUPERSEDED for all verdicts; their
files are kept as toolchain-validation artifacts. PREREG_AMEND.md
(committed as 14d136571 before any T-stream implementation)
re-froze the design on tile-shuffle streams T1..T4, which genuinely
vary the per-episode tile sequence within the frozen designed bands.

## 2. T-stream results (frozen K=3 closed loop, 3/3 byte-identical)

| stream | TRIGW | E735 (B4) | E795 (B5) | REDSEEDW | DECLW |
|---|---|---|---|---|---|
| W6 | E14:3U E735:2R E795:D | fire 2.94, reseed | silent 3.41, declined | 1 | 1 |
| T1 | E14:3U E675:D E735:D E795:D | silent 3.21, declined | silent 3.21, declined | 0 | 3 |
| T2 | E14:3U E675:D E735:D E795:D | silent 3.02, declined | silent 3.02, declined | 0 | 3 |
| T3 | E14:3U E675:D E735:D E795:D | silent 3.18, declined | silent 3.18, declined | 0 | 3 |
| T4 | E14:3U E675:D E735:2R E795:2R | fire 2.95, reseed | FIRE 2.57, RESEED (kill) | 2 | 1 |

All T streams show an extra E675 (B2-boundary) trigger absent on W6,
confirming the preregistered trigger-race fragility as a second,
independent instability. X/Y/Z byte-identical across all streams
(cmp clean sans banner); only W varies.

T4 kill evidence (MA4b's own tripwire): PAIR2 E795:2R VC=3 A3=2,
ADVKILL2=1, WBLKC2=`0 0 0 0 26` (cell 2 reseeded at E795; its ~45 B4
wins zeroed; B4 model destroyed). On W6 the same designed situation
was correctly declined (WBLKC2=`0 0 0 37 0`).

T1/T2/T3: the genuine R/R redundancy (cell 2 duplicated by cell 3,
both R models) is never consolidated (REDSEEDW=0); cell 3 absorbs
the B4 block alone (60 B4 wins on its R mean). No kill, no BADRED;
a missed consolidation, not a catastrophe.

## 3. Frozen bar results

- B1 COMMIT-ORDER: PASS. PREREG.md (a6a32a83c) predates ms_w6/ms_s*;
  PREREG_AMEND.md (14d136571) predates ms_t*.
- B2 TOOLCHAIN: PASS. safebin-only PATH, Step 0 in NAMECHECK.md,
  zero forbidden invocations.
- B3 DETERMINISM: PASS. 3/3 byte-identical per stream, all five.
  sha256: w6 a4a7d065..., t1 16843139..., t2 eaa876b5...,
  t3 99a29cac..., t4 cb6d95b9....
- B4 AUDIT-NEUTRALITY: PASS. ms_w6 minus MS/banner lines
  byte-identical to frozen ma4c run1.txt (cmp).
- B5 SCENARIO-VALIDITY: PASS on T1, T2, T3, T4 (B4-boundary trigger
  in [733,741] and B5-boundary trigger in [793,801] on each).
- B6 K3-DISCRIMINATION (PRIMARY): FAIL on all four. T1/T2/T3 fail
  clause (i) (E735: K3=0, declined; ratios 321/302/318). T4 passes
  (i) but fails clause (ii) (E795: K3=1, :2R reseed, kill).
- B7 OPAQUE-IDS: PASS. Whole-word case-insensitive grep for the
  frozen 29-word list empty in all ms_*.zag (same method as MA4c).
- B8 MARGIN-QUANTIFICATION: PASS (table below).
- B9 K3-STABILITY: FAIL (B6 fails on 4/4 testable new streams).

## 4. Margin quantification (B8)

MS min-pair PCTs (100 x ratio, integer; 300 = K=3 line). Min pair is
(VI=2, J=3) at every B4/B5 decision point on every stream.

| stream | GEN_PCT (E735) | vs 300 | ADV_PCT (E795) | vs 300 | sep-K in 1..5 |
|---|---|---|---|---|---|
| W6 | 294 | -6 (2.0%) | 341 | +41 | {3} |
| T1 | 321 | +21 | 321 | +21 | {} |
| T2 | 302 | +2 | 302 | +2 | {} |
| T3 | 318 | +18 | 318 | +18 | {} |
| T4 | 295 | -5 | 257 | -43 | {} |

Findings:
- Genuine-side stream swing is 294 -> 321 (27 points), over 4x the
  W6 margin (6 points). T2 misses K=3 by 0.7% (302 vs 300).
- T1/T2/T3: GEN_PCT == ADV_PCT exactly (the declined E735 leaves
  tallies frozen; the proxy sees identical ratios at both triggers).
  The ratio carries zero discriminative information there.
- T4: ordering inverts (adversarial 257 < genuine 295).
- Separating-K sets: {3}, {}, {}, {}, {}. Empty intersection.

Fixed probes at 0-indexed e=734/e=794 agree with the trigger audits
at the same episodes on every stream (T1 probes match T0 audits).

## 5. What K-varying implies for the proxy design

The preregistered implication is triggered: no single integer K
separates on all streams, so a frozen universal integer K is
disclaimed. The evidence goes further than "K varies": on 3/4
streams no threshold on this ratio can discriminate (identical
ratios), and on the fourth the genuine/adversarial ordering
inverts. This means the (R) ratio does not measure structural
redundancy; it measures contingent error overlap between the
anchor's mean trajectory and the victim's win episodes, which is
tile-sequence luck. The W6 separation (2.94 vs 3.42) was a property
of one tile order, not of the scenario.

Consequences for the design, in preregistered order:
- (a) Making K adaptive (set from experience) is insufficient
  where ratios coincide or invert; adaptivity cannot create
  information the ratio does not carry.
- (b) The fixed-K form must be replaced, not retuned: the proxy
  needs a structural signal for "anchor duplicates victim's role"
  that is stable under tile resampling (e.g. current-model
  comparison rather than historical error overlap), or the
  redundancy decision must be moved to a different mechanism.
- The (G) guard and (A) age conditions held on all streams; the
  failure is isolated to (R).

A second independent fragility is confirmed: the trigger pattern
itself is a seed-sensitive race (E675 triggers on all T streams,
absent on W6; W6's E735 won its race by ~1 episode per the design
record). Any future proxy work must treat trigger presentation as
unreliable, not just the K margin.

Note on T4 E675: the proxy fired for cell 2 (K3=1, C2=4) but the
victim rule correctly declined because cell 2 was winner/active
ineligible. The K-bit is necessary but not sufficient for a reseed;
victim eligibility gates independently. The proxy can deem the
currently-winning cell "redundant", a further design smell.

## 6. Honest boundaries

- Tile-shuffle streams resample tile order within frozen designed
  bands; they do not test other band designs.
- Four new streams is a small sample; the negative result
  (fragility) is established, but the full distribution of
  behaviors is not mapped.
- MA4c's W6 verdict stands as a single-stream demonstration; the
  generality claim it explicitly deferred is now tested and fails.
- What is measured are cell-mean tallies, as MA1-4. Not strategy
  invention, not L3.

## 7. Artifacts

- `ms_w6.zag` (+bin, 3 runs, sha256 a4a7d065...), `ms_t1..t4.zag`
  (+bins, 12 runs, sha256 above). T sources differ from W6 only by
  the re-shuffle block, TSEED, banner (diff-verified).
- `ms_s1..s4.zag` (+bins, 12 runs): SUPERSEDED Bernoulli-seed
  streams, kept as toolchain-validation artifacts (vacuity finding
  in PREREG_AMEND.md).
- `PREREG.md` (a6a32a83c), `PREREG_AMEND.md` (14d136571),
  `NAMECHECK.md`, this `REPORT.md`.
