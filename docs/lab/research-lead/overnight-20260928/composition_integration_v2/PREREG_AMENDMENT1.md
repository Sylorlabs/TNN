# PREREG AMENDMENT 1: H-COMPINTEG-2 query-relation fix

Status: FROZEN 2026-10-02. Committed before the redesigned
implementation is run. The original PREREG.md stands; this
amendment corrects a battery-design flaw discovered during
implementation testing (probe run, not a verdict run). No kill
bar is weakened: K1-K11 keep their meaning, with corrected
hand-derivations below.

## Flaw (fatal under guards): query relation collides with world
facts in the (101,70) arms

The I1/I3/I5/G2/G3 arms query relation 70 while the Z-world
chain facts also use relation 70: (101,70,102),(102,70,103),
(103,70,104). In explore cycle 1, lv_predict(101,70) returns 102
(the live world fact (101,70,102), via the FACT scan, not the MAP
fallback), and lv_observe(101,70,108) then treats the world fact
as a contradicted prediction: it supersedes (101,70,102) via a
self type-3 edge and teaches FACT(101,70,108).

In C295's unguarded run this was harmless (t2_exec replayed
without a liveness check, so cycles 2-4 rebuilt trials on the
superseded fact and the FACT score reached 3). Under GUARD-T3 it
is fatal: every cycle-2+ trial licenses the superseded
(101,70,102), the licensing-liveness veto fires, t2_try_verify
rejects, adapt_extend creates nothing, the FACT score stays 0,
and the query withholds (-3). The guard is correct to refuse
building on superseded facts; the battery design was flawed
(the C295 relation-70 query was an Amendment 1 visibility hack
that is no longer needed, since GUARD-T1's provenance gate
blocks learner-originated alternatives regardless of relation).

## Redesign (frozen)

The (101, *) arms query relation 79 (a fresh relation with no
world facts and no MAP field-4 == 79), instead of 70. Z-world
chain facts keep relation 70 (the trial must extend MAP_X's
[70,70,70] relseq). All other setup is unchanged.

Consequences (frozen):
- lv_predict(101,79): no FACT(101,79,*), no MAP with field 4 ==
  79, so the MAP fallback finds nothing executable from 101;
  returns -999999 on cycle 1 (no basis), exactly as the C295
  derivation assumed.
- lv_observe(101,79,v): activate(101,79) finds no fact, so it
  teaches FACT(101,79,v) via ev_teach_in with NO supersession.
  World Z facts are never superseded by the learner; trials
  always license live non-superseded facts; GUARD-T3 never fires
  on the legitimate path.
- Prediction FACTs now carry r=79 != 70 = R[j]. They would be
  visible to adapt_specialize's r_alt != R[j] scan, but
  GUARD-T1's provenance gate blocks them (all are
  learner-originated via ev_teach_in). The Amendment 1
  relation-invisibility trick is superseded by the guard; the
  arm no longer depends on it.
- integ_explore and compose_integ2 take the query relation as a
  parameter; the driver passes 79 for the (101, *) arms.

## Corrected hand-derivations (I1/I3/I5/G2/G3)

- I1: explore x4 integ_explore(W,101,79,op=1,retire=1). Cycle 1:
  adapt_extend creates one trial [70,70,70,2] (frontier 104 via
  live fact (104,2,108); 101 -(70)-> 102 -(70)-> 103 -(70)-> 104
  -(2)-> 108), executes to 108, lv_predict returns -999999 (no
  basis), lv_observe teaches FACT(101,79,108) score 0 (no
  supersession). Cycles 2-4 predict 108 and confirm; score
  reaches >= 3. Query compose_integ2(W,101,79): lv_setup
  predicts 108 rel >= 3; native DFS fails (MAP_X ends at 104);
  bracket: integ2_revise finds no live adapted MAP; fresh
  operators create a=[70,70,70,2] and t=[70,70]; specialize
  creates nothing (GUARD-T1 blocks the learner-originated
  (101,79,108) FACT; no other r != 70 facts at the links);
  integ_tag_extend records kind 1 on a. lv_dfs terminates at
  108 via a. Verify 108 == 108 (licensing live, GUARD-T3
  silent; GUARD-T2 silent: licensing facts are world-channeled).
  Promote MAP_Z with LINK14 to a.
  Expect: ans=108; a type-16->MAP_X, relseq [70,70,70,2],
  kind 1; MAP_Z LINK14->a; exactly 2 live adapted MAPs;
  explore FACT(101,79,108) score >= 3.

- I3: setup as I1 through explore (query relation 79);
  q1=compose_integ2(W,101,79) -> 108 with MAP_Z LINK14->a.
  World change: teach (104,2,140), kill (104,2,108).
  q2=compose_integ2(W,101,79): lv_setup predicts 108 rel 3
  (FACT(101,79,108) persists); native DFS finds nothing at 108;
  bracket: integ2_revise finds a STALE (cc_relseq unreadable:
  licensing fact dead; probe agrees), kind 1, rev_extend_src
  builds a2=[70,70,70,2] via (104,2,140): 101 -(70)-> 102
  -(70)-> 103 -(70)-> 104 -(2)-> 140, type-16 a2->a, retires a;
  lv_dfs: a2 ends at 140 != 108. Expect: q1=108; q2=-2; a
  retired; a2 live, relseq [70,70,70,2], type-16 a2->a; no
  LINK14 targets a2; FACT(101,79,108) score still 3.

- I5: continue I3's workspace; retire stale MAP_Z; up to 10
  explore cycles integ_explore(W,101,79,op=1,retire=0); stop
  when lv_setup(W,101,79) returns 140 rel >= 3; q3=
  compose_integ2(W,101,79). Expect: cycles <= 10; q3=140;
  MAP_Z2 LINK14->a2.

- G2: as I3 (query relation 79) with the veto assertions:
  q1=108; q2=-2; a retired; a2 live, type-16 a2->a (revision
  fires); type-14 count unchanged across q2 and no LINK14->a2
  (no circular promotion); FACT(101,79,108) score 3.

- G3: continue G2's workspace; as I5 (query relation 79).
  Expect: cycles <= 10; q3=140; MAP_Z2 LINK14->a2.

- I4: query compose_integ2(W,101,79) with no explore:
  lv_predict finds no FACT(101,79,*) and no MAP field 4 == 79;
  withholds -3. Expect: ans=-3; zero type-16; 1 live MAP.

I2, I6, G1, S1 are unchanged (their query relations 72/74 do
not collide with world facts).

## Kill bars

K1-K11 unchanged in meaning; the (101, *) arms use the
corrected derivations above. K10 (hygiene) and K11 (frozen
integrity, commit order) stand. This amendment was frozen and
committed before the redesigned implementation was run; the
probe run that motivated it was an implementation test, never
a verdict run.
