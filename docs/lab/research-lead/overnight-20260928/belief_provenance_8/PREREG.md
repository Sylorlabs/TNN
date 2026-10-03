# PREREG: BP-8 (multi-channel absorption, large and heterogeneous cycles)

Worker: BELIEF-PROVENANCE-8 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_8/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen forms (BP-2 R1-R7,
bp7_absorb renamed) plus block behaviors probe-measured
2026-10-03 in /tmp/bp8probe (ephemeral; three probe
binaries, all pure Zag under safebin). The 7 falsifiable
predictions (FP1-FP7) stay sealed; this lane tests the
two open dynamics suggested by BP-7: multi-channel
absorption and cycles larger than 5 with heterogeneous
edges.

## 0. What is being tested

Two open-dynamics questions, each with discriminating
kill bars:

- MCH (multi-channel absorption): the frozen absorb
  (BP-5/BP-6/BP-7 convention) counts NEW type-7 and
  type-3 self-edges on ONE fact since watermarks and
  applies at most one R2 (if n7>0) then at most one R3
  (if n3>0). Three delivery shapes: (a) type-7 AND
  type-3 on the SAME fact in one event (match then
  contradict); (b) contradict then match on one fact
  (order reversed); (c) type-7s on fact fM1 and a
  type-3 on fact fM2, same belief (multi-fact).
  Predicted: (a) nets sup 90/conf 0/disc 1 (R2 then
  R3; the R3 zeroes the conf the R2 just set, so the
  bar also pins the frozen application order);
  (b) absorbs ONLY the contradict (sup 80/disc 1):
  the block drops a match that arrives after a
  contradict on the same fact, so absorption is
  order-sensitive at the evidence layer; (c) two
  type-7s on fM1 collapse to ONE R2 (conf 2, not 3:
  per-channel single-application saturation), then
  the fM2 type-3 applies one R3: net sup 90/conf 0/
  disc 1, identical to (a): the layer is fact-blind
  given the same channel multiset.
- CY12 (12-cycle, homogeneous type-14): BP-6 CY5
  showed min-convergence, fixpoint idempotence, and
  snap-up on 5 nodes. Predicted: the same three
  properties hold at 12 nodes (weakened z7=40 spreads
  to all 12 via one backward R6 sweep; re-application
  is idempotent; raising z7 to 80 snaps the ring up
  to all 80 via one backward sweep).
