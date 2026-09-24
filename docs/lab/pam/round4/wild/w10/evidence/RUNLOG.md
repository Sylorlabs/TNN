# W10 runlog — 2026-09-24

## Fixtures (frozen, inherited; byte-identical re-verified before build)
- `wild/w10/w10_bundles.txt`: 2291 bundles (C=1102, B=1109, W=12, P=18, F=50)
- Generator `wild/w10/gen_w10.py` rerun -> byte-identical (recorded in
  `wild/RESUME_WILDB3.md`).

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; `--no-zagd`).
- Command (cwd `pam/round4/wild/w10`, IO module copied beside source):
  `znc w10_duel.zag -o ~/workspace/scratch_wildb3/w10_duel --no-zagd`
- Result: success; only the known benign A0101/A0102 warnings.
- content_sig exceeds signed i64: the instrument tracks
  (content_sig mod 1024000) via Horner parsing, which determines
  (content_sig mod 1000) exactly (1024000 mod 1000 == 0) and the T_splice
  bit-op result mod 1000 exactly. The scorer mirrors with exact big-int
  arithmetic; all 2291x6 E values agree.
- Binary is scratch-only (NOT committed):
  `~/workspace/scratch_wildb3/w10_duel`

## Battery (3 runs)
- `./w10_duel w10_bundles.txt 1000 > w10_mu1000_a.txt`
- `./w10_duel w10_bundles.txt 1000 > w10_mu1000_b.txt`
- `./w10_duel w10_bundles.txt 500  > w10_mu500.txt`
- `cmp w10_mu1000_a.txt w10_mu1000_b.txt` -> identical (K2).
- SHA-256 mu=1000:
  `be483f1e59ebac6280e2a9ffa1ab537086d291f86758417c5fbbbb70cf6e90e4`
- SHA-256 mu=500:
  `efd48b92b1c2332e59fc208d8b09e56ce9bca6d93ff9ba87ed29c6e9dd85a5c9`

## Score
- `python3 wild/w10/score_w10.py w10_mu1000_a.txt w10_mu1000_b.txt w10_mu500.txt`
  -> exit 0. All 2291 candidates' 6 spoof E values, bestT, margin, verdict
  match exact-arithmetic recomputation.
