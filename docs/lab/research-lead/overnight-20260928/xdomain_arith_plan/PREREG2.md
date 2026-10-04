# PREREG2: xdomain_arith_plan -- H1/H2/H3 Verbatim Ports on Sum-then-Plan, XIO Control

Frozen 2026-10-02, before implementation. This file is committed ALONE
before any driver, assembly, binary, or run output for THIS prereg
exists. It SUPERSEDES PREREG.md (commit aa708f552), which is left
untouched. Reason for supersession, stated transparently: PREREG.md
registered a different experiment than the assigned task. It tested
novel typed-contract / value-composition mechanisms expecting success.
The assigned task requires verbatim ports of the existing H1
(whole-MAP chaining / mutation), H2 (fragment recombination), H3
(constraint DFS) invention mechanisms plus the XIO-general core as a
control, on the arithmetic to planning pair, expecting the chain-bound
negative per C215/C231. This prereg registers that experiment. The
prior worker's draft source ap.zag (committed under PREREG.md) is
renamed to ap_superseded_draft.zag and is NOT executed.

## Background

C215 (composition_xdomain): mechanisms A, B, C all FAIL cross-domain;
composition is navigation concatenation. C231 / xdomain_harder: H1, H2,
H3 all FAIL on transform-then-navigate; invention is novel-chain
construction. Shared diagnosis: cross-domain needs typed function
composition with a computed-value handoff, which no chain-bound
mechanism performs. Question: does the negative generalize to a new
pair, arithmetic to planning?

## The pair: sum-then-plan (arithmetic to planning)

X = SUM (arithmetic, node to number). Facts r=71: (basket,71,value).
Learned by the base sum trial template as pure unrolled INC chains
(t2_asm_sum; NO guard/set cells at all). Output is a computed number.

Y = PLAN (goal-directed action sequences, number to node). Facts r=82:
(param,82,step) action chains from a numeric plan parameter to a goal
literal. Learned by the base chain trial template as guard/set chains.
In the base the plan templates were removed (K-T2-2, K-T2-3), so plans
are learned as chain graphs; the planning-ness is in the world
semantics (parameterized action sequences to goals). Output is a goal
node.

Z = plan(sum(s)): compute the arithmetic result, feed it as the plan
parameter. Query (103,93) -> 203. Requires sum(103)=15 then
plan(15)=203.

Structural difference vs the harder pair (count-then-navigate), all
preregistered:

1. X is value-weighted arithmetic (sum over fact OBJECT values via
   t2_gather_sum), not link counting. Sum graphs are pure INC chains
   with zero guard/set cells, so sum MAPs are invisible to chain
   perception for a stronger reason than count MAPs (no chain cells
   whatsoever, not even broken guard/set alternation).
2. Y is goal-directed planning (action steps to a goal literal),
   indexed by computed numeric parameters.
3. The handoff direction matches the harder pair (number to node),
   but the number-typed domain is a different arithmetic (sum, not
   count). This discriminates mechanisms that are count-specific.

## World specification (exact)

X domain (SUM). Relation 71 facts, query relation 91.
- X1: ev_teach (101,71,5),(101,71,3),(101,71,7).
  Query (101,91) expected 15. (trial: sum graph, 3 values)
- X2: ev_teach (102,71,4),(102,71,6).
  Query (102,91) expected 10. (trial: sum graph, 2 values)

Y domain (PLAN). Relation 82 facts, query relation 92.
- Y1: ev_teach (15,82,201),(201,82,202),(202,82,203).
  Query (15,92) expected 203. (trial: chain MAP [82,82,82])
- Y2: ev_teach (10,82,211),(211,82,212),(212,82,213).
  Query (10,92) expected 213. (rebind of Y1 MAP; LINK14)

Interference gap: 30 facts (5000+i, 60+(i%10), 6000+i) for i in 0..29,
taught between training and Z in TREAT.

Z facts (taught after the gap in TREAT):
- (103,71,6),(103,71,9). sum(103) = 15.
- Plan from 15 already taught in Y1: 15->201->202->203.

Z query: (103,93) expected 203. Fresh subject 103 throughout; query
relation 93 is new. No X/Y pairing taught.

Trial-alone cannot solve Z in FRESH (103's 71-facts reach only 6 and 9,
both leaves; sum(103)=15 != 203; count(103)=2 != 203), so any Z failure
is mechanism-specific, not a broken world.

## Mechanisms (verbatim ports, zero edits to mechanism source)

- H1: cat ../invention_mutation/mu_core.zag
  ../invention_mutation/mu_patch.zag ap_driver.zag > ap_full_h1.zag
- H2: cat ../invention_recombine/ir_base.zag
  ../invention_recombine/ir_patch.zag ap_driver.zag > ap_full_h2.zag
- H3: cat ../invention_constraint/invent_base.zag
  ../invention_constraint/invent_patch.zag ap_driver_h3.zag
  > ap_full_h3.zag
