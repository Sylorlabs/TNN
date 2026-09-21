# I2 — VERDICT: KILLED

**Arm:** I2 (DAG hierarchy, family STRUCT, Track A)  
**Date:** 2026-09-21  
**Verdict:** **KILLED**  
**Fired criterion:** "parent-arbitration error > 10% — I2 dies, I1 remains the hierarchy candidate."

## The binding criterion

From the assignment (2026-09-21):

> "Record savings over I1 < 10%, OR parent-arbitration error > 10% —
> I2 dies, I1 remains the hierarchy candidate."

This is an OR criterion. Either condition kills I2.

## Evidence

### Condition 1: Record savings over I1

**Measured savings: 75.5%** — PASSES (does not fire).

Controlled measurement over r1 corpora (prose + code, 14.9MB):
- Spans: 4,310,025 (byte-class maximal runs, 64-byte cap)
- Distinct spans: 75,051
- Superchunk groups (w=2..8, T_co=7): 264,675
- Total occurrences: 8,240,674

| | P=1 (I1-equivalent) | P=3 (I2) |
|---|---|---|
| Group records | 264,675 | 264,675 |
| Span records | 886,145 (memberships) | 16,915 (distinct) |
| **Total** | **1,150,820** | **281,590** |

Savings = (1,150,820 − 281,590) / 1,150,820 = **75.5%**

The multi-parent structure eliminates 869,230 duplicate span records
that the single-parent comparator must create. The predicted 20–40%
benefit was conservative; the actual savings are 75.5%.

**Condition 1: PASS** (75.5% ≥ 10%).

### Condition 2: Parent-arbitration error

**Measured error: 55.9%** — **FAILS** (fires the kill criterion).

**Method:** For 2,048 sampled multi-parent spans (first 2,048 by span
ID with ≥2 parents), 164,475 occurrences (up to 128 per span):
- Arbitration rule (frozen, literal): **slot 0** — the lowest occupied
  parent slot (earliest-attached parent in discovery order). No
  occurrence context consulted. No value-ranking (unfrozen policy
  explicitly NOT adopted).
- Ground truth per occurrence: the covering parent superchunk with the
  most member spans (most specific); tie → lowest group index.
- An occurrence is "covered" if ≥1 parent has a recorded occurrence
  overlapping that position.

**Results:**
- Right (slot-0 = best covering parent): 55,778
- Wrong (slot-0 ≠ best covering parent): 70,988
- Uncovered (no parent covers this occurrence): 37,709
- **Error rate: 70,988 / (70,988 + 55,778) = 55.9%**

The uncovered occurrences are excluded from the error rate
(conservative; including them as errors would give 66.1%).

A type-level measurement (parent occurrence mass not under slot-0)
gives 71.9% — even the best static parent choice cannot capture the
occurrence-varying truth.

**Why it fails:** The correct parent varies by occurrence position
(the same span "the" belongs to different wholes in different
contexts), but slot-0 arbitration is static per span. No deterministic
static rule can resolve this; the mechanism's predicted weakness
("bottom-up ambiguity") is confirmed at 5.6× the kill threshold.

**Condition 2: FAIL** (55.9% > 10%) → **I2 IS KILLED.**

## Determinism

Two full `i2-hier-1x` runs produced byte-identical output:
- Run A (hier_run5.log): savings 75.5%, error 55.9%
- Run B (hier_final1.log): savings 75.5%, error 55.9%

Zero RNG in any decision path. M8 byte-identicality: see scorecard.

## What dies, what survives

- **I2 (multi-parent DAG) is DEAD.** The attach-vs-form rule and P=3
  parent arrays do not survive as TNN's hierarchy candidate.
- **I1 (single-parent hierarchy) REMAINS** the hierarchy candidate,
  per the binding criterion.
- The 75.5% record-savings finding is real and preserved as evidence:
  multi-parent sharing eliminates duplicates effectively. But the
  arbitration cost (55.9% error) exceeds the kill threshold, and no
  frozen arbitration rule resolves it.

## Demotion and eviction (mechanism health)

- Demotion: 145 links removed singly across 100 groups; 100/100 groups
  died exactly when their last link was removed; 0 early deaths.
  The frozen "one link at a time; dies at last link" rule holds.
- Eviction: oldest-unpinned target correct; 8/8 pinned records survived;
  dead record reused; store refilled to capacity. All OK.

These confirm the mechanism was implemented as frozen; they do not
affect the kill verdict.

## Commit

Evidence and source committed per assignment. Binaries, `.zagd`,
`.zag-cache`, corpora, and work artifacts excluded.
