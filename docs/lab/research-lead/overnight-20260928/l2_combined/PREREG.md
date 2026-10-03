# PREREG: L2-COMBINED (multi-adaptation composition in one pipeline)

Frozen before any implementation. Commit contains only this file and
NAMECHECK.md (Step 0 guard). All commits local on tnn-native-lab;
never pushed.

## 1. Hypothesis

Every individual L2 adaptive-reuse operator is demonstrated (ledger
C302). The open question is whether they COMPOSE: can one learner
fire MULTIPLE different adaptation operators in a single solution,
with the later adaptation operating on the earlier one's output?
Claim: YES for SUBSTITUTE followed by iterative EXTEND. A chain MAP
that is BOTH stale in the middle AND too short for the query span is
repaired by substitute-then-extend in one query pipeline, with full
provenance, and the composite is reused as one unit.

## 2. World (driver scaffold, not learner cognition)

Facts taught in order (ev_teach; node ids hand-derived: tnn2_init
marks 0,1 live so user nodes start at 2; each ev_teach allocates one
node):

- f0 (101,1,102) -> node 2
- f1 (102,1,103) -> node 3   [killed after teaching]
- f2 (103,1,104) -> node 4
- f3 (102,1,112) -> node 5
- f4 (112,1,103) -> node 6
- f5 (104,1,105) -> node 7
- f6 (105,1,106) -> node 8
- f7 (106,1,107) -> node 9
- f8 (102,1,110) -> node 10  [distractor fact, live]

Native MAPs taught (prior knowledge, independently learned):

- m: relseq [1,1,1] from 101 via t2_lu_first walk
  (101->2->102, 102->3->103 while f1 live, 103->4->104).
  Graph cells 12 nodes (11..22), MAP node 23. term=104.
- d (distractor piece): explicit facts [10], vals [102,110].
  4 cells (24..27), MAP node 28. term=110.
- n (replacement piece): explicit facts [5,6], vals [102,112,103].
  8 cells (29..36), MAP node 37. term=103.

World change: kill f1 -> ns(W,3,36,0). m is now stale at hop 1
(fact 3 dead) but too short anyway (term 104 < goal 107).

No paired training example of any chain longer than 3 links exists.
The 7-link solution chain is never taught.

## 3. Learner pipeline (l2c_query; new patch, no new machinery)

Query (s=101, r=70, goal=107), flags sub_on/ext_on are DRIVER-SET
causal controls only (l2_substitute SUB_ON/ET_ON precedent), never
written by the learner. In the treatment both are 1 and every firing
is learner-triggered:

1. SELECT: longest live MAP with start==s; exact terminal==goal wins
   immediately (learner-owned; no MAP id named).
2. STALE-CHECK: first hop whose licensing fact (type-1 edge) is dead.
   - stale and sub_on: SUBSTITUTE fires (trigger = dead fact).
   - stale and not sub_on: MAP unusable; ext_on still attempts
     extend (to show the refusal), else trial fallback.
3. SUBSTITUTE (proven C298 semantics): split at dead hop; prefix
   101->102, dead hop 102->103, suffix 103->104; node-id order
   search for first live piece with endpoints 102->103 and all
   facts live (d examined and rejected on endpoints, n matches);
   assemble facts [2,5,6,4] vals [101,102,112,103,104]; verify by
   real execution to m's stored terminal 104; promote m2 with
   type-16 to m and to n.
