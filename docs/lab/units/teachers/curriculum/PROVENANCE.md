# PROVENANCE — Track B curriculum corpora

**Pinned corpus identities (M-30: committed before any arm is built).**
The builder aborts on any length or hash mismatch — a re-fetched corpus that
differs from these pins is rejected, never silently used.

| corpus | file | bytes | SHA-256 |
|--------|------|-------|---------|
| Shakespeare prose (Project Gutenberg #100) | pg100.txt | 5,638,480 | `3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37` |
| sqlite3.c (SQLite amalgamation 3.53.4) | sqlite3.c | 9,515,341 | `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189` |

Measured 2026-09-21 from the fetch URLs below. Both match the prereg's
"~5.4MB prose / ~9.5MB code" (§1.10).

## Source 1 — Project Gutenberg #100: The Complete Works of William Shakespeare

- **Fetch:** `fetch/fetch_gutenberg_100.sh`
  (`https://www.gutenberg.org/cache/epub/100/pg100.txt`, "The Complete Works
  of William Shakespeare" — the file's own header reads *"The Project
  Gutenberg eBook of The Complete Works of William Shakespeare"*).
- **License: public domain.** Shakespeare died in 1616; the Project Gutenberg
  edition is public domain in the United States (the file carries the Project
  Gutenberg License, which for this ebook marks it freely reusable).
- **Handling:** used byte-for-byte as served. No header stripping, no
  normalization — the Gutenberg license header is part of the corpus, by
  declaration (deterministic beats pretty).

## Source 2 — SQLite amalgamation 3.53.4: sqlite3.c

- **Fetch:** `fetch/fetch_sqlite_amalgamation.sh`
  (`https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip`; only
  `sqlite3.c` is extracted, the zip is not retained — zip entry timestamps
  are not byte-stable inputs).
- **License: public domain.** SQLite is dedicated to the public domain by its
  authors ("The author … has dedicated this code to the public domain";
  https://www.sqlite.org/copyright.html). The amalgamation header carries the
  same dedication.
- **Handling:** `sqlite3.c` used byte-for-byte as shipped. Version pin
  3.53.4 (= 3530400) is frozen — a different amalgamation version is a
  different corpus and fails the hash pin.

## Non-commit rule

Corpora are **never committed** (prereg §1.12 / task binding). Fetch scripts
are committed; corpora live in `$CORPUS_DIR` (default `/tmp/tnn-corpora`) and
are verified against the pins above at every build. The committed slice
manifests carry per-slice SHA-256s, so any corpus substitution is detectable
downstream even if the pins were somehow bypassed.
