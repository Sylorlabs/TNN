# 10GB Generalist Phase 2 — Crew-4 Status (2026-09-23 ~23:35 UTC, in progress)

## Session summary

Crew 4 resumed from STATUS_20260923_2345.md. Verified both inherited jobs are
alive (never restarted them). Verified all 6 done-source SHAs match manifests.
Prepared run-1 merge script (merge_zag_bin), remaining-splits script, and
confirmed the teach invocation form.

## Run-1 cleaning status (unchanged from crew 3 except progress)

### DONE & VERIFIED — SHAs re-verified 2026-09-23 23:25 UTC, ALL MATCH
| source | out dir | facts | SHA256 |
|---|---|---|---|
| gb_A | stage/gb_A_run1 | 2,559,300 | 5a0b2ee8d616a8d99300404d5c2c97feed63c23fba3457dc0b27c01f04e354 |
| gb_B | stage/gb_B_run1 | 2,152,486 | 7a1f12848f4d858be288cbf71fdf725488ad89b1a93686c32962d9f6facfa1 |
| ostx | stage/ostx_run2 | 56,485 | a530f27e114f26287c4dc1a32cec2288c0495d76e46bc80825fce6c4669eb9f8 |
| se_bio | stage/se_bio_run2 | 62,234 | 1f3ea38da83979b7aa09aba85993589f4ff1a190ac094a4785c9d9ca15fa1c6d |
| se_chem | stage/se_chem_run1 | 98,420 | 2c93bbb7b0f605e34faed402960e54cb63d9556924f09248d6bf47ef70a074f7 |
| se_phys | stage/phys_run1 | 588,421 | 3b454f66546193683906ca29a21a972778abc9b907953edff254253dc2f45fff |

### DONE (crew 4, 2026-09-24 ~03:35 UTC)
- **Math** (stage/se_math_run1): 3,809,868 facts.
  SHA256: `35a4828ebb696d488c11cc7288fdb41d740cfe8d15398a8d0a2affe08d981c2d`
  MANIFEST.json written (clean_batched format + merge_note documenting the
  Zag two-stage re-merge).

## Commits (crew 4)
- `f5c3fb26` (tnn-native-lab): STATUS_20260923_crew4.md, job_wiki_crew4.sh,
  merge_run1_zag.sh under knowledge/ingest_10gb/teach/.
- `e5abb692` (tnn-native-lab): merge_run2_zag.sh, run2_clean.sh, STATUS update.
- `a7cdb741` (tnn-native-lab): STATUS update (daemon restart, en14 resume).

## RESUME INSTRUCTIONS (for next crew / after restart)

If job_wiki_crew4.sh is not running:
1. Check progress: `tail -3 ~/workspace/scratch_10gb_work/logs/wiki_splits_crew4.log`
2. Verify existing files are contiguous (per stem): the script auto-resumes by
   counting `find $OUT -name "${stem}_n*.xml" | wc -l` and passing as skip/start.
3. Simply re-run: `~/workspace/scratch_10gb_work/job_wiki_crew4.sh` (background).
   It handles: en14/17/19/22/24/26/27 splits → en1 resume → consolidate →
   batched clean → stage/wiki_run1.
4. WARNING: `grep ^en1` falsely matches en14_ files. Use `find -name "en1_n*.xml"`.

### IN PROGRESS (updated 2026-09-24 06:28 UTC)
- **Wiki splits** (job_wiki_crew4.sh running, 4th start after 3 terminations):
  en14 at 40,338 files (in skip phase, will write once past page 40,338).
  Remaining: en14 (~133K to go), en17, en19, en22, en24, en26, en27,
  en1 resume, consolidate, clean. ~40h long pole at ~6/sec.
  The script auto-resumes; just re-run it after any kill/restart.
  Log: logs/wiki_splits_crew4.log.
- **Commits**: f5c3fb26, e5abb692, a7cdb741, e67d193e, 28167ff8, 112d4ef2
  (tnn-native-lab).

### Benchmark (crew 4)
New split_wiki.py (read-accumulation) on en14 bz2: 934 pages / 180s = 5.2/sec —
NO faster than old code (5.3-6.6/sec) under CPU contention. Box is the
bottleneck. Decision: leave en9 (PID 1880) undisturbed; no restart benefit.

## Key findings

- Teach invocation: gate_bin has NO `teach` mode. The working form (per
  teach_store.sh, matches binary usage) is:
  `./gate_bin ingest facts_run1.dat bad.bin store1/ ncap`
  where bad.bin (~/workspace/tmp10/bad.bin, 99780 bytes) is the 1000-record
  negative control, run automatically after ingest. ncap = nrecs*1.2+100000.
  The TEACH_RUNBOOK's `./gate_bin teach facts_run1.dat store1/` is shorthand.
- questions.tsv exists at ~/workspace/tmp10/questions.tsv (250 id\tquestion).
- panswer form: `./gate_bin panswer <storedir> <questions.tsv> <ansdir>`.
- Remaining bz2 files all present: en14,17,19,22,24,26,27 + en1 (3.4GB total).

## Scripts prepared (~/workspace/scratch_10gb_work/)
- job_wiki_crew4.sh — sequential en14/17/19/22/24/26/27 + en1 resume
  (skip=13942 start=13942) + consolidate → stage/wiki_in + batched clean →
  stage/wiki_run1. RUN ONLY after PID 1880 finishes.
- merge_run1_zag.sh — 8-source merge with merge_zag_bin in runbook order
  (ostx, gb_A, gb_B, se_bio, se_chem, se_phys[stage/phys_run1], se_math, wiki).
  Exits 1 if any shard missing. Writes facts_run1.dat + .sha256 + record count.

## Run-1 merge shard map (for merge + run-2)
- stage/ostx_run2/facts.dat, stage/gb_A_run1/facts.dat,
  stage/gb_B_run1/facts.dat, stage/se_bio_run2/facts.dat,
  stage/se_chem_run1/facts.dat, stage/phys_run1/facts.dat,
  stage/se_math_run1/facts.dat (in progress), stage/wiki_run1/facts.dat (todo)

## Next steps (for crew 4 continuation or crew 5)
1. Wiki splits running (job_wiki_crew4.sh). Wait for completion (~40h).
   If killed, re-run the script (it auto-resumes). See RESUME INSTRUCTIONS above.
2. After wiki splits + clean → stage/wiki_run1/facts.dat exists:
   Run merge_run1_zag.sh → facts_run1.dat (+SHA). Python cross-check if time.
3. Run-2: run2_clean.sh (repeats all 8 cleanings to *_r2 dirs), then
   merge_run2_zag.sh (merges + requires SHA facts_run2 == facts_run1).
4. Teach ×2 (teach_store.sh pattern), diff -r stores, record installed/rejected.
5. panswer ×2, diff answers.tsv, score_panswer.py, autopsy, new connections.
6. Commit deliverables to tnn-native-lab under knowledge/ingest_10gb/teach/
   (commit_racefree.py or commit_big_files.py, TMPDIR=~/workspace/tmp_commit).

## Box discipline
- Load ~13-19 on 2 vCPU. Sequential jobs only. math + en9 currently overlap
  (both inherited); do not add a third heavy job.
- Never kill PID 1880 or 272800 without recording state.
- Never /tmp for bulk. Never touch ingest_1gb/ or frozen baseline probes.
