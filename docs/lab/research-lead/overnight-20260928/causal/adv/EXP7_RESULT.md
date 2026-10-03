# H-EXP7 Result: H-EXP7 SURVIVES (5/5)

**Date:** 2026-09-29
**Prereg:** causal/adv/PREREG_EXP7.md (commit a9814aa83, frozen
before any implementation; verified strict ancestor of the result
commit below)
**Implementation:** causal/adv/exp_invent7.zag (exp_invent6.zag
VERBATIM + exactly the 5 frozen additions; diff shows 149 added
lines, 0 removed)
**Raw evidence:** causal/adv/evidence/exp7_{s1,s2,s0,a1,f1,g1,h1}_raw.txt
(3/3 byte-identical runs per fixture; md5s below)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere (no generators, verifiers,
analysis, or scratch). Binaries built in /tmp only, not committed.
No em dashes in loop documentation.

## Verdict: H-EXP7 SURVIVES (5/5)

Both H-EXP6 red-team downgrades are closed at the mechanism level.
Classification: bounded L2 discriminating-state selection with
honest transition-level reporting. Not L3: no new representation is
invented; the vocabulary (actions, variables, values) is given by
the episode format.

## The repair (5 frozen additions, nothing else changed)

1. **trans index helpers** (trans_idx/trans_get/trans_add): 108 i32
   cells indexed (((a*3)+v)*3+o)*3+x, z_alloc(432), separate memory.
2. **compute_transitions**: for EP_ACT episodes, on the exact raw
   change predicate compute_controllable uses (ns != os), counts
   action a changing variable v FROM clamped o TO clamped x.
3. **emit_trans_table / emit_trans_row**: TRANSITION TABLE after the
   CHANGE-TO TABLE; rows list only nonzero from->to cells, e.g.
   `TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`.
4. **emit_transition_evidence**: TRANSITION-EVIDENCE line after every
   CHANGE-EVIDENCE line (ranked picks indented, top pick not). Per
   required (variable,value): per change-action `a: from {o:c,...}
   (m/n)` where m = change-to episodes, n = outcome episodes for
   that action; `transitions: none` when no change observed.
   Carryover-only is not repeated (it stays in the CHANGE-EVIDENCE
   line directly above).
5. **Legend extension**: one frozen sentence appended after the
   EXP5/EXP6 legend text (byte-identical).

## Frozen kill-bar evidence

- **K-E7-1 PASS (X-E6-1 closed):** On G1, ranked pick [2] (2 0 0)
  TRANSITION-EVIDENCE line:
  `temp==2 transitions: 0: from {1:3} (3/4); 1: from {0:2} (2/2); ...`
  Contains the frozen substrings "0: from {1:3} (3/4)" and
  "1: from {0:2} (2/2)". A planner at temp==0 now sees that only
  action 1 ever effected the 0->2 transition, while action 0's
  three temp->2 changes were all from temp==1.
- **K-E7-2 PASS (X-E6-2 closed):** On H1, the ranked pick requiring
  temp==2 TRANSITION-EVIDENCE line:
  `temp==2 transitions: 0: from {1:1} (1/11); 1: from {0:1} (1/1); ...`
  Contains the frozen substrings "0: from {1:1} (1/11)" and
  "1: from {0:1} (1/1)". The 1-in-11 change no longer renders
  identically to the 1-in-1 change.
- **K-E7-3 PASS (no regression):** K-E6-1, K-E6-2, K-E6-4 checks
  reproduce on exp7 outputs. All 7 fixtures (S1,S2,S0,A1,F1,G1,H1)
  are byte-identical to committed-source exp6 outputs with the
  added lines excluded (cmp clean on all 7): the only added lines
  are the TRANSITION TABLE block, one TRANSITION-EVIDENCE line per
  pick, and the legend sentence. K-E6-1 substrings present 3x each
  on F1; K-E6-2 substrings present on S1.
- **K-E7-4 PASS (determinism):** 3/3 byte-identical runs per
  fixture. md5s: S1 fffd7b90df92bd818425faeafcb39879,
  S2 cfcd78710ea1fd4fc11a1efcba6b23bd,
  S0 166126b807aa5f3d1ec3f389d80463df,
  A1 330eff81a35ad932f2eb894017983139,
  F1 f182d8a6a0523d04d531367bde0fd866,
  G1 4b7e445a19f28b5d05d41363b96ed9fd,
  H1 2151589e50be604cd0d92f039c2e3d86.
- **K-E7-5 PASS (table consistency):** On F1, the TRANSITION TABLE
  contains the frozen hand-verified row
  `TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`.
  Structural invariant spot-checked on G1: for every (a,v,x),
  sum over o of trans[a][v][o][x] == chgto[a][v][x] (e.g. a0 temp:
  x=1: 1==1, x=2: 3==3; a1 temp: x=0: 1==1, x=1: 1==1, x=2: 2==2).

## Honest limits (carried from the frozen prereg)

- Transitions are observed change, not causal attribution and not
  a capability guarantee.
- From/to values are clamped to 0..2 like outcomes; the change
  predicate uses raw values, so a raw 5->2 renders as 2->2.
- The (m/n) rate is a per-action outcome denominator inside the
  observed episode set; it does not measure robustness or
  reproducibility.
- No setup planning; no state-as-combination reachability.
- Actions outside 0..3 are not represented.

## Commit lineage (branch tnn-native-lab, local only)

- a9814aa83: PREREG H-EXP7 FROZEN (alone; before any implementation)
- this commit: exp_invent7.zag, EXP7_RESULT.md (this file),
  evidence/exp7_{s1,s2,s0,a1,f1,g1,h1}_raw.txt (only owned files
  staged; concurrent workers' files untouched)
- Ordering: prereg is a strict ancestor of this commit
  (verified via merge-base --is-ancestor before pushing the
  commit message).

## Suggested follow-up for parent

H-EXP7 now warrants an independent red team (natural attacks:
X-E7-1 a fixture where from-value counts mislead about
reproducibility, e.g. coincidental from-values; X-E7-2 probing
whether a 1/1 rate over-weights a lone episode; X-E7-3 a clamp
edge case where raw 5->2 renders as 2->2). The research paper's
NQ3 line should be updated to H-EXP7 SURVIVES (5/5).