- XIO (control): cat ../composition_A/cx_core.zag
  ../xio_adapters/xio_core.zag ap_driver_xio.zag > ap_full_xio.zag

Patches and cores are concatenated verbatim (byte-compared with cmp at
build time). Drivers are new (this worker). Pinned compiler:
src/tools/toolchain/znc_linux_x86_64_abed8aa1.

H3 fairness protocol (same as xdomain_harder): Z query via ev_query_c
with C = [plen,-1,-1,-1,-1,103] for plen = 1,2,3,4 (all-don't-care
except plen and first_lit). X/Y training queries use plain ev_query.

## Arms (per mechanism)

- TREAT: train X, train Y, gap, census, Z facts, Z query.
- ABL-X: train X, train Y, delete all MAPs with r=91, gap, Z facts,
  Z query.
- ABL-Y: train X, train Y, delete all MAPs with r=92, gap, Z facts,
  Z query.
- FRESH: gap only, Z facts, Z query.
- XIO adds ABL-XIO: full training, adapters disabled (xio_on=0).
  Expect the C215-style negative reproduced.

Each arm runs in a fresh workspace (z_alloc + tnn2_init), one binary
per mechanism.

## Hypotheses and kill bars

Capability hypotheses (one per mechanism). A "working Z" means BOTH:
Z ans == 203 AND a MAP with (s=103, r=93) promoted (ZMAP id != -1).

- AP-H1: H1 (mutation) constructs a working Z on TREAT.
  PREDICTED KILLED: mu_best_plen sees only Y plan MAPs (sum MAPs have
  plen -1, pure INC chains); mu_extend_one stages them on 103, walks
  103's 71-facts to 6/9, extends a longer 71-chain verified against
  203: fail. KILLED if TREAT Z ans != 203 or ZMAP id == -1.
- AP-H2: H2 (fragment recombination) constructs a working Z on TREAT.
  PREDICTED KILLED: ir_relseq is -1 for sum MAPs (no guard/set);
  Y plan fragments ([82,82,82]) exist but ir_frag_candidates from
  s=103 needs an 82-fact with subject 103: t2_lu_first(103,82) = -1,
  so DFS never starts: RECOMB-FAIL. KILLED if TREAT Z ans != 203 or
  ZMAP id == -1.
- AP-H3: H3 (constraint-driven invention) constructs a working Z on
  TREAT. PREDICTED KILLED at every plen 1..4: invent_dfs builds fact
  chains from 103 (103->6, 103->9, then dead ends); every endpoint
  fails verification against 203. KILLED if no plen yields Z ans ==
  203 with ZMAP id != -1.
- AP-XIO (control, informative): XIO adapter constructs a working Z
  on TREAT. PREDICTED FAIL, with a NEW diagnosis if confirmed:
  xio_stage_exec for oty-1 MAPs re-derives a COUNT graph
  (t2_chain + t2_asm_count) from the MAP's DEP relation. For a SUM
  MAP this computes count(103)=2, not sum(103)=15; the plan stage
  from 2 then finds no 82-facts. So XIO's typed composition is
  count-specific, not arithmetic-general: it crosses chain/count and
  count/chain (C229, xio_harder) but NOT sum/plan. If XIO instead
  PASSES, that falsifies this diagnosis and is reported as a
  surprise positive.

Competence hypothesis (must hold for any negative to be clean):

- AP-COMP: in TREAT, X1==15, X2==10, Y1==203, Y2==213 for EACH of the
  four binaries. If any competence query fails for a mechanism, that
  mechanism's result is VOID (broken world/port), not a clean
  negative.

Determinism bar:

- AP-DET: 3/3 byte-identical runs per binary (SHA-256 recorded). Any
  divergence VOIDs that mechanism's result.

Causal bars (only evaluated if a capability hypothesis PASSES):

- AP-CAUSAL: if TREAT Z==203 with ZMAP, then ABL-X Z must != 203 and
  ABL-Y Z must != 203. FRESH Z != 203 must also hold.

## Verdict rule

XDOMAIN-ARITH-PLAN-COMPLETE iff: AP-COMP holds for all four binaries,
AP-DET holds for all four binaries, and each of AP-H1/AP-H2/AP-H3 is
adjudicated (KILLED with white-box diagnosis, or PASSED with
AP-CAUSAL satisfied) and AP-XIO is adjudicated with its diagnosis.
Per-mechanism outcomes and the shared-vs-new diagnosis are reported
in REPORT.md.

## Constraints honored

Unfrozen only (xdomain_arith_plan/). Frozen source read-only. Pure Zag
(safebin, Step 0 in NAMECHECK.md). Zero em/en dashes (byte-verified
before commit). Paper untouched. Nothing pushed. 0 modes, 0 bridges,
0 handlers, 0 new semantic cases, 0 domain-pair templates. No
ARITH_TO_PLAN template. No hardcoded (sum,plan) pair selection. The
world facts above are the experiment, not a solver.
