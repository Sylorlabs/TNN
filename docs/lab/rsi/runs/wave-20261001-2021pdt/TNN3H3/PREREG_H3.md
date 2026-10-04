# PREREG H3: Procedure-as-operand unification (graphs are ordinary nodes)

Lane: TNN3H3, wave-20261001-2021pdt. Status: NOT FROZEN. Substrate verification FAILED (SUBSTRATE-ALREADY-UNIFIED on item (a); SUBSTRATE-ABSENT on item (c)). No bars frozen. This document records the verification evidence so the failure is inspectable and no future worker re-freezes this hypothesis in its current form.

Hypothesis source: docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md, section H3, read verbatim by this worker (not cited from the task message).

H3 as hypothesized: executable graphs live in the same addressable memory as facts, so a procedure can be an operand of another procedure. "The separate graph-cell allocation path is folded into the generic node allocator; the fact machinery's READ/LINK operations apply to graphs without special casing." Capability-source delta claimed: net negative, zero lines added, the MAP-versus-graph special casing deleted.

Context: H1 was killed this wave by sealed evaluation (H1 DEAD) with a presentation-level FABRICATION verdict on the builder's dev evidence. H2 was then stopped at the prereg stage by the verification-first process fix (SUBSTRATE-ABSENT: link_edge is direction-neutral, no restriction to lift; deletion would remove the only graph construction). The mandatory process fix applies to H3 as well: verify the substrate against the frozen build BEFORE freezing any bars. That verification is section 2 below.

Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash verified by this worker with sha256sum on 2026-10-01; matches the expected value character for character).

## Section 2: substrate verification (measured, quoted)

### (a) "Separate graph-cell allocation path" vs "generic node allocator": THE SEPARATE PATH DOES NOT EXIST. Unification is already the case. VERIFICATION FAILS as hypothesized.

Quoted verbatim from the frozen source, lines 86-104 (the generic allocator):

```
fn alloc_node(W:[]u8)i32 {
  let n:i32=2;
  while(n<1024){
    if(ng(W,n,36)==0){
      ns(W,n,36,1); ns(W,n,0,0);
      ...
      hs(W,20,hg(W,20)+1); return n;
    }
    n=n+1;
  }
  ...
}
```

Quoted verbatim, lines 338-348 (the cell constructors):

```
fn t2_lit(W:[]u8,v:i32)i32 {
  let n:i32=alloc_node(W); if(n<0){return -1;}
  ns(W,n,0,902); ns(W,n,20,v); return n;
}
fn t2_cell(W:[]u8,tag:i32)i32 {
  let c:i32=alloc_node(W); if(c<0){return -1;}
  ns(W,c,0,tag); return c;
}
```

Every graph cell constructor calls `alloc_node`, the same generic allocator used for fact nodes (ev_teach line 299, ev_teach_in line 311, promote_graph line 534, miss_inquire lines 796/802/806, guides, UNCERT nodes, MAP nodes). The sibling allocator `alloc_raw` (lines 105-117) is called exactly twice in the whole build: rec_evict line 250 and ev_observe line 846, never for cells. `z_alloc` (line 28) allocates only []u8 scratch buffers, never workspace nodes. All alloc_node callers verified by repository-wide grep: cells (lines 339, 343), frame (line 414), MAP (534), facts (299, 311), guides/uncert (796, 802, 806), all test scaffolding.

The frozen build's own header states the design intent (lines 16-17): "One workspace, one bid, one miss path, one event log, one executor." And the Change 1 comment (lines 329-330): "Literals are 902-nodes holding the value in field20 (data, not a new node type...)". Cells are ordinary nodes with tags 101-104 living in the same 1024-node store, the same field layout (offsets 64+n*40), the same generic READ/LINK machinery (ng/ns/eg/es link_edge).

Consequence: the H3 clause "the separate graph-cell allocation path is folded into the generic node allocator" names a change that cannot be made, because the two paths are already one. There is no separate allocation path to fold. This is SUBSTRATE-ALREADY-UNIFIED on verification item (a).

### (b) "MAP-versus-graph special casing (separate layouts, separate selectors)" to be deleted: NO SUCH DELETABLE SET EXISTS. Measured deletion set is EMPTY.

What the hypothesis points at: MAP nodes (tag 20) store field4=r, field8=s, field20=graph root (promote_graph, lines 530-537). Graph cells (tags 101-104) store field4=operand-slot/output-operand, field8=literal node, field12=branch target. Fact nodes (tag 1) store field20=s, field24=r, field28=o. These are three genuinely different STRUCTURES with genuinely different field semantics, each read by the code that created them (execute() reads cells, t2_sig reads cells, activate/t2_lu_first read tag-1 facts, contradict_map reads tag-20 MAPs). There is no code that treats one shared structure two different ways and could be simplified by deleting a case: nothing to delete, zero lines.

