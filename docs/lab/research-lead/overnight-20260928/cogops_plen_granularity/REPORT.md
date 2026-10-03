# REPORT: COGOPS-PLEN-GRANULARITY -- does finer replay granularity make plen pressure bite?

**Verdict: INCOMPLETE (negative on the preregistered bars).**
GF1 PASS; GF2 FAIL (4/8 < 6/8); GF3 FAIL (strict clause 3/8 < 4/8);
GF4 PASS; GF5 PASS; GF6 PASS. Per the frozen mapping the
robustness bars failed, so no mechanism confirmation is claimed.

**Mandatory correction to the mapping's gloss:** the mapping's
GF2-fail gloss ("plen is inert even at 1-point replay
resolution") is contradicted by the data and is not adopted.
What the data show: finer granularity makes the plen
coefficient **sporadically behaviorally relevant** -- revise
trajectories diverge between plen=1 and plen=3 in 0/8 pairs at
quantized replay, 1/8 at medium, 3/8 at fine. The "make pressure
bite via granularity" hypothesis is neither robustly confirmed
nor retired; it is demoted to a weak, sporadic effect. The
>=6/8 bar was too aggressive for the effect size the search
dynamics actually produce.

Prereg `4e04d7b47` (plus append-only repair `0f817e0a`; see
Provenance) strictly precedes implementation. 3/3 byte-identical,
sha256 `dd8f0656753f9a5c8e00de91df43fa02559214c48f21edc8e6db3a1015f7a762`.

## Design recap

`gran.zag` = the RNG lane's matched-RNG revise driver (same 8
pair seeds, seed body, 40-episode setup, RNG record/match
protocol, 30-generation revise, adopt rule `best > cur+150`,
850 raw passer bar) plus: (a) `replay_mode` cell 2402
(researcher-owned factor): g=0 quantized tiers (byte-exact copy
of the RNG scorer), g=1 medium (per-snapshot 25-point steps,
strict refinement of g=0), g=2 fine (g=1 plus 1-point near-miss
credit, capped 999; strict refinement of g=1); (b) a
counterfactual flip diagnostic (cells 2403/2404, reporting
only) counting selection comparisons where explicit plen=1 vs
plen=3 boolean outcomes disagree; (c) a PADAPT arm (plenmode 4:
pmode 3, cell 2370=0, `plen_adapt` thermostat live). 72 revise
searches per run. Full design in PREREG.md.

## Results

RNG match: 48/48, 0 mismatches. Seed-body `cur` stays 100-208
across all (pair, rg), matched within every pair.

### Trajectory divergence (decisive measure: GEN sequences)

| rg | P1 vs P3 diverge | PA vs P3 diverge |
| 0 (quantized) | 0/8 | 8/8 |
| 1 (medium) | 1/8 (pair 0) | 8/8 |
| 2 (fine) | 3/8 (pairs 0, 4, 7) | 8/8 |

### Counterfactual flip counts (P1+P3 arms; upper bound, see Mechanism)

| pair | g=0 | g=1 | g=2 |
| 0 | 0 | 30 | 6 |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 6 | 6 | 6 |
| 4 | 0 | 0 | 24 |
| 5 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 40 |

Pivotal flips (pairs where trajectories actually diverge):
g=0: 0/8; g=1: 1/8; g=2: 3/8. Pair 3's flips (6 at every g) are
all non-pivotal: trajectories byte-identical there.

### Revise cost (cost = trials if adopted else 369), matched pairs

rg=0: P3 [152,164,369,369,369,140,332,320] mean 276.9;
       PA [152,164,369,368,369,140,248,200] mean 251.2.
rg=2: P3 [152,164,369,369,369,140,332,368] mean 282.9;
       PA [152,164,369,368,369,140,248,152] mean 245.2.
