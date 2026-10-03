# PREREG H4: Learner-authored content-to-action projection

Lane: TNN3H4, wave-20261001-2021pdt. Status: NOT FROZEN. Substrate verification FAILED (SUBSTRATE-ABSENT on item (b); SUBSTRATE-ABSENT on item (c)). No bars frozen. This document records the verification evidence so the failure is inspectable and no future worker re-freezes this hypothesis in its current form.

Hypothesis source: docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md, section H4 ("H4. Learner-authored content-to-action projection"), read verbatim by this worker (not cited from the task message).

H4 as hypothesized: replace the researcher-constant action write in `miss_inquire` (field20=30) with a learner-owned projection structure, a small executable cell over the frozen ISA that the learner authors, mapping uncertainty content (subject, relation, attached content) to an action value. `ev_act` keeps only the generic machinery of reading field20. The action alphabet becomes learner-extensible because the learner writes the projection. Fixes M2-W1 (informant discrimination) and M2-W3 (the constant-action triple). Capability-source delta claimed: net negative, zero lines added, the constant write and the fixed-alphabet assumption deleted, the projection cell learner-created and executed by existing protected EXECUTE machinery.

Context: H1 was killed this wave by sealed evaluation (H1 DEAD) with a presentation-level FABRICATION verdict on the builder's dev evidence. H2 was then stopped at prereg (SUBSTRATE-ABSENT: link_edge is direction-neutral, deletion removes the only graph construction). H3 was stopped at prereg (SUBSTRATE-ALREADY-UNIFIED on the allocator claim, SUBSTRATE-ABSENT on the construction path). The mandatory process fix for H4: verify the substrate against the frozen build BEFORE freezing any bars. That verification is section 2 below.

Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash verified by this worker with sha256sum on 2026-10-01; matches the expected value character for character).

## Section 2: substrate verification (measured, quoted)

### (a) The researcher-constant action write in miss_inquire: EXISTS and is the only action-content wire. PASSES as described.

Quoted verbatim, lines 795-811 (miss_inquire):

```
fn miss_inquire(W:[]u8,s:i32,r:i32)void {
  let u:i32=alloc_node(W); if(u<0){return;}
  ns(W,u,0,30);
  ns(W,u,4,-4);
  write_node(W,u,s,r,2,0);
  let pr:i32=pol_get(W);
  if(pr<2){
    pr=alloc_node(W); if(pr<0){return;}
    ns(W,pr,0,2); ns(W,pr,4,-5);
    pol_set(W,pr);
  }
  let g:i32=alloc_node(W); if(g<0){return;}
  ns(W,g,0,1); ns(W,g,4,s);
  write_node(W,g,30,-999,0,0);
  link_edge(W,g,1,u,0);
  link_edge(W,pr,10,g,0);
  return;
}
```

`write_node` (line 118-120) is:

```
fn write_node(W:[]u8,n:i32,a:i32,b:i32,c:i32,d:i32)void {
  ns(W,n,20,a); ns(W,n,24,b); ns(W,n,28,c); ns(W,n,32,d); return;
}
```

So line 808's `write_node(W,g,30,-999,0,0);` writes field20=30 on the guide node `g` (tag 1), field24=-999, field28=0. This is the constant action write the hypothesis names.

It is the ONLY action-content wire. Repository-wide grep for `ns(W,*,20,*)` writes shows the only guide field20 write is this one (other field20 write sites: alloc_node/alloc_raw zeroing lines 93/102/111, write_node itself line 119, t2_lit line 340, fr_set line 175 for frame registers, pol_set/mp_set lines 915/917 for header slots). The only READ of guide field20 as an action value is in ev_act, line 896:

```
  if(best>=2){
    let av:i32=ng(W,best,20);
    link_edge(W,best,6,best,0); log_ev(W,3,0,0,av,1,0,0); return av;
  }
```

The frozen self-test `t_t2_inquire` even codifies the constant (lines 1244-1245):

```
      if(ng(W,n,0)==30 && ng(W,n,20)==9002 && ng(W,n,24)==77){u=n;}
      if(ng(W,n,0)==1 && ng(W,n,4)==9002 && ng(W,n,20)==30){g=n;}
```

