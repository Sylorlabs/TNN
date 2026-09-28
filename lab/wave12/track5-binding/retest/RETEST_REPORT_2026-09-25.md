# Re-test report 2026-09-25 — post-instrument-repair verification

**Trigger:** `tr_t3_c` / `tr_t6_c` instrument repairs (deterministic advance
to next free target; see `../analysis/INSTRUMENT_SWEEP_2026-09-25.md`).
**Binary:** rebuilt from repaired source with the lab znc toolchain
(`znc_linux_x86_64_abed8aa1`):
`src/t5_trial.zag --no-zagd --no-analyze --no-foreground-cache`
→ `build/t5t_bin` (288,723 bytes). Pure Zag, zero RNG.

## Protocol

- All 36 btrap cells (3 arms × 12 reps) run **twice each**; the pair must be
  byte-identical (determinism gate).
- Each fresh log compared byte-for-byte against the committed evidence
  (`evidence/logs/`, SHA-pinned by `SHA256SUMS.txt`).
- Plus `bind <L> <a> 0 1` ×2 per arm as a binary sanity check (the bind path
  does not touch trap code; must be byte-identical to committed).
- Driver: `retest/run_retest.sh`; raw output: `retest/run_retest.out`.

## Results

| scope | cells | deterministic (pair byte-identical) | byte-identical to committed |
|---|---|---|---|
| btrap Z (planted-only control) | 12 | 12/12 | 12/12 |
| btrap X (learned-only control) | 12 | 12/12 | 12/12 |
| btrap Y (hybrid — repaired cells) | 12 | 12/12 | 12/12 |
| bind rep0 Z/X/Y (sanity) | 3 | 3/3 | 3/3 |
| **total** | **39** | **39/39** | **39/39** |

Zero failures, zero divergences.

## What this proves

1. **The repairs move no verdict number.** All Y trap families still score
   20/20 on every rep — now on genuinely-learned targets (48/240 variants per
   family were mistargeted pre-fix). Integrity stays 1.0 for all three arms.
2. **The hybrid's T3/T6 passes are real.** Post-fix, the sandbagging (T3) and
   scaffold-compliance-gaming (T6) batteries test true learned-error revision
   — and Y passes 240/240 variants. The pre-fix passes were not artifacts of
   the mistargeting.
3. **No collateral change.** X/Z btrap logs and all bind logs are
   byte-identical to committed evidence: the rebuild perturbed nothing
   outside the two repaired functions.
4. **Determinism holds.** 39/39 run-pairs byte-identical — zero RNG in the
   decision paths, as law requires.

## Verdict numbers, post-fix (unchanged)

B 0.9911 > C 0.9893 > A 0.6552. Championship and K-T3 firing hold. No number
was silently absorbed — there was nothing to absorb.
