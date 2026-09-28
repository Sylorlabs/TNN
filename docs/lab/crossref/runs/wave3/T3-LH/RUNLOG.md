# RUNLOG — T3-LH crossref crew (wave3 tier-3)
Session: a88095a4-7b3a-4c08-bb9b-18915ddb0798
Started: 2026-09-24 00:33 PDT

## 1. Frozen prereg verification
- Prereg file: ~/workspace/tnn-lab/crossref/PREREG_TIER3.md
- sha256 of file on disk: 538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1
- T3-LH section: lines 21-27 (extracted via sed -n '21,27p')
- Local tnn-native-lab head (pre-fetch): 5643289
- Committed PREREG_TIER3.md (blob 943ab5c984cd16b4a618bbc94329780b2d425a68 at branch head, fetched via API, base64-decoded): sha256 = 538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1 — IDENTICAL to on-disk file. Step-1 gate PASSED (earlier mismatch was a gh-api --raw misuse artifact; re-fetched properly).
- T3-LH section as committed (lines 21-27) matches the extracted text; it contains NO mention of commit c28f2e3a — that identifier comes only from the crew dispatch task.

## 2. Commit c28f2e3a verification (API + git)
- API: GET /repos/sylorlabs/TNN/commits/c28f2e3a -> HTTP 422 "No commit found for SHA: c28f2e3a"
- git: local clone shallow (1 commit); `git fetch origin c28f2e3a` -> "couldn't find remote ref"; prefix not in first 200 commits of branch.
- Local repo grep for 'c28f2e3a': no hits in docs/lab, crossref, ops.

## 3. Remediation commit chain verification (API)
All commits listed resolve on tnn-native-lab (full SHAs via API, files enumerated):
- 94498e7d0a84 freeze preregistration (wave12)
- c3dc58d472 clean learner core + whitebox suite (wave12)
- 3cb3a8b46 / a4f91852 verification evidence
- 825594a5 analogy prereg; b3f1df23 analogy test driver + evidence + verdict
- 9ed0203a freeze LH battery clean-rerun prereg (PREREG_RERUN.md)
- 3642f69e rerun apparatus (harness + runner)
- 445464a3 / 22ad3a90 clean-rerun evidence + verdict (1/4)
- 18330599 clean-rerun evidence (2/4: LH-1 and LH-5 runs)
- c7fcf8d3 clean-rerun evidence (3/4: LH-2 runs)
- 0cd56df2 clean-rerun evidence (4/4: LH-3 runs)
- c9ac9fb1fd8f886fe26cfccb86b12d3b95fff6e4 R34 remediation: annotate tainted evidence — 36 files (35 modified docs + CONTAMINATION_REGISTRY.md)
- a01a5e83 freeze COMPARISON prereg; fe0cda3d86485eb56a0802c5dde2ca40ab5ea2cc COMPARISON analysis + verdict (RNG verdict; tree ecc3fda4, 4 files added)
- Spot-check 3 annotated docs at branch head via API: LH-1/RESULT.md, longhorizon/PREREG.md, ruleslab/TRIAL_RESULTS.md — all carry "## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)" intact.

## 4. Spot rerun: LH-1R from committed sources (clean checkout)
- Clean-checkout dir: ~/workspace/scratch-crossref/T3/T3-LH/crew/clean/ (layout mirrored: clean/wave12/r34-remediation/{r34_clean_learner.zag, r34_lh_clean_harness.zag, rerun/} + clean/toolchain/...)
- Committed sources fetched as git blobs (sha verified): learner f1dbdbdc... (sha256 4f4b436b...), harness 7823055f... (sha256 c95144bb...). Both match the original crew's source.sha256.txt record exactly.
- Toolchain substrate from pinned local: R33_CONTINUING_LIFE_V1/{common,observation,world,storage,checkpoint}.zag + R33_NATIVE_SHA256_V2.zag + R33_NATIVE_IO_V1.zag (not on branch; documented).
- Build (cwd=rerun/): znc <harness> --no-zagd --no-analyze --no-foreground-cache -o lh_clean -> wrote native binary, exit 0. First attempt failed with layout lesson (added wave12/ middle level to match original).
- lh1 run1 exit 0; lh1 run2 exit 0; stdout byte-identical excl. LH_RESOURCE telemetry (sha256 da312916... both runs).
- Byte-identical vs committed evidence lh1_run1.stdout.log (blob faa7d297...; matches bundle SHA256SUMS 54054ff7...).
- PASS bars all hold: train_updates==480; LH_FAILURES=0 (ea=16,eb=16 per block); ra=15,active=0,upd_delta=0; disabled B 12/24 with updates==0; scramble A 0/16; 19+1 switches; 16 explores; max|score| 22300 — exactly the recorded verdict profile.

## 5. Verdict
SPOT-REPRODUCED. Anomaly recorded: dispatch identifier c28f2e3a does not resolve on any branch (API 422); actual final comparison verdict commit is fe0cda3d86485eb56a0802c5dde2ca40ab5ea2cc.
