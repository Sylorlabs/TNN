# PREREG: DDES L3 Gap Analysis (A1 Architecture-Adversary)

Frozen before any analysis text. Pure documentation. No Python. No em dashes.

## Task

Determine what DDES would need to achieve L3, against the mandatory
Criterion 0 (four conjunctive requirements):

- C0-A runtime-defined semantics: semantics of the new cognitive object
  reside in learner-created persistent state; source contains only
  generic execution/construction machinery, no dedicated semantic case.
- C0-B open structural form: learner constructs variable-sized/growing
  structures incrementally, not one complete answer from a finite
  researcher-enumerated family.
- C0-C multiple unforeseen forms: freeze the learner, then an independent
  adversary designs materially different sealed families after the freeze;
  at least one evaluation family must be adversary-designed post-freeze.
- C0-D cognitive reuse: the invented structure improves transfer,
  prediction, procedure learning, causal inference, memory, planning,
  or sample efficiency.

## Kill bars

- K1: L3 gap analysis documented. For each of C0-A through C0-D, name
  exactly which element of the frozen DDES source (ddesr.zag @ 17c97a2cd,
  repaired binary; generalize work @ 843c45fee for reference) fails it,
  with line-level or function-level specificity. Quote the source.
- K2: A learner-derived action-effect model design is specified in
  concrete terms: what state the learner keeps, what probe experience it
  runs, how it induces the code-to-effect map, and how synthesis then
  uses the induced map instead of researcher arithmetic. Must be
  falsifiable in principle (name an experiment that would show the
  learner failing to induce the map).
- K3: Assessment of incremental vs fundamental: argue whether the K2
  design is an extension of DDES or a replacement architecture, and
  whether the result would still be DDES. Reasoning must reference the
  specific functions that would survive vs be replaced.

## Scope rules

- Analysis only. No implementation, no Zag changes, no benchmark runs.
- Judge the frozen repaired source as it exists (17c97a2cd), using the
  generalization result (843c45fee) only as evidence of where
  researcher authority lives.
- No new C0 semantic cases, thresholds, or world definitions are
  introduced here.
- Adversarial posture: assume the L3 claim is false; look for the
  structural reason it cannot hold, not the minimal patch.
