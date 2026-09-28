# R1-PRIMARY — Verdict: REPRODUCED

**Type:** A (clean-environment replication)
**Commit under test:** `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch `tnn-native-lab`, `sylorlabs/TNN`)
**Clean checkout:** `~/workspace/scratch-crossref/R1/clean/` (fresh shallow clone, frozen commit checked out directly, `git status` clean)
**Run directory:** `~/workspace/scratch-crossref/R1/primary/`
**Toolchain:** `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**SHA-256:** `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
**Date:** 2026-09-22/23 PDT

## Verdict

**REPRODUCED** — every committed D-family headline claim from the 2026-09-22 day verdict was rebuilt from frozen sources in a clean environment and reproduced byte-identically, with all numbers re-measured from my own rerun data.

## Committed vs measured

| Claim (committed) | Measured (my rerun) | Method |
|---|---|---|
| B (learned-only) 0.9911 | **0.9911** (S0=0.991077) | 36 configs × 3 byte-identical runs; all logs byte-match committed evidence |
| A (planted-only) 0.6552 | **0.6552** (S0=0.655236) | same |
| C (hybrid) 0.9893 | **0.9893** (S0=0.989308) | same |
| Ordering B > C > A | **confirmed** | same |
| K-T3 fired | **fired** | mastery parity 1.0000 vs 1.0000 (≤0.05 ✓); revisability Δ = 1.0000 (≥0.20 ✓); C beats B on 0 metrics ≥5pp ✓ |
| D1 planting composite 0.6551 | **0.6551** (12/12 reps, cost 0.0514, esc 12) | 24 bind configs × 3 runs; all byte-match committed |
| D2 teaching composite 0.9911 | **0.9911** (12/12 reps, cost 0.9108, esc 0) | same |
| K-Q1 fired (D2 revisability ≥ 0.90, D1 < 0.20) | **fired** (D2 1.0000, D1 0.0000) | same |
| K-Q2 never fired (0 transcription errors) | **confirmed** (E_dump=E_obs=E_prb=0) | corpus legs all exit 0, digests match |
| Learned teacher = planted teacher, end-states byte-identical | **confirmed** — learner digest `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467` under BOTH legs (planted teacher `6aee9aa2…`, learned teacher `6f387ee3…` differ; the byte-identical claim is on the learner's end state) | Q1B N=5, all byte-identical, SHA-256 `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151` = committed `n5_sha256.txt` ×5 |
| 10% noise: absorbed/filtered/untaught 19/0/4; mastery 173/192; §B.7 96/96 | **confirmed** (`Q1N_ACCOUNT,taught,19,0,4`) | N=5 byte-identical; hash `e0bbbbd21ce4928e9c424017d591969cb55dcef28ed77fbfa29a782b39c4661f` = committed |
| 25% noise: 49/0/10; mastery 143/192; §B.7 96/96 | **confirmed** (`TQN_ABSORB,49,0,49,143,0`) | N=5 byte-identical; hash `e8983ac4e3e0b42360442015c45dc51b18267d5753a518c5b79784d337fd63d4` = committed |
| 50% noise: 99/0/19; mastery 93/192; §B.7 96/96 | **confirmed** (`Q1TQ_ABSORB,noisy50,99,0,19`) | N=5 byte-identical; hash `7aa4c7861682660723a1423ba015b75d8e0ecf224b64aedc9aaae8bcb6b3a0a3` = committed |
| No knee in teacher noise (fully absorbed at every level) | **confirmed** — absorption 19/19, 49/49, 99/99; filtered=0 at every level; linear through origin | same |
| S10 scale leg: no degradation vs S1 | **confirmed** (mastery 1.0000, revisability unchanged, all arms) | S10 configs × 3 runs, byte-match committed |

Integrity hard gate (every rep): all trap families 20/20, hallu ≤ 1, K1=K2=K3=1, refusal=1 → **PASS on all 36 Track 5 reps and all 24 Q2 trap legs**.

## Scale of the rerun

- **Track 5 (A/B/C):** 75 configs (36 bind s1 + 36 btrap + 3 s10) × 3 runs = **225 runs**; every run byte-identical within its triple; all 75 final logs byte-identical to committed evidence (`matched_committed=75`, `fail=0`).
- **Q2 (D1/D2):** 50 configs (24 bind + 24 btrap + 2 s10) × 3 runs = **150 runs**; all byte-identical within triple; all 50 logs byte-identical to committed evidence (`matched_committed=50`, `fail=0`).
- **Q1B:** 5 runs, byte-identical, hash matches committed N=5 record.
- **Noise series:** 5 runs each, byte-identical, hashes match committed N=5 records.
- All binaries rebuilt from frozen sources with the pinned toolchain; pure Zag verification, zero RNG anywhere; Python used only as glue (drivers, parsers). Every slice < 2²⁵. Heavy work under `~/workspace`, not `/tmp`.

## A note on the substrate gap (documented, not substituted)

During the build I found that the frozen `q2-distillation/src/substrate/` and the three frozen noise-leg `src/substrate/` trees contain only the two R33 native files — the `cl/` subdirectory (`substrate/cl/common.zag`, imported by `t5_core.zag`) is absent from those committed trees. The frozen Q2 prereg specifies "verbatim Track 5 substrate copies" and "identical substrate", and the frozen `q1b-teacher-bakeoff/src/substrate/` contains the full substrate — its `cl/common.zag` is **byte-identical** (`8aec83cb…`) to Track 5's, and the noise legs' R33 files are byte-identical (`e6379ddb…`) to Track 5's. This proves the whole wave shares one canonical substrate; the missing `cl/` is a committed-tree gap, not a different artifact.

Resolution: the build areas were completed with the wave-canonical frozen substrate bytes (verified byte-identical where files overlap). Nothing was invented or borrowed from a different source. The proof this is faithful rather than substitution: **every one of the 375 rerun outputs is byte-identical to the sealed committed evidence**, including the sealed SHA-256 map, session digests, and corpus digests. A wrong substrate could not reproduce the sealed digests.

## Frozen evidence pins (git tree SHAs at 7b2100d0)

- `docs/lab/wave12/track5-binding/evidence` → `41d304d70b8c7f87f2326fce13897570662d3390`
- `docs/lab/wave12/track5-binding/src` → `029f9fc3198bda9070b9b533b2d06eb8476191cf`
- `docs/lab/wave12/track5-binding/prereg` sealed map SHA-256: `8e7dc59f58942ee47829d006d7a0bbc9c8ff9ee18805d3cf0230d787f9189737`
- Expected domain hash: `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8` (confirmed on smoke run)
- `docs/lab/wave12/q2-distillation/evidence` → `ac010f504612ee3cb1d9a6582455c93c77753d6a`
- `docs/lab/wave12/q2-distillation/corpus` → `f1150160733f9770ad795c094e914ad2c5fafbc8` (SHA-256: `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada`; binary verifies this at startup — P4 passed)
- `docs/lab/wave12/q2-distillation/src` → `9e9e45325960ed80e4d3c51b34109540b935a0b2`
- `docs/lab/q1b-teacher-bakeoff/evidence` → `d8e34ba711cf3acf47a1070c271d4e65e22fda7c`
- `docs/lab/q1n-noisy-teacher/evidence` → `1a6ca9c81c09e28a0ebaf3cde31f839f1724e50b`
- `docs/lab/tq-noisy25/evidence` → `8c0f7d2f720f68001a801de6463e844ed7ffbb81`
- `docs/lab/q1tq-noisy50/evidence` → `aec083beb796f53d541ca11fc4a2c6e05c9dd37e`

## Non-interference

The repo (`~/workspace/scratch-crossref/R1/clean/`) was read-only throughout; no commits, no edits, no copied binaries into it. No other workstream touched. The clean checkout remains at the frozen commit with a clean `git status`.

## Files

- `~/workspace/scratch-crossref/R1/primary/VERDICT.md` (this file)
- `~/workspace/scratch-crossref/R1/primary/RUNLOG.md` (full run log)
- `~/workspace/scratch-crossref/R1/primary/logs/t5/SHA256SUMS.txt`, `~/workspace/scratch-crossref/R1/primary/logs/q2/SHA256SUMS.txt` (rerun artifact hashes)
- Drivers: `run_t5.sh`, `run_q2.sh`, `recompute_t5.py`
