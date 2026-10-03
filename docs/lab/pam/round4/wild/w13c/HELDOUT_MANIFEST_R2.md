# W13c Held-Out Round 2 — Stream Manifest

Five adversary-authored streams. Row format: `lease_id|kind|channel|tag|conf|mrgF|strong|agree`.
`lease_id` = 1-based line ordinal (grant time). All tags < 2^23. Every genuine (G)
row satisfies conf ≥ 705, mrgF ≥ 3588, strong ≥ 1, agree ≥ 1.

| filename | bytes | SHA-256 | attack label |
|---|---|---|---|
| w13c_heldout2_ring.txt | 3140122 | 96c6ea862919eada613ba98c1e9fa5a2dffb22d7b29fa1a1f04f6a897d83f86c | Multi-party corroboration rings |
| w13c_heldout2_forged.txt | 3141321 | 6080a4e7ee92c7d6c52deb33fa34ed63d1783686c8cb8bab8a455812a3cdb90a | Bar-passing forged credentials |
| w13c_heldout2_sleeper.txt | 1246289 | 13a79c0d92a9fed5940abfbbfeeb4b0b9276f83e34200c72d47723be1bd1bb60 | Sleeper-cell betrayal pattern |
| w13c_heldout2_tagsquat.txt | 725819 | 3c9c1ecc40f4d6636f4fd3532882296236c734e661a6a8244bc5cb3de504cd91 | Tag-squatting on genuine claims |
| w13c_heldout2_adaptive.txt | 777717 | 4b051ea1cdcf39c5b24e9af80e320cbf8b72bdc328375cdd07b034bf41387aad | Adaptive camouflage in dense regions |

Attack mechanisms are described in `ATTACKS_SEALED.md` (sealed — do not open until
evaluation runs are complete). Generation provenance is in `GENLOG_R2.md`.
