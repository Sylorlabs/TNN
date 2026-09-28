# PREREG — 1GB INGESTION RUN (frozen 2026-09-22)

Micah's order: "lets try a run ingesting at least a gigabyte of data, lets try
all of english and basics." Storage is no longer the blocker (S5 adopted:
5.53 B/fact slot overhead).

## §1 Corpus — "all of english and basics" (concrete)

| Source | Content | Role |
|---|---|---|
| en.wiktionary pages-articles XML dump | English entries: headword, POS, senses/definitions, inflections | "all of english": vocabulary + definitions + lexical grammar |
| simple.wikipedia pages-articles XML dump | Articles in simple English | "basics": basic world knowledge |
| WordNet 3.1 data files | Synsets, glosses, lexical relations | structured lexical knowledge |

Total as-downloaded bytes MUST be ≥ 1 GiB (1073741824). The corpus crew
(`knowledge/ingest_1gb/corpus/`) downloads, SHA256-hashes, and commits
`MANIFEST.tsv` + `MANIFEST.md` + `STRUCTURE.md` BEFORE any ingestion.
Ingestion of a source whose manifest entry is not committed is forbidden.

Grammar/syntax note: lexical grammar (POS, inflections, verb frames) comes
from wiktionary/wordnet entries. Standalone syntax-rule knowledge is OUT OF
SCOPE for this run (documented gap, not a claim).

## §2 Fact model (canonical)

