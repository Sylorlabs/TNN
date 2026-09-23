# AMENDMENT_001_PROCEDURAL — pre-freeze baseline handling (2026-09-23)

This amendment records procedure only. It does not alter any frozen
prediction, kill bar, or expectation in PREREG.md.

## What happened

Before the prereg freeze (commit a9a6d36c), the existing FL2 source
(`fl2.zag` equivalent logic) and substrate (`tn.zag`) were copied into
`mechanics/` and an unchanged FL2 baseline was rebuilt to verify the
toolchain and the evidence pipeline. The baseline evidence SHA256
(`20fee727aaf7746c7b86e93e6bf441381dab9e1e1f4d85437e0b7c5882582263`)
matched the canonical FL2 evidence, confirming the copy was faithful.

## What did NOT happen

No G8 variant mechanism was implemented, built, or run before the
freeze. All ten variant sources (`v_a0` … `v_c4`) were written after
commit a9a6d36c. The `WORLD` const, the `g8base.zag` shared harness,
and all variant-specific machinery postdate the freeze.

## Why it matters

The frozen prereg's "verbatim FL2" claims (c1, and the FL2 arms run
in-binary in every variant) rest on the copied source being byte-faithful
to canonical FL2. The SHA256 verification above is the evidence.

## Disposition

No frozen text is modified. This file stands as the procedural record.
