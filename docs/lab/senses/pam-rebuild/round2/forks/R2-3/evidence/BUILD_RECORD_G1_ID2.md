# Build & acceptance record — G1 registration (candidate id 2)

**Amendment:** self-PAM prereg amendment 2026-09-27-A
(`docs/lab/senses/pam-rebuild/selfpam/amendments/AMENDMENT_2026-09-27_G1_ID2.md`),
committed as `e58ee88753818d5b4a2ffb5c200f8b411748eabc` on `tnn-native-lab`
(parent `23bf8c639f2b`), BEFORE any run below.
**Date:** 2026-09-27 | **Crew D** (self-PAM production drive)

## Toolchain

- Pinned znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  (verified by `build_g1.py` before compiling; matches the program-pinned value)

## Sources staged (build dir `~/workspace/selfpam_consumer/build_r23/`)

| File | Origin | SHA-256 |
|---|---|---|
| `sense.zag` | R2-3/src (patched: range 0..2) | `6c1363f4c64c3b8f7ae99222c09f8efe5eff921aa2dc42c5cd0642ca6b123462` |
| `r2p_gates.zag` | R2-3/src (patched: id-2 branches) | `01a38a25f7b93def95eece2a3d35cfc396ebaba266785d1b0969a669f7a7391e` |
| `r2p_front.zag` | R2-3/src (untouched) | `c66d87c68088d5f58ee899e381c9513f91f3fea01500164d9ca99b80a2c68a80` |
| `r2p_protos.zag` | R2-3/src (untouched) | `5e10eda3357d7e20a326258ddb30a521a9e94129895dc87d5c1c5296dde52bd7` |
| `g1_candidate.zag` | vendored, byte-identical to `selfpam/src/g1_candidate.zag` | `6ba9ea447387db4e47f13ea2295ea7da4ba735c27c8d41c638ca0fefa8abdecb` |
| `codec.zag` | vendored, byte-identical to `selfpam/src/codec.zag` | `ca9d1fd1cd10b164e95a2ca2f4b2a96c7944ba7452958cb0d1156db9643ccd4c` |
| `R33_NATIVE_IO_V1.zag` | `selfpam/src/` (canonical, staged not vendored) | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` |
| `R33_NATIVE_SHA256_V2.zag` | `selfpam/src/` (canonical, staged not vendored) | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |

Vendoring check: `build_g1.py` refuses to build unless the two vendored
files are byte-identical to the canonical `selfpam/src/` files — passed.

**Binary:** `sense_bin`, SHA-256
`1db54a68a3a5873ea4ea10e41afc51ec89ac1aa06294940a8b82ce3349bfca74`
(build scratch in the workdir; never committed)

## Corpus

- `round2/fixtures/r2p/` holds 600 of the 1,200 frozen `.pair` files
  (colordisc/colorconst/shapetrans) plus all 1,200 `.truth` files;
  the 600 audio/video `.pair` files (pitchdisc/timbredisc/motiondir) were
  never committed to the branch.
- The 600 missing pairs were regenerated from the **committed frozen
  generator** `round2/fixtures/gen_r2p.py` (master seed 20260923) into
  workdir scratch `~/workspace/selfpam_consumer/pairs_full/` (600 committed
  pairs symlinked in, 600 regenerated).
- **Manifest check:** all 1,200 `.pair` SHAs verified against the committed
  `MANIFEST.r2p.sha256` — 1200/1200 OK (see below). The corpus the
  instrument read is byte-identical to the frozen corpus; nothing about the
  corpus changed.

## Acceptance runs (runs of record — executed AFTER amendment B commit)

Binary: `sense_bin` rebuilt from the committed sources reproduces
SHA-256 `1db54a68a3a5873ea4ea10e41afc51ec89ac1aa06294940a8b82ce3349bfca74`
byte-identically (verified by fresh `build_g1.py` run).
Corpus: `~/workspace/selfpam_consumer/pairs_full/` — 1,200/1,200 `.pair`
SHAs verified OK against the committed `MANIFEST.r2p.sha256` (600 committed
pairs symlinked + 600 regenerated from the frozen generator, seed 20260923;
170 photo inputs downloaded per `FIXTURE_SOURCES.md` and verified 170/170
against the committed photo manifest before regenerating motiondir).

Reports/ledgers committed under
`round2/forks/R2-3/evidence/admission_report_selfpam_r{1,2,3}.txt` and
`ledger_selfpam_r{1,2,3}.txt`.

| Run | Gate | Result |
|---|---|---|
| selfpam r1 | id 2 | withheld 1099/1200 (91.58%), overlap 0, 0 errors |
| selfpam r2 | id 2 | withheld 1099/1200 (91.58%), overlap 0, 0 errors |
| selfpam r3 | id 2 | withheld 1099/1200 (91.58%), overlap 0, 0 errors |
| regression id 0 | reference | report+ledger byte-identical to committed `admission_report_reference_r1/r2/r3.txt` + `ledger_reference_r1/r2/r3.txt` |
| regression id 1 | broken | report+ledger byte-identical to committed `admission_report_broken.txt` + `ledger_broken.txt` |

`ledger_final` (all three id-2 runs):
`644c61f0590746a7e7fa1575001b86b9939714df268d2b174972df9ab3465905`

## Verdict

- B1: 1,200/1,200 processed, 0 errors — PASS
- B5 `pairs_withheld/1200 >= 90%`: 1099/1200 = 91.58% — PASS
- Kill check `overlap_pairs == 0` on all id-2 passes: 0 — PASS
- B4 positive control (id 1: 100% overlap, <50% withhold): overlap 1200,
  withheld 0 — PASS (and byte-identical to the frozen R2-3 verdict evidence)
- B6: ×3 byte-identical reports, ×3 byte-identical ledgers — PASS
- Hash chains: all 5 ledgers (3 id-2 + id-0 + id-1 regressions) verified by
  the committed patched `mirror/verify_ledger.py` — PASS
- Regression id 0/1 byte-identical to historical evidence — PASS (also
  independently confirms the 1,200-pair corpus is byte-identical to the
  corpus the R2-3 verdict evidence was generated from)

**Scope reminder:** these are registration-acceptance runs per amendments
2026-09-27-A/B. Per PREREG §5.5 they do not count as CELL-A; §8 blockers
remain open; DEMO_ONLY scope is unchanged.
