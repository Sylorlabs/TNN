# SUM-ADDRESSABILITY: the zero-addressing formation type (2026-10-03)

Worker: SUM-ADDRESSABILITY. Non-ledger task (claim minting paused).
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/sum_addressability/
Method: analytical. Builds on the COUNTMAP-ADDRESSABILITY REPORT.md
(lane countmap_addressability) and on read-only source analysis of
the same frozen build block (countmap1_block.zag, SHA256
56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004)
plus the XHIER-COUNTMAP-FIX block (xf_block.zag, verdict
XHIER-COUNTMAP-FIX-PASS). No experiment built, no code run, no
frozen source modified, the singleton lookup NOT changed
(COUNTMAP-2 stays on hold per constraints). No prereg was needed
because nothing was implemented; Section 7 separates tested claims
from reasoned ones.

## 0. The banked statement this report starts from

COUNTMAP-ADDRESSABILITY finding (b): "sum structures form via
`t2_asm_sum` + promote but have *zero* composition addressing (no
sum lookup/executor exists)", with the recommendation to "watch sum
structures as the next unaddressed formation type."

This report answers the four follow-up questions from the parent:
the full formation/addressability map for sums, whether the zero
is truly zero (and what "zero" hides), the concrete change list for
making sums addressable, and whether any third formation type is
unaddressed.

## 1. Sum formation: the full map

Formation is the trial layer's sum phase inside `t2_trial` (frozen
block, sum branch). Read from source, step by step:

* Gate: `comb_present(W)>=0`, i.e. at least one live tag-8 node
  exists. The gate is a world condition, not a query condition:
  once any tag-8 node is live, every subsequent miss runs the sum
  phase.
* Gather: `t2_gather_sum` collects up to 12 of the subject s's
  direct (non -999) facts: their values into `vals`, their fact
  ids into `sf` (the licensing facts).
* Search: subsets enumerated by decreasing size (`sz` from m down
  to 1), bitmask from `(1<<m)-1` downward, `popcnt` filter per
  size. Largest subsets tried first.
* Assemble: `t2_asm_sum` totals the subset values and declines
  (returns -1) when the total is <= 0 or > 900 (the execute
  budget). Otherwise it builds an unrolled chain of exactly
  `total` INC (tag 103) cells on frame slot 0, linked by SEQ
  edges. No guards, no sets, no literals, no per-cell provenance
  edges. It is the degenerate assembler: a pure INC run whose
  length IS the value.
* Verify: `t2_try_verify(W,root,0,expected,masked,st)` with s0=0
  (frame slot0 = 0 is the sum convention); `execute()` runs the
  INC chain; `res_op` reads slot 0, which now holds the total.
* Promote: `promote_graph(W,root,s,r,v2,ff,c)`: a tag-20 MAP with
  field4 = r (the QUERY relation), field8 = s (query subject),
  field20 = graph root, field28 = answer; type-1 DEP edges to the
  c licensing facts; `ev_teach_in(W,s,r,ans)` teaches the answer
  as a fact. No dedup check: every verified trial mints a fresh
  MAP, so formation is unbounded per subset.

