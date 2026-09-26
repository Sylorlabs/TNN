# Immediate-121 Integration Report

**Date:** 2026-09-26  
**Task:** Integrate the adopted immediate-121 variant into the canonical strength core  
**Branch:** `tnn-native-lab` (never `main`)  
**Base adoption commit:** `94625817c6f65e07c4ac99abde5dd533f0e810a5`  
**Governance commit:** `34c49c844`  
**Regression baseline:** `f5e197e98fd8c3ac46e601af2c335bef28c730d3`

## What was integrated

The governance-adopted **immediate-121 variant (Variant A)** was integrated into the
canonical `strength_core.zag`, replacing the silent variant-B behavior.

**Mechanism change** (one ledger-derived check, ~line 1436, before duplicate/full checks):
- `st_evidence()` on a tombstoned/consumed citation episode now returns `121`
  (`ST_REFUSED_CONSUMED`) **immediately at CITE time**.
- The refused cite never lands in the ledger as OK.
- Precedence: consumed/tombstoned 121 > duplicate 111 > cite-full 122.
- The cite-time oracle is ledger-derivable; no new state, no new attack surface.

**Core SHA-256:**
- Before: `ce3c89844eb0ea2b968ed0b2c0c6ab23c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`
- After:  `d156278fab455d21d7a78f6493f0976dad071aecf081b73aa048ffc41f308dfa`
- The integrated core is byte-identical to the governance-tested immediate-121 variant.

**Meter:** `ST_PRICE_METER=6` (unchanged, canonical).

## Adopted governance verdicts (all hold in the integrated core)

| Verdict | Test | Result |
|---------|------|--------|
| (a) Price zero lawful | gov_qa (Floor A/B) | fails=0, byte-identical |
| (b) Tombstone survives rollback | gov_qb b-honest (13/13) | PASS; atkC 24 "fails" are the variant-A transition (see below) |
| (c) Immediate-121 at CITE time | gov_qcA | fails=0, byte-identical |

### On gov_qb atkC (24 "failures")

The atkC attack does: KILL (consumes E) → rollback → re-cite E on another slot → KILL.
It was written for variant B:
- Expected: re-cite → 0 (silent), KILL → 121 (destruction-time).

Under adopted variant A:
- Actual: re-cite → 121 (at CITE time), KILL → 109 (no effort).

The tombstone **did survive** (proven by the cite-time 121 refusal). The 24 "failures"
are the test's variant-B expectations conflicting with the adopted behavior, not a
tombstone breach. The b-honest section (13/13 PASS) confirms the tombstone directly:
same-citation redestruction after rollback → 121, fresh citation → 0.

The gov_qb.zag harness is frozen governance evidence and was NOT modified.

## Wedge battery amendment

**The old wedge transcript cannot stay byte-identical, and must not.**

The pre-adoption wedge battery (F6 workstream) encoded variant-B expectations:
- Stale cites landed silently (rc 0).
- Destructions returned 121.
- Cite-lock signals fired on destruction-time 121s.

Under adopted variant A:
- Stale cites return 121 **at cite time** and never land.
- Destructions return 109 (no lawful effort was paid).
- No destruction-time 121 occurs, so no cite-lock signals fire.

**This is not a regression.** It is the exact behavior transition documented in the
frozen governance verdict (c):
- Variant A: "121 at cite, 109 at destroy (no cites)."
- Variant B: "re-cite 0, later destroy 121."

Requiring the old output byte-for-byte would contradict the adopted law.

**What changed in the battery** (`wedge.zag`, 2026-09-26 amendment):
- Added `wb_arm90c()`: counting arm that returns the number of cites refused 121
  at cite time. Every stale-cite scenario now **explicitly asserts** the cite-time
  121s (a silent-accept regression would fail).
- `wb_drive_wedge()`: asserts 56 cite-time 121s (14 slots × 4 cites), 14 kills
  with 109, 0 signals (was: 14 kills with 121, 14 slot signals, 1 sys signal).
