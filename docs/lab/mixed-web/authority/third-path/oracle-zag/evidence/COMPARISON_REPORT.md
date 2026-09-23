# COMPARISON REPORT — TP1 Zag-native oracle vs committed TP1 results

**Oracle prereg:** `PREREG_ORACLE_ZAG.md` (frozen before any oracle run;
commit `23eaecc19d4906da13fdfb6e0a0f7fba7e24d30f`).
**Trial under verification:** TP1 verdict commit
`c85c9b41770c1878fb00a8dc991a5b4f17f8caaa`
(frozen design prereg `44afdbefc168edddcae50e9dd91eac12cd9fa156`).
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned). Pure Zag, zero RNG. Oracle source: `src/opz_oracle.zag`
(decision logic re-derived from PREREG-TP1 §3; ledger byte layout is the
evidence format under verification).

## Frozen-data verification (before any oracle run)

- 15 round-3 logs (`docs/lab/mixed-web/authority/round3/evidence/`):
  **30/30 files** (15 logs + 15 err files) verify against the committed
  SHA256SUMS.
- Corpus (`third-path/evidence/tp_data.json`): all **220/220 envelopes**
  match the frozen `round3/manifest_r3.txt` exactly — rows, block, level,
  twin label, stipulated gold, rel_ind, latent truth. **0 field
  mismatches.** Twin labels reproduce the Bresenham formula
  `(i·n_A) mod 20 < n_A` with **0 mismatches** (all 9 levels); S8 latent
  truths reproduce the `i mod 2 == 0` rule with **0 mismatches**.

## Byte-identical repetitions

| Run | stdout sha256 |
|---|---|
| run_zag_0.log | `c51467d1b669ac1acdf0b56aecc2f396eb7e68c8f68b679f1e38e46101353343` |
| run_zag_1.log | `c51467d1b669ac1acdf0b56aecc2f396eb7e68c8f68b679f1e38e46101353343` |
| run_zag_2.log | `c51467d1b669ac1acdf0b56aecc2f396eb7e68c8f68b679f1e38e46101353343` |

3/3 byte-identical (kill bar ORACLE-ZAG-DET: ≥3 — PASS).

## Decision comparison (0-mismatch criterion)

Committed reference: `third-path/evidence/run0.log`
(sha256 `d57fda225db8d54201ca443e6e39716aba4e5ca5a97683128a49ed61b432d1d9`).

| Check | Expected | Recomputed | Result |
|---|---|---|---|
| P\| decision lines (2,640) | run0.log | run_zag_0.log | **0 mismatches** (2,645 lines incl. H/S/C compared) |
| H\|T1 | `e17861bac9fca2647669b3ef39e56aeaec3db689a7ce62d2fa6312b3151aa861` | identical | MATCH |
| H\|T2 | `3c030dd4222168014a350f039d43447fd58115b9a656f56e58078c7b2ca212ea` | identical | MATCH |
| H\|T3 | `d2f45295b38d24c8de4c90645a7a204da958854475f1f49f4a74571ed99542a0` | identical | MATCH |
| S\| counts | `S\|880\|880\|880` | `S\|880\|880\|880` | MATCH |
| C\| shape counts | `C\|1\|200\|2\|20\|3\|0\|0\|0` | `C\|1\|200\|2\|20\|3\|0\|0\|0` | MATCH |

Kill bar ORACLE-ZAG-MATCH: **PASS** (0 mismatches).

## Derived metrics (oracle X| summary)

- **S8 false-confidence:** 0/80 converges per path (T1 0, T2 0, T3 0) → **0%**.
- **T3 verdict-identical to T1:** **880/880** decisions identical.
- **Firing behavior** (CONVERGE counts per path × threshold × block):

| Path | @500 (k=1) | @667 (k=2) | @750 (k=3) | @833 (k=5) |
|---|---|---|---|---|
| T1 Block U | 140 | 100 | 80 | 60 |
| T1 S8 / G2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| T2 (all blocks) | 0 | 0 | 0 | 0 |
| T3 Block U | 140 | 100 | 80 | 60 |
| T3 S8 / G2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

T1@500 fires exactly where rel ≥ 500 on S1_UNCORR (7 levels × 20 = 140),
0 fires on ties and no-reliability controls — the licensed threshold
behavior. T3's fire pattern is identical to T1's at every threshold.

## Verdict

**ORACLE PASS:** the pure-Zag oracle independently recomputes all 2,640
TP1 decisions, all 3 ledger heads, all shape/sequence counts, S8
false-confidence (0%), and the firing behavior with **0 mismatches**
against the committed TP1 results, across 3 byte-identical runs.
