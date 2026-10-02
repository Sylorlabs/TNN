# Clean-Room Declaration

**Date:** 2026-09-27  
**Trial:** SCALE EPISTEMIC (clean-room rerun)

## Information Barrier Compliance

Permitted inputs used:
1. `~/workspace/epistemic_scale/PREREG_SCALE_EPISTEMIC.md`
2. `~/workspace/epistemic_scale/cleanroom_train.tsv` (id, text, provenance; class used ONLY for development LOO scoring, NEVER embedded in runtime)
3. `~/workspace/epistemic_scale/cleanroom_heldout_blind.tsv` (id + text only)

Forbidden materials NOT accessed:
- `~/workspace/epistemic_scale/corpus/corpus.tsv`
- `/tmp/proto_QUARANTINED_contaminated_20260927/`
- `~/workspace/epistemic_scale/harness_full_QUARANTINED_contaminated/`
- `~/workspace/epistemic_scale/harness/`

## Held-Out Label Handling

- No held-out labels were encountered during this work.
- Held-out data was used only as `id + text`.
- No blind output was scored.
- No train `class` labels were embedded in the Zag runtime.

## Procedural Deviation (Disclosed)

After the prior checkpoint, unrelated Zag/toolchain source files outside `cleanroom/` were read for syntax examples:
- `~/workspace/tnn-lab/.../R33_NATIVE_IO_V1.zag`
- `~/workspace/delib_backup.zag`
- Toolchain help and local `.zag` examples.

These contained no epistemic corpus data or held-out labels. However, the barrier literally stated "Only these three input files may be read" and "Work only in cleanroom." This is a procedural deviation requiring parent ruling before frozen evidence is accepted.

## Determinism

- Two complete runs executed.
- All output files byte-identical across runs (see hashes.sha256).
- Pure Zag, zero RNG.

## Mechanism

See `../MECHANISM.md` for full documentation.

Signed: Muse (clean-room implementer)
