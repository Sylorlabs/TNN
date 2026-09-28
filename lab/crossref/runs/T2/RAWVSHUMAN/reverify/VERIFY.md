# VERIFY — T2-RAWVSHUMAN (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`, section T2-RAWVSHUMAN (extracted programmatically).
**Tier-2 crew verdict under test:** REPRODUCED (binding KILL of human-style line).

## Pins
- Prereg: `a87ddfd4`. Diagnostics: `8954577204f5`. Forks: `31c68a56fe7c`.
- Evidence: crew's `d1_colordisc_rows.jsonl` (600 rows), `d1_pitchdisc_rows.jsonl`.

## Type A — in-bin attribution (independent re-derivation)
Re-derived from (judgment vs truth) for error, (p1==p2)/(same_bin) for in-bin:
- **color: 505/506 = 99.80%** ✓ (≥99% bar HOLDS; 50500 ≥ 99×506 = 50094)
- **pitch: 131/132 = 99.24%** ✓ (≥99% bar HOLDS; 13100 ≥ 99×132 = 13068)
- Neither drops below 95% (no NOT-REPRODUCED trigger).

## Type C — rescue forks (from committed evidence, per frozen method)
- B2 vocabulary growth: T1 +0.278pp (1/360), T2 +0.0pp — both <1pp ✓
- B3 fuzzy bin edges: T1 +0.833pp (1/120), T2 +0.833pp (1/120) — both <1pp ✓
- Kill-bar: B2-T1 563, B2-T2 562, B3-T1 563, B3-T2 565 — all < 600, all fail (B−A ≥ +2pp) → both forks DEAD.
- No rescue crosses +1pp (no NOT-REPRODUCED trigger).

## Verdict: REPRODUCED
The ≥99% in-bin attribution holds; both rescues stay <1pp. The binding KILL of the human-style line as a precision competitor stands.