PA-P3 per-pair deltas, every rg: [0,0,0,-1,0,0,-84,-120]
(rg=2 pair 7: -216). PA never worse than P3 in 24/24 arms,
strictly better in pairs 3, 6, 7 at every granularity.
Sign test on 3/3 non-tied favoring PA: p=0.125 --
suggestive, not significant (n=8).

Notable: pair 3, PA adopts (best 850/850/856) where P3
exhausts the budget with best=0, at all three granularities.
Pair 0 at g=1/g=2: P1 finds higher-raw bodies than P3
(914 vs 871; 917 vs 874) -- the weaker length penalty
retaining longer, higher-raw variants, i.e. the pressure
doing exactly what a parsimony pressure is designed to do.

Thermostat: PLEN-ADJ fired in 7/24 PA arms (pairs 0,3 at
g=0; 0,3 at g=1; 0,3,5 at g=2). PA diverges from P3 in
24/24 arms regardless of firing, so the PA-vs-P3 gap is
driven by plen=0 itself, not the 0->1 step.

## Kill bars

- GF1 REPLICATION: g=0 P1vsP3 SAME 8/8 (>=7/8); flips=0 in
  7/8 pairs (>=7/8; pair 3's 6 flips are non-pivotal);
  g=0 GEN sequences byte-match the RNG lane's published
  sequences 16/16. **PASS**.
- GF2 BITES: g=2 flips>0 in 4/8 pairs (pivotal: 3/8),
  needed >=6/8. **FAIL**.
- GF3 DOSE-RESPONSE: monotone 7/8 (>=6/8) but strict
  f(g=2)>f(g=0) only 3/8 (pairs 0,4,7), needed >=4/8.
  **FAIL**.
- GF4 ADAPTIVE EFFECT: g=2 PA vs P3 differ 8/8 (>=4/8).
  **PASS** (weak bar: the 0-vs-3 gap is arithmetically
  wide; the informative result is the cost table above).
- GF5 DETERMINISM: 3/3 byte-identical. **PASS**.
- GF6 GUARDS: build.sh guards (safebin-only PATH,
  python3/python unresolvable, no python token, no
  `as *i32`, no `_MODE`, opcodes exactly 1..8, no
  `while.*!(`, one main). **PASS**.

## Mechanism analysis

**Why the effect is sporadic, not robust.** A plen-u vs
plen-v flip needs a compared pair with
u*Dlen < Draw < v*Dlen. The search dynamics, not the scorer
alone, decide whether such comparisons arise. In 5/8 pairs
at g=2 the revise search never visits a pivotal one; in 3/8
it does. Finer granularity widens the reachable set of
(Dlen, Draw) coincidences (0/8 -> 1/8 -> 3/8 divergence),
but cannot force the search to visit them. The >=6/8 bar
assumed the search would routinely visit the flip region;
it does not.

**Non-pivotal flips are real, not a diagnostic bug.**
Pair 3 (all g): 6 counterfactual disagreements, identical
trajectories. The diagnostic replicates the actual
decisions exactly (verified: `cmp_under(p)` ==
`pop_fit`/`off_beats_pop` outcome whenever plen_of==p);
disagreements on non-pivotal comparisons occur in the
worst-find loop, where intermediate `pop_is_better`
outcomes can differ while the final argmin is unchanged.
Counterfactual flips are therefore an upper bound on
pivotal flips; trajectory divergence is the decisive
measure.

**Diagnostic limitation (honest):** `tournament()` does its
own inline comparison (length tiebreak, not age) and does
not call `pop_is_better`, so tournament parent-selection
is uninstrumented -- flip counts miss that path entirely.
The divergence analysis covers all paths; the counts do
not. Kept as preregistered; noted, not silently fixed.

**Why PA vs P3 diverges everywhere.** Flip condition for
0 vs 3 is 0 < Draw < 3*Dlen -- far wider than 1 vs 3's
Dlen < Draw < 3*Dlen. plen=0 (raw-only selection) vs
plen=3 disagree routinely. The thermostat firing (7/24
arms) is incidental to the PA effect.

## Answers to the three key questions

1. **Can finer granularity make plen pressure behaviorally
   relevant?** Yes, demonstrably but sporadically:
   0/8 -> 1/8 -> 3/8 trajectory divergence across
   g=0,1,2. The coefficient flips pivotal selection
   decisions once replay is fine enough.
2. **What granularity is needed?** Pivotal flips first
   appear at g=1 (25-point per-snapshot, 1/8 pairs) and
   strengthen at g=2 (1-point, 3/8). Sub-25-point
   resolution is where the coefficient starts to bite;
   the quantized tiers never bite for 1-vs-3.
3. **Rescue adaptive PLEN, or is plen the wrong mechanism?**
   Neither extreme. Plen is not "fundamentally wrong": it
   bites, and -- opposite to the original K4 hypothesis's
   sign -- *lower* revise-phase plen (PA: 0->1) costs less
   than or equal to plen=3 in 24/24 matched arms
   (strictly less in 3/8 pairs per granularity). The K4
   hypothesis (under-pressured revise hurts) had the
   mechanism backwards; combined with the RNG lane, the
   K4 gap is best explained as RNG/history artifact, not
   pressure level. But "rescue" as a robust optimizer is
   not earned either: the biting is sporadic (3/8) and
   the cost edge is suggestive (p=0.125), not
   significant. The adaptive concept survives as a live,
   weak pressure -- not as a confirmed win.

## SUF analysis (honest)

L2, not L3 -- same split as the parent lanes; this lane
adds a causal discrimination, no learning claim.
Researcher-owned: the three scorers, the diagnostic, the
pair seeds, the PA proxy (plen-0 start is not the full
adaptive create->revise trajectory). Genuinely new: (a)
the dose-response of behavioral relevance on replay
granularity (0/8->1/8->3/8); (b) the sign reversal --
lower revise plen helps or is neutral, contradicting the
K4 hypothesis's direction; (c) the moot-flip mechanism
(counterfactual disagreement without trajectory effect).
NOT claimed: a robust rescue of adaptive PLEN (bars
failed); any claim about the full adaptive trajectory
(PA tests revise-phase plen only); statistical
significance of the cost edge.

## Follow-ups

- The sporadic biting suggests the search rarely visits
  the flip region: instrument *where* in (Dlen, Draw)
  space revise comparisons live, and whether a
  learner-owned signal could steer toward pivotal
  comparisons (stall-triggered pressure was already
  proposed in the parent lane).
- Causal test of plen HISTORY (RNG lane follow-up,
  still open): arms differing only in pre-revise plen
  history, revising at the same plen with matched RNG.
- The PA cost edge (3/8 pairs, consistent across g):
  replicate on fresh pair seeds to test whether it is
  real; if real, the "pressure" story inverts -- the
  question becomes why plen=3 ever helps.
- Tournament selection remains uninstrumented; a future
  diagnostic should cover it if flip-counting is reused.

## Provenance

- Prereg: `4e04d7b47` (frozen GF1-GF6) + append-only
  repair `0f817e0a` (restored a sibling lane's files that
  the prereg commit's stale-base tree had dropped; no
  science touched). Lesson: build commit trees from a
  freshly re-read tip in the same atomic step.
- Implementation: `gran.zag` (from `rng.zag` @ 6daff87c5),
  `build.sh`, `gran_bin`, 3/3 byte-identical runs
  (sha256 `dd8f0656753f9a5c8e00de91df43fa02559214c48f21edc8e6db3a1015f7a762`),
  `analysis.sh` (shell text analysis of emitted lines).
- 48/48 RNG-MATCH, 0 mismatches; g=0 reproduces the RNG
  lane's GEN sequences 16/16.
- Non-ledger task. Commits local only, explicit
  pathspecs, never pushed.
