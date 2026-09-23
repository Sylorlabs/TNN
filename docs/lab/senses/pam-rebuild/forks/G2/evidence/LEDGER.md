# LEDGER.md — G2 hash-chained ledger (FNV-1a-64)

Genesis L_0 = FNV-1a-64("G2-PRP-1") = 822c6b564b0752e1.
Record encoding (277 bytes): tid u8, judgment code u8, disposition u8,
norm LE16, pred_hash LE64, obs_hash LE64, 256 signed residual bytes.
Chain rule: L_n = FNV-1a-64(L_{n-1} || record bytes).

## Batch chains (425 adversarial fixtures)

| mode | records | final chain | independent python verify |
|---|---|---|---|
| contract | 425 | cf4ab3fd62a17a71 | PASS |
| ablated | 425 | 3582ea7ee3b45ff9 | PASS |

Determinism: batch stdout byte-identical across 3 runs per mode: PASS.
