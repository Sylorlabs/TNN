# PREREG Amendment A1 — storage basis, audit allocation, integrity contract

- **Date:** 2026-09-22
- **Amends:** `docs/lab/ops/storage-compression/PREREG.md` (frozen commit `010a3806`)
- **Status:** pre-results (definitive measurement matrix not yet landed; S1/S2/S3 smoke tests pass)

## A1.1 — Three storage bases (the 92 B figure is written/logical, not allocated)

The frozen prereg's "92 bytes/fact" baseline counts **written/logical bytes**:

| Component | Written bytes/fact |
|---|---:|
| Slot | 24 |
| Dense ID→slot index | 4 |
| One used audit entry | 64 |
| **Total written** | **92** |

The instrument **preallocates** audit capacity for `2N+8192` records as full 1 MB
chunks at init. At the 240K anchor that is 30 MB ≈ 128 B/fact of audit capacity vs
64 B/fact written. Total **allocated** ≈ 24 + 4 + 128 ≈ **156–159 B/fact**
(virtual; RSS ≈ written bytes at P=1 since untouched pages are not resident).

There is **no persistent disk tier** in the throughput instrument: all KB state is
process heap; knowledge disappears with the process. "Bytes/fact" in this
investigation therefore means, in order of measurement:

1. **Logical/written bytes/fact** (SCALE_MEM — the headline for codec comparison).
2. **Allocated virtual bytes/fact** (capacity planning; includes preallocation).
3. **RSS bytes/fact** (resident; ≈ written at P=1).
4. **Future persistent bytes/fact** (a disk format does not yet exist; any persistent
   proposal must specify its own layout — written basis is the starting point).

All scheme results must state which basis the headline uses. The 92 B baseline and
all "B/fact" scheme targets in this investigation are on the **written basis**
unless stated otherwise.

## A1.2 — Lazy/right-sized audit allocation added as a candidate (H8)

Because the written-vs-allocated gap is entirely the eager audit preallocation,
**lazy audit-chunk allocation** (allocate each 1 MB audit chunk on first use;
keep only the pointer array preallocated) is added as a preregistered candidate.
Expected effect: allocated audit 128 → ~64 B/fact at P=1 (written basis
unchanged); total allocated ~159 → ~95 B/fact. Kill bar: RSS-vs-N slope must not
regress; install slowdown ≤ 1%.

## A1.3 — Add-only vs general event semantics

The throughput instrument is **add-only**: the only ops are `op=1` (add;
rc ∈ {0 success, 1 dupe, 2 cap, 3 gate}) and `op=7` (episode marker, one per
pass). There is **no revise or delete path** in the measured instrument.

Consequences:

- Revisability/deletability are **constraints on schemes**, not measured behaviors.
  Any scheme that handles revisions/deletes (sparse overrides, tombstones) must
  demonstrate the mechanism on a synthetic workload or be scoped as
  designed-not-measured. A successful add-only codec **must not** be generalized to
  full TNN memory without a mutation/replay test covering add, revise, delete,
  and episode events.
- The audit's value copy is lossy for general i64 (`a1=(v&0x7FFFFFFF)`,
  `a2=((v>>32)&0x7FFFFFFF)` drop bits 31 and 63). Exact in-instrument (values are
  0..219066); any claim of general audit-based replay must handle full i64.

## A1.4 — Integrity contract: no per-entry hash chain in the instrument

The instrument's audit array is **append-only but not hash-chained**: source
inspection finds no per-entry cryptographic hash chain in the throughput
learner. The end-of-run FNV-1a digest over (id, recalled value) is tamper
*detection* over the slot table, not a per-entry ledger chain.

Therefore:

- The baseline must **not** be described as tamper-evident per entry.
- Any audit-compression scheme that reduces or restructures the ledger must carry
  **structural kill bars**, not just KB-CORRECT: (i) demonstrated tamper
  detection (flip a bit in each structure; verification must fail); (ii) replay
  from the compressed form must reproduce the semantic audit stream
  byte-identically vs a reference logger on a mixed workload (dupes, failures,
  multi-pass episodes). "Preserved by construction" is not an acceptable bar —
  the audit is write-only in the instrument, so the digest and flaw battery
  cannot see it.
- If a scheme introduces a real hash chain (e.g. per-chunk SHA-256), its timed
  cost must be included in the install measurement.

## A1.5 — Known baseline defect: audit cap silently drops records at P=3

`audit_cap = cap*2 + 8192`. Passes 2–3 re-teach the same ids → N dupe-failure
records (`rc=1`) per extra pass → 3N+3 entries at P=3, exceeding the cap for all
N > 8189. `sc_audit_append` then returns 1 and the caller **silently drops the
record**. The "append-only ledger" is not append-only under the instrument's own
legal configs (`npass ≤ 3`). Anchor runs use P=1 and are unaffected. Any
persistent-ledger proposal must fix this (e.g. growable capacity); the defect is
documented here so no scheme inherits it silently.

## A1.6 — Consultant hypotheses incorporated

Three consultants were dispatched (Sol via gpt-5.6-sol, Grok-4.6, native Muse).
The native Muse hypotheses (H1–H10, `evidence/HYPOTHESES_MUSE.md`) are
incorporated as preregistered candidates:

- **H1** audit-as-derivation + per-chunk hash chain (audit 64 → ~0.01 B/fact).
- **H3** chunk-homogeneous tagged-width values (value 8 → ~1.6 B/fact).
- **H5** identity index for dense-sequential ids (index 4 → 0 B/fact). **Implemented as S3.**
- **H8** lazy audit allocation (see A1.2).
- H2/H4/H6/H7/H9/H10 as specified in the hypotheses doc, including the
  expected-negative controls (H4/H6/H9).

H5's scope: valid iff id assignment is dense-sequential (a theorem of the
instrument's add path: ids 0..N−1 taught in order, slots append in add order).
Designs for sparse/external ids must use the documented fallback (dense, or hash
past the ~3.2× sparsity crossover) — scope the claim, don't overclaim.

## A1.7 — Schemes implemented pre-amendment (smoke-tested, not yet measured)

- **S1** = FL1 (slot id removed, 24→20 B) + FL2 (compact 24 B audit records).
  48 B/fact written. Smoke: 96/96 flaws, digest `44a61309cf780de1` (matches base).
- **S2** = S1 + FL3 (sparse lifecycle/strength: 12 B slot with override table) +
  FL4 (per-chunk clock base + i16 delta). 40 B/fact written. Smoke: 96/96,
  digest matches base. Override path implemented; battery exercises the
  zero-override path (override-heavy workloads need a follow-up measurement).
- **S3** = S2 + H5 (identity index; dense index deleted). 36 B/fact written.
  Smoke: 96/96, digest matches base.

All three keep facts explicit, countable, individually addressable, revisable,
and deletable; zero RNG; pure Zag.
