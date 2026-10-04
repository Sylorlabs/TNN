# REPORT.md -- X-Domain Harder Pair: Invention Mechanisms on Transform-then-Navigate

## Verdict: XDOMAIN-HARDER-COMPLETE (clean negative, shared diagnosis)

**No invention mechanism (H1, H2, H3) crosses the domain gap that
composition could not. All three fail on a HARDER pair
(transform-then-navigate) for the same shared architectural reason:
every invention mechanism is a novel-CHAIN constructor, and
cross-domain composition needs typed function composition with a
computed-value handoff. The failure is clean, deterministic (3/3
byte-identical per mechanism), and diagnosed to the exact line where
each mechanism's chain assumption breaks.**

## The harder pair

X = COUNT (transform, node -> number). Y = CHAIN on numeric subjects
(navigate, number -> node). Z = Y(X(s)): count s's links to get k,
then walk the Y chain starting FROM k. Query (21,93) -> 52.

Harder than chain+count in three ways (all preregistered):

1. The FIRST domain (X=count) is non-navigational and invisible to
   every chain-based perception operator. In chain+count, X=navigate
   was visible; only Y was invisible. Here the mechanisms fail at
   perceiving X itself.
2. The intermediate k=4 is a COMPUTED NUMBER, not a fact-store node.
   Feeding a computed value as a navigation subject is a type
   transition (value -> subject) that no chain machinery performs.
3. Y's chain MAPs are learned on NUMERIC subjects (3, 2); Y's knowledge
   is indexed by computed values.

Structural difference: X count graphs use guard(102)/set(101) +
INC(103) + MOV epilogue; Y chain graphs use guard/set only
(different cell types). X outputs a NUMBER; Y outputs a NODE
(different output kinds).

## Results

### Competence (all mechanisms, TREAT): XH-COMP HOLDS

| Query | H1 | H2 | H3 | via |
|-------|----|----|----|-----|
| X1 (11,91)->3 | 3 | 3 | 3 | trial count template |
| X2 (15,91)->2 | 2 | 2 | 2 | trial count template |
| Y1 (3,92)->32 | 32 | 32 | 32 | trial chain [82,82,82] |
| Y2 (2,92)->42 | 42 | 42 | 42 | rebind (LINK14) |

MAP census (identical across mechanisms, ids vary):
- 2 count MAPs: r=91, plen=-1 (INC breaks guard/set alternation),
  class=count.
- 2 chain MAPs: r=92, plen=4, relseq [82,82,82], class=chain.

Both domains are solidly learned. The negative is clean.

### Z: all mechanisms fail, all arms (XH-H1/H2/H3 KILLED)

| Arm | H1 Z | H2 Z | H3 Z |
|-----|------|------|------|
| TREAT | -2 | -2 | -2 |
| ABL-X | -2 | -2 | -2 |
| ABL-Y | -2 | -2 | -2 |
| FRESH | -2 | -2 | -2 |

No Z MAP promoted in any arm (ZMAP id=-1 throughout). Trial alone
cannot solve Z in FRESH (the 81-chain from 21 reaches 22..25, never
52; count(21)=4 != 52), so the failure is invention-specific, not a
broken world.

SHA-256 (3/3 byte-identical runs each):
- H1: `6126c2a3ce047954a44c068a4f117d7e04c210b7a8fd75148fcb677cde4df379`
- H2: `d05623b740b048cd5687ecf4ce08e146ad36ceaa6a84a222e15c446b9a37c06a`
- H3: `bf37838d26df1a93d4b595e1e2f014d83138aa28fd66feaf9247ff43ed94dec8`

## Per-mechanism diagnosis (white-box)

### H1: mutates the wrong chains (perception sees Y, not X; action extends navigation)

`mu_best_plen` scans MAPs via `rb_chain_plen`. The X count MAPs return
-1 (INC cell breaks guard/set alternation), so the ONLY mutation
parents are Y's chain MAPs (plen 4). `mu_extend_one` stages them on
21, executes along 21's 81-facts to 24, and extends into (24,81,25).
The extension is a LONGER 81-CHAIN, verified against 52:

```
RB-STAT tried=2 rejected=2
MUT-STAT tried=2 rejected=2
Z ans=-2
ZMAP id=-1
```

Two extensions tried (one per Y parent), both rejected: the extended
chain computes 25, not 52. H1's "too short" signal fires on the wrong
domain (it extends Y's navigation instead of bridging X's computation),
and even a successful extension could only produce a longer walk, never
a count-then-walk. The mutation operator is navigation-only: it cannot
represent "compute k, then navigate from k" because it has no
value-as-subject step.

### H2: no fragments satisfiable (perception sees Y, not X; chaining needs a start)

`ir_relseq` returns -1 for the X count MAPs (INC cell), so they
contribute zero fragments. Y's chain MAPs ([82,82,82]) ARE visible and
fragmentable. But `ir_frag_candidates` from s=21 requires an 82-fact
with subject 21: `t2_lu_first(21,82)` = -1. Zero candidates, DFS never
starts:

```
RB-STAT tried=2 rejected=2
RECOMB-FAIL
Z ans=-2
ZMAP id=-1
```

H2's failure localizes precisely: fragments exist (Y's chains), but
the chaining search is SUBJECT-ANCHORED. It can only chain fragments
starting from the query subject's facts. The needed first step is not
"walk from 21" but "compute count(21)=4, then walk from 4" -- a
subject CHANGE to a computed value, which fragment chaining cannot
express. Even if X's count MAPs were fragmentable, chaining a count
fragment to a chain fragment would concatenate their relseqs, not feed
the count's numeric output as the chain's subject.

