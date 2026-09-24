# Crew-4 Handoff — 10GB Generalist Phase 2

## Completed (2026-09-24)

### Math cleaning: DONE
- 3,809,868 facts, SHA256: 35a4828ebb696d488c11cc7288fdb41d740cfe8d15398a8d0a2affe08d981c2d
- Location: ~/workspace/scratch_10gb_work/stage/se_math_run1/facts.dat
- MANIFEST.json written (clean_batched format).
- NOTE: Final subset merge was redone with merge_zag_bin two-stage (9+9 shards)
  after the Python k-way merge process died silently at 89%. The two-stage Zag
  merge was PROVEN byte-identical to merge_facts.py on a tie-heavy synthetic
  fixture (SHA bb0d5260... both). Tie-break logic verified: strictly-less
  comparison keeps lowest shard index.

### Wiki en9 split: DONE
- 223,959 pages (shard_00: 50K, shard_01: 50K, shard_02: 50K, shard_03: 50K,
  shard_04: 23,959). Files verified well-formed.

### Wiki en1: 13,942 files (pre-existing, verified contiguous)

## In Progress

### Wiki remaining splits: RUNNING (long pole, ~40h)
- Script: ~/workspace/scratch_10gb_work/job_wiki_crew4.sh
- Log: ~/workspace/scratch_10gb_work/logs/wiki_splits_crew4.log
- Status (2026-09-24 06:05 UTC): en14 at 35,038 files, writing at ~6.3/sec.
- Remaining: en14 (partial, ~138K to go), en17, en19, en22, en24, en26, en27,
  en1 resume, consolidate → stage/wiki_in, batched clean → stage/wiki_run1.
- The script auto-resumes. If killed, just re-run it.
- WARNING: `grep ^en1` falsely matches en14_ files. Use find -name "en1_n*.xml".

## Prepared (committed, not yet run)

- merge_run1_zag.sh: 8-source run-1 merge (ostx, gb_A, gb_B, se_bio, se_chem,
  se_phys, se_math, wiki) → facts_run1.dat
- merge_run2_zag.sh: 8-source run-2 merge + determinism gate
- run2_clean.sh: independent re-cleaning of all 8 sources to *_r2 dirs

## Commits (tnn-native-lab)
- f5c3fb26: STATUS, job_wiki_crew4.sh, merge_run1_zag.sh
- e5abb692: merge_run2_zag.sh, run2_clean.sh, STATUS
- a7cdb741: STATUS (restart/resume)
- e67d193e: STATUS (resume instructions)

## Blocked
- Run-1 merge: waiting on wiki splits + clean (stage/wiki_run1/facts.dat)
- Run-2: waiting on run-1 merge
- Teach/panswer/score: waiting on run-2

## Verified Run-1 source SHAs (2026-09-23 23:25 UTC)
- gb_A: 2,559,300 facts, 5a0b2ee8d616a8d99300404d5c2c97feed63c23fba3457dc0b27c01f04e354ad
- gb_B: 2,152,486 facts, 7a1f12848f4d858be288cbf71fdf725488ad89b1a93686c32962d9f6facfa1be
- ostx: 56,485 facts, a530f27e114f26287c4dc1a32cec2288c0495d76e46bc80825fce6c4669eb9f8
- se_bio: 62,234 facts, 1f3ea38da83979b7aa09aba85993589f4ff1a190ac094a4785c9d9ca15fa1c6d
- se_chem: 98,420 facts, 2c93bbb7b0f605e34faed402960e54cb63d9556924f09248d6bf47ef70a074f7
- se_phys: 588,421 facts, 3b454f66546193683906ca29a21a972778abc9b907953edff254253dc2f45fff
- se_math: 3,809,868 facts, 35a4828ebb696d488c11cc7288fdb41d740cfe8d15398a8d0a2affe08d981c2d
