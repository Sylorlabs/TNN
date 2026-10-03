# PREREG H-FDCR-UNIFIED2 FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED2 Repair Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED DOWNGRADED (red team: FDCR_UNIFIED_ADV_RESULT.md)
**Status:** FROZEN. Implementation must strictly follow this prereg.

## Hypothesis

The three H-FDCR-UNIFIED red-team downgrades can be repaired without
breaking the 23/23 frozen bars:

- X-FU1 (first-input-only association): repair with majority-vote over
  ALL training inputs.
- X-FU2 (feature fragmentation): repair with feature accumulation
  before con_form; the call site will pass nfeat>1.
- X-FU4b (trace inconsistency): repair by including the cb*5000 term
  in intent_trace_emit.

The X-FU3 bridge-asymmetry boundary can be closed by extending concept
support to bridge rules.

## Repairs (frozen)

### R1: Majority-vote concept association (X-FU1)

`handle_proc_learn_unified` currently computes `train_con` from only
the first training pair's input. Replace with:

- For each training input, compute its concept via
  `con_find_member_str`.
- For each distinct concept found, count how many training inputs are
  members of that concept.
- Select the concept with the highest count.
- Require strict majority: count * 2 > nseg. Otherwise train_con = -1.
- Ties for the top count: first-seen wins (disclosed tie-break).

The same majority-vote logic is used for bridge concept association
(see R4).

### R2: Feature accumulation (X-FU2)

`handle_concept_learn` currently calls `con_form` with nfeat=1 per
fact. Restructure to two passes:

- Pass 1: parse all facts in the batch into (subject, feature) pairs.
- Pass 2: group by subject (string content). For each distinct
  subject, accumulate all its features (deduplicated, max 8).
  - If the subject is already a member of an existing concept (from a
    prior batch, via `con_find_member_str`), extend that concept's
    feature set with the new features (skip duplicates, max 8
    features). Do not create a new concept.
  - Otherwise, call `con_form` once with the full accumulated feature
    set (nfeat may be > 1).
- Return the number of facts parsed (preserves documented contract).

Honest limitation (disclosed): when an entity's concept gains a
feature via extension, other existing members are not re-evaluated
against the enlarged feature set. This is a v2 simplification, not
full FDCR revision.

### R3: Trace consistency (X-FU4b)

`intent_trace_emit` currently displays proc scores as
`lm*10000+seq`, omitting the `cb*5000` term used by
`intent_winner`. Repair:

- Compute `qcon` (query concept) once at the top of the proc loop,
  as `intent_winner` does.
- For each proc candidate, compute `pcon` and `cb` (1 if qcon>=0 and
  pcon>=0 and qcon==pcon, else 0).
- Display `concept_boost=` followed by cb, and display the score as
  `lm*10000+cb*5000+seq`.
- Bridge candidates: display `concept_boost=` and include the term
  (see R4).

The trace must explain the actual winner. A user reading the trace
must be able to predict the winner from the displayed scores.

### R4: Bridge concept support (X-FU3 boundary)

- New `intent_record_br_con(W, bslot, train_len, concept)` records
  concept association for bridge rules (parallel to
  `intent_record_proc_con`).
- `handle_proc_learn_unified`: when a bridge is learned (rc>=1000),
  compute train_con via the same majority-vote (R1) and call
  `intent_record_br_con`.
- `intent_winner`: bridge scoring becomes
  `cf*20000+lm*10000+cb*5000+seq`, where cb=1 if the query and the
  bridge rule share a concept.
- `intent_trace_emit`: bridge candidates display `concept_boost=`
  and the full score.

The existing `intent_record_br` (concept=-1) is retained for
compatibility but no longer used by the unified handler.

## Frozen Kill Bars

- **K-FU2-1 (X-FU1 repair):** Setup: concepts {cat,dog} in concept 0
  (via `T cat | is_a | pet` and `T dog | is_a | pet`). Train P1 on
  `cat>tac;bat>tab` (1 of 2 inputs are concept members). Verify P1's
  recorded train_con == -1 (majority vote: 1*2 <= 2, no association).
  Train P2 on `cat>tac;dog>god` (2 of 2 members). Verify P2's
  train_con == 0. Both must hold.

- **K-FU2-2 (X-FU2 repair):** (a) Cross-batch: `T cat | is_a | pet`
  then `T cat | color | orange` as separate `handle_concept_learn`
  calls. Verify `con_count == 1` (not 2). Verify concept 0 has
  `nfeat == 2`. (b) Within-batch:
  `T bird | is_a | pet; T bird | color | blue` in a single call.
  Verify a single concept is created/used with nfeat == 2. Both (a)
  and (b) must hold.

- **K-FU2-3 (X-FU4b repair):** Setup: concept {cat,dog}. Train P1 on
  `cat>tac` (concept-associated), P2 on `abc>aaa;def>ddd` (not).
  Run `intent_trace_emit` on query `dog`. Verify the trace output
  contains `concept_boost=1` for the P1 candidate and the displayed
  score for P1 is 15000 (10000 + 5000 + 0), not 10000. Verify the
  displayed winner matches `intent_winner`'s actual winner.

- **K-FU2-4 (no regression):** All 23/23 original H-FDCR-UNIFIED
  tests PASS. Run the full test suite (Part A: 9 unified, Part B: 10
  intent, Part C: 4 concept) via the main() function and verify
  23/23.

- **K-FU2-5 (determinism):** Three runs byte-identical (cmp-verified).

## Honest Boundaries

- Majority vote requires strict > 50%. A 50/50 split yields -1.
- Feature extension does not re-evaluate other members (see R2).
- Max 8 features per concept (existing store limit).
- Max 16 facts per concept-learn batch (parse array limit).
- The repairs are bounded L2 integration fixes, not L3.

## Classification Target

Bounded L2 integration repair. Not L3. No representational
invention claimed.

## Governance

- Pure Zag. No Python in implementation, tests, or analysis.
- Prereg commit must strictly precede implementation commit.
- New file `unified_fdcr2.zag` (copy of `unified_fdcr.zag` with
  repairs); the original is not modified.
- No em dashes in documentation.
