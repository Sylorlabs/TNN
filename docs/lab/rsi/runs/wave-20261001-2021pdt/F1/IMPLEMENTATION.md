# IMPLEMENTATION.md - F1 generic executable semantics candidate

Lane F1, wave wave-20261001-2021pdt. Implementation turn 2026-10-01 ~20:34 PDT.
Status: IMPLEMENTATION COMPLETE. READY FOR SEALED EVALUATION.

## 1. What was built

A standalone candidate experiment implementing prereg PREREG_F1.md section 7,
in pure Zag, compiled by the pinned znc. Two candidate sources in `impl/`:

- `impl/f1_isa.zag` (405 lines): frozen protected ISA substrate. Executable
  vocabulary in created graphs: READ, WRITE, COPY, ADD, EQ, BRANCH, EXECUTE
  (EXECUTE(root, frame) is approved protected-core machinery). Contains only
  generic execution and storage machinery: u8-backed i64 cell storage,
  node/graph/learner-state containers, the EXECUTE interpreter (sequential
  nodes, BRANCH control, step cap 500, call-depth cap 8, EXECUTE composition
  over learner-named graphs), text serialization of learner-created state,
  and text parsing helpers. No domain semantics, no task knowledge, no
  researcher-named semantic cases, no reification schema, no candidate family.
- `impl/f1_learn.zag` (487 lines): the incremental constructor. Experience
  loop: predict with EXECUTE(main, frame), monitor own prediction failures,
  on K1=2 consecutive failures run a construction burst (up to KB=4 events):
  deterministic trial over single-ISA-element insertions placed before the
  terminal WRITE node, committing the first strictly-improving move in frozen
  ISA order over runtime registers and frame slots. Each event logged with
  its episode index in the white-box trace. On trigger with no improving move
  and node cap MAXN=24 reached, the learner snapshots the old graph under a
  learner-chosen name and restarts from the seed (revision by supersession).
  Created structures persist in learner-created state files; the trace logs
  every episode, trigger, construction event, stall, supersession, and
  per-structure execution counts.

Dev scaffolding in `dev/` (663 lines total): `f1_devgen.zag` (world
generator), `f1_score.zag` (accuracy, memorizer baseline, EXEC counts,
structural signatures), `f1_ncmenu.zag` (NC-A menu control),
`f1_nckit.zag` (NC-B finite-kit control), `f1_testexec.zag` (interpreter
machinery unit test), `run_dev.sh` (full dev battery).

Frozen binary protocol for the sealed harness:
`f1_learn <episodes> <state_in|-> <state_out> <trace> <pred>`
Episode lines: `<x0> [<x1> ...] <y|?>` (`?` masks truth: prediction only).

## 2. Binary hashes (3/3 byte-identical builds, sha256)

| binary | sha256 |
|---|---|
| f1_learn | 0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727 |
| f1_devgen | 05edc211b6fb46e1fa4408e85c7d595ac77a9399f4d75336f09e1cb8e3c434ee5143cbe692b32180f20 |
| f1_score | 18f4166b93bb1bbba2ba128b37826309e1cb8e3c434ee5143cbe692b32180f20 |
| f1_ncmenu | c4ba04fe83a89db8bce6b40b3313df6f4ee57ed79232b1c6522435df6f4ee5238dc |
| f1_nckit | b02af2d2dcbce1e9f3fccad3a397ef3e4a1994cc16481a1ec4d2eb8995733a83 |
| f1_testexec | d5e17169772dc3d87faa5f1ecec132a686144ee6c7609b148c4b1830580238dc |

Binaries live in `dev/bin/`. Rebuild reproducibility was verified by three
independent builds with cmp (all identical) before recording hashes.

## 3. Development results (builder's own fixtures, not sealed data)

World D1 (y=2x), 10 train episodes x=0..9:
- T1 experience: 1 construction event at episode 2
  (`ADD r0,f0,f0`, buffer err 6 -> 0). Final graph: [ADD r0,f0,f0, WRITE r0].
  Creation trace in learner state; 0 stalls; 0 supersedes.
