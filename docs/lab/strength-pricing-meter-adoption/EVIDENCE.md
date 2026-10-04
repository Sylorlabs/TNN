# Meter Adoption Evidence

**Date:** 2026-09-26
**Mechanism:** IMPORTANCE METER (ST_PRICE_METER=6), integrated into F6 mainline

## Regression results

| Suite | Result |
|-------|--------|
| S1 matrix (B/C/C-P3/B2 × VUP/WBS/JI × 0/1/2) | 36/36 byte-identical to pre-adoption |
| Gates B/C/C-P3/B2 | 8/8 byte-identical (4 gates × 2 passes) |
| Wedge battery | Byte-identical to baseline; deterministic ×2 |
| Adoption battery (adopt_test) | 50/50 pass; deterministic ×2 |
| Meter tests (meter_test) | 8/8 pass; deterministic ×2 |

## Personality-bug disposition

**Status:** BUG FOUND IN FORK, FIXED IN ADOPTION

The meter fork (a2c3970b) did not check deliberation kind in `st_price` — a
weight-table deliberation (kind=1/2) would bind under METER mode. Fixed with
fail-closed kind check: METER requires kind=3, DELIB requires kind=delib_pers.
Mismatch → -1 → destruction returns 122, never a discount.

**Proof:**
- `m2_cost_mismatch`: DELIB-kind deliberation + METER mode → dryrun = -1 (PASS)
- `m3_cost`: Fresh METER-kind deliberation → dryrun = 1, destruction proceeds (PASS)
- `m4_framing_invariant`: Tier-1 vs tier-7 JUSTIFY → identical price (PASS)

## Determinism

- Pure Zag, zero RNG (no RNG calls in mechanism or checker).
- All batteries byte-identical across reruns (×2 minimum).

## Source SHAs (SHA-256)

See `evidence/SHA_MANIFEST.txt` for the full manifest.