The formation address is fully specified at formation time as
(subject s, subset of s's direct facts). The index keys already
exist in learner state and are learner-derived, never hardcoded:
the MAP node itself carries field8 = s and field4 = r, and the
type-1 provenance edges name the licensing facts (each carrying
its own relation in field24 and value in field28).

One tested-adjacent note: the frozen XP-COUNTMAP-1 driver never
opened the sum gate (it teaches only tag-1 facts, never a tag-8
node), so no sum MAP formed in that run. But the frozen block's
own self-test `t_p2` constructs a tag-8 node and queries
(110,41) with expected 60 over facts (110,31,10), (110,32,20),
(110,33,30); on the source path the sum phase is the only phase
that can verify 60, so `t_p2`'s `== 60` assertion is source-level
evidence that the sum path forms and promotes correctly in this
exact frozen block. The self-test was read, not executed; see
Section 7.

## 2. Sum addressing: the zero is truly zero

Exhaustive scan of the frozen block for anything that names or
runs a sum structure outside the formation path. Result: nothing.

* xs5 layer: no `xs5_find_summap`, no `xs5_sum_exec`, no sum leg
  anywhere. `xs5_compose` tries exactly (NAV,AGG) and the
  symmetric (AGG,NAV). `xs5_agg_exec` reassembles count graphs
  ephemerally; it never touches a sum graph.
* xhier layer: `xhier_compose` tries (NAV,MAP_Z) only. No sum leg.
* Unified composition: `cc_relseq` requires the 102/101 guard/set
  alternation starting at a 102 cell; a sum graph's first cell is
  103, so `cc_relseq` returns -1 and `cc_satisfy` fails. The
  fallback `cx_contract` calls `rb_chain_plen`, which requires
  the same alternation, so it also returns -1 and `un_satisfy`
  fails. `un_candidates` can therefore never admit a sum MAP as
  a segment.
* Rebind: `pc_try_one` requires `rb_chain_plen >= 2`; sum MAPs
  are skipped before any path matching.
* Adaptation: `xs5_select` (driving `xs5_truncate` /
  `xs5_reroute`) gates candidates on `cc_relseq`; sum MAPs are
  excluded.
* Revision: `t2_revise_graph` walks type-1 edges of tag-20 MAPs
  to find stale licensing facts; it can structurally touch a sum
  MAP's provenance like any MAP's, but it forms no address and
  promotes nothing.

The banked claim is confirmed and sharpened: there is no sum
lookup, no sum executor, and no code path in any of the five
composition-adjacent layers (xs5, xhier, unified, rebind,
adaptation) that can even name a sum MAP as what it is.

## 3. The stronger finding: sums are misaddressable, not just unaddressable

New in this analysis, and worse than the banked "zero". The
count-MAP detectors in the frozen block cannot distinguish a sum
graph from a count graph:

* `xs5_has_inc` walks the field-20 graph and returns 1 on ANY
  tag-103 INC cell. A sum graph is a pure INC chain, so its
  first cell already matches.
* Therefore a live sum MAP is returned by `xs5_find_countmap`
  (first live id in 2..1023), passes `xhier_agg_ok` (which uses
  the same predicate), satisfies the `xs5_agg_exec` capability
  gate (`if(xs5_find_countmap(W)<0){return -2;}`), gets
  LINK14-attached as a composite's count MAP inside
  `xs5_try_nav_agg` (`link_edge(W,zm,14,cm,0)` where cm may be a
  sum MAP), and is counted as a "count MAP" by the driver's own
  census `cm1_scan_countmaps` (which uses the same predicate).
* `xs5_agg_rel` would then read the "aggregation relation" off
  the sum MAP's first type-1 provenance fact (in the `t_p2`
  world: one of 31, 32, 33, the licensing facts' relations), and
  `xs5_agg_exec` would aggregate over that relation. In a world
  with one sum MAP and one count MAP, lowest live id decides
  which structure the entire composition layer believes is "the
  count MAP".

This persists after XHIER-COUNTMAP-FIX (PASS): `xhier_exec` now
uses the composite's own count MAP's provenance relation
(`xhier_mapz_rel`), which fixes the carried-address issue for
genuine count MAPs, but `xhier_agg_ok` still uses `xs5_has_inc`,
so a sum MAP still passes as the agg leg and `xhier_mapz_rel`
reads a relation off its licensing facts.

Consequence: once the sum gate opens (a tag-8 node present, as
in the block's own `t_p2`), the sum path does not merely create
an unaddressable structure; it creates a structure that actively
corrupts the existing singleton count lookup. The split is worse
than banked: the singleton is not even type-honest. This is a
latent correctness issue in every build carrying the has-INC
predicate, independent of COUNTMAP-2 and SUM-1.

## 4. What would it take to make sum structures addressable (SUM-1)

All changes are confined to unfrozen experiment-layer patches;
none touch the protected ISA (the assemblers, the single
executor, and promote already generalize). Order matters: item 1
is a correctness fix independent of the rest.

1. Type-honest detectors. Replace the has-INC predicate with two
   structural detectors derived from the graph itself, which is
   the learned-property-consistent direction (selection by
   structure, not by allocation order):
   * count detector: the graph contains at least one GUARD
     (102) cell AND at least one INC (103) cell.
   * sum detector: the graph contains at least one cell AND
     every cell is INC (103).
   Apply to `xs5_find_countmap`, `xhier_agg_ok`, and the driver
   census. This stops sum MAPs from shadowing count MAPs and is
   needed even if SUM-1 never ships. It changes no frozen
   verdict: in every frozen world no sum MAP is live, and every
   graph the old has-INC predicate matched still matches the
   count detector (count graphs always carry guards; chain
   graphs carry no INC cells; MAP_Zs carry root -1).
2. Parameterized sum lookup: `find_summap(W, s_wanted,
   r_wanted)`: scan live tag-20 MAPs; match the sum detector AND
   field8 == s_wanted AND field4 == r_wanted; lowest id as
   tiebreak only. No new node types, edge types, or opcodes: the
   (s, r) key is already on the MAP node, written by
   `promote_graph` at formation time.
3. Sum executor: `sum_exec(W, m)`: execute the STORED graph via
   the single executor (`t2_exec` with root = ng(W,m,20),
   s0 = 0). Deliberate design choice: unlike `xs5_agg_exec`,
   which reassembles ephemerally and treats the stored MAP as a
   license token (the COUNTMAP-ADDRESSABILITY Section 1
   refinement), the sum executor runs the stored structure as a
   procedure. That makes the MAP addressable as what it is, and
   turns the token-vs-executed distinction into an explicit
   experimental variable instead of an accident.
4. Composition legs: (NAV, SUM) in `xs5_compose`: a nav MAP walks
   s to endpoint e; `sum_exec` over `find_summap(W, e,
   r_wanted)`; verify against expected; promote the MAP_Z with
   LINK14 edges to the nav MAP and to the sum MAP. Symmetric
   (SUM, NAV) for ordered-pair completeness.
5. Deliberate formation fall-through: when `find_summap` finds
   nothing for (e, r_wanted), request trial formation for that
   subject rather than relying on accidental fall-through (the
   COUNTMAP-2 item-5 lesson). Design note: the current sum phase
   sums s's direct-fact values regardless of the query relation
   r; the wanted-relation plumbing needs an explicit decision,
   because the sum's natural key is the subject while field4 = r
   records the query relation at formation time.
6. Trigger (SUM-1 stays on hold until): a world with a tag-8
   node present, a nav MAP walking s to an endpoint e, where the
   answer is the sum of e's direct-fact values with expected
   supplied, and no direct trial path from s verifies, so the
   nav leg is required (closing the B2-style escape hatch where
   trial answers directly and composition is never needed).
7. Kill-bar hygiene: prereg BEFORE implementation; pure Zag;
   safebin; 3/3 byte-identical runs; a frozen regression bar
   that the singleton worlds (XP-COUNTMAP-1, XP-DAGFAN-4,
   XHIER-COUNTMAP-FIX) still pass verbatim with the new
   detectors in place.

## 5. Other formation types: the full census

Every tag-20 MAP formation site in the frozen block, with its
addressing regime:

| Formation site | Structure type | Formation | Composition addressing | Split? |
|---|---|---|---|---|
| t2_trial chain phase (t2_asm_chain) | chain MAP | unbounded, per path | set enumeration via relseq (xs5_is_navmap, un_candidates, rebind plen) | no |
| t2_trial count phase (t2_asm_count) | count MAP | unbounded, per relation | singleton, lowest live id, query-blind | YES (banked) |
| t2_trial sum phase (t2_asm_sum) | sum MAP | unbounded, per subset; gated on tag-8 | none; and misdetected as count (Section 3) | YES, stronger (this report) |
| xs5_try_nav_agg / xhier_try_pair / compose_try (promote_graph, root -1) | MAP_Z composite | unbounded via promote | set enumeration (xhier_is_mapz, up to 16) | no on the composite; per-composite agg address fixed by XHIER-COUNTMAP-FIX |
| pc_try_one rebind (promote_graph chain) | rebound chain MAP | per verified rebind | set enumeration, like chain | no |
| xs5_truncate / xs5_reroute (xs5_promote) | adapted chain MAP | per adaptation | set enumeration, like chain | no |
| ev_teach / ev_teach_in | tag-1 facts | taught | first-live per (s, r) via t2_lu_first: fully parameterized | no |
| k_get | tag-903 node | get-or-create singleton | get-or-create singleton | no: honest singleton (formation and addressing unified) |

There are exactly three graph assemblers in the frozen block
(`t2_asm_chain`, `t2_asm_count`, `t2_asm_sum`); no other
formation path mints executable graphs. Conclusion: sum is the
ONLY formation type with zero addressing. Beyond count and sum
there is no third unaddressed formation type in the frozen
block.

The census confirms the COUNTMAP-ADDRESSABILITY design rule:
the honest configurations are many/many, many/parameterized,
and one/one (`k_get`); the dishonest ones are many/singleton
(count) and many/zero-with-misdetection (sum).

## 6. Recommendations for the parent

1. Do NOT change the singleton lookup. COUNTMAP-2 stays on
   hold. SUM-1 stays on hold too: no current lane meets the
   Section 4 item-6 trigger.
2. Consider the item-1 detector fix (count detector requires a
   GUARD cell; sum detector is all-INC) as standalone
   correctness hardening the next time any lane touches the
   xs5/xhier composition patches. It is not a generality
   expansion; it makes the existing singleton type-honest, and
   it preserves every frozen verdict verbatim. Flagged, not
   implemented, per constraints.
3. Adopt the Section 5 census as the standing
   formation/addressability checklist: every new assembler
   answers three questions at design time: how formed (many or
   one, indexed by what), how addressed (set, parameterized,
   singleton), and what detector distinguishes its graphs from
   the other assemblers' graphs. The sum case proves the third
   question is load-bearing: two assemblers can share a node
   tag and a lookup predicate while making structurally
   different graphs.
4. If SUM-1 is ever triggered, prefer executing the stored sum
   graph (item 3) over the `xs5_agg_exec` reassembly pattern;
   the token-vs-procedure distinction is now an explicit
   experimental variable, not an accident.

## 7. What was tested vs what was reasoned

Tested (frozen, by XP-COUNTMAP-1, PASS 8/8, 3/3 byte-identical):
in the frozen driver world no sum MAP forms (the sum gate never
opens; `cm1_scan_countmaps` counts only count MAPs); the
singleton lookup returns MAP_Y and r_agg stays 82.

Tested (frozen, by XHIER-COUNTMAP-FIX, PASS): `xhier_exec` uses
the composite's own count MAP's provenance relation via
`xhier_mapz_rel`.

Reasoned (this report, read-only source analysis of the frozen
blocks, no new runs, no builds): the full sum formation map
(Section 1); the zero-addressing scan across all five
composition-adjacent layers (Section 2); the misaddressing
finding that sum MAPs satisfy `xs5_has_inc`, `xhier_agg_ok`,
and `cm1_scan_countmaps` and corrupt the singleton (Section 3);
the SUM-1 change list, trigger, and kill-bar hygiene (Section
4); the full formation census and the "no third unaddressed
type" conclusion (Section 5); the recommendations (Section 6).
The `t_p2` self-test path was read, not executed; its assertion
is cited as source-level evidence only. All line and function
references are to countmap1_block.zag as frozen (SHA256
56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004,
per COUNTMAP-ADDRESSABILITY), with the fix block xf_block.zag
checked for the Section 3 persistence claim.

## 8. Notes for the parent

* No ledger entry: non-ledger task, nothing minted.
* This report is the only new file, committed on tnn-native-lab
  with an explicit pathspec, local only, never pushed.
* No build was performed (analysis only), so no safebin
  activation was needed; nothing was implemented, so no prereg
  was required. If any follow-up builds on this analysis, the
  prereg and pure-Zag rules apply as usual.
* The singleton lookup was not changed. COUNTMAP-2 stays on
  hold. SUM-1 is proposed and held pending its trigger.
* Style: no em/en dashes in this file (hyphens only), opaque
  identifiers throughout.
