# PREREG.md -- Invention Hypothesis 3: Constraint-Driven Novel Form

## Status: FROZEN (preregistration precedes implementation)

Frozen 2026-10-02. Any breakage requires fresh prereg plus fresh sealed
worlds plus rerun. Kill bars below are immutable for this wave.

## Hypothesis

TNN can construct a genuinely novel MAP form via backtracking search guided
by goal constraints. The search is constructive (builds cell by cell from
individual facts), not selective (does not choose from existing MAPs or a
finite menu). The final form is source-underdetermined: the source provides
general constraint checkers and backtracking machinery, but the specific
form is determined by the goal's constraint values plus the world's facts.

## Mechanism (to be implemented, unfrozen only)

`invent_try(W, s, r, expected, C)`:
- C is a constraint struct: [plen, rel_exact_r, rel_exact_n, first_rel,
  last_rel, first_lit]. A value of -1 means "don't care".
- Backtracking DFS over chain positions 0..plen-1. At each position,
  candidate facts are those with subject == current value, in node id
  order. A candidate is skipped if it violates any constraint (pruning):
  first_rel must match at pos 0; last_rel must match at pos plen-1;
  rel_exact count must stay reachable (count so far <= N and remaining
  positions can still reach N).
- On reaching plen positions: assemble via t2_asm_chain, verify via
  t2_try_verify (must produce expected), promote via promote_graph.
- Returns the verified answer or -2.

`ev_query_c(W, s, r, expected, flags, C)`: if C != 0 and invent_on()==1,
try invent_try first. On -2, fall through to standard ev_query
(activate, rebind, trial, bootstrap).

`invent_check(W, m, C)`: structural verification. Extracts the MAP's
relation sequence via cc_relseq-style walk (from executable structure,
never MAP labels) and checks plen, rel_exact count, first_rel, last_rel,
first_lit (v[0]). Returns 1 iff all non-don't-care constraints hold.

## Worlds (3 problems, fresh workspace each)

Problem 1:
- Facts (teach order): (3,3,10) (10,7,20) (20,5,30) (30,7,40) (40,9,90)
  then distractors (3,5,11) (11,5,90) (3,7,12) (12,7,90).
- Goal: s=3, r=70, expected=90.
- Constraints: plen=5, rel 7 exactly 2, first_rel=3, first_lit=3.
- Predicted invention result: chain [3,10,20,30,40,90], relseq [3,7,5,7,9].
- Predicted trial result: finds distractor path [3,11,90] (relse q [5,5],
  plen 2), correct answer 90 but violates plen and rel7 constraints.

Problem 2 (requires backtracking through a decoy dead end):
- Facts (teach order): decoys (50,3,65) (65,5,75), then solution
  (50,3,60) (60,5,70) (70,7,80) (80,9,150), then distractors
  (50,7,55) (55,7,150).
- Goal: s=50, r=71, expected=150.
- Constraints: plen=4, rel 5 exactly 1, last_rel=9.
- Predicted invention result: backtracks from decoy (65 has no outgoing
  facts), finds [50,60,70,80,150], relseq [3,5,7,9].
- Predicted trial result: finds [50,55,150] (relse q [7,7], plen 2),
  violates plen, rel5, last_rel constraints.

Problem 3:
- Facts (teach order): (200,3,205) (205,7,215) (215,5,225) (225,7,235)
  (235,9,245) (245,7,300), then distractors (200,5,210) (210,5,300).
- Goal: s=200, r=72, expected=300.
- Constraints: plen=6, rel 7 exactly 3, first_rel=3.
- Predicted invention result: [200,205,215,225,235,245,300],
  relseq [3,7,5,7,9,7].
- Predicted trial result: finds [200,210,300] (relse q [5,5], plen 2),
  violates plen and rel7 constraints.

## Arms

- TREAT: invent_on()=1. ev_query_c with constraints for each problem.
  After each query, run invent_check on the promoted MAP.
- NO-INVENT: invent_on()=0 (one-line diff binary). Same driver. Trial
  handles the queries. invent_check must FAIL on all 3 (proves the
  invention mechanism is what produces the constrained form, and that
  trial's answer-only success is form-inadequate).

## Frozen kill bars

K1 (construction): TREAT must promote a MAP for all 3 problems whose
invent_check returns 1. All 3 must satisfy every non-don't-care
constraint exactly.

K2 (inadequate existing): NO-INVENT must produce invent_check=0 on all
3 problems (trial finds the answer via a short distractor path whose
form violates the constraints).

K3 (novelty): Before invention runs, a scan of all existing MAPs must
find zero MAPs satisfying the constraints (invent_check=0 for every
pre-existing MAP).

K4 (structural difference): The 3 invented MAPs must have pairwise
different (plen, relseq) pairs.

K5 (determinism): 3/3 byte-identical transcripts per binary.

K6 (no hardcoded answers): Source contains zero occurrences of the test
world fact ids, value sequences, or expected answers as literals tied
to the invention logic. The constraint VALUES come from the driver
(goal side), not the mechanism.

## What counts as PASS

All of K1 through K6 hold.

## What counts as FAIL (any one)

- Invention returns -2 on any problem (no construction).
- invent_check=1 fails on any TREAT problem (wrong form).
- NO-INVENT achieves invent_check=1 on any problem (trial could do it).
- A pre-existing MAP satisfies constraints (not novel).
- Non-deterministic output across the 3 runs.
- Source inspection reveals the answer encoded in the mechanism.

## SUF evaluation (in REPORT.md, not a kill bar)

Inadequate existing (K2), new form (K1+K3), source-underdetermined
(K6 plus 3 different forms from one general mechanism), internally
evaluated (t2_try_verify execution check), useful (produces expected
via required form), persistent (promoted MAP in learner state),
reusable/revisable/transferable (assessed; persistence verified,
full transfer left to follow-up).
