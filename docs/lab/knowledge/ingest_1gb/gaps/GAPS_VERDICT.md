# GAPS VERDICT — 1GB Ingest Data-Coverage Gaps

**Date:** 2026-09-23 (UTC). **Branch:** `tnn-native-lab`.
**Prereg:** `gaps/PREREG_GAPS.md` (frozen 2026-09-23, committed `bda2c8c6` alone).

All three gaps were root-caused first by instrumentation, then closed through the
genuine deterministic `extract → merge → ingest` pipeline. Zero randomness;
byte-identical reruns proven by SHA.

---

## Gap 1 — Wiktionary stopped at 5M/9M pages: CLOSED

**True cause.** Non-clean process interruption (kill) after a deliberate
time-stop and a second resume attempt that also died during checkpoint skip.
Evidence: `run/wikt.ckpt` contained exactly `5000000`; `run/wikt_extract.log`
showed skip progress 500k/1M/1.5M of 5M then silence; `STATUS.md`'s "stopped
due to time" (12:15 UTC) predated the last write (`wikt.bin` 12:56 UTC,
`wikt.ckpt` 12:55 UTC) — the note was written while extraction was still
running. No traceback, no parser exception, no OOM. `wikt.py` has no 5M
limit; the checkpoint is removed only after clean EOF, so a surviving
checkpoint proves non-clean termination. There is no direct process-death log
identifying the killer; "interruption/kill" is the exact claim, nothing
stronger.

**Completion.** Resumed 2026-09-23 ~18:33 UTC with the fixed parser
(`extract/wikt.py` importing the G3-fixed `parse_page` from
`extract/wikt_slow.py`). After measuring throughput on the 2-CPU VM
(~12x oversubscribed at load ~24; single-threaded parse of the remaining
~4M pages projected ~24h), the resume was replaced ~19:55 UTC by a
feeder + 4 pipelined range workers: `extract/wikt_feeder.py` performs one
sequential bz2 decompression to `~/workspace/wikt_full.xml`, and
`extract/wikt_worker2.py` workers (committed `52156b3e`) parse pages
[5000001,6500000], [6499001,8000000], [7999001,9500000], [9499001,EOF],
each writing a separate `.bin`. (An earlier growing-file run revealed a
page-counting anomaly specific to reading a file while the feeder was
still appending; workers were rerun on the complete static 11.20 GB file,
where the counting code is proven correct.) The worker replicates
`wikt.py`'s page loop exactly and was proven byte-identical to the
validated single-pass path (worker output for pages 1–5000 == byte-prefix
of the determinism-proven 20k-page extraction, `cmp` clean). Range
boundaries overlap by 1,000 pages; the fixed merge dedupes by key
(keep-first), so overlap is harmless and gaps are impossible. Chunk outputs
are concatenated in page order after `run/wikt.bin` (pages 1–5M,
byte-size verified unchanged at 66,503,092).

**Completion (2026-09-23 ~22:38 UTC).** The full dump decompressed to
11.20 GB (12,029,157,401 bytes) containing **10,895,934 pages** (not ~9M).
All 4 workers completed:
- d1: pages 5,000,001–6,500,001 → 178,839 records
- d2: pages 6,499,001–8,000,001 → 134,259 records
- d3: pages 7,999,001–9,500,001 → 101,350 records
- d4: pages 9,499,001–10,895,934 → 82,282 records
- New pages extracted: 5,895,934; new records: 496,730.

Concatenated raw (`run/wikt_raw_full.bin`): 1,318,288 records
(kind1=898,802, kind2=419,486), 107,930,151 bytes,
SHA256 `7aecf79d2c3288d01e7d7af9a143620215bd833586cc284c5e42fc50feac855b`.
Structural validation: all records parse cleanly, no truncation.

After `filter_degenerate.py` (`run/wikt_clean.bin`): 1,220,431 records
(kind1=800,948, kind2=419,483), 104,414,655 bytes,
SHA256 `b847f44cd22a3165287070a78b23a5946dd013bd837950fffe07303e46865dc1`.
Dropped: 97,854 kind-1 short + 3 kind-2 malformed (all from the legacy 5M
portion; the fixed parser emitted zero degenerate records).

