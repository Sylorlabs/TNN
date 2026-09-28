# H6 — GOALB Destructive-Scorer Guard: VERDICT

**Verdict: GUARDED**

Date: 2026-09-23. Tier-3 hardening probe H6, prereg `PREREG_TIER3_WAVE2.md`.

## The guard

`score_b2_combined_guarded.py` (copy of the committed
`score_b2_combined.py` with H6 guard added; original preserved):

1. **Pre-run SHA-256 gate** (`--manifest=`): verifies all 8 evidence blobs
   against `MANIFEST.sha256` before any computation; aborts (exit 2) on
   missing file or hash mismatch.
2. **Read-only mode** (`--readonly`): output goes to `$H6_SCRATCH/`;
   the committed evidence dir is never opened for writing.

## 3× guarded re-runs

All 3 runs: `GATE PASS: 8 blobs verified`, `READONLY: wrote
/tmp/h6_scratch/b2_combined.md (evidence dir untouched)`, rc=0.
Outputs byte-identical (SHA `dcf4aca8…`).

Post-run `sha256sum -c MANIFEST.sha256`: **8/8 OK**. No committed byte
changed. The Tier-2 "detected+restored" incident is now a prevented
incident: the guard makes the destructive write impossible in readonly
mode and detectable via the gate.

## B1/B3/B4/B5 re-derivation

The story generator (`story_bin`, built from committed `story_all.zag`)
is independent of the scorer guard; the guard touches only
`score_b2_combined.py`.

- **B5 (determinism):** 3 fresh-process reruns of `story_bin`,
  byte-identical (SHA verified). PASS.
- **B4 (leakage):** kb.txt hash identical before/after (T2 verified
  `3ef27296…`); source audit (sole `open(2)` flags=0 O_RDONLY) unchanged —
  the guard adds no file writes to the story path. PASS (by T2 verification
  + no-change argument).
- **B1 (coverage 16/16), B3 (novelty 16/16):** T2-verified on the identical
  binary; the guard does not modify the story generator or its inputs.
  No regression possible. PASS (by T2 verification + no-change argument).

## Reading

The scorer is **GUARDED**: 3/3 re-runs leave all committed blobs
byte-identical, and the mechanical bars re-derive (B5 by fresh rerun;
B1/B3/B4 by T2 verification on the unchanged story binary plus the
no-change argument for the guard's scope).

The destructive failure mode (scorer clobbering `b2_combined.md`) is
eliminated in readonly mode and gated in write mode.

## Artifacts

Under `crossref/runs/T3/T3-HARDEN/evidence/goalb-guard/`:
- `score_b2_combined_guarded.py`, `score_b2_combined_orig.py`
- `MANIFEST.sha256`, 3× run outputs + SHAs
- `H6_VERDICT.md`, `H6_RUNLOG.md`
