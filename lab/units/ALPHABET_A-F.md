# TNN Representation Program — Brainstorm Crew 1
## Unit-of-Knowledge Alphabet: Arms A–F (+ variants)

**Status: PROPOSED — frozen arms and kill bars below await Micah's signature before any build.**
**Program bet (thesis):** LLM tokens are a fixed discretization built for matrix math. TNN's units must be COGNITIVE: chunking is an act TNN performs on the raw stream itself (no fixed tokenizer — humans aren't born with one either), vocabulary is taught/learned like a child learns words, and a chunk is a byte span with a stable ID that memory points back to, retrieves, and reuses (caching territory).

**Scope note:** this catalog covers *segmentation and identity* — how the stream becomes addressable units. It does not cover what a unit *means* (that's the teachers/vocabulary track, see `TEACHERS.md` from the sibling crew). The two tracks meet at Arm D: a chunk ID is the handle a taught meaning hangs off.

---

## 0. Shared protocol (all arms, no exceptions)

**Determinism contract (law, not a metric).** Every arm is a pure function of (corpus bytes, complete logged internal state). No RNG, no wall-clock, no pointer-keyed maps, no float nondeterminism — all scoring is integer arithmetic. Arrays only; every iteration order is index order. **Global tie-break (total order):** lower start offset wins; then longer span; then lower candidate sequence number. Any arm that cannot reproduce byte-identical chunk tables and memory contents on rerun FAILS the battery regardless of scores — this is reported as a law violation, not a low score.

**Audit compatibility.** All arms log to the same append-only ledger (16-word entries: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60). New chunk-vocabulary op codes (proposed, frozen at build):
`CUT_PROPOSE=0xC0, CUT_COMMIT=0xC1, CUT_REFUSE=0xC2, CUT_ROLLBACK=0xC3, CUT_SPLIT=0xC4, CUT_MERGE=0xC5, CUT_KILL=0xC6, CHUNK_REUSE=0xC7, SPAN_OBSERVE=0xC8`.
Memory ops keep their existing codes; a memory entry that references chunks carries chunk IDs in its b-fields.

**Span identity.** Never `==` on slices (Zag slice equality is not content identity). Spans are identified by `(corpus_id, start, end)` integer triples, or by chunk ID. Content hashing is FNV-1a 64-bit in pure Zag (no native imports, no dependency on the R33 SHA shim).

**Stable ID scheme (arms with IDs).** Chunk IDs are `u32`, monotonically increasing from a single counter, **never reused**. Killed chunks are tombstoned (`state=dead`); dangling references are impossible by construction, and the audit trail shows exactly when an ID died and why.

**Corpora & probes.** Shakespeare prose (~5.4MB) and sqlite3.c (~9.5MB), already pipelined. Byte-exact recall probes of 64 bytes (precedent). Curriculum at 1x, then 10x. Fixed memory budget per arm (proposed: 1MB entries + table cap, identical across arms — frozen at sign-off).

**Shared metrics.**
- **M1** byte-exact recall: fraction of 64-byte probes recalled byte-exact.
- **M2** stored bytes: memory entries + chunk table (audit reported separately as instrumentation cost).
- **M3** mean reuse: references per chunk (copies/coords arms score 1.0 by construction).
- **M4** dedup ratio: unique span bytes ÷ stored bytes.
- **M5** revision churn: (killed + revised) ÷ committed.
- **M6** law check: byte-identical rerun (boolean; violation = FAIL).

---

## Arm A — Raw bytes, no chunking (CONTROL)

### (1) Mechanism sketch
No segmentation, no vocabulary, no IDs. A memory entry is a coordinate triple: `{corpus_id: u8, start: u32, len: u32}`. Byte-exact recall re-reads `corpus[start .. start+len)` — no copy is stored (the corpora are static buffers, so coordinates are stable). There is no chunk table and no chunk ops; the audit ledger sees only standard memory ops (`MEM_ADD` with b1=start, b2=len, b3=corpus_id). Retrieval is a linear scan over entries comparing integer triples — O(n) per lookup, no content comparison needed for identity.

Organs involved: (1) deliberate memory substrate only — add/kill/pin/promote/demote/strengthen/weaken operate on coordinate entries. Organs (2)–(5) have nothing to chew on: no hypotheses about units, nothing to consolidate, no traces to compose, no structure to revise. That absence is the point of the control.

Propose/commit/revise/kill lifecycle: not applicable — there are no boundaries to propose. Entries are added by whatever upstream process wants to remember a span, killed/demoted by judgment as usual.

### (2) Falsifiable predictions
- **P-A1 (strength):** A achieves M1 = 1.0 on byte-exact recall trivially whenever the entry exists — coordinate recall cannot corrupt content. *Fails if* any recall error is ever traced to the addressing layer.
- **P-A2 (weakness):** A's M3 (reuse) is exactly 1.0 and its M4 (dedup) is exactly 1.0 by construction — two entries covering overlapping spans share nothing and the system cannot know they overlap without a content scan. *Fails if* any cross-entry sharing is observed (it can't be — that's the prediction).
- **P-A3 (weakness):** On the 10x curriculum, A's M2 (stored bytes) grows linearly with entries and exceeds B-64's by ≥3x at equal M1, because every repeated span is re-registered with fresh coordinates. *Fails if* A's stored bytes stay within 1.5x of B-64's.
- **P-A4 (corpus split):** A shows no corpus-differentiated behavior — its metrics on Shakespeare vs sqlite3.c differ only by entry count, never by structure. Any "smart" arm must beat A *differently* on the two corpora to prove it learned something corpus-specific.

### (3) Falsification / retirement criterion
A is a control, not a contender: it is **retired** (dropped from future batteries) if B-64 strictly dominates it on M1, M2, and retrieval-op count on both corpora at 10x — at that point "no segmentation" is proven pure cost. Conversely, **if A ties-or-beats every lettered arm on M2 at equal M1, the smart arms die, not A** — that result would mean segmentation itself is unjustified overhead, and the whole representation program reverts to coordinates.

### (4) Buildability note
Trivially pure-Zag. Data structures: one array of `{corpus_id: u8, start: u32, len: u32, strength: u8, state: u8}`. No chunk table, no new op codes, no hashing. Hazards: none. Retrieval scan is O(n) integer compares — slow at scale but correct and deterministic; a production version would want an index, which is itself a segmentation-like structure, and that irony is documented, not fixed, in this arm.

---

## Arm B — Fixed-size chunks (CONTROL, three sizes: B-8, B-16, B-64)

### (1) Mechanism sketch
The stream is tiled into aligned fixed-size blocks: chunk `k` covers bytes `[k*S, (k+1)*S)` for S ∈ {8, 16, 64}. Chunk ID *is* the index — `id = start >> log2(S)` — so no chunk table needs to exist for addressing; the mapping is a pure arithmetic function, deterministic by construction. A memory entry references a list of chunk IDs covering its span (a 64-byte probe = eight B-8 IDs, four B-16, one B-64). An optional stats array indexed by ID holds `{use_count: u32}` for M3 reporting only — it drives no decisions.

Organs: (1) memory substrate holds ID lists; (4) symbolic recall resolves ID → byte range arithmetically and composes traces. Organs (2), (3), (5) idle — boundaries are imposed, never hypothesized or revised. Audit: memory ops carry chunk IDs in b-fields; no CUT_* ops are ever emitted. There is no propose/commit lifecycle: every block boundary is committed by fiat at time zero.

### (2) Falsifiable predictions
- **P-B1 (strength):** All three sizes achieve byte-identical reruns trivially and emit zero CUT_* audit entries — the cheapest possible segmentation. *Fails if* any addressing error occurs (impossible by construction; the prediction is a sanity anchor).
- **P-B2 (weakness):** Fixed grids cut mid-word and mid-identifier, so M3 (reuse) stays near 1.0–1.3 on both corpora: a repeated word landing at different alignments produces different chunk-ID sequences and is never recognized as the same unit. *Fails if* any B size scores M3 ≥ 2.0 on either corpus.
- **P-B3 (granularity):** B-64 dominates B-8 on M2 (fewer IDs per entry) but B-8 dominates B-64 on M1 partial-span recall — we predict a strict tradeoff with no size winning both, on both corpora. *Fails if* one size wins both metrics on both corpora (then the other sizes retire early).
- **P-B4 (corpus split):** The B-8/B-16/B-64 ranking is identical on Shakespeare and sqlite3.c — fixed grids cannot adapt, so corpus character must not change the ordering. *Fails if* the ranking flips between corpora (that would indicate a corpus interaction we don't understand).

### (3) Falsification / retirement criterion
Controls: a B size is **retired** from future batteries when another B size strictly dominates it on M1, M2, and M3 on both corpora (battery hygiene — keep the cheapest surviving grid as the "dumb baseline"). B as a family is **killed as a contender** (it was never one) the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1 — at that point fixed grids have served their purpose and the question is only *which* smart arm wins.

### (4) Buildability note
Pure Zag, nearly trivial. No chunk table (ID = index arithmetic). Optional stats: one `[]u32` of length `corpus_len / S` — for sqlite3.c at S=8 that's ~1.2M entries = 4.7MB, fine in one slice (under 2^25). Memory entries hold small ID lists; cap list length (a probe ≤ 64 bytes → ≤ 8 IDs for B-8) so entries are fixed-size structs. Hazards: none. This is the arm you build first to validate the harness, the audit plumbing, and the probe protocol before any smart arm exists.

---

## Arm C — Delimiter chunks (CONTROL, two variants: C-W, C-P)

- **C-W:** boundaries at whitespace/newline transitions (space, `\t`, `\n`, `\r`).
- **C-P:** C-W plus punctuation (`.,;:!?()[]{}"'` and friends — frozen byte set at sign-off).

### (1) Mechanism sketch
One deterministic scan pass builds the chunk table: maximal runs of non-delimiter bytes become chunks; maximal delimiter runs become their own chunks (so reconstruction is lossless — every byte belongs to exactly one chunk). Chunk record: `{id: u32 (monotonic), start: u32, end: u32, state: u8 (always committed), use_count: u32, strength: u8, src_ep: u32 (scan episode), just: u8 = 0 (imposed)}`. IDs assigned in stream order. Memory entries reference chunk-ID lists exactly as in Arm B; (4) symbolic recall resolves ID → `(start, end)` via table lookup (integer compare on ID — never slice `==`).

Organs: (1) holds the table and ID-referencing entries; (4) resolves and composes. (2)/(3)/(5) idle — boundaries are imposed by the delimiter set, which is frozen before the run and never revised mid-run. No propose/commit lifecycle; the scan *is* the commit, logged as a run of `CUT_COMMIT` entries (or one bulk `SCAN_COMMIT` — frozen at sign-off; per-cut entries are simpler to audit and we propose per-cut).

### (2) Falsifiable predictions
- **P-C1 (strength):** On Shakespeare, C-W's chunks approximate words, so we predict M3 ≥ 3.0 (common words recur across many entries) and M2 ≤ 0.5× B-64's at equal M1. *Fails if* C-W's reuse is within 1.5x of B-64's on prose — then even word-shaped chunks buy nothing.
- **P-C2 (weakness):** On sqlite3.c, C-P fragments identifiers and operators (`sqlite3_prepare_v2(` → many tiny chunks), so we predict C-P's chunk count ≥ 4× C-W's on code and its M3 < C-W's M3 on code — the "smarter" delimiter set is *worse* on code. *Fails if* C-P beats C-W on M3 on sqlite3.c.
- **P-C3 (weakness):** Neither variant revises: a boundary the scan got wrong (e.g., splitting `don't` or `e-mail`) is wrong forever — M5 churn is exactly 0. *Fails if* churn > 0 (impossible by construction; anchors the "no revision" property D must beat).
- **P-C4 (the bar for smart arms):** Any smart arm that merely rediscovers delimiter boundaries must still beat C-W on M2/M3 to justify its machinery — we predict D does (via dedup of sub-word repeats like `the`, `ing`, `sqlite3_`) and F does not on prose. *Fails as a prediction about D/F individually, not about C.*

### (3) Falsification / retirement criterion
Controls: C-W and C-P persist for the full battery (they're the "dumb-smart" baselines). A variant **retires** from future batteries if a smart arm beats it by ≥2x on M3 *and* on M2 at equal M1 on both corpora — it has then been strictly superseded as a baseline. **If no smart arm beats C-W on Shakespeare by end of 10x, every smart arm is killed** — the program's complexity is unjustified for prose, and the code-corpus results decide whether anything survives at all.

### (4) Buildability note
Pure Zag, straightforward. Delimiter set: a 256-entry `u8` table (1 = delimiter). One scan pass, O(n). Chunk table: variable-length records in one array; worst case every byte alternates delimiter/non-delimiter → ~2.7M chunks on Shakespeare × 24B = 65MB — **exceeds the 2^25 single-slice indexing limit**, so shard the table (e.g., 4 shards, shard = id >> 20, index = id & mask — deterministic arithmetic, no hashing). Alias shard slices to locals before indexing (large-struct-array gotcha). Per-cut `CUT_COMMIT` audit entries: b1=start, b2=end, b3=len, d1=FNV-1a(span), d2=just code 0. Hazards: none beyond sharding, which is mechanical.

---

## Arm D — Self-cut byte span + stable ID (MICAH'S HYPOTHESIS — the flagship)

Three variants: **D** (pure self-cut), **D-T** (curriculum-taught seed vocabulary), **D-R** (reuse-gated commit).

### (1) Mechanism sketch

**The cutting decision, in TNN-native terms.** A cut is a *hypothesis about the world* — "this byte span is a unit" — and it travels the full organ pipeline:

1. **Proposal — organ (2) eliminative hypothesis logic, fed by organ (1) observation.** The memory substrate watches the stream through a bounded candidate window. At each position it maintains candidate spans = suffixes of the last W bytes (W=256 proposed, frozen at sign-off) with lengths 2..LMAX (LMAX=64). Each candidate accumulates deterministic evidence in a fixed-size open-addressed table (4096 slots, linear probing, insertion sequence numbers; eviction = lowest count, tie → oldest sequence — total order, no randomness):
   - `rep`: verbatim occurrence count (integer).
   - `contdiv`: distinct continuation bytes across occurrences (256-bit bitset = 4×u64 per candidate — deterministic OR-accumulation).
   - `reuse`: memory entries already referencing this span's coordinates.
   
   A candidate is **proposed** when `rep ≥ REP_BAR` AND `len ≥ MIN_LEN` (3) AND `contdiv ≥ 2` (the span is followed by *different* bytes in different occurrences — it is a unit with variable context, i.e., word-like — not a fixed larger string's prefix). The `contdiv ≥ 2` bar is the eliminative step: candidates that are always followed by the same byte are eliminated as mere prefixes of something bigger. Proposal emits `CUT_PROPOSE` (slot=provisional ID from the monotonic counter, state=proposed; b1=start, b2=end, b3=len, b4=rep, b5=contdiv; d1=FNV-1a(span), d2=just code 1/2).
   
   This is infant statistical learning made deterministic: transitional-probability dips become integer `contdiv` counts, and there is no sampling anywhere.

2. **Commit — organ (3) deliberate consolidation/promotion.** Promotion of a proposed chunk to committed **is vocabulary acquisition** — the exact analogue of a child learning a word. The reasoning-control gate (`inspect → propose → commit/refuse`) applies: consolidation commits only if the chunk passes a verification probe (byte-exact recall of the span through the new ID + a reuse forecast of ≥1 expected reference). Refusals are logged (`CUT_REFUSE`) — a refused hypothesis is data, not silence. Commit emits `CUT_COMMIT`; the chunk record becomes `{id, start, end, state=committed, use_count=0, strength=judgment-set (initial: unset/neutral), src_ep, just}`.

3. **Use — organs (1) + (4).** Memory entries hold **chunk-ID lists, never byte copies** — the ID is the cache handle. Retrieval resolves ID → span by table lookup (integer ID compare). Hot chunks get `pin`ned; cold chunks get `demote`d (committed→proposed: vocabulary decay *without* deletion — the ID and its history survive); dead chunks get `kill`ed (tombstone; ID never reused). `strengthen`/`weaken` are judgment-set by TNN, never derived from `use_count` — the count is evidence for judgment, not a formula input. Every reference emits `CHUNK_REUSE` (slot=chunk_id, b1=mem_slot, b2=new use_count). **Force-pin is human/trainer-only**, audited and visible — e.g., a trainer can force-pin curriculum vocabulary; TNN cannot force-pin anything itself.

4. **Revision — organ (5) native structural revision.** Wrong cuts are revised, not patched over: `CUT_SPLIT` (parent → two children at a cut offset, children get fresh IDs, parent tombstoned) and `CUT_MERGE` (two adjacent chunks → one new ID, parents tombstoned). Both go through the same propose/commit/refuse/rollback gate. Post-commit verification runs the recall probe; failure → `CUT_ROLLBACK`, chunk returns to proposed. Revision is how the vocabulary *learns its own mistakes* — M5 churn measures it.

**D-T (taught seed):** the curriculum (trainer) pre-commits a seed vocabulary — e.g., the 500 most frequent C-W chunks on the training split — via `CUT_COMMIT` with just code 3 (trainer-taught), optionally force-pinned (human-only, audited). The self-cut organ then runs as in D: it may propose overlapping spans, and revision may split/merge taught chunks. Tests whether teaching accelerates or interferes.

**D-R (reuse-gated commit):** proposals are automatic as in D, but commit requires `reuse ≥ REUSE_BAR` (proposed, e.g., 2 — a second independent memory entry must reference the span's coordinates before the ID is minted). Stricter "cache territory" semantics: no ID exists until the span has proven worth caching. Tests whether commit latency costs more than premature-commit churn saves.

### (2) Falsifiable predictions
- **P-D1 (strength — the thesis bet):** D's M2 (stored bytes) ≤ 0.6× B-64's at equal M1 on Shakespeare at 10x, driven by M3 ≥ 4.0 — stable IDs turn repetition into references instead of copies. *Fails if* D's M2 ≥ B-64's on either corpus: the flagship's complexity buys nothing.
- **P-D2 (strength — corpus adaptation):** D's chunk-length distribution differs significantly between corpora (shorter, denser chunks on code; word-shaped on prose) *without any corpus-specific parameter* — same bars, different learned vocabulary. *Fails if* the distributions are statistically indistinguishable: D is not adapting, it's just cutting.
- **P-D3 (weakness — cold start):** Before the 1x horizon completes, D underperforms C-W on M2/M3 — proposals cost audit entries and table slots before any reuse pays back. We predict D crosses C-W between 1x and 3x. *Fails if* D never crosses C-W by end of 10x (then the cold start is actually a permanent deficit).
- **P-D4 (weakness — churn risk):** Early committed chunks get revised: we predict M5 ∈ [0.1, 0.3] at 10x — non-trivial but bounded. *Fails high* (>0.3: the vocabulary never stabilizes — see kill criterion) *or fails low* (<0.05 with M3 < 2.0: the revision organ is asleep and bad cuts fossilize).
- **P-DT1 (D-T):** D-T reaches D's 3x-horizon M3 by the 1x horizon (teaching accelerates). *Fails if* D-T's taught chunks suffer ≥50% revision/kill by the self-cut organ — teaching that the system itself overwrites is interference, not acceleration.
- **P-DR1 (D-R):** D-R's final vocabulary is ≤ 0.7× D's size with M3 ≥ D's (gating keeps only proven units). *Fails if* >50% of D-R's eventual vocabulary is still uncommitted at end of 10x — the gate is pure delay.

### (3) Falsification criterion — **any one kills the variant**
- **D is KILLED if:** (i) M2-per-recall ≥ B-64's on both corpora at 10x (complexity buys nothing); **or** (ii) M5 > 0.30 at 10x — over 30% of its own committed vocabulary killed/revised by its own revision organ means the unit hypothesis never stabilizes; **or** (iii) M1 < B-64's M1 at equal memory budget (worse *and* bigger). If D dies, the program thesis dies with it — see verdict below.
- **D-T is KILLED if:** ≥50% of taught seed chunks are revised/killed by end of curriculum AND untaught D matches D-T on M1/M2/M3 — teaching adds nothing measurable.
- **D-R is KILLED if:** commit latency strands >50% of its final vocabulary uncommitted at 10x while D commits and wins on M3 — gating is pure delay.

### (4) Buildability note
Pure-Zag buildable — this is the most machinery, but none of it needs anything Zag lacks. Data structures:
- **Chunk table:** array of 24-byte records `{id:u32, start:u32, end:u32, state:u8, just:u8, strength:u8, _pad:u8, use_count:u32, src_ep:u32}` — shard past 2^25 bytes exactly as in Arm C (shard = id >> 20). Tombstones stay in place (state=dead); IDs never reused.
- **Candidate table:** 4096 slots × (hash u64 + start u32 + len u8 + rep u32 + contdiv 4×u64 + seq u32) ≈ 4096 × 56B ≈ 224KB — one slice, trivially fine. Open addressing with linear probing; eviction scans for min (count, seq) — O(4096) worst case per position is too slow for 9.5MB (39B ops); instead maintain eviction lazily: only evict on insert-when-full, and cap inserts (only spans with rep ≥ 2 enter the table — first repeat observed via the rolling hash). Rolling FNV-1a over lengths 2..64 per position is 63 hashes × 9.5M positions ≈ 600M hash steps — fine in native Zag, no allocation.
- **Audit entries per cut:** `CUT_PROPOSE`/`CUT_COMMIT` as specified in §0; `CUT_SPLIT`: slot=parent_id, b1=child1_id, b2=child2_id, b3=split_offset, d2=reason; `CUT_MERGE`: slot=new_id, b1=left_id, b2=right_id; `CUT_KILL`: slot=id, d2=kill-reason code; `CHUNK_REUSE`: slot=chunk_id, b1=mem_slot, b2=use_count.
- **Reasoning-control gate:** the existing inspect/propose/commit/refuse/rollback path — cuts are just another committable change; post-commit verification = byte-exact recall probe through the new ID, failure → `CUT_ROLLBACK`.
- **Zag hazards:** (a) never compare spans with `==` — all candidate matching is on `(hash, start, len)` integers, with FNV-1a collisions resolved by byte loop `memcmp`, not slice equality; (b) alias the chunk-table shard to a local before indexing; (c) the candidate bitset OR-accumulation must be order-independent (it is — OR commutes — so rerun determinism holds regardless of observation order subtleties); (d) eviction tie-breaks follow the global total order — document the exact comparator in the prereg, because this is the subtlest byte-identical-rerun risk in the arm; (e) corpus buffers (5.4MB/9.5MB) each fit in one slice under 2^25 — no chunking needed for the corpora themselves.
- **D-T extra:** seed list is trainer-supplied data, loaded as a frozen array of `(start, end)` pairs; force-pins logged with trainer identity. **D-R extra:** a pending-proposal table keyed by `(start, end)` counting independent referencing entries; commit fires when the count hits REUSE_BAR.

---

## Arm E — Ephemeral chunk, no persistent ID ("just a chunk")

### (1) Mechanism sketch
Segmentation exists **transiently, per episode, in a scratch window** — e.g., the current input buffer is scanned into temporary spans for processing (whatever boundaries the episode's task needs), and then the segmentation is discarded. Nothing stable is stored: the memory substrate holds **byte copies, not references**. A memory entry is `{start:u32, end:u32, bytes: owned copy}` — the coordinates are provenance metadata; the bytes are the payload. Two entries covering the same span are two independent copies that the system cannot know are identical without a content scan (which it never performs — there is no ID space to resolve through).

Organs: (1) stores copies; (4) composes traces by copying bytes together (concatenation allocates). (2) may hypothesize about spans but its hypotheses evaporate with the scratch window — nothing is consolidatable because there is no identity to consolidate *onto*. (3) promotes entries, not units. (5) has no structure to revise. No `CUT_*` ops are ever emitted (nothing persists to commit); the audit sees `MEM_ADD` with b-fields carrying `len` and `d1=FNV-1a(bytes)`.

This arm is the *reductio*: it grants the skeptic everything — "fine, segment all you want, just don't store the segmentation" — and measures what references were buying.

### (2) Falsifiable predictions
- **P-E1 (weakness — predicted fatal):** M4 (dedup ratio) is exactly 1.0 always, and M2 ≥ 2× B-64's at equal M1 on both corpora by 10x — copies scale with entries, references would have scaled with vocabulary. *Fails if* E's M2 stays within 1.5× of B-64's (then copies are somehow cheap enough that references don't matter).
- **P-E2 (weakness):** M3 = 1.0 by construction — reuse is unrepresentable. Any probe requiring "the third occurrence of span X" forces a full content re-scan; we predict retrieval-op counts ≥ 10× D's at 10x. *Fails if* within 3× (then reference resolution isn't the bottleneck we claim).
- **P-E3 (strength — the only one):** E's M1 is trivially 1.0 whenever the entry exists, and its implementation is the simplest of all smart arms — no table, no IDs, no revision. It is the cheapest arm to *build*, the most expensive to *run*. *Fails if* any recall corruption is traced to the copy path.
- **P-E4:** E's metrics are identical whether the scratch segmentation uses delimiter, fixed, or surprise boundaries — the segmentation method cannot matter because nothing persists. *Fails if* the transient method changes any M-metric: that would mean segmentation is leaking into storage through an unlogged channel (a law-violation-grade bug, actually — worth knowing).

### (3) Falsification criterion
**E is KILLED if** M2 ≥ 2× B-64's M2 at equal M1 on either corpus at 10x — copies-only is strictly dominated by even the dumbest persistent segmentation, proving persistent identity (not segmentation per se) is the load-bearing idea. (We expect this criterion to fire. E exists to be killed informatively: its death certificate reads "references matter, transient segmentation does not.")

### (4) Buildability note
Pure Zag, trivial. Entries are variable-length (owned byte copies) — store as `{start:u32, len:u32, data: []u8}` with data `nio_alloc`'d per entry; or a single bump arena with offsets (simpler, deterministic). Scratch window: reuse the input buffer, no allocation. Hazards: none, except honest accounting — the arena *will* grow unboundedly with entries, which is the measured phenomenon, not a bug to fix. Do not "optimize" E with dedup — that would turn it into Arm D with extra steps and invalidate the control.

---

## Arm F — Surprise-driven cuts (two variants: F-S, F-B)

Thesis: the stream segments *itself* where it becomes unpredictable — the infant statistical-learning analogue, but fully deterministic.

### F-S: Markov-surprise cuts

**(1) Mechanism sketch.** A deterministic order-2 byte Markov predictor: `counts[65536][256]` (u32, saturating). **Pass 1 (train):** walk the corpus, increment `counts[(b[i-2],b[i-1])][b[i]]`. **Pass 2 (cut):** walk again with the frozen table; at each position compute the prediction `argmax` over the 256 counts for the context — tie-break: lowest byte value (total order, no randomness). Signal: **confident-miss** = (predicted ≠ actual) AND (count[predicted] ≥ CONF_BAR). A cut is emitted at position `i` if confident-miss holds AND its confidence (count[predicted]) is the local maximum within ±W positions AND positions are ≥ MIN_GAP apart — ties broken by lower offset per the global rule. Chunks = spans between cuts, recorded in the standard chunk table with just code 4 (surprise).

Organs: (2) eliminative hypothesis logic treats "cut here" as a hypothesis — the verification gate checks the resulting chunk recurs (`rep ≥ 2`) before commit; non-recurring surprise cuts are refused (`CUT_REFUSE`) — surprise alone doesn't mint vocabulary, surprise *proposes* it. (3) commits surviving cuts. (1)/(4) as in D. (5) may merge adjacent low-reuse chunks. The predictor itself is instrumentation, not intelligence: it never makes a decision, it only scores positions.

**(2) Falsifiable predictions.**
- **P-FS1 (strength):** On Shakespeare, F-S boundary F1-agreement with C-W ≥ 0.70 — surprise rediscovers word boundaries without being told about whitespace. *Fails if* < 0.5: the predictor isn't finding linguistic units.
- **P-FS2 (weakness — cut storm):** On sqlite3.c, high-entropy identifiers trigger confident-misses constantly; we predict F-S cut count ≥ 5× C-W's on code with M3 < 1.5 — surprise over-segments noise. *Fails if* cut count stays within 2× of C-W's (then the predictor is more robust than we think).
- **P-FS3:** F-S's M3 on prose is within 1.5× of C-W's — surprise buys little over delimiters for clean prose. *Fails if* F-S beats C-W by ≥2× (then surprise is genuinely finding sub-word structure like morphemes — update the theory).

**(3) Falsification criterion.** **F-S is KILLED if** (i) its Shakespeare boundary agreement with C-W is within ±0.05 F1 AND its M3 ≤ C-W's — it rediscovers whitespace at 67MB of predictor cost; **or** (ii) cut count > 5× C-W's on sqlite3.c (cut storm — the signal doesn't survive noise); **or** (iii) it loses to D on M3 on both corpora (surprise is the wrong signal for unit-hood; repetition+continuation wins).

**(4) Buildability note.** Pure Zag with one big caveat: `counts` is 65536 × 256 × 4B = **64MB — exceeds the 2^25 single-slice indexing limit**, so shard into 3 contiguous shards (e.g., 21846 contexts each ≈ 22.3MB) with shard = ctx / 21846, deterministic arithmetic. u16 saturating counters would halve it (32MB, 2 shards) — proposed; frozen at sign-off. Pass 1 and pass 2 are O(n) each. All argmax scans are index-ordered with lowest-byte tie-break. **Determinism risk:** none beyond the usual — counts are insertion-order-independent (addition commutes). Audit: `CUT_PROPOSE` with d2=4 at candidate cuts, `CUT_COMMIT`/`CUT_REFUSE` after the recurrence check. Hazards: the table build is the most memory-heavy structure in the whole battery — shard carefully, alias shards to locals, never hold two shards' borrows across a call boundary in ways the compiler dislikes.

### F-B: branching-continuation cuts

**(1) Mechanism sketch.** No predictor table. For each position, consider the longest prefix (lengths 2..LMAX) with `rep ≥ REP_BAR` (tracked via the same rolling-hash candidate mechanism as Arm D's proposer); for each such span, `contdiv` = distinct continuation bytes (bitset, as in D). **Cut before position `i`** if the span ending at `i-1` has `contdiv ≥ BR_BAR` (proposed: 3) — i.e., cut where a *repeated* span's continuation branches: the span is a completed unit because what follows it varies. This is "transitional-probability dip" with the probability replaced by integer branch counts. Chunks recorded with just code 5. Same propose → verify (recurrence) → commit/refuse gate as F-S.

**(2) Falsifiable predictions.**
- **P-FB1:** F-B's chunks have higher mean `contdiv` than C-W's by construction; we predict this translates to M3 ≥ C-W's on *both* corpora — branching is corpus-agnostic in a way whitespace isn't. *Fails if* M3 < C-W's on either corpus.
- **P-FB2:** F-B and F-S agree on ≥ 0.6 boundary F1 on Shakespeare (two surprise signals, one phenomenon) but diverge on sqlite3.c (F-B's repetition requirement filters identifier noise that F-S chokes on) — we predict F-B's code cut count ≤ 0.5× F-S's. *Fails if* F-B's code cut count ≥ F-S's: the repetition filter isn't filtering.

**(3) Falsification criterion.** **F-B is KILLED if** its M3 < C-W's on both corpora (branching finds worse units than whitespace); **or** it matches F-S within noise on all metrics on both corpora — redundant arm, keep F-S (cheaper to reason about) and retire F-B.

**(4) Buildability note.** Pure Zag; reuses Arm D's candidate-table machinery (rolling FNV, 4096-slot table, bitsets) with a different commit rule — build D's proposer once, parameterize the trigger. Cheapest smart arm to build after D exists. Same Zag hazards as D's proposer (eviction total order documented in prereg).

---

## Control-arm rationale: why A, B, C are non-negotiable

Without the dumb arms, we cannot prove the smart ones earn their complexity. Each control isolates exactly one question:

- **A (raw bytes) isolates: "is segmentation needed at all?"** It is the null hypothesis of the entire program. If any smart arm cannot beat *coordinates* on stored bytes at equal recall, segmentation is unjustified overhead — full stop. A also guards against a subtle failure mode: a smart arm could win on M3 while losing on M2 (elegant vocabulary, bloated storage), and only A makes that tradeoff visible, because A is the cheapest possible addressing scheme. Precedent: earlier TNN versions found no-chunking hurt; A retests that finding on the new five-organ architecture instead of inheriting it as folklore.

- **B (fixed grids, three sizes) isolates: "does boundary *placement* matter, or just boundary *existence*?"** B has segmentation without any intelligence — boundaries are arithmetic. If D beats B, the win must come from *where* D cuts, not from the mere fact of cutting. Three sizes (8/16/64) isolate granularity: they map the tradeoff curve (small = many IDs per entry, large = coarse units) so a smart arm's adaptivity can be credited properly — D choosing a 5-byte chunk where B-8 would use 8 is a *decision*, and B is what makes it legible as one. B is also the harness validator: the first arm built, proving the audit plumbing, probe protocol, and rerun check before any smart machinery exists.

- **C (delimiters, two variants) isolates: "how much of the smart arms' win is just rediscovering whitespace?"** This is the dangerous confound. A surprise-driven or repetition-driven cutter that merely re-derives word boundaries is an expensive way to write a tokenizer — C-W prices that discovery at one scan pass and zero decisions. Any smart arm must beat C-W *on C-W's home turf* (prose) to justify itself, and the C-W/C-P split further isolates the value of the delimiter prior itself: if C-P loses to C-W on code, we've measured the cost of a wrong linguistic prior, which is exactly the failure mode imposed segmentation always risks and self-cutting claims to avoid.

**No-free-lunch enforcement:** all twelve arms run the identical protocol — same corpora, same curriculum episodes, same memory budget, same probe set, same audit ledger. No arm gets a private metric. Kill bars are frozen at sign-off; a dead arm's death is recorded with its evidence, not argued away. Controls are never "killed" mid-battery — they are retired from *future* batteries only under strict dominance, because a control's job is to be the wall the contenders are measured against.

---

## Cross-cutting notes for the build phase

1. **Build order (proposed):** B-64 (harness validation) → A (null baseline) → C-W (dumb-smart baseline) → D's candidate proposer (shared with F-B) → D → F-B → F-S (heaviest) → E (trivial, build any time) → C-P, B-8, B-16 (parameter sweeps) → D-T, D-R (need D working).
2. **The 2^25 rule** hits three structures: the C/D chunk tables (shard by id >> 20), F-S's predictor (3 shards), and nothing else — corpora fit in single slices.
3. **The `==` rule** hits everywhere spans are compared: candidate matching, dedup checks, recall verification — all integer-triple or FNV+memcmp, never slice equality. State it once in the prereg; grep the codebase for `==` on slice types in review.
4. **Eviction determinism** (D proposer, F-B) is the subtlest byte-identical-rerun risk: the (count, seq) comparator and the insert-on-second-repeat rule must be specified to the integer in the prereg.
5. **Strength stays judgment-set** in every arm: `use_count` is evidence, never an input to a strength formula. Any arm found auto-deriving strength from counts fails review — that's reward-by-another-name and it violates program law.
6. **Force-pin** appears only in D-T (trainer seeds), always with trainer identity in the audit, always visible. No arm lets TNN self-force-pin.

---

## Proposed frozen kill-bar summary (awaiting signature)

| Arm | Dies if (any one) |
|---|---|
| A | Retired if B-64 strictly dominates on M1/M2/ops both corpora @10x |
| B-8/16/64 | A size retires if strictly dominated by another B size both corpora |
| C-W/C-P | Retire if a smart arm beats it ≥2x on M3 and M2 @equal M1, both corpora |
| **D** | M2/recall ≥ B-64 both corpora @10x; **or** churn > 0.30; **or** M1 < B-64 @equal budget |
| D-T | ≥50% of taught chunks revised/killed AND untaught D matches D-T |
| D-R | >50% of final vocab uncommitted @10x while D commits and wins M3 |
| E | M2 ≥ 2× B-64 @equal M1 either corpus (expected to fire — informative death) |
| F-S | ≈C-W boundaries (±0.05 F1) with M3 ≤ C-W; or code cuts > 5× C-W; or loses M3 to D both corpora |
| F-B | M3 < C-W both corpora; or within noise of F-S everywhere (redundant) |

*Twelve arms total: A, B-8, B-16, B-64, C-W, C-P, D, D-T, D-R, E, F-S, F-B. Bars above are PROPOSED — Micah signs before any build.*
