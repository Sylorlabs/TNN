# PREREG — W17 CORROBORATION CODEC (grok W9, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

Belief as a compression fact — canonical key with an EXT producer-set of
cardinality ≥ 2, both claims C3-passing, GEN never corroborating — catches
strictly more GEN→EXT laundering than C3 alone while holding correct-admit in
the K3 band, because the frozen honest tape's true claims repeat across
producers and the launders do not.

## 2. Mechanism (frozen, pure Zag, zero RNG)

Per proposal (ADD §5 pipeline through features): canonicalize → triple key
`(subject_hash, predicate_id, object_hash)` → binary-search KeyIndex (sorted;
B-tree fanout 16 per grok, page invariant — implemented as sorted vectors with
binary search + memmove, O(log N) search, O(N) worst-case insert memmove which
is linear and K4-legal) →
- **Miss:** append singleton, `belief_bit=0`, QUARANTINE. C3 recorded as
  `c3_preview` only (emitted in OUT, cannot publish).
- **Hit, same object, same producer:** exact duplicate; write nothing new.
- **Hit, same object, new producer:** insert producer into the sorted set;
  publish this claim as belief iff frozen C3 bit=1 on this claim AND ∃ prior
  claim with same triple, different producer, class≠GEN, whose C3 bit=1.
  GEN-class producers never corroborate (a GEN in the set does not satisfy
  the ∃).
- **Hit, same subject+predicate, different object:** ContradictionRec;
  `belief_bit=0` on every key under that subject+predicate; C3 cannot override.
- Parse-failing clauses are skipped (not claims).

**"Admit" mapping:** `dec=1` iff `belief_bit=1` (cardinality ≥ 2 with the
C3-conjunction above). QUARANTINE counts as not admitted.

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78%).
- **K6/K8** adopted per ADD §8.
- **K-CC-1:** any belief record with producer-set cardinality < 2 → KILL
  (OUT lines carry the set size; scorer verifies).
- **K-CC-2:** any belief record whose producer-set relied on a GEN-class
  producer to reach cardinality 2 → KILL.
- **K-CC-3:** both sides of a contradiction present as belief → KILL.
- **K-CC-4:** laundering-subset (4 LAU) catch ≤ C3-only (0/4) → KILL.
- **K-CC-5:** probe P-CC5 (ADD §6 item, named before any run) published as
  belief → KILL.

## 4. Predicted outcome

Honest C rows share one triple across producers 1/2/10: first sighting
quarantines; once two distinct EXT producers with C3 bit 1 exist, further
C3-passing rows publish → correct-admit ≈ 789/1102 ≈ 71.6% (K3 band). LAU
(all producer 4, GEN): singletons/duplicates → 4/4 caught. FRK/FRG:
quarantined (never belief). W rows: quarantined. P pairs: at most one member
reaches belief (members with C3 bit 0 cannot publish; the ∃ requires a
C3-passing prior) → K1 holds. Contradiction path unexercised on the tape
(subjects are per-family, objects uniform) — reported, not a kill (no bar
requires it).
