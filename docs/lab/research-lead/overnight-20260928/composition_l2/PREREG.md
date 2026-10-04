# PREREG: Composition L2 Adaptive Reuse

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
No kill bar below may be weakened or reinterpreted after results are seen.

## Hypothesis

The unified composition DFS (mechanisms A+B+C, `composition_unified/un_patch.zag`)
fails L2 because it has no MAP adaptation operator: a MAP whose relation
sequence does not exactly fit the goal's facts is either used whole or not at
all. We add three adaptation operators as STANDING candidate-generation rules
inside `un_candidates`:

- EXTEND: if a MAP's constraint walk (its `cc_relseq` relation sequence)
  succeeds from the DFS cursor, greedily continue with the MAP's LAST relation
  while matching facts exist, up to 3 extra links. Candidate variant 1000+ext.
- TRUNCATE: if the constraint walk FAILS, try proper prefixes of the relseq
  (L-1 down to 1); the longest satisfiable prefix becomes candidate variant
  2000+plen.
- SPECIALIZE: if any step of the default walk was AMBIGUOUS (2 or more live
  facts share subject+relation, counted by a new `lu_count2` helper), re-walk
  choosing at each ambiguous step the fact whose object is nearest the segment
  start value (a locality prior computed from data at runtime, no domain
  labels). Candidate variant 3000.

## Learner-triggered, not researcher-invoked

The operators are evaluated for EVERY candidate MAP at EVERY DFS level. They
fire solely on structural preconditions computed from learner state:
relseq satisfiability, existence of continuation facts, observed ambiguity.
The researcher never selects an operator per problem. The causal control is a
one-line `adapt_on()` toggle (1 vs 0); the NA build differs by exactly that
line, and must reproduce the old L2 failure.

## Mechanism trace predictions (design-derived, not kill bars)

- L2-TREAT: X walks 101->104 by constraint, extends via fact (104,1,105) to
  length 4; DFS continues from 105 with Y (3 r2 links) to 108. Expect
  ADAPT-STAT ext=1, trunc=0, spec=0.
- L1-TREAT: no extension possible, no ambiguity, constraint walks succeed.
  Expect ADAPT-STAT ext=0, trunc=0, spec=0 (behavior identical to baseline).
- TR-TREAT: X2=[1,1,1,1] constraint walk fails from 101; longest satisfiable
  proper prefix is plen 2 (101->103); Y2=[2,2,2,2] covers 4 r2 links to 107.
- SP-TREAT: default walk takes the distractor branch (taught first, lowest
  node id wins `t2_lu_first`); ambiguity at step 1 triggers the specialized
  nearest-object walk 101->102->103->104.

## Frozen kill bars

- K1: L2-TREAT ans=108.
- K2: L1-TREAT ans=107 (no regression vs the L1 baseline).
- K3: L2-ABL-X ans=-2, L2-ABL-Y ans=-2, L2-FRESH ans=-2.
- K4: L2-NOADAPT (adapt_on=0 build) ans=-2.
- K5: TR-TREAT ans=107; TR-NOADAPT ans=-2; TR-FRESH ans=-2.
- K6: SP-TREAT ans=107; SP-NOADAPT ans=-2; SP-FRESH ans=-2.
- K7: L2-PROV: LINK14 MAP_Z->X = 1 and LINK14 MAP_Z->Y = 1.
- K8: L2-REUSE ans=108.
- K9: L2-TREAT ADAPT-STAT ext_gen >= 1; L1-TREAT ADAPT-STAT ext_gen = 0.
- K10: L2-TREAT ADAPT-STAT satisfy_calls < 200 (bounded adaptation cost).
- K11: 3/3 runs byte-identical per binary; sha256 digests recorded.
- K12: all deliverables contain zero em/en dash bytes (verified by byte scan).

## Battery specification (exact)

Shared: X trained by facts (11,1,12),(12,1,13),(13,1,14) and ev_query(11,71,14);
Y trained by (21,2,22),(22,2,23),(23,2,24) and ev_query(21,72,24);
30 gap facts (5000+i, 60+(i%10), 6000+i) for i in 0..29.
X2 trained by (11,1,12),(12,1,13),(13,1,14),(14,1,15) and ev_query(11,71,15);
Y2 trained by (21,2,22),(22,2,23),(23,2,24),(24,2,25) and ev_query(21,72,25).

- L1-TREAT: Z (101,1,102),(102,1,103),(103,1,104),(104,2,105),(105,2,106),
  (106,2,107); query (101,70,107).
- L2-TREAT: Z (101,1,102),(102,1,103),(103,1,104),(104,1,105),
  (105,2,106),(106,2,107),(107,2,108); query (101,70,108).
- L2-ABL-X: as L2-TREAT but subjects 11..14 killed. L2-ABL-Y: subjects 21..24
  killed. L2-FRESH: no X/Y training at all.
- L2-REUSE: after L2-TREAT in the same workspace, repeat query (101,70,108).
- L2-PROV: LINK14 checks on promoted MAP_Z.
- TR-TREAT: X2/Y2 trained; Z (101,1,102),(102,1,103),(103,2,104),
  (104,2,105),(105,2,106),(106,2,107); query (101,70,107).
- TR-NOADAPT: same in the adapt_on=0 build. TR-FRESH: no training.
- SP-TREAT: X/Y trained; Z taught in this order: (101,1,5001),(5001,1,5002),
  (5002,1,5003) [distractor branch, taught first], then (101,1,102),
  (102,1,103),(103,1,104),(104,2,105),(105,2,106),(106,2,107);
  query (101,70,107).
- SP-NOADAPT: same in the adapt_on=0 build. SP-FRESH: no training.

## Cost measurement

REPORT.md will carry an L1 vs L2 cost table from ADAPT-STAT (satisfy calls,
variants generated) and RB-STAT (rebind tried/rejected), plus the observed
COMP-SEGS for each passing arm.

## Implementation notes (frozen design)

- Variant of `un_patch.zag` named `l2_patch.zag`; driver `l2_driver.zag`;
  assembled `l2_full.zag` = cc_base + l2_patch + l2_driver; pinned compiler
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- New: `lu_count2`, `lu_pick` (mode 0 = first fact, mode 1 = nearest object),
  `adapt_walk` (constraint walk + greedy extension + ambiguity flag),
  `adapt_trunc_find` / `adapt_trunc_k`, `un_satisfy_v` (variant dispatch),
  `cand_ins` (insertion with variant codes), `adapt_on()`.
- Buffer growth: per-segment ovals slots 8->12, ofids 7->11, allf 72->84
  slots, vbuf/fbuf 32/48 and 28/44 bytes. Max walk 10 links (relseq <= 7,
  extension <= 3).
- `compose_try` emits ADAPT-STAT sat/ext/trunc/spec.
- NA build: `l2_patch_na.zag` via one-line sed (adapt_on 1->0),
  `l2_driver_na.zag` runs only the NOADAPT arms.
