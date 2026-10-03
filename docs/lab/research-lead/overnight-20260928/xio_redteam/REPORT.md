# REPORT.md -- XIO Adapter Red-Team Battery

## Verdict: XIO-REDTEAM-COMPLETE

Eight adversarial attacks executed against the H-XIO-1 typed I/O
adapters (commit e34ed5ebc). Per-attack verdicts:

- A1 type confusion (structural INC, NODE output): **KILL**
- A2 wrong handoff (first-valid path, coincidental verify): **BOUND**
- A2b denial by distractor shadowing: **BOUND**
- A3 adapter explosion brake: **SURVIVE** (count) / **BOUND** (compute)
- A4 stale adapter (revision, deletion): **BOUND** (4a SURVIVE, 4b SURVIVE)
- A4c id recycling silently rebinds a stage: **KILL**
- A5 three-stage (pair-only): **BOUND**
- A6 oty proxy vs the sum family: **KILL**

Scope note: this battery does not rerun H-XIO-1's frozen kill bars
(K1-K8) and does not void XIO-ADAPTERS-COMPLETE. It bounds the trust:
the adapter mechanism is sound inside its tested envelope
(chain/count families, no MAP deletion or id recycling, two-stage
compositions, first-valid-path worlds) and unsound outside it. Three
kills, all with concrete reproductions below.

## Method

`rt_full.zag` = frozen base + xio_core (first 1924 lines of
`xio_full.zag`, driver cut off) + new red-team driver `rt_driver.zag`.
Eight attack worlds, each a fresh 110656-byte learner. Pure Zag,
safebin PATH. 3/3 runs byte-identical, sha256
`d22cab6cafe0759003a872a11359096a544a83ee97a375a83fde5912728e35c4`
(`rt_run1/2/3.txt`). Line citations below refer to `rt_run1.txt`.

---

## A1: type confusion -- KILL

**Design.** Hand-build MAP S: a chain graph (guard/set per link) with
an INC cell on slot 1 after every set (a step counter), output = the
walked node on slot 0. INC is used structurally; the MAP outputs a
NODE. If oty is a real type signature, oty(S) must be 0.

**Predicted.** oty(S)=1 (misclassified); the true pair (S as chain
stage, count MAP as count stage) is killed by the oty-difference gate;
the composite query fails; a control world with a trial-built chain
MAP succeeds.

**Observed.**
- Line 7: `A1 S=131 oty(S)=1 exec(S,21)=24 chainstage(S,21)=-999999`.
  The graph is competent (executes to node 24) but oty says NUMBER.
- Line 8: `PAIRS n0=0 n1=3 gated=6 tried=0`. All three MAPs (S + two
  count MAPs) are oty 1; every ordered pair is gated out. xio_try never
  considers the true pair.
- Line 10: `A1 ans=-2 adapters=0`. The composition fails.
- Control, lines 18-21: `PAIRS n0=1 n1=2 gated=2 tried=4`,
  `XIO-BUILD ... m1=138 m2=44 o1=0 o2=1 ... mid=24 ans=2`,
  `A1c ans=2 adapters=1`. Identical facts, correctly classified chain
  MAP: the composition works.

**Why KILL.** The misclassification alone would be a blemish; the
oty-difference gate converts it into permanent exclusion: a competent
MAP can never serve as either stage of any adapter. Worse, the two
structural proxies disagree with each other: oty says NUMBER while
`rb_chain_plen` (strict alternating 102/101 check) returns -1, so S is
stranded in a dead zone, unusable as a chain stage by rebind/staging
and unpairable as a count stage by the gate. "Contains INC" is a fact
about the frozen ISA's mechanics, not a type signature; inferring
output type from it bakes a researcher-side semantic assumption into
the mechanism.

**Honest bound.** The learner's current trial cannot promote such a
graph (chain/count/sum templates only), so the proxy holds on the
trial's actual output distribution. The kill is principled, not live:
any future MAP family that uses INC structurally (bounded walks need
counters) breaks pairing completely, not gracefully.

## A2: wrong handoff -- BOUND

**Design.** Standard Z world, but decoy chain facts taught BEFORE the
true Z facts: (31,81,91),(91,81,92),(92,81,93), plus a decoy count
chain (93,82,94),(94,82,95) whose count (2) coincides with the expected
answer. The true path 31-32-33-34 (mid=34) still exists.

**Predicted.** The oty-0 stage takes the first valid gathered path
(the decoy, lower fact ids), the decoy count verifies by coincidence,
and the adapter is built on the wrong intermediate.

