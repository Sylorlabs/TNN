# SEALED FAMILY C2: Shared-step diamond (M1-W3 shape)

**Status:** SEALED. World file hash recorded below BEFORE the sealed run.
Designed post-freeze from PREREG_H1.md section 4.2 only. Independent of the
builder's dev worlds (not seen by this worker).

## World file

`adv_c2_world.txt` (18 lines)

## SHA-256 (pre-run seal)

`94c7bda47f07018ec16d9721c11dc38ea5a379d38821279560a10a2ff163894c`

## ID ranges (adversary-recorded; no collision with battery 40000-49999)

- Subjects: 62001-62007, 62011-62012, 62023-62024 (62000s block)
- Relations: 6201 (A), 6202 (S, shared step), 6203 (B), 6204 (P1 = A-then-S),
  6205 (P2 = B-then-S)
- Objects: 62011-62031 (62000s block)

## Law forms (new; not battery variants)

- A: o = s + 10 via relation 6201, demonstrated on 62001-62002.
- S (shared step): o = v + 5 via relation 6202, demonstrated on the A-outputs
  62011-62012 AND on the B-outputs 62023-62024. One step object used by two
  parent procedures.
- B: o = s + 20 via relation 6203, demonstrated on 62003-62004.
- P1 = A-then-S: o = s + 15 via relation 6204, demonstrated on 62001-62002.
- P2 = B-then-S: o = s + 25 via relation 6205, demonstrated on 62003-62004.

## Event sequence

Demonstrations (12 OBSERVEs):
- A: (62001,6201,62011) (62002,6201,62012)
- S on A-outputs: (62011,6202,62016) (62012,6202,62017)
- B: (62003,6203,62023) (62004,6203,62024)
- S on B-outputs: (62023,6202,62028) (62024,6202,62029)
- P1: (62001,6204,62016) (62002,6204,62017)
- P2: (62003,6205,62028) (62004,6205,62029)

Engagement probe (1 QUERY; demonstrated parent must answer):
- (62001,6204,62016)

Diamond probes (3 QUERYs, novel subjects):
- (62005,6204,62020): P1 on novel 62005 (62005 + 15)
- (62006,6205,62031): P2 on novel 62006 (62006 + 25)
- (62007,6204,62022): P1 on novel 62007 (62007 + 15)
- K-H1-3 bar: at least 2/3 correct, and the engagement probe must be correct.

Collateral probes (2 QUERYs):
- (62002,6204,62017) [demonstrated P1 instance]
- (62011,6202,62016) [demonstrated shared-step instance]

## Rationale for H1

The shared step S (+5) is one logical object linked by two parent graphs
(P1 and P2). Stamped per-instance literals cannot express sharing; per the
prereg, sharing requires one named object linked by two graphs. The three
novel-subject diamond probes force misses through the shared step. White-box
inspection counts learner-created names and reuse events per K-H1-1.
