# PREREG H7: Revision as re-derivation from live facts

Lane: TNN3H7, wave-20261001-2021pdt. Status: NOT FROZEN. Substrate verification FAILED (SUBSTRATE-ABSENT on item (b)). No bars frozen. This document records the verification evidence so the failure is inspectable and no future worker re-freezes this hypothesis in its current form.

Hypothesis source: docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md, section H7 ("H7. Revision as re-derivation from live facts"), read verbatim by this worker (not cited from the task message).

H7 as hypothesized: delete the single literal-swap revision schema (`t2_revise_graph`, about 46 lines) and replace the revision operator with supersede-then-rederive: the contradiction marks the old MAP superseded (H5 transition) and "the learner's own construction process runs again against the current fact store." The unit of revision becomes re-derivation, not patching. Capability-source delta claimed: zero lines added; about 66 lines of revision-schema code deleted; net negative; no new handlers; "re-derivation reuses whatever construction the learner owns."

Context: H1 was killed this wave by sealed evaluation (zero learner-created names) with a presentation-level FABRICATION verdict. H2/H3/H4/H6 were stopped at prereg by the verification-first process fix, all SUBSTRATE-ABSENT with the same root cause: the frozen TNN-2 core has no learner-reachable construction, update, or standing-maintenance paths. H5 (the generic transition H7's supersession step relies on) ADVANCES this wave on a dev implementation with all nine frozen bars passing, but H5's supersession is not the crux of H7: H7's load-bearing clause is "re-derivation reuses whatever construction the learner owns." The hypothesis document itself flags the dependency (HYPOTHESES.md cross-hypothesis notes): "H1 is load-bearing for H3 and partly for H7/H8: re-derivation and laws inherit whatever construction the learner owns. If H1 fails, H7's negative prediction (re-learning the same wrong thing) becomes the expected outcome rather than a surprise." H1 failed this wave. That verification is section 2 below.

Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash verified by this worker with sha256sum on 2026-10-01; matches the expected value character for character).

## Section 2: substrate verification (measured, quoted)

### (a) t2_revise_graph, the ~46-line deletion target: EXISTS, exactly 46 lines, and is the only revision machinery. PASSES as described.

Definition site, line 706. Closing brace, line 751. 706 to 751 inclusive is 46 lines, matching the hypothesis's "about 46 lines" exactly.

Quoted verbatim, lines 702-710 (comment plus entry):

```
// surgical revision: find the stale SETREG step via provenance, tombstone
// it, insert a corrected step, rewire, re-execute. On verification failure
// the graph is reverted and 0 returned. On success the promoted answer
// fact is contradicted and the corrected answer taught; standing untouched.
fn t2_revise_graph(W:[]u8,m:i32,factn:i32,old_o:i32,new_o:i32)i32 {
  let root:i32=ng(W,m,20); let s:i32=ng(W,m,8); let r:i32=ng(W,m,4);
  let ans_old:i32=ng(W,m,28);
  let e:i32=0; let stale:i32=-1;
```

Quoted verbatim, lines 723-733 (the corrective construction inside the deletion target):

```
  let succ:i32=seq_nx(W,stale);
  let ly:i32=t2_lit(W,new_o); if(ly<0){return 0;}
  let nst:i32=t2_set(W,0,ly); if(nst<0){return 0;}
  link_edge(W,nst,1,factn,0);
  ns(W,g,12,nst);
  if(succ>=0){seq_link(W,nst,succ);}
  if(succ>=0){t2_kill_edge(W,stale,12,succ);}
  ns(W,stale,0,0); ns(W,stale,36,0);
```

Quoted verbatim, lines 751-753 (function end, next function starts):

```
  return 1;
}
// ============ unified query: exact hit, else trial, else P-INV, else miss ============
```

Single caller: line 696, inside `revise_on_contradict`, which is itself called only from `ev_observe` (line 849) on the contradiction branch. Repository-wide grep for `t2_revise_graph` returns exactly two hits: the call at 696 and the definition at 706. There is no other revision machinery in the frozen build; deleting it removes all graph revision.

Verification item (a) passes: the deletion target exists exactly as hypothesized.

### (b) "The learner's own construction process" that re-derivation would reuse: DOES NOT EXIST. SUBSTRATE-ABSENT. VERIFICATION FAILS.

Exhaustive inventory of every construction path in the frozen build, by who authors it and what triggers it.

