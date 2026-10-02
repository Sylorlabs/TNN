# PREREG H2: Learner-asserted derivation direction (invertible learner links)

Lane: TNN3H2, wave-20261001-2021pdt. Status: NOT FROZEN. Substrate verification FAILED (SUBSTRATE-ABSENT). No bars frozen. This document records the verification evidence so the failure is inspectable and no future worker re-freezes this hypothesis in its current form.

Hypothesis source: docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md, section H2, read verbatim by this worker (not cited from the task message).

H2 as hypothesized: the learner may assert derivation links in either direction over structures it created, including cells whose guard tests an output slot and whose set writes an input slot. Inversion becomes a construction the learner expresses with the generic LINK affordance, not a schema the researcher must supply. Substrate change claimed: "the forward-only assumption is deleted from the assemblers and the generic LINK operation (already protected machinery) is no longer direction-restricted by researcher code." Capability-source delta claimed: net negative, zero lines added.

Context: H1 was killed this wave by sealed evaluation (zero learner-created names) and an independent red team rendered a presentation-level FABRICATION verdict: PREREG_H1.md asserted a naming affordance (tag 904, NAME edges) that the frozen tnn2.zag never contained, while freezing a "0 added lines" deletion plan, so the test was vacuous and the dev harness constructed the signature it then verified. The mandatory process fix for H2: verify the substrate against the frozen build BEFORE freezing any bars. That verification is section 2 below.

Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash verified by this worker with sha256sum on 2026-10-01; matches the expected value character for character).

## Section 2: substrate verification (measured, quoted)

### (a) The generic LINK operation: EXISTS, but is direction-neutral. The claimed restriction does not exist. VERIFICATION FAILS as hypothesized.

Quoted verbatim from the frozen source, lines 121-131:

```
fn link_edge(W:[]u8,f:i32,t:i32,to:i32,clk:i32)i32 {
  let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)==-1){
      es(W,e,0,f); es(W,e,4,t); es(W,e,8,to); es(W,e,12,clk);
      hs(W,24,hg(W,24)+1); return e;
    }
    e=e+1;
  }
  return -1;
}
```

`link_edge` accepts arbitrary (from, type, to, clock) and writes them into the first free edge slot. There is no check on the relationship between `f` and `to`: no index comparison, no direction validation, no rejection of any (from, to) pair. A repository-wide search for direction language (`backward`, `forward`, `direction`, `inverse`, `invert`) returns only four hits, all about the retention/ACT "directional bid" (eviction bid direction), none about edge-link direction. No researcher code anywhere in the frozen build restricts the direction of `link_edge`.

Consequence: the H2 clause "the generic LINK operation (already protected machinery) is no longer direction-restricted by researcher code" describes a change that cannot be made, because the restriction it names does not exist. This is a SUBSTRATE-ABSENT finding on verification item (a) as the hypothesis phrases it. The operation exists; the restriction does not.

### (b) The "forward-only assumption" in the assemblers: EXISTS as a constructive schema, not as a restriction. PASSES with corrected characterization.

Quoted verbatim, lines 362-376 (t2_asm_chain):

```
// chain graph: guard each link (v[j] -> v[j+1]), set on match.
fn t2_asm_chain(W:[]u8,v:[]u8,plen:i32,f:[]u8)i32 {
  let root:i32=-1; let prev:i32=-1; let j:i32=0;
  while(j<plen-1){
    let lx:i32=t2_lit(W,get32(v,j*4)); if(lx<0){return -1;}
    let ly:i32=t2_lit(W,get32(v,(j+1)*4)); if(ly<0){return -1;}
    let g:i32=t2_guard(W,0,lx); if(g<0){return -1;}
    let st:i32=t2_set(W,0,ly); if(st<0){return -1;}
    ns(W,g,12,st);
    link_edge(W,st,1,get32(f,j*4),0);
    if(prev>=0){seq_link(W,prev,g);} else {root=g;}
    prev=st; j=j+1;
  }
  return root;
}
```

Every constructed step guards slot 0 against the input value `v[j]` (`t2_guard(W,0,lx)`) and sets slot 0 to the next value `v[j+1]` (`t2_set(W,0,ly)`), chained in fact order via `seq_link` (which is `link_edge(W,a,12,b,0)`, ET_SEQ). `t2_asm_count` (lines 379-395) repeats the identical forward guard/set pattern with an INC cell and a MOVE epilogue; `t2_asm_sum` (lines 398-410) unrolls INC cells. The call sites in `t2_trial` (lines 603, 626, 642, 657) always pass forward-ordered value sequences gathered by `t2_gather` (line 442: BFS from the query subject following subject-to-object facts) and `t2_chain` (line 428: `set32(v,0,s)` then follows object links forward). There is no code path in the frozen build that constructs a cell whose guard tests an output slot and whose set writes an input slot.

