# INGEST_DISK_FORMAT.md — 1GB English ingest persistent format

Frozen with the ingest binary. All integers little-endian unless noted.
All files deterministic: two runs over the same fact stream produce
byte-identical artifacts (proven by rerun SHA comparison).

## facts.bin (input, built by the extraction pipeline)

Record stream, no header:

```
[1B kind][2B key_len BE][4B text_len BE][key bytes][text bytes]
```

- kind: 1=dict sense, 2=inflection, 3=Simple Wikipedia sentence, 4=WordNet gloss.
- Records sorted by key bytes (unsigned lexicographic). The G2 duplicate
  gate assumes sorted input.
- key_len ≤ 160, text_len ≤ 4096.

## bad.bin (input, negative control)

Same record format. Frozen composition: 200 wellformed duplicates of the
last real-stream key (expect G2), 250 empty-text (G1), 250 NUL-in-key (G1),
250 circular dict definitions (G3), 250 sentences without terminal
punctuation (G3). The run is VOID unless the histogram is exactly
g1=500, g2=200, g3=500, installed=0.

## blob_NNNNNN.dat (fact text tier)

Each file exactly 33,488,896 bytes (32 MiB − 64 KiB, under the znc 2^25
slice limit). Records never straddle chunks; the tail of each chunk is
zero-padded. Global offset → chunk = off / 33488896, in-chunk = off % 33488896.

Blob record:

```
[1B kind][4B id LE][2B key_len BE][4B text_len LE][key][text]
```

id = the fact's S5 slot number. Revisions append a NEW record with the same
id; the override table points at the newest.

## store.dat (S5 slot tier + audit)

```
[8B magic "IGNST001"][4B cap][4B n][4B nsealed][4B nchunks][4B clock]
[widths: nchunks bytes]                       // wtag per chunk
per sealed chunk c: [4B len][len bytes]       // compact slot chunk
[chain: nsealed*32 bytes]                     // sha256 chain over chunks
[4B events_n][events: events_n*16 bytes]      // 16-word audit events
[32B seal]                                    // sha256(last_chain || events)
[8B blob_total][4B blob_nchunk][8B blob_recs]
```

Slot chunk layout (S5, ported): 4096 slots × (w value bytes + 4 meta bytes).
Meta: clock_delta i16, flags u8, spare u8. flags bit0 = deleted (tombstone),
bit1 = revised (newer record in blob via overrides.dat). The S5 chain covers
values+meta; revise/delete recompute the chain and re-seal (events tag 9/10
record the operation).

## sparse.idx (retrieval index)

```
[4B count][entries...]
entry: [2B key_len BE][8B blob_offset LE][key bytes]
```

One entry per 1024th fact (id % 1024 == 0), built by streaming the blob once.
Lookup: binary search for the greatest entry key ≤ query key, then linear
blob scan forward. Query consults flags (tombstone) and overrides.dat.

## overrides.dat

```
[4B count][count × ([4B id LE][8B blob_offset LE])]
```

Revision pointers. Grows only; a second revise of the same id replaces its
entry in place.

## manifest.txt / audit.log

manifest.txt: key=value lines (n, nsealed, clock, blob_total, blob_chunks,
blob_recs, g1, g2, g3, lessons, lessons_rejected, negcontrol, seal hex).

audit.log: deterministic lines — INGEST-START, one LESSON line per 65,536
records (CAL verdict, installs, reject histogram), NEGCONTROL line (exact
histogram + PASS/FAIL), SEAL line, SUMMARY line.
