# CAUSAL-EDITINVENT Preregistration (ONE-SYSTEM-RULE compliant)

Preregistered 2026-09-30 ~08:15 PDT by the CAUSAL-EDITINVENT worker (subagent of the
research-coordinator). This prereg strictly precedes implementation. Verify:
`git merge-base --is-ancestor <prereg-commit> <impl-commit>` must be true.

Related: `NAMECHECK.md` (worker name check). Parent result: CAUSAL-REVERT-PASS
(prereg `c09afd95e`, amendment `ab68dd121`, impl `da0cd17b6`).

## 0. ONE-SYSTEM RULE compliance (standing directive, Micah 2026-09-30)

This work does NOT create a new Zag subsystem, mode, bridge, or handler. It is a
DELTA on the existing causal-lane learner (`causal_revert.zag` at `da0cd17b6`):
one continuing learner that, through EXPERIENCE (a law change), produces NEW
LEARNED STATE (an authored edit operation). There are NO modes (no
INVENT/OLD/FROZEN); the old-vocabulary failure, the insufficiency proof, the
diagnosis, and the invention are sequential steps in a single learner trace.

Capability-source delta (frozen record):
- Cognition source lines added: TBD at impl (estimated <150 on the 836-line base).
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: `dmax` (runtime delay-domain variable, init 2);
  the EXTEND-DELAY edit operation (constructed by the learner, not in source).
- Capability-source delta: the invention capability comes from experience (E3)
  + generic diagnosis machinery, not from new hardcoded edits.

## 1. Goal

Make the REVISE edit vocabulary itself learner-authored. The missing piece for a
genuine L3-revision claim (parent context): in CAUSAL-REVERT-PASS the revision
trigger, the KMAX bound, the consistency criterion, and the edit vocabulary
(change-delay / add-rule / remove-rule, delays in {1,2}, at most 2 rules) were all
researcher-supplied. This work targets exactly one of those: the edit vocabulary.

Concretely: the learner must derive a NEW structural edit operation from an
observed inconsistency pattern (exhaustive failure of the old vocabulary), where
the new operation does not exist in source and a source audit proves it.

## 2. Substrate (inherited, unchanged)

Graph model from `causal_revert.zag` (commit `da0cd17b6`): 32-byte slots
(nr, src[2], dst[2], delay[2]); variables X=0,Y=1,Z=2; 12 rules (src!=dst,
delay in {1,2}); 78 graphs; min-arrival Bellman-Ford behavioral signature;
consistency = passive-evidence prediction match. Pure Zag, pinned znc.

The OLD (researcher-supplied) edit vocabulary V_old, frozen:
- change-delay: set a rule's delay to any value in {1,2} except current
- add-rule: add a rule from the 12 delay-{1,2} rules, gated nr<2
- remove-rule
- KMAX=3 BFS. Invariant: every V_old edit preserves (delays subset of {1,2})
  and (nr<=2). Hence any k-edit sequence stays inside the 78-graph old envelope.

## 3. Pre-prereg exploratory findings (allowed; implementation not yet written)

Exploratory Zag programs in /tmp (never committed) established, observed
2026-09-30 ~14:56-15:05 UTC:
- F1: All 220 3-rule graphs (delays {1,2}) have behavioral signatures inside the
  15-signature set of the <=2-rule envelope. Zero 3-rule-only signatures. Under
  min-arrival semantics the 3rd rule is always behaviorally redundant. Therefore
  rule-count/capacity extension is DEAD as the invented edit type: no evidence
  can provably require 3 rules. (Design pivot recorded here, not after results.)
- F2: Delay-3 adds 13 new behavioral signatures (28 vs 15). Delay-domain
  extension is behaviorally load-bearing.
- F3: C-not-A (delay<=3 envelope minus old envelope) has 13 signatures,
  including sig=3999 = (Y=3, Z=INF) from [(X->Y,3)].
