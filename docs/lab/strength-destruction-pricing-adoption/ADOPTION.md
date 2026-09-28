# Deliberative Pricing Adoption — "Destruction Costs, But Not Always The Same"

**Hypothesis (Micah, 2026-09-26):** DESTRUCTION COSTS, BUT NOT ALWAYS THE SAME.

**Status:** ADOPTED into F6 mainline as the deliberative destruction-price mechanism.
**Date:** 2026-09-26
**Branch:** `tnn-native-lab`
**Source base:** `docs/lab/wave8/strength-retrial/port-fix-2026-09-26/implementation/` (commit `c442e892fa0a`)

---

## 1. What was adopted

Deliberative pricing (`ST_PRICE_DELIB=5`) is now the F6 mainline destruction-price
mechanism. Before TNN (or a trainer) destroys a memory, TNN must **deliberate**:
look at the ledger, weigh the evidence, and commit to a price. That price binds
the destruction. No deliberation → no destruction (fail-closed, rc=122).

The fork's hand-authored weights are preserved **unchanged**:

| Input | Rule (unchanged) |
|---|---|
| Base | 2 |
| Strength high-water | ≥76: +1; 26–75: 0; ≤25: −1 |
| Prior distinct citations | ≥3: +1; 1–2: 0; 0: −1 |
| Max JUSTIFY tier | ≥6: +1; 3–5: 0; 1–2: −1; no trail: 0 |
| Stated destruction reason | 7: override to 4; 3 or 4: −1; else 0 |
| Final | Clamp 0–4 |

All inputs are ledger-derived (no external signals, no RNG).

## 2. The personality fix (fail-closed)

**Problem:** The fork recorded a deliberation under one personality (HISTORY-SEEING
vs EPOCH-FRESH). If the personality was switched afterwards, the old deliberation
could bind under the new personality — a stale deliberation granting a discount
it was never computed for.

**Fix (adopted):** The binding is personality-aware at three independent layers:

1. **Mechanism (`st_price`):** Finds the latest in-window successful deliberation.
   Its recorded personality must equal the store's current `delib_pers`.
   Missing, stale, wrong-slot, or mismatched → undefined price → **122**.
2. **COST (`st_deliberate_dryrun`):** Reports the enforceable bound price, or **-1**
   on mismatch (was: recomputed a potentially discounted price under the new
   personality).
3. **Checker (`ck_verify_delib_binding`):** Independently requires current/recorded
   personality agreement; refuses the ledger otherwise.

**Result:** Deliberate under P1 → switch to P2 → destroy → **122, never a discount.**
A fresh deliberation under P2 restores lawful destruction at the recomputed price.

## 3. What was preserved

- **Store-wide citation consumption** (GLOBAL mode): cites burn store-wide;
  double-spend refused (121).
- **Shared high-water logic** in mechanism and checker: `ST_PRICE_HIGHWATER=0`
  remains the store default so frozen pre-adoption drivers are byte-identical.
  Production drivers select `ST_PRICE_DELIB` explicitly.
- **Visible citation-lock signals** (`ST_OP_CITELOCK`, `ST_OP_CITELOCK_SYS`).
- **Trainer-only `st_kill`** (role gate 113; trainer path uses the same priced
  effort check).
- **Generation-scoped tombstones** (slot reuse can't resurrect spent cites).
- **64-bit episode identity** (signed 56-bit; valid 0..2⁵⁵−1; refused at ≥2⁵⁵).
- **Over-cite refusal** (122 at CITE time, before the epoch bricks).

## 4. Operation numbering

- `ST_OP_DELETE_STRONG=20`, `ST_OP_CITELOCK=21`, `ST_OP_CITELOCK_SYS=22`
  (unchanged).
- **`ST_OP_DELIBERATE=23`** (adopted).

## 5. Verification

See `EVIDENCE.md` for the full pre/post regression table.

- 36-cell S1 matrix × 2 passes: byte-identical to pre-adoption.
- Gates B/C/C-P3/B2 × 2 passes: byte-identical.
- Wedge battery × 2 runs: `WB_VERDICT fail=0`, byte-identical.
- Adoption battery (51 checks): all pass, including the explicit
  personality-mismatch → 122 test.
- Pure Zag, zero RNG, deterministic.

## 6. Tree location

```
docs/lab/strength-destruction-pricing-adoption/
  src/strength_core.zag        — adopted mechanism
  src/strength_checker.zag     — adopted checker
  src/substrate/               — trial substrate
  src/strength_trial.zag       — F6 trial driver (frozen)
  src/port_stress.zag          — stress driver
  src/port_wedge_battery.zag   — wedge battery
  src/adopt_test.zag           — adoption verification battery
  scripts/merge_adopt.py       — deterministic merge script
  ADOPTION.md                  — this document
  EVIDENCE.md                  — verdict evidence + pre/post table
  evidence/                    — compact logs, manifests, SHAs
```
