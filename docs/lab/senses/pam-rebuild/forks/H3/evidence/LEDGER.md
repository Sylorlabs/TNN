# H3 Ledger Evidence

## Format

Each `StateTransition` is a canonical byte string:

```
H3|task=<task>|fx=<fixture path>|t0=<T0 claim>|br=<i:cf:br;...>|inst=<installed or NONE>|disp=<disposition>|judge=<judgment>|dur=<0|1>|
```

The ledger is hash-chained: `chain[i] = SHA-256(chain[i-1] || transition[i])`,
with `chain[-1]` = 32 zero bytes. In single-fixture mode, each run starts from
zeros. In streaming mode, the chain runs across all 600 episodes and the final
`ledger_head` is emitted.

SHA-256 is the toolchain substrate `R33_NATIVE_SHA256_V2.zag`, validated
against the FIPS 180-4 `"abc"` vector:
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.

## Independent verification

- **B6**: 60 fixtures × 3 runs. All stdout byte-identical. All 60 ledger
  hashes recomputed independently with Python `hashlib.sha256` (zeros ||
  transition): all match.
- **Streaming**: 6 scenes × 600 episodes. Each scene's ledger verified by
  independent recompute (`eval/verify_ledger.py`): `chain[i]` must equal
  `SHA-256(chain[i-1] || transition[i])`, and the final head must match the
  emitted `ledger_head`.

## Ledger heads (streaming, 600 episodes each)

(TBD — filled after the re-run with the fixed binary.)

## Sample chain (first 3 episodes, colordisc stream)

(TBD — filled after the re-run.)
