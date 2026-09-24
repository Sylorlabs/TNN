# VERDICT — M1 Threshold Adoption: Held-Out Wrongs at Long Horizon
### (PAM Round 4, Gov-LH Crew 4)

**Date:** 2026-09-24. **Prereg:** `PREREG_M1_GOVLH.md`
(committed alone: `1f6d190c0538c42c5b93ba37ecd70ef58be51e4d`).
**Method:** pure-Zag instrument (`m1_govlh.zag`), zero RNG, 3 byte-identical
runs (`187e5bf9…b696` ×3), all 82 reported numbers independently reproduced
by `score_m1_govlh.py` (82/82 match; S=1 anchors reproduce Round 3 exactly;
§3 partition equality holds).

**Governance question (NOT resolved here — Micah's word):** adopt
OPT = (ST=0, AT=0, CT=705, MT=3588) as the bar, or hold it as a measurement
only? This verdict reports the four evidence legs and states plainly what
OPT protects against and what it abandons. It recommends nothing on adoption.

## Leg 1 — Held-out wrongs: 82.58% does NOT survive with 0 false-PASS

False-PASS counts, OPT vs SAFE, at 1x / 10x / 100x (deterministic ±3 jitter
for k≥1; S=1 is exact geometry):

| Family (n) | S=1 OPT/SAFE | S=10 OPT/SAFE | S=100 OPT/SAFE |
|---|---|---|---|
| N1 1145-class, real (1) | **1 / 1** | 10 / 10 | 100 / 100 |
| N2 single-arm exploit, real (311) | **311 / 0** | 3105 / 0 | 31043 / 0 |
| N3 boundary grid, synth (144) | **100 / 25** | 900 / 222 | 8899 / 2217 |
| N4 corroborated pairs, synth (12) installs | **12 / 12** | 77 / 77 | 720 / 720 |
| N5 double-arm exploit, real+synth (404) | **404 / 0** | 4040 / 0 | 40400 / 0 |
| W calibration (12) | 0 / 0 | 0 / 0 | 0 / 0 |
| P calibration (9) installs | 0 / 0 | 5 / 5 | 43 / 43 |

**HELD-OUT CLEARANCE: FAILED** (prereg §8). OPT false-PASSes on *every*
novel family at *every* scale. The 0-false-PASS result was a property of the
frozen calibration sets only. Two findings cut through:

- **N1 = 1/1 under both bars:** the frozen sweep contains exactly one real
  confidently-wrong *corroborated* wrong (strong=agree=1, conf≥705,
  mrgF≥3588) — the trial-1145 class made concrete. No threshold bar on
  these four axes blocks it; SAFE doesn't either. This is the irreducible
  residual the Round-3 verdict predicted.
- **N4 = 12/12 installs under both bars:** confidently-wrong corroborated
  *pairs* install under OPT and under SAFE alike — the pair-install surface
  is a conf/margin-only problem, and the arms are irrelevant to it.

Reading guide (honest framing): N1/N2/N5-real are, by construction, the
partition of {broad wrongs : PASS(OPT)} — their OPT FP rate is 100% by
definition. Their decision-grade content is the **OPT−SAFE gap**, not the
raw count. N3/N4 are the unbiased geometry probes: **69.4% (100/144)** of
the frontier grid passes OPT; corroborated pairs install 12/12 under both.

## Leg 2 — Broad-wrong explosion: STRUCTURAL, not a calibration artifact

| Scale | OPT FP | SAFE FP | BASE FP | OPT rate | OPT−SAFE gap | Gap rate |
|---|---|---|---|---|---|---|
| 1x (1,109) | 712 | 1 | 7 | 64.20% | 711 | 64.11% |
| 10x (11,090) | 7,115 | 10 | 68 | 64.15% | 7,105 | 64.07% |
| 100x (110,900) | 71,144 | 100 | 672 | 64.15% | 71,044 | 64.06% |

Per prereg §8 the explosion is **STRUCTURAL**: the OPT−SAFE gap holds at the
same rate at 10x/100x with the partition intact (partition_ok=1 at S=1;
N1+N2+N5real = 712 exactly). Decomposition of the 712:

- **1** is irreducible (N1 — passes SAFE too; the 1145 class).
- **711 are admitted ONLY because ST=AT=0** (N2=311 single-arm + N5real=400
  double-arm — every one blocked by SAFE, at all scales, SAFE FP on these
  families = 0 exactly).

The Round-3 trade is now priced in real wrongs: the 84 extra true passes
(826→910) were bought by abandoning the (g)-check arms against **711 real
wrongs** the frozen sweep already contained. Under jitter the gap is
unchanged in kind (wrong-side flips add ~1.4% at 100x, both directions
measured in Leg 3).

## Leg 3 — Headroom: six trials, seven absorbable, knife-edges counted

- **H-trial** (trials above the 82% line): **6** at 1x, 47 at 10x, 453 at
  100x. True-PASS rate under ±3 jitter: 82.58% → 82.45% → 82.45% (stable;
  226 fragile flips vs 43 lucky flips per 90,090 jittered replicas at 100x).
- **H-absorb = 7**: only seven additional bar-*failing* correct trials can
  be added to the denominator before 910/(1102+k) breaks 82%.
- **H-knife**: of the 910 passes, **2 sit exactly at conf=705** and **1
  exactly at mrgF=3588** — one unit of remeasurement flips them.
- **H-jitter** (dangerous direction): blocked novel wrongs that PASS under
  ±3 jitter — 139 at 10x, **1,529 at 100x** (over N1∪N2∪N3∪N5 replicas).
  Fragile true passes: 20 at 10x, 226 at 100x (0.25%).

## Leg 4 — Adversarial (the discarded class): fully exploited, fully blockable

- **N5** (strong=agree=0, high conf/margin): OPT admits **404/404** at S=1
  and **40,400/40,400** at S=100; SAFE blocks **all of them** (0 at every
  scale). The 4 synthetic engineered points (874/1000 × 6600/10410) pass
  OPT and are blocked by SAFE, as constructed.
- **N2** (exactly one arm off): OPT admits 311/311 (31,043/31,043 at 100x);
  SAFE blocks all (0 at every scale).

The arms the optimizer disabled are doing *all* of the work against these
families: the OPT−SAFE gap on N2∪N5 is 715/715 at S=1 with zero SAFE leakage
at any scale.

## Calibration-set guarantees under remeasurement (diagnostic)

- **W (C1): robust.** 0 false-PASS at all scales — the 12 TMB-5 wrongs are
  margin-blocked with 1,200+ units of headroom (max wrong mrgF 2373 vs
  MT=3588); ±3 jitter never reaches the bar.
- **P (C2): knife-edge.** 0 installs at exact geometry, but **5 pair-replica
  installs at 10x, 43 at 100x** — pair V5's weaker member sits at conf=704,
  one unit under CT=705, and +1 jitter installs the pair. Identical under
  OPT and SAFE (pair members carry strong=agree=1 by the frozen worst-case
  convention). The "0 installs" guarantee does not survive remeasurement.

## What OPT protects against, and what it abandons

**Protects:** the 12 frozen TMB-5 wrongs (robustly); the 9 frozen CC1 pairs
(knife-edge on conf); any wrong with mrgF < 3588 or conf < 705.

**Abandons:** 711 real wrongs with conf≥705 ∧ mrgF≥3588 that the
disjoint-span (g)-check would have caught; 69% of the (conf, margin)
frontier grid; 12/12 corroborated wrong-pair installs (which defeat SAFE
too); the 1 real 1145-class wrong in the frozen sweep (which defeats SAFE
too).

## Caveats (travel with the numbers)

1. B-derived families (N1/N2/N5-real) are held-out per the prereg's frozen
   definition — the B set never constrained the Round-3 search — but they
   come from the same frozen sweep: novel *profiles*, not novel sources.
2. SYNTH families (N3/N4/N5-synth) are bar-geometry probes, not claims
   about real-world wrong distributions.
3. The ±3 jitter is a deterministic remeasurement *model*, not a measured
   noise distribution; it probes knife-edges, it does not certify robustness.
4. No kill bar was set by the governing prereg; NOTHING in this verdict
   resolves the adoption question.

## Artifacts

`gen_m1_govlh.py`, `m1_govlh_cases.txt` (sha
`420af6e5…707229f`), `m1_govlh.zag`, `R33_NATIVE_IO_V1.zag` (pinned
`e6379ddb…f61d8`), `score_m1_govlh.py`, `evidence/` (run1/2/3.txt,
DIGESTS.txt), `RUNLOG_M1_GOVLH.md`. No binaries, no `.zagd` committed.
