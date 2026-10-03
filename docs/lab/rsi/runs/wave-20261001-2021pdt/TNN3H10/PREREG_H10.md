# PREREG_H10: one learner-owned structural workspace

Lane: TNN3H10, wave wave-20261001-2021pdt. Worker: subagent (depth 2/2), writing only.
Status: **NOT-FROZEN. SUBSTRATE-ABSENT.** No kill bars are frozen. No implementation
is authorized by this document. This prereg records the mandatory substrate
verification against the frozen source and why it fails.

Frozen source: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
SHA-256 (verified by worker with sha256sum): a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
1591 lines. Cognition path: lines 1-1357 (test battery and remediation port below).

Hypothesis under test (from TNN3/HYPOTHESES.md, wave-20261001-1721pdt):
H10. One learner-owned structural workspace. All subsystem state (MAPs, guides,
UNCERT nodes, taught facts, standing records) lives in a single learner-addressable
workspace with one node and edge format; subsystem boundaries become learner-created
link types, not separate stores; selectors become generic graph queries over the
unified store. Net negative: per-format selectors and layout conventions deleted.
Capability-source delta claimed: zero added. Falsifiable prediction: sealed
interference worlds showing catastrophic interference (cross-type edge collisions
in the shared store) kill H10.

Prior finding this verification must confront: H3 (this wave, PREREG_H3.md)
found that MAPs (tag 20), cells (tags 101-104), and facts (tag 1) are "three
genuinely different structures with genuinely different field semantics, each read
by the code that created them," that "cells already use the generic allocator
(SUBSTRATE-ALREADY-UNIFIED)," and that the measured deletion set for H3 was
"empty (zero lines)" because "there is no code that treats one shared structure
two different ways and could be simplified by deleting a case."

CONTLEARN baseline (qualified): INTEGRATION-DEMONSTRATED, narrowed by red team to
"machinery integration in a persistent arena under per-query supervision, not
learner-owned integration." Measured on the fixed disclosed 149-event script:
REUSE_COUNT 30 (R1c 6, R2c 3, R3c 3, R4c 12, R5c 6), per-phase-reset control
identical within phases and 0/18 on the cross-phase probe, 3/3 byte-identical
determinism, 0 of 12 P1 facts lost under 2x unrelated load. Red-team bounds:
learner causal contribution zero (H2-v2 K-H2-3(a) on the byte-identical source);
R5c is fact retention, not procedure reuse (no promoted MAP ever executed at
query time; H2-v2 K-H2-4(b)); every accept decision matched a supplied answer
key (flags=0); K5a equality shows per-phase outcomes are history-insensitive.

## 1. Verification (a): per-format selectors and layout conventions

The store is already unified: one node table (noff, lines 50-52), one edge table
(eoff, lines 53-55), one allocator (alloc_node, lines 87-104, zero-fills all ten
fields), one raw field accessor (ng/ns). H10's "separate stores" do not exist.
What is per-format is the READER side: every subsystem reads its own layout.
Enumerated from the cognition path (lines 1-1357), with quotes:

Fact readers (tag 1; layout field20=s, field24=r, field28=o, field32=clock;
writer ev_teach, lines 297-309):
- activate, lines 140-152:
  `if(ng(W,n,36)==1 && ng(W,n,0)==1 && is_superseded(W,n)==0){`
  `  if(ng(W,n,20)==s && ng(W,n,24)==r){`
- t2_lu_first, lines 419-427: `if(ng(W,n,36)==1 && ng(W,n,0)==1 && ng(W,n,20)==s && ng(W,n,24)==r){return n;}`
- t2_chain (428-441), t2_gather (442-473), t2_gather_sum (474-484), t2_rels via
  inc_fill (545-556): all scan `ng(W,n,0)==1` with `ng(W,n,20)==s`,
  `ng(W,n,24)==r`, `ng(W,n,28)` as the value.
- bootstrap_miss (763-794), line 766: `if(ng(W,n,36)==1 && ng(W,n,0)==1 && ng(W,n,24)==r){`
- ev_query (813-835), line 822: recent-scan `if(ng(W,m,36)==1 && m>=2 && ng(W,m,0)==1){recent=m;}`

