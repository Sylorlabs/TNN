# 1GiB Ingest — Corpus Manifest

Frozen spec: PREREG_INGEST1GB.md. Snapshot date for Wikimedia dumps: 20260901.

## Files (as-downloaded)

| file | bytes | md5 (upstream) | md5 (local) | sha256 (local) | integrity |
|---|---|---|---|---|---|
| enwiktionary-latest-pages-articles.xml.bz2 | 1632298458 | fd033eda351cff35429f7dd3598d9ecb | fd033eda351cff35429f7dd3598d9ecb | 06acca8138eacb3e8ae9c1d6232f836e37c3bf9b6d582a86693731fe0d336c20 | md5 match; bzip2 stream verified via successful full extraction |
| simplewiki-latest-pages-articles.xml.bz2 | 356186307 | 066f0b2e8d6cf5504abf26b8b86027bb | 066f0b2e8d6cf5504abf26b8b86027bb | 6832fd106ae0e4734a349d6351709fc219ccebad5850234214a57e653f7812f8 | md5 match; bzip2 -t OK |
| wordnet31.zip | 11058667 | (n/a — NLTK transport) | d3392d6facef35433ffcef838b47cae1 | 2a9e7da7d0c17ad875e4171a4d28ae17ab6969c7d67f1cf0f59d65c66d0fdd37 | unzip -t OK |

**Total as-downloaded: 1,999,543,432 bytes (1.86 GiB) ≥ 1 GiB bar.**

## Sources

- enwiktionary: https://dumps.wikimedia.org/enwiktionary/20260901/enwiktionary-latest-pages-articles.xml.bz2
  (downloaded via 8 parallel HTTP range requests, concatenated, MD5-verified)
- simplewiki: https://dumps.wikimedia.org/simplewiki/20260901/simplewiki-latest-pages-articles.xml.bz2
- wordnet: NLTK wordnet31.zip (DEVIATION — see below)

## Deviation (frozen-source amendment required)

PREREG_INGEST1GB.md specifies `https://wordnetcode.princeton.edu/3.1/WordNet-3.1.tar.gz`.
That URL returned HTTP 404. Substituted NLTK's `wordnet31.zip`, which contains the
WordNet 3.1 database files (data.noun/verb/adj/adv, index.*, LICENSE "WordNet 3.1
Copyright 2011 by Princeton University", log.grind.3.1). Content is the WordNet 3.1
lexical database, but the transport/package differs from the frozen spec. This
substitution is NOT silently approved — it is surfaced here for prereg amendment.

## Extraction outputs (run/)

| file | source | kind | records |
|---|---|---|---|
| wn.bin | wordnet31.zip data.* | 4 (gloss) | 117,789 |
| wiki.bin | simplewiki ns=0 articles | 3 (sentence) | (running — see wiki_extract.log) |
| wikt.bin | enwiktionary ==English== | 1 (sense), 2 (inflection) | (pending wiki completion) |

Record format (all): [1B kind][2B key_len BE][4B text_len BE][key][text].
