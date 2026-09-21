# ARM I1 — Strict Tree Hierarchy (`STRUCT`) — Specification

**Track:** A (representation bake-off)
**Arm ID:** I1
**Mechanism:** Strict tree hierarchy
**Status:** Frozen prereg `sylorlabs/TNN`, branch `tnn-native-lab`, commit `b0b9140c0eda`
**Date:** 2026-09-21

## 1. Mechanism (frozen)

I1 stores knowledge as a strict tree hierarchy of chunks:

- **Level 0:** finest chunks (fixed 64-byte grid units at ingest).
- **Formation:** runs of 2–8 adjacent same-level chunks become superchunk
  candidates after `T_co = 7` co-recalls (a co-recall = one fixed 8-block
  region recalled in one rehearsal episode), or via deliberate promotion.
- **Single parentage:** every unit has at most one parent. IDs are
  level-scoped: `id = (level<<27) | (corpus<<24) | serial`.
- **Traversal:** top-down and bottom-up.
- **Maximum level:** 4.
- **Demotion:** after `E` quiet episodes (no recall), a superchunk demotes
  (children detach, unit drops one level). `E` is **PROVISIONAL** (`E=3`)
  pending freeze resolution (`PREREG_FREEZE.md:99`).
- **Revision:** revising a unit marks its **ancestors** stale. Stale parents
  must be rebuilt or dissolved — never silently served.

## 2. Binding kill criteria (frozen, `PREREG_FREEZE.md:502`)

The arm dies if **any** fires at 1x:

1. **(i)** Level-2+ superchunks account for `<5%` of successful recalls at
   equal store cost versus flat chunks.
2. **(ii)** Parent maintenance + stale rebuild exceeds `20%` of total audit
   operations on any corpus.
3. **(iii)** Level-1 boundary agreement with natural breaks `<50%` on
   corpus A.

## 3. Interpretations (NOT frozen — provisional, nonbinding)

The freeze does not define:

- **Natural breaks:** implementation treats a boundary as natural if it is
  at a corpus edge or preceded by whitespace (` `, `\n`, `\t`, `\r`).
  Run formation prefers (not requires) whitespace-aligned ends:
  score = `16*natural + run_length`, longest wins on ties.
- **"Runs of 2–8":** left-to-right scan; at each parentless position the
  eligible 8-block must reach `T_co`; among valid run lengths 2..8 the
  highest-scoring (break-aligned, then longest) is chosen.
- **E (demotion episodes):** `E=3`, labeled PROVISIONAL-PENDING-FREEZE.
- **M8 instance:** combined M1+M3 instance (A17 unresolved; combined
  chosen provisionally).
- **I1 as ID arm:** provisionally treated as ID arm per
  `ARM_INTERFACE.md §9`; M1 swap probe and M7 lookup battery retained.

No provisional interpretation was used to trigger a binding kill.

## 4. Invariants (enforced)

- Single parentage: `attach` refuses if child already parented or parent
  has 8 children.
- No silent stale: `recall_content` returns -1 for `F_STALE` units.
- ID uniqueness: level-scoped serials per (corpus, level); collision
  probes cover corpus 8 (the former overlap bug is fixed).
- Determinism: zero randomness in any decision path; byte-identical
  reruns verified (M5 ×2, M8 ×3 perturbations).

## 5. Battery modes (1x)

| Mode | Corpus | Purpose |
|------|--------|---------|
| m1-1x-prose / m1-1x-code | prose / code | Recall + boundary fidelity + swap probe |
| m2-t1-prose / m2-t1-code | tier-1 | Compositional recall, ETC |
| m2-t2-prose / m2-t2-code | tier-2 | |
| m2-t3-1x | tier-3 | |
| m3-1x | churn | 3000 fresh → 3000 kills → 4000 fresh |
| m4-1x-prose / m4-1x-code | prose / code | 200 defects → revise-or-kill |
| m5-1x | prose | Footprint (bytes/unit) |
| m6-p2c-1x / m6-c2p-1x | prose↔code | Transfer |
| m7-1x | prose | ID→slot lookup battery |
| m8-1x | all | Combined determinism artifacts |

M9 (takeoff shape) is reported inside M2 modes as `m9_*` fields.
