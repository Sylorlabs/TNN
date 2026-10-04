# REPORT.md -- X-Domain Arithmetic to Planning: H1/H2/H3 Verbatim Ports + XIO Control

## Verdict: XDOMAIN-ARITH-PLAN-COMPLETE (clean negative, one new boundary)

**No invention mechanism (H1, H2, H3) crosses the arithmetic to planning
gap. All three fail on sum-then-plan for the same shared architectural
reason as C215/C231: every invention mechanism is a novel-CHAIN
constructor, and cross-domain composition needs typed function
composition with a computed-value handoff. The failure is clean,
deterministic (3/3 byte-identical per mechanism), and diagnosed to the
exact line where each mechanism's chain assumption breaks. The
XIO-general control ALSO fails here, revealing a new boundary: XIO's
typed composition is count-specific, not arithmetic-general.**

## The pair: sum-then-plan

X = SUM (arithmetic, node -> number). Facts r=71: (basket,71,value).
Learned by the base sum trial template as pure unrolled INC chains
(t2_asm_sum): NO guard/set cells at all. Output is a computed number.

Y = PLAN (goal-directed action sequences, number -> node). Facts r=82:
(param,82,step) chains from a numeric plan parameter to a goal
literal. Learned as guard/set chain MAPs. (The base's plan templates
were removed under K-T2-2/K-T2-3, so plans are learned as chain graphs;
the planning-ness is in the world semantics: parameterized action
sequences to goals.)

Z = plan(sum(s)): query (103,93) -> 203. Requires sum(103)=15, then the
plan 15->201->202->203 taught in Y1. Fresh subject 103; query relation
93 is new; no X/Y pairing taught.

Structural difference vs the harder pair (count-then-navigate):

1. X is value-weighted arithmetic (sum over fact OBJECT values via
   t2_gather_sum), not link counting. Sum graphs are pure INC chains
   with zero guard/set cells: sum MAPs are invisible to chain
   perception for a stronger reason than count MAPs (no chain cells
   whatsoever, not even broken guard/set alternation).
2. Y is goal-directed planning indexed by computed numeric parameters.
3. The number-typed domain is a different arithmetic (sum, not count),
   which discriminates count-specific machinery. This is what kills
   the XIO control (see below).

## Results

### Competence (all mechanisms, TREAT): AP-COMP HOLDS

| Query | H1 | H2 | H3 | XIO | via |
|-------|----|----|----|-----|-----|
| X1 (101,91)->15 | 15 | 15 | 15 | 15 | trial sum (1 tried, 0 rejected) |
| X2 (102,91)->10 | 10 | 10 | 10 | 10 | trial sum (1 tried, 0 rejected) |
| Y1 (15,92)->203 | 203 | 203 | 203 | 203 | trial chain [82,82,82] (2 tried, 1 rejected) |
| Y2 (10,92)->213 | 213 | 213 | 213 | 213 | rebind (1 tried, 0 rejected) |

MAP census (identical across mechanisms, ids vary):
- 2 arith MAPs: r=91, plen=-1 (pure INC chains), oty=1.
- 2 plan MAPs: r=92, plen=4, relseq [82,82,82], oty=0, class=chain.

Both domains are solidly learned. Every negative below is clean.

### Z: H1/H2/H3 KILLED, XIO control FAILS, all arms

| Arm | H1 Z | H2 Z | H3 Z | XIO Z |
|-----|------|------|------|-------|
| TREAT | -2 | -2 | -2 | -2 |
| ABL-X | -2 | -2 | -2 | -2 |
| ABL-Y | -2 | -2 | -2 | -2 |
| FRESH | -2 | -2 | -2 | -2 |
| ABL-XIO | n/a | n/a | n/a | -2 |

No Z MAP promoted in any arm (ZMAP id=-1 throughout; XIO adapters=0
throughout). Trial alone cannot solve Z in FRESH (103's 71-facts reach
only 6 and 9, both leaves; sum(103)=15 != 203; count(103)=2 != 203),
so the failures are mechanism-specific, not a broken world.

SHA-256 (3/3 byte-identical runs each):
- H1: `213ac782c000525bab1b307966ab19a0d8fce8211cb2e170f60ffc3b28d16abf`
- H2: `69e193016877b1e3bddf727229abcd4107b4640e435bc42878c5b0f82663a639`
- H3: `8b2257ec8dc048d9324219cc769ea8b023f265af8b2aa32726a235b32e8fef32`
- XIO: `b5e2c1f412edc7a11309a560816fe92dffb6da4f359dbca3889909703319368c`

## Per-mechanism diagnosis (white-box)

### H1: mutation never stages (chain-bound at STAGING, one step earlier than harder)