- HET (6-cycle, heterogeneous edges): ring
  v1-14->v2-14->v3-1->v4-14->v5-3->v6-14->v1
  (one type-1 edge, one type-3 edge, rest type-14).
  R6 follows ONLY type-14 edges, so the predicted
  result is that the fixpoint does NOT generalize to
  the graph-theoretic cycle: weakening v4 (just past
  the type-1 edge) is invisible to every R6
  application (v3's R6 is a no-op returning 255),
  and R6(v4) reabsorbs the weakening (v4 back to
  100 from its healthy type-14 successor v5); the
  full sweep converges to all 100, idempotently.
  Behind the type-3 edge: R6(v5) is a no-op (255)
  and a weakening of v6 is likewise reabsorbed.
  The combiner converges per type-14 reachability
  component, not per graph cycle.

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-7's bp7_learner.zag reused VERBATIM
as bp8_learner.zag (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e,
re-verified after copy): record schema (8 u8),
R1-R7, eff(), bp2_bar_after. Constants: BASE=100,
INC_HI=20, INC_LO=10, DEC=20, BAR0=50, MIN_BAR=10.

New learner machinery this lane: NONE. In
particular bp8_absorb is the BP-7 absorb renamed
(identical body: n7>0 -> one R2 indep=0; n3>0 ->
one R3; out carries n7/n3); it is driver-side
test-harness code, NOT a belief-layer change. The
R6 combiner, R2/R3/R5, and the edge-type
restriction of R6 to type-14 stay frozen.

Test-harness code (in bp8_driver.zag, not belief
machinery): bp8_absorb, bp8_selfcnt, bp8_allsup
(all-sup helper for the 12-node bars), world
builders per arm, in-driver bars.

Block behaviors (probe-measured 2026-10-03,
/tmp/bp8probe; frozen block SHA-256
172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a):
- P1 (match then contradict, graph-less fact):
  ev_observe ret 1 then 0; +1 type-7, +1 type-3.
- P2 (contradict then match, graph-less): ret 0
  then 0; +1 type-3, +0 type-7 (later match
  dropped).
- P3 (double match): +2 type-7s, rets 1,1.
- P6 (match then contradict, graph-licensed):
  ret 1 then 0; +1 type-7, +1 type-3 (same as P1).
- P7 (contradict then match, graph-licensed):
  ret 0 then 1; +1 type-3, +0 type-7 on the
  original fact (the ret differs from P2's 0, but
  the absorb-relevant edge counts are identical;
  the ret is emitted, NOT barred).
- P8: absorb net for (n7=1,n3=1) is sup 90,
  conf 0, disc 1 (R2-then-R3 order).
- P4/P5 (rings): 12-node type-14 ring weakens to
  all-40 via one backward R6 sweep, idempotent,
  raises to all-80 via one backward sweep.
- P3b (probe part 3, HET ring): R6 on a node with
  no type-14 successors returns 255 and changes
  nothing; weakening past a type-1 edge is
  invisible to R6 and reabsorbed by R6 on the
  weakened node itself.

## 2. Arm MCH: multi-channel absorption (world W8)

tnn2_init. fS=ev_teach(601,61,10) tag 2;
mS=promote_graph(W8,-1,601,61,10,[fS],1);
bp2_form(mS,0): sup=100, conf=1, ext=1, self=0,
d_self=255.
fR=ev_teach(602,62,20) tag 6;
mR=promote_graph(W8,-1,602,62,20,[fR],1);
bp2_form(mR,0): sup=100, ext=0, self=1.
fM1=ev_teach(603,63,30) tag 2;
fM2=ev_teach(604,64,40) tag 4;
mM=promote_graph(W8,-1,603,63,30,[fM1,fM2],2);
bp2_form(mM,0): sup=100, ext=1, self=1.

Event S (same fact, match first): watermarks on
fS; ra=ev_observe(W8,601,61,10) (=1, match);
rb=ev_observe(W8,601,61,999) (=0, contradict);
bp8_absorb(mS,fS): n7=1, n3=1 -> R2 then R3.
Hand-derived: R2: sup=110, conf=2, disc=0; R3:
sup=90, disc=1, conf=0. Net: 90/0/1. (If the
frozen order were R3-then-R2 the net would be
90/1/0; the bar pins the order.)

Event R (order reversed): watermarks on fR;
rc=ev_observe(W8,602,62,999) (=0, contradict);
rd=ev_observe(W8,602,62,20) (match after
contradict: dropped on the original fact; ret
emitted not barred, probe P7=1 graph-licensed);
bp8_absorb(mR,fR): n7=0, n3=1 -> R3 only.
Hand-derived: sup=80, disc=1, conf=0.

Event M (multi-fact): watermarks on fM1,fM2;
ev_observe(W8,603,63,30) twice (=1,1: two
type-7s); ev_observe(W8,604,64,999) (=0: one
type-3); bp8_absorb(mM,fM1): n7=2 -> ONE R2
(saturation): sup=110, conf=2, disc=0;
bp8_absorb(mM,fM2): n3=1 -> R3: sup=90, disc=1,
conf=0. Net equals event S: fact-blind given the
same channel multiset.

## 3. Arm CY12: 12-cycle homogeneous (world WC)

tnn2_init. z[0..11]=alloc_node, bp2_form(.,1)
each (B-COMP): sup=100. Ring:
link_edge(z[i],14,z[(i+1)%12]) for i=0..11.

Hand-derived (frozen R6 = min over live type-14
recorded targets; R2 indep=1 = +20; R3 = -20):
- 3x R3(z[6]): sup=40.
- R6(z[5]): targets {z[6]} -> 40; z[4],z[11]
  untouched at 100.
- Backward sweep R6(z[5..0],z[11..6]): each
  takes its successor's 40 -> all 40.
- Re-apply R6 all 12: all stay 40 (fixpoint).
- 2x R2(z[6],1): 40->60->80. R6(z[5]) -> 80;
  z[4] stays 40 (it was set to 40 by the FULL
  sweep; the 1-hop does not reach it).
- Backward sweep again (z[6] applied last, its
  successor z[7] already 80): all 80.

## 4. Arm HET: 6-cycle heterogeneous (world WH)

tnn2_init. v[0..5]=alloc_node, bp2_form(.,1)
each: sup=100. Edges: v1-14->v2, v2-14->v3,
v3-1->v4, v4-14->v5, v5-3->v6, v6-14->v1.
(Type-1 and type-3 edges are inert under R6,
which reads only type-14; v3 and v5 have NO
type-14 successors, so R6 on them returns 255.)

Hand-derived:
- 3x R3(v4): v4=40.
- R6(v3): no type-14 successors -> ret 255,
  v3 stays 100, v4 stays 40. The type-1 edge
  blocks the 1-hop that CY5 showed (contrast
  K-CY5-1HOP where the predecessor took the
  min).
- R6(v4): targets {v5}=100 -> v4=100, ret 100.
  The isolated weakening is reabsorbed; in the
  homogeneous ring the weakened node kept 40
  through the sweep because its successor was
  weakened first, which cannot happen here.
- Full sweep R6(v1..v6): all 100 (v5 never
  moves: its only outgoing edge is type-3).
- Re-apply: all 100 (fixpoint).
- 3x R3(v6): v6=40 (w6pre). R6(v5): ret 255,
  v5=100 (the type-3 edge carries nothing).
  R6(v6): targets {v1}=100 -> v6=100.

## 5. Kill bars (frozen)

Preconditions:
- PC-MCH-FORM: mS: sup==100 && ext==1 &&
  self==0; mR: sup==100 && ext==0 && self==1;
  mM: sup==100 && ext==1 && self==1.
- PC-CY12-FORM: all 12 z[i] sup==100.
- PC-HET-FORM: all 6 v[i] sup==100.

MCH bars:
- K-MCH-RETS: ra==1 && rb==0 (block evidence
  codes for match / first contradict).
- K-MCH-SAME: abS n7==1 && n3==1 &&
  b_sup[mS]==90 && b_conf[mS]==0 &&
  b_disc[mS]==1 (both channels absorbed, frozen
  R2-then-R3 order).
- K-MCH-ORD: abR n7==0 && n3==1 &&
  b_sup[mR]==80 && b_disc[mR]==1 &&
  b_conf[mR]==0 (order-sensitive: the later
  match is dropped, only the contradict
  absorbs).
- K-MCH-SAT: abM1 n7==2 && b_conf[mM]==2 &&
  b_sup[mM]==110 (two type-7s collapse to one
  R2: per-channel single-application).
- K-MCH-MULTI: abM2 n3==1 &&
  b_sup[mM]==90 && b_conf[mM]==0 &&
  b_disc[mM]==1.
- K-MCH-BLIND: b_sup[mS]==b_sup[mM] &&
  b_conf[mS]==b_conf[mM] &&
  b_disc[mS]==b_disc[mM] (90/0/1 both:
  same-fact and multi-fact delivery net
  identically).

CY12 bars:
- K-CY12-WEAK: b_sup[z6]==40.
- K-CY12-1HOP: b_sup[z5]==40 &&
  b_sup[z4]==100 && b_sup[z11]==100.
- K-CY12-FULL: all 12 b_sup==40 after the
  backward sweep.
- K-CY12-FIX: all 12 b_sup==40 after
  re-application.
- K-CY12-RAISE: after 2x R2(z6,1):
  b_sup[z6]==80; R6(z5): b_sup[z5]==80 &&
  b_sup[z4]==40.
- K-CY12-RAISEFULL: all 12 b_sup==80 after
  the backward sweep.

HET bars:
- K-HET-WEAK: b_sup[v4]==40.
- K-HET-BLOCK: R6(v3) ret==255 &&
  b_sup[v3]==100 && b_sup[v4]==40 (type-1
  blocks the 1-hop).
- K-HET-ERASE: R6(v4) ret==100 &&
  b_sup[v4]==100 (isolated weakening
  reabsorbed).
- K-HET-FULL: all 6 b_sup==100 after the
  full sweep.
- K-HET-FIX: all 6 b_sup==100 after
  re-application.
- K-HET-T3: w6pre==40 && R6(v5) ret==255 &&
  b_sup[v5]==100 && b_sup[v6]==100 (type-3
  carries nothing; weakening behind it
  reabsorbed).

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output
  (SHA-256).
- K-HYG: pure Zag under safebin (`which
  python3` / `which python` empty at build and
  run); zero em/en dash bytes in lane files and
  run outputs; 0 new edge types (1/3/7/14
  frozen-and-pre-existing; 7 is block-written
  evidence; the type-1 and type-3 edges in the
  HET ring reuse pre-existing kinds); 0 new
  node types (tags 1/3/20 pre-existing); 0
  modes, 0 bridges, 0 handlers; xf_block.zag
  SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build;
  bp8_learner.zag byte-identical to
  bp7_learner.zag (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e);
  opaque identifiers.

Bar count: 3 PCs + 18 K bars + K-DET + K-HYG = 23.

## 5b. Amendment (2026-10-03, after the first
implementation run; transparent re-freeze)

