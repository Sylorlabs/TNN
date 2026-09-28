# LEDGER.md — R2-11 hash-chained ledger verification

Each battery run appends one ledger line per trial:
`seq \t task \t fixture \t judgment \t conf \t disp_code \t percept_hex \t prev_hash \t hash=<sha256>`

where `hash = sha256(core_line + "\n")` and `prev_hash` chains to the
previous line's hash (`0…0` for seq 1). `disp_code` is numeric (0=INSTALL,
1=NOTE, 2=DISCARD).

## Verification

`src/verify_ledger.py <ledger> <trials.tsv>` checks:
1. every line's `hash` recomputes from its core,
2. every `prev_hash` links to the previous hash (unbroken chain),
3. every core's (seq,task,fixture,judgment,conf,disp,percept_hex) matches
   the trial's TSV row.

## Results (final, verified 2026-09-23)

| Run | Lines | Hash OK | Chain OK | Core-vs-TSV OK | Head |
|-----|------:|---------|----------|----------------|------|
| A run1 | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| A run2 | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| A run3 | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| A off  | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| B run1 | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| B run2 | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| B run3 | 10000 | yes | yes | yes | `310a1d70a8d1faef` |
| B off  | 10000 | yes | yes | yes | `310a1d70a8d1faef` |

Both forks share the same percept pipeline, hence identical heads.
Run-2 ledgers were repaired after a service restart caused the driver to
append a fresh run to a stale partial ledger; the repair kept the last
10,000 lines (the complete fresh run), and the repaired ledgers verify
clean and match run1/run3 byte-for-byte.

## B6 byte-identity

The three emit-on TSVs per fork are compared byte-for-byte
(`cmp`). Identical files + verified ledgers = B6 satisfied.

Full TSVs/ledgers live in the work area
(`work/r2-11/battery/r2a/`); their SHA256s are in `battery/SHA256SUMS`.
