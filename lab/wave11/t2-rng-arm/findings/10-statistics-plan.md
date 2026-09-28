# Slice 10 — Statistical analysis plan for the Arm B vs Arm C head-to-head (Track 2)

## 1. Slice
Track 2, slice 10: the preregistered statistical analysis plan for the fenced-RNG
Arm B vs deterministic state-variation Arm C comparison — sample sizes, power,
paired tests, multiplicity control, interim looks, and void-vs-loss rules.

## 2. Falsifiable claim
Arm C's expression variation is more *lawful* than Arm B's seeded RNG: on n = 500
matched (probe, base state, lawful edit) pairs, C's adaptivity directional-hit rate
exceeds B's by ≥ 0.10 (one-sided paired test, Holm-adjusted); C clears the G3 NMI
bar (slice 10) while B's NMI stays at/below its permutation-null 99th percentile
(the dice signature: varied but state-independent). If the paired comparison fails
to reject, or B clears G1–G3 alongside C, the claim "deterministic state variation
is more adaptive than seeded RNG" is dead, and C retires under K7.

## 3. Design
**Unit of pairing.** Every comparison uses matched triples (p, s, i): probe p, base
state s, variant index i = 1..8. For each triple both arms run the identical binary;
B draws from its prereg-enumerated seeded RNG points (seed log is part of the state
log), C uses its lawful state variants (slice 10's lawful_edit). Arm C's output must
be byte-identical whether or not the seed triple is present — that is itself the
no-RNG-leak check (cf. t1 09-no-rng-audit). Randomization is never inside the
analysis: all tests are deterministic functions of committed logs.
**Dimensions and tests (per horizon, 1x and 10x):**
- D1 adaptivity hit rate: paired McNemar on pair-level binary hits, H1: pC > pB,
  n = 500 pairs. α = 0.01 one-sided, power ≥ 0.90 at δ = 0.10 (pC=0.60, pB=0.50,
  pair ρ = 0.3 → SE ≈ 0.026, z ≈ 3.8). One interim look allowed (see below).
- D2 expression diversity: qualifying metric only, paired t-test on per-bucket
  log distinct-expression counts, n = 500 buckets; 90% power at standardized
  MDE d = 0.16, α = 0.01. Pre-registered expectation: B WINS this metric; a B
  win here does not count toward the K7 majority — it is the dice signature when
  paired with a D1 loss.
- D3 integrity traps: 1440 matched traps, arm-level gate. Both zero-failure → tie
  (neither scores); any failure loses the dimension. If both fail, paired McNemar,
  α = 0.01. Zero-failure evidence strength: rule-of-three upper 95% bound 3/1440.
- D4 judgment stability: verdict + memory-decision invariance, 300 probes × 8
  variants per arm, per-probe binary (invariant or not), paired McNemar,
  H1: pC > pB; 90% power at δ = 0.04 (0.99 vs 0.95, ρ = 0.5), α = 0.01.
- D5 reproducibility-from-logged-state: gate, not a test. n = 200 replays/arm;
  any mismatch → arm loses (cf. K1). Zero-mismatch bound: 3/200 = 1.5% at 95%.
- D6 cost: wall-clock latency + audit-log bytes, n = 1000 decisions, paired
  t-test on logs, two-sided α = 0.01, 90% power at d = 0.13. Win = lower cost.
**Multiplicity.** Holm-Bonferroni step-down across the 5 decisive dimensions
(D1, D3, D4, D5-as-gate-comparison, D6) within each horizon, FWER 0.05. Gates
(replay, integrity/verdict/memory-leak laws) never enter multiplicity: they are
≥1-firing laws, not p-values. D2 excluded (qualifying descriptor). 1x and 10x are
separate families; a dimension counts only if won at BOTH horizons (K7 conjunction).
**Interim looks.** One interim permitted, only on D1, at 50% of planned pairs, for
efficacy only. Lan-DeMets O'Brien–Fleming spending of the D1 one-sided α = 0.01;
builder computes exact boundaries from the OF spending function and commits them
before the first run (reference values: z ≈ 3.29 interim / z ≈ 2.37 final).
Non-binding futility stop allowed on K-bar evidence; spends no alpha. All other
dimensions: single final read, no interim.
**Expected adaptivity loss, pre-registered.** B is expected to lose D1 (hit ≈ 0.50,
NMI ≈ null) and win D2. This pattern is scored as the dice signature, not a
surprise. If B instead clears D1/G3 alongside C, that is a pre-registered
surprise: report as-is per no-free-lunch; B takes the D1 dimension and the K7
majority rule applies unchanged — the expectation never rescues C.

## 4. Kill bar
- Arm C retires iff Arm B wins ≥ 3 of the 5 decisive dimensions at BOTH horizons
  (K7), or any K1–K4 firing occurs on C.
- Arm B retires iff it loses ≥ 3 decisive dimensions at both horizons (the
  amendment's posture: loss on adaptivity, judgment stability, integrity traps,
  or reproducibility-from-logged-state retires the arm), or its seed log fails
  replay twice (an RNG arm that cannot reproduce from logged state is unfenced).
- A 2–2–1 or tied split on decisive dimensions = inconclusive: neither arm
  retires on the head-to-head; report as-is, and B's retirement review goes to
  Micah with the full verdict sheet.

## 5. Honesty notes
- McNemar assumes pair independence; base-state reuse induces correlation — use
  cluster-robust SEs (cluster = base state) or accept the bars as conservative.
- D3/D5 at ~100% are gate comparisons, not powered tests; they cannot detect
  small-but-real differences — that is intentional (laws are not statistics), but
  say so openly.
- D2's "qualifying" status is a judgment call: it prevents RNG from winning on
  cheap variety, but it also means a dimension where B dominates contributes
  nothing to the majority — report the raw numbers regardless.
- The OF interim spends alpha inside D1's Holm share; if the interim boundary is
  computed wrong, the whole D1 decision is suspect — commit the numbers first.
- This plan measures *behavioral* difference between arms, not *why* C is
  adaptive; the lawfulness mechanism is slice 10's claim, not this slice's.
- **Void-vs-loss rule (binding).** VOID = the data cannot be trusted; no metric
  result counts and no dimension is scored. Voids: any G0 replay mismatch
  (per K1, including the single dated logging-omission repair), B's seed-log
  failing to reproduce, the harness itself failing K1, or a corrupted-state pair
  (slice 22). LOSS = the data is valid and the arm takes the hit. Losses: any
  metric gate failure or p-test decision against the arm. A void is never a win
  for either arm. Anti-gaming: an arm with >5% void rate across pairs retires —
  dodge-by-void is a falsification of the arm, not a reprieve. A second
  seed-log replay failure retires B outright (K1 terminal clause).

## 6. Next build step
Build the matched-triple runner first: for one probe × one state, execute 8
variants on both arms from committed logs, verify byte-identical replay for C
(G0) and seed-log replay for B, and confirm the pairing harness itself passes K1
before any metric code lands — an uninterpretable pairing invalidates every
test in this plan.