Path 1: the trial loop. `t2_trial` (lines 586-665) calls the three assemblers `t2_asm_chain`, `t2_asm_count`, `t2_asm_sum` at lines 603, 626, 642, 657, and nowhere else calls them (repository-wide grep confirms: definition sites 363, 379, 398; call sites only 603, 626, 642, 657). `t2_trial` is called only from `mp_run` (line 672), called only from `ev_query` (line 830) on the miss path. The loop is entirely researcher-authored: attempt order (path lengths k=2..4, then sum subsets, then count rels, then length-2 chains), schema choice per gather strategy, fixed guard slot 0 and set slot 0 in every assembler (`t2_guard(W,0,lx)`, `t2_set(W,0,ly)`), chaining topology via `seq_link`, verification against the caller-supplied scalar `expected`. The learner's entire contribution is the accumulated fact store that `t2_gather`/`t2_gather_sum`/`t2_chain` read, plus the scalar `expected` value and MISS_POLICY flags passed by the caller. The learner chooses no schema, no slot orientation, no topology, no construction parameter. The construction is researcher-written and triggered by query misses, not learner-directed.

Path 2: the deletion target itself. `t2_revise_graph` (lines 706-751) builds a literal node (`t2_lit`, line 725) and a fixed forward set cell (`t2_set(W,0,ly)`, line 726) with researcher-fixed rewiring. Called from `revise_on_contradict` (line 696) on the `ev_observe` contradiction branch. Researcher-authored; this is the machinery H7 deletes, not machinery re-derivation could reuse.

Path 3: fact and scaffolding construction. `ev_teach_in` writes tag-1 fact nodes with scalar fields; `miss_inquire` (lines 795-811) writes the UNCERT node (tag 30) and guide with fixed fields; `bootstrap_miss` writes MAP nodes with fixed structure. All researcher-written with fixed fields; no learner choice of structure. (H6's prereg verified exhaustively that no code path after creation updates UNCERT nodes, and H4's verified that the event interface allocates no learner-controlled executable cells.)

The six cell constructors (`t2_cell`, `t2_guard`, `t2_set`, `t2_mov`, `t2_inc`, lines 342-359) are invoked, exhaustively: lines 368-369 (t2_asm_chain), 384-386 and 392 (t2_asm_count), 405 (t2_asm_sum), and 726 (t2_revise_graph, the deletion target). After H7's deletion, the only remaining invocations are the trial loop's researcher-written schemas. There is no fourth path, and no path anywhere in the file on which experience allocates a cell or writes a cell field with learner-chosen content.

Consequence: the H7 clause "re-derivation reuses whatever construction the learner owns" has no referent in the frozen substrate. What the learner "owns" in any construction sense is zero; H1's sealed evaluation this wave found zero learner-created names, and H2/H3/H4 found zero learner-reachable construction paths. The only executable "re-derivation" the post-deletion build could perform is re-running `t2_trial` on a subsequent miss, which re-runs the identical researcher-written stamped-path schemas. That is exactly the treadmill the hypothesis's own falsifiable prediction names: "if re-derivation reproduces the identical stale structure (because the learner's construction process is still the stamped-path schema and nothing about it changed), H7 is dead: re-derivation without a changed construction process is a treadmill that re-learns the same wrong thing, and revision cannot be fixed independently of construction." The substrate guarantees this outcome, not as an empirical surprise but as a structural certainty, because there is no construction process of the learner's to run again.

### (c) A contradiction-to-construction trigger for re-derivation: DOES NOT EXIST on the frozen substrate. INDEPENDENT CONFIRMATION.

H7 requires that contradiction cause re-derivation: "the contradiction marks the old MAP superseded ... and the learner's own construction process runs again." On the frozen substrate, the contradiction branch of `ev_observe` (lines 836-856) is:

```
  if(n>=0){
    if(ng(W,n,28)==o){
      link_edge(W,n,7,n,0); ref_prot(W,n);
      log_ev(W,4,s,r,o,1,0,0); return 1;
    }
    link_edge(W,n,3,n,0);
    revise_on_contradict(W,n,o);
    ...
    let nn:i32=ev_teach_in(W,s,r,o);
    if(nn>=0){link_edge(W,nn,4,n,0);}
    log_ev(W,4,s,r,o,0,0,0); return 0;
  }
```

