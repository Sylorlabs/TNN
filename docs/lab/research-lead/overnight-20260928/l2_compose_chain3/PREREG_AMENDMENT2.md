# PREREG_AMENDMENT2: Z MAP id bookkeeping (3,4,5 not 4,5,6)

Frozen pre-verdict 2026-10-03, transparent correction.
The second build-E run (exploratory) confirmed the
mechanism exactly (QD3 op=4 tries=16 val=65; QD4
tries=24; both ablations and the control match their
predicted op/tries/val), but the in-Zag Z-exact and
t16-edge checks failed: this worker's PREREG_AMENDMENT1
kept compose2's Z ids (4,5,6) while the mB' removal
leaves only 3 taught MAPs (mD' id 0, mA' id 1, mP' id
2), so map_create assigns Z4->3, Z5->4, Z6->5.

## Corrected id mapping (supersedes the ids in
PREREG.md section 6 and PREREG_AMENDMENT1)

- Z4 = 3(1,7,90,97,1,1,29,26,27,3,4,0),
  facts[15,16,17,18,19,20,21], e_add(3,2,16).
- Z5 = 5->4: 4(1,7,140,148,1,1,29,22,23,3,4,0),
  facts[23,24,25,26,27,28,29], e_add(4,3,16).
- Z6 = 6->5: 5(1,7,160,167,1,1,23,22,23,3,4,0),
  facts[31,32,33,34,35,36,37], e_add(5,4,16).
- FULL: QD1 via=3; QD2 via=4; QD3 via=5; re-asks
  via 3/4/5 entered=0. t16=3: e_has(3,2,16)=1,
  e_has(4,3,16)=1, e_has(5,4,16)=1;
  e_has(5,2,16)=0, e_has(3,1,16)=0,
  e_has(4,2,16)=0; LINK14 to 3, 4, 5.
- ABLATE-INV: t16=2: e_has(3,2,16)=1,
  e_has(4,3,16)=1, e_has(5,4,16)=0.
- ABLATE-ABS: t16=3 (correction: AMENDMENT1 wrote
  t16=2, inconsistent with its own three listed
  edges): e_has(3,2,16)=1, e_has(4,2,16)=1,
  e_has(4,3,16)=0, e_has(5,4,16)=1.
- CONTROL: t16=1: e_has(3,2,16)=1,
  e_has(3,1,16)=0; LINK14 to 3; QD1 via=3,
  QD1-B via=3 entered=0.

All op/tries/dec/val/phit predictions are unchanged;
only MAP-id-dependent checks (via, Z-exact ids, t16
edges, LINK14 targets) shift by one. No bar was
weakened: the 3-chain signature (QD3 op==4,
tries==16, val==65, Z6-exact==1) and the termination
signature (QD4 tries==24) are unchanged in form.
