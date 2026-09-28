# CACHE LAYER: DEDUP + CONTENT-ADDRESSED DESIGN

**EXPLORATORY — NOT EVIDENCE**

**Date:** 2026-09-21
**Track:** WIDE EXPLORATION worker — TNN representation program ("what is a unit of
knowledge, if not an LLM token")
**Status:** NON-BINDING design sketches + falsifiable predictions. Nothing here is a
frozen claim, a metric change, a bar, or a kill criterion. It may not be cited as program
evidence. If any proposal below contradicts the frozen prereg
(`~/workspace/tnn-lab/units/PREREG_FREEZE.md`, awaiting Micah's sign-off), the
contradiction is flagged in an **AMENDMENT PROPOSAL** section and NOT adopted — it needs
Micah's re-approval per RULE-9.
**Scope:** arms K1/K2/K3/L1/L2 identity semantics as a real cache substrate. Pure-Zag
sketches only. Zero randomness in any AI decision path (program law RULE-3).

Parent material (all read, all PROPOSED except where marked):
`units/ALPHABET_G-L.md` (arm K family: K1 full SHA-256, K2 FNV-1a-64, K3
content-payload + position-reference composite; arm L family: position IDs),
`units/ARCHAEOLOGY_R31.md` (dual-route endogenous chunking — the "chunking must not
erase raw evidence" verdict, which this doc's cache design must respect),
`units/PREREG_FREEZE.md` (frozen bars: K1 dedup kill <15% on corpus A, A-24; K1/K2
bidirectional kill, A-25; K3 hybrid-promotion rule, A-26; M-32 M7 bars: hit ≥90%,
reuse ≥1.5, dedup ≥0.4).

---

## 0. The question in one line

Content-addressed IDs make the store *structurally* a cache: the identity function
`ID(content)` doubles as the dedup key. This doc works out what that implies for a
real substrate — what "add" means on a hit, how one-entry-per-content interacts with
the deliberate memory organs (kill/pin/promote/demote/strengthen/weaken), and what
exactly we would measure to falsify the design.

---

## 1. IDENTITY SEMANTICS — ID = hash(content)

### 1.1 Hash choice: reuse R33, do not reinvent

The substrate already ships a native, bounded SHA-256:
`toolchain/R33_NATIVE_SHA256_V2.zag` (`fn ns_sha256(input:[]u8, out:[]u8) i32`),
imported by `substrate/cl/common.zag` as a **bare** `@import` (commented-out imports
are silently ignored — AGENTS.md lesson; any trial substrate dir must carry
`R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` beside `cl/` or the compile
fails). API: input ≤ 33,554,360 bytes, out ≥ 32 bytes; negative return = error code
(`-7403` bounds, `-12` alloc, `-7401` constant-load). Chunks are ≤ 4 KiB staging
windows — orders of magnitude under the bound, so the call is a flat, deterministic
`O(len)` per add. There is no reason to write another hash for the K1 primary arm;
the K2 arm exists precisely to price the hash (FNV-1a-64, ~15 lines of pure Zag, no
native import), so the bake-off itself measures "was native SHA-256 worth it."

### 1.2 Truncation policy: none. The digest is the identity, all 256 bits.

The record already stores `id: u64[4]` — that *is* the full SHA-256 digest (four
64-bit words), not a truncation. No truncation policy is needed, and introducing one
would buy collisions with no upside: the quad fits in the record, compares as four
integer words, and probes from `digest[0] mod capacity` exactly as arm K1's prereg
freezes. Truncation only enters as a **K2 question** (64-bit FNV-1a, where the
birthday bound is honest and the collision chain is a first-class citizen — see
§1.3). Recommendation: keep K1 at the full quad; the "what if we hashed less" leg
belongs to K2's bake-off, not the primary substrate.

### 1.3 Deterministic collision handling with zero randomness

Collision taxonomy (deterministic, no randomness anywhere):

1. **Probe collision** (two digests, same table slot): open addressing, linear probe
   from `digest[0] mod capacity` — the prereg-frozen rule. Deterministic because the
   start point is a pure function of content.
2. **Digest equality, distinct bytes** (true SHA-256 collision): on quad equality,
   confirm with a full explicit byte-loop over the append-only byte store (never slice
   `==` — Zag gotcha). A *true* collision chains by **insertion order** (logged) in a
   slot-linked list; the ID stays the digest, disambiguated by chain position. The
   chain path is exercised only with preregistered synthetic forced collisions —
   not reachable in practice, but the code path exists and is tested.
3. **K2 digest equality:** same as (2), except the chain path is *expected* to engage
   (chain-length bar: K2 dies if any chain exceeds 4 on any corpus run, A-25).

Tie-breaking anywhere else (arbitration, merge-select) is by ascending integer
(slot, offset, tiling) — never by digest word, never by hash-map iteration order,
never by wall clock. This keeps "same input + same logged state → byte-identical
output" constructional: the ID is a pure function of content, so replays cannot
diverge on identity even when allocation order, heap fragmentation, or ASLR-equivalent
bases differ across reruns (this is prediction P2 below).

Sketch (pure Zag; slice-aliasing and large-struct conventions honored):

```zag
@import("R33_NATIVE_SHA256_V2.zag")   // BARE directive — not //-commented

// Digest quad compare: four integer compares. Never slice ==.
fn digest_eq(a:*Chunk, b:*Chunk)i32 {
    let ia:[]u64 = a.*.id;            // alias before indexing (large-struct rule)
    let ib:[]u64 = b.*.id;
    if(ia[0]!=ib[0]){return 0;}
    if(ia[1]!=ib[1]){return 0;}
    if(ia[2]!=ib[2]){return 0;}
    if(ia[3]!=ib[3]){return 0;}
    return 1;
}

// Content-confirm on quad equality: explicit byte loop over immutable segments.
fn bytes_confirm(seg:[]u8, off:u32, len:u32, want:[]u8)i32 {
    let i:u32=0;
    while(i<len){ if(seg[off+i]!=want[i]){return 0;} i=i+1; }
    return 1;
}

// ID minting: pure function of content. No state read, no state mutated.
fn mint_id(content:[]u8, quad:[]u64)i32 {
    let dig:[]u8 = nio_alloc(32);                 // returned by nio_alloc → nio_free only this
    if(dig.len!=32){return -12;}
    let rc:i32 = ns_sha256(content, dig);
    if(rc!=0){ nio_free(dig); return rc; }
    let w:i32=0; let q:i32=0;
    while(w<4){                                   // big-endian pack, deterministic
        let x:u64=0; let b:i32=0;
        while(b<8){ x=(x<<8)|(dig[q*8+b] as u64); b=b+1; }
        quad[w]=x; w=w+1; q=q+1;
    }
    nio_free(dig);
    return 0;
}
```

Note the `_zag_arg`-style pitfall does not apply here, but the AGENTS.md lesson
about `_zag_strcmp` returning 1 on equality is the same class of trap:
`digest_eq` returns **1 on equality** by construction — documented, tested, and never
compared against 0-style C semantics by accident.

### 1.4 AMENDMENT PROPOSAL (none yet)

This section (§1) proposes no change to any frozen bar. K1's prereg (A-24: full
SHA-256, probe/chain rules, synthetic collision vectors, dedup bars) is taken as
written. If the bake-off later shows the chain-order rule ("insertion order, logged")
violates the M8 byte-identical gate under allocator perturbation, that contradiction
gets a dated amendment — it is flagged here as a watched risk, not a proposal.

---

## 2. DEDUP MECHANICS — one entry or two?

### 2.1 Core design decision: **ONE payload entry per unique content; occurrences are
separate reference records.**

The same byte span occurring twice is **one memory entry** at the payload level, and
that is a structural fact, not a policy: under K identity the two occurrences are
literally the same chunk. But the deliberate-memory organs cannot operate on "the
same chunk" without losing *where* it was seen — and position is what L1 owns. The
resolution is the K3 composite (predicted in ALPHABET_G-L as the substrate both
schemes are secretly asking for):

- **Payload record** (content-addressed): `id_content = sha256 quad`, `refcount`,
  signed `value` (MA4), `strength` (judgment-set), `flags` (pin), level/tiling links.
  Exactly one per unique byte span. Dedup is automatic and structural.
- **Reference records** (position-addressed): `id_pos = (stream, seg, off)` →
  pointer at the payload slot. One per occurrence. This is where "the" at line 10
  and "the" at line 10,000 remain distinguishable.

So the honest answer to "one entry or two" is **both, at different layers**: one
payload entry (the thing the K bake-off prices), plus one lightweight reference
record per occurrence (the thing L identity governs). Neither pure-K1 (one record,
position-blind) nor pure-L1 (N records, no dedup) is the working substrate; K3's
split is load-bearing for everything in §2.2.

Why this split is forced, not optional — consider the alternatives:
- **One record only (pure K1):** `kill` of "the word at line 10" kills the shared
  record — 10,000 other occurrences lose their memory. Reference counting alone
  cannot express "forget *this occurrence*" vs "forget the pattern." Kill becomes
  unusable as a deliberate act on occurrences.
- **N records only (pure L1):** no dedup at all; the cache layer has nothing to be
  a cache *of*; M-32's dedup bar (≥0.4) is unreachable by construction. This is the
  arm L1's kill criterion (A-27: >3× K1 store cost with no accuracy advantage).

### 2.2 Exact memory-op semantics

Define the ops against the K3 split. Every op below is audited with the existing
16-word entry layout
(op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60);
`OP_DEDUP_HIT` and `OP_ADD_CHUNK` are the already-proposed new opcodes (crew-2
namespace, subject to A-3 unification).

| Operation | Payload effect | Reference effect | Audit |
|---|---|---|---|
| `add(content, pos)` on **miss** | new payload record; refcount=1 | new reference record pos→payload | `OP_ADD_CHUNK` (quad in b1..b4, position in a1..a2) |
| `add(content, pos)` on **hit** | refcount++ (occurrence count); **no strength change** (see §2.3) | new reference record pos→payload | `OP_DEDUP_HIT` + ref-add (refcount is visible work, not a silent shortcut) |
| `kill_reference(pos)` | refcount-- | reference record dropped | `OP_KILL_CHUNK` with `link_only=1` |
| `kill_payload(content)` (deliberate) | payload dropped **iff refcount==0**; else refused and audited as refused (a deliberate act cannot orphan references — Y6-style atomicity applies here) | all references dropped atomically (they were the only barrier) | `OP_KILL_CHUNK`; or refusal entry if refcount>0 |
| `pin(content)` | payload `flags.pin=1` (force-pin stays human/trainer-only, audited, visible — program law) | references inherit protection (cannot be triage-killed while payload pinned) | pin audit (existing op) |
| `promote/demote(content)` | hierarchy link ops on the payload record (I-family) | n/a | `OP_LINK_PARENT` / demotion |
| `strengthen(content)` / `weaken(content)` | **judgment-set only, never automatic** (§2.3) | n/a | existing strengthen/weaken ops with cited evidence |

**Pressure behavior (G1 triage) under this split:** triage picks victims by
`(value ASC, slot ASC)` over *payload* records. Killing a payload with refcount>0
requires the deliberate `kill_payload` path; under pressure the triage organ instead
kills *references* (link-only), dropping occurrence records while the payload
survives. Payload death under pressure requires refcount to reach 0 *and* an
explicit deliberate decision — pressure alone never orphans. This keeps G1's
thrash/junk-fusion kill criteria meaningful: they are measured on payload records,
not on occurrence bookkeeping.

**Byte store interaction:** bytes are append-only (ALPHABET_G-L cross-cutting law
3). Dedup means the byte store still holds N copies (immutable segments) while the
*index* holds 1 payload + N references. Payload-byte savings (K1's metric) come
from the index/record side, and if a future GC compacts the byte store, the payload
record is the single pointer the compactor walks. No byte loss, ever — kills drop
records only.

### 2.3 What "add" means when the content already exists — **no-op with audit note
plus refcount++, NEVER automatic strengthen**

This is the one decision I considered a genuine fork ("test both" per RULE-2
would demand a leg), and I am taking a position for the sketch while leaving the
fork open for the bake-off:

- **Chosen:** `add` on a hit = `OP_DEDUP_HIT` + refcount++ + new reference record.
  Strength is **untouched**. Strengthen is a separate, deliberate, audited judgment
  by the memory organ — repetition is *evidence* the organ may cite, but it is never
  a formula applied by the cache layer. This is forced by Micah's law: *"strength
  is set by judgment (TNN's or a human's), never by formula or background
  accumulation"* (MEMORY.md boundary, strength-trial program law).
- **Rejected fork (documented, not built):** auto-strengthen on hit. It is a
  frequency→strength formula by another name — background accumulation wearing a
  cache costume. If built, prediction P4 says it inflates junk (";" and whitespace
  become the strongest memories). Per RULE-2 this fork could be a leg — recorded
  here as the named loser to test, per no-free-lunch.

The dedup hit is still *visible*: `OP_DEDUP_HIT` is a first-class audit entry, so
the reuse accounting in §4 and the M7 metric family can see every hit. The cache
never acts silently — "reuse is visible work, not a silent shortcut" (ALPHABET_G-L,
K1).

### 2.4 AMENDMENT PROPOSAL

- **Proposed (non-binding):** reference-record lifecycle (`link_only` kills,
  payload-refusal when refcount>0) adds two audit-entry *flavors* to
  `OP_KILL_CHUNK`. This is within the "new audit opcodes are cheap and visible"
  law (only op *codes*/flavors change, never the 16-word layout), but the
  opcode-namespace unification (A-3) may want these flavors named before build.
  Flagged for the sign-off checklist, not adopted.
- **No change proposed** to frozen bars A-24/A-25/A-26/A-27, M-32, or any kill
  criterion.

---

## 3. K3 HYBRID — the predicted eventual substrate (layout sketch)

K3 = content-addressed **payload**, position-addressed **reference**. This section is
a build-ready sketch, not a build order — K3 is the third arm in the K-vs-L
bake-off (A-26/A-29), and if it loses the bake-off it dies as a candidate. The
sketch exists so that *if* it wins, the substrate is already specified.

### 3.1 Record layout

```
Payload {                        // exactly one per unique byte span
  id_content: u64[4]             // sha256(content) — K1's quad
  seg:    u32                    // first-seen segment (byte home)
  off:    u32
  len:    u32
  level:  u8                     // I-family hierarchy
  tiling: u8                     // J-family tiling tag (payload is tiling-shared)
  value:  i64                    // MA4 signed judgment about this memory
  strength:u8                    // judgment-set, never formulaic
  flags:  u8                     // bit0 = pin (force-pin: human/trainer-only)
  refcount:u32                   // live reference records pointing here
  parent: i32                    // I-family links live on the payload
  child_head: i32
  chain_next: i32                // collision chain (insertion order), -1 = none
  revise_head: i32               // OP_REVISE_LINK chain head (K1 revision lineage)
}

Reference {                      // one per occurrence
  id_pos:  u64[2]                // (stream, seg, off) packed — L1's eternal ID
  payload: i32                   // payload slot (integer selector)
  tiling: u8                     // which tiling observed this occurrence (J)
  flags:  u8                     // occurrence-local flags (e.g. taught-mark)
}
```

Payload lives in the dedup hash table (open addressing, linear probe from
`digest[0] mod capacity`, capacity 2× expected uniques — A-24). References live in
a per-segment array (occurrence order = stream order — L1's "sequential recall is
free" property survives: walk the reference array, dereference payload).

### 3.2 Revision under K3 (corpus C behavior)

An edit changes bytes → new content hash → **new payload** (possibly deduplicated
for free against an existing span — an edit that makes a span identical to another
span *merges for free*, ALPHABET_G-L K3). The position ID stands still; the
reference record's `payload` selector is repointed, audited by
`OP_REVISE_LINK(old_quad → new_quad, reason, cite_ep)` — append-only lineage, and
M-18's "kill+re-add ≠ revision" rule is satisfied because the payload record is
born with its revise-link. References never dangle; history is never rewritten
(K1's promise, inherited).

### 3.3 Why K3 is the *predicted* eventual substrate (still must win the bake-off)

- It is the only layout where the K arm's dedup bars (A-24: ≥15% on corpus A) and
  the L arm's eternity bar (A-27: zero ID churn) can both hold: content churns in
  the payload layer, positions stand still in the reference layer.
- It makes taught vocabulary (arm O) sane: teaching points at the payload
  ("the word *quark*" = one payload ID); every occurrence reference inherits the
  teaching. Under pure L1, teaching is enumeration (one ID per occurrence); under
  pure K1, teaching has no position to attach *where*-judgments to.
- It satisfies R31's dual-route verdict by construction: the raw route keeps
  `(seg, off)` byte spans; the chunked route keeps payloads. Chunking can never
  erase raw evidence because the byte store is append-only and the payload is an
  index over it, not a replacement.

### 3.4 AMENDMENT PROPOSAL (none)

K3 is already the third bake-off arm (A-26/A-29). This sketch proposes no change
to the bake-off's metrics, conditions, or the hybrid-promotion rule (beats both
pure schemes on ≥3/5 metrics → pure schemes demoted to components).

---

## 4. CACHE-HIT ACCOUNTING — precise enough to measure later

Frozen metrics keep their definitions (M-32: hit ≥90%, reuse ≥1.5, dedup ≥0.4 —
none redefined here). What follows is the *instrumentation vocabulary* a cache
substrate must emit so those metrics — and future ones — are computable from the
audit ledger alone. Every term is integer-counted; wall-clock is informational only
(M-56).

**Definitions (ledger-derived, all counts):**

- **ADD-MISS:** `add(content,pos)` where the digest is absent → new payload.
  Counted by `OP_ADD_CHUNK` entries.
- **ADD-HIT (dedup hit):** `add(content,pos)` where the digest is present and
  byte-confirmed → refcount++ + new reference. Counted by `OP_DEDUP_HIT` entries.
  (A "hit" never implies the content was *useful* — only that it was *seen*.)
- **RECALL-HIT:** a recall query that resolves to an existing reference/payload
  with no new record created. Counted by recall-query entries with `created=0`.
- **RECALL-MISS:** a recall query that finds no covering chunk (falls back to raw
  route per R31's dual-route rule, or to a fallback coarse chunk per H1).
- **REUSE:** a recall served from a payload that has been recalled before —
  `reuse_count = total_recalls − distinct_payloads_recalled`. The M7 "reuse ≥1.5"
  bar is `total_recalls / distinct_payloads_recalled ≥ 1.5`.
- **PROBE-COST:** table probes per add (mean and max over the run — both logged;
  the max is the adversarial figure, the mean is the honest one).
- **HIT-RATE (add-side):** `ADD-HIT / (ADD-HIT + ADD-MISS)` over a frozen window.
- **OCCURRENCE FAN-OUT:** `references / payloads` — mean refcount; the structural
  measure of how "cache-like" the store is. Fan-out 1.0 = no dedup at all.
- **STALE-HIT:** an ADD-HIT on a payload whose references are all dead
  (refcount was 0, payload retained deliberately) — counted separately so
  "resurrection" of deliberately-retired content is visible in the ledger.

**Measurability rule:** every quantity above is derivable from the audit ledger +
the store image at episode boundaries — no wall clock, no sampler, no unlogged
state. A run that cannot reconstruct these numbers from its ledger fails the
determinism gate's spirit even if its bytes match (the state wasn't *complete*).

**Prediction-adjacent accounting claim (P5 below):** the audit-ledger byte
histogram (wave-11's first measurement) will show `OP_DEDUP_HIT` as a distinct,
large-count opcode on repetitive corpora — the cache's footprint is *visible in
the histogram*, which is exactly what "reuse is visible work" means operationally.

---

## 5. FALSIFIABLE PREDICTIONS (each with its experiment)

**P1 — Dedup ratio bands on the frozen corpora.**
On 64-byte cut spans (fixed grid, the K-bake-off baseline): `dedup_ratio =
1 − unique_payload_bytes / input_bytes` will land in **[0.50, 0.80] on corpus A
(Shakespeare prose)** and **[0.25, 0.55] on corpus B (sqlite3.c code)** — because
A is dominated by short repeated words, character names, and verse refrains (high
span repetition at fixed phase), while B repeats boilerplate and idioms but carries
a long tail of unique identifiers that defeat byte-exact matching.
*Experiment:* K1 1x leg, fixed-64B cut, count payload table occupancy vs input
bytes; report the ratio with the integer counts. *Falsifies* if either corpus
falls outside its band (the caching story is then mis-calibrated, not just weak —
and A-24's 15% kill floor is far below the P1 band, so P1 failing would not kill
K1; it would kill *this sketch's* calibration).
*Note:* ratio, not the K-arm's "payload savings" bar — different quantities; the
frozen bar is untouched.

**P2 — Content-addressing makes byte-identical reruns structural.**
Because `ID = f(content)` reads no allocator/heap/timing state, the K1/K3 arms
will pass the M8 adversarial-perturbation legs (heap pre-fragmentation,
ASLR-equivalent base offset, free-list order reversal — A-35) with **zero
ID divergence across all 5 runs** — not merely byte-identical outputs, but
identical ID assignment *order*: the nth distinct span minted gets the same slot
in every run. A serial/issuance ID scheme (arm M) can also pass M8, but only by
keeping issuance order out of allocator state — the experiment discriminates by
*why* they pass: under content addressing, perturbing allocation cannot move an ID
because the ID was never allocated.
*Experiment:* M8 protocol (N=5 + the four perturbations) on K1 vs M (counter-ID
control); diff the minted-ID sequence per run, not just final outputs. *Falsifies*
if any K1 run diverges in ID assignment (then identity is leaking unlogged state
and the determinism-gate claim is broken at the design level).

**P3 — Second-pass hit rate saturates near unity (the cache actually caches).**
Two-pass protocol on corpus A with deliberate (H2-budgeted) cuts: pass 1 populates
the store; pass 2 over the *identical* byte stream will show add-side hit-rate
**≥ 0.95** (nearly every add is an `OP_DEDUP_HIT`), because deterministic cutting
on identical bytes yields identical spans and content addressing recognizes them.
*Experiment:* run H2+K1 twice over corpus A; report pass-2 hit-rate and
occurrence fan-out. *Falsifies* if pass-2 hit-rate < 0.90 — which would mean the
cut policy is not a pure function of (bytes, logged state) (a determinism-gate
violation wearing a cache costume) or the dedup table is lossy.

**P4 — Auto-strengthen-on-hit inflates junk (the rejected fork, priced).**
If a leg is run with the rejected fork (§2.3: `add`-on-hit auto-strengthens),
then within 10,000 episodes the correlation between span frequency and strength
will exceed **0.9**, and the top-decile-strength set will be dominated by
punctuation/whitespace spans (the most frequent, least valuable content) —
measurable against the judgment-held arm where frequency–strength correlation
stays **< 0.5**. *Experiment:* RULE-2 test-both leg — identical curriculum,
strength-on-hit vs judgment-only; report frequency–strength correlation and the
byte composition of the top strength decile. *Falsifies* if auto-strengthen does
*not* inflate junk (then the "strength is judgment" law's cache-side rationale is
weaker than claimed — the law itself is frozen regardless; this tests the
*mechanism story*, not the law).

**P5 — Revision churn forks payloads linearly; references stay still (corpus C).**
On the frozen 100-patch corpus-C series, K3's unique payload count will grow
**≈ (patches × mean touched spans)** — every one-byte edit forks identity
completely (K1's near-dupe brittleness, acknowledged in ALPHABET_G-L) — while the
reference-record count stays flat (positions are eternal) and **zero** existing
position IDs change (A-27's eternity bar). The discriminating sub-prediction: an
edit that makes a span byte-identical to an *already-stored* span produces an
`OP_DEDUP_HIT`, not a new payload — the "merges for free" effect — countable in
the ledger.
*Experiment:* K3 on corpus C; report payload growth vs patches×touched, reference
count flatness, free-merge hit count. *Falsifies* if payload growth is
sub-linear *without* free-merges explaining it (dedup is then doing something
unaccounted — similarity smuggled in), or if any position ID changes (L-side
promise broken — kills the composite's reason to exist).

---

## 6. HARDEST OPEN QUESTION

**How does repetition inform strength without becoming a formula?**

Everything else in this doc is mechanism — hash it, probe it, count it, audit it.
But §2.3's decision exposes the one genuine tension between the cache layer and
Micah's law. The cache *knows* something real: a span seen 10,000 times with
refcount 10,000 is, in every information-theoretic sense, load-bearing for the
system's memory. The deliberate-memory organs are *forbidden* from converting that
into strength by rule — strength is judgment-set, never formulaic, never
background accumulation. Yet a judgment organ that ignores 10,000 repetitions is
not being principled; it's being blind. The open question is what the *interface*
between structural repetition-evidence and deliberate judgment looks like:

- Is repetition-evidence one input among many to a deliberate strengthen decision
  (cited in the audit via `cite_ep`), with the organ free to refuse?
- Does the organ need its *own* bar for "when does frequency become evidence"
  (a prereg-frozen threshold — which is itself a formula wearing a bar costume)?
- Or is there a third category — neither automatic strengthen nor ignored
  evidence — like a "noticed but unjudged" state that a later deliberation can
  pick up?

P4 prices the failure mode of getting this wrong (junk inflation), but no
prediction here tells us the right interface. The bake-off can measure outcomes
(recall quality, junk rates) but the *judgment vs formula* line is a design-law
question, and design-law questions are settled by Micah, not by experiment. That
is why this is the hardest: it's the one place where the cache's structural
honesty and the program's judgment law don't yet have a shared vocabulary.

Second-hardest, recorded for completeness: **near-duplicates.** A one-byte
difference forks identity completely under K; L shares position but not content.
Both schemes leave the similarity hole open (ALPHABET_G-L open tension 1), and
every softening of identity (prefix hashing, LSH-style buckets) threatens either
the zero-randomness law or byte-exact recall. Flagged as future-arm territory —
not smuggled into this substrate.

---

## 7. BUILD NOTES (for whoever builds the K-family trial substrate)

- Trial substrate dirs must carry `R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag`
  beside `cl/` (AGENTS.md lesson — the `@import` in `cl/common.zag` is bare and
  fails confusingly otherwise).
- Never slice-`==` digests (quad integer compare only); alias large-struct array
  fields to locals before indexing; chunk all buffers ≤ 2^25 bytes
  (toolchain wall, §1 A-6 — chunking is a build note with byte-identical-equivalence
  proof, never a prereg amendment).
- `_zag_strcmp`-class trap: equality functions return 1 on equality in this codebase's
  conventions — `digest_eq` follows suit, documented at the definition site.
- `nio_free` only what `nio_alloc` / `_zag_i64_to_str` returned (the `dig` buffer in
  `mint_id` is freed exactly once on every path — including the error path).
- Audit entries stay 16 words; only new op *codes*/flavors (`OP_DEDUP_HIT`,
  `link_only` flavor of `OP_KILL_CHUNK`) — the wave-11 ledger byte histogram can
  then tell memory administration apart from cache work apart from representation work.
- Determinism gate first: before any scale leg, diff two reruns per leg (the K-arm
  bake-off's cross-cutting gate in ALPHABET_G-L §"Recommended experiment matrix" step 4).
- No binaries, no `.zagd`, no `.zag-cache/` committed — ever.

---

## 8. AMENDMENT PROPOSALS — consolidated (all NON-BINDING, all need Micah)

1. §2.4: name the `link_only` / payload-refusal flavors of `OP_KILL_CHUNK` in the
   A-3 opcode-namespace unification before any K3 build.
2. §1.4: watched risk — if "insertion order, logged" chain ordering ever conflicts
   with the M8 gate, a dated amendment (not a silent fix).
3. RULE-2 candidate: the §2.3 strengthen-on-hit fork as a named test-both leg
   (P4 prices it; the prereg currently mandates judgment-only strength, so the leg
   needs explicit sign-off as an experiment, not as a policy change).

No frozen bar, metric, or kill criterion is reinterpreted, softened, or changed
anywhere in this document.
