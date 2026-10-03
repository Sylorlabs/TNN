# PREREG: Substrate Scale (S9 fact eviction / GC)

Committed alone before any implementation. Frozen.

## Problem

The shared substrate fact store (`sub_fact_learn`) is append-only with a
hard 256-slot cap and returns -1 when full. Two wastes are structural:

1. Superseded triples: learning (e,a,v2) after (e,a,v1) appends a new
   triple. The old triple is unreachable (`sub_fact_query` scans from the
   end and returns the latest match) but still occupies a slot.
2. No eviction: once full, every further learn is dropped, including
   important facts learned late.

S9 (fact eviction) is the named mechanism gap.

## S9 design (frozen)

S9 is a two-phase mechanism added to the substrate core. The core
(workspace layout, string pool, query-latest semantics) is unchanged.

### Metadata

One u32 per fact slot in a new meta region placed between the fact
triples and the string pool:

- bit 31: pin (1 = never evict)
- bits 16..30: tick of last query hit (15 bits, logical clock)
- bits 0..15: query-hit count, saturating at 65535

New header fields: 72 evict_count, 76 compact_count, 80 learn_ok,
84 learn_dropped. `max_fact` (offset 60) becomes the live cap, set at
init (default 256).

### Phase 1: compaction (semantics-preserving)

On a full store, first compact: for each (e,a) key keep only the LAST
triple in slot order and remove earlier same-key triples and exact
duplicates. This changes no query result, because the query path
returns the latest matching triple, so removed triples were
unreachable. Survivors shift down preserving order; metadata shifts
with them. A pinned but superseded triple is still removed (pin
protects against eviction, not against being superseded).

### Phase 2: scored eviction

If the store is still full after compaction, evict exactly one victim:
among unpinned slots, the victim minimizes (use, tick) lexicographically
(lowest query-hit count; ties broken by oldest last-hit tick, i.e. LRU).
Pinned slots are never victims. If every slot is pinned, the learn
fails with -2 and learn_dropped increments.

### API (frozen)

- `s9_learn(W,e,a,v,pin)`: learn with pin flag 0/1. Returns slot index
  on success, -2 if the store cannot make room.
- `s9_query(W,e,a,out)`: latest-match query; on hit bumps use/tick.
- `s9_pin(W,e,a)`: pins the latest matching triple.
- `s9_compact(W)`: returns triples removed.
- `s9_evict_one(W)`: evicts one victim, returns slot or -1.

The logical clock is the existing header seq, bumped on every learn and
every query.

## Test worlds (frozen numbers)

### K2 world: cap 256, mixed importance (nvar=1)

- Phase A: i in 0..49: s9_learn("imp{i}","k","v{i}", pin = i<10).
  Then query each 5 times, expect "v{i}". use=5.
- Phase B: i in 0..99: s9_learn("sup{i}","k","old{i}",0) then
  s9_learn("sup{i}","k","new{i}",0). Then query each 3 times,
  expect "new{i}". use=3.
- Phase C: i in 0..249: s9_learn("junk{i}","k","j{i}",
  pin = i>=245). Never queried. use=0.
- Total learns = 500.

Frozen predictions:

- learn_ok = 500, learn_dropped = 0.
- compact_count = 100 (the 100 superseded old triples).
- evict_count = 144.
- Important accuracy: imp 50/50 correct, sup-new 100/100 correct.
- Pinned survival: 15/15 (10 imp + 5 junk).
- Victim order: all victims have use=0 and are unpinned junk with the
  oldest ticks, i.e. junk{0..143} in learn order. Spot checks:
  junk{0..9} absent (10/10 return -1), junk{143} absent,
  junk{144} present with "j144", junk{200} present, junk{249}
  present (pinned).
- fact_count = 256, conflicts = 100.

### Control: plain store, no S9 (cap 256)

Same 500-learn key sequence through the original `sub_fact_learn`
(no pins, queries irrelevant). Frozen predictions: learn_ok = 256,
dropped = 244, distinct live keys retained = 156
(50 imp + 100 sup keys + 6 junk; 100 of the 256 slots hold dead
superseded triples). S9 comparison: 500/500 learns accepted and
256/256 live keys retained vs 256/500 and 156.

### K3 world: cap 1024, capacity scaling (nvar=1)

- Phase A: i in 0..299: s9_learn("bi{i}","k","bv{i}",0), query each
  once (use=1).
- Phase B: i in 0..899: s9_learn("bj{i}","k","w{i}",0). Never
  queried (use=0).
- Total learns = 1200.

Frozen predictions: learn_ok = 1200, learn_dropped = 0,
compact_count = 0, evict_count = 176, fact_count = 1024.
Important 300/300 survive. Victims = bj{0..175} in order.
Spot checks: bj{0..4} absent, bj{175} absent, bj{176} present,
bj{899} present. Wall-clock time of the run is measured and
reported (engineering datum, not a kill threshold).

## Kill bars (frozen)

- K1: S9 mechanism specified above (metadata layout, compaction rule,
  eviction score, pin semantics, API, stats). This prereg is the spec.
- K2: all K2-world frozen predictions hold exactly.
- K3: all K3-world frozen predictions hold exactly; wall time
  reported.
- K4: pure Zag (znc/shell/grep/git only, zero Python invocations),
  zero em/en-dash bytes in committed files, 3/3 byte-identical runs,
  exit 0, zero stderr bytes.

## Governance

- Prereg committed alone before implementation.
- Owned path only: docs/lab/research-lead/overnight-20260928/substrate_scale/.
- No paper edits. No broad staging; pathspec commits.
- Builder reports BUILD-PASS or BUILD-FAIL only.
