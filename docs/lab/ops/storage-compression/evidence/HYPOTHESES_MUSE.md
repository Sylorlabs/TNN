# Storage-compression hypotheses — native Muse consultant

- **Author:** Muse (native consultant; developed from first principles — no outside models consulted)
- **Date:** 2026-09-22
- **Prereg:** frozen commit `010a3806`, branch `tnn-native-lab`
- **Basis:** independent code inspection of `ops/throughput/thru_learner.zag` (1238 lines) plus
  `ops/storage-compression/PREREG.md`. All structural claims below were verified against the
  code, not inherited from the FL1–FL4 writeup. Hypotheses only — no implementation.

## §0. What code inspection established (ground facts)

1. **Ids are dense-sequential in the instrument.** `sc_run_pass` teaches store ids `0..n-1` in
   order; `sc_add` appends slot `s.*.n` per successful add. Therefore in every measured run
   **index[id] ≡ id exactly** (no dupes: ids unique; `learn_gate=1`; `n < cap`).
2. **The only read path is id → index → slot → value@16.** Verified by grep: slot fields
   id@0, lifecycle@4, strength@8, clock@12 are *never read anywhere*; `sc_recall` reads only
   `o+16`. The 96-probe flaw battery and the FNV-1a digest use `sc_recall` only.
3. **The audit is write-only.** `sc_audit_chunk` is called only from `sc_audit_append`; nothing
   reads the ledger back. No behavioral test can distinguish a compressed audit from a deleted
   one — audit schemes need *structural* kill bars (demonstrated tamper detection + replay).
4. **Only two op codes exist:** `op=1` (add; rc ∈ {0 success, 1 dupe, 2 cap, 3 gate}) and
   `op=7` (episode; one per pass, `slot=-1`, only `stage` varies). There is **no revise or
   delete path** in the instrument — revisability/deletability are constraints on schemes,
   not measured behaviors.
5. **Values are small non-negative ints.** `sc_fact_truth`/`sc_supplied` produce values in
   `[0, 219066]` (max is category-16 word count; every other category ≤ 2 bytes, most ≤ 1).
   All instrument values fit in 18 bits.
6. **Anchor runs use P=1** (per THROUGHPUT_REPORT.md): audit entries per run = N (op=1/rc=0)
   + 1 (op=7). `SCALE_MEM` reports *written* bytes: `(ops_audit*64)/n ≈ 64`.

## §1. Corrections to the FL1–FL4 analysis (overstatements / errors found)

