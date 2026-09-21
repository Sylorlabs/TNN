# M5 determinism note — harness-state collision, not AI nondeterminism

## What happened

The two 1x batteries' M5 runs differed in exactly one trailing field of the
human-readable stdout line:

- r1a (first battery, 2026-09-21 08:5x UTC): `M5,13770,5638480,684124,1689280,0`
- r1  (second battery, 2026-09-21 09:2x UTC): `M5,13770,5638480,684124,1689280,-1`

The trailing field is the status of `t_m5`'s final `write_file("ledger.bin")`
in the shared H2 working directory: `0` = wrote, `-1` = failed. The second run
failed the write because `ledger.bin` from the first run still existed in the
directory (the writer does not overwrite). All metric fields and the
`METRIC_JSON` line were byte-identical between the two runs.

## Resolution

Deleted the stale `ledger.bin`, reran `m5-1x` clean (this directory). Result:

- stdout byte-identical to the r1a run (`diff` clean)
- `ledger.bin` byte-identical to the r1a run's ledger
- ledger SHA-256: `c988bd357c9d7e5a19485c18326003636ca995b05945a4ac4f5ac0cf4460090f`

## Verdict

Deterministic. The single-field difference was a harness working-directory
collision, not nondeterminism in the arm. The anomalous `,-1` record in
`evidence/r1/m5-1x/` is preserved as-is and must not be silently overwritten;
this directory holds the clean rerun.
