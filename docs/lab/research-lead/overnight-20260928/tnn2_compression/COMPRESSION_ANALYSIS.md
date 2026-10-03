# TNN-2 Architecture Compression Analysis

Date: 2026-09-30. Status: COMPRESSION-ANALYSIS-COMPLETE (investigation only).
Target: `tnn2.zag`, 1591 lines, frozen at `f4de7ff46`. Read-only; no edits made.

## 1. Summary metrics

| Metric | TNN-1 (act-remed) | TNN-2 | Delta |
|---|---|---|---|
| Total lines | 1328 | 1591 | +263 |
| Cognition region lines (1-918) | ~881 nonblank | 822 nonblank | -59 nonblank* |
| Cognition functions | ~53 (prior method) | 108 (`^fn` in 1-918) | - |
| Test battery lines | - | 438 (919-1356) | - |
| ACT ported + main | - | 235 (1357-1591) | - |
| Fixed semantic cases (new) | 0 | 0 | 0 |
| Modes / bridges / handlers | 0 / 0 / 0 | 0 / 0 / 0 | 0 |
| Fixed plan templates | 3 (+exec_plan) | 0 | -3, -1 executor |
| Fixed assembler topologies | 0 | 3 (chain/count/sum) | +3 |
| Learner-created structures | MAPs, guides | MAPs, guides, 4-op graphs, UNCERTAINTY nodes | +2 types |

*The +263 total is (565 added - 302 removed). The 302 removed lines are
the old template system (T_PLAN/T_STEP/T_COMB tags, TM_*/SK_* tags,
plan_new/step_new/plan_c2/plan_g/plan_it/plan_comp, exec_plan), confirmed
by diff. The 565 added lines are the trial machinery, revision operator,
inquiry integration, and 5 new tests (~86 lines).

**Headline: ~118 lines of the 1591 are dead in the cognition path**
(test-only functions, a test-gated assembler branch, inlined wrappers).
Deleting them loses zero capability. Further unification saves ~30 more.
The 1200-line ceiling remains distant; reaching it needs architectural
deletion, not trimming.

## 2. Method

Every function in the cognition region (lines 1-918) was checked for
callers in the cognition path (as distinct from the test battery,
lines 919-1591). A function is DEAD-IN-COGNITION if its only callers
are test functions. Node-tag creations were audited to find
test-gated branches. Each section is classified ESSENTIAL,
CANDIDATE-FOR-DELETION, or NEEDS-MEASUREMENT.

## 3. Section-by-section classification

### 3.1 Substrate (lines 1-86): ESSENTIAL

emit/i64s/e64, z_alloc, get32/set32, WSZ/NN/NE, hg/hs, noff/ng/ns,
eoff/eg/es, loff/lg/ls, 13 edge-type tags, 4-op ISA tags (101-104),
node-type tags. The memory layout and ISA. One dead tag: ET_REG (11)
has zero `link_edge` uses in cognition. Trivial (1 line) but delete it.

### 3.2 Allocation (87-139): ESSENTIAL

alloc_node, alloc_raw, write_node, link_edge, is_superseded.

### 3.3 Retrieval (140-165): ESSENTIAL

activate (exact-hit), decay. The retrieval core that passes FW1/FW2/FW4/FW5.

### 3.4 Frame and the single executor (166-220): MIXED

- fr_get/fr_set, res_op, seq_nx, execute: ESSENTIAL. `execute` is the
  single executor (K-T2-2 satisfied; diff-verified byte-identical to base).
- exec_val (4 lines): CANDIDATE-FOR-DELETION. Only callers are t_c6/t_c7
  (lines 973, 980). Test-only helper sitting in the cognition region.

### 3.5 Eviction and ACT support (221-296): ESSENTIAL (one candidate)

is_prot, evcount, bid, rec_evict, evict_node, ref_prot: ESSENTIAL.
ctx_push/ctx_get: ESSENTIAL (ev_act context matching).
log_ev (~6 lines + ~15 call sites): CANDIDATE (low priority). The event
log region (`loff`/`lg`) has ZERO readers anywhere in the file. Write-only
instrumentation. Removing the calls saves little and loses debuggability;
deprioritize behind the ~118 dead lines.

### 3.6 Teach (297-317): ESSENTIAL (unification candidate)

ev_teach and ev_teach_in are near-duplicates (the former adds clock bump,
decay, ctx_push, SUP link, and log call). Unifying them behind one
function with a flag saves ~7 lines. CANDIDATE for unification, not
deletion. Low risk; NEEDS-MEASUREMENT only to confirm no test depends on
the exact side-effect difference.

### 3.7 Change 1: trial machinery (318-676): MIXED (the core of this report)

