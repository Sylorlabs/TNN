# PREREG.md -- X-Domain Harder Pair: Invention Mechanisms on Transform-then-Navigate

## Worker and date

X-Domain Harder-Pair Worker. 2026-10-02. Unfrozen variant. Pure Zag.
Faxed to the ledger before any implementation. This file is committed
ALONE before any driver, binary, or run output exists.

## Background

Composition cross-domain (chain+count, commit 0c91d9b3f, ledger C215)
was a CLEAN NEGATIVE: mechanisms A, B, C all implement composition as
navigation concatenation (chain-structured admission filters,
t2_asm_chain assembly everywhere) and cannot do value-level handoff
between typed computations.

Invention H1 (mutate failing structure), H2 (recombine sub-MAP
fragments), H3 (constraint-driven construction from facts) all PASS at
L2 with different principles. But all three are CHAIN-construction
mechanisms:

- H1: extends a failing CHAIN MAP by one cell on the "too short" signal
  (rb_chain_plen, t2_asm_chain).
- H2: recombines contiguous sub-CHAIN fragments of MAP relation
  sequences (ir_relseq demands guard/set alternation; assembly is
  t2_asm_chain + SEQ links).
- H3: backtracking DFS building CHAINS cell by cell from facts
  (invent_relseq demands guard/set; invent_dfs walks fact sequences).

Question: does ANY invention mechanism cross the domain gap that
composition could not?

## The harder pair: transform-then-navigate

X = COUNT (transform, node -> number). Facts are chains; the query asks
for the link count. Learned as count graphs: guard(102)/set(101) links
each with an INC(103) cell, plus a MOV epilogue. Output is computed
arithmetically, not retrieved.

Y = CHAIN on numeric subjects (navigate, number -> node). Facts are
chains whose SUBJECTS are small numbers (the kind of values X outputs).
Learned as guard/set chain MAPs. Output is a walked node.

Z = Y(X(s)): count s's links to get k (a computed number), then walk
the Y chain starting FROM k. Query (21,93) -> 52.

Why this is HARDER than chain+count:

1. The FIRST domain (X=count) is non-navigational and invisible to
   every chain-based perception operator. In chain+count, X=navigate
   was visible to all admission filters; only Y was invisible. Here the
   mechanisms fail at perceiving X itself, not just at composing X+Y.
   (rb_chain_plen, ir_relseq, invent_relseq all return -1 on count
   graphs because the INC cell breaks guard/set alternation.)

2. The intermediate k is a COMPUTED NUMBER, not a fact-store node.
   chain+count handed off a node (34) that Y-facts were taught on.
   Here k=4 is produced by arithmetic; there is no "there" to walk to.
   Feeding a computed value as a navigation subject is a type
   transition (value -> subject) that no chain machinery performs:
   rebind stages MAPs on query subjects, trial gathers from query
   subjects, H1 extends from staged endpoints, H2 chains fragments from
   the query subject, H3 walks facts from the query subject. None of
   them computes k=4 and then re-subjects.

3. Y's chain MAPs are learned on NUMERIC subjects (3, 2). Y's knowledge
   is indexed by computed values. Even Y's visible chain MAPs cannot
   stage on s=21 (21 has no 82-facts), so visibility does not help.

Structural difference (both required properties hold):

- Different cell types: X count graphs use guard(102)/set(101) +
  INC(103) + MOV epilogue; Y chain graphs use guard/set only.
- Different output kinds: X outputs a NUMBER (computed); Y outputs a
  NODE (walked literal).

## World specification (exact)

X domain (count). Relation 81 facts, query relation 91.

- X1: ev_teach (11,81,12), (12,81,13), (13,81,14).
  Query (11,91) expected 3. (trial: count graph, 3 links)
- X2: ev_teach (15,81,16), (16,81,17).
  Query (15,91) expected 2. (trial: count graph; rebind cannot
  handle count graphs because rb_chain_plen = -1)

Y domain (chain on numeric subjects). Relation 82 facts, query
relation 92.

- Y1: ev_teach (3,82,30), (30,82,31), (31,82,32).
  Query (3,92) expected 32. (trial: chain MAP [82,82,82])
