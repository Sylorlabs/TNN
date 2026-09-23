# PROPOSED Amendment — WordNet 3.1 transport (deviation approval)

**Status:** PROPOSED — pending Micah's signature. Evidence complete 2026-09-23.
**Amends:** PREREG_INGEST1GB.md §1 (corpus: "WordNet 3.1 data files") and
REPORT.md §7.5 (transport deviation note).

## Deviation

The frozen spec's corpus table names "WordNet 3.1 data files" as the source;
the acquisition crew targeted `https://wordnetcode.princeton.edu/3.1/WordNet-3.1.tar.gz`,
which returns HTTP 404 (verified 2026-09-22 and 2026-09-23). The crew
substituted NLTK's `wordnet31.zip`
(`http://www.nltk.org/nltk_data/packages/corpora/wordnet31.zip`, 11,058,667 B,
SHA256 `2a9e7da7d0c17ad8…` per corpus manifest) without approval.

## Root cause of the naming miss

Princeton never shipped a `WordNet-3.1.tar.gz`. WordNet 3.1 was released as
**database files only**; the canonical Princeton distribution is
`https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz`
(HTTP 200, `application/x-gzip`, 16,358,468 B — verified live 2026-09-23;
SHA256 `3f7d8be8ef6ecc7167d39b10d66954ec734280b5bdcd57f7d9eafe429d11c22a`).

## Equivalence proof (2026-09-23, gap-closure crew)

1. Downloaded the canonical `wn3.1.dict.tar.gz` from `wordnetcode.princeton.edu`.
2. Byte-compared the four files the extractor reads (`data.noun`, `data.verb`,
   `data.adj`, `data.adv`) against the `wordnet31/` members of the NLTK zip:

   | file | SHA256 (both sources) | verdict |
   |---|---|---|
   | data.noun | `2cad22fe43461ee7ae61a564ae6a518c57445c8597e53542caddb5c26a6a5d94` | IDENTICAL |
   | data.verb | `eb1cf196dab6e1b815a1c86fa20c909fb7413b2f34250d7fe60a0fb35ef59e03` | IDENTICAL |
   | data.adj | `ca1033bf627eb95f6cbb2864f8990be8e6a01a3c182e7d7c7094ccf8ead242cc` | IDENTICAL |
   | data.adv | `aea301f39ac1b24be9a880dbc6cc6331bc5391f58c7525a1b298a13c922f2ed3` | IDENTICAL |

3. Re-ran the `extract/wn.py` extraction logic verbatim against the Princeton
   files → output SHA256
   `575bab57e195f27908cfcd660cd42ba38bccec3bf363c34f4922a48bd205cbb7`,
   **byte-identical** to committed `run/wn.bin` (`run/wn.sha1`), 117,789 facts
   (82,190 n / 13,789 v / 18,185 a / 3,625 r).

## Proposed ruling

The NLTK `wordnet31.zip` transport is **content-identical** to the canonical
Princeton WordNet 3.1 database distribution for every byte the pipeline reads.
No fact in `run/wn.bin` depends on the transport. Approve the substitution;
correct the canonical filename in the corpus record to `wn3.1.dict.tar.gz`.
No re-extraction required (re-extraction from the canonical source was
performed as the proof itself and reproduced the artifact bit-for-bit).

**Requested:** Micah's signature to close REPORT.md §7.5.
