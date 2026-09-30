# CAUSAL-EDITADV Preregistration (C0-C attack on CAUSAL-EDITINVENT)

Preregistered 2026-09-30 by the Causal Edit-Invention Adversary (subagent of
the research-coordinator). This prereg strictly precedes implementation.
Verify: `git merge-base --is-ancestor <prereg-commit> <impl-commit>` is true.

Step 0 name-check: `STEP0_NAMECHECK.md` (written before any other work).

Target: CAUSAL-EDITINVENT-PASS (prereg `811fc06c9`, impl `4c233f82a`).
Claim under attack: the diagnose-and-relax meta-procedure is a GENERIC
procedure for revising the revision vocabulary, scoped over envelope
parameters {max_rules, delay_max}. Worker recommendation under test:
"does diagnose-and-relax generalize beyond delay_max or reveal its
boundary?" ONE-SYSTEM RULE: this attack adds no semantic case, mode,
bridge, or handler; it tests the generality of the existing mechanism.

## 1. Frozen mechanism understanding (from 4c233f82a)

`diagnose(E)`: c_mr = E-consistent count among 220 3-rule delay<=2 graphs;
c_dl = E-consistent count among 171 <=2-rule delay<=3 graphs.
binding=2 iff c_dl>0 and c_mr=0; binding=1 iff c_mr>0 and c_dl=0; else 0.
`main`: binding==2 installs EXTEND-DELAY (dmax+1); otherwise prints
`BINDING-NOT-CONSTRUCTIBLE` and stops (no constructor exists for max_rules).

Reachability: diagnose is reached only after FAIL_OLD (V_old BFS, KMAX=3,
returns -1) and prove_insufficient=0. From a 1-rule W0 every <=2-rule graph
is <=3 edits away (add+remove per rule), so FAIL_OLD holds iff c_old=0,
where c_old = E-consistent count among the 78 old-envelope graphs.

## 2. Pre-prereg exploratory findings (/tmp only, never committed)

- F1: old envelope: 78 graphs, 15 behavioral signatures. Matches prereg F2.
- F2: 220/220 3-rule (delays<=2) graphs have signatures inside the old
  15-signature set. Zero 3-rule-only signatures. S_mr subset of S_old,
  verified computationally (independent re-verification of prereg F1).
- F3: delay-3 envelope: 171 graphs, 28 signatures. Matches prereg F2.
- F4: sweep over 49 evidence cells E(arrY,arrZ)={(Y,arrY-1)=0,(Y,arrY)=1,
  (Z,arrZ-1)=0}, arrY in 1..7, arrZ in 2..8: in EVERY cell, c_mr>0 implies
  c_old>0; binding=1 occurs in ZERO cells; binding values are in {0,2} only.
  binding=2 in exactly 11 cells (delay-only region); binding=0 in 38.
- F5: E_B={(Y,6)=0,(Y,7)=1,(Z,7)=0} (needs arrY=7: 3-hop chain, 4-variable
  territory, outside {max_rules,delay_max}): c_old=0, c_mr=0, c_dl=0,
  binding=0.

## 3. Design pivot (recorded here, before implementation)

The brief asked for "a law change where max_rules binds". F2+F4 prove this
family CANNOT be constructed: any E consistent with a 3-rule graph is
consistent with an old-envelope graph (signature-subset), so c_old=0 implies
c_mr=0 for ALL E, and diagnose (reached only when c_old=0) can NEVER return
binding=1. Family A therefore becomes the impossibility proof plus the
unreachability demonstration, not a binding construction. Likewise Family C
(ambiguity) is provably unreachable: it needs c_mr>0 with c_old=0.

## 4. Attack families (frozen)

Shared harness: each driver = lines 1-617 of the 4c233f82a blob
(everything before `fn main`) VERBATIM + a new attack main. The mechanism
functions (diagnose, invent, revise_dmax, prove_insufficient, diag_*,
pattern_analysis, pick_best, neighbors_dmax) are byte-identical; only the
driver main (evidence + call sequence + verdict prints) is new.
`audit_frozen.sh` verifies the mechanism region of each driver is
byte-identical to the 4c233f82a blob.

### Family A: SCOPE-COLLAPSE (the max_rules arm is dead)

Driver A:
- A1: enumerate old envelope; predict n=78, nsig=15.
- A2: enumerate 220 3-rule delay<=2 graphs via frozen compute_arrivals;
  predict in_old=220, out_old=0.
