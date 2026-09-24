# RUNLOG — T2-REMATCH crossref heavy crew (senses long-horizon rematch replication)

## Prereg verification (frozen)
- Local `~/workspace/tnn-lab/crossref/PREREG_TIER2.md` sha256:
  `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`
- Committed `docs/lab/crossref/PREREG_TIER2.md` @ tnn-native-lab (blob
  `b1178370036bffbda6eb68ea0989c0e427dc31b7`, branch head
  `0f8fa713adbe5c8966308f1354a44e287f9b9c22`) sha256:
  `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`
- MATCH. Frozen T2-REMATCH section extracted programmatically via sed on the
  `## T2-REMATCH` heading. Proceeding.
- Pinned verdict commit `1c01a1adcf8dcec824b77f11e83a9c3fe91c2634` verified via
  API ("senses-rematch: final results + verdict (B STAYS DEAD)"); it is an
  ancestor of tnn-native-lab (compare: ahead 387, behind 0).
- NOTE: `docs/lab/senses/rematch/` does NOT exist at branch head
  0f8fa713 — removed by later (RAW-VS-HUMAN wave) commits. Pinned commit
  1c01a1ad is the frozen evidence source; all reruns use its blobs.

## Plan
1. Download all frozen blobs under docs/lab/senses/{rebuild,rematch} @ 1c01a1ad;
   sha256-compare against local ~/workspace/senses-rebuild|rematch files.
2. Rebuild A and B binaries from verified committed Zag sources with the
   pinned toolchain ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
3. Verify local fixture data against committed manifests
   (TRAIN_T1/TEST_FRESH counts+MANIFEST @ 1c01a1ad; T2/T3/T4 manifests @ 85bc2687;
   round-1 ADV_R1/TEST_R1 fixtures vs committed MANIFEST.sha256 cdd1a6be8f).
4. Rerun binary evaluation (run_all.py) for budgets T1, T2, T4 (allowed subset;
   T3 skipped) + TEST_FRESH/ADV_R1/TEST_R1 eval inputs; then fit.py + analyze.py.
5. KB5: 3 reruns of the fitted pipeline; verify digest prefix 100b19f4...
6. Commit VERDICT.md + RUNLOG.md to tnn-native-lab (lab-relative paths
   crossref/runs/heavy/T2-REMATCH/...), TMPDIR=~/workspace/tmp_commit,
   commit_racefree.py; never touch VERDICT_TABLE.md.

## Log
- 2026-09-23 ~04:25 PDT: crew started; prereg verified; tree @ 1c01a1ad fetched.

## Source verification (all vs pinned commit 1c01a1ad)
- 41 frozen blobs fetched via API; 40 byte-identical to local files
  (all .py, all .zag sources, gen.py, score.py, relations.py, CALIBRATION.md,
  PREREG_AMENDMENT.md, counts.json ×2). 1 DIFF: rematch/VERDICT.md — local copy
  is the later 3f013f01 revision; diff is only the "Commits" section listing
  SHAs (all numbers identical). 2 LOCAL-MISSING: harness/fixtures/MANIFEST.sha256,
  REGENERATION.md — downloaded from pinned commit for verification.
- Rebuilt A and B binaries from verified sources with pinned znc:
  md5 f35a4b23f50e5f546e579dbd037367d6 (A) and 7bf5598ecdac8dcdcc030cfeaeebd0f4 (B)
  — BYTE-IDENTICAL to on-disk originals and to the BUILD_LOG.md record.
- Fixture data: T2 (3,700), T3 (18,500), T4 (37,000) fixtures — 0 sha-mismatch
  vs committed MANIFEST.sha256 (local manifest files byte-equal to committed
  ones @ 85bc2687). T1 (740 files) and TEST_FRESH (740 files) — byte-identical
  to fresh deterministic regeneration (frozen gen.py, seeds 20260922/20260923),
  proving per-index determinism. All .truth files present/parseable.
  Round-1 harness fixtures: 2020 files, 0 mismatch vs pinned manifest.
