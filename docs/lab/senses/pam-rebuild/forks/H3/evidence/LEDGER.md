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
- **Streaming**: 6 scenes × 600 episodes (pristine frozen binary, isolated
  runs). Each scene's ledger verified by independent recompute
  (`eval/verify_ledger.py`): `chain[i]` must equal
  `SHA-256(chain[i-1] || transition[i])`, and the final head must match the
  emitted `ledger_head`. 6/6 verified. KB5 byte-replay: motiondir scene
  re-run byte-identical.

## Ledger heads (streaming, 600 episodes each, pristine binary)

| Scene | ledger_head (sha256) |
|---|---|
| colordisc | `8ebbfb2d5b8ed3b91a58eef3c87edb1347bf6dbfe779aaaf516cb8d57569fa7e` |
| colorconst | `99567d8c28676193f30f0cb2ec703c495eb045ee16bcf81d50164ca4b0289e23` |
| shapetrans | `2dbf1d192cdb89cebfb9dfb6e015bcf19590aa26bcd0789c078e6f2e65660403` |
| timbredisc | `67a12501549807831525a90a9ca8f4b9e8cec3ed5ea0428f944b5f31841d4c9d` |
| motiondir | `ce7eba19c8ccedee567c3707b8081edc6065730dadbd210a319d775268ffcc2f` |
| pitchdisc | `3631f7d809fb8061bb5afc0fe7641bf3ac6d1a87784a6492d55757aa7457b712` |

## Sample chain (first 3 episodes, colordisc stream)

| ep | chain (truncated) |
|---|---|
| 0 | `920cf8033d34ca1b683e94f850ca7d53…` |
| 1 | `540495b89b9963e5f9ba7d3cf76a9979…` |
| 2 | `e612ec8a5adb42ea1e1c3c187bd1a1d9…` |

Full per-episode chains are in the scene JSONL files (evaluation scratch;
the heads above plus `eval/verify_ledger.py` reproduce them).
