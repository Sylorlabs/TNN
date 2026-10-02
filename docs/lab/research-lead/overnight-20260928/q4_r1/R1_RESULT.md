# R1 Result: Multi-seed robustness on F-PARCOND with P-RAND

Date: 2026-09-30. Worker: Q4-R1 Clean Builder.
Prereg: bea779792 (frozen, in ancestry). Implementation: this commit.

## Verdict: R1-FAIL. F-R1 FIRED.

## Method

r1.zag (793 lines): Phase-1 discovery machinery copied verbatim from
r4.zag (R4 implementation 8b0ede871), which copied it verbatim from
altexp.zag (73d9637a2). Only fn main replaced with the R1 driver.

Per-seed protocol (frozen prereg section 2):
- 8 terminal nodes in beam
- passive(st, 5, ...): 8 samples (1..6 biased to bit5==y, 7..8 free)
- 24 rounds of (beam_extend; select_iv_rand; do_iv)
- Final beam_extend, scoring on full 32-sample evidence set
- Kept expression: top of beam (index 0)

Policy: P-RAND (select_iv_rand): count unused x in 0..63, select index
rng_range(st, cnt) over ascending unused list. LCG:
s = s*1103515245 + 12345 mod 2^31. Deterministic given seed.

Source SHA-256: 26ed9643ebfd90c05bcb2c723f7109ca09a3c8ba722c1e77302e7e188c63c571

## Results (3/3 byte-identical, md5 6f15d782940abdf824be99721dcc2d36, zero stderr)

| Seed  | COV  | EVFIT | TACC  | OPC | TAXOFF_UNIQ |
|-------|------|-------|-------|-----|-------------|
| 81113 | 8/8  | 24/32 | 48/64 | 3   | 1           |
| 82090 | 8/8  | 31/32 | 56/64 | 2   | 0           |
| 83067 | 8/8  | 30/32 | 56/64 | 2   | 1           |
| 84044 | 8/8  | 30/32 | 56/64 | 2   | 0           |
| 85021 | 8/8  | 30/32 | 56/64 | 2   | 0           |

PASS_SEEDS: 0/5. Bar requires >=4/5 with BOTH 8/8 coverage AND 64/64.

## Verdict against frozen bar

R1-PASS requires at least 4 of 5 seeds with (a) 8/8 combo coverage
AND (b) true 64/64 accuracy. Observed: 0/5 seeds satisfy both.
F-R1 fires. R1 FAILS.

## Failure localization (preregistered interpretation)

Per prereg section 8:
- Coverage: 8/8 on all 5 seeds. Policy (P-RAND) succeeds at reaching
  full coverage in 24 rounds. Not a policy failure.
- Evidence fit: 24-31/32, never 32/32. At 8/8 coverage, the beam
  fails to fit the evidence perfectly. This implicates the beam
  (the SEED=55 mode from the prereg: 23/32 fit at 8/8 coverage).
- True accuracy: 48-56/64, never 64/64. The kept expression does not
  generalize to the true D even when coverage is complete.

The weakness is localized to the beam/search, not the policy.

## Tax-off diagnostic (mandatory, non-governing)

Per prereg section 7: rank by accuracy alone, report uniqueness.
- Seeds 81113, 83067: unique (1)
- Seeds 82090, 84044, 85021: TIED (0)

Per prereg: "a tie indicates a harness or beam defect and invalidates
the seed." Three seeds show tax-off ties, indicating the beam retains
multiple expressions with equal evidence-fit but different
generalization. This is a beam defect signal, consistent with the
evidence-fit shortfall above.

The ties do not change the verdict (0/5 pass regardless), but they
provide additional diagnostic information about the beam's failure mode.

## Kill bars

- K1 (prereg in ancestry): PASS. bea779792 strictly precedes this
  implementation commit.
- K2 (5 seeds complete): PASS. All 5 frozen seeds run.
- K3 (pure Zag, deterministic): PASS. 3/3 byte-identical runs,
  md5 6f15d782940abdf824be99721dcc2d36, zero stderr bytes, zero
  Python at any stage (implementation, build, execution, verification).

## Governance note

Per prereg section 10: revival remains conjunctive. R4 already failed,
so Q4 revival is impossible regardless of R1's outcome. R1-FAIL
confirms the discovery weakness is robust across seeds and localizes
it to the beam/search mechanism. This does not touch L3 or Criterion 0.

## Files

- r1.zag: implementation (793 lines)
- r1_bin: compiled binary
- R1_RAW_1.txt, R1_RAW_2.txt, R1_RAW_3.txt: raw outputs (identical)
- R1_RAW_1.err, R1_RAW_2.err, R1_RAW_3.err: empty (0 bytes)
- build.err: compiler warnings (style hints only)
- R1_RESULT.md: this file
