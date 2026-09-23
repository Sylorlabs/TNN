# EXPLORATORY — NOT EVIDENCE

**WIDE EXPLORATION track — CACHE LAYER: INVALIDATION-ON-REVISION + ID STABILITY**
Date: 2026-09-21. Worker: wide-exploration subagent.

This document is **exploratory and NON-BINDING**. It is not program evidence. It proposes
nothing into the frozen program. The prereg (`docs/lab/units/PREREG_FREEZE.md`, Micah-signed
2026-09-21 per tasking) is FROZEN: no bar, metric, or kill criterion is changed,
reinterpreted, or softened anywhere below. **No design in this file may enter the program
without a dated amendment proposal signed by Micah** — stated per design below.

**Hard laws every sketch below obeys (inherited, not negotiable):** pure Zag; ZERO
randomness in any AI decision path; byte-identical reruns from (input + full logged state);
real mechanisms, no stubs as headline evidence; no binaries, no `.zagd`, no `.zag-cache`
in this work. Zag conventions from `~/AGENTS.md` honored throughout: no slice `==`
(integer compares only), large-struct array fields aliased to locals before indexing,
`_zag_strcmp` returns 1 on equality, `_zag_arg(n)` never freed, 16-word audit layout
(op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, **stage@52, d1@56, d2@60**), no single
slice over 2^25 bytes, `@import` bare.

**Sources studied:** `ALPHABET_G-L.md` (K-vs-L bake-off, arms K1/K2/K3/L1/L2, §comparison),
`RISKS.md` R3 (stable IDs under heavy revision), `ARCHAEOLOGY_R31.md` (split/merge
dynamics), `METRICS.md` M4 (revision success) and M7 (ID-layer cache metrics),
`ALPHABET_S-X.md` (U-vs-D invalidation head-to-head), `ALPHABET_Y-Z.md` (Y3 versioned IDs,
Y6 tombstone-native IDs, Z5 recipe IDs), `PREREG_FREEZE.md` §3/§7/§8.

**Documentation inconsistency (flagged for the parent, not a finding):** the on-disk
`PREREG_FREEZE.md` still carries the header "Status: PROPOSED — NOT FROZEN. Nothing in
this document is approved." My tasking states Micah signed 2026-09-21 and the prereg is
FROZEN. I proceed on the tasking's authority and treat every bar below as frozen; the
header/body mismatch should be reconciled by whoever owns the freeze commit.

## §0 — The problem, crisply

The catalog answers "what is the ID" (K: what, L: where, M: issuance order, Y3: serial +
lineage, Z5: recipe). It does **not** answer the cache question: **when the bytes change,
who tells the cache, and what survives?** That is invalidation-on-revision, and it is
where every identity scheme either earns its keep or rots:

- A memory op (pin, promote, kill, recall) names an ID. After a revision, does that name
  still mean what the op meant when it was issued?
- The audit ledger must prove the answer either way — silently changing what an ID names
  is the R5 violation (silent corruption), and a name that points at nothing is the R3
  violation (ghost IDs).

**Frozen touchpoints (inventory — nothing here is altered):**
- **M4 revision success:** 100 boundary + 100 content defects per corpus; bar revision ≥
  80% per class; REVISED = wrong→right **with ID/lineage continuity** ("same ID, audit
  shows a revise/repair entry — not a kill+re-add, which is a new unit wearing the old
  ID"); 20 revision episodes max; KILL-SUBSTITUTION (kill > 50% + revision below bar →
  M4 = 0); whole-corpus re-ingest invalidates the run.
- **U-vs-D head-to-head kill rule (ii):** D-with-invalidation dies if it loses to U on
  total cost **including 100 mid-stream byte edits** — the literal "100 mid-stream edits"
  in the frozen record.
- **K-vs-L bake-off:** condition (c) = 100-patch corpus-C series; metric `ref_stability` =
  fraction of pre-revision references whose ID is unchanged after each patch batch; L's
  bar = **100%** (any change = eternity violated = L dies); hybrid-promotion rule (K3
  beats both on ≥3/5 metrics → pure schemes demoted to components).
- **R3 5,000-edit storm:** bar = **zero ghosts**, tombstone/live ratio < 2, counted on a
  100KB sqlite3.c slice with 5,000 deterministic scripted edits. Any ghost = memory-
  integrity violation; the wave-5/6 integrity story does not survive it.
- **Y3:** lineage depth > 50 kills; any recall resolving to a tombstoned span kills.
- **D (flagship):** "tombstoned IDs never reused."
- **M7 (ID arms):** hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4 (rounds 1–2; round 3 with edits
  reported, not barred — "edits legitimately create new content").
- **M1 swap probe:** N=64 deterministic ID→content remaps; recall must go through the ID
  layer end-to-end or fail loudly; side-channel bypass → metric scored 0.

Note: **no single frozen item carries the exact wording "100 mid-stream edits; ≥80% ID
stability."** §6 maps that phrasing onto the frozen items above and tests whether it
survives as a scheme-neutral bar. (Spoiler: it does not — the amendment proposal is in
§7.)

