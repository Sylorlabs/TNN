# Q4 Baseline Comparison Result: BASELINE-COMPARED

Date: 2026-09-30. Worker: Q4 Baseline Comparison Worker.
Prereg: 98ece92e4 (committed before implementation).
Implementation: q4_baseline.zag (pure Zag, no Python).

## Verdict: BASELINE-COMPARED

All four kill bars pass. The honest answer to "does the learner beat
simple memorization" is: **not on raw Phase-1 accuracy, but yes on
Phase-2 compositional reuse.** Details below.

## Reference numbers (from committed results)

- Learner Phase 1: 64/64, 7 ops, from 8 biased passive + 24 adaptive
  interventions (32 observations). Best single-bit observable: 40/64.
- Learner Phase 2 reuse: hit_iv = 0, 64/64. Scratch: hit_iv = 24, 52/64.

## Kill Bar Results (3/3 byte-identical, md5 1d85d5767ca303d781dba1e55df717a2)

### K1: Baselines implemented: PASS

MEM (lookup table on (x1,x2,x3)), 1NN (Hamming on bits 0-2), LIN (grid
search over w1,w2,w3,b in {-1,0,1}, 81 combos, tie-break fewest nonzero
weights), RAND (seeded coin flip), MEM-COMP (memorize-then-compose for
Phase 2). sealed() fam 5/6 and passive() replicated verbatim from
q4_parcond.zag; E1 passive uses the identical seed (123456789) as the
first RNG consumer, so the 8 passive samples are the same ones the
learner saw.

### K2: Experiments measured: PASS

3/3 byte-identical runs, exit 0, zero stderr on all runs.

### K3: Honest assessment

E1 (matched 8 biased passive samples, combo coverage 5/8):

| Baseline | Accuracy |
|----------|----------|
| MEM      | 56/64 = 0.875 |
| 1NN      | 40/64 = 0.625 |
| LIN      | 56/64 = 0.875 (w = 1,1,1,-1, i.e. x1+x2+x3 >= 2) |
| RAND     | 40/64 = 0.625 |
| (learner, 32 obs) | 64/64 = 1.000 |

E2 (8 passive + 24 uniform random, same 32-observation budget, dumb
sampler; combo coverage 8/8):

| Baseline | Accuracy |
|----------|----------|
| MEM      | 64/64 = 1.000 |
| 1NN      | 64/64 = 1.000 |
| LIN      | 56/64 = 0.875 (structural ceiling) |
| RAND     | 40/64 = 0.625 |
| (learner, 32 obs, adaptive) | 64/64 = 1.000 |

E3 (uniform draws to cover all 8 combos, seeds 1..20): total 160 draws,
mean 8.0, max 8. See PRNG artifact note below.

E4 (Phase 2, same 8 passive fam-6 samples as the paper, seed 555555555;
D-combo coverage 6/8):

| Baseline | Accuracy |
|----------|----------|
| MEM-COMP (D table via D = C' XOR x4, then C' = D_table XOR x4) | 56/64 = 0.875 |
| (learner reuse, hit_iv = 0) | 64/64 = 1.000 |
| (learner scratch, hit_iv = 24) | 52/64 = 0.813 |

### K4: Purity and determinism: PASS

Pure Zag at every stage (znc compile, shell, git only). Zero Python
invocations. 3/3 byte-identical. Zero em dash bytes in committed docs
(shell-verified).

## Findings

**F1. On raw Phase-1 predictive accuracy, memorization ties the
learner.** MEM reaches 64/64 whenever it has full combo coverage (E2),
matching the learner's 64/64. The learner does not beat a lookup table
on prediction in this 8-combo world. Prediction P1 holds.

**F2. The learner beats every hypothesis-class baseline.** LIN caps at
56/64 (F-PARCOND is not linearly separable; the best threshold,
x1+x2+x3 >= 2, gets exactly 7/8 = 56/64, matching hand analysis).
Single-bit observables cap at 40/64. RAND at 40/64. The learner's 64/64
with a 7-op expression is a genuine improvement over linear,
single-feature, and random baselines. Prediction P2 holds (MEM 56/64 at
5/8 coverage, 1NN 40/64, LIN exactly 56/64).

**F3. On Phase-2 reuse the learner genuinely beats memorization.**
MEM-COMP scores 56/64 versus learner reuse 64/64 on the identical 8
passive samples. The reason is structural: the learner reuses D as a
*general rule* (the Phase-1 7-op expression, 64/64 on all combos), so
XOR(D, X4) generalizes everywhere; MEM-COMP reuses D as a *partial
table* (6/8 combos covered), so composition fails on the 2 unseen
combos. **Prediction P4 is falsified, and the falsification favors the
learner**: the reuse-vs-scratch gap is not merely library-vs-no-library.
A memorized library component composes worse than a learned general
component. This is the C0-D dividend made concrete: the value of the
learned representation is in its generality under composition, not just
its availability.

**F4. Sample-efficiency comparison is confounded by a PRNG artifact
(disclosed).** E3 mean draws to full coverage is 8.0 with max 8 across
all 20 seeds, which looked suspicious until analyzed: rng_range(st,64)
takes the low 6 bits of the LCG state, and the combo key uses the low 3
bits; the map x -> (5x+1) mod 8 is a single 8-cycle, so (rng_range % 64)
& 7 has period exactly 8 for every seed. Uniform draws therefore cover
all 8 combos deterministically in 8 draws. This inflates E2's MEM/1NN
scores (coverage was guaranteed, not earned) and makes E3 uninformative
about true coupon-collector efficiency. It does not affect E1 (the
x6==y rejection step breaks the cycle) or E4, and it does not affect
the learner's own 64/64 (the learner faced the same sampler; its 24
adaptive interventions are deterministic beam-disagreement choices, not
RNG draws). A follow-up with a better PRNG or high-bit sampling would
be needed for a clean sample-efficiency number. Prediction P3 holds
numerically (8.0 < 32) but for the artifact reason, not the statistical
one; reported here so no one cites E3 as a real efficiency result.

## Falsifiers of my predictions

- FP1 (MEM fails 64/64 at 32 uniform obs): does NOT fire. MEM hits 64/64.
- FP2 (LIN exceeds 56/64): does NOT fire. LIN is exactly 56/64.
- FP3 (E3 mean draws > 32): does NOT fire. Mean is 8.0 (artifact, see F4).

## Bottom line for the promotion pipeline

Step 5 (simple-baseline comparison) is complete with a scoped, honest
result:

1. The learner's Phase-1 discovery claim must not be stated as "beats
   memorization on accuracy": a lookup table ties it at 64/64 given
   coverage. The correct statement is "beats linear, single-feature,
   and random baselines; ties memorization on prediction."
2. The Phase-2 reuse claim is *strengthened*: reuse of the learned
   general component (64/64) beats memorize-then-compose (56/64) on
   identical evidence. The C0-D advantage is real and learner-specific.
3. The compactness claim (7 ops vs 8 table entries) and the
   composition-generality claim are where the learned representation
   demonstrably wins; raw accuracy on 8 combos is not the differentiator.
4. Do not cite E2/E3 as sample-efficiency wins without the PRNG-artifact
   caveat.

## Files

- PREREG_Q4BASELINE.md: test prereg (98ece92e4)
- q4_baseline.zag: implementation (pure Zag)
- q4_baseline_bin: compiled binary (untracked, not committed)
- Q4BASELINE_RAW_1/2/3.txt: 3/3 byte-identical raw outputs
- Q4BASELINE_RAW_1/2/3.err: empty stderr logs
- Q4BASELINE_RESULT.md: this file
- build.err: znc build log