ESSENTIAL:
- seq_link, t2_lit/t2_cell/t2_guard/t2_set/t2_mov/t2_inc (cell constructors)
- t2_asm_chain (chain assembler; the workhorse)
- t2_asm_count (count assembler; gated on di==0, runs in freeze)
- t2_exec, t2_lu_first, t2_chain, t2_gather, t2_rels, inc_fill
- t2_try_verify, promote_graph, t2_trial, mp_run (thin wrapper; inlining
  saves ~5 lines, trivial)

CANDIDATE-FOR-DELETION (dead in the cognition path):
- t2_asm_sum (13 lines), t2_gather_sum (10 lines), comb_present (8 lines),
  popcnt (3 lines), and the sum subset-enumeration loop inside t2_trial
  (~24 lines). **The sum branch is gated on `comb_present(W)>=0`, which
  requires a tag-8 (T_COMB) node. No code in the cognition region
  (lines 1-918) creates tag-8 nodes; the sole creator is test t_p2
  (line 1106). In any real world, and in the freeze, the sum assembler
  NEVER runs.** This is ~58 lines of dead weight, and it means the
  arithmetic capability attributed to Change 1 does not actually execute
  outside test scaffolding. This bears directly on the FW3 freeze
  interpretation (see section 5).
- t2_sig (19 lines): graph-signature helper called only from t_t2_revise
  (lines 1287, 1290). Test-only; does not belong in the cognition region.
- map_standing (10 lines): called only from tests (1160, 1210, 1286, 1301).
  Dead in cognition.
- contradict_map (3 lines): the old demotion wrapper. Its one cognition
  call site was inlined (`link_edge(W,n,3,n,0)` at line 844). Only tests
  call it now. Dead in cognition.

ARCHITECTURAL (not line-deletion, but the important finding):
- The three assemblers are THREE FIXED TOPOLOGIES (chain, count, sum).
  t2_asm_count is t2_asm_chain plus an INC per link plus a MOVE epilogue;
  they are near-identical and could be one parameterized assembler
  (~20 lines saved, and the "fixed family" shrinks from 3 to 2).
  More importantly, the trial loop searches (gathered paths) x (3 fixed
  topologies). This is a larger finite researcher-authored family than
  the 3 templates it replaced, not open construction. The red-team
  question stands: the final structures are enumerable from a
  researcher-written family (path length <= 4, 3 topologies, literal
  values from observed facts). See section 5.

### 3.8 Change 3: revision (677-752): ESSENTIAL (with a generality caveat)

t2_kill_edge, revise_on_contradict, t2_revise_graph: ESSENTIAL for the
demonstrated capability. But the repair procedure is FULLY
RESEARCHER-AUTHORED: find the SETREG (tag 101) via provenance, find its
guard (tag 102), tombstone the stale step, insert a corrected SETREG
with the observed value, rewire guard and successor, re-execute, revert
on failure. **The learner contributes exactly one thing: `new_o`, the
contradicting observation's value. No part of the repair topology is
chosen by the learner.** "Replace bad MAP step" is a hardcoded
algorithm, not a general revision capacity. This does not make it a
deletion candidate (it works and is tested), but it means Change 3 as
built does not satisfy the generality claim in its own prereg. Fixing
that is a research problem (learner-authored repair operators), not a
compression problem. Flagged for the revision red team.

### 3.9 Change 2: inquiry and miss policy (753-812): ESSENTIAL (one measurement)

- k_get, miss_inquire: ESSENTIAL. The miss -> UNCERTAINTY (tag 30) ->
  guide -> POLICY_ROOT chain is the structural fix for FW6.
- bootstrap_miss (P-INV, ~32 lines): NEEDS-MEASUREMENT. It runs as a
  fallback AFTER the trial loop fails. Its job (k agreeing examples ->
  generalize the value) overlaps the trial loop's single-hop fallback.
  Experiment: disable bootstrap_miss (return -2 immediately) and run the
  46/46 suite plus the FW battery. If nothing regresses, delete it
  (~32 lines). If the P-INV tests fail, the question becomes whether the
  trial loop should subsume that case rather than keeping a parallel
  mechanism. Either way, two miss-path mechanisms is one too many.
- Generality caveat (not deletion): the guide constructed by
  miss_inquire has a HARDCODED choice=30. The structural loop
  (uncertainty -> guide -> POLICY_ROOT -> ev_act selects) is learner-
  driven, but the discriminating content of the inquiry (what question
  the guide represents) is a constant. The inquiry red team should press
  on this.

### 3.10 Entry points (813-918): ESSENTIAL

ev_query (trial-first, bootstrap fallback, miss_inquire on true miss),
ev_observe (revise_on_contradict on contradiction), ev_act (unchanged
5-step selection, now over learner-built guides), tnn2_init,
pol_get/pol_set/mp_get/mp_set. The ev_act nested loops are long but
functional; no duplication found.