4. SPAN-CHECK: term != goal and ext_on: EXTEND-ITER fires (trigger =
   span shortfall), operating on m2 (the substitute's output).
   Reuses extn_step verbatim (C301 semantics): frontier licensing by
   real facts, TERM/NOFRONTIER/EXECFAIL/BUDGET stops, type-16 per
   step. Precondition: start MAP fully satisfiable; a stale MAP is
   REFUSED (EXTN-REFUSE-STALE), which is the wrong-order failure.
5. VERIFY full chain live; on episode success write provenance:
   LINK14 from final MAP to {m, n, m2}; type-15 co-use for each
   consecutive delivery pair. Answer through the final MAP.

Order is learner-discovered: staleness is checked before span
because span reasoning on a stale MAP is untrustworthy. The trace
shows SUB-* lines before EXTN-* lines (white-box).

## 4. Hand-derived treatment trace (FULL arm, query 1)

Node ids: m=23, d=28, n=37.
Substitute: 16 cells (38..53), exec frame 54, m2=55.
Ext1: 20 cells (56..75), frame 76, id=77.
Ext2: 24 cells (78..101), frame 102, id=103.
Ext3: 28 cells (104..131), frame 132, id=133 (final).

Arithmetic:
- m2: facts [2,5,6,4] = prefix [2] + piece [5,6] + suffix [4];
  vals [101,102,112,103,104]; 4 links; exec verifies to 104.
- ext1: frontier 104, lic fact 7 (104,1,105); plen 5; term 105.
- ext2: frontier 105, lic fact 8 (105,1,106); plen 6; term 106.
- ext3: frontier 106, lic fact 9 (106,1,107); plen 7; term 107.
- type-16 hops 133->103->77->55->23 = 4; ultimate ancestor 23.
  (55 has a second type-16 to 37, the piece.)

Frozen trace lines (K3), verbatim and in order:

```
L2C-QUERY s=101 goal=107
L2C-SEL m=23 plen=3 term=104
SUB-STALE m=23 hop=1 fact=3
SUB-CAND id=23 skip=self
SUB-CAND id=28 s=102 e=110 skip=ep
SUB-CAND id=37 s=102 e=103 flive=2 MATCH
SUB-BUILD rels=1,1,1,1 facts=2,5,6,4
SUB-VERIFY term=104
SUB-PROMOTE m2=55
L2C-SPAN term=104 goal=107 EXTEND
EXTN-STEP n=1 parent=55 id=77 plen=5 lic=104,1,105 term=105
EXTN-STEP n=2 parent=77 id=103 plen=6 lic=105,1,106 term=106
EXTN-STEP n=3 parent=103 id=133 plen=7 lic=106,1,107 term=107
EXTN-STOP reason=0 ext=3 ans=107 final=133
L2C-VERIFY term=107 OK
L2C-ANS via=133 val=107
```

## 5. Arms (each on a fresh workspace)

- FULL: setup + kill; l2c_query(101,70,107,sub=1,ext=1).
  Derived: ans=107, sub=1, ext=3, stop=0 TERM, final=133.
- REUSE: setup + kill; query1 (as FULL, light asserts); then
  query2 = same (101,70,107).
  Derived: ans2=107 via m=133 (exact-terminal select), sub=0,
  ext=0, no new MAPs/edges (t16 stays 5, t14 stays 3, t15 stays 5,
  mapcount stays 7). Trace q2:
  L2C-QUERY / L2C-SEL m=133 plen=7 term=107 /
  L2C-SPAN term=107 goal=107 OK / L2C-VERIFY term=107 OK /
  L2C-ANS via=133 val=107 (zero SUB-/EXTN- lines).
- EXT-ONLY: sub=0, ext=1.
  Derived: SUB-STALE fires; extend attempted on stale m and
  REFUSED by the operator precondition (EXTN-REFUSE-STALE m=23);
  generic trial cannot bridge 7 links (caps at 4); ans=-2;
  t16=t14=t15=0. Proves extend-alone cannot do the task and that
  substitute must fire first (wrong order fails).
- SUB-ONLY: sub=1, ext=0.
  Derived: substitute fires, m2=55 promoted (t16=2: 55->23,
  55->37); term 104 != 107, no extend; ans=-3 (L2C-SPAN SHORTFALL);
  t14=t15=0. Proves substitute-alone cannot do the task.
- EXACT: sub=0, ext=0.
  Derived: SUB-STALE fires, MAP unusable, trial fails; ans=-2;
  t16=t14=t15=0. Proves exact reuse fails.
- FRESH: facts only (+kill), no MAPs; sub=1, ext=1.
  Derived: L2C-NOSEL; trial fails (no 7-link path within 4-link
  cap; count/sum/1-link candidates reject 107); ans=-2; t16=0.
  Proves the learned structure was load-bearing.

## 6. Frozen kill bars

- K1 (FULL exact): ans=107, sub_fired=1, ext=3, stop=0, final=133;
  relseq(133)=[1,1,1,1,1,1,1]; type-16 hops(133)=4;
  ult_native(133)=23.
- K2 (provenance exact): t16 count=5 with pairs
  {(55,23),(55,37),(77,55),(103,77),(133,103)};
  t14 count=3, all from 133, dsts {23,37,55};
  t15 count=5 with pairs
  {(23,37),(37,55),(55,77),(77,103),(103,133)};
  no other 14/15/16 edges.
- K3 (white-box trace): all 17 frozen lines of section 4 present
  verbatim in order in run1.txt; SUB-* lines precede EXTN-* lines
  (learner-discovered order); each firing names op, trigger, ids.
- K4 (EXT-ONLY ablation): ans=-2; t16=t14=t15=0; trace contains
  SUB-STALE m=23 hop=1 fact=3 and EXTN-REFUSE-STALE m=23.
  Extend-alone fails; wrong order (extend without substitute)
  fails at the operator precondition.
- K5 (SUB-ONLY ablation): ans=-3; t16=2 with pairs {(55,23),
  (55,37)}; t14=t15=0; ng(55,28)=104; trace contains
  L2C-SPAN term=104 goal=107 SHORTFALL. Substitute-alone fails.
- K6 (EXACT control): ans=-2; t16=t14=t15=0. Exact reuse fails.
- K7 (FRESH control): ans=-2; t16=0. Fresh learner fails.
- K8 (REUSE): ans1=ans2=107; q2 sub=0 ext=0 final=133;
  after q2: t16=5, t14=3, t15=5, mapcount=7 (unchanged);
  q2 trace has zero SUB-/EXTN- lines. The multi-adapted
  composite persists as one unit.
- K9 (determinism): 3/3 runs byte-identical (sha256 equal,
  pairwise cmp clean), binary exit 0 on all runs.
- K10 (0 new machinery): frozen copies cc_base.zag, un_patch.zag,
  adapt_patch.zag, extn_patch.zag sha256-identical to origins;
  origins unmodified (git diff empty on source dirs). New code
  (l2c_patch.zag + l2c_driver.zag) issues link_edge only with
  types 14/15/16; 0 new edge types, 0 new opcodes, 0 modes,
  0 bridges, 0 handlers, 0 new semantic cases, 0 new node tags;
  no relation/value literals in the learner patch (world values
  live in the driver only). Grep audit recorded.
- K11 (commit order): prereg commit contains only PREREG.md and
  NAMECHECK.md; verified by git show --stat before implementation.
- K12 (no dashes): check_no_dash.sh clean on all deliverables.

Falsifiers (any one voids the claim): a frozen trace line absent
or out of order; any control arm passing (ans=107); t16/t14/t15
counts differing; a second adaptation firing in REUSE q2; any new
edge type/opcode/mode in new code; non-deterministic runs.

## 7. What is NOT claimed

- One world family (chain routing, stale middle + short span).
  No generality claim beyond the six arms.
- The kill is builder-designed, not adversary-designed.
- This is L2 composition evidence, not L3 invention.
- SUB_ON/EXT_ON are driver-set causal-control flags for the
  ablation arms only (composition_l2 adapt_on precedent); the
  treatment arm's firings are fully learner-triggered.

## 8. Build plan

cat cc_base.zag un_patch.zag adapt_patch.zag extn_patch.zag
l2c_patch.zag l2c_driver.zag > l2c_full.zag; compile with pinned
znc src/tools/toolchain/znc_linux_x86_64_abed8aa1; run 3x;
sha256 all artifacts.
