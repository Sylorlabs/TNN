# R1-CROSS — Type C Cross-Check VERDICT

**Verdict: REPRODUCED**

Independent re-derivation of every R1 headline claim (Track-5 A/B/C, Q2 D1/D2,
Q1B teacher bakeoff, teacher-noise legs 10%/25%/50%) from the frozen evidence,
using independently written Zag verification code. All committed headline
numbers re-derive within the preregistered ±0.005 tolerance; all committed
byte-identical digests match exactly; K-T3 and K-Q1 evaluate FIRED and K-Q2
evaluates never-fired under the frozen prereg rules. One evidence-completeness
caveat is recorded below (supporting statement, not a headline bar).

- Frozen prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Verification date: 2026-09-23 UTC (runs completed 01:32 UTC)
- Verifier sources: `~/workspace/scratch-crossref/R1/cross/r1check/`
  (`r1c.zag`, `r1_t5.zag`, `r1_q2.zag`, `r1_q1b.zag`, `r1_noise.zag`)
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`)
- Each verifier run 3×; all outputs byte-identical across the three runs.

## 1. Track 5 — A/B/C (learned-only / hybrid / planted-only)

Empirical arm identification from the raw logs (no label trust):
sealed label with revisability 0.0 → A (planted-only) = `Z`;
label with nonzero `explanted` → C (hybrid) = `Y`;
remaining label → B (learned-only) = `X`. Matches the committed mapping.

| arm | metric | committed | re-derived | Δ |
|-----|--------|-----------|------------|---|
| B (X) | mastery | 1.0000 | 1.0000 | 0 |
| B (X) | revisability | 1.0000 | 1.0000 | 0 |
| B (X) | integrity | 1.0000 | 1.0000 | 0 |
| B (X) | retention | 1.0000 | 1.0000 | 0 |
| B (X) | cost | 0.9108 | 0.9107 | 0.0001 |
| B (X) | **composite** | **0.9911** | **0.9910** | 0.0001 |
| C (Y) | mastery | 1.0000 | 1.0000 | 0 |
| C (Y) | revisability | 1.0000 | 1.0000 | 0 |
| C (Y) | integrity | 1.0000 | 1.0000 | 0 |
| C (Y) | retention | 1.0000 | 1.0000 | 0 |
| C (Y) | cost | 0.8931 | 0.8930 | 0.0001 |
| C (Y) | **composite** | **0.9893** | **0.9893** | 0 |
| A (Z) | mastery | 1.0000 | 1.0000 | 0 |
| A (Z) | revisability | 0.0000 | 0.0000 | 0 |
| A (Z) | integrity | 1.0000 | 1.0000 | 0 |
| A (Z) | retention | 1.0000 | 1.0000 | 0 |
| A (Z) | cost | 0.0524 | 0.0523 | 0.0001 |
| A (Z) | **composite** | **0.6552** | **0.6552** | 0 |

(All Δ ≤ 0.0001, from fixed-point truncation in the verifier; tolerance ±0.005.)

K-T3 (frozen rule: arm1 mastery within 5pp of arm0; arm1 revisability ≥ arm0 + 20pp;
no metric where arm2 beats arm1 by ≥ 5pp):
- |M_B − M_A| = 0.0000 ≤ 0.05 ✓
- Rv_B − Rv_A = 1.0000 ≥ 0.20 ✓
- max over 5 metrics of (mean_C − mean_B) = 0.0000 < 0.05 ✓
- **K-T3 FIRED** ✓

Supporting checks: integrity hard gate 0 failures (36/36 reps); DOMAIN_HASH
`7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`
in all 36 bind logs; S10 mastery/revisability equal S1 rep0 per arm; overflow 0;
bind DIGEST lines match across both committed runs 12/12 per arm;
SHA256SUMS.txt: 139/139 files hash-verified, 63/63 committed run-pairs hash-equal.

## 2. Q2 — D1 (planted) / D2 (LLM-distilled)

| arm | metric | committed | re-derived | Δ |
|-----|--------|-----------|------------|---|
| D2 | mastery | 1.0000 | 1.0000 | 0 |
| D2 | revisability | 1.0000 | 1.0000 | 0 |
| D2 | integrity | 1.0000 | 1.0000 | 0 |
| D2 | retention | 1.0000 | 1.0000 | 0 |
| D2 | cost | 0.9108 | 0.9107 | 0.0001 |
| D2 | **composite** | **0.9911** | **0.9910** | 0.0001 |
| D1 | mastery | 1.0000 | 1.0000 | 0 |
| D1 | revisability | 0.0000 | 0.0000 | 0 |
| D1 | integrity | 1.0000 | 1.0000 | 0 |
| D1 | retention | 1.0000 | 1.0000 | 0 |
| D1 | cost | 0.0514 | 0.0514 | 0 |
| D1 | **composite** | **0.6551** | **0.6551** | 0 |

K-Q1 (frozen: D2 passes gate AND Rv_D2−Rv_D1 ≥ 0.20 AND M_D2 ≥ M_D1 − 0.05):
- D2 gate: 0 failures across 24 reps ✓
- Δrevisability = 1.0000 ≥ 0.20 ✓
- Δmastery = 0.0000 ≥ −0.05 ✓
- **K-Q1 FIRED** ✓

K-Q2 (frozen: fires iff CAUGHT_ERR ≥ 1 with D1-installed errors):
re-derived from `corpus.json` (240 input claims, 240 dump rows, 240 teach rows,
parsed independently):
- E_dump = 0, E_obs = 0, E_prb = 0, inconsistent = 0, CAUGHT_ERR = 0
- `withheld` = 0 in all 24 bind logs
- corpus sha256 recomputed = `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada`
  = committed `SHA256.txt` ✓
- `ERROR_INVENTORY.md` and the embedded `error_inventory` object both read n=0
  on all five counters ✓
- **K-Q2 never fired** ✓

Supporting: SHA256SUMS.txt 100/100 files hash-verified, 50/50 run-pairs
hash-equal (Q2 evidence is complete: 50 configs × 2 runs).

## 3. Q1B — learned teacher vs planted teacher end states

- Planted-leg learner digest: `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`
- Learned-leg learner digest: `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`
- **Equal: end-states byte-identical** ✓ (teacher digests differ, as expected)
- Each leg's digest identical across both committed runs ✓
- per_slice.csv: 16/16 rows, battery 12/12 every slice (96/96 per leg),
  mastery 24/24 every slice (192/192 per leg) ✓
- n5_sha256.txt: 5 identical hashes =
  `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151` ✓

## 4. Teacher-noise legs — 10% / 25% / 50% fully absorbed, no knee

| leg | flipped | absorbed | filtered | untaught | world-true mastery | §B.7 battery |
|-----|---------|----------|----------|----------|--------------------|--------------|
| 10% (q1n) | 23/228 = 10.09% | 19 | 0 | 4 | 173/192 | 96/96 |
| 25% (tq) | 59/228 = 25.88% | 49 | 0 | 10 | 143/192 | 96/96 |
| 50% (q1tq) | 118/228 = 51.75% | 99 | 0 | 19 | 93/192 | 96/96 |

All values re-derived from the committed `run1_stdout.txt` accounting lines and
`per_slice.csv` tables; all match the committed numbers exactly.
No-knee condition: absorbed/taught-false = 19/19, 49/49, 99/99 = 1.0 at all
three levels; filtered = 0 at all three; §B.7 battery stays 12/12 per slice
while world-truth mastery falls 173 → 143 → 93. **Fully absorbed, no knee** ✓.

## 5. Caveats and exact divergences

1. **T5 evidence completeness (material caveat).** The committed
   `track5-binding/evidence/logs/` record contains 139 files: 63 configs with
   both runs committed (36 bind-s1 pairs, 24 btrap pairs for X/Z, 3 bind-s10
   pairs) and 12 `btrap_Y` configs with only the single run. The coordinator's
   "75 configs × 2 runs, byte-identical (75/75 in SHA256SUMS.txt)" statement is
   therefore overstated against the committed record (63/75). Every committed
   pair is byte-identical and hash-equal; every headline number re-derives from
   the committed single runs. This does not touch any headline bar or kill
   clause, but the determinism sub-claim for the 12 Y-trap configs cannot be
   reconstructed from committed evidence.
2. **Fixed-point truncation.** The verifier uses integer micro-unit arithmetic;
   printed values truncate (0.9910 vs committed 0.9911; 0.9107 vs 0.9108;
   0.8930 vs 0.8931; 0.0523 vs 0.0524). Maximum Δ = 0.0001 ≪ ±0.005 tolerance.
   Not a divergence in the evidence.
3. **Digest "recomputation" scope.** The committed record contains digest
   *strings* (no serialized learner-state bytes), so the strongest available
   re-derivation is: (a) both legs' recorded learner digests are equal;
   (b) each matches across both committed runs; (c) the 5-run stdout hash chain
   is identical. All hold.

## 6. Frozen pins

- prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- evidence tree SHAs (at frozen commit):
  - `docs/lab/wave12/track5-binding/evidence/logs`: `ec89a683762d62d929001d4d08fdd3eba7f561e9`
  - `docs/lab/wave12/q2-distillation/evidence/logs`: `dbe58e6a6bb19a03c4ea606eef6cc5cb34c29081`
  - `docs/lab/wave12/q2-distillation/corpus`: `f1150160733f9770ad795c094e914ad2c5fafbc8`
  - `docs/lab/q1b-teacher-bakeoff/evidence`: `d8e34ba711cf3acf47a1070c271d4e65e22fda7c`
  - `docs/lab/q1n-noisy-teacher/evidence`: `1a6ca9c81c09e28a0ebaf3cde31f839f1724e50b`
  - `docs/lab/tq-noisy25/evidence`: `8c0f7d2f720f68001a801de6463e844ed7ffbb81`
  - `docs/lab/q1tq-noisy50/evidence`: `aec083beb796f53d541ca11fc4a2c6e05c9dd37e`
  - `docs/lab/wave12/track5-binding/analysis`: `39af3556e57fdebd58180a939bcdfc6cbb22d8c5`
  - `docs/lab/wave12/q2-distillation/analysis`: `001b047585ba0a6ff2516e77e859e8619aa2038a`
  - `docs/lab/wave12/track5-binding/prereg`: `ebb9eeee84e63a98dcd03d5c4be698e554c918c9`
  - `docs/lab/wave12/q2-distillation/prereg`: `9525031860c296206cc59557908acecccead9869`
  - `docs/lab/crossref`: `7791b9b452b11378b4fea715a5411f5dd9c48c1f`
- domain hash: `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`
- corpus sha256: `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada`
- Q1B learner digest (both legs): `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`
- Q1B n5 hash: `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`
- verifier binaries (sha256):
  - r1_t5: `0b03aaf17b93d28ef5b99c8f84d9f314a825bd44baabc08e0453a59bb36a4788`
  - r1_q2: `ab8029c44cd28c27a27f368e46dd200daec976b0af7ba917bf962d20c4403567`
  - r1_q1b: `55357a66288105ed538887a1eb30c90cd800497f74aec7ba90b699a44e776adb`
  - r1_noise: `1a7a99ccadb0567d6a8b6da416c3e66fa79e5212cae44dc3dedc5e5be03af901`
- verifier run outputs (sha256, identical across 3 runs each):
  - t5: `85c4a735b85d2f17f83283ccc3d3be07d2f21f9e93c946a09f4da9a8eec5f9b7`
  - q2: `93ef2e42391fc5bc9991b0600aefff85a2c7e3b0035024e73c8b21b5108f8636`
  - q1b: `b6fa66d28fe7e151b287fa0aa98399eff290a3bada1f0165dd4c62bc7ad06aa0`
  - noise: `2dafa828de017baa05aeba73dd33f2ead131b394a5232561238bb2038dac0fd1`
- znc toolchain: sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`

## 7. Method note

Zero trust in R1-PRIMARY code or outputs: the primary crew's scratch was never
read. The verifier sources were written from the frozen prereg rule texts and
the committed evidence files' observable formats only. Metric definitions were
re-implemented independently in Zag from the prereg descriptions
(mastery = mean d1/d2/d3; revisability = min(rev_false, rev_genuine);
integrity = mean(applicable trap fracs, 1−hallu, k1, k2, refusal);
retention = min(1, r3/r2); cost = 1/(1 + esc/eps·100 + 0.1·ops/eps);
composite = 30/25/25/10/10). Integer micro-unit arithmetic; zero RNG.
SHA-256 via the generic R33 substrate (self-tested against the "abc" vector).