## 4. Deletion candidates (capability impact: none)

| Candidate | Lines | Why safe |
|---|---|---|
| t2_asm_sum | 13 | Dead: gated on test-only tag-8 |
| t2_gather_sum | 10 | Only feeds t2_asm_sum |
| comb_present | 8 | Only gates the dead sum branch |
| popcnt | 3 | Only used by sum subset loop |
| sum subset loop in t2_trial | ~24 | Inside the dead branch |
| t2_sig | 19 | Test-only (t_t2_revise) |
| exec_val | 4 | Test-only (t_c6/t_c7) |
| map_standing | 10 | Test-only; demotion path dead in cognition |
| contradict_map | 3 | Inlined at call site; test-only |
| ET_REG tag | 1 | Zero uses |
| **Subtotal** | **~103** | |

Unification candidates (need measurement, small risk):
| Candidate | Saving | Experiment |
|---|---|---|
| ev_teach / ev_teach_in merge | ~7 | Run 46/46; confirm no test depends on side-effect delta |
| t2_asm_chain / t2_asm_count merge | ~20 | Parameterize INC-per-link + MOVE epilogue; run suite |
| mp_run inline into ev_query | ~5 | Trivial; run suite |
| log_ev call removal | ~15 calls | Confirm no external reader; low priority |

**Projected: 1591 -> ~1488 (dead-code deletion, zero capability loss) ->
~1456 (unification).** The 1200-line ceiling is still ~290 lines away;
closing that gap requires architectural deletion (section 6), not trimming.

## 5. Findings that affect freeze interpretation (not just compression)

1. **The sum assembler never runs in the freeze.** If TNN-2's FW3 result
   is a PASS, it comes from the chain or count assemblers, not the sum
   path. If FW3 is a FAIL, the dead sum branch is a candidate
   contributor: the arithmetic capability was built but left gated
   behind test scaffolding. Either way the freeze report should note it.
2. **The "one graph type" claim is partial.** K-T2-2 (one executor) is
   satisfied, but construction still selects among 3 researcher-authored
   topologies. The family is larger than the 3 templates it replaced,
   but it is still a finite enumerable family: path length <= 4, 3
   topologies, literals from observed facts, no nested calls, no
   learner-chosen wiring beyond path order.
3. **Revision is a hardcoded repair procedure.** It demonstrates
   counterexample-driven restructuring (a real advance over pure
   demotion), but the repair topology is not learner-authored.
4. **Inquiry constructs the loop, not the question.** Guide choice=30
   is constant; the discriminating need is not derived.

## 6. NEEDS-MEASUREMENT experiments (ordered by information value)

1. **Disable bootstrap_miss.** If the suite and FW battery hold, delete
   ~32 lines and remove the last parallel miss-path mechanism. If P-INV
   tests fail, decide: subsume into trial loop or keep with justification.
2. **Delete the sum branch** (t2_asm_sum, t2_gather_sum, comb_present,
   popcnt, subset loop). Run 46/46 + FW. Expect zero change (it is dead);
   any change reveals an unmapped tag-8 creator.
3. **Move test-only functions out of the cognition region** (t2_sig,
   exec_val, map_standing, contradict_map) into the test battery or a
   test-helper section. Zero behavior change; clarifies the architecture.
4. **Assembler unification.** Merge chain/count; measure that T2-CHAIN4
   and count tests still pass.
5. **Ablation of each assembler.** Disable chain, count individually;
   record which tests/worlds need which. This maps capability to
   machinery and tells the next generation what a truly general
   assembler must cover.

## 7. What NOT to delete

- The trial loop core (t2_trial, t2_gather, t2_try_verify,
  promote_graph): this IS the new general capability.
- The revision operator: the only topological-revision machinery; its
  generality is weak but its existence is the advance.
- miss_inquire and the UNCERTAINTY->guide->POLICY_ROOT wiring: the
  structural fix for the degenerate act path.
- execute, activate, eviction, bid: the frozen substrate.
- The test battery: evidence, not cognition; keep.

## 8. Verdict

COMPRESSION-ANALYSIS-COMPLETE. Deletion plan delivered: ~103 lines of
dead-in-cognition code removable with zero capability loss, ~32 more
pending one experiment (bootstrap_miss), ~32 via unification. The deeper
finding is architectural, not arithmetic: TNN-2 replaced 3 fixed
templates with 3 fixed assemblers, a hardcoded repair procedure, and a
constant-content inquiry guide. The mechanisms are real advances (runtime
construction, topological revision, learner-populated POLICY_ROOT), but
each still carries researcher-authored structure where the claims say
"learner-authored." The next generation's work is to move that structure
across the line, not to trim lines around it.
