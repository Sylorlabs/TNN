# R4 Result: Active-Policy Advantage

Status: R4-FAIL. F-R4 FIRED. The disagreement-IV policy is HONESTLY
RETIRED.

Prereg: PREREG_R4.md (commit 08c2d1f4f), committed alone before any
R4 implementation. Commit order verified: 08c2d1f4f is a strict
ancestor of the implementation commit. K1 PASS.

## Implementation

r4.zag (787 lines): the full altexp.zag machinery (commit 73d9637a2)
copied verbatim (allocation helpers, LCG RNG, sealed(5), node /
signature / beam functions, passive(), select_iv, select_iv_rand,
do_iv) with fn main replaced by the R4 driver. The driver runs, for
each of the 12 frozen seeds, the P-DIS evidence loop and the P-RAND
evidence loop (each from the seed: 8 verbatim passive samples with
the X6-confound bias, then 24 rounds of beam_extend, policy select,
do_iv), computes combo coverage = distinct (x & 7) among the 32
observations, and emits per-seed coverages plus aggregates
(SUM_DIS, SUM_RAND, DIFF, WINS, BOTH8). No other logic change.
Policies are the attack's verbatim select_iv / select_iv_rand.

Built with znc 2026.07.0-dev, pure Zag, zero Python at every stage
(build, run, verification, byte checks via shell grep only). Zero
em/en dash bytes.

Determinism: 3/3 byte-identical runs, md5
409ab79e4acf9409cbc2207adadf88ea, zero stderr on all three. K2 PASS,
K3 PASS.

## Results (per frozen seed, paired)

| Seed  | P-DIS cov | P-RAND cov |
|-------|-----------|------------|
| 61977 | 7         | 7          |
| 62954 | 7         | 8          |
| 63931 | 8         | 8          |
| 64908 | 8         | 8          |
| 65885 | 8         | 8          |
| 66862 | 8         | 8          |
| 67839 | 8         | 8          |
| 68816 | 7         | 8          |
| 69793 | 8         | 8          |
| 70770 | 7         | 8          |
| 71747 | 8         | 8          |
| 72724 | 8         | 8          |

Aggregates: SUM_DIS=92, SUM_RAND=95, DIFF=-3 (mean margin -0.25),
WINS=0, BOTH8=8.

## Verdict against the frozen dual bar

(a) Mean margin >= 0.75 combos: observed -0.25. MISS.
(b) P-DIS wins >= 8/12 paired seeds: observed 0/12. MISS.
F-R4 (mean RAND >= mean DIS): 95 >= 92. FIRES.
INCONCLUSIVE (both 8/8 on >= 10/12): BOTH8=8. Does not trigger.

R4-FAIL. Per the frozen prereg, the disagreement-IV policy is
honestly retired: the mechanism is passive plus random-IV discovery,
the claim is updated accordingly, and R1 runs with P-RAND (revival
plan section 6, Phase B).

## Interpretation

The result is stronger than a bare miss: random interventions beat
disagreement interventions outright on the preregistered primary
metric (95 vs 92 coverage; 0 of 12 paired wins for P-DIS). The
attack's "decorative" reading is confirmed and sharpened: at the
24-round budget the disagreement machinery is not merely
unnecessary, it is strictly dominated by deterministic random
sampling on combo coverage. The 24-round budget is generous to both
policies (median coverage 8), but it is not inconclusive (BOTH8=8 <
10), so the dual bar stands as the operative gate and the policy
comparison is adjudicated, not deferred.

Failure localization (plan 4.1/4.4): a coverage shortfall implicates
the policy, and the shortfall is on the P-DIS side. The beam is
exonerated as a policy confound here because coverage is a pure
policy output, independent of beam fit quality.

## What this means for revival

Revival is conjunctive (R1 AND R2 AND R3 AND R4); R4 fails, so the
Q4 discovery claim is NOT revived. The honest bounded-L2 claim from
the revision stands. R4 is the localized weakness that was
suspected, and it is now measured: the "active" component does not
survive a preregistered policy comparison. The defined next target
is the mechanism with P-RAND named as the R1 policy.

## Files

PREREG_R4.md, r4.zag, r4_bin, R4_RAW_{1,2,3}.txt, R4_RAW_{1,2,3}.err
(all empty), build.err (empty).

Raw evidence: R4_RAW_1.txt (md5 409ab79e4acf9409cbc2207adadf88ea).
