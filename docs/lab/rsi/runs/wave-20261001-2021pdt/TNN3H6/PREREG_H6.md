# PREREG H6: Standing-bearing uncertainty objects

Lane: TNN3H6, wave-20261001-2021pdt. Status: NOT FROZEN. Substrate verification FAILED (SUBSTRATE-ABSENT). No bars frozen. This document records the verification evidence so the failure is inspectable and no future worker re-freezes this hypothesis in its current form.

Hypothesis source: docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md, section H6, read verbatim by this worker (not cited from the task message).

H6 as hypothesized: merge the UNCERT node with the evidence model so uncertainty carries support counts the learner updates on every related experience; the researcher's fixed bid() formula (edge-type counts, about 12 lines) is deleted; a guide's bid becomes the learner-maintained standing of its UNCERT node, updated by generic CONFIRM/CONTRADICT events the learner links. Capability-source delta claimed: net negative, zero lines added.

Context: H1 was killed this wave by sealed evaluation (FABRICATION on dev evidence); H2/H3/H4 stopped at prereg by verification-first (all SUBSTRATE-ABSENT, same root cause: the frozen TNN-2 core has no learner-reachable construction path; H4 additionally found protected EXECUTE unreachable from ev_act). The mandatory process fix for H6: verify the substrate against the frozen build BEFORE freezing any bars. That verification is section 2 below.

Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash verified by this worker with sha256sum on 2026-10-01; matches the expected value character for character).

## Section 2: substrate verification (measured, quoted)

### (a) The fixed bid() formula: EXISTS, exactly 12 lines, and is the only bid computation. PASSES as hypothesized.

Quoted verbatim from the frozen source, lines 229-248:

```
fn evcount(W:[]u8,n:i32,t:i32)i32 {
  let c:i32=0; let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)!=-1 && eg(W,e,8)==n && eg(W,e,4)==t){c=c+1;}
    e=e+1;
  }
  return c;
}
fn bid(W:[]u8,n:i32)i32 {
  let c:i32=evcount(W,n,1)+evcount(W,n,2)+evcount(W,n,6)+evcount(W,n,7)-evcount(W,n,3);
  let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)!=-1 && eg(W,e,4)==10 && eg(W,e,8)==n){
      let g:i32=eg(W,e,0);
      c=c+evcount(W,g,1)+evcount(W,g,2)+evcount(W,g,6)+evcount(W,g,7)-evcount(W,g,3);
    }
    e=e+1;
  }
  return c;
}
```

`evcount` (lines 229-236) has exactly two callers, both inside `bid` (lines 238, 243). A repository-wide grep for `bid(` returns the definition plus eight call sites: four production (lines 145, 259, 872, 884) and four test-battery (lines 954, 986, 1206, 1211). No other bid computation exists anywhere in the 1591-line file. The hypothesis's "about 12 lines" is exact: `bid` is lines 237-248, twelve lines.

Important scope finding the hypothesis does not address: `bid()` is shared by THREE selectors, not just guide selection. Line 145 is `activate()` (query path: highest-bid fact matching subject and relation wins). Line 259 is `evict_node()` (retention: the LOWEST-bid live unprotected node is evicted). Lines 872 and 884 are `ev_act()` (guide selection: highest-bid guide linked to POLICY_ROOT wins). Deleting `bid()` therefore breaks query-path fact selection and retention eviction as well, and the hypothesis names no replacement for either.

### (b) A learner-reachable path for the LEARNER to update support counts on UNCERT nodes via CONFIRM/CONTRADICT events: DOES NOT EXIST. VERIFICATION FAILS. SUBSTRATE-ABSENT.

Exhaustive inventory, by claim component.

Claim component 1: UNCERT nodes exist and are learner-reachable. PARTIALLY TRUE, but creation is researcher-written. `miss_inquire` (lines 795-811) creates the UNCERT node (tag 30, line 797) and its guide on `ev_query`'s true-miss path:

```
fn miss_inquire(W:[]u8,s:i32,r:i32)void {
  let u:i32=alloc_node(W); if(u<0){return;}
  ns(W,u,0,30);
  ...
  link_edge(W,g,1,u,0);
  link_edge(W,pr,10,g,0);
  return;
}
```

