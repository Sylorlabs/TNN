# CORPORA.md — Track A shared corpora (round r1)

Frozen source record for the representation bake-off. The raw sources below
are workspace-only (never committed). The derived corpora are byte-identical
outputs of `build_corpora.py`; their hashes are in `corpora/r1/MANIFEST.json`.

## Raw sources (downloaded 2026-09-21)

| File | URL | Bytes | SHA-256 |
|---|---|---|---|
| `pg100.txt` | `https://www.gutenberg.org/files/100/100-0.txt` (Shakespeare, PG #100) | 5,422,721 | `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb` |
| `pg10.txt` | `https://www.gutenberg.org/files/10/10-0.txt` (KJV Bible, PG #10) | 4,436,268 | `0f1a83cbcdc1d3fae6bcc3daaa496d4fa723fcce9526e84e20df12ae33fda986` |
| `longobject.c` | `https://raw.githubusercontent.com/python/cpython/main/Objects/longobject.c` (CPython main, 2026-09-21) | 225,065 | `a7ff4647cb10290a834a37bdd74a2cc0afdf03cec667992849ce8c91e9d0c13e` |
| `sqlite3.c` | extracted from `https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip` (SQLite 3.53.4 amalgamation, 2026) | 9,515,341 | `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189` |

Notes:
- The first SQLite trunk-zip URL tried (`.../src/zip/trunk/sqlite-amalgamation.zip?uuid=trunk`)
  returned a truncated download (curl error 18) and was discarded; the versioned
  3.53.4 amalgamation above replaced it. Zip integrity verified (`unzip -t` clean);
  `sqlite3.c` ends with the standard amalgamation footer.
- Raw cache lives at `units/arms/harness/corpora/raw/` (workspace only, git-ignored).

## Derived corpora (`corpora/r1/`, from `build_corpora.py`)

| File | Derivation | Bytes | SHA-256 |
|---|---|---|---|
| `prose.bin` | `pg100.txt` verbatim | 5,422,721 | `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb` |
| `code.bin` | `sqlite3.c` verbatim | 9,515,341 | `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189` |
| `t1_prose.bin` | last 10% of `prose.bin` by byte offset (`prose[floor(len*9/10):]`) | 542,273 | `b82b4da67930aa04370a6bb431ae1e76e31060f7e009a9ab282bcaf4e41cb202` |
| `t1_code.bin` | last 10% of `code.bin` by byte offset | 951,535 | `f5dd474fdc780d487234982c6bb45bd493efff9cbac70280335e62d50ca92a3e` |
| `t2_prose.bin` | `pg10.txt` verbatim (M-5 third corpus) | 4,436,268 | `0f1a83cbcdc1d3fae6bcc3daaa496d4fa723fcce9526e84e20df12ae33fda986` |
| `t2_code.bin` | `longobject.c` verbatim (M-5 third corpus) | 225,065 | `a7ff4647cb10290a834a37bdd74a2cc0afdf03cec667992849ce8c91e9d0c13e` |
| `t3.bin` | deterministic synthetic generator, seed `0x544E4E3300000033`, 1 MiB | 1,048,576 | `c0821737c163bf0cb0cf92482f9bdb82a0c915a8b752e46c46edb6bb9d9d385f` |
| `churn_fresh.bin` | deterministic synthetic generator, seed `0x544E4E3300000043`, 448,000 bytes (7,000 × 64-byte units) | 448,000 | `3ad44a4fad84c8a83ac50c7d97a9fb9a6471aaa1f7f6ddf4121d411e0b756cf5` |
| `mem_vocab.txt` | 5,000 most frequent whitespace-delimited tokens of `prose.bin` (frequency order) | 34,411 | `de66633e562598b5085a929fbbc42479e572ad0f48c17edc9b0066da5543fe41` |
| `mem_vocab_sorted.txt` | same 5,000 tokens, byte-sorted (memorizer lookup order) | 34,411 | `d8240ea192349532ddcd75eebc24f60f477cf0a40db70d62982df4a330acd18e` |
| `MANIFEST.json` | full hashes, seeds, T1 offsets, derivation log | 1,472 | — |

T3 generator (frozen): xorshift64 seeded `0x544E4E3300000033`; per 64-byte block,
byte `j` of block `i` = `(xorshift64() >> ((j%8)*8)) & 0xFF`. Environment input,
not an AI decision. The churn generator uses the same construction with seed
`0x544E4E3300000043`.

## 10x legs

The 10x corpus is built by the committed `build_10x.py`: deterministic 10-fold
tiling of the 1x corpora (each file repeated verbatim 10×, no tags or markers);
tile hashes are recorded in `corpora/r10/MANIFEST.json`. Not yet built
(1x validation first).
