# BUILD_LOG_FIX1 — build record for the fix1 instrument binary

**Date:** 2026-09-27 | **Procedure:** `BUILD_RECORD_G1_ID2.md` (same as the
amendment-A build — no new build tooling)

## Toolchain pin

- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA-256 verified before compiling:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  (matches the committed pin exactly)

## Build

Ran `python3 build_g1.py --no-verify` from
`docs/lab/senses/pam-rebuild/round2/forks/R2-3/src/`:

- Vendoring check passed: `g1_candidate.zag` in the build dir is
  byte-identical to `selfpam/src/g1_candidate.zag`
  (`b7f9622a834bdc8a06235eb6846ce1d351db155df9d35890b6451a19c90a48d1`).
- Source SHAs staged (content SHA-256):
  - `sense.zag`: `4874064b1883a58511cf5d3953ef9fa4e1614792d324f72aec1e7b39baef09a6`
  - `r2p_gates.zag`: `04193a19df136dceeb99113b89a78ec8a6b77b8a4190e6142a91d5ee49bf5271`
  - `g1_candidate.zag`: `b7f9622a834bdc8a06235eb6846ce1d351db155df9d35890b6451a19c90a48d1`
  - `codec.zag`: `ca9d1fd1cd10b164e95a2ca2f4b2a96c7944ba7452958cb0d1156db9643ccd4c` (unchanged)
  - `R33_NATIVE_IO_V1.zag`: `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` (unchanged)
  - `R33_NATIVE_SHA256_V2.zag`: `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` (unchanged)
- Result binary: `fd13d2eb9ca8a1677420b6f8f2a47f6be5cf46fa54f988d68d6f97b3667560ca`
  (build scratch only — NOT committed, per the repo content standard)

The raw `build_g1.py` output (with staged SHAs) is in `build_fix1.log`.

## Runs

- Corpus manifest check: 1200/1200 `.pair` SHAs OK against
  `round2/fixtures/r2p/MANIFEST.r2p.sha256`.
- `sense_bin 2/3/4` × 3 runs each (ids 2, 3, 4), plus `sense_bin 0` and
  `sense_bin 1` regression runs. ~19 s per 1,200-pair run.
- Results: id 2 → 1200/1200, id 3 → 1099/1200, id 4 → 1200/1200;
  0 errors, 0 overlap everywhere; ×3 byte-identical reports and ledgers;
  all 11 hash chains verified with `mirror/verify_ledger.py`.
