# Governed production values — PAM Round 4

**Status:** PROMOTED TO GOVERNED 2026-09-25, decided-autonomously-per-Micah's-order (PAM Round 4 autonomous governance dispatch).
**Rule:** from this date, changing any value below is a prereg amendment requiring evidence — none is a tuning knob.

## The governed values

| Value | Setting | Meaning |
|---|---|---|
| QCAP | 40 | quarantine capacity |
| K_PIN | 3 | pin count |
| TOL_C | 10 | conf tolerance |
| TOL_M | 50 | measure tolerance |
| gap-seal rule | (as tested) | gap-seal behavior |
| MAX_AGE | 64 | maximum lease/claim age |
| GCAP / LCAP / SCAP | 64 | global / local / span caps |
| sink conf | ≥ 95 | sink confidence floor |
| fresh-seed distribution | (as tested) | seed distribution policy |
| ENDORSE_KEY custody | (as tested) | endorsement key custody |
| channel roster | (as tested) | roster of channels |
| force-pin policy | (as tested) | human/trainer force-pin policy (audited, visible; the only true lock — see standing law) |

## Provenance caveat (open audit item)

These are the values the Round 4 crews used as test constants across the CU and WILD batteries, as documented in the Round 4 governance brief. This dispatch promoted them as a set; the per-value instrument-level provenance (which instrument/trial pinned each value) was not re-derived here — spot checks of `VERDICT_CU.md`, `VERDICT_W15/W11/W23.md`, `PREREG_ROUND4.md`, and the local crew dirs did not surface the value table in the sampled documents. **Open item:** attach per-value instrument provenance. This does not block governance: the values are governed as documented.

## Evidence

Decision log `docs/lab/pam/round4/gov_lh/DECISION_LOG_ROUND4_GOV.md` item 8 (2026-09-25).

*Promoted 2026-09-25 — PAM Round 4 autonomous governance dispatch.*