- A3: corollary demos with the FROZEN diagnose: diagnose(E3)->binding=2
  (E3 = R3 evidence from the frozen main; the live arm); diagnose(E_B)->
  binding=0. Corollary: c_old=0 => c_mr=0 for all E, so binding=1 and the
  ambiguous branch are unreachable in every trace that reaches diagnose.
  The declared two-parameter scope collapses to {delay_max}.
- A verdict: `A-VERDICT SCOPE-COLLAPSE` iff n=78, nsig=15, in_old=220,
  out_old=0, E3 binding=2, E_B binding=0; else `A-VERDICT UNEXPECTED`.

### Family B: HONEST-STOP (no parameter binds)

Driver B mirrors the frozen Phase-1 pipeline exactly, with W0=[(X->Y,1)]
(the R3 prior winner) and E_B={(Y,6)=0,(Y,7)=1,(Z,7)=0}:
- B1: FAIL_OLD: revise_dmax(W0,E_B,...,2) returns -1. Predict k=-1.
- B2: prove_insufficient(E_B). Predict count=0.
- B3: pattern_analysis + diagnose. Predict `max_rules->3: 0/220`,
  `delay->3: 0/171`, `binding=none_or_ambiguous`, returns 0.
- B4: frozen branch (binding != 2): prints `BINDING-NOT-CONSTRUCTIBLE`,
  stops; no invent, no resolve. Predict honest stop, no silent misresolve.
- B verdict: `B-VERDICT HONEST-STOP` iff k=-1, count=0, binding=0 and the
  frozen stop string printed; else `B-VERDICT UNEXPECTED`.

### Family C: AMBIGUITY-HUNT (sweep for a live binding=1 or ambiguity)

Driver C: 49-cell sweep as in F4, using frozen prove_insufficient,
diag_count_maxrules3, diag_count_delay3 and the verbatim frozen binding
branch (quiet, no per-cell diagnose prints):
- C1: zero cells with (c_old=0 AND c_mr>0). Predict 0 violations.
- C2: binding=1 in zero cells. Predict 0.
- C3: binding=2 in exactly 11 cells; binding=0 in 38 cells.
- C verdict: `C-VERDICT NO-AMBIGUITY` iff C1=0, C2=0, b2=11, b0=38;
  else `C-VERDICT UNEXPECTED`.

## 5. Frozen verdict rules

- ADV-BREAKS (SCOPE-COLLAPSE) iff A1, A2, A3 match predictions: the
  max_rules diagnostic arm provably never fires in any reachable trace and
  the ambiguity arm provably never fires, so "generic diagnose-and-relax
  over {max_rules, delay_max}" is really single-parameter delay diagnosis
  with vestigial arms. The generality claim breaks. CAUSAL-EDITINVENT-PASS
  (R3) is NOT retracted: its trace (diagnose binds delay, invent dmax+1)
  remains valid; its ceiling narrows to "learner-authored delay-domain
  extension in one law-change family; the meta-procedure is provably
  delay-specific, not parameter-generic."
- ADV-SURVIVES iff some constructed family makes the frozen diagnose
  return binding=1 (requires F2 false; would need a prereg addendum).
- ADV-BOUNDARY iff the max_rules arm is live but unbound in these families
  (F2+F4 already exclude this), or B4 honest-stops where a constructor was
  expected (no constructor was ever claimed).
- Any `*-VERDICT UNEXPECTED` forces re-analysis before a verdict label.

## 6. Kill bars (frozen)

- K1: prereg commit strictly precedes every implementation commit
  (`git merge-base --is-ancestor` true).
- K2: all three drivers execute 3/3 byte-identical against the frozen
  mechanism: 3 fresh znc compiles per driver, stdout sha256 identical;
  `audit_frozen.sh` passes on all drivers (mechanism region byte-identical
  to the 4c233f82a blob).
- K3: verdict in {ADV-SURVIVES, ADV-BREAKS, ADV-BOUNDARY} per Section 5;
  pure Zag plus shell only; `check_no_dash.sh` clean on all committed
  files; contaminated paper untouched.

## 7. ONE-SYSTEM accounting (attack adds no cognition)

- Cognition source lines added: 0 (mechanism frozen; drivers are test code).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0. Learner-state structures created: none.

## 8. What this does NOT do

- Does not modify the frozen mechanism (any modification would void K2).
- Does not claim an L-level for the attack; it is an adversarial test.
- Does not re-litigate R3's PASS; it attacks only the generality claim.