The learner's only role is experiencing a query miss; the UNCERT node, the guide, the guide-to-uncertainty type-1 edge (line 809), and the POLICY_ROOT-to-guide type-10 edge (line 810) are all written by researcher code with fixed fields. Every other reference to tag 30 in the file is test scaffolding: lines 1047, 1182 (hand-built uncertainty nodes in tests) and line 1378 (`r_mk_uncert`, a test helper). The tag definition is line 85 (`fn T_UNCERT()i32 { return 30; }`).

Claim component 2: after creation, experience updates support counts on the UNCERT node. FALSE. After `miss_inquire` returns, NO code path in the file writes any edge to or from an UNCERT node, and no code path writes any field on an UNCERT node. The complete list of edge writers that could carry standing semantics, with targets:

- Line 538 (`promote_graph`): type-2 self-edge on a newly promoted MAP node (tag 20). Target: MAP, never UNCERT. Researcher-written at promotion.
- Line 781 (`bootstrap_miss`): type-2 self-edges on a new MAP node. Target: MAP. Researcher-written.
- Line 579 (`contradict_map`): type-3 self-edge on a MAP. Called ONLY from the test battery (lines 1159, 1209). Dormant on the cognition path, exactly as H9's hypothesis text notes.
- Line 744 (inside the revision path): type-3 self-edges on stale FACT nodes (tag 1) whose old answer was superseded. Target: fact nodes, never UNCERT. Researcher-written.
- Line 844 (`ev_observe`, contradiction branch): type-3 self-edge on the activated FACT node n. Target: fact node, never UNCERT. Fixed researcher rule.
- Line 897 (`ev_act`): type-6 self-edge on the SELECTED GUIDE (best). Target: the guide, never its UNCERT node. Fixed researcher rule, unconditional on selection.
- `ev_observe` match branch: type-7 self-edge on the fact node. `ev_query` hit branch: type-6 self-edge on the fact node. Both fixed researcher rules on fact nodes.

Claim component 3: generic CONFIRM/CONTRADICT events the learner links. FALSE on both halves. There are no CONFIRM/CONTRADICT events anywhere in the source: grep for `CONFIRM` and `CONTRADICT` (case-insensitive) returns only `contradict_map` (the dormant test-only function), `revise_on_contradict` (which the comments at lines 676 and 705 state explicitly does NOT demote standing and writes no CON edge to the MAP), and test comments. `log_ev` (lines 285-290) writes integer-kind rows to a log store (header 28); there is no reader of that store anywhere in the file (the only `ls(` uses are the writer itself and its accessor definition), so the log cannot feed standing even in principle. And there is no learner link affordance at all: the learner's entire interface is `ev_teach`/`ev_observe`/`ev_query`/`ev_act`, and every edge write inside those functions has a fixed type, fixed target pattern, and fixed trigger decided by researcher code. The learner cannot choose to write an edge of its choosing to a node of its choosing, so it cannot "link" any event to an UNCERT node.

Claim component 4: standing counts the learner maintains. FALSE. `map_standing` (lines 568-577) reads type-2 (+1) and type-3 (-1) edges on MAP nodes; as inventoried above, nothing on the cognition path writes those edges to a live MAP after creation (`contradict_map` is test-only), so even MAP standing is effectively static on the cognition path. For UNCERT nodes there is no standing field and no standing-counting reader at all; the node's fields are written once at creation (`write_node(W,u,s,r,2,0)`, line 799) and never touched again.

The closest existing instrument, `r_learn_confirm` (lines 1380-1382: `link_edge(W,ses,6,a,0); link_edge(W,ses,7,a,0)`), writes confirmation-shaped edges onto an uncertainty-like node, but it is test-battery scaffolding: all five callers (lines 1455, 1480, 1504, 1570, 1571) sit inside test functions. It is not reachable from `ev_observe`, `ev_query`, or `ev_act`. This is the same dev-harness pattern that killed H1: a test helper constructs the signature the test then verifies, while the cognition path has no such capability.

Consequence: the H6 substrate requirement "updated by generic CONFIRM/CONTRADICT events the learner links" names machinery that does not exist. The only standing updates anywhere are researcher-written fixed edge writes to fact, MAP, and guide nodes, and none of them target UNCERT nodes. This is the same root cause as H2/H3/H4 (no learner-reachable construction or update path), now confirmed on the uncertainty/standing axis.