- Y2: ev_teach (2,82,40), (40,82,41), (41,82,42).
  Query (2,92) expected 42. (rebind of Y1's MAP; LINK14)

Interference gap: 30 facts (5000+i, 60+(i%10), 6000+i) for i in 0..29,
taught between training and Z in TREAT (mirrors the xdomain worker).

Z facts (taught after the gap in TREAT):

- (21,81,22), (22,81,23), (23,81,24), (24,81,25). count(21) = 4.
- (4,82,50), (50,82,51), (51,82,52). walk(4) = 52.

Z query: (21,93) expected 52. Fresh literals throughout; query
relation 93 is new. No X/Y pairing taught; Y's subjects (3,2) are the
VALUE KIND that X outputs, but no fact links X's training to Y's.

## Arms (per mechanism)

- TREAT: train X, train Y, gap, census, Z facts, Z query.
- ABL-X: train X, train Y, delete all MAPs with r=91, gap, Z facts,
  Z query.
- ABL-Y: train X, train Y, delete all MAPs with r=92, gap, Z facts,
  Z query.
- FRESH: gap only, Z facts, Z query.

Each arm runs in a fresh workspace (z_alloc + tnn2_init), same binary.

## Hypotheses and kill bars

Capability hypotheses (one per mechanism). A "working Z" means BOTH:
Z ans == 52 AND a MAP with (s=21, r=93) is promoted (ZMAP id != -1).

- XH-H1: H1 (mutation) constructs a working Z on TREAT.
  KILLED if TREAT Z ans != 52 or ZMAP id == -1.
- XH-H2: H2 (fragment recombination) constructs a working Z on TREAT.
  KILLED if TREAT Z ans != 52 or ZMAP id == -1.
- XH-H3: H3 (constraint-driven invention) constructs a working Z on
  TREAT.
  KILLED if TREAT Z ans != 52 or ZMAP id == -1.

Architectural prediction (recorded before running, does not move the
bars): all three XH-H* are expected to be KILLED. H1's mutate_try
extends 81-chains and verifies against 52 (fail); H2's recombine_try
finds no 82-fragment satisfiable from 21 (RECOMB-FAIL); H3's invent_dfs
finds no fact chain from 21 reaching 52 (INVENT-FAIL). The shared
reason, if confirmed: every invention mechanism is a novel-CHAIN
constructor; cross-domain needs typed function composition with a
computed-value handoff, which none of them implements.

Competence hypothesis (must hold for a negative to be clean):

- XH-COMP: in TREAT, X1==3, X2==2, Y1==32, Y2==42 for EACH mechanism.
  If any competence query fails for a mechanism, that mechanism's
  result is VOID (broken world/port), not a clean negative.

Determinism bar:

- XH-DET: 3/3 byte-identical runs per binary (SHA-256 recorded). Any
  divergence VOIDs that mechanism's result.

Causal-reuse bars (only evaluated if a capability hypothesis PASSES):

- XH-CAUSAL: if TREAT Z==52 with ZMAP, then ABL-X Z must != 52 and
  ABL-Y Z must != 52, proving both domains causal. FRESH Z != 52 must
  also hold (no trial-only solution).

## H3 constraint protocol (fairness)

H3's invent_try runs only via ev_query_c with a constraint struct. To
give H3 its best chance, the Z query is issued via ev_query_c four
times with C = [plen, -1, -1, -1, -1, 21] for plen = 1, 2, 3, 4
(all-don't-care except plen and first_lit). This searches the entire
chain space from 21 up to length 4. X/Y training queries use plain
ev_query (C plen = -1, falls through to standard). If any plen yields
ans == 52, XH-H3 PASSES. Predicted: all four INVENT-FAIL, because no
fact chain from 21 reaches 52 at any length (21's reachable set via
any relation is {22,23,24,25}, all leaves).

## Assemblies (patches verbatim from prior workers)

- H1: cat ../invention_mutation/mu_core.zag
  ../invention_mutation/mu_patch.zag xh_driver.zag > xh_full_h1.zag
  (mu_patch verbatim; mu_shared.zag NOT included, driver carries its
  own helpers; mu_core defines no main)
- H2: cat ../invention_recombine/ir_base.zag
  ../invention_recombine/ir_patch.zag xh_driver.zag > xh_full_h2.zag
  (ir_patch verbatim)
- H3: cat ../invention_constraint/invent_base.zag
  ../invention_constraint/invent_patch.zag xh_driver_h3.zag
  > xh_full_h3.zag (invent_patch verbatim)

Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1.
Binaries: xh_bin_h1, xh_bin_h2, xh_bin_h3.
Runs: xh_run_h1_{1,2,3}.txt, xh_run_h2_{1,2,3}.txt,
xh_run_h3_{1,2,3}.txt.

## Constraints honored

Unfrozen only (new dir xdomain_harder/). Frozen source read-only.
Pure Zag (safebin, Step 0 in NAMECHECK.md). Zero em/en dashes
(byte-verified). Paper untouched. Nothing pushed. 0 modes, 0 bridges,
0 handlers, 0 new semantic cases, 0 domain-pair templates. The world
facts above are the experiment, not a solver: no fact sequence from
21 reaches 52, no template for count-then-navigate exists in any
patch, and the drivers never name fragment triples, parents, or
constraints beyond the H3 plen sweep.

## Verdict rule

XDOMAIN-HARDER-COMPLETE iff: XH-COMP holds for all three mechanisms,
XH-DET holds for all three binaries, and each XH-H* is adjudicated
(KILLED with white-box diagnosis, or PASSED with XH-CAUSAL satisfied).
Per-mechanism pass/fail and the shared architectural diagnosis are
reported in REPORT.md.
