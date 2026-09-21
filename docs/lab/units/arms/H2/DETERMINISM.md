# H2 Determinism Report — 1x double-run + M8

**Date:** 2026-09-21
**Rule:** zero randomness in every AI decision path and every harness path
(no RNG, no clock reads; T3/churn corpora are fixed deterministic inputs).

## Double 1x battery (corrected source)

| Battery | When (UTC) | Modes | Exit |
|---------|-----------|-------|------|
| r1a (first) | 08:43–09:09 | 14 | all 0 |
| r1 (second) | 09:12–09:36 | 14 | all 0 |

**13/14 modes byte-identical stdout** across the two batteries
(`diff` clean on every `stdout.txt`).

## The one difference: M5 (explained, not nondeterminism)

- r1a: `M5,13770,5638480,684124,1689280,0`
- r1:  `M5,13770,5638480,684124,1689280,-1`

The trailing field is `t_m5`'s `write_file("ledger.bin")` status in the
shared working directory. The second run's write failed (`-1`) because
`ledger.bin` from the first run still existed. All metric fields and the
`METRIC_JSON` line were identical.

**Clean rerun** (stale `ledger.bin` deleted):
`evidence/r1/m5-1x-clean-rerun/` — stdout byte-identical to r1a,
`ledger.bin` byte-identical, SHA-256
`c988bd357c9d7e5a19485c18326003636ca995b05945a4ac4f5ac0cf4460090f`.

The anomalous `,-1` record in `evidence/r1/m5-1x/` is preserved as-is.
See `evidence/r1/m5-1x-clean-rerun/NOTE.md`.

## Post-repair smoke

After the t_m8-only source repair (store-image sizing + arg dispatch;
BUILD_NOTES.md), rebuilt 10:17 UTC and reran `m1-1x-prose`:
**byte-identical** to the 1x evidence. The repair touched only t_m8.

## M8 five-regime gate

All five regimes (clean/frag/aslr/starve/freelist-rev) byte-identical on
stdout, store hashes, store chain, ledger bytes (4,731,008 B), ledger chain,
and allocator trace. See M8-REPORT.md.

## Conclusion

H2 is deterministic: identical inputs → byte-identical outputs across
repeated runs and adversarial heap perturbations. The single observed
difference traces to harness working-directory state, was reproduced clean,
and is documented, not hidden.
