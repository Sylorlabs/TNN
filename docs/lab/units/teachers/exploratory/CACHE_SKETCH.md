# CACHE SKETCH — Taught-word chunk IDs as a cache layer

**Crew:** 7 (non-binding exploratory track), TNN Representation Program
**Date:** 2026-09-21
**Status:** PURE DESIGN DOC. No code, no frozen changes. The Track B prereg is FROZEN
(Micah signed 2026-09-21); nothing here changes any frozen bar, metric, kill
criterion, or the §P / TST-1 / §C specs. Every metric and rule sketched is labeled
**PROPOSED-FUTURE-AMENDMENT** and needs Micah's re-approval per RULE-9 before it
constrains any build.

## Context this sketch plugs into

- **Arm D** (Micah's cached chunk-ID hypothesis): *a chunk is a byte span with a
  stable ID that memory points back to, retrieves, and reuses.* The cache layer is
  D's home territory.
- **Arm U** (recompute-on-demand, no stored segmentation): the falsification
  battleground. If U wins the D-vs-U head-to-head on total cost, caching is "a
  convenience, not a necessity" — and this sketch retires to "interesting but
  uneconomical." The sketch is written honestly under that sword: it must earn its
  keep against recompute, not assume it.
- **K vs L identity schemes** (ALPHABET_G-L.md): K = content-addressed (bytes → ID,
  position accidental); L = position-addressed (position → ID, bytes accidental);
  counter IDs (monotonic serials, per A-4) as the third candidate. The bake-off —
  not this sketch — decides which scheme wins. The sketch shows how taught words
  plug into a cache layer under *each* scheme, so the layer doesn't pre-decide the
  bake-off.
- **M7** (METRICS.md): hit rate ≥ 90%, reuse factor ≥ 1.5, dedup ratio ≥ 0.4 on the
  deterministic repetition protocol; non-ID arms scored N/A with justification.
- **The taught-word lifecycle** (§B.5/§B.6, installed-vs-learned ruling 2026-09-21):
  taught words arrive **judgment-held at provisional strength**, are revisable by
  the learner's own deliberation always, and only a visible audited force-pin makes
  anything immutable.

## Non-goals

- No ID-scheme decision (K vs L vs counter is the bake-off's job).
- No change to M7's frozen bars; the taught-word extensions below are new,
  PROPOSED sub-metrics.
- No eviction-policy fiat beyond the safety invariant (§5).
- No treatment of the near-duplicate hole (spans differing by one byte share
  nothing under K) — acknowledged in the K-vs-L analysis as future
  similarity-addressed work; not solved here.

## 1. What gets cached: the taught-word cache entry

When a taught word reaches ADOPT (or REVISE — a revised word is still a taught
word, with learner-modified span), the cache admits one entry:

```
CACHE_ENTRY {
  id:            ChunkID            // per the arm's scheme (K/L/counter)
  content_ref:  bytes | content_hash // the span's bytes, or hash for K
  provenance:   { teacher_id, proposal_seq, session_id, confidence,
                  verdict: ADOPT|REVISE, ledger_entry_index }
  strength:     provisional | judged_promoted   // §F/T-1 ladder position
  rev_links:    [ (old_id -> this_id, reason_code, ledger_index) ]  // §4
  refcount:     u64                // memories currently pointing at this id
  pinned:       bool               // force-pin state; visible, audited
}
```

Two properties are load-bearing for everything below:

1. **The stimulus tape is the ground-truth backing store.** TST-1 tapes are
   harness-owned, append-only, and byte-identical on replay. Cache payload bytes can
   therefore be evicted aggressively — they are always re-derivable from
   (stimulus_tape_id, byte_range). What must never be evicted while referenced is
   the **ID → provenance record**: the mapping from a stable handle to *what it
   was and who taught it*. Bytes are recoverable; provenance is not.
2. **Provenance rides with the ID.** A taught word's cache entry is not just
   bytes — it carries the teacher, the proposal seq, the confidence, and the
   verdict. This is what makes the cache auditable ("who taught you that word?")
   and what lets the §C census (ATTACK_CATALOG.md P-A3) read the cache as its
   input rather than re-scanning tapes.

## 2. ID issuance at ADOPT, per scheme

The learner's ADOPT path does a **dedup lookup before issuing an ID**:

- **K (content-addressed):** `id = HASH(span_bytes)` (frozen hash choice is a
  sign-off item; the R33-native SHA-256 substrate exists). Dedup is structural:
  identical bytes → identical ID, across sessions, for free. The lookup *is* the
  hash.
- **L (position-addressed):** `id = (session_id, base_offset, len)`. Same bytes at
  a new position → new ID. Cross-session dedup needs a **sidecar content index**:
  `content_hash → [ids]`, consulted at ADOPT; on a hit, the new memory links to
  the *existing* ID (or records an alias — sign-off item) instead of minting a
  duplicate entry.
- **Counter:** `id = next_serial++`. Same as L: dedup requires the sidecar table
  `content_hash → id`, consulted before minting.

**Lookup path (all schemes):** normalize the adopted span's bytes → content hash →
probe dedup table → **hit:** link the new memory to the existing ID (`refcount++`,
`reuse++`, no new payload stored; the re-teach is logged with its own provenance
— see §6) → **miss:** issue a fresh ID per the scheme, store payload + provenance.

Note the honest cost: under L and counter schemes the dedup table is extra
state the bake-off must charge to the scheme (it counts toward `store_cost` in
the K-vs-L discriminating experiment). K pays the hash on every ADOPT instead.
No free lunch; the experiment prices it.

## 3. Dedup across sessions

Sessions are the natural fragmentation boundary: each session has its own
stimulus slice and its own `session_id`. Without cross-session dedup, re-teaching
"quark" in session 9 mints a second entry — teaching becomes enumeration (the
K-vs-L analysis already calls this out as L's failure mode for taught vocabulary).

- The **dedup table is per-learner, cross-session, persistent**: keyed by content
  hash → ID, with a **provenance chain** per ID: first-taught session, re-teach
  count, and the list of (teacher_id, session_id, confidence) for each re-teach.
- **Re-teach semantics:** a re-teach that dedups to an existing ID is *not* a new
  word — it's corroborating evidence for the existing entry (weight it per the
  source-reliability thinking in R23_LESSONS.md T3, don't just count it). The
  learner's deliberation sees "teacher 3 re-taught ID h at conf 200 in session 9"
  as evidence about an existing belief, not a new proposal to adopt.
- **Open sign-off item:** is the dedup table shared *across learners* (peer
  teaching by ID — "do you have h? I do, here's its provenance") or per-learner?
  Cross-learner sharing is the primitive for every multi-instance future
  (CORE/USER sharing, user-trained instances), but it couples learners'
  vocabularies in ways the prereg hasn't approved. Flagged, not decided.

## 4. Invalidation when a word is revised

Taught words are revisable **by law** (installed-vs-learned ruling; only a
force-pin blocks revision, and it's visible). REVISE changes the span
(SPAN_SHIFT/SPLIT/MERGE/GENERALIZE/NARROW) — the cached content is now wrong.
The invalidation protocol, per scheme:

- **K:** new bytes → new ID, structurally. Write a **REVISION link record**:
  `old_id → new_id` with the §L reason_code and the ledger index of the revising
  op. The old entry is *not* deleted — it's tombstoned-with-a-forwarding-address.
  Readers holding `old_id` resolve through the link chain (bounded depth —
  PROPOSED cap 8, sign-off item; exceeding the cap is an `INTEGRITY`-class event,
  not silent truncation).
- **L:** the position ID is stable; update the content in place **and** write the
  revision as an audit entry (the ID now names revised content — the audit trail
  is what makes this honest rather than Orwellian). No link chain needed; the
  entry's `rev_links` log the content history.
- **Counter:** version bump — `(serial, gen+1)`; the old `(serial, gen)` entry
  keeps a forward link like K.

**Stale-reader rule:** a memory referencing a revised ID must resolve to the new
content *through the audited link*, never silently keep reading old bytes, and
never crash on a dangling ID. The revision link is what distinguishes "the word
changed" from "the word vanished." This is also where the cache earns its
auditability: the complete judgment history of any taught word (taught → revised →
revised again) is walkable from the ledger alone.

**Interaction with strength:** revision does not change strength by itself
(strength is judgment-set, never formulaic — standing law). A revised word keeps
its ladder position; promotion/demotion remain deliberate acts.

## 5. The safety invariant (eviction)

The cache is not infinite, so eviction exists — but one invariant is non-negotiable:

> **An ID → provenance record MUST NOT be evicted while `refcount > 0`.**
> Payload bytes may be evicted freely (re-derivable from the stimulus tape);
> the ID, its provenance, and its revision links are pinned by reference count.

Rationale: memories point *at IDs*. Evicting the record an ID names while a
memory still holds the ID creates dangling references — the one failure this
layer is not allowed to have. When `refcount` drops to 0 (all referencing
memories killed/revised away), the full entry becomes evictable under the arm's
normal policy (sign-off item). Eviction itself is audited (one ledger entry per
evicted payload batch, not per byte — cost sanity).

## 6. Cache-hit scoring as a future metric (PROPOSED — extends M7, changes nothing frozen)

M7 measures hit/reuse/dedup for ID arms generally. Taught vocabulary deserves
sub-cells, because a cache that dedups emergent chunks but re-ingests every taught
word is failing at exactly the thing Track B is for:

- **M7-T1 — taught-hit rate (PROPOSED):** retrievals of taught words served from
  the ID→content mapping without re-ingest, over a fixed deterministic retrieval
  schedule drawn *only* from taught IDs (mirroring M7's 5,000-lookup schedule).
  Definitionally parallel to M7's hit rate; the schedule construction is a
  sign-off item.
- **M7-T2 — cross-session taught reuse factor (PROPOSED):** total references to
  taught IDs ÷ distinct taught IDs live, measured across a multi-session battery
  with deliberate re-teaching. This is the metric that punishes
  teaching-as-enumeration: an L-scheme arm with no sidecar dedup scores ~1.0 here.
- **M7-T3 — revision-link integrity (PROPOSED):** fraction of revised taught words
  whose revision chains resolve within the depth cap with no dangling IDs, over a
  battery with preregistered learner-initiated revisions. A cache layer that
  corrupts on the first REVISE fails the taught track's reason for existing
  (revisability is 25% of the verdict weights).
- **M7-T4 — teacher-dedup ratio (PROPOSED):** re-teaches of the same word across
  sessions that resolve to the existing ID ÷ total re-teaches. Distinguishes "the
  cache recognized the word" from "the cache stored it twice."

Bars for M7-T1…T4 are **deliberately not proposed here** — they need the same
bake-off treatment as M7's own bars (measure first, bar second). The metric
*definitions* are the proposal; the numbers are sign-off items. M7's
N/A-with-justification rule applies unchanged: non-ID arms are not punished for
lacking a cache.

## 7. Adversarial angle: the cache must not become a smuggling channel

Two threats, both with existing hooks:

- **Slow-drip vocabulary building (ATTACK_CATALOG.md A3).** A teacher that drips a
  fixed tiling across sessions builds a "clean" cached vocabulary — every entry
  individually legitimate-looking. Defense: the §C cross-session census (P-A3)
  reads the cache's provenance chains as its input — the cache *feeds* the
  detector rather than hiding from it. Cache admission from teacher proposals is
  therefore census-visible by construction (§1, property 2). A cache layer that
  laundered provenance would defeat P-A3; this sketch refuses that design.
- **Position-addressed spoofing (K-vs-L analysis).** Under L, spoofed bytes at a
  trusted position keep the trusted ID — the red team attacks there. Cache
  entries under L/counter schemes therefore store the **content hash alongside
  the ID** and verify-on-read: a hit is either *verified* (bytes match the
  recorded hash) or *trusted* (position-only, unverified). Verified vs trusted
  hits are reported separately — under adversarial input the distinction is the
  whole game, and a "hit rate" that conflates them is a lie.

## 8. What this sketch assumes vs. what it leaves open

**Assumes (inherited, not decided here):** TST-1 tapes are append-only and
replayable (backing store); taught words are judgment-held and revisable;
force-pin is visible and audited; M7's definitions of hit/reuse/dedup.

**Leaves open for sign-off:** hash choice for K; link-depth cap; eviction policy
beyond the §5 invariant; cross-learner dedup-table sharing; M7-T bars; alias vs
re-link semantics on L/counter dedup hits; whether the census (P-A3) lives in the
harness or the cache layer (this sketch assumes harness, cache feeds it).

## 9. Relationship to the D-vs-U battleground

This sketch is arm D's natural implementation — and it is written knowing arm U
exists. Every piece of state above (dedup table, sidecar index, link chains,
refcounts) is a cost U doesn't pay; the D-vs-U total-cost comparison
(`cpu_ops + λ·resident_bytes·queries + μ·rekey_bytes`) prices exactly this.
If the crossover analysis shows U winning at realistic churn, this sketch is
refuted as architecture and survives only as an optional optimization — which is
the honest outcome, and the sketch is built to accept it: nothing here claims
caching is necessary, only what it would look like if it pays.