The test requires field20==30 on the guide to pass. Verification item (a) passes exactly as the hypothesis phrases it.

### (b) A learner-reachable construction path for authoring a small executable cell: DOES NOT EXIST. SUBSTRATE-ABSENT. VERIFICATION FAILS.

The cell constructors are lines 338-361 (`t2_lit`, `t2_cell`, `t2_guard`, `t2_set`, `t2_mov`, `t2_inc`; cells are tag 101-104 nodes allocated by the generic `alloc_node`, with guard/set semantics in field4/field8/field12/field16). Repository-wide grep for every invocation of these six constructors returns, exhaustively:

- Lines 366-372: `t2_asm_chain` (guard cell + set cell per link, fixed slot 0)
- Lines 382-393: `t2_asm_count` (guard + set + inc + move epilogue, fixed slots)
- Lines 405-406: `t2_asm_sum` (inc cells only)
- Lines 725-729, 736: `t2_revise_graph` (literal + forward set cell `t2_set(W,0,ly)`, fixed slot 0)

The assemblers are called only from `t2_trial` (lines 603, 626, 642, 657), called from `mp_run` (line 672), called from `ev_query` (line 830). The construction there is entirely researcher-authored: guard slot, literal values (gathered from existing facts by `t2_gather`/`t2_chain`), set orientation, and chaining topology are all fixed by the assembler schema. The learner's only influence is the scalar `expected` value used for verification and the MISS_POLICY flags (masked/dc/di). The learner cannot choose a guard slot, a set slot, a cell topology, or any field of a cell.

`t2_revise_graph` is called from `revise_on_contradict` (line ~697), called from `ev_observe` (line 849). The learner supplies only the contradicting scalar observation `o`; the inserted cell is a fixed forward set cell writing the new value.

The event interface, exhaustively, allocates no learner-controlled executable cells and writes no ET_SEQ (type 12) edges between cells:

- `ev_observe` (line 836): stores facts/scalars via `ev_teach_in`, writes edges of types 9/5/7/3/1/4, calls `revise_on_contradict`. No tag 101-104 allocation on any learner-driven path.
- `ev_query` (line 813): `activate` (exact match), the researcher-written trial loop, `bootstrap_miss` (MAP nodes), `miss_inquire` (tag-30 UNCERT node + tag-1 guide node + edges types 1/10). No learner-authored cell.
- `ev_act` (line 859): selection and bidding over guide edges only; writes a single type-6 edge; no construction of any kind.

There is no generic field-write path reachable from the event interface: `ns()` is invoked from event-reachable functions only with researcher-fixed tags, offsets, and values. No code path lets experience allocate a cell and write its guard/set fields with learner-chosen content.

Consequence: deleting the constant write does NOT give the learner a construction path. The "small executable cell over the frozen ISA that the learner authors" cannot be authored by the learner through any path from ev_observe/ev_query/ev_act. This is the H2 finding exactly: deletion removes capability; it does not liberate construction. The falsifiable prediction ("if the learner authors projections but they collapse to constants, H4 is dead") is untestable on this substrate: the learner cannot author projections at all, so the negative outcome would be vacuous, not informative. Freezing bars against learner-authored projections on this substrate would repeat H1's vacuous-test failure.

### (c) The protected EXECUTE machinery executing a learner-authored cell from ev_act: NOT REACHABLE FROM ev_act ON ANY CELL. SUBSTRATE-ABSENT. VERIFICATION FAILS.

`execute()` (lines 192-215) is the 4-op ISA executor: tags 101 (MOVE), 102 (BRANCHEQ), 103 (INC), 104 (DEC), with frame operands >= 1000. Its callers, exhaustively:

- Line 217: `exec_val`, called only from test scaffolding `t_c6`/`t_c7` (lines 973, 980). Not the cognition path.
- Line 416: `t2_exec`, called from `t2_trial` (line 500, the researcher-written trial loop) and from test scaffolding (line 1289).
- Line 732: `t2_revise_graph` (re-execution after surgical revision, researcher-authored).

`ev_act` (lines 859-907) contains NO call to `execute`, `exec_val`, or `t2_exec`. Its action wire is the direct scalar read at line 896 (`let av:i32=ng(W,best,20);`), with `log_ev` and a plain `return av;`. Quoted verbatim, the tail of ev_act:

