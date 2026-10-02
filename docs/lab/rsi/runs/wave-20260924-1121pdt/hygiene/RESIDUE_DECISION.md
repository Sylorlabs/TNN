# Residue decision: wave-20260924-0521pdt secondpath

Decided by the wave-20260924-1121pdt hygiene worker on 2026-09-24.
Directory: docs/lab/rsi/runs/wave-20260924-0521pdt/secondpath/

Three uncommitted residue files were found. Evidence from all of them
stays void either way. Disposition rule used: a residue file that is
byte-identical to an already-committed copy is removed as a duplicate;
a unique residue file is moved into secondpath/void/ as a clearly-labeled
void work product (kept for lineage only).

## sha256 comparisons (all computed with sha256sum, 2026-09-24)

Residue files:
- judge4_base.zag:
  7547eae365fe8843633b40987cc0e5dde26c13b901ae6c680eb0e3e07095fa34
- driver4_base.zag:
  a7fc96323b063bfeeef3935881bc1d684afb210161b0dab3d51e90621068877b
- R33_NATIVE_IO_V1.zag (residue, since removed):
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8

Committed baselines (git working copy, same directory):
- judge4.zag:
  d02c6ca6f0b29be4d57e47e50c2b133b1fa7dbc18d45afe87e63955b44819fa6
- driver4.zag:
  fd670f83283f62f7c1b68769e5664c18c1fbb34b423b1482d929faaf6d4fbeca

Archive-branch committed copy used in prior FIT work (branch
tnn-native-lab-wave-archive-20260923-2321pdt, e.g.
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/interactive/
R33_NATIVE_IO_V1.zag):
- R33_NATIVE_IO_V1.zag:
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8

## Dispositions

1. R33_NATIVE_IO_V1.zag: REMOVED as a byte-identical duplicate of the
   committed copy (e6379ddb... matches exactly). Before removal, a scratch
   backup was copied to ~/workspace/tnn-fitchat-1121pdt/
   R33_residue_scratch_copy.zag (scratch only, never /tmp) in case the FIT
   check needed it. The FIT check pulled its R33 copies read-only from the
   archive branch instead, so the scratch backup is unused.

2. judge4_base.zag: UNIQUE (7547eae3... differs from committed
   d02c6ca6...). Moved to
   docs/lab/rsi/runs/wave-20260924-0521pdt/secondpath/void/
   judge4_base.zag. Evidence void, kept for lineage only. See
   secondpath/void/VOID_README.md.

3. driver4_base.zag: UNIQUE (a7fc9632... differs from committed
   fd670f83...). Moved to
   docs/lab/rsi/runs/wave-20260924-0521pdt/secondpath/void/
   driver4_base.zag. Evidence void, kept for lineage only. See
   secondpath/void/VOID_README.md.

Nothing was committed and nothing was pushed. The coordinator commits.
