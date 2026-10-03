# Node2-v2 Build Report

## Implementation Summary

Built Node2-v2 consequence-driven policy update on unfrozen TNN-2 variant.
Frozen source read-only; all changes in `n2v2.zag` (unfrozen variant).

## Changes vs Frozen TNN-2

### 1. Policy Node (new function `n2v2_pol_get`)

Tag 40, subtype 2 (field 4 = 2). Gets or creates the policy node.

Field layout:
| Field | Content | Init |
|-------|---------|------|
| 0 | tag | 40 |
| 4 | subtype | 2 |
| 8 | revealed-action history slot 0 (most recent) | -1 |
| 12 | revealed-action history slot 1 | -1 |
| 16 | revealed-action history slot 2 (oldest) | -1 |
| 20 | default action | 30 |
| 24 | default content | -999 |
| 28 | resolution count | 0 |
| 32 | miss count | 0 |

History slots hold WORLD-REVEALED actions (a_w), not guide actions.
This is the minimal change that restores reachability vs Node 2.

### 2. Production Write Path (new function `resolve_uncertainty_v2`)

Called from `ev_observe_aw` when an open uncertainty exists for (s,r):

1. Find open uncertainty u for (s,r) (tag 30, live, not superseded).
2. Supersede u and its guide g via type-3 self-edge convention.
3. Increment resolution count (field 28).
4. If `a_w >= 0`:
   a. Shift history: field 16 := field 12; field 12 := field 8; field 8 := `a_w`.
   b. If field 8 == field 12 == field 16 == A, with A >= 0 and A != field 20:
      - Set field 20 := A (production write).
      - Reset history: fields 8, 12, 16 := -1, -1, -1.
5. If `a_w == -1`: history unchanged.

### 3. Production Read Path (modified `miss_inquire`)

Reads default action from policy field 20 (instead of literal 30).
Reads default content from policy field 24 (instead of literal -999).
Creates guide with these values. Increments miss count (field 32).

### 4. Action Channel (new function `ev_observe_aw`)

`ev_observe_aw(W,s,r,o,a_w)`:
- `a_w = -1`: no action information. Behavior identical to frozen `ev_observe`.
- `a_w >= 0`: world reveals action `a_w` with this observation.
- When no fact exists for (s,r): teaches the fact, then calls
  `resolve_uncertainty_v2(W,s,r,a_w)`.

This is an interface extension on the world-to-learner channel,
not a change to protected cognition.

## Source Delta

- New functions: `n2v2_pol_get` (18 lines), `resolve_uncertainty_v2` (45 lines),
  `ev_observe_aw` (28 lines).
- Modified: `miss_inquire` (reads policy instead of literals; +8 lines).
- Total new/modified cognition lines: ~100.
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- New node types: 0 (uses tag 40, already in frozen source).
- New edge types: 0 (uses existing type-3 supersede convention).

## Consequence Re-entry Chain (verified)

- **Experience:** world reveals action `a_w` = 45 via `ev_observe_aw`,
  resolving an open uncertainty.
- **Retained consequence:** `a_w` recorded in policy history slots (fields 8/12/16),
  tagged by construction as world-sourced.
- **Production write:** after three consistent `a_w` = 45 revelations,
  field 20 := 45 (OVERWRITE, not append).
- **Later production read:** next `miss_inquire` reads field 20 (= 45).
- **Changed action:** new guide created with action 45; `ev_act` returns 45.

The chain is acyclic: world -> record -> write -> read -> action.
No edge from action back to world within one update cycle.

## Provenance

The revealed action `a_w` has source = world (external observation).
The guide's action (learner's suggestion) never becomes evidence for
revising itself. This satisfies the architectural provenance requirement.