### H3: constructs the wrong chains (search space is fact chains from 21)

H3 got the most generous protocol: `ev_query_c` with don't-care
constraints, plen swept 1..4, searching the ENTIRE chain space from 21.
The DFS succeeds at every plen (21->22, 21->22->23, ...), but every
constructed chain is an 81-chain whose endpoint (22/23/24/25) fails
verification against 52:

```
Z plen=1 INVENT-STAT tried=1 rejected=1 ... Z ans=-2
Z plen=2 INVENT-STAT tried=1 rejected=1 ... Z ans=-2
Z plen=3 INVENT-STAT tried=1 rejected=1 ... Z ans=-2
Z plen=4 INVENT-STAT tried=1 rejected=1 ... Z ans=-2
ZMAP id=-1
```

(Correction to the prereg's prediction wording: the outcome is
verify-failure, not DFS INVENT-FAIL, because 21's 81-facts DO form
chains. The conclusion is unchanged: no fact chain from 21 reaches
52.) H3 builds chains FROM the subject THROUGH the facts. The Z
solution is not a chain from 21; it is a computation (count) followed
by a chain from the computed value. H3's search space (fact sequences
anchored at s) does not contain the solution at ANY plen, so no
constraint set could find it.

## The shared broken assumption

All three invention mechanisms define invention as **novel CHAIN
construction**:

| Stage | H1 | H2 | H3 |
|-------|----|----|----|
| Perception | rb_chain_plen (chain MAPs only) | ir_relseq (chain MAPs only) | invent_relseq (chain MAPs only) |
| Search | extend staged chain by 1 cell | chain (map,start,len) fragments | DFS over fact sequences |
| Assembly | t2_asm_chain | t2_asm_chain + SEQ links | t2_asm_chain |
| Goal test | verify walked value == expected | verify walked value == expected | verify walked value == expected |

Every cell assumes the solution is a walkable chain from the query
subject. The count domain (X) is invisible to all three perception
operators. The required handoff (computed number -> navigation
subject) is unrepresentable in all three search spaces. This is the
SAME disease as composition A/B/C (navigation concatenation), one
level deeper: not only is COMPOSITION chain-bound, INVENTION is
chain-bound too.

What cross-domain needs (confirmed harder here):

1. **Typed I/O contracts**: node->number (count) vs number->node
   (chain). Plen/relse q describe path shape, not computation.
2. **Computed-value handoff**: k = X(s) must become Y's SUBJECT.
   No current machinery re-subjects a query to a computed value.
3. **Heterogeneous execution**: a count graph feeding a chain graph,
   not longer chains.

## Honest boundaries

1. The pair is harder than chain+count by construction (invisible
   first domain, computed intermediate, reversed handoff), but it is
   still one pair. The shared architectural reason (chain-bound
   invention) is white-box evident in all three patches, not swept
   from the pair space.
2. H3's plen sweep (1..4) was the most generous protocol; a critic
   cannot blame constraint choice. H1/H2 got their standard pipelines
   (their patches' full ev_query).
3. X/Y competence is via trial/rebind (existing machinery), not via
   the invention stages. The invention stages were tested ONLY on Z,
   which is the correct isolation: the question is whether invention
   crosses the domain gap.
4. B's type-15 history (the one piece that crossed the gap in
   composition-xdomain) has no analogue in H1/H2/H3: none of them has
   a cross-domain co-use episode concept. If a future mechanism keeps
   B's history and adds typed function composition, these results say
   the composition operator must be rebuilt, not just the history.
5. Positive within-domain invention for H1/H2/H3 is established by
   their own reports (all COMPLETE); this worker's ports use their
   patches verbatim (concatenated, not modified). Training-phase
   signatures reproduce (X1/X2 trial count, Y1 trial chain, Y2 rebind
   + LINK14), confirming port fidelity.

## Standing metrics

- Cognition lines added: 0 (drivers only, ~150 lines each; patches
  and bases verbatim from prior workers).
- Modes / bridges / handlers / new semantic cases / domain-pair
  templates: 0 / 0 / 0 / 0 / 0.
- Researcher-owned: world design, drivers, ablation procedure, H3
  plen sweep, search biases inherited from H1/H2/H3.
- Learner-owned: X/Y MAP graphs, trial verifies, rebind LINK14.

## Deliverables

- `xh_driver.zag` (H1/H2), `xh_driver_h3.zag` (H3, plen sweep)
- `xh_full_h1/h2/h3.zag` (assembled), `xh_bin_h1/h2/h3` (pinned znc)
- `xh_run_h1_1/2/3.txt`, `xh_run_h2_1/2/3.txt`, `xh_run_h3_1/2/3.txt`
  (3/3 byte-identical; SHAs above)
- `xh_compile_h1/h2/h3.txt`, `PREREG.md` (frozen 23266dc1c),
  `NAMECHECK.md`, `REPORT.md` (this file)

Assembly recipes (bases/patches verbatim from sibling dirs):
- H1: `cat ../invention_mutation/mu_core.zag ../invention_mutation/mu_patch.zag xh_driver.zag`
- H2: `cat ../invention_recombine/ir_base.zag ../invention_recombine/ir_patch.zag xh_driver.zag`
- H3: `cat ../invention_constraint/invent_base.zag ../invention_constraint/invent_patch.zag xh_driver_h3.zag`

Pure Zag. Safebin PATH. Zero em/en dashes (byte-verified). Paper
untouched. Frozen source read-only. Committed locally, nothing pushed.