```
  if(best>=2){
    let av:i32=ng(W,best,20);
    link_edge(W,best,6,best,0); log_ev(W,3,0,0,av,1,0,0); return av;
  }
  log_ev(W,3,0,0,0,0,0,0); return 0;
```

So the H4 clause "the projection cell is learner-created and executed by existing protected EXECUTE machinery" is false for the action path in two independent ways: the cell cannot be learner-created (item b), and even a researcher-placed cell would never be executed by ev_act, because the action path bypasses EXECUTE entirely. Wiring EXECUTE into ev_act would be an addition of cognition-path machinery, which contradicts the hypothesis's net-negative, zero-lines-added framing.

### (d) Measured deletion set (not estimated)

- Line 808: `write_node(W,g,30,-999,0,0);` in `miss_inquire`. 1 line: the constant action write.
- The "fixed-alphabet assumption" is embodied in: (i) the line-808 constant itself; (ii) `ev_act` line 896's read of field20 as the action value (H4 keeps this: "ev_act keeps only the generic machinery of reading field20"); (iii) the frozen self-test `t_t2_inquire` lines 1244-1245, which asserts field20==30 on the guide (a test that would fail if the constant were deleted, so the deletion is not self-contained: it requires a test change too, unless the self-test is also deleted).

A compilable H4-shaped change would additionally require: replacing the constant with an execute-based projection read (an ev_act machinery addition), and a learner-reachable construction path for the projection cell (an addition of learner construction machinery, or a rewiring of the trial loop to emit projection cells under learner control). None of this is a deletion. The "net negative" claim has no viable deletion-only implementation.

## Section 3: verification verdict

SUBSTRATE-ABSENT on (b) and (c). The prereg is NOT frozen. No kill bars are frozen, no sealed family is specified, no verdict rule is adopted, because a prereg that cannot verify its substrate is not frozen.

What failed:
- Verification (a): PASSED. The constant write exists exactly as hypothesized: line 808 `write_node(W,g,30,-999,0,0);` in `miss_inquire`, the only write of field20 on guide nodes, with `ev_act` line 896 the only reader. The frozen self-test codifies the constant at lines 1244-1245.
- Verification (b): FAILED, SUBSTRATE-ABSENT. No code path from ev_observe/ev_query/ev_act lets the LEARNER allocate a cell (tags 101-104) and write its guard/set fields. The six cell constructors are invoked only from the three researcher-written assemblers inside the trial loop and from the researcher-written surgical revision. Deleting the constant write does not create a construction path.
- Verification (c): FAILED, SUBSTRATE-ABSENT. The protected EXECUTE machinery (lines 192-215) is not reachable from ev_act on any cell, learner-authored or otherwise: ev_act's action wire is a direct `ng(W,best,20)` field read with no execute call. H4's "executed by existing protected EXECUTE machinery" is not true of the action path.

What a future H4-shaped hypothesis would need (recorded for the next worker, not adopted): (1) a learner-reachable construction path that lets experience author cell structures with learner-chosen guard/set content (an addition, with positive cognition-source delta recorded); (2) EXECUTE wired into the ev_act action path (an addition, reviewed against the ONE-SYSTEM RULE and the pending EXECUTE placement decision); (3) a replacement for the self-test constant assertion at lines 1244-1245. Such a hypothesis cannot keep H4's net-negative, zero-lines-added framing. It must also reckon with the emerging wave pattern (H2, H3, H4): the frozen TNN-2 core appears to have no learner-reachable executable-construction path at all; ev_observe writes facts/scalars only, ev_act only selects, and the trial loop's construction is researcher-authored. Any successor hypothesis that depends on learner-authored executable structure must either build that path as an explicit addition or demonstrate one that this verification missed.

Governance notes for the record: pure Zag observed (writing only; no computation, no binaries, no forbidden executables invoked). Safebin activated per setup_safebin.sh; `which python3` and `which python` print nothing under the safebin PATH. Branch tnn-native-lab, working copy /home/hatch/workspace/tnn-rsi; no commits made by this worker, coordinator commits; no push. Writes confined to docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H4/ (NAMECHECK.md, this file). No em-dashes used in lane documentation.
