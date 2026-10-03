# GENLOG_R3.md

Round 3 held-out generation log — process only. Attack mechanisms are sealed
in `ATTACKS_SEALED_R3.md`; this file carries no mechanism detail beyond the
attack labels.

## Determinism statement

Generation is fully deterministic: integer counters and modular arithmetic
only. No RNG, no timestamps, no PIDs, no salted `hash()`. The only hash used
is `hashlib.sha256` over the final file bytes for manifest purposes.
`gen_heldout3.py` was run twice; both runs produced byte-identical streams
(all five SHA-256 digests identical across runs).

## Content sources (frozen M1 tape, read-only)

Source: `/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt` (2,241 lines).

| Pool | Definition | Asserted count | Verified count |
|---|---|---|---|
| Genuine | C rows with conf >= 705, mrgF >= 3588, strong >= 1, agree >= 1 | 671 | 671 |
| False | all 1109 B + 12 W + 18 P rows | 1139 | 1139 |
| Forged | false rows passing all four admission bars | 3 | 3 |

Genuine content: cycling cursor over the 671 genuine rows in tape order; each
G row emitted takes the next cursor entry (cursor resets per stream).
False content: cycling cursor over the 1,139 false rows in tape order; B rows
as logged, W rows with strong=agree=1 (per the W|conf|mrgF|1|1 tape format),
P rows as `conf|mrgF` with strong=agree=1 (per the P|idx|conf|mrgF|1|1 tape
format and the s=a=1 convention). The forged_cred stream's attack rows cycle
the 3 forged rows instead of the full false pool.

## Stream composition (row counts)

| Stream | Label | Rows | G rows | F rows |
|---|---|---|---|---|
| w13c_heldout3_sybil_quorum.txt | sybil_quorum | 100136 | 88000 | 12136 |
| w13c_heldout3_tagshadow.txt | tagshadow | 99998 | 83332 | 16666 |
| w13c_heldout3_sleeper_flip.txt | sleeper_flip | 40000 | 20000 | 20000 |
| w13c_heldout3_forged_cred.txt | forged_cred | 25000 | 22000 | 3000 |
| w13c_heldout3_launder_chain.txt | launder_chain | 24999 | 16666 | 8333 |

Total 290133 rows (<= 300000 budget). Genuine background traffic in every
stream is emitted as same-tag, different-channel row pairs with |Delta
ordinal| <= 3 on recurring tags, giving 100.00% of G rows a corroborating
partner (measurement target >= 80%).

Row format: `lease_id|kind|channel|tag|conf|mrgF|strong|agree` with lease_id =
1-based line ordinal. Generator: `gen_heldout3.py` (committed in this
directory as the reproducibility record).

## Verification results (`verify_heldout3.py`)

For each stream the verifier checked: 8-field format; lease_id == line
ordinal; kind in {G, F}; all fields non-negative integers; tag < 2^23;
every G row passes the admission bars; every G row's content in the 671
genuine pool; every F row's content in the 1139 false pool; and the genuine
corroboration fraction (G rows in >= 1 same-tag/different-channel pair with
|Delta ordinal| <= 3).

| Stream | Verdict | G corroboration |
|---|---|---|
| w13c_heldout3_sybil_quorum.txt | PASS | 100.00% (88000/88000) |
| w13c_heldout3_tagshadow.txt | PASS | 100.00% (83332/83332) |
| w13c_heldout3_sleeper_flip.txt | PASS | 100.00% (20000/20000) |
| w13c_heldout3_forged_cred.txt | PASS | 100.00% (22000/22000) |
| w13c_heldout3_launder_chain.txt | PASS | 100.00% (16666/16666) |

All five streams passed every check. One verifier fix during development:
the genuine pool contains duplicate content tuples (664 unique of 671), so
pool-count assertions run on the raw lists and content-membership checks run
on the de-duplicated sets.