**Observed.**
- Line 33: `XIO-BUILD id=411 m1=27 m2=115 o1=0 o2=1 rel1=81 rel2=82
  qr=93 mid=93 ans=2`. Built on mid=93, not 34.
- Line 37: `XIO-REUSE id=411 ans=2`; line 38: `A2 reuse ans=2
  adapters=1`. Fresh subject 41 reuses correctly (41-44-2).

**Why BOUND, not KILL.** Staged execution is first-valid, not best,
and expected-answer verification cannot distinguish the intended
composition from a coincidental one, so the BUILD audit trail records
a wrong intermediate. But execution re-derives both stages from live
learner state on every use, so the wrong intermediate is not
memorized: reuse self-heals. The damage is contained to provenance,
not answers. A perverse-but-stable property: the adapter is a correct
procedure with a false birth certificate.

## A2b: denial by distractor shadowing -- BOUND

**Design.** Same as A2, but the decoy count chain is a single link
(93,82,94), so the decoy count (1) does NOT match the expected answer
(2).

**Predicted.** The true pair is rejected (first-valid v1=93, count 1
!= 2 for every pair), the query fails despite a valid composition
existing.

**Observed.** Line 50: `A2b ans=-2 adapters=0`. Lines 51-52 enumerate
the len-4 paths and their counts: `path-end=93 count=1`,
`path-end=34 count=2`. The true composition (34-2) exists and is
visible, but every pair is rejected on the shadowed first path.

**Why BOUND.** The fragility is base-wide first-match semantics
(`t2_gather` id-ordered BFS, `t2_lu_first`), which the adapter
inherits; it is not an adapter-specific defect. The adapter fails
closed (-2, no adapter) rather than building wrong. Documented as a
denial-of-composition bound: one distractor path of equal length
kills the true pair, and xio_try does not try the next path for the
same pair.

## A3: adapter explosion brake -- SURVIVE (count) / BOUND (compute)

**Design.** (a) Repeated and multi-relation composite queries; (b) a
direct masked `xio_try` call; (c) an instrumented full pair scan on a
failing composite, run twice.

**Predicted.** At most one adapter per query; relation-keyed dedup;
masked builds nothing; the failing scan repeats identically (no
negative memoization).

**Observed.**
- Lines 64-66: q1 builds (mid=34), q1b reuses, adapters stay 1.
- Lines 70-71: new relation qr=94 builds a second adapter (mid=74);
  adapters=2. Growth is linear in verified composite relations.
- Line 74: `A3 masked-try=-2 adapters-before=2 adapters-after=2`.
- Lines 84-86: `A3 failq=-2` then two identical
  `SCAN tried=8 rejected=8 stage-calls=12` lines.

**Why SURVIVE on the count question.** The brakes hold: one build per
query (xio_try returns after the first verified build), relation-keyed
lookup prevents duplicates, masked mode builds nothing, and the
`xio_has_typed` gate skips the scan entirely when no oty-1 MAP exists.
**Why BOUND on compute.** Every failed query re-runs the full
quadratic pair scan (8 tried pairs, 12 stage executions for 4 MAPs,
each stage doing a full BFS gather plus graph rebuild); there is no
failure memoization. The H-XIO-1 report already discloses brute-force
pairing as future work; this quantifies it.

## A4: stale adapter -- BOUND (4a SURVIVE, 4b SURVIVE)

**Design.** Build the standard adapter, then (4a) revise the world
(extend the count chain so the true count becomes 3), then (4b) delete
the count stage MAPs.

**Predicted.** 4a: the adapter serves the new answer (re-derivation),
the recorded answer goes stale-but-unused, the old answer is cleanly
rejected. 4b: the orphaned adapter serves nothing.

**Observed.**
- Line 99: `XIO-REUSE id=380 ans=3`; line 100: `rec-ans-now=2`. The
  adapter re-derived the revised world; field 28 still says 2 and is
  never consulted.
- Line 102: `A4a old-answer=-2`. The expected-check in `xio_adapt`
  rejects the stale answer instead of serving it.
- Line 104: `A4b del-m2 old-ans=-2 adapters=1`. The orphaned adapter
  (m2 deactivated) serves nothing; `xio_exec` checks liveness and tag
  on every call.
- Line 107: `A4b relearn=3 adapters=1` with no XIO line: the base
  trial re-learned the revised composite on its own.

