# RUNBOOK — 1GB ingest full run

Prereqs: frozen prereg, corpus manifested under `corpus/` (≥1 GiB),
`build/ingest_bin` built from `build/ingest.zag`.

## 1. Extract (Python, deterministic streaming)

`extract/extract.py` streams the three archives and emits one JSONL per
source, then `extract/to_facts.py` converts to `facts.bin` records:

```
[1B kind][2B key_len BE][4B text_len BE][key][text]
```

- kind 1: `wikt:en:{word}:{pos}:{sensenum}` ← en.wiktionary English senses
- kind 2: `wikt:en:{word}:{infl}:{n}` ← inflected-form entries (text names headword)
- kind 3: `wiki:simple:{slug}:sent{n}` ← Simple Wikipedia sentences
- kind 4: `wn:3.1:{id}` ← WordNet 3.1 synset glosses

Rules: keys ≤160B, texts ≤4096B, no NUL/control bytes in keys, texts
non-empty. Sort ALL records by key bytes (external sort), write
`run/facts.bin`. Record the extraction code version + input SHAs in
`run/EXTRACT.log`. Re-run extraction twice; require byte-identical
`facts.bin` (proves determinism, K-extraction).

## 2. Negative control

`extract/make_bad.py run/facts.bin run/bad.bin` — reads the LAST key of the
sorted stream, emits the frozen 1,200 synthetic records (200 dupes of last
key, 250 empty-text, 250 NUL-key, 250 circular, 250 no-terminal).

## 3. Ingest

```
NF=$(python3 -c "print record count of run/facts.bin")
NCAP=$(( NF * 11 / 10 ))
./build/ingest_bin ingest run/facts.bin run/bad.bin run/store $NCAP
```

Hard requirements (the binary enforces them; rc=2 = VOID):
- every lesson's 8 CAL probes dry-run correct or the lesson is dropped;
- negative control exactly g1=500/g2=200/g3=500/installed=0.

Save `run/store/` (store.dat, blob_*.dat, manifest.txt, audit.log).

## 4. Index + evaluate

```
./build/ingest_bin sindex run/store
```

- E1 retrieval: sample 1,000 installed ids (deterministic stride), `bquery`,
  require 1,000/1,000 FOUND with byte-identical texts vs facts.bin.
- E2 revision: 100 ids, `revise` with new texts, `bquery` shows new text,
  neighbors unchanged, chain re-verifies (query still works).
- E3 deletion: 100 other ids, `delete`, `bquery` shows DELETED, neighbors fine.
- E4 determinism: full rerun into `run/store2`, `sha256sum` every artifact —
  all identical.
- E5 corruption: flip one byte in a COPY of a blob chunk, confirm query of an
  affected key fails loudly (no silent wrong answer); restore.

## 5. Report

`run/REPORT.md`: source bytes (per source + total GiB), facts extracted,
installed, rejected by gate (g1/g2/g3), install rate, lessons accepted /
rejected, negative-control verdict, B/fact per tier (blob text, keys,
sparse index, audit events, S5 slots, overrides), total persistent B/fact,
S5 slot overhead separately, seal hex, eval results E1–E5.

## 6. Commit

Commit: REPORT.md, manifest.txt, audit.log, EXTRACT.log, MANIFEST.*,
STRUCTURE.md, eval scripts + outputs. NEVER commit: source archives,
facts.bin, bad.bin, store.dat, blob_*.dat, sparse.idx, ingest_bin,
.zagd caches.
