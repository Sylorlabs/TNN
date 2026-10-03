# PREREG_AMEND2.md -- COMPOSE-LEARNCOMPOSE-1 prereg amendment

Date: 2026-10-03. Worker: COMPOSE-LEARNCOMPOSE-1. Committed BEFORE
any implementation commit.

## Cause

PREREG 1.4 step 2 ("the lowest id with exact contract match") is
ambiguous when the lowest matching id is already assigned to an
earlier instruction. The first implementation allowed reuse, which
collapses distinct program roles: on F-C1 W2, both Y and W legs
adapted to map 35, producing G(Y(X(C)),Y(X(C))) = 4 != 3 and
forcing an unnecessary revision (observed TRIES=5, MODE=REVISE;
expected TRIES=4, MODE=RETRIEVE).

## Clarified rule (1.4, frozen)

Adaptation is INJECTIVE over distinct original ids:
for each instruction in program order,
1. if its original id was already mapped earlier in this
   adaptation (same orig_id), reuse that new id (preserves
   intentional sharing);
2. else the original id, if in [base,base+nm), contract-matching,
   and not already used;
3. else the lowest contract-matching id not already used;
4. else -1 (unmapped).
Reusing one new map for two distinct original roles is forbidden;
a role with no distinct filler is unmapped (then DROP_UNMAPPED).

This is contract-defined, domain-blind, and general (no shape
knowledge). It preserves the prereg's intent (faithful adaptation);
the reuse behavior was an implementation error, not a specified
rule.

## Bar updates (consequences of the clarified rule)

- W2: ANS=3, TRIES=4, WIDEN=0, MODE=RETRIEVE, SIM=3, NEGREC=0.
  (Adaptation [34,35,36,37]; 4 execs; success.)
- W3: ANS=9, TRIES=3, WIDEN=0, MODE=REVISE, SIM=2, NEGREC=0.
  (X unmapped; injective i1->f1(46), i2->f2(47); DROP_UNMAPPED ->
  [46(C),47(C),48(i0,i1)]; 3 execs; 9==9. Repair, no revision.)
  NOTE: W3 base moved 38->46 to avoid substrate map-id-40 collision
  (772+40*32=2052 overlaps the nm counter; pre-existing BACKCHAIN
  substrate bug, not a C mechanism issue). Contracts and sketch
  unchanged.
- FANIN (main): ANS=9, TRIES=3, WIDEN=0, MODE=REVISE, SIM=2,
  NEGREC=0. (Same shape as W3: [8(C),9(C),10(i0,i1)]; 3 execs.)
- ADV: ANS=3, TRIES=8, WIDEN=0, MODE=REVISE, SIM=3, NEGREC=1.
  (Adapted [42,43,44,45] -> 5 != 3; R2 TRUNCATE k=2 -> [42,43] -> 3.
  The 8 tries include re-execution in the revision valuator; the
  operator order and outcome are per-spec.)
- F-C3b: E0.FAIL=1 (not 2). W3 now succeeds via repair (no failure
  recorded); only ADV records negative evidence. F-C3a (NEGREC=1,
  MODE=REVISE on ADV) unchanged.

F-C1a (T2<T1): 4<7. F-C1b (T3<T1): 3<7. Both hold.