- Decision: run ALL FOUR budgets T1/T2/T3/T4 (T3 included though the prereg
  allows skipping it) + TEST_FRESH/TEST_R1/ADV_R1 eval sets, in clean workdir
  ~/workspace/scratch-crossref/T2-heavy/T2-REMATCH/work/ (verified script
  copies; data via symlink; original artifacts untouched).
- ~04:55 PDT: xref binary-evaluation pipeline launched (background, chunked +
  resumable run_all.py, Pool(2) as committed).

## Rerun progress
- Binaries smoke-tested OK (judgment/confidence/ops parse as run_all.py expects).
- T1 binary eval: 740 records, 0 errors (~5 min). My runs_TRAIN_T1.jsonl is
  BYTE-IDENTICAL (sha256 354697fc...) to the original crew's cache — binary
  evaluation fully reproducible from verified fixtures + rebuilt binaries.
- T2/T3/T4/TEST_FRESH/TEST_R1/ADV_R1 running sequentially (Pool(2) as committed);
  est. ~13h total at observed ~2.4 rec/s. Pipeline is chunked + resumable.

- T2 binary eval in progress: first chunk (2,000/7,400 records) byte-identical
  to the original crew's cache. VM heavily loaded (load avg 8→26, other crews:
  PAM R2-11 forks, wikt extraction, 10GB work) — observed rate ~80-144 rec/min
  vs original ~570/min. Pipeline is chunked+resumable; stage-2 (compare + KB5)
  chained to run automatically after. All four budgets retained for full
  REPRODUCED (digest match requires T3).

## Reboot incident (2026-09-23 ~12:55 UTC)
- VM rebooted (uptime reset). Pipeline parent bash + stage-2 + watcher died.
- State at reboot: T1 complete (740 rec); T2 at 6,000/7,400 records (chunks 1-3
  appended; final dedup/sort/rewrite not reached). No corruption: run_all.py
  resumes from the jsonl `done` set.
- Relaunching pipeline (resumes T2) + stage-2. This mirrors the original crew's
  4-reboot survival via the same resumable mechanism.

- T2 COMPLETE post-reboot: 7,400 records, 0 errors; full cache BYTE-IDENTICAL
  to original crew's runs_TRAIN_T2.jsonl (sha256 e348a43b...). Fresh-VM rate
  ~311 rec/min (1,400 motion records in 4.5 min) — T3/T4 now projected ~2h/~4h.
- T3 binary eval running.

## Second reboot (~14:50 UTC)
- VM rebooted again (uptime reset). T3 at 18,000/37,000 records (9 chunks done,
  all byte-identical to original). Pipeline/stage-2/watchers dead; /tmp wiped
  (scripts now live in crew/ dir, survived).
- Relaunching pipeline (resumes T3) + stage-2.

- T3 at 20,000/37,000 (chunks 1-10 byte-identical). VM load 25-35 from
  legitimate program work (PAM R2-4 fork evals, wikt extraction, 10GB
  cleaning). My Pool(2) kept modest per task. Rate ~50-60 jobs/min under
  this load; pipeline automated+resumable, stage-2 chained. Continuing
  full T1-T4 scope for REPRODUCED (digest match requires T3).

## Third reboot (~17:38 UTC)
- VM rebooted a third time. T3 at 24,000/37,000 (chunks 1-12 byte-identical).
  Relaunching pipeline (resumes T3) + stage-2.

## T3 complete (2026-09-23 19:40:12 UTC)
- 37,000 records, errors 0. All 18 chunks byte-identical to original cache.
  Full cache byte-identical. T4 (74,000) started.

- T4 at 40,000/74,000 (chunks 1-20 byte-identical). /tmp 95% full from other
  crews' work (rt_attack, wikt, etc.) — will use workspace scratch for chunk
  comparisons, not /tmp. Not deleting others' files.