### (c) Guide-selection machinery reading learner-maintained standing after bid() deletion: IMPOSSIBLE on this substrate. VERIFICATION FAILS.

The exact `bid` call sites in guide selection, quoted:

Line 872 (primary candidates in `ev_act`):
```
          let b:i32=bid(W,cand);
          if(b>bb){bb=b; best=cand;}
```

Line 884 (neighbor candidates in `ev_act`):
```
                let b2:i32=bid(W,c2);
                if(b2>bb){bb=b2; best=c2;}
```

Line 145 (`activate`, query-path fact selection):
```
        let b:i32=bid(W,n);
        if(b>bb){bb=b; best=n;}
```

What replaces them: nothing available. There is no learner-maintained standing field on guides or on UNCERT nodes to read, and no learner write path that could populate one (see (b)). Any replacement would be new researcher-written lookup code, which contradicts the hypothesis's net-negative, zero-added-lines claim. Structurally, `bid(W,cand)` in `ev_act` counts edges on the GUIDE (plus POLICY_ROOT's edges via type-10 neighbors); it never reads the UNCERT node's state. The only UNCERT contribution to a guide's bid is the fixed +1 from the type-1 guide-to-uncertainty edge written once at creation (line 809). "A guide's bid becomes the learner-maintained standing of its UNCERT node" would require a guide-to-UNCERT standing lookup that no code performs and no standing that any code maintains.

### (d) Measured deletion set (not estimated)

- Lines 229-236: `evcount` (8 lines). Sole callers are inside `bid`; orphaned by deletion.
- Lines 237-248: `bid` (12 lines, matching the hypothesis's "about 12 lines" exactly).
- Total contiguous deletion: lines 229-250 is 22 lines of which 229-248 (20 lines) are the two functions; line 249 begins `rec_evict`, line 250 its body.
- Production call sites requiring replacement code: lines 145 (`activate`), 259 (`evict_node`), 872 and 884 (`ev_act`).
- Test-battery call sites that would also break: lines 954, 986, 1206, 1211.

The "0 added lines" framing is not implementable: the four production call sites each need a replacement expression, and no learner-maintained value exists to substitute, so replacement code must be researcher-written. Further, because `bid()` is shared by fact selection and retention eviction, the deletion as hypothesized would silently change two mechanisms the hypothesis never discusses.

## Section 3: verification verdict

SUBSTRATE-ABSENT. The prereg is NOT frozen. No kill bars are frozen, no sealed family is specified, no verdict rule is adopted, because a prereg that cannot verify its substrate is not frozen.

What failed: verification (b) and (c). The fixed `bid()` formula exists exactly as hypothesized (12 lines, the only bid computation), but the substrate it would be replaced by does not exist: there is no learner-reachable path by which experience updates support counts on UNCERT nodes, there are no CONFIRM/CONTRADICT events, there is no learner link affordance, and there is no learner-maintained standing field for the guide selectors to read. The closest confirmation instrument (`r_learn_confirm`) is test-battery scaffolding unreachable from the cognition path. Additionally, `bid()` is shared machinery for query-path fact selection and retention eviction, which the hypothesis leaves unaddressed.

What a future H6-shaped hypothesis would need (recorded for the next worker, not adopted): a learner-reachable affordance that lets experience write standing-bearing edges (or fields) to UNCERT nodes with learner-chosen targets, reachable from `ev_observe`/`ev_query`/`ev_act`; a standing reader the guide selectors can call in place of `bid`; and an architecture accounting that handles `bid()`'s other two call sites (fact selection, eviction) instead of deleting shared machinery. Such an affordance does not exist in the frozen build and would be an addition, which contradicts the current zero-lines-added framing. The falsifiable prediction as written (singleton contradiction versus systematic shift producing identical versus discriminating standing trajectories) is untestable until the standing-update path exists: there is currently no mechanism by which standing trajectories get written at all. Note this also bears on H9 and H11, which likewise assume learner-fed standing instruments; both should be re-verified against this finding before any bars are frozen for them.

Governance notes for the record: pure Zag observed (writing only; no computation, no binaries, no forbidden executables invoked). Safebin activated, `which python3` and `which python` print nothing under the safebin PATH. No commits made by this worker; coordinator commits. Never push. No em-dashes used in lane documentation.