Fact = one binary record:
```
[1B kind][2B key_len BE][4B text_len BE][key bytes][text bytes]
```
- kind: 1=dict (wiktionary sense: key=`wikt:en:{word}:{pos}:{n}`, text=definition)
- kind: 2=infl (wiktionary inflection: key=`wikt:en:{word}:infl:{form}`, text=gloss/tags)
- kind: 3=wiki (simplewiki sentence: key=`sw:{title}:{n}`, text=sentence)
- kind: 4=wn (wordnet: key=`wn:{synset}:{word}`, text=gloss)
- Keys are unique by construction per kind (sense#/sent# included).

Extraction (Python glue, audited, deterministic): stream-parse XML dumps in
document order, emit records. The extractor does NO judgment, NO dedup beyond
what §3 states — it is a mechanical parser like NORMALIZE.md. Its determinism
is proven by byte-identical re-extraction.

Sort (Python glue, deterministic external merge sort, Python 3.12): records
sorted by (key bytes) before ingest. Rationale: makes the Zag dupe check O(1)
memory (adjacent comparison) while remaining a REAL check executing in the
learning path on the real stream. Sort is a mechanical transform, documented
and byte-identical across runs.

## §3 The learning path — judgment gate (pure Zag, zero RNG)

Every fact passes the gate in `ingest.zag`. Gate checks, per fact:
- **G1 WELLFORMED**: kind in 1..4; 1 ≤ key_len ≤ 160; 1 ≤ text_len ≤ 4096;
  no NUL bytes; no bytes < 0x20 except 0x0A in text; key has no 0x0A.
- **G2 DUPE**: key byte-equal to previously installed fact's key
  (adjacent in sorted stream; full key compare) → reject DUPE.
- **G3 CONSISTENCY** (kind-specific, mechanical):
  - dict: text not byte-equal to word part of key (circular); text_len ≥ 4.
  - infl: text names the headword (contains word bytes); text_len ≥ 4.
  - wiki: text ends in [.?!]; text_len ≥ 10.
  - wn: text_len ≥ 4.
- **G4 CALIBRATION** (per lesson = 65536-fact batch): 8 frozen CAL probes
  (4 must-accept genuine records, 4 must-reject: empty text, dupe of lesson's
  fact 0, NUL-in-key, circular dict). Verdicts derived dry-run (never
  installed) via the same gate fns. Lesson installs facts ONLY if 8/8 CALs
  correct; else lesson REJECTED, cause logged, run continues.

Deliberate install (gate pass → evidence → eliminative verify → add):
the S5 decision core ported identically (see §4). Successful adds are
derivable from slots (no per-add audit, S4 H1); failures, episodes,
revisions, deletions → 16-word event log.

**Negative control**: one synthetic lesson of 1000 bad facts (250 each of
the 4 must-reject shapes) is injected mid-run. Require 1000/1000 rejected
with correct reasons; ANY install → run VOID.

**Truthfulness scope**: installation = faithful capture of the source, NOT
truth endorsement. Wiki sentences are single-source claims; every record
carries its kind/source byte. (Aligns with web-crawl SUSPECT tier.)

## §4 Storage — S5 as default, text blob tier

- **Slot tier**: S5 store ported IDENTICALLY from
  `ops/storage-compression/src/s5_learner.zag` (decision core + width
  compaction + chain + event log). Slot[i] = u64 blob offset of fact i.
  Meta flags per slot: bit0 = deleted (tombstone), bit1 = revised
  (override active). Port equivalence proven by textual diff of ported
  functions + behavioral test (100k numeric facts through both, slot bytes
  compared).
- **Blob tier** (new, required: S5 slots hold i64, not text): append-only
  records (§2 layout), chunk files `blob_XXXX.dat` ≤ 64 MiB each.
- **Revision**: append new record (same key); sparse override table
  (S2-style: id → new blob offset); set revised flag; audit event.
  Old record orphaned (append-only blob, unreachable).
- **Deletion**: set tombstone flag; audit event. Record stays in blob
  (append-only) but unreachable.
- **Retrieval index**: post-ingest deterministic pass emits (key, id)
  pairs → sorted → `index.dat`; query = binary search (pure Zag).
- **Disk format**: `INGEST_DISK_FORMAT.md` (this prereg's companion):
  blob chunks + slot chunks + meta + index + audit log + report JSON.
  The S5 instrument was process-heap-only; this run defines the
  persistent layout. No wall-clock in artifacts (logical clock only).

S5-adoption coordination: this store IS the S5 scheme (ported, equivalence
proven). If/when the canonical S5-adoption interface lands, conform to it;
until then this is the reference implementation. No semantic divergence
permitted (proven by §4 port-equivalence test).

## §5 Scale, chunking, determinism

- znc 2^25 slice limit: blob reads in ≤32 MiB slices; slot chunks are
  4096-entry S5 chunks (already compliant); sort is external merge.
- Zero RNG in the decision path (certifier gate).
- Byte-identical rerun: ingest twice; SHA256 of every artifact
  (blob chunks, slot files, index, audit log) must match. Run logs may
  differ (timings); artifacts must not.

## §6 Evaluation (frozen)

- **E1 retrieval battery**: deterministic sample of 1000 installed facts
  (every (N/1000)th fact + boundary facts: first/last of each kind);
  query each key → byte-exact text match vs source record. Bar: ≥99.5%
  exact match; EVERY miss gets a written autopsy.
- **E2 revision proof**: 100 deterministic facts revised (text → marked
  corrected variant); verify query returns new text, audit shows 100
  revision events, 1000 neighbors unaffected.
- **E3 deletion proof**: 100 deterministic facts deleted; verify query
  returns NOT-FOUND, audit shows 100 delete events, neighbors unaffected.
- **E4 B/fact**: (blob bytes + slot bytes + index bytes + audit bytes) /
  installed facts, on the written basis (A1.1). Report slot overhead
  separately (expect ≈ 8–9 B: width-4 offsets + meta). Bar: slot
  overhead ≤ 12 B/fact.
- **E5 install accounting**: installed count, rejected count by reason
  (G1/G2/G3/CAL/negative-control), install rate (facts/s).

## §7 Kill bars

- K1: manifest ≥1 GiB, SHAs committed before ingestion. FAIL → no run.
- K2: zero installs bypassing the gate (code inspection + CAL evidence).
- K3: negative control 1000/1000 rejected. FAIL → run VOID.
- K4: byte-identical rerun (all artifact SHAs match). FAIL → no claim.
- K5: E1 ≥ 99.5% with autopsy of every miss.
- K6: E2 + E3 all verified (100/100 revisions, 100/100 deletions).
- K7: slot overhead ≤ 12 B/fact on written basis.
- K8: zero RNG (certifier); pure-Zag decision path.

## §8 What this run does NOT claim

- That installed wiki sentences are true (faithful capture only).
- That TNN understands the ingested English (retrieval ≠ comprehension;
  comprehension probes are a separate trial).
- Syntax-rule knowledge (documented gap, §1).
