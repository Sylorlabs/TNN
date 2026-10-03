# COUNTMAP-SINGLETON Architecture Analysis (2026-10-03)

Worker: COUNTMAP-SINGLETON. Non-ledger task (claim minting paused).
Branch: tnn-native-lab. Lane: docs/lab/research-lead/overnight-20260928/countmap_singleton/
Method: read-only source analysis of the XP-DAGFAN-4 frozen build
(xdagfan4_block.zag on lane-xdagfan2-20261003, HEAD cea1856d2).
No experiment built, no code run, no branch touched.

## Question

XP-DAGFAN-4 discovered that `xs5_find_countmap` is a singleton and
that the prereg's MAP_V (a second count structure) was impossible.
Parent asks: is the singleton count MAP an architecture fact
constraining all future count-composition designs, and does it
warrant a dedicated experiment?

## Short answer

The singleton is real but it is a composition-layer design choice,
not a protected-core invariant. It decomposes into four separable
facts, only one of which is the lookup the worker hit. The precise
statement: exactly one count MAP is *addressable* by the
XS5/XHIER composition layer per world lifetime; the base trial
layer can *form* more, but they are invisible to composition; and
the query pipeline order makes the first count MAP suppress the
formation of alternatives. A dedicated experiment is warranted, but
not as a rerun proving the singleton. It is warranted as (1) a
frozen negative result banking the two-relation failure mode, and
(2) a design-alternative test of an indexed count MAP lookup.
Prereg sketches for both are in Section 7.

## 1. What "singleton" means: scope

One count MAP per world lifetime, visible to the XS5/XHIER
composition layer. Concretely:

* `xs5_find_countmap` (xdagfan4_block.zag:2134) scans the whole node
  table (ids 2..1023) and returns the FIRST live (field36==1) tag-20
  MAP whose field-20 graph contains an INC cell (tag 103). No
  relation parameter, no query-context parameter, no frame
  parameter. The scope is global to the learner world.
* Every aggregation path in the composition layer goes through this
  one lookup. There is no second call site pattern, no fallback,
  no "which count MAP" argument anywhere in xs5/xhier code.

So "singleton" = the composition layer has exactly one addressable
count structure, selected by lowest live node id, for the entire
world. It is not one-per-relation, one-per-composite, or
one-per-context.

## 2. Source-verified decomposition (four facts)

### Fact A. The lookup is singleton by construction (code)

```zag
fn xs5_find_countmap(W:[]u8)i32 {
  let m:i32=2;
  while(m<1024){
    if(ng(W,m,36)==1 && ng(W,m,0)==20){
      if(xs5_has_inc(W,ng(W,m,20))==1){return m;}
    }
    m=m+1;
  }
  return -1;
}
```

First match wins; the function cannot return a second count MAP
even if one exists. Three call sites, all treating the result as
THE count MAP:

* `xs5_agg_rel` (:2147): derives the world's single aggregation
  relation r_agg from the singleton's first type-1 provenance edge.
  One r_agg per world, fixed at first count learning.
* `xs5_agg_exec` (:2177): hard gate. No singleton, no aggregation
  at all (returns -2). The count template is assembled fresh per
  query via `t2_asm_count` over r_agg; the singleton MAP's stored
  INC graph is never executed by the composition layer. The MAP is
  a capability token plus provenance carrier plus LINK14 target,
  not an executed procedure.
* `xs5_try_nav_agg` (:2190): every promoted composite MAP_Z gets
  LINK14 edges to (nav MAP, singleton count MAP). All composites
  share numerically the same count MAP node.

### Fact B. Formation is unbounded in principle (code)

`promote_graph` (:533) mints a fresh tag-20 MAP per call with no
dedup check. `t2_trial`'s count path (:635-647) iterates relations,
assembles a count graph per relation chain via `t2_asm_count`, and
promotes on verify. Nothing in the base layer prevents a second,
third, or tenth count MAP. In the XP-DAGFAN worlds exactly one
formed only because exactly one relation (82) was ever successfully
counted through the trial path.

Correction to the A1 amendment's phrasing: "a second count
structure MAP_V cannot form" is mechanism-relative, not
architectural. Under XS5-SELECT adaptation it cannot form (Fact D).
Via the base trial path it can form whenever a count verifies
against expected. What cannot happen, in any current code path, is
*addressing* a second count MAP through the composition layer.

### Fact C. Pipeline order makes the singleton self-reinforcing (code)

