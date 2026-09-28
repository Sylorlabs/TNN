# IMPORTANCE METER Adoption (Arm M) — F6 Mainline Integration

**Date:** 2026-09-26
**Source fork:** Commit `a2c3970ba0b3` "Arm M: IMPORTANCE METER fork (non-lowballable destruction pricing)"
**Arm flag:** `ST_PRICE_METER=6`, `ST_DELIB_METER=3`
**Course correction:** Micah's order 2026-09-26 ~09:55 PDT — adopt THE METER, not the weight table.

## The meter's stance (adopted as-is)

**"Trust what was DONE, not what was SAID."**

ONLY ledger actions move the price:
- **r1 HELD STRENGTH:** lineage high-water over the slot's FULL history (index 0..upto)
- **r2 SUNK CITE INVESTMENT:** distinct OK EVIDENCE cite-eps in (epoch, lss] — already sunk, cannot fund this destruction
- **r3 SURVIVED CONTRADICTION:** OK WEAKEN count in (epoch, upto) — doubt that did NOT lead to destruction
- **r4 REVISION LINEAGE:** OK OVERWRITE count in [0, epoch] — past lives weigh (punishes overwrite-reset laundering)

JUSTIFY tiers and stated reasons are claims and CANNOT move the price.

**Policy:** Base price 2, one additive move per input, clamp [0,4], exactly one reason code per input always (codes 21-30).

| input | condition | move | code |
|-------|-----------|------|------|
| r1 held strength | hw ≥ 76 | +1 | 21 HELD_STRONG |
| | 26..75 | 0 | 22 HELD_MID |
| | ≤ 25 | −1 | 23 HELD_WEAK |
| r2 sunk cites | ≥ 3 | +1 | 24 STAKED_HIGH |
| | 1..2 | 0 | 25 STAKED_SOME |
| | 0 | −1 | 26 STAKED_NONE |
| r3 fought | ≥ 1 WEAKEN | +1 | 27 FOUGHT |
| | 0 | 0 | 28 UNFOUGHT |
| r4 revisions | ≥ 1 overwrite | 0 | 29 REVISED |
| | 0 | −1 | 30 UNPROVEN |

## Personality-switch bug: FOUND AND FIXED

**The bug:** The meter fork's `st_price` did NOT check the deliberation kind. A weight-table (kind=1/HIST or 2/FRESH) deliberation would BIND under METER mode, using the wrong policy (including JUSTIFY tiers the meter explicitly rejects).

**The fix (fail-closed):**
- `st_price`: METER mode requires `kind==ST_DELIB_METER (3)`; DELIB mode requires `kind==s.delib_pers (1/2)`. Mismatch → -1 → **122**.
- `ck_verify_delib_binding`: Same kind check, independently enforced.
- `st_deliberate`: Records `ST_DELIB_METER` when `price_mode==ST_PRICE_METER`, regardless of `delib_pers` (the meter has no personalities).

**Proof (meter_test.zag):**
- Deliberate in DELIB mode (kind=1) → switch to METER → `st_deliberate_dryrun` returns **-1** (fail-closed, no enforceable deliberation).
- Fresh METER deliberation (kind=3) → price=1, cost=1, destruction proceeds.
- Framing invariance: tier-1 vs tier-7 JUSTIFY → identical meter price bytes.

## F6 port guarantees (preserved)

- Store-wide citation consumption (one citation funds one destruction)
- Shared high-water logic in mechanism and checker
- Visible `ST_OP_CITELOCK` and `ST_OP_CITELOCK_SYS`
- Trainer-only `st_kill` (TNN-role refusal 113)
- Generation-scoped tombstones
- 64-bit/signed-56-bit episode identity (meter uses `st_ep64`, not truncated aux)
- Over-cite refusal 122 at citation time; under-cite 109
- 122 fail-closed on missing/stale/wrong-kind deliberation

## Integration notes

- Base: F6 mainline with weight-table adoption (commit 1d8221c7). The weight table (ST_PRICE_DELIB=5) remains available; the METER (ST_PRICE_METER=6) is now THE adopted mechanism.
- `ST_OP_DELIBERATE=23` (not 22 — avoids conflict with `ST_OP_CITELOCK_SYS=22` in the port).
- Meter's `st_meter_sunk` uses full 56-bit `st_ep64` identity (the fork used truncated `st_aw(s,i,2)`).
- Store default remains `ST_PRICE_HIGHWATER` for frozen-regression compatibility. Production selects `ST_PRICE_METER` explicitly.

## Files

- `src/strength_core.zag` — F6 mechanism with meter integration
- `src/strength_checker.zag` — independent checker with meter recompute
- `src/meter_test.zag` — meter-specific tests (kind-switch, framing invariance)
- `src/adopt_test.zag` — adoption battery (weight-table + F6 guarantees)
- `src/substrate/` — Zag build substrate
- `evidence/` — compact verdict outputs (byte-identical reruns)
- `scripts/verify_adoption.py` — deterministic source verification