**Why BOUND (not SURVIVE).** Revision and deletion are handled
cleanly, which is genuine robustness: execution re-derives oty,
graph root, and DEP relation from live state on every call, so the
recorded fields are audit-only. But the orphan adapter node persists
(adapters=1) as dead weight, and the binding itself (bare node ids)
is not validated beyond liveness+tag. That is A4c.

## A4c: id recycling silently rebinds a stage -- KILL

**Design.** Build the adapter (m1=27 chain, m2=115 count). Delete the
chain MAPs, freeing ids 27 and 45. Hand-promote a COUNT MAP (built
with the base's own `t2_asm_count`/`promote_graph`) so first-fit
allocation lands it exactly on id 27, the adapter's recorded m1.

**Predicted.** The adapter's liveness+tag checks pass on the new
occupant; the recorded (o1=0, rel1=81) provenance silently describes
a stage that is now (oty=1, rel=82).

**Observed.**
- Line 121: `A4c newmap=27 ad.m1=27 rec-o1=0 live-oty(ad.m1)=1
  live-deprel(ad.m1)=81`. The new MAP took id 27. The adapter still
  points at it. Recorded o1=0, live oty=1: the binding was swapped
  with no signal.
- `live-deprel=81`, not 82: the deleted MAP's old DEP edges (to
  facts with rel 81) were never removed, and `xio_dep_rel` takes the
  first edge in id order, so the new MAP's own provenance (rel 82)
  is shadowed by the previous occupant's. Stale edges, not just a
  stale id.
- Cascade, confirmed by probes: the freed id 45 was taken by
  `promote_graph`'s internal `ev_teach_in` fact (31,82,7). Because
  `t2_gather` scans in id order, this low-id fact now sorts before
  the original (31,81,32) fact, so the masked trial's first-valid
  len-3 path became [31,7,70]. Line 123: `A4c masked-via-adapter=70`.
  The masked trial then PROMOTED a chain MAP (id 453) for (31,93)-70
  and TAUGHT the answer fact (31,93,70) (id 454). Line 124:
  `A4c unmasked-true=70` via `activate` on the poisoned fact, with no
  RB-STAT line: every future (31,93) query is now answered 70 before
  the adapter pipeline even runs.

**Why KILL.** A persistent procedural structure must not silently
change what procedure it denotes. The adapter holds bare node ids
with no generation check, and `alloc_node` is first-fit over freed
ids, so deletion plus re-promotion rebinds a stage undetectably.
The cascade shows the blast radius is not confined to the adapter:
recycled ids perturb the base learner's own id-ordered path
enumeration, a masked query teaches a wrong answer fact on
first-valid, and the query relation is permanently poisoned. Root
causes, in order: (1) bare-id binding without generations, (2)
first-fit id recycling, (3) first-valid-path trial semantics that
promote and teach on masked queries.

## A5: three-stage -- BOUND

**Design.** Reverse 2-stage control: count(50,82)=3, then a 3-link
83-chain walk from 3 to 72, query (50,96)-72. Three-stage: chain81
31-33, count82 33-2, chain83 2-72, query (31,95)-72. (An earlier
design used a 2-link 83-chain; probing showed rebind solved it via
the cross-relation path 50 -92-> 3 -83-> 70 -> 71, consuming the
promoted answer fact (50,92,3) as a navigation link. The 3-link chain
makes that path length 5, which no plen-4 chain MAP can rebind.)

**Predicted.** The reverse 2-stage builds a count-to-node adapter;
the 3-stage fails with adapters unchanged.

**Observed.**
- Line 135: `XIO-BUILD id=461 m1=115 m2=27 o1=1 o2=0 rel1=82
  rel2=81 qr=96 mid=3 ans=72`. The reverse direction works, symmetric
  by design.
- Line 139: `A5 three-stage ans=-2 adapters=1`. No adapter chaining:
  `xio_exec` performs exactly two stage executions and never
  consults `xio_adapt`; `xio_try` pairs MAPs only.

**Why BOUND.** Pair-only composition is confirmed as a hard boundary,
matching the prereg's honest boundary (one cross-domain family).
Three-stage needs are correctly refused, not silently misbuilt.

## A6: oty proxy vs the sum family -- KILL

**Design.** Enable sum trials exactly as the frozen base's own test
does (hand-placed tag-8 node, cf. t_p2). Teach (60,84,3),(60,84,5);
query (60,94)-8 promotes a sum MAP (INC-only graph, output 8, a
NUMBER, so oty=1 is correct). Then check what the adapter's stage
re-derivation computes for it, and whether xio_try excludes it.

