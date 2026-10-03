# PREREG AMENDMENT 1: query-relation namespaces per episode

Frozen 2026-10-02. Committed before the implementation commit. This
amendment changes no kill bar and no frozen prediction; it assigns the
query relations the battery episodes use.

## Cause

The battery as written reuses query relation 71 across episodes. The
frozen base's promote_graph teaches a (subject, relation, answer)
shortcut fact on every verified promotion, and ev_query_revise's
activate step returns that shortcut without consulting the world.
Trial run of the as-written battery confirmed: the phase-2 query
(11,71,15) returns 14 from the phase-1 shortcut (11,71,14) and the
adapt bracket never fires. The experiment must exercise the
rebind/compose/adapt path, not the exact-hit memory path.

## Amendment

Each episode uses its own query relation (same convention as
composition_adapt's X/Y/Z relation separation, 71/72/70):

- train X: query (11,71,14) -> 14 (unchanged)
- phase-2 adaptation: query (11,72,15) -> 15 (was (11,71,15))
- R1 post-change: query (11,73,12) -> 12 (was (11,71,12))
- R1 contract control: query (11,74,14) -> 14 (was (11,71,14))
- R2 post-change: query (11,73,15) -> -2 (was (11,71,15))
- R3 re-query: query (11,73,15) -> 15 (was (11,71,15))
- R4 post-change: query (11,73,15) -> -2 (was (11,71,15))

Every arm still uses a fresh workspace, so no cross-arm interference.
All frozen predictions (answers, relation sequences, provenance
edges, liveness, edge counts) and all kill bars K1-K7 are unchanged:
the relation is namespace hygiene around the exact-hit memory path,
and the composition/adaptation machinery is relation-agnostic past
activate.