`ev_query_xs5` (:2423) tries, in order: activate, rebind,
`xs5_compose`, then `mp_run`/`t2_trial`, then bootstrap, then
`xs5_select`. Once the first count MAP exists, any query countable
over the singleton's r_agg succeeds inside `xs5_compose`, which
runs BEFORE the trial layer. The trial count path, the only
formation path for new count MAPs, therefore never fires for
already-covered counting. The first-learned aggregation relation
wins permanently, and the mechanism that could create an
alternative is starved by the earlier success of the mechanism
that reuses the incumbent. This is a genuine architecture-dynamic
fact, not just a code shape: the singleton is dynamically stable,
not merely statically imposed.

Consequence: a world that later needs counting over a second
relation WILL reach the trial layer (composition fails: r_agg is
fixed, verify against expected fails), and trial CAN mint the
second count MAP, but the composition layer will still ignore it
(Fact A). Formation without addressability.

### Fact D. The adaptation layer cannot create count structures (code)

`xs5_select` (:2391) adapts only chain MAPs: TRUNCATE and REROUTE
operate on relseqs extracted via `cc_relseq`. Count graphs are
INC-cell structures, not chains; they have no relseq to truncate
or reroute. `xs5_agg_exec` assembles count graphs ephemerally per
query and never promotes them as MAPs. So the L2-style adaptation
machinery that the current research program cares about most is
structurally blind to count structure. This is the actual reason
MAP_V was impossible in XP-DAGFAN-4 run 1: no 83-relseq MAP
existed to truncate, verify declined the 83-count (2 vs expected
4, per `t2_try_verify` :497 which requires v==expected unmasked),
and no mechanism in the frozen world could synthesize an
83-count structure.

## 3. What designs the singleton rules out

At the composition layer (XS5/XHIER as frozen in XP-DAGFAN-1..4):

1. Two simultaneous aggregation relations. Z_a counting over rel
   82 and Z_b counting over rel 85 cannot both be composed:
   `xs5_agg_rel` yields one r_agg; a second count MAP is invisible.
2. Per-composite aggregation templates. Every MAP_Z shares the
   numerically identical count MAP node via LINK14.
3. Learner-authored count variants selected by composition. No
   "which count MAP" parameter exists; the learner could not get a
   second count procedure *used* even if it created one.
4. Context-dependent counting (per query context, per frame, per
   nav endpoint).
5. Count-structure adaptation: truncate/extend/specialize/reuse of
   the count template itself, the exact L2 operations now top
   priority, cannot apply to the one structure every composite
   depends on.

What it does NOT rule out: the base trial layer learning a second
count (unreachable through composition); ablation of the
singleton killing all aggregation at once (already demonstrated in
spirit by XP-DAGFAN-4 K7 for the nav part); worlds that need only
one aggregation relation (all current DAGFAN worlds).

## 4. Frozen limitation or design choice?

Design choice, at the experiment layer. Two senses of "frozen"
must be kept apart:

* Protected-core sense: NO. `xs5_find_countmap` is defined in
  xs5_patch.zag, whose own header says "Pure Zag. Unfrozen only."
  The protected machinery (`t2_asm_count`, `t2_try_verify`,
  `promote_graph`, the ISA ops) is fully capable of minting,
  verifying, and executing multiple count structures. No core
  change is needed to support indexed count MAPs.
* Per-experiment freeze sense: YES for XP-DAGFAN-1..4, where the
  xs5/xhier patches were part of the frozen build block. But that
  freeze is per experiment and is lifted by the next prereg. It
  does not bind future count-composition designs.

Could it be changed? Yes, cheaply: index count MAPs by their
provenance relation (r_agg is already learner-derived per MAP via
type-1 provenance edges), e.g. `xsN_find_countmap(W, r_wanted)`,
and record per-composite which count MAP was used at LINK14 time.
Zero new edge types, zero new MAP types, zero new opcodes; the
provenance needed for the index already exists.

Should it be changed? Not speculatively. The trigger should be a
real experimental need: the first lane that requires two
aggregation relations (heterogeneous composition, L2 adaptive
reuse across structures with different aggregation, arithmetic to
planning with partial mismatch). Until then, the singleton is a
documented constraint, and the DAGFAN kill bars that assume it
(P5.1 "MAP_Y has exactly 2 incoming") remain valid for their
worlds.

## 5. Implications for future count-composition designs

* Any design needing more than one aggregation relation must
  replace the global lookup with a parameterized one. The lookup
  is the single point of change; formation and execution already
  generalize.