MAP readers (tag 20; layout field4=r, field8=s, field12=-1, field16=-1,
field20=graph root, field24=promo edge index, field28=answer; writer
promote_graph, lines 533-544: `ns(W,m,0,20); ns(W,m,4,r); ns(W,m,8,s);
ns(W,m,12,-1); ns(W,m,16,-1);` then `write_node(W,m,root,hg(W,24),ans,0);`
which sets field20=root, field24=promo edge count, field28=ans):
- revise_on_contradict (685-705), line 690: `if(ng(W,m,36)==1 && ng(W,m,0)==20){`
- t2_revise_graph (706-752): `let root:i32=ng(W,m,20); let s:i32=ng(W,m,8);
  let r:i32=ng(W,m,4);` and `let ans_old:i32=ng(W,m,28);`
- map_standing (568-577): generic edge scan, tag-agnostic.

Cell readers (tags 101-104; layout field4=operand slot or dest, field8=literal
node or source, field12=branch true-target, field16=branch fallthrough):
- execute (192-215), the single executor, reads per tag:
  `if(tag==101){ let d:i32=ng(W,cur,4); let sr:i32=ng(W,cur,8); ...`
  tag 102 reads `ng(W,cur,4)`, `ng(W,cur,8)`, `ng(W,cur,12)`, `ng(W,cur,16)`.
- t2_sig (511-532): walks SEQ plus BRANCHEQ true-targets, records (tag, literal
  field20) per cell.
- t2_revise_graph, lines 713/720: `if(ng(W,c,36)==1 && ng(W,c,0)==101){stale=c;}`
  and `if(ng(W,c2,36)==1 && ng(W,c2,0)==102 && ng(W,c2,12)==stale){g=c2;}`

UNCERT / guide / misc layouts (writers in miss_inquire, lines 795-812):
- UNCERT node (tag 30): `ns(W,u,0,30); ns(W,u,4,-4); write_node(W,u,s,r,2,0);`
  so field4=-4, field20=s, field24=r, field28=2. No cognition-path reader scans
  tag 30 by content; guides link to it.
- Guide node: disguised as a fact: `ns(W,g,0,1); ns(W,g,4,s);
  write_node(W,g,30,-999,0,0);` so tag 1, field4=s, field20=30 (action value),
  field24=-999 sentinel, field28=0. Read by ev_act (859-901):
  `let r0:i32=ng(W,cand,4);` used as the context-match key, and
  `let av:i32=ng(W,best,20);` returned as the action value.
- k-node: k_get (753-762), line 756: `if(ng(W,n,36)==1 && ng(W,n,0)==903){return ng(W,n,20);}`
- comb marker: comb_present (557-564), line 560: `if(ng(W,n,36)==1 && ng(W,n,0)==8){return n;}`
- Frame/literal convention: tag 902 nodes; fr_get/fr_set (166-178) walk field4
  chains; t2_lit (338-341) sets `ns(W,n,0,902); ns(W,n,20,v);`.

Already-generic (tag-agnostic) machinery, not per-format: alloc_node, alloc_raw,
write_node, link_edge, ng/ns/eg/es, evcount (229-236), bid (237-248),
is_superseded (132-139), is_prot (221-228), seq_nx (184-191), seq_link (318),
map_standing, contradict_map (578-585), evict_node (254-275), decay (153-165),
log_ev, ctx_push/ctx_get.

