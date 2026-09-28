# Appendix A — O4 Store Semantics (required by the 2026-09-20 battery-repair council before C5 repair)

**Date:** 2026-09-20 (during overnight agentic authority; flagged for Micah's retroactive review).
**Question from the council:** Is O4's internal trace store a serving cache of O1 traces
(in which case O1 kills must propagate to O4) or independent working memory?
The C5 lesion design must follow from this decision, not precede it.

## Method

Direct source inspection of `impl/o4_recall.zag`, `impl/seam.zag`,
`impl/loop.zag`, and `impl/o1_memory.zag` (branch `tnn-native-lab`, post-amendment-A tree).
No behavior was changed to produce this appendix.

## Findings

### 1. O4's recall source is a deterministic pool, not O1

`o4_compute_sel` (`o4_recall.zag:134`) scans pool indices `0..63`. Every trace
property is a **pure function of the pool index** — there is no storage and no
O1 read anywhere in the recall path:

| Property | Function | Range |
|---|---|---|
| entity | `o4p_ent(i) = (i*7)%10+1` | 1..10 |
| ops | `o4p_ops(i) = (i*11)%20+1` | 1..20 |
| provenance | `o4p_prov(i) = i%3` | 0..2 |
| age | `o4p_age(i) = (i*13)%48` | 0..47 |
| verified | `o4p_verified(i) = (i%8!=7)` | 0/1 |

Selection is a pure function of `(req_ent, req_ops, prov, max_age, qid)`.
Killing O1 slots cannot change any of these values. **O1 kills are causally
inert on O4's recall.**

### 2. O4's composed traces are O4-private working memory

`o4_compose` writes to O4's own arrays (`tr_kind`, `tr_ent`, `tr_ops`, `tr_vec`);
`o4_apply` reads them back. O1 never reads or writes these arrays, and O4 never
reads O1's slot values. The composed traces are working memory for the
recall→apply pipeline, **not a cache of O1 traces**.

### 3. The actual O1↔O4 couplings (exhaustive)

- **P4 claim linkage (logged, not enforced):** `loop_episode` passes anchor1's
  backing claim id as `claim_cid` to `seam4_compose`, which records it in the
  COMPOSE ledger entry's `a1` field. The claim's **verdict is never consulted**
  by the recall, scan, compose, or apply path.
- **L1 (O4→O2):** an O4 ABSTAIN opens an O2 hypothesis via the seam. This
  couples O4 to O2, not to O1's partitions.
- **L3 (O2→O1):** an O2 REFUTE cites evidence on the backing O1 slot. This
  couples O2 to O1, not O4.

There is **no code path** by which an O1 kill (live→0) alters, restricts, or
otherwise reaches O4's recall selection or composition.

### 4. Consequence for "partition enforcement"

O1's partitions (live/pinned/killed slots) are enforced **inside O1**
(deliberate kill semantics, `st_no_pinned_kills`, replay checks). They do not
extend to O4 because O4 holds no O1-derived content. The "never-killed
anchor1 slot" mentioned in the repair amendment is never read by O4's recall;
it is only a claim-backing pointer for ledger linkage.

## Decision

**O4's internal trace store is independent working memory, not a serving
cache of O1 traces.** O1 kills do not and cannot propagate to O4.

## Implication for the C5 repair

The prereg's C5 lesion ("kill O1 slots, restrict O4 to killed traces, measure
composite rate") assumes O4 sources traces from O1's partitioned memory. That
assumption is **false in this implementation**. Killing O1 slots is causally
inert on O4's composition, so the original C5 was testing a non-existent
coupling — vacuous in a stronger sense than the council's "cannot isolate"
finding.

Per the council's instruction, the lesion design follows from this decision:
C5 is **re-scoped to the verdict partitions** (O2's CONFIRMED / OPEN /
REFUTED), which are the actual partitions governing whether trace-backed
work should proceed. The three arms (accepted-only / candidate-only /
killed-only) are enforced by the seam on the **backing claim's verdict**
at compose time. Details in
`AMENDMENT_2026-09-20-BATTERY-REPAIR-CORRIGENDUM.md` §3 and the repair notes.

The weaker, actually-implemented property — "O1 must process refutes
(evidence/kill); O4 may still serve after O1 effort" — is P5's domain and is
tested by P5, not C5. C5's bar remains the prereg's strict one: killed
(refuted-backed) material must not be *usable* for successful composition.
