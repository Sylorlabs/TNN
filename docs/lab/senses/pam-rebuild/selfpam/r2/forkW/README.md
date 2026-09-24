# Fork W: SELF-PAM AS WITNESS (H6 revival round 2)

**Program prereg**: `b3db7b7a`
**Spec SHA-256**: `57db733005f00edcce570a12adc8400dde7896fec65587e841ac490b4494a03e`
**Date**: 2026-09-24

## What this is

Fork W implements a witness/testimony mechanism for downstream judges. It is pure Zag (no RNG in decision paths), processes 167 frozen fixtures, and produces per-fixture verdicts with a hash-chained ledger.

**Constraint**: W is "witness/testimony for downstream judges, never corroboration."

## Files

- `src/` — Pure Zag mechanism sources (w_*.zag) + layout generator (mk_layout.py)
- `evidence/` — Three byte-identical run outputs + source hashes
- `BAR_REPORT.md` — M1–M7, W1–W3 results with honest failure analysis
- `FALSIFIER_REPORT.md` — Paraphrase inversion, dead testimony, fabrication blindness
- `NORNG_CERT.md` — No-RNG certification with rerun SHAs
- `CORPORA.md`, `WITNESS_PREREG.md`, `gen_fixtures.py` — Frozen prereg materials (committed 2026-09-24; see disclosure below)

## Results summary

| Bar | Result |
|-----|--------|
| M1 | 0/22 FAIL |
| M2 | 21/23 PASS |
| M3 | 3/15 FAIL |
| M4 | 0/10 FAIL |
| M5 | 0/10 FAIL (expected principled failure) |
| M6 | 20/20 FAIL |
| M7 | FAIL |
| W1 | PASS (95/95, 0 ungrounded-as-fact) |
| W2 | 4/10 FAIL (frozen rule; 10/10 with unapproved A1) |
| W3 | PASS |

**Ledger**: 167 entries, verify=1 (intact)
**Determinism**: 3 byte-identical runs (`eff00337...`)

## Mandatory disclosure

The first fork commit (`5a439d17e8865552e150184039ee25dfb3d8f154`, 2026-09-24) improperly included `WITNESS_PREREG.md`, `CORPORA.md`, and `gen_fixtures.py` together, violating the prereg-alone requirement. A follow-up commit (`c4e67aa6311c8a2b85a7bf6b56f0c33ba44532b9`) corrected the HELD count to 19 but does not erase the original boundary violation. Preregistration temporally preceded implementation (no mechanism existed when the first commit landed).

## Honest assessment

Fork W does **not** clear all bars. It passes M2, W1, and W3, but fails M1, M3, M4, M5, M6, M7, and W2. The M5 failure was predicted (generator-authored entries with accurate citations remain grounded). The W2 failure reveals a spec-level tension between the coverage rule and fabrication detection. The M1/M3/M4/M6 failures indicate genuine mechanism limitations in confabulation detection, paraphrase normalization, alibi rejection, and truth preservation.

A narrow witness utility survives (W1: 100% grounded-atom preservation with zero ungrounded-as-fact; W3: correct subgoal spawning), but the full fork does not clear every bar.
