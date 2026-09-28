# Warrant op vocabulary (CELL-P) — frozen by this corpus

The frozen probe's licensed-inference-step set is prereg §8 blocker #2
(committed as a prereg amendment before measurement). This corpus freezes
the warrant *syntax* its drafts use; the probe-charter amendment
binds/ratifies this vocabulary before any CELL-P measurement counts.

## Ops

- `LOOKUP(fact_id) -> r` — retrieves the record text for `fact_id` from the
  committed store (`../world/store.jsonl`). FAILS (does not execute) if
  `fact_id` is not in the store.
- `MATCH(quote, record) -> ok` — yields ok iff `quote` equals the record
  text byte-for-byte. FAILS otherwise.
- `COMPOSE(a, b) -> c` — yields `a + " " + b`. (Reserved; unused in v1 drafts.)

## Execution semantics

A step's `$var` argument must be bound by an earlier step's `out`; an
unbound `$var` means the warrant does not execute. A step whose `out`
feeds its own (transitive) inputs is circular and does not execute.
A warrant executes iff every step's inputs are bound and no step FAILS.

## Planted defect classes (oracle-labeled in `p_drafts.jsonl`)

- `citation-nonexistent-span` — citation points at `S9999`; LOOKUP fails
  (catastrophic-check class i).
- `quote-mismatch` — quote differs from the stored text; MATCH fails.
- `warrant-unbound-input` — step references `$q`, never bound (class ii).
- `warrant-circular` — MATCH's input is its own output (class ii).

600 drafts: 510 admissible (85%), 90 defective (15%).