- **C1 — 92 B (and FL's 36 B) count *written* bytes, not allocated.** `sc_store_init`
  preallocates the full audit capacity up front: `ceil((2N+8192)/16384)` × 1 MB chunks.
  At the 240K anchor that is 30 MB ≈ **128 B/fact allocated for audit** vs 64 written, i.e.
  total *allocated* ≈ 24.4 (slots) + 4.0 (index) + 130.2 (audit) ≈ **159 B/fact**, not 92.
  Nuance (verified reasoning, not measured): untouched `malloc` pages are not RSS-resident,
  so at P=1 RSS ≈ written bytes ≈ 92 B/fact; the 2× over-allocation costs *virtual* size
  (plus page-fault time on first touch and OOM risk under virtual-memory limits). Any scheme
  must state which basis its headline uses; the prereg's RSS-vs-N slope (§4) measures ~92
  at P=1, ~159 virtual. FL's 36 B target is on the written basis.
- **C2 — The audit cap is simultaneously over- AND under-provisioned.** At P=1 it is 2×
  over-allocated (N+1 entries used of 2N+8192). But `npass ≤ 3` is legal, and passes 2–3
  re-teach the same ids → N dupe-failure records (`rc=1`) per extra pass → 3N+3 entries at
  P=3, which exceeds the 2N+8192 cap for every N > 8189. `sc_audit_append` then returns 1
  and the caller **silently drops the record**. The "append-only ledger" is not append-only
  under the instrument's own legal configs. (Anchor P=1 runs are unaffected.)
- **C3 — FL2's "preserves every information bit" does not generalize.** True of the record
  as stored, but the record's value copy is already lossy:
  `a1=(v&0x7FFFFFFF)`, `a2=((v>>32)&0x7FFFFFFF)` drop bits 31 and 63. Audit-based replay of
  a general i64 (negatives, |v| ≥ 2³¹) returns corrupted values. Exact in-instrument (values
  are 0..219066); false in general. Also FL2's 20 B is not minimal: `(op,slot,id,v_lo,v_hi)`
  keeps a redundant coordinate — `(tag,id,value)` = 13 B suffices given the index, or
  `(tag,slot,value)` = 13 B given slot.id. FL2 keeps both id *and* slot.
- **C4 — FL4 understates.** Clock is not merely per-pass constant: per §0.2 it is *write-only*,
  and per H1 it is *derivable* (clock(slot) = number of episodes before its add). Clock needs
  **zero stored bytes even multi-pass**, not 4 B/chunk.
- **C5 — FL3's sparse-override idea is untestable here.** No revise path exists (§0.4), so the
  "store only deviations" override branch can never fire in the instrument. Any revision
  behavior must be demonstrated on a synthetic workload or scoped as designed-not-measured.
- **C6 — Audit schemes are behaviorally untestable in this instrument** (§0.3). KB-CORRECT's
  digest and the flaw battery cannot see the audit. "Preserved by construction" is not an
  acceptable bar; each audit hypothesis below carries a demonstrate-it kill bar (tamper
  detection + replay byte-identity on a mixed workload with dupes/failures/episodes).

---

## §2. Hypotheses

### H1 — Cross-structure minimal information: the audit as derivation + event markers

**Mechanism sketch.** The slot table, dense index, and audit are three views of one event
stream. Minimal information to rebuild all three:
- *Slot table* (primary): per slot — value; id (iff ids not inferable, cf. H5); deviations
  of lifecycle/strength from defaults (cf. H7); clock is **derivable** (episodes-before-add),
  store nothing.
- *Index*: derivable by scanning slot ids — it is a cache, not information. Marginal cost 0
  (rebuilt in O(N), or eliminated outright by H5).
- *Audit*: every `op=1/rc=0` record is derivable from the slot table — slot position *is*
  the add-order counter (k-th successful add ↔ slot k); id from slot.id/index; value from
  slot; `rc`/`b2`/`stage` are constants. **Marginal new information per successful add: 0
  bytes.** What the audit must still carry: (a) tamper-evidence, (b) non-derivable events —
  episodes (P/run) and failure records (rc ∈ {1,2,3}, rare; these create no slot).

  Scheme: delete per-add audit records. Tamper-evidence becomes a **per-chunk hash chain**:
  when a 4096-slot chunk seals, append `H(prev_chain ‖ chunk_bytes)` (32 B per 4096 facts).
  Non-derivable events go to a compact event log: `(1 B tag, 4 B add-counter position,
  4 B payload)` ≈ 9 B per episode/failure. Replay: walk slots 0..N−1 emitting the semantic
  `op=1` records, interleaving event-log entries at their add-counter positions — reproduces
  the full audit stream (op,slot,rc,id,value per entry); the chain verifies integrity.
  Tamper *localization* degrades from per-entry to per-chunk — stated tradeoff.

**Expected bytes/fact:** audit 64 → ~0.01 (32 B/4096 amortized chain + ~0 event bytes at P=1
with zero failures). Combined with H3+H5: total ≈ **2 B/fact**.

**Speed impact:** install — replaces 64 B × 16 stores per add with nothing; per chunk one
SHA-256 over 96 KB (~30–60 µs per 4096 adds ≈ 0.01 µs/fact amortized). The 6.2 µs install is
dominated by the teach/verify path (untouched), so expect install ≈ flat (±5%), possibly a
hair faster (less memory traffic: 256 KB audit writes/chunk eliminated). Recall: untouched.

**Kill bar:** (i) byte-identical recall digest + 96/96 flaws; (ii) *demonstrated* tamper
detection — flip one bit in a slot chunk and, separately, one bit in the event log; the
chain MUST fail verification in both cases (argued ≠ demonstrated); (iii) replay from
(slots + events + chain) reproduces the semantic audit stream byte-identically vs a
reference logger on a mixed workload containing dupes, cap/gate failures, and P=3 episodes;
(iv) install slowdown ≤ 10%. **DEAD** if any tamper goes undetected or replay diverges.

### H2 — Episode run-length encoding

**Mechanism sketch.** `op=7` records are `(7,-1,0,0×12,stage=pass,0,0)` — 64 B each, P per
run, only `stage` varies (= pass number = clock after increment). Replace with a single
event-log entry per run: `(tag=7, first_clock, count)` = 12 B **total**. (Premise correction:
episodes are per-*pass*, not per-fact; the cap's "2×" is headroom, not one-episode-per-fact.
At the P=1 anchor this saves 64 B → 12 B total ≈ 0.0002 B/fact — negligible there, but it
removes the only per-run audit term and matters as P grows. Fully subsumed by H1's event
log; listed separately only because it was asked.)

**Expected bytes/fact:** 64×P B/run → 12 B/run (≈ 0 B/fact).

**Speed impact:** unmeasurable (fewer writes, no read path).

**Kill bar:** replay must reproduce all P episode records with correct stages; H1's clock
derivation must still hold. **DEAD** if P=3 replay diverges.

### H3 — Chunk-homogeneous tagged-width values

**Mechanism sketch.** All instrument values fit in 18 bits (§0.5). Store one width tag per
4096-slot chunk in a side array (nchunks bytes ≈ 0.0002 B/fact); slots hold values at the
chunk's width ∈ {1,2,4,8}. Chunk width = max width needed, decided by **in-place compaction
at chunk seal**: track max width during fill, `memmove` down on seal (amortized O(1)/fact,
deterministic). Recall: load width (one extra, highly predictable load), read
i8/i16/i32/i64 + zero/sign-extend; tag encodes signedness for the general case (instrument
values are non-negative; sign handling must be proven on a synthetic negative workload —
the instrument cannot test it). At the anchor (C=24, m=10000 ≥ 4096) chunks are
category-pure: most 1 B, c14/c17/c18/c19 chunks 2 B, c16 chunks 4 B → weighted ≈ 1.6 B/fact.

**Expected bytes/fact:** value 8 → ~1.6 avg. Slot (with FL1/FL3/FL4, H1-clock) = value only
≈ **1.6 B/fact** (vs 24).

**Speed impact:** install +1 width-classify per add (few compares) + amortized compaction —
expect ≤ 2% overhead. Recall +1 load + small switch — expect ≤ 5% slowdown (KB-WIN allows
10%).

**Kill bar:** byte-identical digest; sign/zero-extension proven correct on synthetic
negatives (|v| ≥ 2³¹, negative i64); recall slowdown ≤ 10%; slot bytes ≤ 2.5/fact at anchor.
**DEAD** if sign-extension is wrong on negatives or slowdown > 10%.

### H4 — Hash index vs dense: the crossover (analysis — do not implement for the instrument)

**Mechanism sketch / analysis.** Dense index costs 4·(id_span/N) B/fact. A deterministic
open-addressing hash (FNV-1a probe sequence — zero RNG, fully deterministic) costs
(4 B key + 4 B slot + 1 B state)/α per entry ≈ 12.9 B/fact at α=0.7. Crossover:
4·(id_span/N) = 12.9 → **id_span/N ≈ 3.2**. Below ~3.2× id-space sparsity dense wins; above,
hash wins. Instrument: id_span/N = 1 → dense wins 3×, and hash probes (~1.4 avg at α=0.7)
are slower than dense's single load. **Hash index is dead on arrival for the instrument.**
It is the designated scheme only if TNN ever uses sparse/external ids (e.g. content-hash
ids): switch at *measured* sparsity > 4×. Deletion needs tombstones (probe degradation
bounded); the instrument has no deletes, so that path would be designed-not-measured.

**Expected bytes/fact:** n/a (negative result by analysis for the instrument).

**Speed impact:** n/a.

**Kill bar:** implement ONLY on a synthetic sparse-id variant (id_span/N ∈ {4,16,64});
**DEAD** unless measured bytes/fact < dense AND probe slowdown ≤ 15% at α=0.7.

### H5 — Identity index for dense-sequential ids (strongest single hypothesis)

**Mechanism sketch.** By §0.1, index[id] ≡ id is a *theorem* of the instrument's add path,
not a cache: ids are assigned 0..N−1 in order and slots append in add order. Replace the
4 B × N dense index **and** its byte-at-a-time 0xFF init pass with a bounds check
(`id < n ? id : absent`). Addressability preserved: the id *is* the slot. Generalizes to
any workload where TNN assigns dense sequential ids — which TNN controls (sequence
numbers, not content hashes). Deletes: 1-bit/slot tombstone bitmap (0.125 B/fact);
identity still holds (dead slots keep their numbers). Revisions never move slots. New facts
append. Fallback for external/sparse ids: dense (H4 says when to hash instead) — scope the
claim, don't overclaim.

**Expected bytes/fact:** index 4 → **0**.

**Speed impact:** install FASTER (no index write per add; no 4·cap byte-stores at init).
Recall FASTER (one fewer dependent load — skips the index chunk fetch; with H10, recall
becomes a single base+offset load).

**Kill bar:** byte-identical digest; flaw family C (never-taught id n+7 → absent via bounds
check) must pass; recall must not slow down (expect speedup); install ≤ baseline.
**DEAD** if any in-scope workload uses non-sequential ids without the documented fallback —
i.e. valid iff id assignment is dense-sequential; the fallback must exist in the design.

### H6 — Dictionary / interned value encoding

**Mechanism sketch.** Value-domain cardinality is small: categories c≥16 take ≤ 10 distinct
values (text-level, t = i%10); c<16 take ≤ ~10²–10⁴ (word-lengths ≤ 20, hash%97 ≤ 97,
freq ≤ 14537). Total distinct ≈ low thousands. Store a dictionary (8 B × D ≈ 32 KB fixed)
+ per-slot code (2 B covers 65 536). Codes assigned deterministically (first-seen order);
lookup via small deterministic hash map value→code, amortized O(1). Recall: code → dict
(dict resident in L1, ~1–2 ns). This is the i64 analog of prereg family (b): interned
*string refs* are exactly the "wide but few" case.

**Expected bytes/fact:** 8 → 2 + 32 KB/N (≈ 0.13 at 240K) ≈ **2.1** — comparable to H3's
~1.6 here, with worse constants and an extra indirection. Crossover: H6 beats H3 iff values
are WIDE (8 B: large ints, string refs) AND low-cardinality — for 8 B values with
D ≤ 65536: 8 vs 2.1, H6 wins 3.8×.

**Speed impact:** install +dict lookup per add (amortized O(1)); recall +1 L1 dict lookup.

**Kill bar:** on the frozen instrument must BEAT H3's measured slot bytes/fact — predicted
NOT to (2.1 > 1.6): **expected dead here**, surviving as the designated scheme for
wide-value workloads (string-ref facts, family (b)) where H3 cannot compress. An honest
negative result on the instrument is the deliverable.

### H7 — Sparse-override columns (FL3/FL4 made revision-robust)

**Mechanism sketch.** Per-chunk header stores
(default_strength, default_lifecycle, default_clock) = 12 B/chunk ≈ 0.003 B/fact;
per-slot overrides live in a small sorted side table of (slot, field_id, value) records,
appended on revise (binary search on read; latest-wins by append order, deterministic).
Empty in the instrument (no revises) → steady-state cost ≈ 0.003 B/fact vs 12 B inline.
Read path: one branch on empty table, else default. This is FL3/FL4 as *designed
mechanisms* rather than instrument constants — it answers C5.

**Expected bytes/fact:** 12 → **~0.003** steady-state.

**Speed impact:** recall +1 predictable branch; revise = O(log K) search + append.

**Kill bar:** (i) digest/flaws unchanged on the instrument; (ii) on a SYNTHETIC revise
workload (the instrument cannot produce one), override reads keep recall slowdown ≤ 10% at
1% revise rate and install+revise stay amortized O(1); (iii) revise-then-recall returns the
revised value — demonstrated, since the instrument can't check it. **DEAD** if the override
path can't be demonstrated correct or costs > 10%.

### H8 — Lazy audit-chunk allocation (allocation-policy free lunch)

**Mechanism sketch.** `sc_store_init` preallocates all `ceil((2N+8192)/16384)` 1 MB audit
chunks up front (30 MB virtual at the anchor — the entire written-vs-allocated gap, C1).
Allocate each audit chunk on first use (boundary crossing in `sc_audit_append`); keep the
`aptrs` array preallocated (8 B per 16384 entries ≈ 0.0005 B/fact). Amortized O(1),
deterministic. Optionally grow `aptrs` by doubling past 2N+8192 — fixes C2's silent drop
at P=3 deterministically.

**Expected bytes/fact:** allocated audit 128 → 64.0003 at P=1 (written basis unchanged);
total allocated 159 → ~95 B/fact virtual. (Per C1's nuance: at P=1 this saves *virtual*
size + page-fault time, not RSS — RSS ≈ written bytes already. The win is real under
virtual-memory pressure and for any run that would otherwise touch spare chunks.)

**Speed impact:** +1 predictable branch per append; init much faster (no 30 MB reservation
walk). Expect install ±1%.

**Kill bar:** RSS-vs-N slope must not regress; init wall-time improves or holds; install
slowdown ≤ 1%. **DEAD** if the lazy path slows appends > 1%.

### H9 — Grouped bit-packing toward the information floor (expected-dead bound)

**Mechanism sketch / analysis.** Information floor for the instrument's values: c0–c15 need
~4–11 bits, c16 needs 18 → entropy-weighted ≈ 9–10 bits ≈ **1.2 B/fact**. H3's width
quantization reaches ~1.6 B. The remaining ~0.4 B is closable only by sub-byte packing:
groups of G=4 consecutive values at minimal bit-width + per-group (bits, base) header;
recall = group lookup + shift/mask (~2–3 ns extra, pure word arithmetic in Zag).

**Expected bytes/fact:** ~1.2–1.3 slot vs H3's 1.6 — saves ~0.35 B/fact ≈ 0.4% of baseline.

**Speed impact:** small recall penalty, significant complexity.

**Kill bar:** must beat H3 by ≥ 10% on slot bytes AND hold recall ≤ 10% slowdown.
**PREDICTED DEAD** on magnitude (cannot move the headline ≥ 20% for KB-WIN) and
complexity risk. Included to bound the space: the floor is ~1.2 B/fact for values; H3
captures ~75% of the available gain at ~5% of the complexity.

### H10 — Single-arena chunk layout (kill the pointer tables)

**Mechanism sketch.** Replace per-chunk `sc_alloc`s + pointer arrays
(`chunk_ptrs`/`idx_ptrs`/`audit_ptrs`: 8 B per chunk ≈ 0.005 B/fact) with ONE arena per
structure (slot arena = nchunks × 98304 in a single alloc; 5.78 MB < 2²⁵ ✓ at anchor;
audit arena 30 MB < 33.5 MB ✓ — at 1M facts audit needs multiple arenas or H1).
Recall becomes `base + (slot/4096)·chunk_bytes + (slot%4096)·slot_bytes` — arithmetic
replaces TWO dependent pointer-chase loads (`ptrs[g]` → `chunk[o]`). Better locality,
fewer TLB entries, 3 allocs instead of ~149, simpler free.

**Expected bytes/fact:** ~0.005 saved (noise) — the win is speed, not space.

**Speed impact:** expect recall +3–8% (dependent-load removal matters most at large N,
where the 1–3.2M probes/s variance already shows cache effects); install slightly faster.

**Kill bar:** recall must not slow down (expect speedup); digest identical; must respect
the 2²⁵ slice limit (arena-chunking where needed). **DEAD** if measured recall doesn't
improve-or-hold.

---

## §3. Combined projection & tradeoff table

| Component | Baseline (written) | FL1–FL4 (written) | H-combined (written) |
|---|---|---|---|
| Slot | 24 | 12 | ~1.6 (H3 tagged value; id/lifecycle/strength/clock removed) |
| Index | 4 | 4 | 0 (H5 identity) |
| Audit | 64 | 20 | ~0.01 (H1 chain + events; H2 episodes) |
| **Total** | **92** | **36** | **~1.7 B/fact** |

H-combined ≈ 98% below baseline, ≈ 21× below FL1–FL4's 36 B. Allocated basis converges to
the written basis (H8 removes the virtual overhang). Speed: install ≈ flat (6.2 µs is
dominated by the untouched teach/verify path — memory-traffic savings are real but small
against it); recall flat-to-faster (H5+H10 remove two dependent loads per probe; H3 adds
one predictable load+switch). All schemes keep facts explicit, countable, individually
addressable (id→slot), revisable (H7), deletable (H5 tombstones), deterministic,
byte-identical, pure Zag, one unified brain. H4/H6/H9 are included as *expected-negative*
controls: H4 dead by analysis at instrument sparsity, H6 predicted to lose to H3 here
(alive only for wide-value/string-ref workloads), H9 predicted dead on magnitude.

**Strongest single hypothesis: H5 (identity index).** The instrument's ids are
dense-sequential and slots append in id order, so index[id]≡id is a theorem of the code
path, not a cache — deleting the 4 B index is free, removes the 0xFF init pass, and
removes a dependent load from every recall. Certainty ≈ 1, cost < 0.
