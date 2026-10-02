# SEALED FAMILY C1: Composition (M1-W1 shape)

**Status:** SEALED. World file hash recorded below BEFORE the sealed run.
Designed post-freeze from PREREG_H1.md section 4.1 only. Independent of the
builder's dev worlds (not seen by this worker).

## World file

`adv_c1_world.txt` (24 lines)

## SHA-256 (pre-run seal)

`7b37daaec113c84c25789f6a8333dc7ccd285d6a98d7a680900364e9cc8249b3`

## ID ranges (adversary-recorded; no collision with battery 40000-49999)

- Subjects: 60001-60048 (60000s block)
- Relations: 6101 (P), 6102 (Q), 6103 (P-then-Q composition)
- Objects: 60011-60078 (60000s block)

## Law forms (new; not battery variants)

- P: o = s + 10, demonstrated on subjects 60001-60004 via relation 6101.
- Q: o = v + 20, demonstrated on the P-outputs 60011-60014 via relation 6102.
  P and Q are demonstrated on disjoint subject sets (60001-60004 vs 60011-60014).
- Composition law: o = s + 30 via relation 6103 (never demonstrated).

## Event sequence

Demonstrations (10 OBSERVEs):
- P: (60001,6101,60011) (60002,6101,60012) (60003,6101,60013) (60004,6101,60014)
- Q: (60011,6102,60031) (60012,6102,60032) (60013,6102,60033) (60014,6102,60034)
- Swapped (decoy setup): (60005,6101,60016) [true P = 60015];
  (60021,6102,60042) [true Q = 60041]

Composition probes (8 QUERYs, novel subjects 60041-60048, relation 6103):
- (60041,6103,60071) (60042,6103,60072) (60043,6103,60073) (60044,6103,60074)
  (60045,6103,60075) (60046,6103,60076) (60047,6103,60077) (60048,6103,60078)
- Correct requires P-then-Q composition (s + 30). K-H1-2 bar: at least 6/8.

Decoy probes (4 QUERYs; punish memorization of demonstration values):
- (60005,6101,60015): demonstrated 60016 (swapped). Returning 60016 counts
  as a memorized value.
- (60021,6102,60041): demonstrated 60042 (swapped). Returning 60042 counts
  as a memorized value.
- (60005,6103,60035): composition on swapped-P subject; never demonstrated.
- (60021,6103,60051): composition on swapped-Q subject; never demonstrated.
- K-H1-2 decoy condition: at most 1/4 returning memorized values.

Retention probes (2 QUERYs, collateral):
- (60001,6101,60011) [demonstrated P instance]
- (60011,6102,60031) [demonstrated Q instance]

## Rationale for H1

Composition is not in any menu (deleted). Per the prereg, it must be
expressed as a named sequence referencing two named procedures, or not at
all. The eight novel-subject probes force misses; the miss path is the only
learner-driven construction opportunity in the event interface. White-box
inspection after the run counts learner-created names and reuse events
per K-H1-1.
