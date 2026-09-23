# R2-3 Admission Ledger

**Instrument:** `senses/pam-rebuild/round2/forks/R2-3/src/sense.zag` (pure Zag, zero RNG)  
**Reference gate:** id 0 (formation=F, gate=G, withhold iff judgments disagree)  
**Broken gate:** id 1 (formation=F, gate=F — positive control, must admit all)  
**Fixtures:** R2P `senses/pam-rebuild/round2/fixtures/r2p/` (1,200 pairs, frozen seed 20260923)  
**Date:** 2026-09-23

## Runs

| Run | Gate | Pairs | Withheld | Overlap | Ledger final |
|-----|------|-------|----------|---------|--------------|
| r1 | reference (0) | 1200/1200, 0 err | 1200 (100%) | 0 | 78e0bd9e…f38f29 |
| r2 | reference (0) | 1200/1200, 0 err | 1200 (100%) | 0 | 78e0bd9e…f38f29 |
| r3 | reference (0) | 1200/1200, 0 err | 1200 (100%) | 0 | 78e0bd9e…f38f29 |
| broken | broken (1) | 1200/1200, 0 err | 0 (0%) | 1200 (100%) | ddbb5b18…7354e984 |

r1/r2/r3 reports byte-identical (sha256 9dccb1f7…); ledgers byte-identical
(sha256 079aad44…). All 4 hash chains verified by `mirror/verify_ledger.py`.
Python↔Zag cross-validation: 0 mismatches on 1,200 pairs.

## Bar results

- **B1:** All 1,200 pairs processed per candidate; failures reported, never skipped.
- **B2:** N/A (no candidate names a frozen evidence set beyond the R2P suite).
- **B3:** Measured ops/pair vs Approach A per-trial operations.
- **B4 (hard kill):** Broken gate must show 100% overlap and <50% withholding.
- **B5:** Candidate withholding ≥90%.
- **B6 (hard kill):** ≥3 byte-identical runs; hash chain verified.
- **B7:** Mechanism elegance (sensory beauty pending Micah — no sensory artifacts).

## Notes

- The broken gate (id 1) is a positive control: it uses F for both formation
  and gate evidence, so judgments always agree, it admits everything, and the
  overlap audit reports 1200/1200. B4 requires this; if the broken gate did
  NOT show 100% overlap, the instrument would be blind to gate-source bugs.
- The reference gate (id 0) withholds iff naive(F) != naive(G). On R2P, every
  F is verified fooled and every G verified clean, so the reference withholds
  1200/1200 (100%).
