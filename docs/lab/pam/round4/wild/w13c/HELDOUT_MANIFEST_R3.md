# HELDOUT_MANIFEST_R3.md

Round 3 held-out stream manifest (adversary-authored, sealed).

## Row format

`lease_id|kind|channel|tag|conf|mrgF|strong|agree`

- 8 `|`-separated fields, one row per line.
- `lease_id` = 1-based line ordinal (unique positive integer).
- `kind` in {G, F} (G = genuine claim, F = false claim).
- All numeric fields are non-negative integers.

## Hard harness constraints (verified on every stream)

- Every `tag` < 2^23 (8388608).
- Every G row satisfies: conf >= 705, mrgF >= 3588, strong >= 1, agree >= 1.
- Every G row's `(conf, mrgF, strong, agree)` content comes from the 671-row
  genuine pool; every F row's content comes from the 1139-row false pool
  (frozen M1 tape `/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt`).

## Streams

| filename | bytes | SHA-256 | attack label |
|---|---|---|---|
| w13c_heldout3_sybil_quorum.txt | 3081077 | 34a32fa73793d586f4f0c67002ae6091892f43454c80052506626ef857190e47 | sybil_quorum |
| w13c_heldout3_tagshadow.txt | 3066219 | c46bd97b47d77187963c9422b4cf934756299717f44764c42609b76eba950e0a | tagshadow |
| w13c_heldout3_sleeper_flip.txt | 1204603 | 8061c31e4b479ab2d18690ca12a335714f9881861319a949e93469121a6739ed | sleeper_flip |
| w13c_heldout3_forged_cred.txt | 761635 | 38f51e9342ef13f95d74a9ff2ff32bf80e598f2e650b068062329f39cc5d66a8 | forged_cred |
| w13c_heldout3_launder_chain.txt | 767806 | 7e102b0053aa6c855746bcc5a670123c17746eb2e86aeabf902f52934dbbdf63 | launder_chain |

Total: 290133 rows across 5 streams (<= 300000).

## Row counts per stream

| filename | rows | G rows | F rows | G corroboration fraction |
|---|---|---|---|---|
| w13c_heldout3_sybil_quorum.txt | 100136 | 88000 | 12136 | 100.00% |
| w13c_heldout3_tagshadow.txt | 99998 | 83332 | 16666 | 100.00% |
| w13c_heldout3_sleeper_flip.txt | 40000 | 20000 | 20000 | 100.00% |
| w13c_heldout3_forged_cred.txt | 25000 | 22000 | 3000 | 100.00% |
| w13c_heldout3_launder_chain.txt | 24999 | 16666 | 8333 | 100.00% |

Corroboration = fraction of G rows sitting in at least one same-tag /
different-channel pair with |Delta ordinal| <= 3. Target >= 80%; achieved 100%
on all five streams.

Attack mechanisms are recorded in `ATTACKS_SEALED_R3.md` (sealed: do not open
until scoring is complete). Generation details in `GENLOG_R3.md`. Reproducible
via `gen_heldout3.py`; independently checkable via `verify_heldout3.py`.
