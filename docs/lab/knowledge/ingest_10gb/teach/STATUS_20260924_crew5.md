# 10GB Generalist Phase 2 — Crew-5 Status (2026-09-24 ~06:45 UTC, in progress)

## What crew 5 did

1. **Found job_wiki_crew4.sh alive** (restarted 06:21 UTC after daemon restart,
   en14 at 40,338 files, in skip phase). Did NOT blindly trust the resume:
   discovered the en14 invocation passed NO skip/start args — every restart was
   doing a full byte-identical REWRITE of en14 from page 0 (self-healing but
   wasting ~2h per restart at ~6 pages/sec).
2. **Killed it** (~10 min in, verified rewrites were byte-identical so no
   harm), then verified all 40,338 en14 files: contiguous 0..40337, every file
   ends with `</mediawiki>\n`, zero bad files.
3. **Caught a duplicate**: a second job instance (old-script, full rewrite,
   started 06:28:35 by the parent per resume instructions after seeing the job
   dead from my kill) was running concurrently. Killed BOTH chains, re-verified
   (still 40338/40338 good — kills landed between writes), then restarted ONE
   instance.
4. **Patched job_wiki_crew4.sh** (committed): every stem now computes its resume
   index via `verify_split.py` (highest contiguous well-formed index from 0)
   and passes `skip_n=start_n=<resume_index>`. A truncated last file from a
   mid-write kill is now detected and rewritten; raw file-count resume would
   have skipped it forever. en1 uses the same verify-based resume (was hardcoded
   13942).
5. **Wrote verify_split.py** (committed): contiguity + tail-byte check per stem,
   prints `resume_index=N`. ~90s per 40K files.
6. **Restarted single instance** 06:36:50 UTC: `en14: resume_index=40338`,
   python running with `40338 40338` skip/start (read-only skip phase now).
7. **Re-verified 7 done-source SHAs** (prefix match; crew 4 verified full SHAs
   2026-09-23 23:25 UTC — all match manifests).
8. **Reviewed prepared scripts** merge_run1_zag.sh / run2_clean.sh /
   merge_run2_zag.sh — all correct; clean_batched.py uses stable key sort +
   sorted file iteration (deterministic). Runbook order confirmed.

## Current state (2026-09-24 06:45 UTC)

- **Wiki splits**: ONE instance running (script PID 9532, python PID 9822).
  en14 skip-scanning past 40,338 pages, then writes. Remaining: en14 (~128K),
  en17, en19, en22, en24, en26, en27 (3.4GB bz2 total), en1 resume, consolidate,
  batched clean → stage/wiki_run1. ETA ~40-50h at current box contention.
  Log: logs/wiki_splits_crew4.log.
- **Done & SHA-verified**: gb_A (2,559,300 / 5a0b2ee8…), gb_B (2,152,486 /
  7a1f1284…), ostx (56,485 / a530f27e…), se_bio (62,234 / 1f3ea38d…),
  se_chem (98,420 / 2c93bbb7…), se_phys (588,421 / 3b454f66…),
  se_math (3,809,868 / 35a4828e…).
- Disk: /home/hatch 79% used (22G free).

## RESUME INSTRUCTIONS (next crew / after restart)

1. Check: `tail -3 ~/workspace/scratch_10gb_work/logs/wiki_splits_crew4.log`
   and `ps aux | grep split_wiki`. Expect exactly ONE python + ONE script.
2. If dead: just re-run `~/workspace/scratch_10gb_work/job_wiki_crew4.sh`
   (background). Verification + skip resume are built in. DO NOT run two
   instances — check ps first.
3. If killed mid-write, the script's verify step detects the truncated tail
   file and rewrites it. If you want to check manually:
   `python3 ~/workspace/scratch_10gb_work/verify_split.py \
     ~/workspace/scratch_10gb_work/wiki_full en14`
4. When stage/wiki_run1/facts.dat exists: run merge_run1_zag.sh →
   facts_run1.dat (+SHA). Python cross-check if time permits.
5. Then run2_clean.sh → merge_run2_zag.sh (SHA determinism gate).
6. Teach ×2, panswer ×2, score per TEACH_RUNBOOK.md / EVAL_PLAN.md.
   Teach invocation: `./gate_bin ingest facts_run1.dat bad.bin store1/ ncap`
   (gate_bin has NO `teach` mode; bad.bin = ~/workspace/tmp10/bad.bin;
   ncap = nrecs*1.2+100000).
7. Commit deliverables to tnn-native-lab under knowledge/ingest_10gb/teach/
   (commit_racefree.py or commit_big_files.py, TMPDIR=~/workspace/tmp_commit).

## Commits (crew 5, tnn-native-lab)
- <TBD>: job_wiki_crew4.sh (verify-based resume), verify_split.py (new),
  STATUS_20260924_crew5.md.

## Box discipline (unchanged)
- Sequential jobs only. Never /tmp for bulk. Never touch ingest_1gb/ or the
  frozen baseline probes. Never commit binaries/.zagd/.zag-cache/bulk data.
