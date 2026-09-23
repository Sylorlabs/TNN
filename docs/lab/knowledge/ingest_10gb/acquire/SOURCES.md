# Sources — 10 GiB Generalist Data Acquisition

All material below is **CC BY 4.0, CC BY-SA (version noted), or public domain**.
Non-commercial (NC) and no-derivatives (ND) licenses were excluded.

Retrieval date for all files: **2026-09-23** (UTC).

## 1. Stack Exchange data dumps (via Internet Archive)

| File | Bytes | License |
|------|-------|---------|
| math.stackexchange.com.7z | 3,629,699,855 | CC BY-SA (see note) |
| physics.stackexchange.com.7z | 729,272,818 | CC BY-SA (see note) |
| chemistry.stackexchange.com.7z | 126,167,549 | CC BY-SA (see note) |
| biology.stackexchange.com.7z | 82,571,431 | CC BY-SA (see note) |

Source: `https://archive.org/download/stackexchange/` (the Stack Exchange Creative
Commons data dump). Individual posts carry CC BY-SA 2.5, 3.0, or 4.0 depending on
contribution date; the Archive's dataset landing page refers to CC BY-SA 4.0.
The manifest records this as "CC BY-SA (version varies by contribution date)".

## 2. OpenStax textbooks (CC BY 4.0, verified from interior copyright pages)

Each PDF's interior copyright page was inspected with `pdftotext`. Only PDFs whose
interior page states "Creative Commons Attribution 4.0 International License
(CC BY 4.0)" are included. Five PDFs whose interior pages state
"CC BY-NC-SA 4.0" were **excluded** (see §6).

| File | Bytes | Interior license |
|------|-------|------------------|
| chemistry-2e.pdf | 212,710,190 | CC BY 4.0 |
| college-physics-1e.pdf | 105,350,118 | CC BY 4.0 |
| elementary-algebra-2e.pdf | 78,400,114 | CC BY 4.0 |
| intermediate-algebra-2e.pdf | 90,157,092 | CC BY 4.0 |
| introductory-statistics.pdf | 26,571,083 | CC BY 4.0 |
| microbiology.pdf | 311,123,598 | CC BY 4.0 |
| prealgebra-1e.pdf | 57,611,246 | CC BY 4.0 |

All OpenStax PDFs were retrieved via Internet Archive mirrors (openstax.org
assets were unreachable from the acquisition VM); the per-file IA URLs are in
the manifest.

Note: Biology 2e (425,358,470 bytes, CC BY 4.0) was planned but the Internet
Archive copy would not resume after a connection break (HTTP 416/empty replies
from the storage node); the ~168 MB partial was discarded and the byte gap was
covered by extending the Gutenberg selection instead (see §4).

## 3. English Wikipedia — deterministic 1/8 slice (CC BY-SA 4.0)

Snapshot: `enwiki-20260901` (1 September 2026).
Selection rule: from the multistream `pages-articles` split list, take every
eighth split by starting page-ID order (indices 0, 8, 16, …), i.e. splits
1, 9, 14, 17, 19, 22, 24, 26, 27 — 9 files, a deterministic ~1/8 slice of the
snapshot. Total: 3,825,297,664 bytes.

Source: `https://dumps.wikimedia.org/enwiki/20260901/`.

## 4. Project Gutenberg — top-ranked public-domain books

Method (deterministic):
1. Downloaded the Gutenberg RDF catalog (`gutenberg_rdf.tar.bz2`, 126,648,258 bytes,
   79,454 records; catalog metadata itself is not part of the corpus).
2. Kept the 78,593 records whose RDF rights value is exactly
   "Public domain in the USA."
3. Ranked by LoCC download count descending, ties by ebook ID ascending
   (`gutenberg_ranked.tsv`).
4. Probed the top 1,500 candidates' plain-text URLs (HEAD Content-Length);
   1,421 usable, 79 unavailable or unusable (skipped, documented in
   `gutenberg_probed.tsv`).
5. Selected the smallest top-N of usable ranked entries reaching the byte
   margin: first top-1,015 for the initial 750 MB margin, extended to top-1,334
   after ineligible OpenStax PDFs were removed, then extended to top-1,745
   (from 2,783 usable probed out of top-3,000 candidates) after Biology 2e
   proved undownloadable. Cumulative probed bytes for the 1,745: 1,512,684,151.

All 1,334 plain-text files (`gutenberg/pg<EID>.txt`) are public domain.
Per-book source URLs are in the manifest (the `https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt`
or `/files/<id>/<id>-0.txt` URL actually downloaded).

## 5. Deduplication against ingest-1GB

The ingest-1GB corpus (`tnn-lab/knowledge/ingest_1gb/corpus/`) contains
`enwiktionary-latest-pages-articles.xml.bz2` (1,632,298,458 bytes),
`simplewiki-latest-pages-articles.xml.bz2` (356,186,307 bytes), and
`wordnet31.zip` (11,058,667 bytes). None of these files — nor any byte-identical
copy of them — is present in this corpus. Verified by filename and size;
no SHA256 collisions.

## 6. Excluded material

The following were downloaded but are **not** in the corpus or manifest because
their interior copyright pages state CC BY-NC-SA 4.0 (non-commercial), which the
acquisition policy prohibits:

- openstax/algebra-and-trigonometry-2e.pdf (116,281,063 bytes)
- openstax/astronomy-2e.pdf (162,975,061 bytes)
- openstax/calculus-volume-1.pdf (46,637,858 bytes)
- openstax/calculus-volume-2.pdf (43,661,805 bytes)
- openstax/calculus-volume-3.pdf (75,066,769 bytes)

Total excluded: 444,622,556 bytes. They are quarantined in the working area and
were replaced by extending the Gutenberg selection (top-1,015 → top-1,334),
which is why the Gutenberg count exceeds the originally planned ~1,000.