`mu_best_plen` = 4 (the Y plan MAPs; sum MAPs return -1 from
`rb_chain_plen` because a pure INC chain fails the first guard(102)
expectation). `mutate_try` iterates plen-4 parents, but
`mu_extend_one` stages each parent on plen-4 gathered paths from the
query subject: `t2_gather(103)` yields only [103], [103,6], [103,9]
(the arithmetic facts are leaves), so the `get32(paths,base)==p`
condition never fires and `t2_try_verify` is never called:

```
RB-STAT tried=0 rejected=0
MUT-STAT tried=0 rejected=0
Z ans=-2
ZMAP id=-1
```

In the harder pair H1 mutated the wrong chains (tried=2, rejected=2);
here it cannot even stage. Same disease (mutation = extend a staged
navigation chain), localized one step earlier: the arithmetic subject's
facts do not form chains, so there is nothing to extend. A refinement
of the shared diagnosis, not a new one.

### H2: no fragments satisfiable (same localization as harder)

`ir_relseq` returns -1 for the sum MAPs (no guard/set cells at all),
so they contribute zero fragments. Y's plan MAPs ([82,82,82]) ARE
visible and fragmentable. But `ir_frag_candidates` from s=103 requires
an 82-fact with subject 103: `t2_lu_first(103,82)` = -1. Zero
candidates, DFS never starts:

```
RECOMB-FAIL
Z ans=-2
ZMAP id=-1
```

Identical failure shape to the harder pair: fragments exist, but the
chaining search is SUBJECT-ANCHORED. The needed first step is not
"walk from 103" but "compute sum(103)=15, then walk from 15": a
subject CHANGE to a computed value, which fragment chaining cannot
express.

### H3: constructs the wrong chains (search space is fact chains from 103)

H3 got the most generous protocol: `ev_query_c` with don't-care
constraints, plen swept 1..4, searching the entire chain space from
103:

```
Z plen=1 INVENT-STAT tried=1 rejected=1 ... Z ans=-2
Z plen=2 INVENT-FAIL ... Z ans=-2
Z plen=3 INVENT-FAIL ... Z ans=-2
Z plen=4 INVENT-FAIL ... Z ans=-2
ZMAP id=-1
```

At plen 1 the DFS builds 103->6 / 103->9 and both endpoints fail
verification against 203; at plen 2..4 there are no chains at all (6
and 9 are leaves). H3 builds chains FROM the subject THROUGH the
facts. The Z solution is not a chain from 103; it is a computation
(sum) followed by a plan from the computed value. H3's search space
does not contain the solution at ANY plen. Same as harder.

### XIO control: typed composition is COUNT-specific, not arithmetic-general (NEW)

This is the informative result of the wave. The census confirms the
adapter machinery PERCEIVES the pair correctly: sum MAPs have oty=1
(INC cells present), plan MAPs have oty=0, so the mismatch gate admits
(sum, plan) ordered pairs. But `xio_try` builds zero adapters and Z
fails in every arm:

```
Z ans=-2
adapters=0
```

White-box cause, at `xio_stage_exec` in xio_core.zag (verbatim): the
oty-1 (NUMBER) stage does NOT re-execute the MAP's own graph. It reads
the MAP's DEP relation (71, correctly recovered via `xio_dep_rel`)
and re-derives a COUNT graph: `t2_chain(W,x,rel)` +
`t2_asm_count(...)`. For a SUM MAP this computes count(103)=2, not
sum(103)=15. The plan stage from 2 then finds no 82-facts
(`t2_gather(2)` empty); reversed pairs fail at stage 1 (no 82-facts
on 103). Every ordered pair is rejected on white-box arithmetic
grounds.

So XIO's generality boundary is now mapped: it crosses chain/count
(C229) and count/chain (xio_harder) because its NUMBER stage
implements COUNT semantics, but it does NOT cross sum/plan. The oty
detector is arithmetic-general (any INC graph reads as NUMBER) while
the stage re-derivation is count-specific. A future fix is not a new
mechanism: the oty-1 stage must re-execute (or re-derive from
provenance) the MAP's OWN arithmetic graph instead of assuming count.
This finding was preregistered as the predicted XIO outcome in
PREREG2 (AP-XIO).

## The shared broken assumption (confirmed on a new pair)

All three invention mechanisms define invention as novel CHAIN
construction; the sum-then-plan pair confirms the C215/C231 diagnosis
generalizes:

| Stage | H1 | H2 | H3 |
|-------|----|----|----|
| Perception | rb_chain_plen (chain MAPs only; sum=-1) | ir_relseq (chain MAPs only; sum=-1) | invent_relseq (chain MAPs only) |
| Search | extend staged chain by 1 cell | chain (map,start,len) fragments | DFS over fact sequences |
| Assembly | t2_asm_chain | t2_asm_chain + SEQ links | t2_asm_chain |
| Goal test | verify walked value == expected | verify walked value == expected | verify walked value == expected |

Every cell assumes the solution is a walkable chain from the query
subject. The arithmetic domain (X) is invisible to all three
perception operators (more strongly here than for count: zero
guard/set cells, not broken alternation). The required handoff
(computed sum -> plan parameter) is unrepresentable in all three
search spaces. Plus the new XIO boundary: even the mechanism that
crosses chain/count pairs is count-specific in its NUMBER stage.

## Honest boundaries

1. One domain pair. The "generalizes" claim rests on the shared
   architectural reason (chain-bound invention), white-box evident in
   all four ports, not on sweeping the pair space.
2. H3's plen sweep (1..4) was the most generous protocol; H1/H2 got
   their standard pipelines (their patches' full ev_query).
3. X/Y competence is via trial/rebind (existing machinery), not via
   the invention stages. The invention stages were tested ONLY on Z:
   the question is whether invention crosses the domain gap.
4. Y plans are learned as chain graphs (the base's plan templates were
   removed under K-T2-2/K-T2-3); the planning-ness is in the world
   semantics (parameterized action sequences to goals). The
   mechanism-level gap tested is the computed-value handoff, which is
   identical for any sequence-valued Y domain.
5. Driver scaffold disclosed: the base's sum trial branch is gated on
   a combination-context node (tag 8) that the base only creates in
   its own test battery. Each driver creates one per arm
   (`ap_comb`/`apx_comb`), following the xio_general precedent
   (xgC_comb). It teaches no facts and no answers; without it the sum
   template is unreachable and competence would be VOID. This does not
   alter any frozen fact, query, expected value, arm, or kill bar.
6. PREREG.md (aa708f552) tested different mechanisms (novel
   typed-contract/value-composition, expecting success) and was
   superseded transparently by PREREG2.md (91e84ee0d) before any
   implementation under PREREG2 existed. Its artifacts
   (ap.zag/REPORT.md/ap_bin/runs) are preserved untouched in
   superseded_prereg1/.
7. Positive within-domain invention for H1/H2/H3 is established by
   their own reports (all COMPLETE); this worker's ports use their
   patches verbatim (concatenated, not modified). Training-phase
   signatures reproduce (X1/X2 trial sum, Y1 trial chain, Y2 rebind),
   confirming port fidelity.

## Standing metrics

- Cognition lines added: 0 (drivers only; patches and bases verbatim
  from prior workers).
- Modes / bridges / handlers / new semantic cases / domain-pair
  templates: 0 / 0 / 0 / 0 / 0.
- Researcher-owned: world design, drivers, ablation procedure, H3
  plen sweep, comb scaffold, search biases inherited from H1/H2/H3/XIO.
- Learner-owned: X/Y MAP graphs, trial verifies, rebind LINK14, oty
  labels.

## Deliverables

- `PREREG2.md` (frozen 91e84ee0d, before implementation)
- `NAMECHECK.md` (this worker: guard, assemblies, build record)
- `ap_driver.zag` (H1/H2), `ap_driver_h3.zag` (H3, plen sweep),
  `ap_driver_xio.zag` (XIO control)
- `ap_full_h1/h2/h3/xio.zag` (assembled), `ap_bin_h1/h2/h3/xio`
  (pinned znc)
- `ap_run_h1_1/2/3.txt`, `ap_run_h2_1/2/3.txt`,
  `ap_run_h3_1/2/3.txt`, `ap_run_xio_1/2/3.txt` (3/3 byte-identical;
  SHAs above)
- `ap_compile_h1/h2/h3/xio.txt`
- `superseded_prereg1/` (prior worker's PREREG.md-era artifacts,
  untouched)

Assembly recipes (bases/patches verbatim from sibling dirs, catted
directly, no copies or edits):
- H1: `cat ../invention_mutation/mu_core.zag ../invention_mutation/mu_patch.zag ap_driver.zag`
- H2: `cat ../invention_recombine/ir_base.zag ../invention_recombine/ir_patch.zag ap_driver.zag`
- H3: `cat ../invention_constraint/invent_base.zag ../invention_constraint/invent_patch.zag ap_driver_h3.zag`
- XIO: `cat ../composition_A/cx_core.zag ../xio_adapters/xio_core.zag ap_driver_xio.zag`

Pure Zag. Safebin PATH. Zero em/en dashes (byte-verified). Paper
untouched. Frozen source read-only. Committed locally, nothing pushed.
