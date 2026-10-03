# COMP-1 Red Team Report

## Verdict: COMP1-REDTEAM-COMPLETE

Four of five attack vectors pass. One process-level ATTACK-SUCCESS.
No scientific claim is broken; the implementation source is sound.

## Target

`docs/lab/research-lead/overnight-20260928/comp1_build/comp1.zag`
(commit `170e39424`). 879 source lines. Prereg `4f6f0c5c8`.

## Step 0 guard

`/usr/bin/python3` present as unremovable system binary. Documented
non-use. Zero Python invocations this wave. Zag/shell only.

## Vector 1: Template enumeration - ATTACK-PASS

Exactly three template constructors exist: `plan_chain2`,
`plan_gather`, `plan_iterate` (source lines 242, 255, 280).
`plan_new` is invoked with a template literal at exactly five call
sites: tm=1,2,3 from the three constructors, tm=4 from
`plan_extend_read` (line 328) and `plan_compose_c2` (line 365).

The tm=4 marker (COMPOSED) is written but never read in any
dispatch. There is no `if(tm==4)` branch anywhere in the source.
The only template-id comparisons are `!=1` (line 308,
`chain_outslot` linearity gate) and `==1` (line 544,
composition input gate). The marker exists solely as trace
provenance for the T4 test. It confers no semantic case.

All T_PLAN nodes are created via `plan_new` (the single
`n_set_tag(...,5)` at line 211 is inside `plan_new` itself).
The executor dispatches on exactly six step kinds (1,2,3,4,5,6);
no hidden seventh kind. Zero new core execution operations
confirmed by inspection.

## Vector 2: Three-hop genuineness - ATTACK-PASS

`plan_extend_read` and `plan_compose_c2` are genuine
plan-structure composition, not a disguised fourth template:

- Both take an existing plan node as input and walk its SEQ
  edge chain, cloning each step node with its operands via
  `clone_step`.
- The extension point is computed from the input plan by
  `chain_outslot` (the destination slot of the last READ).
- The appended READ relations come from the subject-incident
  relations of the executed intermediate value, not from a
  fixed enumeration.
- Different input plans produce structurally different
  composed plans. The output shape is a function of the
  input plan graph.

A fourth template would have a fixed step shape independent
of input. These functions have no fixed shape; they are
parameterized by the plan they extend. The composition claim
holds.

## Vector 3: Expected-value leakage (e-ruling) - ATTACK-PASS

Structural verification, not just test observation:

- `mp_build(ws,es,m,subj,rel,out,flags)`: no `expected`
  parameter.
- `mp_build_compose(ws,es,m,subj,rel,cands,vals,nc)`: no
  `expected` parameter.
- `mp_run` receives `expected` but consults it only in the
  selection loop (lines 611-612), after all candidates are
  constructed and executed. Construction-phase `trace_add`
  calls (lines 591, 600) record only (template, index, value).
- The masked bit (`flags&1`) is never consulted in
  `mp_build` (only bits 1 and 2 drive the disable flags).
- The query node stores `expected` at pay2 (line 582), but
  the query node is never passed to either constructor.

There is no code path by which `expected` can reach candidate
construction. The F2 byte-identical-trace property is
structurally guaranteed. Independently confirmed: three
full binary runs produce byte-identical output (`cmp` clean).

Note: `mp_build_compose` gates composition on executed values
(`v!=-2 && v!=-999999`). These values come from `exec_plan`,
not from `expected`. Using execution results to guide search
is legitimate under the e-ruling, which constrains
`expected` specifically.

## Vector 4: Bootstrap budget - ATTACK-SUCCESS (process-level)

The fenced bootstrap section contains exactly 157 code lines
(non-blank, non-comment), against the prereg bound of 150.

The prereg (`4f6f0c5c8`, PREREG_COMP1.md) states:

- "Cognition source lines added: projected at most 150"
- "cognition source lines (bound 150)"
- "growth past the bound without a fresh prereg fails review"
- K1 incorporates "the One-System accounting bound" by
  reference.

No fresh prereg was written for the 157-line actual. The
BUILD_REPORT reframes the overage as "a +7 variance on a
projection, not a kill-bar failure." The prereg's own
language is stronger than that: it uses the word "bound"
three times and says growth past it "fails review."

This is a process deviation, not a scientific invalidation.
The 7 extra lines (4.7%) sit in `mp_run`'s promotion block
and change no capability claim, no template count, and no
architectural metric. But the red team records it honestly:
the bound was exceeded without the fresh prereg the frozen
spec requires.

Recommendation: file a prereg amendment documenting the
157-line actual, or trim 7 lines from the fenced section.
Do not silently reframe a stated bound as a mere projection.

## Vector 5: Determinism - ATTACK-PASS

Three independent executions of `comp1_bin`: 10/10 tests pass
on every run, outputs byte-identical (`cmp` clean across all
three pairs).

## K1/K2/K3 spot-check

- K1 (prereg ordering): PASS. `git merge-base --is-ancestor`
  confirms `4f6f0c5c8` is an ancestor of `170e39424`.
- K2 (architecture): PASS by inspection. Zero handlers,
  zero semantic cases, zero modes, zero bridges, exactly
  three templates, candidates from subject-incident
  relations only.
- K3 (pure Zag): PASS. No Python or other languages in the
  build path observed.

## Bottom line

The scientific claims under attack all hold: three templates
plus genuine plan-structure composition, a structurally
enforced e-ruling, and deterministic 10/10 behavior. The
single finding is process-level: the 150-line bootstrap
bound was exceeded by 7 lines without the fresh prereg the
frozen spec requires. BUILD-PASS stands; recommend the
prereg amendment before any SURVIVES consideration.
