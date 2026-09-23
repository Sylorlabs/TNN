# RUNLOG — T2-AUDIOCONT (replacement crew)

## Inherited state
- Predecessor crew was killed mid-run by runtime daemon restart; its final message never arrived.
- Verified partial state at ~/workspace/scratch-crossref/T2/AUDIOCONT/: only empty dirs clean/repo and crew — no VERDICT.md, RUNLOG.md, or checkouts survived. clean/repo was an empty directory, not a repo. Re-clone required (allowed: resume valid state, re-clone if corrupt/absent).
- Replacement crew dispatched 2026-09-22 ~21:36 PDT.

## Steps

## Pins frozen (recorded before running)
- Tier2 prereg (authoritative): `7b2100d09911c5c10252c5756c7def288e70bd1f` (commit object verified via git cat-file; branch tnn-native-lab, repo sylorlabs/TNN)
- Test head: `070c94cb46084c204433bf1d6d3567b4ebf574b3` (verified via GitHub API + git fetch)
- Red-team head: `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c` (verified via GitHub API + git fetch)
- Round-2 frozen prereg commit: `9d1dbf865e36ff3bd13a66c696af60e08fc94d95` (verified via git fetch)
- Baseline flagships (committed, commit `42cb573023d30d4ec79ccc1a9e976415b407cf54`):
  - b_gamma_kids_v3.wav SHA256 `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f` ✓ matches frozen pin
  - bbeta_kids_v3.wav SHA256 `94349376a35bd7dbc5d31ab5173c309243f19293680a91399674de22082baecb` ✓ matches frozen pin
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (SHA256 prefix `498abcb5ab346f8cb246222a`; used for all builds)
- ANOMALY: task text expected pin `e15eebc5c4ec` — does not exist as a commit/tree/blob in sylorlabs/TNN (GitHub API 422 "No commit found"; `git cat-file -t` → "Not a valid object name"), and appears NOWHERE in the frozen PREREG_TIER2/SCOPE at 7b2100d. All pins named by the frozen authority verified instead. Proceeded; recorded here and in VERDICT.md. (No STOP issued: the authority never pins this value.)

## Environment
- Clean clone: `~/workspace/scratch-crossref/T2/AUDIOCONT/clean/repo` (blobless clone of tnn-native-lab + explicit fetch of pinned commits; `git fsck` clean)
- Run dir: `~/workspace/scratch-crossref/T2/AUDIOCONT/crew/`; committed evidence extracted to `crew/evidence/` (docs + redscan.zag + flagship WAVs from pinned commits — no checkout, no live-tree copies)
- TMPDIR=/home/hatch/workspace/tmp_commit; all work under scratch, never /tmp
- Pure Zag for measurement/verification; deterministic Python/numpy used only as independent instrument cross-check (glue); zero RNG throughout

## Scope finding (recorded before running tests)
- The round-2 render battery sources (r2g.zag, r2b sources, patch_*.py, analyze_*.py, render WAVs, placement logs, redteam_out scan records) were NEVER committed: only 3 commits touch continuity_round2/ (prereg 9d1dbf, results 070c94cb, red-team f2c7b85e); at the red-team head, work/ contains ONLY redscan.zag. The frozen prereg promised "Results, fixed sources ... committed after" — the sources were not. A raw Type-A render rerun from committed sources is therefore impossible; replication proceeded on what IS committed: verdict docs, redscan.zag, ear clips/keys (keys never opened), and the flagship WAVs.
- Replication strategy: (a) Type C flagship-scan re-derivation from committed WAVs + committed redscan.zag (rebuilt from source); (b) instrument verification vs numpy; (c) pure-Zag exact re-derivation of the committed statistics and kill-rule decision logic for all six dispositions.

## Results
1. redscan.zag built from committed source with pinned znc: rc=0 (warnings only).
2. Flagship dip scans 3/3 byte-identical (md5 4cbd7bd1... bbeta, 1ca4ba70... bgamma):
   - B-β v3: floor5=8341 micro; runs: 590 ms @28710 ms, 180 ms @9170 ms, rest ≤60 ms; peak 707977, DC 0, zcr 2177.933/s, clipped 0 — BYTE-IDENTICAL to committed scan record (flag_bbeta_dip.txt values quoted in REDTEAM_ROUND2.md)
   - B-γ v3: floor5=15762 micro; runs: 1300 ms @28700 ms, rest ≤20 ms; peak 671234, DC 30, zcr 2808.200/s, clipped 0 — BYTE-IDENTICAL to committed record
   - "No missed unintended cutouts" re-derived ✓; longest runs are the scored/preserved endings (28.71 s / 28.70 s per frozen scores); no 100–990 ms variant-seed runs in flagships ✓