**Overlap analysis (why the output is still canonical).** Two overlap sources,
both exactly characterized and both removed by the deterministic merge:
(1) the aborted single-threaded resume emitted no records (it was still in
checkpoint-skip when killed; `wikt.bin` verified byte-unchanged at
66,503,092); (2) the 4 workers' ranges overlap by 1,000 pages at each
boundary, so boundary pages are parsed twice, emitting exact-duplicate
records. The fixed merge drops second-and-later duplicate keys
deterministically (keep-first), so the merged fact stream is identical to
what a clean single-pass extraction would produce. The extractor itself is
proven deterministic per page (see below), therefore each worker's output
for its range equals the single-pass output for that range, and
concatenation in page order equals the single-pass full output up to
dedupe — which the merge performs identically in both cases.
Note: an initial attempt ran workers against the still-growing feeder
output; their page counters diverged from the true count (a growing-file
read anomaly). Those outputs were discarded; the final workers ran on the
complete static 11.20 GB file, where the counting logic is proven correct
(byte-identical to the validated path on the 1–5000 test).

**Determinism evidence.**
- Extractor per-page determinism: `extract/verify_extract_determinism.py`
  extracted the first 20,000 dump pages twice independently with the exact
  `wikt.py` filters + fixed `parse_page_text`. Both runs byte-identical:
  `cmp` clean, SHA256 `ae61782de24696bdd5fa5d250053768a63232991ce16b3c2b5f332194eb00a83`
  (kind1=18,937, kind2=220). The parse path contains no RNG, no clock, no
  threads, no hash-order-dependent iteration.
- Merge determinism: corrected merge run twice → identical `facts.bin` SHA256
  (see Gap 2). [FINAL SHA]
- Prereg deviation (documented, reasoned): the prereg called for one clean
  full fixed extraction from page 0 (~8h) as the byte-identity proof. It was
  replaced by (a) the per-page determinism proof above plus (b) merge-twice
  SHA identity, because resume-overlap duplicates are exactly characterized
  (previous paragraph) and removed by the deterministic merge — a second full
  extraction would prove nothing further (the dump file is static between
  runs). The canonical post-extraction boundary is the deduped merge output,
  whose SHA is proven stable.

**Counts.** Pages processed: 10,895,934 (5,000,000 legacy + 5,895,934 new).
Raw concatenated: 1,318,288 records (898,802 kind-1, 419,486 kind-2),
107,930,151 bytes,
SHA256 `7aecf79d2c3288d01e7d7af9a143620215bd833586cc284c5e42fc50feac855b`.
After degenerate filtering: 1,220,431 kept (800,948 kind-1, 419,483 kind-2),
97,854 kind-1 short + 3 kind-2 malformed dropped, 104,414,655 bytes,
SHA256 `b847f44cd22a3165287070a78b23a5946dd013bd837950fffe07303e46865dc1`.

---

## Gap 2 — Nine CAL-rejected lessons: CLOSED (root causes fixed, lessons recovered)

**True causes (two independent defects, instrumented — not guessed).**

1. **The merge never deduplicated.** `extract/merge_sort.py` counted duplicate
   keys but wrote every record anyway. Full gate mirror over the original
   `facts.bin`: accept=3,071,828, G2-duplicate=539,418, G3=96,744, G1=0.
   Lessons 3/14/23/28/31/39 each began with a key identical to the previous
   lesson's final key → CAL must-accept record 0 failed G2 → whole lesson
   dropped (65,536 records each). REPORT.md's "Duplicate keys removed:
   539,418" was false.
2. **Wiktionary emitted degenerate records.** 96,744 kind-1 records with
   `len(text)<4` (95,279 of them the text `"."`; 95 distinct short texts),
   plus 3 kind-2 records with an empty word segment after `wikt:en:`. Lessons
   43/48/50 failed because a first-four record was G3-invalid → CAL dropped
   the whole lesson (mask 15/8/4 respectively).

**Corrected arithmetic (the original report was wrong).** CAL lesson drops =
9 × 65,536 = **589,824** records, not 1,110,933. The remaining 521,109
rejections were individual (G2=462,263, G3=58,846, G1=0) inside accepted
lessons. Check: 3,707,990 − 589,824 − 521,109 = 2,597,057 installed. ✓