---

## §1 — Revision semantics, Design A: IMMUTABLE-VERSIONED IDs (the git design)

**Rule:** an ID names an exact byte content, forever. Revision never mutates a record; it
**mints a new ID** and links it. This is arm K1/K2 as specified ("a revised chunk's
content hashes differently, so its identity dies by definition — this is honest, not a
bug") plus Y3's lineage machinery made explicit.

### Data structures (pure-Zag sketch)

```zag
@import("cl/common.zag")   // bare import: native sha256 + io (AGENTS.md lesson)

struct ChunkRec {
    id:     [4]u64,   // content hash quad (K1) — compared as 4 integer words, never slice ==
    slot:   i32,      // store slot
    state:  u8,       // 0=live, 1=tombstoned
    refs:   u32,      // live reference count (memory ops holding this ID)
    head:   i32,      // slot of current lineage head, -1 = self is head
    prev:   i32,      // slot of previous version in this lineage, -1 = birth
    ver:    u32,      // lineage depth from birth ID
    pinned: u8,       // force-pin immune (program law)
}

// Revision: old bytes B -> new bytes B'. ID(old) is NEVER edited.
fn revise(rec: *ChunkRec, new_bytes: []u8, reason: u32, cite_ep: u32, s: *Store) -> i32 {
    let h: [4]u64 = sha256_quad(new_bytes);          // native, deterministic
    let slot: i32 = 0;
    st_add(s, &slot);                                 // out-slot pattern
    let r: *ChunkRec = &s.recs[slot];                 // alias before field indexing
    r.*.id    = h;                                    // struct-assign of fixed array: fine
    r.*.state = 0;  r.*.refs = 0;  r.*.pinned = 0;
    r.*.prev  = rec_slot(rec);  r.*.ver = rec.*.ver + 1;
    r.*.head  = slot;
    // old record: tombstone + forward link (append-only; history never rewritten)
    audit(OP_TOMBSTONE, rec_slot(rec), reason, cite_ep);       // d1 = new slot
    audit(OP_REVISE_LINK, rec_slot(rec), 0, cite_ep);          // b1..b4 = old hash quad,
                                                              // d1 = new slot, d2 = ver
    rec.*.state = 1;  rec.*.head = slot;
    ret slot;
}
```

Opcode numbers are NOT assigned here — A-3 (opcode namespace unification) owns that;
`OP_TOMBSTONE` / `OP_REVISE_LINK` are names pending unification.

### Consequences, worked fully

- **Memory ops.** Pin/promote/kill/recall name IDs. After a revision the named ID is
  tombstoned. Two sub-designs, both deterministic: (A-i) *sticky references* — the op
  follows `head` to the live version (recall always serves current bytes; a pin on the
  old ID pins the lineage, forwarded); (A-ii) *exact references* — the op addresses the
  exact version named (recall of an old ID returns old bytes with a `stale=1` audit note,
  or fails loudly if the policy says references must be current). The catalog's arms
  implicitly choose: K1's "recall follows revision links (append-only chain) to the live
  ID" is (A-i); Y3's "never dangles" with explicit version lineage supports (A-ii). **The
  choice must be preregistered per arm** — mixing them inside one run is silent
  corruption by another name (the same ID resolving two ways depending on caller).
- **Audit trail.** Every revision is 2 entries (tombstone + link); the chain is
  append-only and walkable from any historical ID to the live head. Provenance is
  *structural*: you cannot rewrite history because old records are never mutated. Cost:
  O(depth) entries per lineage; Y3's kill bar (mean depth > 50) is the fragmentation
  tripwire, and K1's churn-swamp bar (chain > 8 AND latency > 2×) is the latency
  tripwire. Both already frozen — Design A lives or dies by them.
- **Recall.** Resolution = walk `prev`/`head` pointers to the live record, then serve
  bytes. Worst case O(depth); the catalog flags compaction as "deliberate audited op,
  future work." Prediction P1 (§8) prices this on the 100-patch series.
- **Integrity win.** Tampering is *visible by construction*: changed bytes = changed ID
  = new record + link. This is why K beats L on the sensor-spoofing row of the
  comparison table — under Design A there is no such thing as "same ID, different
  bytes," so silent drift (ghost clause G3, §5) is structurally impossible. The price is
  paid in chain-walking and ID turnover.
- **Failure mode.** Reference-following cost grows with edit count (K1's predicted
  weakness, stated in the arm). Near-duplicate spans share nothing (catalog's known
  hole). ID turnover means any external system caching IDs (the peer teacher, the
  TST tapes) must speak lineage, not IDs — a cross-arm interface cost the catalog does
  not yet price.

---

## §2 — Revision semantics, Design B: MUTABLE-STABLE IDs with version chains

**Rule:** an ID is a **handle minted at birth** that names a *role/position*, not bytes.
Revision mutates the *current version pointer* under the handle; the handle never dies
from a content change. This is L1/L2 ("position p keeps its ID forever, even as its
bytes change") and arm D's stable-ID line, generalized with Y3-style versions.

### Data structures (pure-Zag sketch)

```zag
struct HandleRec {
    hid:    u64,      // birth-minted handle: monotonic counter, never reused
    cur:    i32,      // slot of current version payload, -1 = none
    vers:   []u32,    // version slots, index = version number (striped, ≤2^25)
    nver:   u32,
    state:  u8,       // 0=live, 1=tombstoned (kill is deliberate, never a side effect)
    refs:   u32,
    pinned: u8,
}
struct Payload {
    hash: [4]u64,     // content fingerprint of THIS version (integrity anchor)
    seg:  u32, off: u32, len: u32,   // byte span in the append-only store
}

fn revise_b(h: *HandleRec, p: Payload, reason: u32, cite_ep: u32, s: *Store) {
    // The handle is NOT edited except cur/nver. The mutation is a *versioned*,
    // audited event — never a silent overwrite.
    let v: i32 = alloc_payload(s, p);
    audit(OP_REVISE, h.*.hid, reason, cite_ep);   // d1 = old cur slot, d2 = new slot;
                                                 // b1..b4 = new payload hash quad
    let vs: []u32 = h.*.vers;                     // alias before indexing (Zag gotcha)
    vs[h.*.nver] = v as u32;
    h.*.nver = h.*.nver + 1;
    h.*.cur  = v;
}
```

### Consequences, worked fully

- **Memory ops.** Trivially stable: pin/promote/kill/recall name the handle and always
  reach *something*. The danger is the mirror image of Design A's: the name is stable
  but its *meaning drifts*. Every op must therefore answer "which version?" — default =
  head (current), with explicit `(handle, version)` addressing available. A recall that
  silently serves v3 when the caller pinned v1 is the Design-B analogue of a ghost
  (clause G3, §5).
- **Audit trail.** The revise entry must carry old→new payload fingerprints (there is
  room: b1..b4 for the new hash, d1/d2 for slots; the old hash is recoverable from the
  old payload record). Without both fingerprints the entry cannot prove *what changed* —
  and an entry that cannot prove what changed is a silent overwrite with paperwork. The
  ledger stays append-only; versions are never mutated after commit.
- **Recall.** O(1) to the current version (handle → cur slot). History is O(1) per
  version by index. No chain-walking — this is Design B's structural advantage, and the
  reason L1 predicts the fastest sequential recall.
- **Integrity price.** Content identity is *not* structural here; it is *procedural* —
  it holds only if every byte change goes through `revise_b` with its audit entry. A
  single write path that mutates a payload in place breaks the scheme silently. The M1
  swap probe is the detector: patch the handle table to point at wrong slots; recall
  must fail loudly or label honestly. Under Design B the probe must additionally cover
  **version confusion** (handle → stale `cur`), which the current probe text does not
  name — candidate for the §7 amendment's probe extension.
- **Failure mode.** The R3 threat note names it: "L (position IDs die on insert — this
  risk is L's predicted cause of death)." The arm spec answers with sealed segments +
  revision map, but the *meaning-drift* risk has no arm-level tripwire today: a handle
  whose bytes changed 500 times still "succeeds" every recall while naming something
  unrecognizable. Y3's lineage-depth bar (> 50 kills) is the closest existing tripwire
  and should be read as covering version count under Design B as well — proposed in §7.

### The honest comparison

| | Design A: immutable-versioned | Design B: mutable-stable handle |
|---|---|---|
| What the ID names | exact bytes, forever | a role/position, across versions |
| Revision cost | 1 new record + 2 audit entries; old ID dies | 1 version slot + 1 audit entry; handle lives |
| Recall cost | O(lineage depth) chain walk | O(1) to head version |
| Memory-op stability | ops must follow `head` (policy choice) | ops never dangle by construction |
| Silent-corruption surface | ~none (structural) | every non-`revise_b` write path; version confusion |
| History | walk `prev` links | index `vers[]` |
| Dedup | free (identical bytes = identical ID) | must be built separately (payload table) |
| Frozen-bar fit | breaks literal M4 "same ID" reading (§6–7) | fits M4 naturally; L's 100% bar is native |
| Kill tripwires | Y3 depth > 50; K1 chain > 8 + 2× latency | L eternity (any change = death); Y6 ledger 10× |

Neither dominates. The catalog's K-vs-L table already says so; this section says *why*
at the mechanism level: **A buys integrity structurally and pays in chains; B buys
stability structurally and pays in drift-policing.**

---

## §3 — What the cache actually invalidates (the cache-layer reading)

This track is the *cache layer*. Under each design, "invalidation-on-revision" means
something different, and only one of them is what the word "invalidation" normally
means:

- **Design A has no invalidation.** There is nothing to invalidate: the old cache entry
  (old ID → bytes) remains *true forever* — those bytes are still those bytes. Revision
  *tombstones* the entry and *links* to the new one. The cache is append-only with a
  live-head pointer. "Stale cache" is impossible; "dangling cache" is the ghost problem
  (§5). Arm U (recompute-on-demand) is the degenerate case: with no stored chunks there
  is nothing to invalidate either — U's B5 blast radius is 0 *by construction*, which is
  exactly why the U-vs-D head-to-head is the fair fight over whether caching pays.
- **Design B has true invalidation.** The cache entry (handle → bytes) becomes *false*
  on revision. Invalidation = bump `cur` + exactly one audited `OP_REVISE`. Three
  sub-rules, all load-bearing: (i) **write-through with tombstone-of-version** — the old
  version payload is never mutated, only superseded; (ii) **read-your-revision** — a
  recall carrying an explicit old `(handle, version)` gets old bytes, loudly labeled
  stale, never silently; (iii) **no silent overwrite** — any byte change without a
  revise/repair audit entry is corruption, caught by R5's round-trip torture (10,000
  chunks × 100 recalls interleaved with kills/revisions, zero mismatches tolerated).
- **The composite (K3's decomposition, already in the catalog):** the *handle* is what
  memory caches (stable, Design B); the *payload* is content-addressed and immutable
  (Design A). Invalidation then has two clean halves: the handle's `cur` pointer moves
  (cheap, O(1)), and the new payload *dedups for free* against the content table — "an
  edited span that now matches another span merges for free" (ALPHABET_G-L.md, K3). This
  is the only design where invalidation is both cheap and integrity-structural. It is
  also, notably, exactly what the frozen hybrid-promotion rule is waiting to crown *if
  it wins the bake-off* — not before (RULE-2, RULE-6).

---

## §4 — Split/merge under each scheme: exact rules

R31's dynamics (ARCHAEOLOGY_R31.md): **split** fires iff `use_count ≥ 3 AND conflict ≥
learned_conflict AND utility ≤ learned_utility_floor`; **merge** fires iff `pair_seen ≥
learned_pair_seen AND joint_gain − separate_regret ≥ learned_gain`. "Chunk boundaries
are mutable hypotheses." The ID layer must turn each firing into deterministic record
ops. The rules below are per-scheme; the *trigger conditions* are identical (they belong
to the cut layer, not the cache layer).

### Design A (immutable)

- **S-A1 (split):** `split(P → C1..Cn)`: P is tombstoned (`OP_TOMBSTONE`, citing the
  split episode); each Ci is minted as a **new ID** (hash of its bytes); one `OP_SPLIT`
  entry records `(P → [Ci], reason, cite_ep)` with the cut points in a1..a5. P's
  revision history is preserved via its `prev` chain — nothing is rewritten.
- **S-A2 (merge):** `merge(C1..Cn → P)`: P is a **new ID**. Children policy is
  orthogonal and preregistered per arm: *absorptive* (G1 triage: `kill(left)+kill(right)`)
  → children tombstoned; *compositional* (I1 superchunk: `OP_SUPER_ADD` + parent links)
  → children stay live with backlinks. The merge entry records which policy applied.
- **S-A3 (the hard rule):** a parent ID **never survives** a split or merge. Under
  Design A it *cannot* — the bytes changed, so the hash changed. Lineage continuity is
  link-based (`OP_SPLIT`/`OP_MERGE` entries), never ID-equality-based. Any test that
  checks "did the parent ID survive" is testing the wrong observable under this design
  (see §6).

### Design B (stable handles)

- **S-B1 (split):** `split(P → C1..Cn)`: P is **retired** (tombstoned with
  reason=SPLIT, children listed in the entry); each Ci gets a **new handle**. Rationale:
  P named *the whole*; assigning P's handle to one child silently redefines what P
  names — the "which twin is the original" problem. Retire-always is the default
  because it keeps every handle's meaning monotonic: a handle never names *less* than
  it did at birth without an audited event saying so, and never names *different*
  bytes under the same version.
- **S-B1′ (the test-both leg, not the default):** *eldest-child-inherits* — the child
  covering P's lowest offset keeps P's handle, others are minted new. Cheaper on
  handle churn; dishonest unless the inherit entry documents the redefinition.
  Prediction P5 (§8) prices the dishonesty. Per RULE-2 both legs run; the default
  recommendation is S-B1.
- **S-B2 (merge):** new parent handle minted; children kept (compositional) or
  tombstoned (absorptive), same orthogonal policy as S-A2. The parent handle is new
  because "the fusion" is a new role — reusing a child's handle for the parent would be
  the merge-direction version of the twin problem.
- **S-B3 (revision without re-cut):** handle unchanged, version bumped, `OP_REVISE`
  with old→new fingerprints (§2). This is the *only* op under which a handle's bytes
  change — everything else mints or retires.

### Mapping the R31 redo bar B-T5

B-T5 requires "a recruited chunk split then re-merged on the record." Under the rules
above the ledger for a null-edit split→re-merge looks like:

```
ADD(P) … SPLIT(P → C1, C2, reason=CONFLICT_SPLIT) … MERGE(C1, C2 → P′, reason=GAIN_MERGE)
```

with **P′ ≠ P under both designs** (new hash under A; new handle under B). The
"re-merged" claim is therefore a claim about **bytes and lineage, not ID equality**: the
audit must show `bytes(P′) == bytes(P)` (verifiable from the payload records) and the
lineage `P → {C1,C2} → P′` unbroken. A checker that diffs ID lists across episodes and
cries "instability" at P→P′ is mismeasuring — §6's amendment proposes the correct
observable. Under S-B1′ (inherit leg) P′ would equal P's handle for the eldest child,
which is precisely why that leg is suspect: it *looks* stable while redefining meaning.

### Interaction with frozen arms (read-only notes, no changes)

- **I1 superchunks** are compositional merges with own IDs — consistent with S-A2/S-B2
  under either design; the child-survives policy is already in the arm text.
- **G1 triage merges** are absorptive — children die; the OP_MERGE record "stores both
  cut points, so a later deliberate re-split is byte-exact" — consistent with S-A2's
  audit requirements.
- **Z6 scar IDs** bind `(ledger_seq_of_forming_revision, span)` — scar-bound IDs are
  Design-A-like (ledger seqs are immutable) and revision-proof by construction; a scar
  chunk that gets re-cut mints a new scar ID. Consistent with S-A1.
- **Z5 recipe IDs** are Design-B-like with a program as the handle: the recipe is
  stable, the derived span moves. "Stability" for Z5 means *recipe* stability, which is
  yet a third observable — more evidence that one "ID stability" number cannot cover
  the catalog (§6).

---

## §5 — Ghost IDs: definition, reclamation, and the R3 storm

### Precise definition

An ID is a **GHOST** iff it is flagged **LIVE** in the ID table and at least one of:

- **(G1) dangling record** — its record slot is dead/tombstoned, or the slot holds a
  different ID's record (use-after-tombstone);
- **(G2) dangling lineage** — its revision chain's head is tombstoned, or the chain is
  broken (a `prev`/`head` pointer names a slot that was reclaimed or never existed);
- **(G3) silent drift** — the bytes it resolves to no longer match the content
  fingerprint recorded at its birth (Design A) or at its current version (Design B),
  **and** no audited revise/repair entry covers the delta. G3 is the R5 violation in
  ID clothing.

Notes: a *tombstoned* ID pointing at dead content is not a ghost — it is a corpse with
a death certificate, which is the honest state. A *live* ID whose content changed
*with* an audited revise entry is not a ghost either — it is a revision. Ghosthood is
precisely **"live-flagged but unresolvable-or-lying."** Under Design A, G3 is
structurally impossible (bytes are the ID); under Design B, G3 is the load-bearing
risk and the M1 swap probe is its detector.

### The deterministic reclamation rule

Reclamation is **episodic mark-sweep**, not per-op refcounting. Rationale: Y6's frozen
kill bar (ledger write volume > 10× D's → kill or batched REF) already prices per-op
refcount writes as potentially unaffordable; a sweep at preregistered episode
boundaries keeps ledger cost O(table) per sweep instead of O(ops).

```
SWEEP (runs only at frozen sweep episodes E_sweep — never mid-stream):
  for each record R in ID table (slot order — deterministic):
    eligible = (R.refs == 0)
           AND (R.pinned == 0)
           AND (R not reachable as a revision-chain head from any live ID)
           AND (R.state == live)
           AND (R not in the protected recent window [E_now - W_protect, E_now])
    // W_protect frozen: a newborn ID is never swept in its birth window,
    // so sweep timing cannot race issuance. Deterministic, no heuristics.
    if eligible:
        audit(OP_TOMBSTONE, R.slot, reason=RECLAIM_SWEEP, cite_ep=E_now)
        R.state = tombstoned
  // Post-sweep invariant check (the ghost detector):
  for each record R with R.state == live:
    assert_resolves(R)  // G1: slot alive; G2: head chain intact; G3: fingerprint match
                        // or covering revise entry. Failure = LOUD HALT + audit entry.
                        // A ghost is a memory-integrity violation, never a cleanup event.
```

```zag
fn sweep_reclaim(s: *Store, e_now: u32, w_protect: u32) {
    let n: i32 = s.nrecs;
    let i: i32 = 0;
    while (i < n) {
        let r: *ChunkRec = &s.recs[i];       // alias before field indexing
        if (r.*.state == 0 and r.*.refs == 0 and r.*.pinned == 0) {
            if (r.*.birth_ep + w_protect < e_now and not_chain_head(s, i)) {
                audit(OP_TOMBSTONE, i, RECLAIM_SWEEP, e_now);
                r.*.state = 1;
            }
        }
        i = i + 1;
    }
    // ghost detector: every live record must resolve
    i = 0;
    while (i < n) {
        let r: *ChunkRec = &s.recs[i];
        if (r.*.state == 0) { cl_check(s, ghost_free(s, i)); }  // loud on violation
        i = i + 1;
    }
}
```

**Five hard properties of the rule:**
1. **Tombstones are never reused** — D's frozen rule, extended to swept IDs. The ID
   value space is monotonic; reuse would resurrect names with stale external
   references (the peer teacher's TST tapes, the T2/T3 corpora indices).
2. **Sweep timing is frozen**, not adaptive — adaptive sweeping would make reclamation
   a function of load, and load is not logged state; byte-identical reruns (M8) require
   the sweep schedule in the prereg.
3. **Ghosts halt, they don't get swept.** Reclamation disposes of *unreferenced live*
   records; a ghost is *referenced-but-lying*, which is evidence of a mechanism bug.
   Sweeping a ghost would destroy the evidence.
4. **Pinned IDs are immune**, including force-pins (program law) — the sweep asserts
   this rather than assuming it.
5. **The protected window W_protect** prevents sweep/issuance races deterministically.
   (Without it, an ID born one op before a sweep could be reclaimed while its first
   reference is still being audited — a deterministic but wrong outcome.)

### Connection to R3's 5,000-edit storm bar

R3's bar is **final-state**: after 5,000 deterministic scripted edits on a 100KB
sqlite3.c slice — zero ghosts, tombstone/live < 2. The rule above is designed to pass
it: every edit's dead records are either linked (revision chains, counted as
tombstoned) or swept (unreferenced), and the ghost detector runs at every sweep, so a
mid-storm ghost halts loudly rather than hiding until the final audit.

**Gap the bar leaves (→ §7 amendment proposal, not a change):** a mechanism could ghost
mid-storm and clean up before the final count — passing the letter, violating the
spirit. The M1 swap probe already establishes the precedent that *mid-trial* integrity
checks are legitimate. The proposal: run the ghost detector (the `assert_resolves`
loop) at every sweep episode during the storm and log the result; any mid-storm ghost
= trial failure, same as a final-state ghost. This strengthens R3 without moving its
numbers.

---

## §6 — The revision test: is "≥80% ID stability" well-defined?

### What the catalog actually froze

The task's phrasing — "the revision test from the catalog (100 mid-stream edits; ≥80%
ID stability)" — does not match any single frozen item verbatim. The nearest frozen
items:

| Frozen item | "100 edits" | "≥80%" | What it actually measures |
|---|---|---|---|
| M4 revision success | 100 boundary + 100 content defects per corpus | revision rate ≥ 80% **per defect class** | wrong→right repair **with ID/lineage continuity** |
| U-vs-D kill rule (ii) | **100 mid-stream byte edits** | — (cost comparison, no %) | total cost incl. invalidation vs recompute |
| K-vs-L `ref_stability` | 100-patch corpus-C series | L's bar = **100%** (any change = death) | fraction of pre-revision references with unchanged ID |
| R3 storm | 5,000 scripted edits | zero ghosts (not a %) | ID-table integrity under churn |

The task's phrasing is closest to **M4's ≥80% fused with the K-vs-L `ref_stability`
concept** — "after ~100 edits, what fraction of IDs are stable." Analyzed as a
*scheme-neutral* bar, it fails. Here is the case, per scheme:

- **Design A (K1/K2 immutable):** "ID stability across a revision" is 0% **by
  definition** — the arm text says identity "dies by definition" on revision. A bar
  demanding ≥80% identifier bit-equality after 100 content edits does not measure
  quality; it measures *whether the arm chose Design A*. K1 would score 0% while
  performing perfect, fully-audited, lineage-clean revisions. The bar is not hard — it
  is **incoherent for this design**. What *is* well-defined for A is *lineage
  resolvability*: fraction of pre-edit references that resolve via audited links to a
  live head. (M7 already accepts the analogous formulation: versioned arms may "mark
  new versions linked to the old ID — either is acceptable if declared and audited.")
- **Design B-stable (L1/L2):** "ID stability" is 100% **by construction** — eternity is
  the promise, and the frozen kill rule already demands exactly 100% ("any revision
  batch changes an existing position ID → L dies outright"). A ≥80% bar for L is a
  tautology that *weakens* the frozen 100% bar. It must not replace it (RULE-7, RULE-9).
- **K3 hybrid:** the ID has two halves — content hash (0% stable across edits, by
  design) and position (100% stable, by design). "ID stability" is ambiguous until you
  say *which half*. The composite needs two numbers, and the bake-off's five metrics
  already split them (`dedup_ratio` for the content half, `ref_stability` for the
  position half).
- **Z5 recipe:** stability means *recipe* stability — a third observable again.

**Verdict on the phrasing:** as a single scheme-neutral bar, "≥80% ID stability over
100 mid-stream edits" is **ill-defined** — tautological for L, contradictory for K,
ambiguous for K3/Z5. It does not survive analysis in that form. **The frozen bars
themselves all survive individually** — M4's ≥80% revision rate, the U-vs-D 100-edit
cost rule, L's 100% eternity bar, and R3's zero-ghost storm are each well-defined and
untouched by this verdict. What is missing is a *coherent cross-scheme reading* of
M4's "ID/lineage continuity" requirement — which is exactly what §7 proposes (as a
proposal, not a change).

Concretely, the incoherence bites inside M4 today: M4's REVISED definition demands
"the unit's ID/lineage is continuous (same ID, audit shows a revise/repair entry —
not a kill+re-add, which is a new unit wearing the old ID)." Under Design A, a correct
revision **is** a new ID — with a `REVISE_LINK`, not a kill+re-add. The anti-gaming
rule's target is *silent replacement* (kill, re-add, claim continuity); a linked
revision is the opposite of silent. Read literally as ID bit-equality, M4 would score
every honest Design-A revision as UNFIXED and hand a 0% to the mechanism the catalog
elsewhere calls "honest, not a bug." That cannot be the intent — but only Micah can
resolve it, hence §7.

---

## §7 — AMENDMENT PROPOSALS (require Micah's dated sign-off; nothing below is in force)

**Proposal P-1 — lineage-continuity reading of M4's REVISED (Design-A coherence).**
Proposed replacement text for the M4 REVISED bullet's parenthetical, applying to arms
that declare immutable-versioned IDs at sign-off:

> *REVISED (wrong→right): the unit's stored bytes now match the source bytes for its
> claimed span, AND continuity holds: either (a) same ID with an audited revise/repair
> entry (stable-ID schemes), or (b) an unbroken audited revision/split/merge lineage
> (`OP_REVISE_LINK` / `OP_SPLIT` / `OP_MERGE` chain) from the defective unit's ID to a
> live ID naming the repaired bytes (immutable-versioned schemes). A kill followed by
> an unlinked re-add — a new unit wearing the old ID, or wearing no link — remains
> KILLED/UNFIXED, never REVISED. The KILL-SUBSTITUTION rule is unchanged.*

Rationale: preserves M4's anti-gaming intent (lineage, not silent replacement) while
making the metric computable for both designs. The ≥80% bar, the 20-episode cap, and
KILL-SUBSTITUTION are untouched.

**Proposal P-2 — per-scheme operationalization of "ID stability" (replaces the
ill-defined composite).** Wherever the program needs a cross-scheme stability number
(bake-offs, scorecards), report the pair, never a single blended %:

> - *Reference stability* (stable-handle schemes; already frozen for L at 100%):
>   fraction of pre-revision references whose handle is unchanged and live.
> - *Lineage resolvability* (immutable-versioned schemes): fraction of pre-revision
>   references resolving via audited links to a live head. Proposed bar: ≥ 80%
>   (mirrors M4's headroom rationale; ghosts counted as failures, not as
>   unresolvable-but-excused).
> - *Ghost count*: must be 0 under both (R3's bar, unchanged).

**Proposal P-3 — mid-storm ghost checkpoints for R3.** Run the §5 ghost detector at
every sweep episode during the 5,000-edit storm and log pass/fail; any mid-storm ghost
fails the trial identically to a final-state ghost. R3's numbers (zero ghosts,
tombstone/live < 2) unchanged; only the *observation schedule* is strengthened, per the
M1 swap-probe precedent.

**Proposal P-4 — version-confusion extension of the M1 swap probe.** For Design-B arms,
the 64 deterministic remaps additionally cover *stale-`cur`* cases (handle table
patched to a superseded version slot). Recall must fail loudly or label the version
stale; serving old bytes as current = side-channel-grade failure (metric scored 0).
Closes the Design-B-specific hole §2 names.

**Proposal P-5 — Y3's depth bar covers version count under Design B.** Read "mean
lineage depth > 50" as "mean lineage depth **or version count** > 50" so
meaning-drift under stable handles has a tripwire. No number changes; scope
clarified.

All five are proposals. If Micah signs none of them, the frozen text stands exactly as
written — including its incoherence for Design-A arms under M4, which would then be a
documented limitation, not a quiet reinterpretation (RULE-9).

---

## §8 — Falsifiable predictions (with test experiments)

**P1 — Revision-chain latency grows with edit count under Design A (no free
lunch for immutability).** Run a K1-style immutable scheme over the preregistered
100-patch corpus-C series with no compaction. *Predicts:* mean revision-link chain
length ≥ 0.5 × (patches touching the span) by patch 100, and mean recall ops ≥ 1.5×
the no-revision baseline. *Falsified if:* chains stay flat — e.g., edited spans
deduplicate against existing payloads (K3's "merge for free") or patches localize —
in which case K's churn weakness is smaller than the arm text claims and the bake-off's
condition (c) should show it. Either outcome is a finding; the prediction is that it
won't be flat.

**P2 — The §5 reclamation rule passes R3's storm with headroom.** 5,000 deterministic
scripted edits on the 100KB sqlite3.c slice, sweep episodes frozen in the trial prereg.
*Predicts:* final tombstone/live ratio < 0.5 (bar allows < 2), zero ghosts at every
checkpoint (P-3 schedule). *Falsified if:* ratio ≥ 2 or any ghost — which fires R3's
bar and kills the mechanism, exactly as designed. The prediction is that an honest
sweep passes with 4× headroom on the ratio.

**P3 — Content-addressed dedup collapses on the revision stream (marginal, not
absolute).** Measure *marginal* dedup ratio per 10-patch batch on corpus C vs the
static-corpus dedup ratio. *Predicts:* marginal dedup ≤ 0.15 × static dedup — every
patch re-IDs its touched spans, so the revision stream contributes almost no new
sharing. *Falsified if:* marginal dedup stays > 50% of static — patches would then be
localized enough that K's re-ID churn is a non-issue, strengthening K's hand in the
bake-off beyond what the arm text concedes.

**P4 — L1 pays a revision-map fragmentation tax on corpus C.** Under L1 with sealed
segments + revision map over the 100-patch series. *Predicts:* revision-map walk ops ≥
20% of total recall ops by patch 100 (adjacent logical positions scatter across
segments; the arm text predicts locality degrades). *Falsified if:* map-walk ops <
5% — L's "eternal ID" would then be nearly free and L1's bake-off standing improves
accordingly.

**P5 — Eldest-child-inherits splits produce silent name-changes; retire-always does
not.** 1,000-split synthetic battery (deterministic split schedule, S-B1 vs S-B1′
legs). *Predicts:* the inherit leg shows ≥ 1 audit-detectable silent name-change (a
handle naming bytes ≠ the bytes named at its birth, with no covering revise entry)
while retire-always shows 0. *Falsified if:* inherit also shows 0 — then the simpler
rule wins on handle economy and S-B1 is dropped as overcautious. (This is RULE-2
working as intended: the judgment call becomes a leg.)

**P6 — The M4 reading matters more than the mechanism.** Run K1 on the M4 battery and
score it twice: literal ID-bit-equality reading vs the P-1 lineage-continuity reading.
*Predicts:* the gap is ≥ 60 points (bit-equality ≈ 0%, lineage ≈ 80%+) — demonstrating
that the *reading* decides pass/fail, not the revision quality. *Falsified if:* the
gap is < 20 points — then P-1 is unnecessary ceremony and M4 stands as written for all
schemes.

---

## §9 — Verdicts (exploratory; the bake-off decides, not this document)

**Versioned vs stable — the exploratory verdict.** Neither pure design satisfies the
frozen bars alone: pure-A breaks the literal M4 "same ID" reading (needs P-1); pure-B
carries the R3-noted insert-death risk and the frozen >3×-cost kill bar. The
decomposition both pure schemes are asking for is **immutable content payloads
(revision visible = integrity, Design A) under stable reference handles (memory ops
don't churn, Design B)** — which is K3's `(content_hash, stream, seg, off)` split,
already in the catalog. The frozen program already encodes the decision procedure:
**K3's hybrid-promotion rule** (beats both pure schemes on ≥3/5 bake-off metrics →
pure schemes demoted to components). Per RULE-2 and RULE-6 this is not crowned by
argument here — it is the leading hypothesis awaiting the bake-off. For the cache
layer specifically: invalidation is only well-defined in the composite (handle-stable
cache entries + version-checked payloads); pure A has tombstone+relink instead of
invalidation, pure B has version-pointer bumps with drift-policing.

**Ghost-ID reclamation rule (summary).** Episodic mark-sweep at frozen sweep episodes:
reclaim iff `refs==0 ∧ unpinned ∧ not a live lineage head ∧ outside the protected
birth window`; reclamation = one audited `OP_TOMBSTONE`; **tombstoned ID values are
never re-minted**; every sweep ends with the ghost detector (`G1/G2/G3`) over all
live records and **any ghost halts loudly** — ghosts are integrity violations, never
cleanup events. Per-op refcounting is rejected as the default because Y6's frozen
kill bar already prices it as potentially unaffordable.

**The five (+1) predictions.** P1 chain-latency growth; P2 storm headroom; P3 marginal
dedup collapse; P4 L1 fragmentation tax; P5 inherit-vs-retire split legs; P6 the M4
reading gap. All are pure-Zag-testable, zero-RNG, byte-identical-rerun compatible.

**Does the frozen revision bar survive?** The *phrasing* "100 mid-stream edits; ≥80%
ID stability" does **not** survive as a scheme-neutral bar — it is ill-defined
(tautology for L, contradiction for K, ambiguous for K3/Z5), and no frozen item
carries exactly that wording. The **actual frozen bars all survive individually**:
M4's ≥80% revision per class, the U-vs-D 100-edit cost kill rule, L's 100% eternity
bar in the K-vs-L bake-off, and R3's zero-ghost 5,000-edit storm. What needs Micah is
§7's five amendment proposals — P-1 (lineage-continuity reading of M4 REVISED) is the
load-bearing one. Until signed, the frozen text stands verbatim, including the
documented incoherence for Design-A arms under a literal M4 reading.

**Open questions for the parent (not findings):** (1) the PREREG_FREEZE.md header/body
status mismatch noted at the top; (2) whether §7's proposals should be filed to Micah
now or held until the K-vs-L bake-off build begins; (3) opcode-namespace unification
(A-3) must assign real numbers to `OP_TOMBSTONE`/`OP_REVISE_LINK`/`OP_SPLIT`/
`OP_MERGE`/`OP_REVISE`/`OP_REPAIR` before any sketch here becomes buildable — flagged,
not decided.
