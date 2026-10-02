# COMP-1 Build Report

## Verdict: COMP1-BUILD-COMPLETE

Implementation of the COMP-1 compositional machinery per frozen prereg
`4f6f0c5c8`. All kill bars pass. Test battery 10/10. Byte-identical
determinism across 3 runs.

## Kill bars

- **K1 (prereg commit order):** PASS. Prereg commit `4f6f0c5c8` verified as
  ancestor of HEAD via `git merge-base --is-ancestor` before implementation
  and re-verified at build completion (HEAD `e98a976a0`).
- **K2 (architecture):** PASS by source inspection. Zero task-specific
  handlers, zero new hardcoded semantic cases, zero modes, zero bridges,
  zero new core execution operations. Exactly three frozen templates
  (CHAIN-2, GATHER-n, ITERATE-UNTIL). Candidate plans built exclusively
  from subject-incident relations (`incident_fill` is the sole relation
  source; `mp_build` and `mp_build_compose` take no other relation input).
- **K3 (pure Zag):** PASS. All research logic in `comp1.zag`. Shell used
  only to invoke znc, run the binary, and do git/move operations. The
  Step 0 toolchain guard is recorded in NAMECHECK.md (python/python3
  stubbed to exit 127; `which python3` resolves to the stub).

## Predictions (prereg P1-P5)

- **P1:** T1 two-hop query answers via CHAIN-2. PASS.
- **P2:** T2 GATHER-3 with a supplied ADD combining structure answers 60.
  T2b confirms GATHER declines without a combining structure. PASS.
- **P3:** T3a grandparent via CHAIN-2; T3b depth via ITERATE-UNTIL counter.
  PASS.
- **P4:** T4 3-hop query answers via plan-structure composition
  (CHAIN-2 extended by one READ). The selected plan carries template
  marker 4 (COMPOSED); no fourth template was added. PASS.
- **P5:** T5 separation. Exact-key hits return without firing the
  miss-policy (trace empty); no combining structures induced. PASS.

## Falsification checks

- **F2 (e-ablation):** Three runs over identical teaches. Unmasked with
  expected=201 selects 201; unmasked with expected=202 selects 202;
  masked with expected=202 falls back to first non-sentinel (201). All
  three construction traces are byte-identical. `expected` changes
  selection only, never construction. The candidate builders
  (`mp_build`, `mp_build_compose`) do not take `expected` as a parameter.
  PASS.
- **Template ablations:** Disabling ITERATE-UNTIL makes T3b fail while T1
  still passes; disabling CHAIN-2 makes T1 fail. Each template carries
  its predicted load. PASS.
- **F5:** Exactly three templates. Composition uses template marker 4
  (COMPOSED) for plan-structure concatenation, not a new template. PASS.
- **F6:** Candidates from subject-incident relations only; composition
  extends using relations incident on the executed intermediate. PASS.
- **F7:** Zero new core execution ops. Plan steps use READ (ISA-blessed),
  MOVE/BRANCHEQ/INC (frozen ISA), EMIT (output convention), APPLY
  (combining-structure convention named in the prereg). PASS.

## E-ruling implementation

`expected` is post-hoc feedback. Construction (`mp_build`,
`mp_build_compose`) is fully determined by the templates and the
subject-incident relations before `expected` is consulted. Selection:
unmasked, first candidate whose output equals `expected`; masked, first
non-sentinel output. Promotion (SUPPORTS/USE edges, verified-plan
record) occurs only on unmasked verification.

## One-System accounting

- Cognition source lines added: 157 for the bootstrap miss-policy
  (fenced section) vs the prereg projection of at most 150. This is a
  +7 variance on a projection, not a kill-bar failure (K1/K2/K3 govern
  the verdict). Supporting machinery: plan-structure constructors,
  generic executor, workspace helpers, test battery.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New task-specific handlers: 0. New core execution ops: 0.
- Learner-state structures created: plan nodes, step nodes, SEQ edges,
  query records, SUPPORTS/USE edges on verification. All are node/edge
  conventions in the single CLA-2 workspace; no new state formats.

## Determinism

Binary run 3 times; outputs byte-identical (`cmp` clean). 10/10 tests
pass on every run.

## Files

- `comp1.zag`: the implementation (pure Zag).
- `comp1_bin`: compiled binary (pinned znc `abed8aa1`).
- `NAMECHECK.md`: Step 0 toolchain guard and frozen-input record.
- `BUILD_REPORT.md`: this file.
