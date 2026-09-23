# Manifest — 10 GiB Generalist Data Acquisition

## Summary

| Item | Value |
|------|-------|
| Total files | 1,765 |
| Total bytes | 10,787,616,909 (10.05 GiB) |
| Target | 10,737,418,240 bytes (10 GiB) |
| Status | **PASS** — exceeds target by 50,198,669 bytes |

## Composition

| Source | Files | Bytes |
|--------|-------|-------|
| Stack Exchange dumps | 4 | 4,567,711,653 |
| OpenStax textbooks (CC BY 4.0) | 7 | 881,923,441 |
| English Wikipedia slice (enwiki-20260901) | 9 | 3,825,297,664 |
| Project Gutenberg books | 1,745 | 1,512,684,151 |

## Selection rules

- **Wikipedia**: deterministic 1/8 slice — every eighth multistream split by
  starting page ID (indices 0, 8, 16, …) from the enwiki-20260901 snapshot.
- **Gutenberg**: ranked 78,593 public-domain-USA records by download count
  (ties by ebook ID); probed top 1,500; skipped 79 unavailable; selected the
  smallest top-N (N=1,334) reaching the byte margin.
- **OpenStax**: interior copyright page verified as CC BY 4.0 for each PDF;
  five CC BY-NC-SA PDFs excluded (see SOURCES.md §6).
- **Stack Exchange**: full site dumps for Math, Physics, Chemistry, Biology.

## Deduplication

None of the ingest-1GB corpus files (enwiktionary, simplewiki, wordnet31)
are present in this corpus.

## Columns

`MANIFEST.tsv` has exactly six tab-separated columns with no header:
`filename`, `bytes`, `sha256`, `source_url`, `license`, `retrieval_date`.
All sizes and hashes were recomputed from disk; the TSV was built
programmatically, not copied from working notes.