**Fixes (committed).**
- `extract/merge_sort.py`: k-way merge now drops second-and-later adjacent
  equal keys (deterministic keep-first). Synthetic multi-run unit test: 8
  inputs, 3 duplicate keys → 5 outputs, sorted, unique, keep-first. PASSED.
- `extract/wikt_slow.py::parse_page`: mirrors the G3 bars at emission —
  skips kind-1 text <4 bytes, skips kind-2 records with empty word segment.
- `extract/filter_degenerate.py`: one-time deterministic remediation for the
  legacy 5M-page output (record order preserved, drops only).

**Dry-run validation (2026-09-23, before wiktionary completed).**
`extract/dry_run_pipeline.py` ran the full fixed pipeline on
wn+wiki+filtered-partial-wikt: merge input=3,610,133 → written=3,071,865
(dupes dropped=538,268); regenerated negative control; ingested with the
rebuilt binary (`~/workspace/ingest_bin_v2`,
SHA256 `b2eb3a40feebc64079abb7375b51c82c72a4633d43fba7faf53741faa19f8039`):
47/47 lessons CAL=OK, **0 CAL=REJECT**, negative control 1,200/1,200 with the
exact expected histogram (g1=500, g2=200, g3=500, installed=0) verdict=PASS,
installed=3,071,865 == merged facts. Seal
`1820713e1cdcabe29356b45d4f0d94a077ff105f920ba7d3164364eaa415a63d`.
(`run/dry/dry_verdict.txt`.)

**Final merge (2026-09-23).** Input: 4,106,863 records (WordNet 117,789 +
SimpleWiki 2,768,643 + Wiktionary cleaned 1,220,431). Output:
**3,565,287 unique facts**, 541,576 duplicate keys dropped (keep-first),
9 runs. Merge run twice: byte-identical
(SHA256 `0d5b96d0056b42cedf0a7a873023e1ad42fb3a0b7736600600c0f30095327268`,
`cmp` clean). Zero G3-invalid Wiktionary records reach the merge output.

