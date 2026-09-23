# REPRODUCE_ORACLE.md — TP1 Zag-native oracle

## Layout

- `src/opz_oracle.zag` — the oracle: envelope shape classifier, T1/T2/T3
  policies, 4 frozen thresholds (500/667/750/833), SHA-256 chained
  ledger per path. Pure Zag, zero RNG. Decision logic re-derived from
  frozen PREREG-TP1 §3 (not from the trial program's code); the ledger
  byte layout is the evidence format under verification.
- `src/R33_NATIVE_SHA256_V2.zag`, `src/R33_NATIVE_IO_V1.zag` —
  byte-copies of the round-3 hash/IO substrate (primitives, not trial
  logic).
- `data_prep/prep_flat.py` — build-script: flattens the frozen
  `third-path/evidence/tp_data.json` (+ `idmaps.json`) into the
  pipe-delimited `data_prep/tp_flat.txt` the oracle reads. No decision
  logic.
- `data_prep/tp_flat.txt` — the oracle's frozen input (220 envelopes).
- `evidence/run_zag_{0,1,2}.log` — the three byte-identical oracle runs.
- `evidence/RUN_SHAS.txt` — sha256 of each run.
- `evidence/COMPARISON_REPORT.md` — expected vs recomputed (0
  mismatches).

## Reproduce

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned build; `@import` resolves relative to CWD, so build from `src/`).

```sh
cd docs/lab/mixed-web/authority/third-path/oracle-zag/src
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 opz_oracle.zag -o opz_oracle
for i in 0 1 2; do ./opz_oracle ../data_prep/tp_flat.txt > run_zag_$i.log; done
sha256sum run_zag_*.log   # all three must equal
                           # c51467d1b669ac1acdf0b56aecc2f396eb7e68c8f68b679f1e38e46101353343
```

Then compare the `P|`, `H|`, `S|`, `C|` lines against the committed
`third-path/evidence/run0.log`
(sha256 `d57fda225db8d54201ca443e6e39716aba4e5ca5a97683128a49ed61b432d1d9`):
expect **0 mismatches** (2,640 decisions + 3 heads + counts), S8
converges 0/80 per path, T3 verdict-identical to T1 on 880/880.

To regenerate `tp_flat.txt` from the frozen corpus (script-status):

```sh
cd docs/lab/mixed-web/authority/third-path/evidence
python3 ../../third-path/oracle-zag/data_prep/prep_flat.py . ../../third-path/oracle-zag/data_prep/tp_flat.txt
```

## Expected results

- `H|T1|e17861bac9fca2647669b3ef39e56aeaec3db689a7ce62d2fa6312b3151aa861`
- `H|T2|3c030dd4222168014a350f039d43447fd58115b9a656f56e58078c7b2ca212ea`
- `H|T3|d2f45295b38d24c8de4c90645a7a204da958854475f1f49f4a74571ed99542a0`
- `S|880|880|880`, `C|1|200|2|20|3|0|0|0`
- `X|S8CONV|T1|0`, `X|S8CONV|T2|0`, `X|S8CONV|T3|0`, `X|T3EQ|880|880`