* Composites must record WHICH count MAP they used, not just that
  they used "the" count MAP. The current LINK14-to-singleton
  pattern bakes the assumption into every composite's structure.
* Kill-bar hygiene: frozen DAGFAN bars that assert singleton
  sharing stay valid for single-relation worlds; a multi-count
  design needs its own prereg, not an amendment to those bars.
* The self-reinforcement (Fact C) is the subtlest part for future
  designs: any indexed lookup must also handle the case where the
  wanted count MAP does not exist yet, i.e. composition must be
  able to *request* formation (fall through to trial per wanted
  relation) rather than only reuse. Currently the fall-through is
  accidental (compose fails, trial happens to try); an indexed
  design should make it deliberate.
* Connection to the 2026-10-03 architectural clarification: the
  count MAP's r_agg is already a learned property (derived from
  type-1 provenance, never hardcoded), which is the right shape.
  What is missing is *selection by* learned properties at the
  composition layer. The singleton lookup selects by "first live
  node id", which is an implementation accident, not a learned
  property. Fixing that is aligned with the domain-blindness
  direction, not in tension with it.

## 6. What was tested vs what was reasoned

Tested (by XP-DAGFAN-4, PASS 22/22, 3/3 byte-identical, on
lane-xdagfan2-20261003): the singleton's observable consequences
in a single-relation world. ZW shares MAP_Y; MAP_Y has exactly 2
MAP_Z consumers; killing t leaves (110,115,4)=4 via the
t-independent ZW. The amendment A1 run 1 (-2, XS5-CREATED n=0)
empirically confirmed that no frozen mechanism could produce
MAP_V in that world state.

Reasoned (this report, from read-only source analysis, no new
runs): Facts A through D, the formation/addressability split, the
pipeline-order self-reinforcement, the five ruled-out designs, and
the frozen-vs-choice distinction. These are code-determined, not
empirically uncertain, but they have not been executed as frozen
kill-barred claims. Section 7 proposes the experiments that would
bank them.

## 7. Recommendation: the warranted experiments

A dedicated experiment IS warranted, but scoped as below. A rerun
"proving" the singleton would add nothing: the lookup is six lines
of code. What is worth freezing:

### XP-COUNTMAP-1: two-relation negative (banks Facts A-C)

World: teach counting over rel 82 (forms MAP_Y as today), then
teach counting over rel 85 with verifying expected so `t2_trial`
mints a second live count MAP (MAP_V2). Frozen kill bars:

* K1: two live count MAPs exist (both tag-20, both INC-ok).
* K2: `xs5_find_countmap` still returns MAP_Y (lowest id).
* K3: `xs5_agg_rel` still returns 82.
* K4: a composition query requiring an 85-count returns -2 through
  the composition layer while the trial layer answers it: the
  formation/addressability split, demonstrated, not asserted.
* K5: determinism 3/3 byte-identical; pure Zag; safebin.

This converts the code-reading claim into a frozen negative
result that future designs must beat.

### XP-COUNTMAP-2: indexed lookup alternative (design probe)

Replace the global lookup with an r_agg-indexed lookup in a new
unfrozen patch; rerun the two-relation world. Frozen kill bars:

* K1: both composites form, each LINK14 to its own count MAP.
* K2: both composition queries answer correctly.
* K3: regression: the full XP-DAGFAN-4 22-check suite still
  passes verbatim (singleton worlds must be unaffected).
* K4: determinism, toolchain as usual.

Recommendation: run XP-COUNTMAP-1 now (cheap, banks the
architecture fact as a frozen result). Hold XP-COUNTMAP-2 until a
lane actually needs two aggregation relations, or run it as a
low-priority design probe. Do not change the singleton
speculatively: no current lane needs it, and the DAGFAN bars
assume it.

## 8. Notes for the parent

* No ledger entry: non-ledger task, nothing minted.
* No commits to lane-xdagfan2-20261003; nothing merged; this
  report is the only new file, committed on tnn-native-lab only.
* Toolchain: no build was performed (analysis only), so no
  safebin activation was needed; all claims rest on read-only
  `git show` of the committed XP-DAGFAN-4 artifacts.
* The A1 amendment's "cannot form" phrasing should be read with
  the Fact B correction if it is cited in future preregs: second
  count MAPs can form via trial; they cannot be addressed via
  composition. The distinction matters for any future
  multi-aggregation design.
