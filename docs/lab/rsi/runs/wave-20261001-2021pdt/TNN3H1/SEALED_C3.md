# SEALED FAMILY C3: Unseen-subject application (M3-W1 generalization shape)

**Status:** SEALED. World file hash recorded below BEFORE the sealed run.
Designed post-freeze from PREREG_H1.md section 4.3 only. Independent of the
builder's dev worlds (not seen by this worker).

## World file

`adv_c3_world.txt` (6 lines)

## SHA-256 (pre-run seal)

`c6d33f698fca096242796d3bad9fbd63eacda227c68740a24aed4f7b3ec4f263`

## ID ranges (adversary-recorded; no collision with battery 40000-49999)

- Subjects: 63001-63006 (63000s block)
- Relations: 6301 (R)
- Objects: 63008-63013 (63000s block)

## Law forms (new; not battery variants)

- R: o = s + 7 via relation 6301, demonstrated on seen subjects 63001-63004.

## Event sequence

Demonstrations (4 OBSERVEs):
- (63001,6301,63008) (63002,6301,63009) (63003,6301,63010) (63004,6301,63011)

Unseen-subject probes (2 QUERYs, novel subjects 63005-63006):
- (63005,6301,63012): R on unseen 63005 (63005 + 7)
- (63006,6301,63013): R on unseen 63006 (63006 + 7)
- K-H1-4 bar (INFORMATIONAL, not verdict-binding): at least 1/2 correct.

## Rationale for H1

A named procedure demonstrated on seen subjects is probed on unseen
subjects. Per the prereg, parameterization beyond naming is H8's claim, not
H1's; this family is coverage only. White-box inspection still counts
learner-created names for the K-H1-1 record.
