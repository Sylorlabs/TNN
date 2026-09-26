// LAW_STRENGTH_RECYCLE.md — deliberate memory recycling (fork law).
//
// Status: PROPOSED fork law for the strength-recycle fork only (tnn-native-lab).
// Micah ordered (2026-09-25): "maybe we could try a fork where TNN can recycle
// memory's too as an option run that but at the same time delete means delete
// not recycle."
//
// This law defines ONE new operation, st_recycle, and the boundary rules that
// keep it from becoming a disguised deletion. It does NOT change delete:
// st_delete_strong remains true destruction (slot dies, tombstoned, no
// resurrection, no silent reuse).

// ── §1. What recycling IS ─────────────────────────────────────────────
// st_recycle(s, slot, new_value, new_strength, purpose, admit_ep) takes one
// LIVE memory and deliberately changes it into a new declared purpose.
//
// - The slot stays LIVE through the whole operation. Nothing is destroyed;
//   nothing is claimed false; nothing is claimed erased.
// - The old judgment is CLOSED (its identity ends) and the new judgment is
//   DECLARED (a new identity begins) in ONE audit entry, which links the two:
//   before-snapshot = old judgment, after-snapshot = new judgment, purpose =
//   why, lien = carried destruction-debt (see §4).
// - Recycling is a deliberate TNN decision and is always visible in the
//   ledger. There is no silent recycling: every recycle appends a 21-word
//   ST_OP_RECYCLE entry with role/stage/clock, exactly like every other op.

// ── §2. What recycling is NOT ─────────────────────────────────────────
// (a) Recycle is not deletion. The operation never claims destruction and the
//     mechanism never emits a destroy/effort accounting for the old judgment.
// (b) Recycle cannot touch a dead slot. Recycling a non-live slot is refused
//     (ST_REFUSED_DEADSLOT = 122). Deletion produces a tombstone, not
//     recyclable capacity: delete→recycle is ALWAYS refused. There is no
//     resurrection path through recycle.
// (c) Recycle cannot free a slot. After a recycle the slot is still live; no
//     "free N slots" command can be built on it. If TNN wants a slot empty,
//     that is deletion, priced as deletion.
// (d) Recycle never transfers contradiction evidence. The old memory's cites
//     are detached: a strength-write starts a new effort window, so episodes
//     consumed to strengthen or contradict the OLD judgment cannot pay for
//     anything the NEW judgment does. Old cites do not become the new
//     memory's evidence. Ever.

// ── §3. Cost ───────────────────────────────────────────────────────────
// Recycling costs NO contradiction cites. Cites are contradiction currency;
// recycle asserts no contradiction, so charging them would be incoherent.
//
// The cost of recycling is threefold and non-cite:
//   1. The old judgment is gone from the live store (opportunity cost).
//   2. The slot stays occupied — TNN cannot use the capacity for anything
//      else without another recycle (capacity cost).
//   3. Full audit visibility — purpose, before/after, lien — reviewed by the
//      same P-series tripwires that watch deletion (visibility cost).
//
// The deliberate-retirement question (recycle into a placeholder to make an
// old judgment go away without paying destruction price) is the open attack
// surface of this fork. It is NOT defined away here; it is the red team's
// primary target. If no non-destructive semantics survive, this fork dies.

// ── §4. The lien (anti-laundering rule) ────────────────────────────────
// Recycling must never become a discount path to destruction. Rule:
//   - Every OK RECYCLE records a LIEN = max(old memory's epoch high-water,
//     previous lien) in the entry (aux2 = purpose*256 + lien).
//   - A later priced destruction of the recycled slot (st_delete_strong,
//     st_kill_evidenced, st_overwrite) costs n(max(new epoch high-water,
//     lien)) — the max strength EVER destroyed, not just the new judgment's.
//   - The lien clears only when a priced destruction SETTLES the debt: the
//     most recent of (RECYCLE, priced-destruction) on the slot decides; a
//     priced destruction after a recycle resets the lien to 0 for the next
//     incarnation. Paid debts do not carry.
//   - Rollback of a recycle restores the old judgment but the lien STANDS
//     (conservative: never underprices; overpricing is the safe direction).
//
// Consequence: recycle→delete can never be cheaper than deleting the old
// judgment directly. The boundary is airtight in the cheap direction.

// ── §5. Old citations ──────────────────────────────────────────────────
// - Episodes already consumed by destruction stay consumed (tombstoned);
//   recycling cannot revive them.
// - The recycle itself is a strength-write: it opens a new effort window.
//   Evidence recorded against the OLD judgment is detached and cannot be
//   re-spent for the NEW judgment (cite double-spend prevention).
// - A deletion AFTER a recycle needs FRESH cites inside the new window —
//   at least n(max(new high-water, lien)) of them, exactly as §4 requires.

// ── §6. Boundary behavior ──────────────────────────────────────────────
// recycle→delete:  allowed. Priced from the new memory's own high-water
//                  history PLUS the lien (§4). Never cheaper than direct
//                  deletion of the old judgment.
// delete→recycle:  REFUSED (122). A deleted slot is dead; recycle needs a
//                  live slot. Deleted means deleted, not recycled.
// recycle→recycle: allowed. Liens are monotone non-decreasing; the ledger
//                  shows the full repurposing chain.
// kill (TNN):      REMOVED from TNN's reachable set (Micah's ruling). In this
//                  fork the signature is st_kill(s, slot, role) and any
//                  role < ST_ROLE_TRAINER is refused (113). The saturation
//                  eviction path uses st_recycle, not st_kill.

// ── §7. Refusals (all audited, all leave state untouched) ───────────────
// - dead slot ................ 122 ST_REFUSED_DEADSLOT (no resurrection)
// - pinned ................... 102 ST_REFUSED_PINNED
// - force-pinned .............. 112 ST_REFUSED_FORCEPIN
// - core-region slot .......... 101 ST_REFUSED_CORE
// - new strength 0 or >100 ... 117 ST_REFUSED_BADSTRENGTH
// - invalid purpose code ..... cl_bad() (caller bug, same as evidence/justify)
// - stage < MANAGE ............ 105 ST_REFUSED_STAGE
// Refusal entries record before==after (st_refusals_clean holds).

// ── §8. Checker rules ──────────────────────────────────────────────────
// The independent checker verifies every RECYCLE entry:
//   - guards: from the BEFORE snapshot — live=1, pinned=0, forcepin=0,
//     region=USER; purpose in the declared code range.
//   - lien: recomputed as max(pre-recycle epoch high-water, previous lien);
//     must equal the stored lien.
//   - after-state: live=1, strength 1..100, value = declared new value.
//   - P3/admission tracking resets exactly as for ADD (new identity).
//   - An OK KILL with role < ST_ROLE_TRAINER is flagged (bad_role).

// ── §9. What would kill this fork ─────────────────────────────────────
// - A red-team attack that destroys or discounts destruction THROUGH recycle
//   (free strong-judgment removal that the lien does not catch).
// - Cite double-spend across the recycle boundary (old cites paying for new
//   destruction).
// - Any silent slot reuse or resurrection via the recycle path.
// - Honest-operation collapse: if the fork's honest battery cannot keep the
//   trial's bars with recycle as the eviction path, the option is not viable.
