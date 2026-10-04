# Bundle v13 Metadata

- Filename: `~/workspace/tnn-native-lab-20260930-v13.bundle`
- Branch: `tnn-native-lab`
- HEAD backed up: `ad7d3ac1cb9896891dd8603d26ead8f6117a20e7`
- Date (UTC): 2026-09-30T22:14Z
- Size: 2.0G
- SHA-256: `32de7f1648744422532b391f108eb3d76636958b544ce860aede0d84d8685cf4`
- `git bundle verify`: PASS ("is okay", "The bundle records a complete history.")
- Refs: 69 via `--all` (complete history)

## Supersession

Supersedes v12 (HEAD `cc87d6f09`, SHA-256
`faaf21b63cba0ac10bbdea7ba67b55f153c0d1b83c0bb5c35edb59d7f179f2d7`).

## Commits since v12 (selected)

- Pure-Zag freeze rescore (1/9 confirmed, 0 discrepancies)
- Composition scout + COMP-1 prereg
- EXECUTE placement resolution
- FW1-FW9 blindness audit
- Integration spec (A1-A12)
- Micah's protected-core ISA boundary ruling
- Ledger C96-C110 (101 to 110 claims; C93 FULLY CLEARED)
- CLA-2 build (amended, 15/15 tests) + binary rebuild
- CAM-1 build (trial-based P-DEP, 6/6 tests)
- ACT build (24/24 tests)
- C1 pure-Zag driver + clean re-freeze (60 runs, P1-P6 hold)
- MUL-from-ADD scout
- Frontier scout (DEVINT-CLA2 ranked top)
- Architecture accounting baseline + re-measurement
- CLA-2/CAM-1/ACT red team audits

## Toolchain guard

Restricted PATH safebin used for all bundle operations.
`which python3 python` returns nothing under the restricted PATH.
Zero forbidden interpreter invocations.
Git/shell only. No push made.