- F4: Candidate evidence E3 = {(Y,2)=0,(Y,3)=1,(Z,3)=0}: ZERO of the 78
  old-envelope graphs are E3-consistent; [(X->Y,3)] IS E3-consistent.
- F5: Diagnosis counts: max_rules->3 relaxation yields 0/220 E3-consistent
  graphs; delay->3 relaxation yields 13/171 E3-consistent graphs.
- F6: From W0=[(X->Y,1)] with delay domain {1,2,3}, the k=1 neighborhood's ONLY
  E3-consistent graph is [(X->Y,3)] (change-delay 1->3). No add-rule or
  remove-rule neighbor is consistent.
- F7: (X->Y,1) is the UNIQUE 1-rule E0-consistent graph for
  E0={(Y,1)=1,(Y,2)=1,(Z,2)=0}.

Design decision (from F1): the invented edit type is DELAY-DOMAIN EXTENSION
(EXTEND-DELAY), derived via a generic diagnose-and-relax meta-procedure.
Split-rule and intermediate-variable edits were considered and rejected
(behaviorally redundant under min-arrival semantics / ungroundable latent).

## 4. The frozen law-change family R3

Phases [G0, G3, G3] (law changes once, then stays; tests invention then stability).
- G0 = [(X->Y,1)], E0 = {(Y,1)=1,(Y,2)=1,(Z,2)=0}.
- G3 = [(X->Y,3)], E3 = {(Y,2)=0,(Y,3)=1,(Z,3)=0}.
G3 is OUTSIDE the old envelope (F4). E3 is the inconsistency pattern.

## 5. The learner-authored edit-type design (frozen)

Single learner trace (no modes). The program `editinvent.zag` (delta on
`causal_revert.zag`) runs:

### Phase 0: construct on E0, dmax=2.
Winner W0 = [(X->Y,1)] (F7).

### Phase 1: E3 arrives. The learner:
1. FAIL_OLD: V_old BFS (dmax=2, KMAX=3) from W0 returns -1 (no consistent graph).
   (This IS the old-vocabulary control, inline; no separate mode.)
2. PROVE: `prove_insufficient` (exhaustive 78-graph check, dmax=2) prints
   `old-envelope E3-consistent count=0`. With the V_old invariant (Sec.2), this
   PROVES no k-edit sequence in V_old, for ANY k, reaches consistency.
3. PATTERN: print residual analysis. From E3 derive required arrival intervals:
   arr[Y]=3 (from (Y,2)=0,(Y,3)=1), arr[Z]>=4 (from (Z,3)=0). Note max
   expressible single delay (2) < required arrival (3).
4. DIAGNOSE (diagnose-and-relax): for each envelope parameter in the frozen
   scope {max_rules, delay_max}, test the MINIMAL relaxation for E-consistency
   by exhaustive enumeration:
   - max_rules 2->3 (delays<=2): count E3-consistent among 220 3-rule graphs.
   - delay_max 2->3 (rules<=2): count E3-consistent among 171 graphs.
   Print both counts. The BINDING parameter is the one whose relaxation yields
   consistency while the other does not.
   Scope disclosure: variable-invention (n_vars 3->4) is EXCLUDED from scope
   (a 4-variable graph would satisfy E3, but inventing a latent variable
   requires grounding machinery that does not exist). Disclosed limitation.
5. INVENT: construct the edit operation along the binding parameter. For
   binding=delay_max: install EXTEND-DELAY, setting the runtime `dmax` from 2
   to (2+1)=3, computed, never a literal. This is a SECOND-ORDER edit: V_old
   edits graphs; EXTEND-DELAY edits the vocabulary. The new operation persists
   as learner state.
   If binding=max_rules (not the case in R3), report BINDING-NOT-CONSTRUCTIBLE
   (honest stop).
6. RESOLVE: extended BFS (dmax=3, KMAX=3) from W0 returns k=1, winner
   W1=[(X->Y,3)] (F6). Assert W1 equals the true law G3.