## Fourth reboot (2026-09-24 02:54 UTC)
- VM rebooted (uptime reset to 1 min). T4 JSONL survived intact at 54,000
  records; chunks 25-27 re-verified byte-identical post-reboot.
- Pipeline, stage-2, and T4 run_all all died. Relaunched exactly one
  pipeline (PID 2652) and one stage-2 (PID 2653) at 02:55 UTC.
- Pipeline skipped T1/T2/T3 (complete) and resumed T4 (PID 2822 + 2 workers).
- T4 at 54,000/74,000, chunks 1-27 byte-identical. 20,000 records (10 chunks)
  remain.

## Fifth reboot (2026-09-24 04:36 UTC)
- VM rebooted again (uptime 0 min). T4 JSONL survived intact at 60,000
  records; last record valid JSON.
- All processes died. Relaunched exactly one pipeline (PID 1812) and one
  stage-2 (PID 1813) at 04:37 UTC. T4 resumed (PID 1962 + 2 workers).
- T4 at 60,000/74,000, chunks 1-30 byte-identical. 14,000 records (7 chunks)
  remain.

## Sixth reboot (2026-09-24 06:20 UTC)
- VM rebooted again (uptime 1 min). Pipeline had COMPLETED at 06:07:52 UTC
  before this reboot (XREF PIPELINE COMPLETE in log).
- T4 JSONL survived at 74,000 records. results_xref.json and
  verdict_summary_xref.json survived.
- kb5.py was interrupted by the reboot mid-run, leaving .kb5bak files and
  a missing runs_ADV_R1.jsonl. Restored both from byte-identical originals.
  A later kb5.py invocation was killed by exec timeout (not a reboot),
  leaving a partial fresh-eval TEST_FRESH; restored from original.

## T4 completion and full verification (2026-09-24 06:08 UTC)
- T4: 74,000/74,000 records, errors 0. FULL file byte-identical to
  ~/workspace/senses-rematch/runs_TRAIN_T4.jsonl (sha256 a43f80df95283e68...).
- Chunks 1-37 all byte-identical (2,000-record chunks).
- CORRECTION: An earlier RUNLOG entry claimed chunks 1-20 were byte-identical,
  but the chunk-20 comparison was invalid (both sed writes failed from /tmp
  ENOSPC, so cmp compared two empty files). The FULL final cmp above
  supersedes all chunk spot-checks and confirms the entire T4 cache is
  byte-identical.
- TEST_FRESH: 740 records, errors 0, byte-identical.
- TEST_R1: 740 records, errors 0, byte-identical.
- ADV_R1: 370 records, errors 1, byte-identical. The 1 error (approach A,
  shapetrans p042.img, task_failed) is pre-existing in the original.

## Results comparison (2026-09-24 06:08 UTC)
- compare_results.py: ALL MATCH for budgets T0-T4 (per-budget params,
  accuracies, KB4 rates, ops identical to committed results_main.json).
- Reproduced means (TEST_FRESH, fitted):
  T0: A=72.1% B=52.1% (B-A=-20.0pp)
  T1: A=83.8% B=56.0% (B-A=-27.8pp)
  T2: A=83.8% B=56.2% (B-A=-27.5pp)
  T3: A=83.8% B=56.6% (B-A=-27.1pp)
  T4: A=83.8% B=56.6% (B-A=-27.1pp)
- B never crosses A (all B-A negative). B never reaches 60% (max 56.6%).
- KB6: confirmed=false, decision="B STAYS DEAD", B_mean=56.6%, delta=-27.1pp.
  Both KB6 bars fail as claimed (needs B-A >= +2pp and B >= 60%).

## KB5 (2026-09-24 06:32-07:02 UTC)
- kb5.py: 3 fresh binary-evaluation reruns (TEST_FRESH + ADV_R1) + fit.py.
- All three digests identical:
  100b19f438b378297d96bf7082061597771464b6595a7d009017dc870bfd968e
- Matches committed kb5_digests_committed.txt exactly (all three).
- KB5 PASS, exit 0.