grep verification: no selector branches on "MAP vs graph" layouts. Tag-20 node creation sites: lines 535, 779, 1157, 1202 (MAP promotion and test scaffolding). Cell tag creation sites: lines 339-359 (t2_lit, t2_cell, t2_guard, t2_set, t2_mov, t2_inc). The layouts differ because the structures differ, not because of a removable special case. The only unification-relevant selector is link_edge itself, already direction-neutral and type-agnostic (verified in H2's PREREG_H2.md).

Measured deletion set: empty. Zero lines. The net-negative claim has no deletion target.

### (c) Post-deletion construction path for a learner-stored graph-as-fact-operand link: DOES NOT EXIST. VERIFICATION FAILS.

The event interface, exhaustively:
- ev_observe (line 836): stores facts via ev_teach_in, where write_node(W,n,s,r,o,...) puts a SCALAR i32 answer value o into field28. The contradiction branch calls revise_on_contradict and ev_teach_in. No cell allocation on any path; no edge from any fact to any graph root; no graph root stored into any fact operand field.
- ev_query (line 813): activate (exact fact match), mp_run (trial loop: assemblers run only inside t2_trial candidate construction, never persisting a fact with a graph operand), bootstrap_miss, miss_inquire (creates a tag-30 UNCERT node and a tag-1 guide node with scalar fields via write_node(W,g,30,-999,0,0)). No construction of graph-as-operand links.
- ev_act (line 859): action selection over guide edges. No construction at all.

The only graph-adjacent persistent links the frozen build writes: ET_DEP edges FROM cells TO licensing facts (t2_asm_chain line 373: link_edge(W,st,1,get32(f,j*4),0)), and the MAP node's field20 holding the promoted graph root (promote_graph line 537: write_node(W,m,root,...)). Neither is a fact with a graph as operand, and neither is written by the learner through the event interface: both are researcher-written construction inside the trial loop. There is no function, reachable or not, that stores a graph root node index as a fact operand or as the target of a learner-authored edge from a fact node. After the (empty) deletion, the post-deletion capability to produce procedure-as-operand links is still zero.

This is the H1/H2 failure mode exactly: the falsifiable prediction ("if on sealed worlds the learner never stores a graph as a fact operand... H3 is dead") would be satisfied trivially and vacuously, because the frozen build cannot express the behavior at all. Freezing bars against procedure-as-operand link creation on this substrate would repeat the vacuous-test failure.

### (d) What the learner CAN do after unification that it cannot do now: NOTHING, in concrete structural terms.

Because (a) shows allocation is already unified and (b) shows the deletion set is empty, the H3 change as stated (a pure deletion / folding) has no executable content. The genuine capability gap behind the hypothesis, a learner-reachable construction path that lets experience store a graph as a fact operand (or as an edge target from a fact node) through ev_observe/ev_query/ev_act, does not exist in the frozen build and would be an ADDITION of researcher-written construction machinery. That contradicts the hypothesis's zero-lines-added, net-negative framing, so it cannot be adopted as an amendment inside this prereg; it would be a different hypothesis with positive capability-source delta and its own architecture accounting.

## Section 3: verification verdict

SUBSTRATE-ALREADY-UNIFIED on (a) and SUBSTRATE-ABSENT on (c). The prereg is NOT frozen. No kill bars are frozen, no sealed family is specified, no verdict rule is adopted, because a prereg that cannot verify its substrate is not frozen.

What failed:
- Verification (a): the claimed "separate graph-cell allocation path" does not exist as a distinct path. All cells are allocated by the generic alloc_node, the same allocator facts use. The unification the hypothesis proposes is already the case.
- Verification (b): the "MAP-versus-graph special casing" is not a deletable special case; the measured deletion set is empty (zero lines). MAP nodes, cells, and facts are three different structures with different field semantics; no selector treats one shared structure two ways.
- Verification (c): no code path reachable from the frozen event interface (ev_observe/ev_query/ev_act) can produce a learner-stored graph-as-fact-operand link. Fact operands (field28) hold scalar answer values only. The falsifiable prediction is untestable on this substrate: the negative outcome would be vacuous, not informative.

What a future H3-shaped hypothesis would need (recorded for the next worker, not adopted): a learner-reachable construction path that lets experience build procedure-as-operand links (a graph root node addressable as a fact operand or as an edge target from learner-created structure) using the already-generic alloc_node and the direction-neutral link_edge. Such a path does not exist in the frozen build and would be an addition, which must be recorded with positive cognition-source delta and reviewed against the ONE-SYSTEM RULE, the protected-core ISA ruling, and the pending EXECUTE placement decision. H3 remains the furthest frontier with the lowest prior (ranked 11/11 in HYPOTHESES.md) and it presupposes H1's success, which this wave killed; any successor must reckon with that ordering.

Governance notes for the record: pure Zag observed (writing only; no computation, no binaries, no forbidden executables invoked). Safebin activated per setup_safebin.sh; `which python3` prints nothing under the safebin PATH. Branch tnn-native-lab, working copy /home/hatch/workspace/tnn-rsi; no commits made by this worker, coordinator commits; no push. Writes confined to docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H3/ (NAMECHECK.md, this file). No em-dashes used in lane documentation.
