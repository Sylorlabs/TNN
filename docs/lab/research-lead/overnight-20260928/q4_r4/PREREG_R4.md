# R4 Preregistration: Active-Policy Advantage on F-PARCOND

Date: 2026-09-30. Worker: Q4-R4 Implementer.
Pipeline: Q4 revival plan section 4 (plan commit 290f0d061, PLANNED).
Target: the "decorative" finding from the Q4 alternative-explanation
attack (result 73d9637a2): RANDIV (random IVs) reached 64/64 true with
a 5-op expression, matching the disagreement-IV run's accuracy with
fewer ops. R4 adjudicates whether the disagreement policy has a
preregistered advantage over random interventions.

## 1. Objective

Test whether the disagreement-IV policy P-DIS beats deterministic
random intervention selection P-RAND on F-PARCOND discovery, on the
primary metric of combo coverage. R4-PASS revives the "active"
component of the Q4 discovery claim. R4-FAIL retires the disagreement
policy honestly: the mechanism becomes passive plus random-IV
discovery and R1 runs with P-RAND.

## 2. Frozen policies (verbatim from the attack)

Both policies are byte-for-byte copies of the attack implementation
(altexp.zag, commit 73d9637a2), which copied the Phase-1 machinery
verbatim from q4_parcond.zag.

P-DIS (disagreement-IV, attack fn select_iv): after each round's
beam_extend, consider the top 8 beam entries (fewer if the beam is
shorter). For each unused x in 0..63 in ascending order, let c1 be the
number of top entries predicting 1 at x; disagreement d = 8 - |2*c1 -
8|. Select the first x attaining the strictly maximal d. No RNG is
consumed by the selection itself.

P-RAND (attack fn select_iv_rand, the RANDIV spec): count the unused
x; select index rng_range(st, cnt) over the ascending unused list,
where rng_range is the seeded LCG (rng_next: s = (s*1103515245 +
12345) mod 2^31, state at st offset 16). Deterministic given the
seed.

Per-round loop (identical for both policies, attack fns
build_learner32 / phase1_rand): reset state (st offsets 0,4,8,12 to
0; clear sigtab; clear used; 8 terminal beam entries; beam count 8);
8 passive samples via the verbatim passive() (first 6 samples retry
up to 1000 draws until bit5 == y, i.e. the X6-confound bias; last 2
are free draws); then 24 rounds of (beam_extend; policy select;
do_iv adds (x, sealed(5,x)) to evidence and marks x used).

Paired design: both policies start each seed from the identical seed
value, so the 8 passive samples are identical across the two arms;
the 24-round budget is identical. The arms differ only in the IV
selection rule.

## 3. Seeds (frozen)

12 fresh seeds, pairwise distinct, disjoint from the tainted
exploratory seeds {11, 22, 33, 44, 55} and from all other committed
seed sets (123456789, 555555555, 770404483):

T1=61977, T2=62954, T3=63931, T4=64908, T5=65885, T6=66862,
T7=67839, T8=68816, T9=69793, T10=70770, T11=71747, T12=72724.

(T_i = 61000 + i*977 for i=1..12. R1 must not reuse these; the R1
prereg will name its own disjoint set.)

## 4. Metrics

Primary metric (governing): combo coverage = number of distinct
(x & 7) combos among the 32 observations (8 passive + 24 IVs).
Coverage is a pure policy output; it isolates the policy from beam
fit-failure modes (the SEED=55 mode: 23/32 fit at 8/8 coverage).

Secondary metrics (reported per seed, non-governing): kept-beam best
evidence fit (/32), kept-beam true /64 accuracy. If the policies tie
on coverage but differ on accuracy, that is a beam effect, not a
policy effect (preregistered interpretation).

## 5. Dual bar (frozen)

R4-PASS requires BOTH:

(a) mean coverage(P-DIS) - mean coverage(P-RAND) >= 0.75 combos;

(b) P-DIS wins the paired per-seed coverage comparison on at least
8 of the 12 seeds (a win is cov_dis > cov_rand; ties are not wins).

Rationale (plan 4.3): 0.75 combos is about 9 percent of the 8-combo
space, and one full combo is the difference between determined (8/8)
and underdetermined (7/8) evidence. The win-rate bar alone has about
a 19 percent null rate at n=12; the dual bar is the operative gate.

## 6. Falsifiers and special cases (frozen)

F-R4: mean coverage(P-RAND) >= mean coverage(P-DIS). R4 FAILS and the
disagreement policy is HONESTLY RETIRED: the mechanism becomes
passive plus random-IV discovery, the claim is updated accordingly,
and R1 runs with P-RAND.

Non-PASS without F-R4: the dual bar is conjunctive, so any miss of
(a) or (b) is R4-FAIL regardless of whether F-R4 fires. The R1
policy is named as the R4 winner: P-DIS if R4 passes, P-RAND
otherwise.

INCONCLUSIVE, not a pass: both policies reach 8/8 coverage on at
least 10 of the 12 seeds. The 24-round budget is then too generous
to discriminate; the preregistered follow-up re-runs with a 12-round
budget as a separate wave. R1 is blocked until that follow-up lands.

## 7. Determinism and purity (frozen)

3/3 byte-identical runs required (identical md5 across runs, zero
stderr). Fixed seeds only. Pure Zag at every stage: implementation,
build, run, verification, analysis. Zero Python anywhere, including
scratch and byte checks. Zero em/en dash bytes (verified with shell
grep byte patterns only, before commit).

## 8. Implementation plan (post-prereg)

r4.zag = the full altexp.zag machinery copied verbatim (allocation
helpers, RNG, sealed(5), node/signature/beam functions, passive,
select_iv, select_iv_rand, do_iv) with fn main replaced by the R4
driver: for each of the 12 frozen seeds, run the P-DIS evidence loop
and the P-RAND evidence loop (each starting from the seed), compute
combo coverage per arm, emit per-seed coverages, then emit aggregate
sums, mean margin, and paired win count. No other logic change.

## 9. Kill bars

K1: this prereg committed alone before any R4 implementation; commit
order verified. K2: 12 paired seeds complete, 3/3 byte-identical.
K3: pure Zag, deterministic, zero Python.

Verdict labels: R4-PASS or R4-FAIL (or INCONCLUSIVE per section 6).
