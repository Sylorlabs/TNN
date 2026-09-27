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

## G1 registration — candidate id 2 (selfpam-fact-gate), 2026-09-27

Under self-PAM prereg amendments 2026-09-27-A (registration) and 2026-09-27-B
(verifier low-byte masking). Build: pinned znc
(`498abcb5…7e58ef`) → `sense_bin` `1db54a68…fca74`, reproduced byte-identically
from the committed sources. Corpus: 1,200/1,200 `.pair` SHAs verified OK
against the frozen `MANIFEST.r2p.sha256`.

| Run | Gate | Pairs | Withheld | Overlap | Ledger final |
|-----|------|-------|----------|---------|--------------|
| selfpam r1 | selfpam-fact-gate (2) | 1200/1200, 0 err | 1099 (91.58%) | 0 | 644c61f0…45905 |
| selfpam r2 | selfpam-fact-gate (2) | 1200/1200, 0 err | 1099 (91.58%) | 0 | 644c61f0…45905 |
| selfpam r3 | selfpam-fact-gate (2) | 1200/1200, 0 err | 1099 (91.58%) | 0 | 644c61f0…45905 |

r1/r2/r3 reports byte-identical; ledgers byte-identical. All 3 hash chains
verified by the patched `mirror/verify_ledger.py` (masks judgment codes
`& 0xFF` exactly as the Zag writer does). B5 PASS (91.58% ≥ 90%), overlap
kill check PASS (0), B1 PASS (0 errors), B6 PASS.

Regression on the same corpus: id 0 report+ledger byte-identical to the
committed `admission_report_reference_r1/r2/r3.txt` + `ledger_reference_r1/r2/r3.txt`;
id 1 report+ledger byte-identical to `admission_report_broken.txt` +
`ledger_broken.txt`; both chains re-verified (masking is a no-op for ids 0/1).

Scope: registration acceptance only (PREREG §5.5 — not CELL-A). §8 blockers
remain open; DEMO_ONLY scope unchanged. Full record:
`evidence/BUILD_RECORD_G1_ID2.md`.
