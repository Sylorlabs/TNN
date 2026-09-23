# Z3 Verdict

**Arm:** Z3 — Budgeted chunks (ECON)
**Date:** 2026-09-21
**Scale:** 1× (r1 corpora)
**10× status:** NOT ATTEMPTED (all 1× bars pass; 10× deferred to coordinator)

## Binding kill criteria (verbatim, byte-verified 2026-09-21)

> "Total cost not ≥20% below the best fixed-granularity arm at equal recall
> accuracy — the machinery buys nothing; OR halving B causes >15% accuracy
> drop for a 50% budget cut (pricing model wrong — cliff, not graceful
> degradation). **The prereg must state explicitly why fixed prices + hard
> budget ≠ reward signal (A-53).**"

## Kill-prong 1: Total cost vs best fixed-granularity arm

**Equal M1 (both corpora):**

| Arm | Prose recall/boundary | Code recall/boundary |
|---|---|---|
| Z3 (S=256/512) | 100.0 / 100.0 | 100.0 / 100.0 |
| b64 (S=64 fixed) | 100.0 / 100.0 | 100.0 / 100.0 |

M1 is equal. The fixed-granularity comparators (all at M1=100.0/100.0):

| Arm | Total cost (bytes) |
|---|---|
| b64 | 14,336,873 |
| b16 | 40,518,457 |
| b8 | 75,427,217 |

**Best fixed-granularity arm: b64** (lowest total cost at equal accuracy).
b64 is named as the best only after verifying all comparators — b16 and b8
are strictly more expensive.

**Z3 total cost** (frozen formula, ARM_SPEC.md §6):

| Component | Bytes |
|---|---|
| Slot table | 826,700 |
| Normal ledger (22,183 × 64B) | 1,419,712 |
| Economic ledger (43,368 × 32B) | 1,387,776 |
| Corpus buffer | 5,422,721 |
| **Total** | **9,056,909** |

- Ratio Z3/b64: **0.6317** (Z3 is 36.8% below b64)
- Bar: ≤ 0.80 × 14,336,873 = 11,469,498
- 9,056,909 ≤ 11,469,498 → **PASS** (kill NOT triggered)

The economic machinery buys a 37% cost reduction at identical recall: fewer,
coarser units (21,183 vs 84,731) priced by the fixed budget.

## Kill-prong 2: Half-B diagnostic (cliff vs graceful)

| Corpus | Full-B (B=4M) recall | Half-B (B=2M) recall | Span (full→half) | Drop |
|---|---|---|---|---|
| prose | 100.0 | 100.0 | 256 → 512 | 0% |
| code | 100.0 | 100.0 | 512 → 1024 | 0% |

Halving B causes **0% accuracy drop** (bar: >15%). The economic granularity
rule degrades gracefully by selecting coarser spans; there is no cliff.
**Kill NOT triggered.** The pricing model is correct.

## A-53: Fixed prices + hard budget ≠ reward signal

Stated explicitly in ARM_SPEC.md §2 (frozen pre-battery): no learned prices,
no optimization pressure, no gradient — the budget is a hard accounting
constraint with a fixed, audited, human-readable allocation rule. It is
accounting, not learning.

## Full M1–M9 row (1×, r1)

| Mode | Result |
|---|---|
| M1 prose | 100.0 / 100.0, 21,183 units, S=256, A15 swap 64/64 PASS |
| M1 code | 100.0 / 100.0, 18,585 units, S=512, A15 swap 64/64 PASS |
| M2 t1/t2/t3 | All tiers qualify from episode 1 (etc=1), not censored |
| M3 | 100.0 / 100.0, 8,050 mgmt entries, 50 weakens, freeze CLEAR |
| M4 prose/code | 100.0 / 100.0 boundary+content revisions, 0 kills |
| M5 | 21,183 units, total_cost 9,056,909 (see above) |
| M6 p2c / c2p | 100.0 / 100.0 / 100.0, 0.0 transfer tax (both directions) |
| M7 | 100.0 hit, 3.24 reuse (≥1.5 ✓), 0.50 dedup; A7/A8 placeholders provisional |
| M8 | PASS — byte-identical across 5 perturbations × 2 reruns |
| M9 | Descriptors recorded for t1 tiers (informational) |

Battery: 18/18 legs pass (each ×2 runs, stdout byte-identical). M8 gate:
PASS. Raw logs and raw `scorecard_assemble.py` output preserved in
`battery1x_v2/work/`; Z3-specific assembly in `scorecard_z3_1x.json`.

## Provisional / ambiguity disclosures

- **ID-arm classification:** PROVISIONAL-PENDING-FREEZE (Micah). A15 M1 probe
  implemented and passing (64/64); labeled provisional.
- **M7 A7/A8:** PROVISIONAL-PENDING-FREEZE. Uses the harness validator's
  unfrozen placeholders (C′ first-byte XOR 0xFF; lookups `(l*37)%nunits`
  split 1666/1667/1667). Repeated units use stable IDs (revive path); C′
  edits are in-place same-ID patches (declared, audited).
- **Dispatch corrections acknowledged:** (1) Original Token→chunk/XFER
  dispatch was wrong and discarded. (2) First corrected §3 quotation was a
  paraphrase; the second correction supplied the byte-verified verbatim row
  used here.

## Verdict

**SURVIVE.** Neither kill prong is triggered:
1. Z3's total cost is 36.8% below the best fixed-granularity arm (b64) at
   equal M1 — the machinery buys a real reduction.
2. Halving B causes 0% accuracy drop — graceful economic degradation, not a
   pricing-model cliff.
