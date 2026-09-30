# CAUSAL-EDITINVENT Results

Implementation of prereg 811fc06c9. Executed 2026-09-30 ~08:20 PDT.

## Verdict: CAUSAL-EDITINVENT-PASS

All frozen predictions held. Ceiling: L2+ with learner-authored revision
vocabulary (NOT L3; C0-A..D require more).

## Predictions vs Observed

- P0: W0=[(0,1,1)] (n_graphs=9 n_classes=2). OBSERVED: [(0,1,1)], 9 graphs, 2 classes. PASS.
- P1a: V_old BFS k=-1. OBSERVED: k=-1. PASS.
- P1b: old-envelope E3-consistent count=0. OBSERVED: 0. PASS.
- P1c: diagnose prints max_rules->3: 0/220, delay->3: 13/171, binding=delay_max.
  OBSERVED: exact. PASS.
- P1d: invent prints "EXTEND-DELAY installed, dmax 2->3". OBSERVED: exact. PASS.
- P1e: extended BFS k=1, W1=[(0,1,3)]. OBSERVED: k=1, [(0,1,3)]. PASS.
- P1f: W1==G3 (1). OBSERVED: 1. PASS.
- P2a: Phase2 k=0. OBSERVED: 0. PASS.
- P2b: KEEP printed. OBSERVED: KEEP. PASS.

## Kill bars

- B1: 3/3 byte-identical stdout from fresh compiles. SHA256:
  d07158929401bc60fba5d4956ba338866984d28a86bed92b714bfcfbdcf8c304
  (all three runs). PASS.
- B2: audit_edit.sh passes A1-A5. PASS.
- B3: check_no_dash.sh passes on editinvent.zag, audit_edit.sh. PASS.
- B4: prereg 811fc06c9 is ancestor of impl commit (verified via
  git merge-base --is-ancestor). PASS.
- B5: Capability-source delta recorded below; 0 new modes/bridges/handlers. PASS.

## Architecture delta (ONE-SYSTEM RULE)

- Cognition source lines added: ~650 (editinvent.zag delta on 836-line
  causal_revert.zag base; much is verbatim-copied substrate).
- New hardcoded semantic cases: 0.
- New modes: 0 (single learner trace; no INVENT/OLD/FROZEN modes).
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created:
  - dmax (runtime delay-domain variable, init 2, persistent).
  - EXTEND-DELAY edit operation (constructed by learner via invent(), not in source).
- Capability-source delta: the invention capability derives from experience
  (E3 inconsistency pattern) + generic diagnose-and-relax machinery. No new
  hardcoded edit was added to source.

## The invented edit type

EXTEND-DELAY: a second-order edit operation that modifies the edit vocabulary
itself (dmax 2->3), constructed by the learner after:
1. Exhaustive V_old failure (k=-1).
2. Runtime proof of insufficiency (0/78 old-envelope graphs E3-consistent;
   with the V_old invariant, proves no k-edit sequence reaches consistency).
3. Residual pattern analysis (required arr[Y]=3 > max delay 2).
4. Generic diagnosis (max_rules->3: 0/220; delay->3: 13/171; binding=delay_max).

The specific value 3 was computed (dmax+1), never a literal in the edit path.
Source audit (audit_edit.sh) proves the type absent from source.

## Standing question

"Why can the existing general architecture not learn this behavior?"

The existing causal-lane architecture (causal_revert.zag) has a FIXED edit
vocabulary with a hardcoded delay domain {1,2}. When the law changes to require
delay-3, the architecture can detect the failure (inconsistency) but has no
general cognitive operation for "diagnose which representational parameter binds
and extend it." What is missing as a general operation: a meta-cognitive
diagnose-and-relax loop that (a) treats the learner's own representational
envelope as an object of analysis, (b) tests minimal relaxations of envelope
parameters against the failure pattern, and (c) constructs a new edit operation
along the binding parameter. This is not a benchmark handler; it is the
general operation of "revise your own revision machinery." The current work
demonstrates it for one parameter (delay_max); the general form would cover
any enumerable envelope parameter.
