# PREREG_AMENDMENT1: plan linkage, program record, ablation snapshot point

Status: AMENDMENT-FROZEN. No implementation exists at this commit.
Amends `PREREG.md` (commit 5293381da). All changes are
pre-implementation clarifications; no bar is weakened, no threshold
moved.

## A1. Plan linkage (Section 3, K4, K8)

PREREG said: `root.child = core, core.next = tail` (sibling chain
via next). PROBLEM: the reuse arm shares plan1's core node inside
plan2. If plan2 reuses the core node verbatim, the core's `next`
field still points at plan1's tail, so executing plan2 would drag
plan1's tail along; repointing it would mutate the shared node and
corrupt plan1. Verbatim reuse requires the shared node to be
untouched.

AMENDED: `root.child = core, root.next = tail`. SEQ execution is:
execute the child subtree, then execute the next subtree. NEST and
PAIR ignore `next`. The core node is then shared by plan2 without
any mutation: plan2 = new root SEQ with child = plan1 core id,
next = plan2 tail id.

K4 amended expectations: post-T1, node count == 5; root SEQ
child == core id, next == tail id; NEST nodes depthlv 1,2 with
child threading inward and next == 255; PAIR nodes count 1;
all tokL == 40, tokR == 41, live == 1.

K8 unchanged: plan2 root.child == plan1 core node id (exact id
equality) still holds, now with zero mutation of the shared node.

## A2. Program record layout (Section 3)

PREREG said: `[plen,targetP,targetD,epoch,acc,measD,measP,pad,
ops x24 @+8]`. AMENDED:
`[plen,tP,tD,epoch,acc,measD,measP,L,R,pad,pad,pad, ops x20 @+12]`.
Rationale: each program binds its own L/R token bytes (copied
from the plan nodes at assembly under the build epoch), so the
program is self-describing and the revision arm can show
epoch-1 vs epoch-2 bindings. 20 op slots suffice (max program
here is 12 ops).

## A3. State byte 7 (Section 3)

Byte 7 is NPROV (provenance log count), not pad.

## A4. ARM-ABLATE snapshot point (Section 5, K5)

PREREG said: snapshot PLAN_OPS after plan_build. AMENDED: the arm
runs the FULL plan-driven construction first (plan_build +
assemble + execute), then snapshots PLAN_OPS, then wipes the plan
region, then runs direct_try(4,3,20000). Rationale: the honest
comparison is full construction-with-intermediate vs
construction-without-it, not plan-creation alone vs search.
Expected PLAN_OPS snapshot ~31 (5 node allocs + 8 assemble ops +
2 NEST level checks + 8 execute ops + 8 w_check scan); K5 bar
(DIRECT_OPS / snapshot >= 10) unchanged.

No other text of PREREG.md changes. All kill bars K1..K13 stand as
amended above.
