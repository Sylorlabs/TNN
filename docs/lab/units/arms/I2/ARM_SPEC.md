# I2 — DAG Hierarchy Arm: Representation Specification

**Arm:** I2 (family STRUCT, Track A)  
**Frozen mechanism:** "Multi-parent: one span, several wholes; attach-vs-form deterministic rule."  
**Status:** See VERDICT.md  
**Date:** 2026-09-21

## 1. What I2 is

I2 inherits I1's single-parent hierarchy and generalizes it: each chunk
(span) carries up to **P=3** parent slots in a fixed integer array
(`-1` = empty, ordered by slot). A span may belong to several superchunks
simultaneously — "one span, several wholes."

## 2. Segmentation (spans)

Spans are maximal runs of one byte-class, with a 64-byte cap (longer runs
split). Byte classes:

- class 1: ASCII alphanumeric + underscore (`0-9`, `A-Z`, `a-z`, `_`)
- class 0: all other bytes

This segmentation is fixed, deterministic, and language-neutral. It is the
arm's declared chunking, not I1's emergent boundaries; the difference is
documented as a deviation in §7.

## 3. Superchunk formation (attach-vs-form)

Candidate superchunks are span-content sequences of 2–8 spans recurring at
least **T_co = 7** times in the corpus (T_co = 7 frozen from I1). Discovery
order is deterministic: window width 2→8, then corpus position order.

**Attach-vs-form rule (frozen, deterministic):** the first occurrence of a
span-ID sequence in discovery order **forms** the superchunk record; every
later identical occurrence **attaches** (occurrence count increments, no new
record). There is exactly one record per distinct qualifying sequence.

## 4. Parent links (P=3)

Each distinct span holds `parents[3]`, filled in group-discovery order.
A link is added when a span is a member of a newly discovered group,
unless that group is already linked (no duplicates). If all 3 slots are
occupied, the new link is **refused** and counted (`overflow3`). No
ranking, scoring, or value judgment is applied — the unfrozen
"highest superchunk value, tie → lowest slot" policy is NOT adopted.

## 5. Parent arbitration (the measured rule)

When a bottom-up query asks "what is this span part of?", the arm's
deterministic arbitration is **slot 0** — the lowest occupied parent slot
(the earliest-attached parent in discovery order). No occurrence context
is consulted. This is the literal reading of "ordered by slot."

## 6. Demotion

Demotion removes **one parent link at a time** (lowest occupied slot
first). A superchunk record dies only when its last parent link (and last
reference) disappears; member spans survive the death of any parent.

## 7. Eviction

On a full store, the arm evicts the oldest unpinned record
(`b_evict_oldest_unpinned`), frees its chunk for reuse, and never evicts
pinned records. Dead records are reused before any growth.

## 8. Controlled P=1 comparator

To measure record savings honestly, the arm builds a controlled
single-parent comparator over the **same** discovery: one parent slot per
span; a span claimed by a second superchunk is **duplicated** (a new span
record parented to the claiming superchunk). Record counts:

- R1 (P=1) = (# groups) + (# span-membership pairs)
- R3 (P=3) = (# groups) + (# distinct spans with ≥1 parent)
- savings = (R1 − R3) / R1

## 9. Battery behavior (M1–M9)

The arm runs the full 1x battery (M1–M9) as an ID arm with provisional
A15/A7/A8 conventions marked PROVISIONAL-PENDING-FREEZE. Hierarchy
evidence (record counts, arbitration error, demotion, eviction) is
measured in the dedicated `i2-hier-1x` mode over the r1 corpora.

## 10. Determinism

Zero RNG in any decision path. Byte-identical reruns required; any M8
byte difference is disqualifying.
