# EXPLORE 04 — Cache-layer design sketch: content-addressed chunk IDs, invalidation, ghost-ID prevention

**Status: EXPLORATORY / NON-BINDING — design notes only, no frozen claims.**
Nothing here changes frozen bars. If pursued, it would amend **A-4** (chunk-ID
width unification), **A-24** (K2 collision-chain rules), **A-47** (Y3
lineage/tombstone policy), and **M-32** (M7 dedup-bar accounting).

**Frozen context:** arm D mints stable IDs for self-cut spans with "tombstoned IDs
never reused"; K1/K2/K3/L1/L2/M/Y3 are the identity-scheme arms; U
(recompute-on-demand) is the anti-caching arm that makes D's caching falsifiable;
M7 bars hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4. Probe 2 (`probe_id.zag`, all 13 checks
PASS, byte-identical) validated the mechanism sketch below at small scale.

---

## 1. The ID

`ID = (content_hash, generation)` — never content-hash alone.

- **content_hash:** FNV-1a 64 (K2) or SHA-256 (K1) over the span bytes. This is the
  *dedup key*: identical live bytes → identical content_hash → dedup falls out,
  which is what M7's dedup ≥ 0.4 bar measures.
- **generation:** a store-local monotonic counter stamped at mint time. This is
  what makes "tombstoned IDs never reused" (arm D, A-47) *implementable*: the full
  ID is the pair, so re-adding identical bytes after a tombstone mints
  `(same_hash, new_generation)` — a fresh ID by construction.

Probe 2 proved the tension this resolves: with pure content-hash IDs, re-adding
tombstoned bytes re-issues the tombstoned ID (the probe's first implementation
did exactly this — a live slot re-acquired a tombstoned ID). The probe's fix —
deterministic remix `id ^ attempt*0x9E3779B9` while the content-ID is tombstoned —
is the poor-man's generation stamp. The real design stamps it explicitly.