With `t2_revise_graph` deleted and `revise_on_contradict` gutted accordingly, the contradiction branch would: write a type-3 self-edge on the fact, teach the new fact, write a type-4 edge. `mp_run`/`t2_trial` are called only from `ev_query`'s miss path (line 830); teaching a fact does not trigger a miss, and nothing in the contradiction branch invokes construction. So post-deletion, the stale MAP (tag 20, with its stale graph root in field20) would sit unrevised: no code marks it superseded (the H5 transition lives in H5's dev implementation, not in the frozen tnn2.zag) and no code re-runs construction against the updated fact store. "Re-derivation" would never fire. This is a second, independent structural reason the hypothesis as specified cannot be implemented on the frozen substrate as a pure deletion.

### (d) Measured deletion set (not estimated)

- Lines 706-751: `t2_revise_graph` (46 lines: the definition at 706 through the closing brace at 751).
- The hypothesis claims "about 66 lines of revision-schema code deleted"; the function itself is 46 lines. The remaining ~20 lines are presumably the calling scaffolding in `revise_on_contradict` (lines 686-700, 15 lines: `t2_kill_edge` is shared with no other caller and would be orphaned; `revise_on_contradict`'s MAP-scan loop exists only to feed the call at line 696). A compilable deletion additionally orphans `t2_kill_edge` (lines 677-684, 8 lines), whose only caller is `t2_revise_graph` (lines 731, 734). Measured, not estimated.

What the deletion does NOT leave behind: any re-derivation trigger and any learner construction to reuse. The deletion removes the only revision machinery and leaves the only construction (the researcher trial loop) untouched but untriggered by contradiction.

## Section 3: verification verdict

SUBSTRATE-ABSENT. The prereg is NOT frozen. No kill bars are frozen, no sealed family is specified, no verdict rule is adopted, because a prereg that cannot verify its substrate is not frozen.

What passed: verification (a). `t2_revise_graph` exists at lines 706-751, exactly 46 lines, the single literal-swap revision schema, called only from `revise_on_contradict` (line 696) on the `ev_observe` contradiction path. The deletion target is real.

What failed: verification (b), the crux. "The learner's own construction process" does not exist in the frozen substrate. Every construction path is researcher-authored: the trial loop's three assemblers (triggered by query misses, fixed schemas, fixed slot 0, caller-supplied `expected`), the surgical revision being deleted, and the fixed-field scaffolding in `miss_inquire`/`ev_teach_in`/`bootstrap_miss`. The learner contributes the fact store and scalar values but chooses no structure. Re-derivation "reusing whatever construction the learner owns" therefore has no referent; the only re-runnable construction is the researcher trial loop, which re-runs the identical stamped-path schemas. The hypothesis's own falsifiable prediction describes exactly this as the dead outcome, and H1's failure this wave (zero learner-created names) is the dependency the hypothesis document itself flagged: "If H1 fails, H7's negative prediction (re-learning the same wrong thing) becomes the expected outcome rather than a surprise."

Supporting failure: verification (c). No contradiction-to-construction trigger exists on the frozen substrate: the `ev_observe` contradiction branch calls `revise_on_contradict` (the deletion target) and teaches the new fact, but never invokes `mp_run`/`t2_trial`, so post-deletion re-derivation would never fire at all. The H5 supersession transition exists only in H5's dev implementation this wave, not in the frozen tnn2.zag the hypothesis's net-negative claim is specified against.

What a future H7-shaped hypothesis would need (recorded for the next worker, not adopted): (1) a learner-reachable construction process, meaning experience can assemble executable structures with learner-chosen content through the event interface; (2) a contradiction-to-construction trigger so supersession causes re-derivation rather than leaving the stale MAP silent; (3) architecture accounting with positive cognition-source delta for both, since neither is a deletion. Such a hypothesis cannot keep H7's net-negative, zero-lines-added framing. It must also reckon with the wave pattern (H2, H3, H4, H6, H7): the frozen TNN-2 core has no learner-reachable executable-construction path at all, and revision cannot be fixed independently of construction, exactly as H7's own falsifiable prediction states.

Governance notes for the record: pure Zag observed (writing only; no computation, no binaries, no implementation files written, no forbidden executables invoked). Safebin activated per setup_safebin.sh; `which python3` and `which python` print nothing under the safebin PATH. Branch tnn-native-lab, working copy /home/hatch/workspace/tnn-rsi; no commits made by this worker, coordinator commits; never push. Writes confined to docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H7/ (NAMECHECK.md, this file). No em-dashes used in lane documentation.