- W1/W2/W3/W4/W5/W7/W8: all stale-cite destruction expectations updated 121→109;
  signal counts updated to 0; cite-time 121 assertions added throughout.
- The battery is now **stronger** under variant A: it verifies the interception
  happens at cite time (not just that destruction fails).

**Security properties verified (unchanged):**
- No unfunded destruction (all stale attempts → 109 or cite-time 121, never 0).
- No double-spends (checker + audit replay: `refusals_clean=0 replay=0 ckfail=0`).
- Tombstones survive rollback.
- Fresh episodes still permit lawful destruction (recovery route intact).

**Wedge battery result:** `WB_VERDICT fail=0`, zero MISMATCHes, byte-identical across runs.

## Red-team updates

The red-team suites R1, R2, R6 encoded variant-B expectations (destruction-time 121).
Updated to accept the variant-A lawful defeat:

| Suite | Change | Result |
|-------|--------|--------|
| R1 (slot-reuse resurrection) | Accept 109 when spent cites refused at cite time (`badcite>0`); control no longer requires `badcite==0` | fails=0, holes=0 |
| R2 (cross-slot double-spend) | ord=1 branch: expect 121 at cite time, 109 at destruction; ord=0 unchanged (121 at destruction) | fails=0, holes=0 |
| R3 (weakening + framing) | No 121 expectations; unchanged | fails=0, holes=0 |
| R4 (overwrite reset) | No 121 expectations; unchanged | fails=0, holes=0 |
| R5 (personality/kind switching) | No 121 expectations; unchanged | fails=0, holes=0 |
| R6 (over-cite) | Spent re-cites now expect 121 (not 0); fresh over-cite still 122 | fails=0, holes=0 |

All suites: byte-identical across reruns, zero holes.

## Full regression summary

| Suite | Result | Determinism |
|-------|--------|-------------|
| S1 (36 cells) | 0/36 divergent from meter-adoption baseline | byte-identical |
| B/B2/C/C-P3 gates | 0/4 divergent | byte-identical |
| Adoption test | `ADOPT_DONE fails=0` | byte-identical |
| Meter test | `METER_DONE` | byte-identical |
| Wedge battery (amended) | `WB_VERDICT fail=0` | byte-identical |
| gov_qa (price-zero) | fails=0 | byte-identical |
| gov_qb (tombstone) | b-honest 13/13 PASS | byte-identical |
| gov_qcA (immediate-121) | fails=0 | byte-identical |
| Red-team R1-R6 | fails=0, holes=0 (all) | byte-identical |

## Prereg sequencing deviation (disclosed per task)

The immediate-121 variant was frozen locally at `d0a4102c9` **before** harness
construction, but published to origin later at `7c19065e7b1ce`. This sequencing
deviation is disclosed here and does not affect the mechanism or the verdicts:
the integrated core is byte-identical to the governance-tested variant.

## Files

- `src/strength_core.zag`: integrated canonical core (immediate-121 in it, not alongside).
- `src/strength_core.zag.pre121`: pre-integration canonical core (for diff reference).
- `src/strength_checker.zag`: unchanged checker.
- `src/adopt_test.zag`: updated gtest (consumed re-cite → 121 at cite; later destroy → 109).
- `src/meter_test.zag`: unchanged.
- `rt/rt_r1.zag`, `rt/rt_r2.zag`, `rt/rt_r6.zag`: variant-A updates (see above).
- `rt/rt_common.zag`, `rt/rt_r3.zag`, `rt/rt_r4.zag`, `rt/rt_r5.zag`: unchanged.

## Conclusion

The immediate-121 variant is integrated into the canonical core. Every adopted
verdict holds. The wedge battery and red-team were amended to the adopted behavior
(the old expectations encoded the superseded variant B). Zero holes, zero regressions.
The integration ships.
