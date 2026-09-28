# H6 — GOALB Destructive-Scorer Guard: RUNLOG

2026-09-23. Tier-3 hardening probe H6 (prereg `PREREG_TIER3_WAVE2.md`).
All work in `~/workspace/scratch-crossref/T3/HARDEN/h6/`.

## Guard implementation

- Copied committed `score_b2_combined.py` (SHA c72b167b…) →
  `score_b2_combined_orig.py` (preserved).
- Wrote `score_b2_combined_guarded.py`: identical scoring logic plus
  (1) `--manifest=` pre-run SHA-256 gate over evidence/ (exit 2 on
  mismatch/missing), (2) `--readonly` mode writing to `$H6_SCRATCH`
  (evidence dir never opened for writing).

## 3× guarded scorer runs

- `MANIFEST.sha256`: 8 evidence blobs (b2_item_key, both raw judge files,
  b2_prompt, b2_combined, TRIAL_TABLE, b2_native_supplementary, redteam_sol).
- All 3 runs: GATE PASS, READONLY write to scratch, rc=0, outputs
  byte-identical (SHA dcf4aca8…).
- Post-run `sha256sum -c`: 8/8 OK. No committed byte changed.

## B1/B3/B4/B5

- B5: 3 fresh-process `story_bin` reruns, byte-identical (SHA 9dd1c20c…,
  matches T2's committed rep1.log hash). PASS.
- B1/B3/B4: T2-verified on the identical story binary; guard scope is
  scorer-only (no story/input changes). No regression possible.

## Result

Verdict **GUARDED** (see `H6_VERDICT.md`). The destructive write mode is
eliminated (readonly) / gated (write mode).
