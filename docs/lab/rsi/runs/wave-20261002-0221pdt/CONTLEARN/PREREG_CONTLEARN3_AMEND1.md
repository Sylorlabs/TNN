# AMENDMENT 1 to PREREG_CONTLEARN3 (transparent, pre-implementation)

Status: FROZEN with the prereg. Date: 2026-10-02, before any build or run.
No results have been seen; no implementation commit exists yet. This
amendment corrects an internal inconsistency in section 4/5, no tuple,
event count, script, or decision-rule change.

The inconsistency: section 4 defined STORE_OK to include an alive DEP
edge from the MAP to the proposal node. Proposal nodes exist only in the
TREAT instrument, so that definition would make STORE_OK_C fail on the
unmodified CONTROL core and contradict CP-6 (control reproduces the
DEMONSTRATED bar).

The correction (matching the driver, which implements the clean split):

- STORE_OK (both cores): for i in 0..5, map(23001+i,522) exists AND has
  an alive DEP edge to fact(21001+i,511,22001+i) AND the integrate query
  returned 22001+i. Bar: 6/6.
- STORE_PROP_CITE (TREAT only): for i in 0..5, map(23001+i,522) has an
  alive DEP edge to proposal(23001+i,522). Bar: 6/6. On CONTROL the
  expected value is 0/6 (no proposal channel); this is not a bar.
- ORDER_OK (TREAT, CP-1) additionally requires STORE_PROP_CITE == 6/6:
  every engaged machinery event cites its licensing proposal in learner
  state.

CP-2 references STORE_OK == 6/6 on TREAT. CP-6 references STORE_OK_C ==
6/6 on CONTROL with zero PROPOSAL lines. Nothing else changes.