- T2 hidden (x=10..19, truth masked, trained state): 10/10 = 100%.
- T3 ablation (hidden, fresh seed-only state): 0/10. Drop = 100 points.
- T4 memorizer control (exact-match table, same example budget): 0/10.
- T5 transfer (x=-9..-1, changed surface, trained state): 9/9 = 100%;
  reuse-invocation EXEC main = 9 (> 0).

Revision:
- T6a counterexample (y=3x, loading D1 state): 1 construction event
  (`ADD r0,r0,f0`, err 3 -> 0); revised graph [ADD r0,f0,f0, ADD r0,r0,f0,
  WRITE r0]; contra-hidden (x=10..19): 10/10 = 100%. Old nodes retained in
  state; trace explains the revision.
- T6b law change inside one run (dbl then tpl, 20 episodes): 2 constructs,
  3 stalls during the transition (no improving single move on the mixed
  buffer; honest stall, no fake progress), then revision to 3x. Final graph
  computes 3x exactly.

Stress / lifecycle:
- T7 alternating law 2x/5x every 3 episodes, 30 episodes: 15 constructs,
  9 stalls, 0 supersedes (cap not reached). Thrash is reported, not hidden.
- T7-extended, same law, 150 episodes (reproducible via
  `bin/f1_learn work/d3b_alt.ep - work/d3b_state.txt work/d3b_trace.txt
  work/d3b_pred.txt`): 60 constructs, 49 stalls, 2 supersedes
  (ep 46: main -> g0; ep 112: main -> g1). After the first supersession the
  trial committed `EXECUTE r0, g0` nodes: the new structure reuses the old
  named structure compositionally (EXEC g0 = 525). After the second
  supersession EXEC g1 = 0: the superseded structure is not executed after
  supersession (clean K-REV lifecycle evidence). Runtime ~2.5 min wall on
  this pathological input; tens-of-episodes runs take seconds.

Determinism:
- T8: reran T1+T2; state, trace, and hidden predictions byte-identical
  (cmp). Full battery rerun after each source change also byte-identical
  (see section 6 deviations). Zero randomness in decision paths.

Machinery unit test (`f1_testexec`, hand-built graphs probing the
interpreter only, not claimed as learner invention): 5/5 CHECKs pass
(EXECUTE composition 3x=15, BRANCH skip, BRANCH fallthrough, step-cap
termination of a runaway loop, unknown-name EXECUTE safe no-op).

## 4. Control outcomes

- C1 menu-selection control (NC-A, `f1_ncmenu.zag`): picks menu_f0 on D1
  train, scores 10/10 on D1 hidden behaviorally. The K-C0A-style audit over
  its source flags exactly the kill sites: three researcher-written semantic
  cases (menu_f0/menu_f1/menu_f2, lines 10-12), the fixed-order scan over the
  researcher-enumerated family (line 29), and the reification of the menu
  choice (line 58). Teeth demonstrated: behavioral success does not save it.
- C2 enumerated-family control (NC-B, `f1_nckit.zag`): kit whose only output
  is the single researcher-fixed shape `(x == K) ? 1 : 0` with a frozen
  ascending rank. Scores 10/10 on its home world (eq, K=3 found) and 0/10 on
  D1. Source shows every kit output is an instance of the one fixed shape
  (kit_emit, line 16) selected by the frozen rank (line 28): the K-C0B
  automatic-kit kill fires on inspection alone. Teeth demonstrated.
- C3 reuse teeth: `f1_score exec` on the transfer trace for the superseded
  g1 reports EXEC g1 = 0, so the K-C0D zero-executions check fires on a real
  named structure. The candidate's own transfer run shows EXEC main = 9
  (check passes when the structure is genuinely reused).

## 5. K-C0A source-audit self-check (candidate impl/)

- grep for forbidden protected semantics
  (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE,
  FIND_THRESHOLD, MAKE_CONDITIONAL): zero hits.
