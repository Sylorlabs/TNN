# RUN_DIGESTS — V2-C pure-Zag battery (B6 evidence)

**Date:** 2026-09-24
**Battery:** 11,840 trials, dmask=4095, 3 full runs in independent workdirs
  (`run1/`, `run2/`, `run3/`), same pre-built binaries.
**B6 bar:** dispositions + ledger + metrics byte-identical across 3 runs;
  ledger hash-chain independently verified in Python each run.

## Binaries (identical all runs; built once from branch-committed sources)

| Binary | SHA256 |
|--------|--------|
| bin/vsense_c | d6d0bc95404ac55887c3f9a540d7db0e466650624bcc1de16f4660ffd1e897c1 |
| bin/deliberate | ab185ba2d13a31c6afdecc3409f71801df37af32f69d04304774eaea234a144d |
| bin/memgate | 0314033408d2fbf121db72595c6d8d02f50a29a279b2fa9839e5e104e2e40040 |

## Per-run artifact digests

| Run | Trials | dispositions.txt | ledger.txt | metrics.json | sweep.jsonl | records.txt | ledger verify |
|-----|--------|------------------|------------|--------------|-------------|-------------|---------------|
| 1 | 11,840 | e09f764e129c741c7edbf0822432bff56922043cf0690b0da64325bfd4a98b78 | 7ddb866264b224402208696ce65bc3e1b95de29fd3c474594fcf4a48768d27c7 | 695035270fe44a96bf6733318f61c51c30a83fe99e29ac2ad8d52a4a7765fb55 | c56152ada5596d455d433b59692ff72230057aebe53e886e71c35b717730bdb7 | 2b46d3ad6287d192fcaba5b728a5105c8f583e17653413711c1d28458123cdee | 11,840 links OK |
| 2 | 11,840 | e09f764e129c741c7edbf0822432bff56922043cf0690b0da64325bfd4a98b78 | 7ddb866264b224402208696ce65bc3e1b95de29fd3c474594fcf4a48768d27c7 | 695035270fe44a96bf6733318f61c51c30a83fe99e29ac2ad8d52a4a7765fb55 | c56152ada5596d455d433b59692ff72230057aebe53e886e71c35b717730bdb7 | 2b46d3ad6287d192fcaba5b728a5105c8f583e17653413711c1d28458123cdee | 11,840 links OK |
| 3 | 11,840 | e09f764e129c741c7edbf0822432bff56922043cf0690b0da64325bfd4a98b78 | 7ddb866264b224402208696ce65bc3e1b95de29fd3c474594fcf4a48768d27c7 | 695035270fe44a96bf6733318f61c51c30a83fe99e29ac2ad8d52a4a7765fb55 | c56152ada5596d455d433b59692ff72230057aebe53e886e71c35b717730bdb7 | 2b46d3ad6287d192fcaba5b728a5105c8f583e17653413711c1d28458123cdee | 11,840 links OK |

**Byte-identical across runs:** dispositions YES / ledger YES / metrics YES /
  sweep YES / records YES.

## Ledger verification method

Independent Python re-check per run (`verify_ledger`): recompute every
SHA-256 link from the previous digest + canonical entry, require
record/ledger line-count equality, and verify each ledger line's canon =
`prev + sha256(rec) + "|" + rec + "|" + dis + "|" + det` where rec is the
source record line and (dis, det) the disposition and detail. All 11,840
links verified in all 3 runs.

## Fixture integrity

- 21,830 files: 10,915 `.r24` + 10,915 `.r24.truth`, one-to-one pairing,
  zero-size = 0, orphans = 0.
- Per-family counts match frozen spec (normal 5,100 / adversarial 5,815).
- Determinism spot-check: 9 fixtures regenerated from `r2a_gen.py` in a clean
  dir — byte-identical (fixture + truth).
