# COUNTMAP-ADDRESSABILITY: the formation/addressability split (2026-10-03)

Worker: COUNTMAP-ADDRESSABILITY. Non-ledger task (claim minting paused).
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/countmap_addressability/
Method: analytical. Builds on the frozen XP-COUNTMAP-1 PASS result
(lane xp_countmap1, verdict XP-COUNTMAP-1-PASS, 8/8 checks, 3/3
byte-identical runs) and on read-only source analysis of the same
frozen build block (countmap1_block.zag, SHA256
56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004).
No experiment built, no code run, no frozen source modified, the
singleton lookup NOT changed (COUNTMAP-2 stays on hold per
constraints). No prereg was needed because nothing was
implemented; Section 9 separates tested claims from reasoned ones.

## 0. The banked statement this report starts from

XP-COUNTMAP-1 froze four claims as experimental results (Facts A-C
tested, Fact D untested):

* The base trial machinery (`t2_asm_count`, `t2_try_verify`,
  `promote_graph`) generalizes to N count structures unmodified.
* Only the composition-layer lookup is singleton: `xs5_find_countmap`
  (lowest live id wins, no relation parameter) and `xs5_agg_rel`
  (the world's single aggregation relation, derived from the
  singleton's type-1 provenance).
* A second count MAP CAN form via the trial path (MAP_V2 over rel
  85 formed and answered through trial); it cannot be ADDRESSED via
  composition (direct `xs5_compose` returned -2 before and after
  formation).

This report answers the four follow-up questions from the parent:
what addressability means here, whether the singleton is
fundamental, what would trigger COUNTMAP-2, and where else the
same split appears.

## 1. What "addressability" means here

Addressability is the composition layer's problem of *naming* a
stored structure so it can be reused. The composition layer works
in node ids; to compose with a learned structure it must resolve
"which structure" to a node id, and it must do so in a way that
picks the right one for the query at hand.

In the frozen block there are two completely different addressing
regimes, side by side:

(a) Formation addressing (trial layer). `t2_trial`'s count path
iterates the query subject's relations (`t2_rels`), builds a
maximal chain per relation (`t2_chain`), assembles a count graph
(`t2_asm_count`), verifies against expected (`t2_try_verify`), and
promotes (`promote_graph`) with type-1 provenance edges to the
licensing facts. The address is fully specified at formation time:
(subject, relation, expected). `promote_graph` mints a fresh
tag-20 MAP per verified trial with no dedup check, so formation
is unbounded and relation-indexed per attempt. The learner state
retains, per count MAP, which relation it counts: readable from
the type-1 provenance edges, learner-derived, never hardcoded.

(b) Composition addressing (xs5 layer). `xs5_find_countmap` scans
node ids 2..1023 and returns the FIRST live tag-20 MAP whose
field-20 graph contains an INC cell. No relation parameter, no
subject parameter, no query-context parameter, no composite
parameter. `xs5_agg_rel` then reads the aggregation relation off
that one MAP. The address is world-global and query-blind: one
ambient r_agg for every composition in the world lifetime.

The split is therefore precise: formation resolves structures by
(subjct, relation); composition resolves them by (first live id).
The composition layer throws away the relation index that the
formation layer already wrote into learner state.

One refinement beyond the banked statement, from source reading.
`xs5_agg_exec` never executes the stored count MAP's INC graph.
It walks a fresh chain over r_agg (`t2_chain`), assembles a count
graph ephemerally (`t2_asm_count`), and executes that
(`t2_try_verify`). The stored MAP serves as a capability token
(the hard gate `if(xs5_find_countmap(W)<0){return -2;}`), a
provenance carrier (r_agg source), and a LINK14 target, but never
as an executed procedure. So "addressing the count MAP" in this
build really means "reading which relation is licensed for
counting", not "retrieving a procedure to run". The split is
sharper than formation-vs-use: even the execution path does not
touch the stored structure, only the license.

## 2. The addressing census: every structure type in the frozen block

| Structure type | Formation | Composition addressing | Split? |
|---|---|---|---|
| Count MAPs (xs5 path) | unbounded, per-relation via trial | singleton, lowest live id, query-blind | YES (banked) |
| Nav MAPs (xs5_compose) | unbounded via trial chain path | set enumeration, all nav-ok MAPs in id order (`xs5_is_navmap` via `cc_relseq`) | no |
| MAP_Z composites (xhier_compose) | unbounded via promote (xs5_try_nav_agg, compose_try, xhier_try_pair) | set enumeration, all MAP_Zs up to 16 (`xhier_is_mapz`) | no, on the composite itself |
| MAP_Z's own count MAP at execution | recorded per composite via LINK14 at compose time | IGNORED: `xhier_exec` resolves its own type-14 count MAP (`xhier_mapz_agg`), checks it exists, then executes the global `xs5_agg_rel` singleton anyway | YES, latent (new, Section 5) |
| Sum structures | formed via `t2_asm_sum` + `promote_graph` on trial verify | none: no find-sum, no sum-exec exists in the composition layer | YES, stronger: zero addressable (new, Section 5) |
| Count MAPs as unified-DFS segments (compose_try/un_dfs) | same as count MAP formation | set enumeration via `un_satisfy`; `cc_satisfy` rejects INC graphs but `cx_contract` (plen path length) could admit one | latent type mismatch (new, Section 5) |
| Facts (`t2_lu_first`) | taught | first-live per (subject, relation): fully parameterized address | no |
| tag-903 node (`k_get`) | get-or-create singleton | get-or-create singleton | no: formation and addressing unified by design (counter-example) |
| Any MAP via rebind_try | rebind does not form | full enumeration, co-use-ordered | no |

The census shows the singleton is the exception, not the rule.
The same codebase already addresses nav MAPs, composites, and
unified-DFS segments as sets; it addresses facts by a fully
parameterized key; and it has one legitimate singleton (`k_get`)
where formation and addressing are unified by construction. The
count MAP is the one structure type whose formation layer makes
many and whose composition layer sees one.

## 3. Fundamental limitation or convenience?

Convenience: a composition-layer design choice, not a
protected-core invariant. The evidence, all code-determined:

* The xs5 patch header reads "Pure Zag. Unfrozen only." The lookup
  lives in experiment-layer code, not in the protected ISA.
* The protected machinery (`t2_asm_count`, `t2_try_verify`,
  `promote_graph`, the ISA ops) mints, verifies, and executes
  multiple count structures with no change needed. Formation and
  execution already generalize; only the lookup is singleton.
* The index key already exists in learner state. `xs5_agg_rel`
  derives r_agg per MAP from type-1 provenance edges. An indexed
  lookup needs no new node types, edge types, or opcodes; it reads
  the relation the formation layer already recorded.
* "Lowest live node id wins" is an implementation accident, not a
  learned property. It cannot survive the 2026-10-03 architectural
  clarification: structures are described by learned properties
  (consumes, produces, constraints, provenance, learned
  applicability), and composition must select by those properties.
  Selecting by allocation order is the opposite of that direction.
  COUNTMAP-2, as specified, is selection by a learned property
  (provenance relation), which is aligned with domain-blindness,
  not in tension with it.

What it would take to make count MAPs addressable (the concrete
COUNTMAP-2 change list, for when it is triggered):

1. Parameterize the lookup: `find_countmap(W, r_wanted)` scans
   live INC-ok tag-20 MAPs and returns the one whose
   provenance-derived relation equals r_wanted (lowest id as
   tiebreak only).
2. Thread the parameter through execution: `xs5_agg_exec` takes
   the wanted relation (or count MAP id) instead of calling the
   global `xs5_agg_rel`; `xs5_compose` tries (NAV, AGG) pairs over
   pairs of structures, not over one ambient r_agg.
3. Keep per-composite addressing honest: at promote time the
   composite already LINK14s its count MAP; under indexed lookup
   it must link the count MAP it actually used.
4. Honor the carried address at execution: `xhier_exec` must use
   the MAP_Z's own type-14 count MAP's provenance relation,
   not the global singleton (fixes the Section 5 latent issue).
5. Make formation fall-through deliberate: today compose fails and
   trial happens to try; an indexed design must request formation
   per wanted relation when the wanted count MAP does not exist
   yet, rather than relying on accidental fall-through.
6. Kill-bar hygiene: the frozen DAGFAN bars that assume the
   singleton (e.g. single shared count MAP node) stay valid for
   single-relation worlds; the indexed design needs its own
   prereg and its own regression bar that the singleton worlds
   still pass verbatim.

None of this touches the protected core. The change is confined
to the unfrozen composition patches.

## 4. What would trigger COUNTMAP-2

Held until a lane genuinely needs two aggregation relations
*used through composition*, not merely formed. The forcing
condition is precise. Consider a query (s, r_new, expected) where:

* a nav MAP walks from s to an endpoint e (the nav leg exists, so
  composition has work the trial layer cannot do alone), and
* the aggregation leg must run over a relation that is not the
  first-learned r_agg, and
* no single-relation trial path from s verifies (so the trial
  layer cannot form-and-answer directly, as it did in
  XP-COUNTMAP-1 B2).

In the current build both layers fail such a query: the trial
layer cannot compose, and composition addresses the wrong count
MAP (r_agg fixed at first learning, verify fails or answers
wrong). That world is the trigger. Note the B2 escape hatch that
kept XP-COUNTMAP-1 from needing it: B2's answer was directly
countable from the subject over one relation, so trial saved it.
The trigger world closes that hatch by requiring the nav leg.

Softer but legitimate triggers:

* Any lane in the current top-priority directions (general
  DAG/fan-out/fan-in composition, L2 adaptive reuse across
  heterogeneous structures, heterogeneous composition with
  partial mismatch) that needs two aggregation relations inside
  one answer, e.g. a fan-out query counting over two relations,
  or a diamond whose branches aggregate over different relations.
* A lane implementing learned-property addressing for structure
  types in general; the count case falls out as one instance, and
  doing it generally is preferable to a count-only patch.

Not triggers: speculative generality ("some future world might
need two relations"); rerunning the XP-COUNTMAP-1 world; the
DAGFAN regression worlds, which assume the singleton and must
keep passing verbatim under any future design.

## 5. Other places with the same formation/addressability split

Three further instances found in this analysis (source-read,
not executed):

(a) `xhier_exec` discards the MAP_Z's own count MAP address.
`xhier_mapz_agg` resolves the composite's own type-14 count MAP
(the address formation recorded at compose time), uses it only
as an existence gate (`if(a<0){return -2;}`), then calls
`xs5_agg_exec(W,e,r_agg)` with `r_agg=xs5_agg_rel(W)`, the global
singleton. Formation records a per-composite address;
execution dereferences the ambient singleton instead of the
carried address. This is the same split one layer up, and it is
a latent correctness issue, not just a generality limit: if
MAP_Y were ever tombstoned while a second count MAP stayed
live, every MAP_Z would silently aggregate over the wrong
relation while its own LINK14 edges name the right one. Any
future MAP_Z work should fix this regardless of COUNTMAP-2.

(b) Sum structures form but are unaddressable. `t2_trial`'s sum
path forms sum graphs (`t2_asm_sum`) and promotes them as MAPs
with no dedup, gated on `comb_present(W)>=0` (existence of a
tag-8 node). The composition layer has no sum lookup and no
sum executor at all: no `xs5_find_summap`, no `xs5_sum_exec`,
no sum leg in `xs5_compose` or `xhier_compose`. Sums are the
stronger version of the split: formation unbounded, composition
addressing zero. If a future lane needs sum composition, it
faces the same design decision from a standing start.

(c) The unified composition can name a count MAP but not execute
it as a count. `un_candidates` enumerates all live tag-20 MAPs
(set-based addressing, no singleton). `un_satisfy` first tries
`cc_satisfy`, which rejects INC-cell graphs (`cc_relseq`
returns -1 on the 102/101 alternation breaking at tag 103), then
falls back to `cx_contract`, the plen path-length contract,
which a count MAP could satisfy via a real path. If admitted as
a segment, `compose_try` reassembles every segment with
`t2_asm_chain`, a chain assembler, and verifies the
concatenation. A count MAP admitted this way would be
re-executed as a chain: addressable but type-mismatched.
Formation makes a count structure; the unified addressing can
see it; the unified execution cannot run it as what it is.
This is a formation/addressability/execution-type three-way
split, latent until a count MAP actually passes the plen
fallback in a live world.

And one counter-example that sharpens the pattern: `k_get` is a
legitimate singleton because formation and addressing are
unified by construction (get-or-create: at most one is ever
made). The count MAP lookup is get-only over a formation layer
that makes many. The design rule this suggests: a singleton
lookup is honest only when formation is singleton too; when
formation is many, addressing must be many (set-based or
parameterized).

## 6. Consequences for the banked facts

* Facts A-C (frozen by XP-COUNTMAP-1) stand unchanged; this
  report adds mechanism detail but no new experimental claims.
* Fact D (adaptation cannot create count structures) stands
  untested, as before. Note it now has a second facet: the
  adaptation layer (`xs5_truncate`/`xs5_reroute`) enumerates nav
  MAPs as a set, so even if it could touch count structures, it
  would address them correctly; the blindness is in what it can
  structurally operate on (relseqs only), not in how it looks
  them up.
* The Fact C self-reinforcement (pipeline order starves
  alternative formation) interacts with the Section 5(a) issue:
  the first-learned relation wins permanently at composition,
  and MAP_Z execution hardens that win into every composite's
  runtime behavior even where the composite's own provenance
  names a different count MAP.

## 7. Recommendations for the parent

1. Keep COUNTMAP-2 on hold. No current lane meets the Section 4
   trigger. Do not change the singleton lookup.
2. Fix or fence the Section 5(a) latent issue when MAP_Z work
   next runs: `xhier_exec` should use the composite's own
   type-14 count MAP's provenance relation. This is a
   correctness fix inside the frozen-world assumptions, not a
   generality expansion, and it is independent of COUNTMAP-2.
3. Treat sum structures (Section 5(b)) as the next unaddressed
   formation type to watch: if any lane starts promoting sums,
   it will hit the zero-addressing wall immediately.
4. Adopt the formation/addressability split as standing
   architecture vocabulary. Every new structure type the
   program introduces should answer two questions at design
   time: how is it formed (many or one, indexed by what), and
   how is it addressed (set, parameterized, singleton). The
   honest configurations are many/many, one/one (`k_get`),
   many/parameterized; the dishonest one is many/singleton,
   which is what the count MAP currently is.
5. When COUNTMAP-2 is eventually triggered, prefer the general
   version: learned-property addressing for structure types,
   with the count provenance relation as one instance, over a
   count-only patch. That is the 2026-10-03 clarification
   applied to addressing.

## 8. What was tested vs what was reasoned

Tested (frozen, by XP-COUNTMAP-1, PASS 8/8, 3/3 byte-identical):
the two-relation world forms MAP_V2 via trial and the
composition layer still returns -2 for it (K1-K4); the singleton
lookup returns MAP_Y and r_agg stays 82 (K2, K3); the phase-B
trace pins the answer 4 to the trial layer (K4).

Tested (frozen, by XP-DAGFAN-4, 22/22): the singleton's
observable consequences in a single-relation world (shared
MAP_Y, MAP_Z provenance shape).

Reasoned (this report, read-only source analysis of the frozen
block, no new runs): the token-not-executed refinement of
addressability (Section 1); the addressing census and the
claim that the singleton is the exception among set-based
regimes (Section 2); the fundamental-vs-convenience verdict
and the COUNTMAP-2 change list (Section 3); the precise
trigger condition (Section 4); the three further split
instances 5(a)-5(c) and the k_get counter-example (Section
5); the Fact D second facet and Fact C interaction (Section
6); the recommendations (Section 7). All line references are
to countmap1_block.zag as frozen.

## 9. Notes for the parent

* No ledger entry: non-ledger task, nothing minted.
* No commits to any lane branch; this report is the only new
  file, to be committed on tnn-native-lab only, explicit
  pathspec, never pushed.
* No build was performed (analysis only), so no safebin
  activation was needed; nothing was implemented, so no prereg
  was required. If any follow-up builds on this analysis, the
  prereg and pure-Zag rules apply as usual.
* The singleton lookup was not changed. COUNTMAP-2 stays on
  hold. The Section 5(a) xhier_exec issue is reported, not
  fixed, per constraints.
* Style: no em/en dashes in this file (hyphens only), opaque
  identifiers throughout, no domain labels.
