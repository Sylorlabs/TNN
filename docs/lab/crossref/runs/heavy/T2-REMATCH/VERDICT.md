# VERDICT — T2-REMATCH crossref replication (heavy crew)

**Track:** T2-REMATCH — senses long-horizon rematch replication
**Crew:** T2-REMATCH heavy (crossref program)
**Frozen prereg:** `crossref/PREREG_TIER2.md` § "T2-REMATCH — senses long-horizon
rematch: B STAYS DEAD (Type A)", sha256
`90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`
(byte-identical to the copy committed on `tnn-native-lab` @
`0f8fa713adbe5c8966308f1354a44e287f9b9c22`, extracted programmatically).
**Pinned verdict commit:** `1c01a1adcf8dcec824b77f11e83a9c3fe91c2634`
(API-verified, ancestor of tnn-native-lab).
**Date:** 2026-09-24
**Budgets run:** T1, T2, T3, T4 (all four; T3 included though the prereg
permits T1/T2/T4 only) + TEST_FRESH / TEST_R1 / ADV_R1 eval sets.

## Clean-checkout verification (before any rerun)

- 41 frozen blobs under `docs/lab/senses/{rebuild,rematch}` @ 1c01a1ad fetched
  via API: 40 byte-identical to the local working files (all Python pipeline
  code, all Zag sources, `gen.py`, `score.py`, `relations.py`, CALIBRATION.md,
  PREREG_AMENDMENT.md, counts.json). The single diff (`rematch/VERDICT.md`)
  is the later 3f013f01 revision whose only change is the "Commits" section
  (all result numbers identical). 2 files absent locally
  (`harness/fixtures/MANIFEST.sha256`, `REGENERATION.md`) were downloaded
  from the pinned commit for verification.
- Rebuilt both binaries from the verified sources with the pinned toolchain
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  `--no-zagd --no-analyze --no-foreground-cache`): md5
  `f35a4b23f50e5f546e579dbd037367d6` (A) and
  `7bf5598ecdac8dcdcc030cfeaeebd0f4` (B) — byte-identical to the on-disk
  originals and to the BUILD_LOG.md record. Zero RNG in either binary.
- Fixture data: TRAIN_T2 (3,700), TRAIN_T3 (18,500), TRAIN_T4 (37,000) —
  0 sha-mismatches vs committed MANIFEST.sha256 (local manifest files
  byte-equal to the committed ones @ 85bc2687); TRAIN_T1 (740 files) and
  TEST_FRESH (740 files) byte-identical to fresh deterministic regeneration
  (frozen `gen.py`, seeds 20260922/20260923), proving per-index determinism;
  all `.truth` files present and parseable. Round-1 harness fixtures:
  2,020 files, 0 mismatch vs pinned manifest.
- Rerun workdir: `~/workspace/scratch-crossref/T2-heavy/T2-REMATCH/work/`
  (verified script copies; data via symlink; original artifacts untouched).
  `run_all.py` used unmodified (Pool(2), chunked + resumable).

## Results (my rerun vs committed)

All binary-evaluation caches byte-identical to the originals:
- TRAIN_T1: 740 records, errors 0, byte-identical
- TRAIN_T2: 7,400 records, errors 0, byte-identical
- TRAIN_T3: 37,000 records, errors 0, byte-identical
- TRAIN_T4: 74,000 records, errors 0, FULL file byte-identical
  (sha256 `a43f80df95283e68...`)
- TEST_FRESH: 740 records, errors 0, byte-identical
- TEST_R1: 740 records, errors 0, byte-identical
- ADV_R1: 370 records, errors 1, byte-identical (1 pre-existing error:
  approach A, shapetrans p042.img, task_failed — also in original)

`compare_results.py`: ALL MATCH — per-budget params, accuracies, KB4 rates,
ops identical to committed `results_main.json` for budgets T0–T4.

### Learning curve (TEST_FRESH, fitted means)

| Budget | A mean | B mean | B−A |
|---|---:|---:|---:|
| T0 | 72.1% | 52.1% | −20.0pp |
| T1 | 83.8% | 56.0% | −27.8pp |
| T2 | 83.8% | 56.2% | −27.5pp |
| T3 | 83.8% | 56.6% | −27.1pp |
| T4 | 83.8% | 56.6% | −27.1pp |

- **B never crosses A:** all B−A deltas negative (−20.0 to −27.8pp).
- **B never reaches 60%:** maximum B mean is 56.6% (T3, T4).
- **KB6 fails as claimed:** `confirmed=false`, decision `"B STAYS DEAD"`.
  T4 B_mean=56.6% (< 60% bar); B−A=−27.1pp (< +2pp bar).

### KB5 (byte-identical rerun digest)

Three fresh binary-evaluation reruns (TEST_FRESH + ADV_R1) + deterministic
fit, sha256 of complete results JSON:
- Run 1: `100b19f438b378297d96bf7082061597771464b6595a7d009017dc870bfd968e`
- Run 2: `100b19f438b378297d96bf7082061597771464b6595a7d009017dc870bfd968e`
- Run 3: `100b19f438b378297d96bf7082061597771464b6595a7d009017dc870bfd968e`

All three identical to each other and to the committed
`kb5_digests_committed.txt`. KB5 PASS, exit 0.

## Verdict

**REPRODUCED.** All four budgets (T1–T4) plus T0 (via fit) rerun from clean,
committed sources with byte-identical binary-evaluation caches. B never
crosses A at any budget; B never reaches 60% (max 56.6%); KB6 fails both
bars as claimed (`confirmed=false`, "B STAYS DEAD"); KB5 digest matches the
frozen value exactly across three fresh reruns.

## Anomalies

- Six VM reboots during the rerun (2026-09-23 12:55, 14:50, 17:38 UTC;
  2026-09-24 02:54, 04:36, 06:20 UTC). All JSONL caches survived intact;
  pipeline resumed from completed records each time. No other crews' jobs
  were killed.
- Heavy environmental contention (load 13–43): unrelated Wiktionary
  extraction, PAM R2 evals, fixture generation, 10GB cleaning jobs.
- `/tmp` 95% full (other crews' files); chunk comparisons moved to workspace
  scratch. No other crews' files deleted.
- RUNLOG chunk-20 spot-check was invalid (`/tmp` ENOSPC made both `sed`
  writes fail; `cmp` compared empty files). Superseded by the full final
  `cmp` confirming the entire T4 cache byte-identical.

## Artifacts
- `RUNLOG.md` (this crew's run log)
- `work/results_xref.json`, `work/verdict_summary_xref.json`
- `work/kb5_final.log` (three digests), `work/kb5_runs.log`
- `work/pipeline_xref.log`, `work/stage2.log`
- `work/runs_*.jsonl` (fresh binary-evaluation caches)