**Consequence for A-4:** pure K1 ("same bytes, same ID") cannot satisfy A-47
("tombstoned IDs never reused") without a generation component. This is evidence
for the K3-hybrid side of the unification decision: the identity substrate is
`content × generation`, and K1 survives only as the *dedup-key component*, not
as the whole ID. (Micah's A-4 decision; this sketch is input, not a ruling.)

## 2. Dedup and the cache

- **Dedup table:** `content_hash → live ID` (only live entries indexed). Add path:
  1. compute content_hash;
  2. if a *live* entry has this hash **and** byte-identical content → return its ID
     (dedup hit; M7 reuse counter++);
  3. if a *tombstoned* entry has this hash → mint `(hash, gen++)` (never resurrect);
  4. else mint `(hash, gen++)` fresh.
- **Collision chains (K2, A-24):** distinct contents sharing a content_hash chain
  off the hash bucket with byte-compare disambiguation (probe 2, check b). Chain
  length is a counted, reported metric — "honest, counted collisions." Chain bar
  proposal: mean chain length is reported per corpus; the A-24 kill bar
  (chain > 4 → K2 dies) applies to *accidental* chains; *forced/adversarial*
  chains are a separate red-team input (see 02, design 2).
- **Cache semantics:** the chunk store is a cache over the corpus + derivation
  log, keyed by full ID. U (recompute-on-demand) is the measured alternative:
  the sketch keeps a ` derivation_cost` ledger per ID so the D-vs-U crossover
  (A-41) can be computed per chunk, not just per arm.

## 3. Invalidation on revision

Revision (Z6 scars, M4 battery, Y3 lineage) follows one rule: **revision never
mutates an ID in place** (this is also L1's "one promise" — A-27).

- `REVISE(span_id, new_bytes)`:
  1. tombstone `span_id` (state → TOMBSTONE, content retained in the arena for
     audit, never served);
  2. mint `(hash(new_bytes), gen++)` as the successor;
  3. append a lineage edge `old_id → new_id` with reason code (the Y3 lineage;
     probe 2 checks c/d);
  4. **invalidation:** every cache entry keyed by `old_id` is dropped or
     re-keyed — the cache never serves content under a tombstoned key.
- **Kill-substitution guard (M-20):** the revision path is instrumented so the
  M4 metric can distinguish genuine revision (lineage edge present) from
  kill+re-add (no edge) — the sketch stores the edge *in the same atomic op* as
  the tombstone, so "forgot to link" is not representable.
- **Cascade policy (Y6):** per-chunk cascade is set at creation (A-50); linked
  span-sets (Y5) invalidate atomically via the LINK edge — any kill leaving a
  live span pointing at a dead LINK fails the Y5 atomicity bar by construction
  (the resolver returns TOMBSTONE, never the stale target — probe 2, check d).

## 4. Ghost-ID prevention

A *ghost ID* is any reference that resolves to content the store no longer
stands behind: dangling pointers, resurrected tombstones, cross-store ID reuse.

Four interlocking rules (all probe-2-validated at small scale):

1. **Resolve total:** every ID presented by an external party (another TNN,
   the teacher wire, a cached reference) resolves to exactly one of
   `{LIVE(content), TOMBSTONE, NOT_FOUND}`. There is no fourth outcome and no
   silent fallback to "nearest live." (Probe 2: `store_resolve` returns 1/2/0.)
2. **Tombstones are forever and visible:** tombstoned IDs are never re-issued
   (generation stamp, §1), never garbage-collected silently (Y3's "tombstone GC
   policy (preregistered, never silent)", A-47), and resolve to TOMBSTONE — a
   *loud* answer, not a missing one. Loudness matters: a silent NOT_FOUND lets a
   caller retry with a different ID and accidentally land on live content
   (the confusion the K1 "contextually-wrong occurrence" bar, A-24(iii), fears).
3. **No cross-store ID reuse without re-keying:** counter IDs (arm M) are
   store-local; the two-TNN merge trial remaps them, and the remap is verified
   (arm M's kill bar: ≥1 dangling/misdirected pointer kills counter IDs as the
   global identity). Content+gen IDs are merge-safe *iff* generations are
   namespaced per store — the merge protocol must re-stamp generations, never
   assume two stores' `gen=7` means the same thing.
4. **Teacher-wire IDs are untrusted input:** any ID arriving over the §P wire is
   resolved through rule 1 before use; a TOMBSTONE or NOT_FOUND answer rejects
   the proposal (arm O's ingress gate), it never triggers a re-fetch-by-guess.
   (Cf. 02 design 3, wire smuggling.)

## 5. What this sketch deliberately does NOT decide (frozen items)

- **A-4 width unification** (u32 monotonic vs u64[4] vs SHA-256 vs
  (serial,gen,refs)): the sketch needs `(content_hash, generation)` but does not
  pick the hash width — that interacts with K2's chain bar and is Micah's call.
- **A-24 numeric bars** (dedup predicted 40%/25%, kill <15%): the sketch provides
  the counters; the bars stay frozen-proposed.
- **M-32 accounting**: whether remix-minted IDs (same bytes, new generation)
  count for or against the dedup ≥ 0.4 bar needs a frozen ruling — the sketch
  flags it: counting them as dedup *hits* would let an arm game M7 by
  revise-and-re-add cycling. Proposed: they count as *misses* (fresh mints).
- **A-41 U-vs-D crossover**: the per-chunk derivation-cost ledger is sketched;
  the λ/μ pricing and kill bars are frozen-proposed, untouched.

---

## Probe evidence

`probe_id.zag` (pure Zag, zero RNG, byte-identical N=2): 13/13 checks PASS —
dedup-honest, forced-collision chaining with content disambiguation,
revise→tombstone→never-reissued, ghost-ID→TOMBSTONE, unknown→NOT_FOUND,
resurrect-attempt→fresh-ID with tombstone intact. The probe is the executable
companion to §§1–4 at 64-slot scale.
