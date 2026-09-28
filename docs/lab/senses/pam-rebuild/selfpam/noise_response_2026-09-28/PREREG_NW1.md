# PREREG NW-1 — Noisy-legitimate withhold measurement (advisor proposal #2)

Date: 2026-09-28. Status: FROZEN before any measurement.
Advisor: z.ai was requested; the z.ai/GLM key still returns HTTP 403 on both
listed models (glm-5.3-flash, glm-5.3-flash-search) as of 2026-09-28 ~01:10 UTC.
Per the brief, grok-4.7 (highest reasoning, streaming) served as the advisor;
its full response is in zai_response.txt (labeled as grok-4.7, not z.ai).
This prereg implements its proposal #2, ranked below its proposal #1 only
because #1 needs the still-unbuilt self-managed substrate (referred to the
free-memory crew as their next kill bar once it lands).

## Question
What is each Self-PAM gate variant's response curve on (a) byte-identical
legitimate evidence, (b) legitimate evidence carrying benign noise, and
(c) adversarial evidence? This informs — but does not decide — Micah's open
exact-identity vs approximate-equality semantic question.

## Corpus (frozen, unmodified)
`docs/lab/senses/pam-rebuild/selfpam/push100/expansion/` at origin/tnn-native-lab:
352 pairs, manifest `fix1/xp_manifest.txt`.
- MUST-ADMIT: 40 `xp_calib_*` pairs, F and G byte-identical (truth=SAME).
- MUST-WITHHOLD: 312 non-calib pairs, F vs G adversarial transformations
  (48 fshuffle, 48 audiorev, 48 pxperm, 48 cycshift, 48 blkswap, 48 sumswap,
  24 wsumcol). All 312 preserve the plain byte sum by construction.

## Noise model (deterministic, in-memory, zero RNG)
From each pair's F blob (length L), preregistered formulas:
- N1: 1 byte +1 (wrapping) at position L/2.
- N2: 3 bytes +1 at L/4, L/2, 3L/4.
- N3: 8 bytes +1 at L*k/8 for k=0..7.
- N4: 1 byte +1 at position 3 (probes the tolerance window head).
Noisy items are never written to disk; formulas + code are the frozen record.
Rationale for N4: span_seq/8's /8 tolerance only covers weighted deltas < 8
without a bucket-boundary cross, i.e. single-byte changes at positions 0..6.

## Gates (from committed g1_candidate.zag, unmodified)
- id2 "selfpam-fact-gate": span_seq(ev)/8 (position-weighted, /8 tolerant).
- id3 "selfpam-sum-gate": span_sum(ev)/8 (legacy, order-blind).
- id4 "selfpam-fnv-gate": FNV-1a 32-bit, exact (tolerance 0).
Verdict: withhold iff judge(F) != judge(candidate).

## Predictions (recorded before measurement)
- id4: must-admit 40/40 admit; must-withhold 312/312 withhold;
  N1/N2/N3/N4 1408/1408 withhold (any byte difference avalanches the digest).
- id2: must-admit 40/40; must-withhold 312/312 (order-sensitive);
  N1/N2/N3 1056/1056 withhold (weighted delta >= L/2+1 >> 8, bucket always moves);
  N4 ~308/352 admit (delta=4 <8, admits unless bucket-boundary cross, ~1/8).
- id3: must-admit 40/40; must-withhold ~0/312 (all 312 preserve plain sum);
  N1 ~308/352 admit, N2 ~220/352 admit (delta=3, admits unless cross, ~5/8),
  N3 352/352 withhold (delta=8 always moves bucket), N4 ~308/352 admit.

## Kill bars
- K1: id4 withholds 312/312 must-withhold (reproduces the committed number).
- K2: every id admits 40/40 must-admit AND 352/352 F-vs-F sanity.
- K3: 3 runs byte-identical (2 normal + MALLOC_PERTURB_=165), same stdout SHA.
- K4 (prediction audit): every predicted cell reported with measured value;
  any |measured - predicted| > 5% gets a white-box explanation in the report.

## Decision relevance (for Micah, not decided here)
If predictions hold, the table shows the /8 "tolerant" variant (id2) behaves
as exact-identity in practice on realistic noise — its tolerance window covers
only the first ~7 bytes. The real choice is then id4 vs id2 (both near-exact;
id2 keeps the sum-measurement family and order-sensitivity), NOT strict vs
lenient. Genuine leniency toward noisy-but-legit evidence exists in NEITHER
variant and would need a different tolerance design.

## Standards
Pure Zag, zero RNG, no wall clock; frozen corpus untouched; no new frozen
fixtures (noise in-memory); evidence committed to tnn-native-lab.