The accurate characterization: the forward-only property is a property of the only constructors that exist, not a restriction imposed on a general constructor. Deleting the assemblers deletes the only graph construction; it does not liberate a general constructor.

### (c) Measured deletion set (not estimated)

Definitions and their comments, lines 362-410 inclusive: 49 lines total.
- Line 362: chain comment (`// chain graph: guard each link (v[j] -> v[j+1]), set on match.`)
- Lines 363-376: `t2_asm_chain` (14 lines)
- Lines 377-378: count comment (2 lines)
- Lines 379-395: `t2_asm_count` (17 lines)
- Lines 396-397: sum comment (2 lines)
- Lines 398-410: `t2_asm_sum` (13 lines)

A compilable deletion additionally requires the four call sites in `t2_trial` (lines 603, 626, 642, 657) and the candidate-construction scaffolding built around them (`t2_trial` spans approximately lines 586-665; each call site sits inside a gather/allocate/verify/promote block that exists only to feed the assembler). The hypothesis text's "0 added lines" framing omits this: the deletion is not self-contained at lines 362-410.

### (d) What the learner CAN do after deletion via the frozen event interface: it cannot assert inverse links. Post-deletion construction capability is zero.

Cell constructors (`t2_cell`, `t2_guard`, `t2_set`, `t2_mov`, `t2_inc`, `t2_lit`, lines 338-361) are called only from the three assemblers (lines 382-392, 405) and from `revise_on_contradict` (lines 725-726, which builds a forward corrected set cell `t2_set(W,0,ly)`). The event interface:

- `ev_observe` (line 836): creates type-1 fact nodes and edges of types 9/5/7/3/1/4; calls `revise_on_contradict`. No cell allocation, no ET_SEQ (type 12) edge writes on cells.
- `ev_query` (line 813): `activate` (exact fact match), `mp_run`/`t2_trial` (the gutted trial loop), `bootstrap_miss`, `miss_inquire`. No learner-reachable cell construction.
- `ev_act` (line 859): action selection over guide edges. No construction.

No code path reachable from `ev_observe`/`ev_query`/`ev_act` allocates executable cells (tags 101-104) or writes ET_SEQ edges between cells. After deleting the assemblers, the only remaining cell constructor is the forward set cell in `revise_on_contradict`. The event interface therefore cannot produce learner-asserted inverse links even after the deletion: the deletion removes the only graph-construction capability, forward and inverse alike. Freezing accuracy bars against "learner-created inverse links" on this substrate would repeat H1's vacuous-test failure exactly: the test would measure a capability the frozen build cannot express, and any "verification" would have to come from a dev harness that constructs the signature itself.

## Section 3: verification verdict

SUBSTRATE-ABSENT. The prereg is NOT frozen. No kill bars are frozen, no sealed family is specified, no verdict rule is adopted, because a prereg that cannot verify its substrate is not frozen.

What failed: verification (a). The generic LINK operation exists and is direction-neutral; the direction restriction the hypothesis proposes to lift does not exist in researcher code. The hypothesis as written ("net negative: delete the forward-only assumption; LINK no longer direction-restricted") cannot be implemented as a pure deletion: deletion removes all graph construction rather than enabling inverse construction.

What a future H2-shaped hypothesis would need (recorded for the next worker, not adopted): a learner-reachable construction path that lets experience assemble cell graphs with learner-chosen guard/set slot orientation, using the direction-neutral `link_edge` and the 4-op ISA executed by `execute()` (lines 192-217, tags 101-104). Such a path does not exist in the frozen build and would be an addition, which contradicts the current zero-lines-added framing; the architecture accounting would have to change accordingly. The falsifiable prediction as written (inverse links created but EXECUTE cannot answer because the 4-op ISA lacks the computation) is untestable until the construction path exists: there is currently no mechanism by which inverse links get created at all.

Governance notes for the record: pure Zag observed (writing only; no computation, no binaries, no forbidden executables invoked). Safebin activated, `which python3` and `which python` print nothing under the safebin PATH. No commits made by this worker; coordinator commits. No em-dashes used in lane documentation.
