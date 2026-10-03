# LEDGER — CRO-1 corroborated-revision offense trial

Frozen prereg: `senses/pam-rebuild/round2/preregs/PREREG_CRO-1.md`
(prereg commit `936de89aa143bed37faf4b9c64836bed15194e40`, committed ALONE
2026-09-24 before any code).

## Frozen inputs

| Artifact | SHA-256 |
|---|---|
| `round2/forks/R2-4/evidence/clean/sweep.jsonl` (11,840 rows) | `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2` (matches `evidence/MANIFEST.sha256` and frozen `v2/ceiling_test/PREREG_CEILING_TEST.md` §1) |
| `v2/f5_backtest/exemplars.tsv` (6-exemplar bank) | `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e` |
| `src/R33_NATIVE_IO_V1.zag` (IO import, byte-identical copy) | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` |
| Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |

## Build

`src/cro_offense.zag` — pure-Zag offense battery (decision rule = frozen
PREREG_CRO-1 §2 D3; F5 predicate verbatim from committed `f5_pred.zag`;
R2-3 disjoint-span filter). Compiled with the pinned toolchain; binary
`cro_offense` built 2026-09-24, NOT committed (no binaries in repo).

Build note: first compile panicked at runtime (slice OOB) — `stem_of` wrote a
19-char dashless fam stem into a 16-byte `cs` buffer. Fixed by enlarging `cs`
to 64 bytes (predicate semantics unchanged; all real stems ≤19 chars). Second
build ran clean, rc=0.

## Runs (determinism bar K3)

Three runs, identical argv:
`./cro_offense ../../R2-4/evidence/clean/sweep.jsonl ../../../../v2/f5_backtest/exemplars.tsv`

| Run | stdout SHA-256 | rc |
|---|---|---|
| run1.out | `1b913b64c1100334c94250ee4c61993ea36d40cbc5e74bfe5b6321cdf439fe8e` | 0 |
| run2.out | `1b913b64c1100334c94250ee4c61993ea36d40cbc5e74bfe5b6321cdf439fe8e` | 0 |
| run3.out | `1b913b64c1100334c94250ee4c61993ea36d40cbc5e74bfe5b6321cdf439fe8e` | 0 |

Byte-identical across all three. Zero RNG in any decision path.

## Measured summary (from stdout tail, identical in all 3 runs)

```
ROWS n=11840 err=0
ATTACK n=4619 ac1=834 ac2=0 ac3=806
STRATA T n=1 ac1=1 ac3=1 HCX n=1108 ac1=6 ac3=0 LC n=3510 ac1=827 ac3=805
CONTROL n=7221 ac1=5299
```

- Attack-success rate (K1): 834/4619 = **18.06%**
- T stratum (trial-1145 class): 1/1 = 100% — seq 1145 → INSTALL under AC-1/AC-3
- W-HC: 7/1109 = 0.63% (T included); HCX-nonT: 6/1108 = 0.54%
- W-LC: 827/3510 = 23.56%
- AC-3: 806/4619 = 17.45% (28 fewer than AC-1: F5-blocked items need 3/3, get 2/2)
- AC-2 (same-span): 0 installs — R2-3 discard holds on all 4,619 attacks
- Control: 5299/7221 = 73.38%
- 28 F5-BLOCKED attack rows install under AC-1 (unanimous verified
  corroboration clears even the trap's 3/3 bar); includes bank exemplars
  themselves (they are wrong-judgment rows with corroborating gate evidence).
