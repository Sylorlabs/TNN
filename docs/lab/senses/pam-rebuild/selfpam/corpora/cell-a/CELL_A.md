# CELL-A — R2-3 acceptance corpus (pinned, not duplicated)

**Cell:** CELL-A — R2-3 acceptance instrument (§3.2 of the frozen prereg).
**Authority:** frozen prereg `../PREREG.md` (commit `204b82831bbabd7dc2918f07d3a5ad75c9842e53`).

## Corpus

The corpus is the **frozen 1,200 R2P pairs** sealed by the R2-3 build crew,
referenced here by pin rather than duplicated:

- Fixture directory (on branch `tnn-native-lab`):
  `docs/lab/senses/pam-rebuild/round2/fixtures/r2p/`
- Upstream sealed manifest: `MANIFEST.r2p.sha256` in that directory
  (git blob `33b5fc5d9787011bbf1161c64350ce3ee5e9cddb`); a byte-identical
  copy is pinned here as `r2p_manifest.sha256`
  (sha256 `cdda12c19557c7e773f144e6a2d0c014b58ec3f853df13fd23ad4742f39217b6`).
- 1,200 pairs: `r2p_<task>_<idx>.pair`, 6 tasks
  (colordisc, colorconst, shapetrans, pitchdisc, timbredisc, motiondir),
  200 each. Each pair: 64-byte header (task@4, idx@8, f_len@20, g_len@24,
  blobs@64), then the F (formation, front-end fooled) and G (gate, clean)
  spans. Companion `<id>.pair.truth` files carry oracle truth.
- Generator: `round2/fixtures/gen_r2p.py` (frozen seed 20260923), sealed by
  the R2-3 crew with `GENERATOR_LEDGER_R2P.md`.

## Bar and kill rules (frozen, §3.2)

- Bar: `pairs_withheld / 1200 >= 90%` on the frozen pairs.
- Kill: a candidate pass with `overlap_pairs > 0` FALSIFIES THE INSTRUMENT
  RUN (not just the candidate) — the run is void and re-done.
- Positive control id 1 must show 100% overlap and < 50% withhold, else the
  instrument run is void.
- ×3 runs; reports and ledgers byte-identical; hash chain verified.

## Execution

Run only after the integration build lands (`src/` + `build.py` +
`verify.py` on the branch). CELL-A precedes any trust in an install path;
it is the acceptance test, not the adjudicator (G1 is withhold-only by
design). No cell counts as run until `report.txt` + hash-chained
`ledger.txt` are committed under `selfpam/evidence/cell-a/`.
