# RUNLOG — Phase 2 resume (2026-09-23, post-daemon-restart)

Previous crew killed by daemon restart; checkpoint STATUS_20260923_1215.md read.
Work dir: ~/workspace/scratch_10gb_work/ (stage/, logs/). TMPDIR not needed
(clean2.py/merge write directly; no bulk temp files).

## Resume findings (verified, not assumed)
- Stage inputs intact: stage/raw/{gutenberg (1745), gb_A (877), gb_B (868), openstax (7 books)},
  stage/se_{bio,chem,phys}_in (chunked XML), se_math/Posts.xml (5.8G, extracted 12:52),
  9 enwiki bz2 at ~/workspace/scratch_10gb/enwiki_20260901/.
- Partial run-1 outputs: gb_A 642/877, gb_B 263/877 (no facts.dat — killed mid-run),
  se_phys mid-run, wiki en1 split 13,943 pages (contiguous n00000000..n00013942).
- Complete run-1 outputs: ostx_run2 (56,485 facts, +R9.6fix, sha a530f27e),
  se_bio_run2 == se_bio_run3 (62,234 facts, sha 1f3ea38d — determinism already proven),
  se_chem_run1 (98,420 facts, +R9.6fix, sha 2c93bbb7).
- gate_bin: works (modes: ingest/sindex/query/bquery/revise/delete/report/panswer).
  "teach" in runbook = `ingest <facts> <bad> <outdir> <ncap>`; negcontrol runs
  inside ingest automatically. audit.log embeds the facts path string — both
  teaches must use the SAME path string for byte-identical stores.
- Biology 2e: DEAD (only 106MB partial + no downloader process). Documented gap
  per SOURCES.md (byte gap covered by Gutenberg extension) and runbook §known gaps.
  No retry — acquisition phase already settled this.
- panswer "5% CPU" profiled: NOT a code bug. strace: 31s wall, 0.008s syscalls.
  Box is oversubscribed (loadavg 9.1 on 2 vCPU; Python 20M-iter loop 9.8s vs ~1.5s
  free). Scan runs ~7K facts/s CPU-bound; full ~5M-fact store ≈ 12min CPU/run,
  ~1h wall at current load. Accept and document; no gate.zag changes.
- questions.tsv: 250/250 ids match frozen battery, texts byte-identical, 2 cols (no answers).

## Memory crisis + fix (2026-09-23 ~13:35)
- phys clean2.py SIGKILLed (rc=137, OOM): box has 7.9GB, 0 free. clean_tree
  accumulates all_recs + cleaned_concat in RAM.
- Measured RSS: gb_A 839MB, gb_B 1160MB (growing), math 837MB (6/87 chunks —
  projected ~12GB!). All would OOM.
- Fix: clean_batched.py — partitions files in R0 order, runs UNMODIFIED
  clean2.clean_tree per subset via symlink tree, k-way merges subset facts.dat
  with merge_facts. PROVEN byte-identical to monolithic on 30-file test
  (sha 7eb92ad3..., cmp PASS).
- Killed monolithic gb_A/gb_B/math; removed stale partials. Relaunching batched:
  gb_A (877 files, 100/subset), gb_B (868, 100/subset), phys (16 chunks,
  4/subset), math (87 chunks, 5/subset), wiki (after split, ~9K pages/subset).
- proc gbA: clean2 --raw stage/raw/gb_A --out stage/gb_A_run1 (full rerun, deterministic)
- proc gbB: clean2 --raw stage/raw/gb_B --out stage/gb_B_run1
- proc phys: clean2 --raw stage/se_phys_in --out stage/se_phys_run1
- proc math: job_math.sh (chunk 5.8G Posts.xml -> stage/se_math_in, clean -> se_math_run1)
- Relaunched batched (all healthy, RSS 80-275MB):
  - proc gbA: clean_batched.py stage/raw/gb_A -> stage/gb_A_run1 (100/subset, 9 subs)
  - proc gbB: clean_batched.py stage/raw/gb_B -> stage/gb_B_run1 (100/subset, 9 subs)
  - proc phys: clean_batched.py stage/se_phys_in -> stage/se_phys_run1 (4/subset, 4 subs)
  - proc math: clean_batched.py stage/se_math_in -> stage/se_math_run1 (5/subset, 18 subs)
- proc wiki: job_wiki.sh RESTARTED (proc_40728bac7088) after OOM kill. The first
  attempt died silently during en1 skip (no output written, processes gone;
  system memory was at ~1GB available). Now 3.86GB available. Fast byte-scan
  resume: en1 skip 13942/start 13942, then en9/14/17/19/22/24/26/27.

## Plan after cleaning
1. merge_teach.sh 1 -> facts_run1.dat (+ sha256)
2. Re-run ALL 8 sources fresh -> merge -> facts_run2.dat; require SHA match
3. teach_store.sh: ingest facts_run1.dat twice (ncap sized +20%), diff -r stores
4. panswer store1 twice -> diff answers.tsv
5. score_panswer.py -> probe_results.tsv; delta vs 14/250 + 5/18 baseline
6. New-connections autopsy (exact probe + response bytes); misses documented
7. Commit code/specs/reports/SHAs (never gate_bin/.zagd/bulk data)