Deletable convention versus load-bearing field semantics (per H3's finding):
- Load-bearing, cannot be deleted without breaking function: the cell layouts
  read by execute (the 4-op ISA semantics live in field4/8/12/16); the fact
  (field20/24/28) keys read by the activate family; the MAP (field4/8/20/28)
  fields read by the revise path. These are three genuinely different structures,
  confirming H3. Deleting the readers deletes the capability.
- Mere convention: the guide disguised as tag 1 with the field24=-999 sentinel
  (a guide is not a fact; the sentinel is a layout hack); the 903 k-node tag;
  the 902 frame/literal tag; the tag-102 guide convention in the remediation
  port scaffolding (r_mk_guide, line 1373, tags guides 102, colliding with
  OP_BEQ=102, which shows tags are not a disciplined unified namespace).
  These conventions could be rewritten, but rewriting them is modified lines,
  not deletion, and none of them is a "selector" whose deletion yields generic
  queries.

## 2. Verification (b): "selectors become generic graph queries" at zero added lines: FAIL

No generic graph query mechanism exists in the frozen source. Exhaustive
inventory of candidates:
- evcount(W,n,t) counts edges into n of one type: tag-agnostic but a counter,
  not a content selector. It cannot find "the MAP for (s,r)" or "the guide for
  context c."
- bid(W,n) is a tag-agnostic scorer, not a query; candidate enumeration in
  activate and ev_act is format-specific.
- is_superseded / is_prot / seq_nx / map_standing are generic edge predicates,
  not structure selectors by content.
- ng(W,n,f) is a raw field read, not a query.
- No function takes a tag (or field list) as a parameter. Every content
  selector hardcodes its tag literal: `ng(W,n,0)==1` (facts), `==20` (MAPs),
  `==101/102` (cells), `==903`, `==8`. The grep enumeration in section 1 is
  complete for the cognition path.

A generic selector (e.g. select by parameterized tag and key fields) would be a
new function: added lines, not zero. Rewriting each existing selector to take
parameters is modified lines at every call site, and the key-field mapping
(which field holds the subject key for which type: field20 for facts, field8
for MAPs, field4 for guides, none for cells) must live somewhere: either a
per-type dispatch table (the deleted format-specificity reintroduced as data)
or a rewrite of all writers to one layout (modified lines across ev_teach,
ev_teach_in, promote_graph, t2_cell/t2_guard/t2_set/t2_mov/t2_inc,
miss_inquire, rec_evict, plus execute's readers). The cell ISA fields
(field4/8/12/16) cannot be folded into a fact-style (s,r,o) layout without
breaking execute, which reads them as operands. The zero-added-lines claim
fails. Honest minimal delta for (b) alone: a new parameterized selector
(estimate 12-18 added lines) plus writer/reader rewrites (dozens of modified
lines), and even then the ISA cell fields remain irreducibly format-specific.

## 3. Verification (c): "learner-addressable" workspace: FAIL, no learner-reachable path exists

Exhaustive search for an event path by which the learner (as opposed to
researcher code) can address any structure in the workspace:

1. The event interface (the only path into cognition) accepts scalar payloads
   only:
   - ev_teach(W,s,r,o), line 297; ev_teach_in(W,s,r,o), line 310
   - ev_query(W,s,r,expected,flags), line 813
   - ev_observe(W,s,r,o), line 836
   - ev_act(W), line 859: no arguments at all
   No event accepts a node index, tag, field offset, edge type, or structure
   handle. All addressing (node indices, structure selection) happens inside
   researcher-written machinery (activate, t2_lu_first, ev_act's edge scan).
   The learner addresses structures only by (subject, relation) content keys,
   never by identity, never across types.

2. ev_teach/ev_teach_in return the allocated node index to the caller, but the
   caller in the frozen binary is the test battery (main, line 1357, runs
   run_all); there is no learner entity in the loop at all. In driver-based
   experiments (CONTLEARN) the caller is researcher-authored driver code. No
   path delivers a structure handle to a learner.

3. The 4-op ISA cannot address the workspace generally: res_op (179-183)
   `if(op>=0){return ng(W,op,20);}` lets a cell read field20 of an
   immediate-indexed node, and fr_set writes only the frame chain via field4
   links. Cells cannot allocate, cannot link, cannot read edges, cannot write
   arbitrary node fields. And no path lets the learner author cells: all cells
   are assembled by researcher-written t2_asm_* (lines 363-410); H2/H3/H4/H6
   found no learner-reachable construction path, and the CONTLEARN red team
   confirmed "no learner-created value is in the causal chain" of any
   integration decision on this byte-identical source.

4. "Subsystem boundaries become learner-created link types" is inexpressible:
   link types are a fixed 13-value enum (lines 60-72: ET_DEP through ET_COR);
   no event creates a link type; link_edge's type argument is only ever passed
   constants from researcher code; the 4-op ISA has no LINK operation.

Conclusion: the workspace is researcher-addressable only. The learner cannot
address MAPs, guides, UNCERT nodes, taught facts, or standing records by any
event path, and no learner entity exists in the frozen build to do the
addressing. This matches H2/H3/H4/H6 (SUBSTRATE-ABSENT, no learner-reachable
construction/update paths) and the CONTLEARN red-team finding. Verification (c)
fails exhaustively.

## 4. Verification (d): deletion set measurement

Per-format selector/reader code in the cognition path (body lines, inclusive
ranges from the function table):

| Function | Lines | Body lines | Format read |
|----------|-------|-----------|-------------|
| activate | 140-152 | 13 | tag 1, f20/f24 |
| t2_lu_first | 419-427 | 9 | tag 1, f20/f24 |
| t2_chain | 428-441 | 14 | tag 1, f20/f28 |
| t2_gather | 442-473 | 32 | tag 1, f20/f24/f28 |
| t2_gather_sum | 474-484 | 11 | tag 1, f20/f24/f28 |
| t2_rels | 485-496 | 12 | tag 1 via inc_fill |
| inc_fill | 545-556 | 12 | tag 1, f20/f24 |
| comb_present | 557-564 | 8 | tag 8 |
| k_get | 753-762 | 10 | tag 903 |
| bootstrap_miss | 763-794 | 32 | tag 1 scan, f24/f28 |
| ev_query | 813-835 | 23 | tag 1 recent-scan |
| ev_act | 859-901 | 43 | edge scan + guide layout f4/f20 |
| revise_on_contradict | 685-705 | 21 | tag 20 scan |
| t2_revise_graph | 706-752 | 47 | tag 20 f4/f8/f20/f28 + cells |
| t2_sig | 511-532 | 22 | cells 101-104 |
| execute | 192-215 | 24 | cells 101-104 (ISA) |
| fr_get/fr_set/res_op | 166-183 | 18 | frame/cell fields |
| t2_exec | 412-418 | 7 | frame setup |
| ev_teach | 297-309 | 13 | tag 1 writer + prev scan |

Measured total of format-specific selector/reader/writer code: about 371 body
lines. Per H3's finding and section 1 above, this set is load-bearing: each
reader reads the structure its writer created, with genuinely different field
semantics. The H10 "deletion set" (per-format selectors deleted with zero
added lines because generic queries take over) is therefore not a real set:
deleting these readers without a replacement breaks activate, execute, the
trial loop, revision, and act selection. The coherent deletion set under H10's
own mechanism is empty, the same result H3 measured.

## 5. Verdict: SUBSTRATE-ABSENT (fifth consecutive)

(b) requires additions (no generic query mechanism exists; zero-delta claim
false) and (c) finds no learner-addressability (no event path; no learner
entity; fixed link-type enum; ISA without alloc/link/edge ops). The H10
substrate change presupposes a learner-addressable unified workspace and
existing generic queries; neither exists in the frozen source. The store is
already unified (one allocator, one node table, one edge table), which is
necessary but not sufficient: unification of the store is not unification of
addressability, and H10's mechanism is about addressability.

This prereg is NOT-FROZEN. No kill bars are frozen, no implementation is
authorized, no sealed worlds are commissioned. This matches the H2/H3/H4/H6
pattern: the frozen TNN-2 core has no learner-reachable construction or update
paths, and H10's hypothesis text assumes them.

## 6. Draft kill bars (NOT FROZEN; for a future re-attempt only)

If a later substrate ever passes (a)-(d), the intended bars, with the
CONTLEARN qualified baseline as the explicit target to beat:

- Baseline to beat (CONTLEARN, qualified): REUSE_COUNT 30 on the disclosed
  149-event script with answer keys on every query, learner causal
  contribution zero, R5c = fact retention only, no MAP ever executed at query
  time, per-phase-reset control identical within phases.
- Required deltas: (1) learner-causal contribution above zero: at least one
  integration decision (promotion accept, guide selection, revision trigger)
  whose white-box causal trace includes a learner-created structure value in
  the decision chain (currently zero per H2-v2 K-H2-3(a)); (2) genuine
  procedure reuse: a promoted MAP root executed at query time through the
  trial/execute path (currently zero per H2-v2 K-H2-4(b)); R5c must be
  redefined as MAP-execution reuse, not exact-hit fact reads; (3) masked
  evaluation (expected=-2, flags=1) cross-phase citation count strictly above
  the masked baseline, removing the answer-key condition; (4) sealed
  interference worlds (adversary-designed post-freeze, materially different
  from FW1-FW9 and from the CONTLEARN script): zero cross-type edge
  collisions in the shared store and no eviction/corruption of previously
  learned procedures by new vocabulary learning; catastrophic interference
  kills H10 per its falsifiable prediction; (5) determinism preserved (3/3
  byte-identical); (6) capability-source delta at or below zero with no new
  modes, bridges, routers, handlers, or semantic cases; (7) process bars:
  prereg committed alone before implementation, pure Zag, frozen ISA hash
  re-verified.
- Three-valued verdict: CONFIRMED (all bars pass on sealed worlds) /
  KILLED (catastrophic interference observed, or any required delta at zero)
  / VOID (prereg violated; correction only as fresh prereg plus fresh sealed
  worlds).

## 7. Re-verification conditions

A future H10 attempt must re-run (a)-(d) against the then-frozen source and
show: a parameterized content selector that already exists (quote it); an
event path by which learner-originated input addresses an arbitrary structure
by identity or type (quote the signature and the addressing step); and a
nonempty deletion set of per-format selectors whose removal does not break
their readers. Until then, H10 stays SUBSTRATE-ABSENT.