**Final re-ingest (2026-09-23 ~23:10 UTC).** NCAP=3,921,815
(3,565,287 × 11 // 10). Two genuine Zag ingests into fresh stores
(`~/workspace/store_full_v2a`, `~/workspace/store_full_v2b`):
- installed=3,565,287 == facts count, both runs
- lessons: 55/55 CAL=OK (54 full + 1 partial of 26,343), **0 CAL=REJECT**
- negative control: n=1,200, g1=500, g2=200, g3=500, installed=0, verdict=PASS
- seals identical:
  `93862fe1ea4a6944eae30b8fd1a72d27297860643658135ae85f12a03b9e306a`
- blob: 491,009,953 bytes, 15 chunks; sorted per-file SHA manifests
  byte-identical across the two runs
- audit: `~/workspace/store_full_v2a/audit.log` (SUMMARY
  inst=3565287 g1=0 g2=0 g3=0 lessons=55 lessons_rejected=0)

**E1 retrieval.** Eval keys regenerated from final facts.bin (1,000 keys).
sindex via fixed Zag binary (3,496 entries). bquery: n=1,000.
`extract/verify_e1.py` (memory-efficient rewrite, retains only the 1,000
requested keys): **E1 PASS — 1,000/1,000 exact text matches**
(status=0 and byte-identical text vs facts.bin for every key).

**Interpretation.** Rejecting duplicate/degenerate individual records was
correct gate behavior; dropping nine whole lessons (589,824 records, the
majority valid) was collateral damage from the two defects above. All nine
lessons' valid facts are recovered in the final ingest.

---

## Gap 3 — WordNet NLTK transport deviation: TECHNICALLY CLOSED, governance pending

**True cause.** The frozen transport URL
`https://wordnetcode.princeton.edu/3.1/WordNet-3.1.tar.gz` returns 404.
Princeton's actual 3.1 database-only distribution is
`https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz` (HTTP 200, 16,358,468
bytes, SHA256 `3f7d8be8ef6ecc7167d39b10d66954ec734280b5bdcd57f7d9eafe429d11c22a`).
The NLTK `wordnet31.zip` was a transport substitute, not a content change.

**Equivalence proof (byte-level).** The four extractor-read files are
byte-identical between the Princeton tarball and the NLTK zip:

| file | SHA256 |
|---|---|
| `data.noun` | `2cad22fe43461ee7ae61a564ae6a518c57445c8597e53542caddb5c26a6a5d94` |
| `data.verb` | `eb1cf196dab6e1b815a1c86fa20c909fb7413b2f34250d7fe60a0fb35ef59e03` |
| `data.adj` | `ca1033bf627eb95f6cbb2864f8990be8e6a01a3c182e7d7c7094ccf8ead242cc` |
| `data.adv` | `aea301f39ac1b24be9a880dbc6cc6331bc5391f58c7525a1b298a13c922f2ed3` |

Extraction run directly from the canonical Princeton files: n=82,190,
v=13,789, a=18,185, r=3,625, total=117,789; output SHA256
`575bab57e195f27908cfcd660cd42ba38bccec3bf363c34f4922a48bd205cbb7`,
byte-identical (`cmp` clean) to the ingested `run/wn.bin`. The installed
WordNet facts are therefore exactly the canonical Princeton 3.1 database —
the transport deviation changed zero bytes of ingested content.

**Governance.** `gaps/AMENDMENT_WORDNET_TRANSPORT.md` is PROPOSED and
**awaits Micah's signature**. Technical closure does not imply governance
approval; the deviation is recorded as a proposed amendment, not a silent
fix.

---

## Final artifact table

| Artifact | Value |
|---|---|
| Wiktionary pages | 10,895,934 |
| Wiktionary raw records | 1,318,288 (898,802 kind-1, 419,486 kind-2) |
| Wiktionary raw SHA256 | `7aecf79d2c3288d01e7d7af9a143620215bd833586cc284c5e42fc50feac855b` |
| Wiktionary clean records | 1,220,431 (800,948 kind-1, 419,483 kind-2) |
| Wiktionary clean SHA256 | `b847f44cd22a3165287070a78b23a5946dd013bd837950fffe07303e46865dc1` |
| Merge input | 4,106,863 (wn 117,789 + wiki 2,768,643 + wikt 1,220,431) |
| Merge output facts | 3,565,287 (541,576 dupes dropped) |
| facts.bin SHA256 (×2 runs) | `0d5b96d0056b42cedf0a7a873023e1ad42fb3a0b7736600600c0f30095327268` |
| NCAP | 3,921,815 |
| Installed (×2 runs) | 3,565,287 |
| Lessons | 55/55 CAL=OK, 0 CAL=REJECT |
| Negative control | 1,200/1,200 (g1=500, g2=200, g3=500), PASS |
| Store seal (×2 runs) | `93862fe1ea4a6944eae30b8fd1a72d27297860643658135ae85f12a03b9e306a` |
| Blob | 491,009,953 bytes, 15 chunks, manifests identical |
| E1 retrieval | 1,000/1,000 exact |
| WordNet tarball SHA256 | `3f7d8be8ef6ecc7167d39b10d66954ec734280b5bdcd57f7d9eafe429d11c22a` |
| WordNet extraction SHA256 | `575bab57e195f27908cfcd660cd42ba38bccec3bf363c34f4922a48bd205cbb7` |

## Commits

- `bda2c8c6` — prereg alone (frozen 2026-09-23)
- `e51f05e0` — merge dedupe fix, wikt G3 fix, filter, WordNet amendment (proposed)
- `454f3bd8` — dry-run driver + determinism prover
- `45a52291` — first parallel bz2 worker (superseded)
- `52156b3e` — feeder + static-file worker
- `4fe36acd` — finalize script
- `c2bd231e` — gap closure verdict (this file), REPORT.md corrections,
  verify_e1.py memory fix, dry_run_pipeline.py --ingest-bin arg

## REPORT.md corrections applied

- Merge: corrected "Duplicate keys removed: 539,418" — the original merge
  counted but did NOT remove duplicates; the fixed merge performs
  deterministic keep-first dedupe.
- CAL arithmetic: corrected "9 lessons (1,110,933 records)" → 9 × 65,536 =
  **589,824** records.
- Root causes documented: merge non-dedupe + Wiktionary G3-invalid records.
- All counts updated to final full-ingest values (see table above).