The first run went 20/21, exposing one prereg error.
No frozen rule was changed to chase the bar; the
correction below re-derives the prediction from the
frozen rules. The implementation was then re-run
from scratch.

- A1 (K-CY12-RAISE composition slip): the prereg
  predicted b_sup[z4]==100 at the raise 1-hop
  ("z4 stays 100"). Wrong: the FULL sweep set every
  node to 40 (K-CY12-FULL, K-CY12-FIX both passed),
  and nothing touches z4 between the sweep and the
  raise 1-hop, so z4 is 40, not 100, when R6(z5)
  is applied. The implementation was faithful to
  the frozen rules (CY12-RAISED emitted z6=80;
  R6(z5) set z5=80); the hand composition forgot
  the sweep's effect on z4. Corrected bar:
  b_sup[z6]==80 && b_sup[z5]==80 &&
  b_sup[z4]==40. The discriminating content is
  preserved: the raise reaches exactly one hop
  (z5 takes 80, z4 unchanged); a transitive
  one-application propagation would have set
  z4=80.

## 6. Falsifiers (what kills the claim)

- MCH: absorb applies R2/R3 per new edge
  instead of per channel (SAT fails: conf
  would be 3); the block drops match-then-
  contradict on one fact (SAME fails);
  contradict-then-match writes a type-7 on the
  original fact (ORD fails: n7 would be 1);
  same-fact and multi-fact nets differ (BLIND
  fails).
- CY12: any node != hand-derived after the
  sweep (non-convergence or oscillation);
  fixpoint re-application moves a value;
  the raise stops early or overshoots.
- HET: any R6 propagation across the type-1
  or type-3 edge (BLOCK/ERASE/FULL/T3 fail);
  R6 following non-14 edges; v5 moving under
  any R6.

## 7. Verdict rule

BP-8-PASS iff every PC bar and every K bar
passes on the frozen implementation, 3/3
byte-identical. A single failed K bar fails its
arm. This lane does not re-open the 7 sealed
predictions, does not change R6/R7/absorb or
the bar rule, and adds no learner machinery.
bp8_absorb and bp8_allsup are test-harness
code only.

## 8. Out of scope (not claimed)

Whether absorption SHOULD be per-channel or
per-edge (the frozen convention is measured,
not endorsed); whether R6 should follow
non-14 edges (measured as type-restricted);
recovery paths for reabsorbed weakenings;
eviction-sync design (still needs the parent
ruling); per-belief bar adoption; d_self
recovery.
