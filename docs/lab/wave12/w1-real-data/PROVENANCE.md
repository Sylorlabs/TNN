# W1 Data Provenance (frozen pre-build, 2026-09-20)

Every dataset used by workstream 1, with source, license, acquisition, and
verification. Corpora are fetched on demand into a local data dir and are
NEVER committed to the repo. The harness verifies the slice hashes
in-harness (prereg K5).

## D1 — natural-language prose

- **Corpus:** Project Gutenberg ebook #100, *The Complete Works of William
  Shakespeare* by William Shakespeare.
- **Source URL:** https://www.gutenberg.org/files/100/100-0.txt
- **License:** Public domain (US). Project Gutenberg license header in the
  file states the ebook is free of copyright in the United States.
- **Acquired:** 2026-09-20 via `curl -sSL` (no login, no key).
- **Distributed size:** 5,422,721 bytes.
- **W1 slice:** bytes [0, 262144) of the distributed file, carved with
  `head -c 262144` → `w1_prose_256k.txt` (262,144 bytes = 4096 × 64-byte
  chunks).
- **Slice sha256:**
  `1b98db74118aa7d86894d90c581ef066e4375ea00876aae2570721fc9464eee2`

## D2 — production source code

- **Corpus:** SQLite 3.53.4 amalgamation, `sqlite3.c` (the entire SQLite
  database engine as a single C file — real production code of the kind
  that appears in LLM code corpora).
- **Source URL:** https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip
  (official SQLite download page: https://www.sqlite.org/download.html)
- **License:** Public domain. SQLite's copyright page
  (https://www.sqlite.org/copyright.html): all SQLite code is dedicated to
  the public domain, no restrictions on use, modification, or distribution.
- **Acquired:** 2026-09-20 via `curl -sSL` (no login, no key).
- **Integrity:** `sqlite3.c` (9,515,341 bytes) sha256 =
  `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`,
  byte-identical to the independently documented hash for this release
  (gwf/x2c package PROFILE for sqlite 3.53.4, verified 2026-09-09).
- **W1 slice:** bytes [0, 131072) of `sqlite3.c`, carved with
  `head -c 131072` → `w1_code_128k.c` (131,072 bytes = 2048 × 64-byte
  chunks).
- **Slice sha256:**
  `ff73e4e03caa24768b76bcedfa18a14b25ed46c68fd415decfc618ec3fe57873`

## Reproduction

```bash
mkdir -p /tmp/w1data && cd /tmp/w1data
curl -sSL --max-time 120 -o shakespeare.txt "https://www.gutenberg.org/files/100/100-0.txt"
curl -sSL --max-time 120 -o sqlite.zip "https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip"
unzip -o -j sqlite.zip "sqlite-amalgamation-3530400/sqlite3.c"
head -c 262144 shakespeare.txt > w1_prose_256k.txt
head -c 131072 sqlite3.c > w1_code_128k.c
sha256sum w1_prose_256k.txt w1_code_128k.c
# expect:
# 1b98db74118aa7d86894d90c581ef066e4375ea00876aae2570721fc9464eee2  w1_prose_256k.txt
# ff73e4e03caa24768b76bcedfa18a14b25ed46c68fd415decfc618ec3fe57873  w1_code_128k.c
```

## Considered and rejected

- **WikiText-2 (raw):** the standard small LM benchmark (CC BY-SA 3.0 /
  GFDL, Salesforce Research). Rejected as the primary corpus because the
  official S3 endpoint (`research.metamind.io.s3.amazonaws.com`) refused
  connections from this environment and the available mirror could not be
  fetched reliably; Gutenberg #100 is larger, public domain, and equally
  "real language of the kind real systems train on."
- **TinyStories (roneneldan):** rejected on provenance — downstream
  redistributors report conflicting licenses (CC-BY-4.0 vs CDLA-Sharing-1.0)
  and the dataset-card license field could not be confirmed from the fetched
  page text. A corpus with ambiguous licensing is not used.
- **The Stack / StarcoderData / CodeSearchNet:** real LLM code corpora but
  gated or multi-GB; infeasible and unnecessary for this slice. The SQLite
  amalgamation is real production C, public domain, and byte-verified.

## License compliance note

Both corpora are public domain — no attribution or share-alike obligations
attach to the slices. Nothing is redistributed in the repo (slices live in
the local data dir; only the hashes are committed).