### Phase 2: E3 again.
Extended BFS from W1 on E3 returns k=0 (already consistent), prints KEEP.
W2=W1=[(X->Y,3)] (invented vocabulary persists; no snapback).

### 5b. Invented-vs-retrieved signature (frozen audit criteria)

The source `editinvent.zag` MUST satisfy (checked by `audit_edit.sh`, shell):
- A1: `dmax` is a runtime variable initialized to 2; the ONLY store to `dmax`
  after init is inside `invent`, and the stored value is computed as dmax+1
  (no literal 3 assigned to dmax).
- A2: `neighbors` (the edit vocabulary) takes dmax as a parameter; no delay
  literal 3 appears in any rule-construction path reachable from `neighbors`.
  (The diagnostic enumerator uses delays up to 3 in clearly-marked WHAT-IF
  analysis code, unreachable from the edit path; the audit whitelists it by
  function name.)
- A3: No pre-built [(X->Y,3)] graph literal; no function named
  add_delay3 / extend_delay / delay3 anywhere in source.
- A4: `diagnose` tests BOTH max_rules and delay_max (grep shows both
  enumerations); the binding is selected by the counts, not by family ID
  (no branch on R3 / phase / evidence literal selecting "delay").
- A5: `prove_insufficient` is called on V_old failure before `diagnose`.

## 6. Frozen predictions (exact)

- P0: Phase 0 winner W0 = [(X->Y,1)].
- P1a: V_old BFS returns -1.
- P1b: `prove_insufficient` prints `old-envelope E3-consistent count=0` (0/78).
- P1c: `diagnose` prints `max_rules->3: 0/220` and `delay->3: 13/171`,
  binding=delay_max.
- P1d: `invent` prints `EXTEND-DELAY installed, dmax 2->3`.
- P1e: extended BFS returns k=1, winner W1=[(X->Y,3)].
- P1f: W1 equals G3.
- P2a: Phase 2 extended BFS returns k=0, prints KEEP.
- P2b: W2=W1=[(X->Y,3)].

## 7. Kill bars (frozen)

L3-EDIT-PASS iff ALL hold:
- B1: P0, P1a-P1f, P2a-P2b print exactly as predicted (byte-identical stdout
  across 3/3 runs from fresh compiles).
- B2: `audit_edit.sh` passes A1-A5 (invented type absent from source).
- B3: `check_no_dash.sh` passes on all committed loop docs (no dashes).
- B4: Prereg commit strictly precedes impl commit
  (`git merge-base --is-ancestor` true).
- B5: Capability-source delta recorded (Sec.0) with 0 new modes/bridges/handlers.

L3-EDIT-FAIL iff any of: a prediction mismatches; `diagnose` binds max_rules
or none; `invent` fires without `diagnose` binding delay_max; audit fails;
non-determinism across the 3 runs; impl commit not a descendant of prereg;
or a new mode/bridge/handler is added (ONE-SYSTEM RULE violation).

Honest ceiling (frozen): PASS demonstrates a learner-authored edit TYPE
derived from an inconsistency pattern with a provable-insufficiency result.
It does NOT claim L3 (C0-A..D all four are required; this work addresses only
the edit-vocabulary piece of L3-revision). A PASS is reported as
CAUSAL-EDITINVENT-PASS with ceiling "L2+ with learner-authored revision
vocabulary", not as L3.

## 8. What this does NOT do (disclosed)

- Does not invent the consistency criterion, KMAX, or revision trigger
  (still researcher-supplied; the remaining L3-revision gaps).
- Diagnosis scope is {max_rules, delay_max}; variable-invention excluded (Sec.5).
- max_rules binding has no implemented constructor (would report
  BINDING-NOT-CONSTRUCTIBLE); R3 is constructed so delay_max binds.
- Single law-change family R3; no adversary-designed second family (C0-C
  needs that; future work).
- This is a causal-lane experiment, not the ONE-SYSTEM target architecture;
  the delta is kept minimal per Sec.0.
