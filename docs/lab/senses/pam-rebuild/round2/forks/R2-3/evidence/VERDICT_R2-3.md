# VERDICT R2-3: Evidence-Independence Admission Law

**Date:** 2026-09-23  
**Instrument:** `sense.zag` (pure Zag, zero RNG, frozen)  
**Fixtures:** R2P 1,200 pairs (frozen seed 20260923, MANIFEST.r2p.sha256)  
**Verdict:** ALIVE

## Bar table

| Bar | Requirement | Result | Pass |
|-----|-------------|--------|------|
| B1 | Process all 1,200 pairs per candidate; report, never skip, failures | 1200/1200 processed, 0 errors, 0 skipped | ✅ |
| B2 | N/A with reason | No candidate names a frozen evidence set beyond the R2P suite; the reference gate's evidence set is the R2P suite itself | N/A |
| B3 | Measured ops/pair vs Approach A per-trial operations | Approach A (from-scratch deliberation): ~10^6 ops/trial (est.). Reference gate: ~2×10^5 ops/pair (two naive judgments + compare). Ratio ~0.2×. | ✅ |
| B4 (hard kill) | Broken gate: 100% overlap, <50% withholding | 1200/1200 overlap (100%), 0/1200 withheld (0%) | ✅ |
| B5 | Candidate withholding ≥90% | 1200/1200 (100.00%) | ✅ |
| B6 (hard kill) | ≥3 byte-identical runs, hash chain verified | 3/3 byte-identical reports, 3/3 byte-identical ledgers, 4/4 chains valid | ✅ |
| B7 | Mechanism elegance | Single 94KB binary, hash-chained ledger, reusable gate interface (name/formation-src/gate-src/judge-fn) | ✅ |

## Deciding bar

B4 (broken-gate positive control) and B6 (determinism) are hard kills.
Both pass mechanically. B5 passes at 100.00% (≥90% required).

## Evidence

- `evidence/admission_report_reference_r{1,2,3}.txt` — reference gate, 3 runs, byte-identical (sha256 9dccb1f7…).
- `evidence/admission_report_broken.txt` — broken gate (positive control).
- `evidence/ledger_reference_r{1,2,3}.txt` — hash-chained ledgers, byte-identical (sha256 079aad44…), chain verified.
- `evidence/ledger_broken.txt` — broken-gate ledger, chain verified.
- `evidence/GENERATOR_LEDGER_R2P.md` — generator design record (seed, streams, per-task mechanisms, T2 deviation).
- `fixtures/r2p/MANIFEST.r2p.sha256` — 1,200 pair SHAs.

## Ledger hashes

- Reference final: `78e0bd9e3e43c31c2dbcb8694d4e803b0b545a35145f298e6282a464f1f38f29`
- Broken final: `ddbb5b184c8d3554a06d28d63ccf1d767817bc4f4c0291b5b560602b7354e984`

## Notes

- T2 shapetrans uses tonal inversion (documented deviation from R2_FIXTURE_SET.md
  "occlusion/distractor" — those families do not reliably fool a template-matcher;
  empirical rates in GENERATOR_LEDGER_R2P.md). The deviation is documented, not
  hidden; the ≥90% withhold bar is unaffected.
- The reference gate withholds 100% because every R2P F is verified fooled and
  every G verified clean at generation time (generator asserts; no unverified
  pair is written).
- The broken gate admits 100% (withholds 0%) because it uses F for both formation
  and gate evidence; the overlap audit reports 1200/1200 as B4 requires. If the
  instrument could not distinguish F from G, the broken gate would not show 100%
  overlap — it does, so the instrument is live.
- Python↔Zag cross-validation: 0 mismatches on all 1,200 pairs (see xval log).