- grep for downgrade kill-pattern markers (COUPLED, COND(, SPECIALIZE,
  REIFY, SPLIT_SCAN) and researcher-named node type tags / semantic
  branches / menu / kit functions: zero hits in `impl/`.
- The only tag-dispatched sites are the ISA op dispatch in the interpreter
  (`f1_isa.zag` op_name lines 99-105, f1_exec from line 292): generic
  execution machinery over the frozen ISA, explicitly permitted by the
  prereg ("source holds only generic execution and construction machinery").
- K-C0B positive-evidence analog: the final D1 structure's serialized
  pattern `N 4 0 8 8 0 0;N 2 0 0 0 0 0;` has zero textual counterparts in
  `impl/` sources (grep count 0 in both files).

## 6. Deviations from the frozen prereg

All within section 7 design constraints; none touch bars or trigger
constants:

1. Insert-before-terminal-WRITE invariant: new nodes are inserted before the
   final WRITE node rather than appended after it (appending after WRITE
   would leave WRITE dead). Disclosed generic machinery, like a calling
   convention; not a semantic template.
2. Burst used to log a spurious STALL after solving the buffer (err 0);
   fixed to return quietly. Verified by trace inspection.
3. Two performance-only changes (early-abort bound in trial evaluation;
   hoisted register/frame scratch buffers): provably semantics-preserving
   (abort only when a candidate provably cannot strictly beat the best).
   Verified empirically: full dev battery outputs byte-identical before and
   after each change (8/8 artifacts cmp-identical).
4. EXECUTE of main (nameid 0) is a guarded no-op in the interpreter; the
   trial only generates EXECUTE over snapshot names 1...

No deviation in: trigger constants (K1=2, KB=4, MAXN=24, BUFN=8, all
disclosed in source), frozen ISA membership, one-element-per-event growth,
no enumerated families, no researcher semantic cases.

## 7. Architecture accounting (prereg section 11)

Baseline: prereg freeze commit 27ef14078 (implementation files first appear
after it; verified: impl/ and dev/ are untracked new directories).

- Cognition-substrate source lines added: 0. No file outside the lane was
  touched; all writes are inside
  `docs/lab/rsi/runs/wave-20261001-2021pdt/F1/`. The candidate is a
  standalone experiment per prereg section 1, not a substrate modification.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New routers: 0. New task-specific handlers: 0.
- Constructed graphs use only the frozen ISA ops listed in section 1.
- New candidate source: 892 lines (405 + 487) in `impl/`; dev scaffolding
  663 lines in `dev/`. Capability demonstrated (doubling, revision,
  supersession, compositional reuse) comes from learner-created state, not
  from added substrate semantics: the D1 final graph's doubling behavior
  exists nowhere in source (section 5).

## 8. Honest boundaries

- Bounded L2+ ceiling stands: nothing here is claimed as L3. The four C0
  clauses are for the independent adversary to test on post-freeze sealed
  worlds; development data establishes no generality.
- Known limitations: greedy depth-1 trial with no lookahead (stalls honestly
  when no single-element move improves); dev worlds did not require BRANCH
  or EQ discovery by the learner (interpreter paths are unit-tested, learner
  discovery of control flow is untested); no dead-code elimination, so
  structures bloat under nonstationarity (T7-extended shows redundant
  EXECUTE stacking, each step locally improving); the trial's candidate
  order over the frozen ISA is fixed and disclosed.
- The sealed adversarial family (K-C0C), the K-C0B menu-equivalence attack,
  K-C0D transfer, and K-REV counterexample families come from the
  independent adversary after freeze. The builder has not seen sealed
  worlds. BUILD-PASS is not promotion; VOID is terminal.

## 9. Verdict for this turn

IMPLEMENTATION COMPLETE. READY FOR SEALED EVALUATION. No blockers.
The frozen binary is `dev/bin/f1_learn`
(sha256 0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727);
the implementation-freeze commit (coordinator's step) should record these
hashes. Dev logs: `dev/work/dev_battery.log`; traces, states, predictions,
and episode fixtures in `dev/work/`.