3. Instrument cross-check vs numpy: peak EXACT, zcr EXACT (3 decimals), DC and floor5 exact under the instrument's documented integer-truncation semantics (verified by reading the zag source: dcmean truncates in sample units before micro conversion).
4. statscheck.zag (pure Zag, zero RNG), 3/3 byte-identical (md5 332048dd...):
   - H1 sign-test p(boundary>within 7/20) = 0.942340 ✓ committed 0.9423
   - H1 sign-test p(overlap>within 8/20) = 0.868412 ✓ committed 0.8684
   - G3 Wilcoxon directional one-sided p(T+≤2) = 0.1875 → 0.19 ✓ committed 0.19
   - (Note: first draft used W=min formulation → 0.375; corrected to the directional T+ formulation the red team used; R/wilcox.test one-sided agrees with T+.)
5. Decision-logic re-derivation from committed numbers (all verified):
   - H1: kill-rule letter SURVIVES real (990 ms > 10 ms ceiling); rates run opposite the mechanism (boundary 10.25 < within 15.00, overlap 9.47 < 15.00; sign p≈0.94/0.87 against prediction) → mechanism contradicted → REFINED ✓
   - H2: 3/4 measures oppose seam hypothesis (one-sided p≈0.98–1.00 against), 4th n.s. p=0.4042 → no seam detectable at any preregistered measure → KILLED (machine) ✓
   - H3: four pooled p-values 0.979/0.992/0.259/0.259 — none significant → frozen letter INDETERMINATE (round-2 SURVIVES default unpreregistered) ✓; VOID-for-material rests on committed corpus limitation (19 wash + 21 wind grains, salt+700000 control reuses 95–100% of grains — recorded in RESULTS_ROUND2.md) ✓
   - G1: all corrected ratios (midpoints 0.83/1.21/1.50/2.16/0.97, exits 1.84/1.07/1.16/1.26/0.71) < 2.4 → letter SURVIVES ✓; margin collapsed 0.12→0.71–0.84; scene-relative shows no localized seam dips, kids reference fails its own bar → REFINED ✓
   - G2: min ratio 1.19 < 2.7 → letter SURVIVES ✓; scene-relative 1.23/0.93/1.40/1.28/1.75/1.00/2.14 shows no monotonic decline (max at 120 s) → drift contradicted → REFINED ✓
   - G3: Wilcoxon n=4 W=2.0 p=0.19 (re-derived), diffs −0.09/+0.23/−0.44/−0.36 mixed signs → density-stress masking failure not observed → KILLED (machine) ✓
   - No SURVIVES-with-confirmed-defect among the six → no v4 recomposition warranted ✓
6. Frozen docs stable: PREREG_ROUND2.md byte-identical across 9d1dbf/070c94cb/f2c7b85e; RESULTS_ROUND2.md byte-identical between test head and red-team head.

## PIN CORRECTION (coordinator, 2026-09-22 23:28 PDT)
- Coordinator confirms: `e15eebc5c4ec` was a transcription artifact (422 "No commit found" in sylorlabs/TNN). DISREGARDED per instruction.
- Proceeded on the frozen prereg's authority, exactly as the §1 rule required: all pins were extracted from `docs/lab/crossref/PREREG_TIER2.md` at frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f` and each was verified via the GitHub API (and git fetch) before running: test head `070c94cb46084c204433bf1d6d3567b4ebf574b3`, red-team head `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c`, round-2 prereg `9d1dbf865e36ff3bd13a66c696af60e08fc94d95`, flagship commit `42cb573023d30d4ec79ccc1a9e976415b407cf54`.
- Verdict unaffected: REPRODUCED (all six dispositions match; no KILLED hypothesis survives; no REFINED mechanism confirmed).