**Predicted.** The stage re-derivation (which assumes oty 1 means the
count family) miscomputes; the prereg's "sum MAPs are excluded from
pairs (documented, not tested)" is not enforced in code.

**Observed.**
- Lines 147-149: `A6 sum-train=8`, `A6 sumMAP=59 oty=1`,
  `A6 true-out=8 xio-stage=1`. The MAP truly outputs 8; the
  adapter's stage procedure computes 1 (it re-derives a count graph
  over the sum's provenance relation: a degenerate 2-chain).
- Line 150: `PAIRS n0=2 n1=1 gated=2 tried=4`. All four ordered
  (chain,sum)/(sum,chain) pairs are tried. There is no sum exclusion
  anywhere in `xio_try`.

**Why KILL.** Two independent breaks of documented claims: (1) the
exclusion exists only in prose, not in code; (2) the "typed" stage
dispatch is really chain-or-count dispatch, and it silently
miscomputes for the third oty-1 family. A composite query whose
expected answer coincided with the mis-staged value would build a
wrong adapter with a clean audit trail. The type proxy is 2-valued;
the world is not.

## Synthesis: what the kills have in common

All three kills are the same architectural smell: the adapter
mechanism reasons about MAPs through **structural proxies** (INC
scan for type, first DEP edge in id order for relation, bare node
id for identity, first gathered path for the handoff) rather than
through **behavioral or generative evidence** (what the graph
computes, which promotion created this node, which path the trial
would defend). Inside the H-XIO-1 test envelope the proxies agree
with reality, which is why K1-K8 pass. Outside it they diverge
silently: no error, no abstention, just wrong provenance (A2),
wrong pairing exclusion (A1), wrong staging (A6), or wrong identity
(A4c). The bounds (A2b, A3-compute, A5) are the flip side: where the
mechanism fails, it mostly fails closed, which is to its credit.

Candidate repairs, in order of leverage:
1. Behavioral stage dispatch: try each stage family per MAP and keep
   what verifies, instead of the 2-valued oty proxy. Fixes A1
   (exclusion) and A6 (mis-staging) at once.
2. Generation-checked stage binding: record the MAP's promotion
   index (field 24) or a monotonic generation in the adapter;
   `xio_exec` refuses on mismatch. Fixes A4c's silent rebinding.
3. Provenance hygiene: DEP edges should not outlive their MAP, or
   `xio_dep_rel` should prefer the MAP's own newest edges. Fixes the
   stale-relation shadowing inside A4c.
4. Per-pair multi-path staging: try all matching-length paths per
   pair (as the trial does) instead of first-valid. Fixes A2/A2b at
   quadratic cost; pairs with A3-compute.
5. Enforce the sum exclusion in code, or extend staging to the sum
   family. One-line or one-family fix for A6's first half.

## Red-team limitations (honest)

- A1's MAP and A6's tag-8 enabler are researcher-constructed; the
  current trial cannot promote a step-counter chain on its own. The
  attacks target the proxy's principle, with live-learner scope
  stated per attack.
- A4c's deletion used the driver's ablation hook; production
  deletion would come through eviction, but the recycling mechanics
  (first-fit `alloc_node`, surviving edges) are the base's own.
- A5's first reverse design was solved by rebind, not the adapter;
  the reported numbers are from the redesigned len-5 run.
- Worlds are small (~600 nodes); nothing here tests scaling beyond
  the H-XIO-1 regime.
- Masked `xio_try` was verified only by direct call and code
  inspection (returns -2 before any pairing).

## Standing metrics

- New code: `rt_driver.zag` (~470 lines), all unfrozen driver-level;
  frozen base + xio_core byte-untouched (assembly by line cut).
- Modes / bridges / handlers / new core semantic cases: 0 / 0 / 0 / 0.
- Capability-source delta of the attacks: zero new capabilities;
  all findings are about the adapter mechanism's trust envelope.
- Determinism: 3/3 byte-identical runs.

## Deliverables (all in xio_redteam/)

- NAMECHECK.md (toolchain guard Step 0, scope, Zag notes)
- REPORT.md (this file)
- rt_driver.zag (red-team driver, unfrozen, new)
- rt_full.zag (assembly: frozen base + xio_core + red-team driver)
- rt_bin (pinned znc build), rt_compile.txt (warnings only)
- rt_run1.txt, rt_run2.txt, rt_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes, paper untouched,
frozen files untouched, committed locally with explicit pathspecs,
nothing pushed.
