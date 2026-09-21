# Y5 — Cross-stream span sets

**Family:** STRUCT
**Mechanism:** One ID over a non-contiguous span set; kills cascade atomically via LINK with eliminative justification.

## 1. What Y5 is

Y5 stores knowledge as **spans** — fixed 256-byte slices of a corpus — and consolidates
related spans into **LINK units**. A LINK is a single ID that names an ordered,
non-contiguous set of spans (2–8 spans per LINK in this implementation). Recalling the
ID replays the spans in order, reconstructing content that was never stored contiguously.

The eliminative core: a LINK survives only while every member span verifies against the
corpus. If any member's bytes change (a defect), the whole LINK is revised or killed as
one atomic unit — never half-killed. A kill that left a live span pointing at a dead
LINK would break atomicity and kill the implementation (binding kill, clause 2).

## 2. Storage layout

- **Serials, not pointers.** Every unit (span or LINK) gets a dense serial number.
  Rows are 40-byte fixed records: offset, length, corpus, flags, span-list pointer
  (LINKs), forward pointer (absorbed members → their LINK), ID remap (swap probe),
  defect kind/shift (revision), resolution cache.
- **Span pool.** LINK member lists live in a flat pool: 12 bytes per member
  (corpus, corpus-relative offset, length), ordered by (corpus, offset).
- **Corpus-relative offsets.** All span offsets are relative to their corpus base,
  verified against corpus length (not the concatenated arena). Cross-corpus spans
  cannot alias.
- **Live queue.** FIFO insertion order for oldest-unpinned eviction.
- **Audit ledger.** 64-byte append-only entries: op, slot, return code, before/after
  bytes, args, stage, two data words. Every mutation (ingest, link, kill, pin,
  weaken, evict, defect) appends exactly one entry.
- **Allocation trace.** Every `nio_alloc`/`nio_free` logs `A <size>` / `F <size>`
  lines; the M8 gate compares these byte-for-byte across perturbations.

## 3. Operations

- **Ingest.** A span is identified by (corpus, grid index). If a live unit already
  covers that span, the existing serial is returned (dedup hit — one ID per span).
  If the span was absorbed into a live LINK, the member serial is returned and
  recall resolves through the LINK. If the member's LINK is dead, a fresh serial is
  allocated — tombstoned members are never revived.
- **LINK formation (consolidation).** Live, unconsidered spans are grouped by first
  content token; runs of 2–8 same-group spans in corpus order become one LINK
  (budget: 2,048 LINKs per pass). Members are tombstoned (forward pointer → LINK,
  never reused). PIN/WEAKEN flags inherit to the LINK. One audit entry per LINK.
- **Recall.** The serial resolves through absorption (member → LINK) and then
  through the ID remap layer; bytes are streamed span-by-span from the corpus
  buffer. Byte-exact or it fails loudly.
- **Kill.** Killing any span of a LINK kills the whole span set with **one** audit
  entry (OP_KILL on the LINK; members were already tombstoned at formation).
  Atomicity invariant: no live non-LINK span may have a forward target that is dead.
  Checked by `y_audit_atomicity` after every revision episode.
- **Revise (defect).** A defect marks a span's bytes changed (kind + shift). The
  owning LINK is re-verified span-by-span; failing members are excised with
  eliminative justification recorded in the ledger. If >20% of LINKs on sqlite3.c
  degrade to single spans under the revision curriculum, the binding kill fires.
- **Pin / weaken / evict.** Pin is an audited flag that exempts a unit from
  oldest-unpinned eviction. Weaken is a management annotation (flag + audit entry)
  that never changes stored bytes. Eviction removes the oldest unpinned live unit;
  killing a LINK's member is impossible (members are already dead) — the LINK dies
  whole.

## 4. Determinism

Zero RNG in any decision path. Grouping is by content token (deterministic),
eviction is FIFO (deterministic), tie-breaks are by serial (deterministic).
Two runs of any mode produce byte-identical stdout and byte-identical M8
artifacts (SHA-256 verified by the external gate — any differing byte is
DISQUALIFIED, not killed).

## 5. Binding kill (authoritative)

> ">20% of Y5 units on sqlite3.c degrade to single spans within the revision
> curriculum (links die faster than they pay); OR any kill leaves a live span
> pointing at a dead LINK (atomicity broken — kill the implementation)."

Measured: `m4_link_degradation_tenths` (LINKs lost during revision ÷ LINKs before)
and `m4_atomicity_violations` (live non-LINK spans with dead forward targets)
on the `m4-1x-code` leg (sqlite3.c). Both are zero at 1x.

## 6. Provisional design choices (logged per the ambiguity rule)

- 256-byte span segmentation; first-content-token grouping; LINKs of 2–8 spans;
  2,048-LINK budget per pass; absorbed members tombstoned, never reused;
  FIFO oldest-unpinned eviction; weaken as an audited flag that never alters bytes.
- M1 ID-swap probe: PROVISIONAL-PENDING-FREEZE (A15). Implemented as 64 live-unit
  probes (T→U remap, byte-verified, restored).
- M7 cache rig: provisional A7/A8 schedule (C, C, C′ edited every-100th-unit,
  5,000 `(l*37)%n` lookups). Reported as ID-arm fields, not slot-cache fields.
- M8 follows the B-64 combined-instance reading (A17): one store runs the M1
  ingest/probe plus the M3 churn sequence per perturbation.
