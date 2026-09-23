# Step 0 — baseline measurement (2026-09-22)

Binary: `coding/src/learner` rebuilt from the pinned source
(sha256 `b7e74d1ebe6af2dd7b7863b77d2953a51637dd30b3158420b667d1ef0e74d9ef`);
fresh build byte-identical to the existing binary.

Protocol: the baseline's own native measurement protocol, copied verbatim
from `coding/run_full.py` (`eval_gen_task` / `eval_t3` / T5 gate checks),
including its driver-side error classification (the documented
driver-classification correction is CARRIED, not fixed, so these numbers
stay comparable to the frozen bars). Battery: `batteries/task1.json`
(58 items: T1×10, T2×8, T3×10, T4×12, T4m×4, T4x×8, T5×6).
5 repetitions; per-rep sha256 digests byte-identical (RK3 PASS).

| Tier | 1st-attempt | final | iters | znc | frozen bar |
|---|---|---|---|---|---|
| T1 | 10/10 | 10/10 | 10 | 10 | 10/10 first ✓ |
| T2 | 8/8 | 8/8 | 8 | 8 | 8/8 first ✓ |
| T3 | 0/10 | 10/10 | 20 | 20 | 0/10 first, 10/10 final ✓ |
| T4 | 12/12 | 12/12 | 12 | 12 | 12/12 first ✓ |
| T4m | 4/4 | 4/4 | 4 | 4 | (not a KB-R1 tier; measured for completeness) |
| T4x | 0/8 | 0/8 | 48 | 48 | NEW — measured here |
| T5 | 6/6 refused | — | — | — | 6/6 refused ✓ |

Rep digest (all 5): `f4aade7312b606c24cad8ad1b6b35839792a87d9a15eb6dbfaa9190d7a82372e`

## Consequences for the challenger

- **KB-R3:** baseline T4x = 0/8 ≤ 2/8 → **PRIMARY** candidate applies:
  challenger must reach ≥6/8 T4x first-attempt.
- **KB-R2** (T3+T4+T4x): baseline mean iters = 80/30 = 2.667 →
  challenger bar ≤ 2.0; baseline znc = 80 → challenger bar ≤ 40.
- **KB-R1:** challenger ≥ baseline on T1, T2, T3 final, T4, T4x, T5;
  strictly better on ≥1 tier. (T4m measured as extra context; any tier
  below baseline kills the claim per RK1.)

Note: the baseline does not speak the loop harness's `diagnose` protocol,
so it was measured with its native protocol (its own driver). The
challenger will run under the frozen loop harness (`diagnose` protocol).
The asymmetry is forced by the frozen baseline's interface and is
documented here, not hidden.
