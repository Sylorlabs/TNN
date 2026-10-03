# REPORT.md -- Invention H3 Red Team

## Verdict: INVENTION-H3-REDTEAM-COMPLETE

**Per-attack: Attack 1 KILL, Attack 2 SURVIVE, Attack 3 BOUND, Attack 4 BOUND, Attack 5 KILL.**

The mechanism under test (byte-identical copy of the frozen
`invention_constraint/invent_patch.zag`, never modified) survives as a
**constructive constraint-satisfaction engine**: it builds chains from
individual facts, never selects existing MAPs, and beats trial's
form-blindness. It does NOT survive as a **form-inventing or
form-discovering search**: it has no quality criterion (first DFS hit
wins, teach order decides), it quits after one verify-fail without
further search, its "search" in all 3 H3 problems ran over a singleton
solution space the researcher fully determined in the constraints, it
promotes degenerate stuttering chains with full confidence, and 1 of its
6 constraints is invisible to the search.

## Method

Adversarial drivers only; the mechanism and base are frozen
byte-identical copies (`rt_mech.zag`, `rt_base.zag`, SHA-256 recorded in
NAMECHECK step 2 context). Two binaries (pinned znc):

- `rt_bin_main`: attacks 1, 2, 4, 5. 3/3 byte-identical runs.
- `rt_bin_scale`: attack 3, 13 configs. 3/3 byte-identical runs.

A faithful counting mirror of the frozen `invent_dfs` (same candidate
order via the frozen `invent_fact_next`, same pruning, full enumeration
instead of first-hit stop) measures solution-space size, backtracks,
visits, and prunes. Mirror fidelity is cross-validated: on all 3 exact
H3 worlds plus the poison world, the real `invent_try` winner's
licensing fact ids equal the mirror's recorded sequence #1 exactly.

## Attack 1: constraint underdetermination -- KILL

Four parallel length-3 chains from 1000, all ending at 2000, all relseq
[3,7,5]. Weak constraints a real goal could state without knowing the
answer: plen=3, first_lit=1000. All 4 chains satisfy the constraints and
verify (mirror: nseq=4, verifying=4 of 4).

- Forward teach order: `invent_try` returns 2000, check=1, winner is
  chain 0 (facts [2,3,4], the first taught). visits_at_first=3,
  backtracks_at_first=0: the very first candidate chain examined was
  taken. No comparison, no scoring.
- Reverse teach order (SAME fact set): winner is chain 3
  (vals=[1000,1103,1203,2000]), check=1. The invented form is determined
  by teach order, not by any property of the forms. Both outputs satisfy
  every constraint; the mechanism is indifferent between them.
- Verify-fail give-up: chains ending at 2000/2001/2002/2003,
  expected=2002. Mirror proves a verifying chain exists (verifying=1 of
  4). `invent_try` emits INVENT-FAIL and returns -2. The first DFS hit
  (chain 0, ends 2000) fails `t2_try_verify` and the search ENDS. There
  is no continued search over the remaining satisfying sequences.

There is no quality criterion anywhere in the mechanism: no scoring, no
comparison, no second attempt. "Invention" under underdetermining
constraints is first-hit-wins in node id order.

## Attack 2: contradictory constraints -- SURVIVE

Three unsatisfiable sets on a small world, plus the depth-cap probe.
All terminate cleanly with INVENT-FAIL and -2:

- A2a: plen=3, rel 7 exactly 5 (unreachable count). -2.
- A2b: plen=2, first_rel=3, last_rel=9 (no rel-9 fact). -2.
- A2c: plen=3, first_rel=5 (nothing from s has rel 5). -2, immediate.
- A2d: plen=8. -2 by the hard `plen<1 || plen>7` rejection.

The DFS is depth-bounded and fact enumeration is finite, so termination
is structural, not luck. The narrow "does it terminate or thrash"
question survives; the cost question is Attack 3.

## Attack 3: search blowup -- BOUND

Dense graphs (S=30 subjects, b outgoing facts each), contradictory
last_rel=9 forcing full exploration, plus satisfiable-late controls.
Full table in `rt_timing.txt`. Visit counts match the full-enumeration
law visits = b*(b^P-1)/(b-1) EXACTLY at all 11 contradictory configs
(e.g. b=6,P=7: 335922). The pruning contributes nothing in the dense
case. All runs terminate (ans=-2); the late-solution runs find the
answer (ans=7000) after near-full exploration.

- Cost is exponential in branching b and depth P: ~b x per +1 b, ~b x
  per +1 P.
- Extrapolated at max depth P=7: b=10 -> ~8 min/query; b=15 -> ~2.2
  hours/query; b=20 -> ~16 hours/query. Infeasibility knee around
  b=12..15 outgoing facts per value.
- The mechanism is feasible in practice ONLY because `invent_try`
  hard-caps plen at 7. That cap is the safety rail and the scope
  ceiling: no chain longer than 7 links can ever be invented, by
  construction. Anything needing longer compositional chains is out of
  scope for this mechanism, permanently unless the cap (and the
  exponential) is redesigned.

## Attack 4: constraint smuggling -- BOUND

Exact rebuilds of the 3 H3 worlds with the exact H3 constraints,
counting EVERY constraint-satisfying fact sequence:

- P1: nseq=1, verifying=1 of 1. visits_at_first=5, backtracks_at_first=0.
- P2: nseq=1, verifying=1 of 1. backtracks_at_first=2 (the decoy).
- P3: nseq=1, verifying=1 of 1. backtracks_at_first=0.

In all 3 problems the constraints admit EXACTLY ONE fact sequence. In
P1 and P3 the DFS never backtracked before the hit: it walked a forced
path. The "search" searched a singleton. The form-selecting work,
choosing plen=5, rel-7-exactly-2, first_rel=3, first_lit=3, was done by
whoever wrote the constraints (the researcher, with the solution in
hand), not by the mechanism. A goal that does not already know the
answer's form cannot write such constraints; a goal that writes only
what it honestly knows gets Attack 1 (arbitrary first hit).

What survives: construction from individual facts (no MAP selected,
recombined, or modified; K3-style novelty is real at the level of
learner state), and the demonstrated gap vs trial's form-blindness.
What does not: the "backtracking search discovers the form" reading.
H3 demonstrates constructive constraint SATISFACTION, not form
DISCOVERY. The 3 "novel forms" were novel to learner state but uniquely
determined by researcher-authored constraints.

## Attack 5: fact poisoning -- KILL

Poison chain taught FIRST (lowest ids): [1000,1005,1006,1005,2000],
relse q [3,7,7,9], a pointless 2-cycle detour that revisits 1005.
Clean chain taught SECOND: [1000,1010,1020,1030,2000], relseq
[3,7,5,7]. Constraints plen=4, rel7 exactly 2, first_rel=3. Mirror:
nseq=2, verifying=2 of 2.

`invent_try` promotes the DEGENERATE chain (vals=[1000,1005,1006,1005,
2000]), invent_check=1. Verification (`t2_try_verify`) is answer-only:
any constraint-satisfying chain producing the expected output is
promoted, however degenerate. Form quality, non-redundancy, and
minimality are invisible to the mechanism. Distractor facts taught first
win ties, and nothing downstream can tell the stuttering form from the
clean one.

Second finding: `first_lit` is search-invisible. The frozen
`invent_dfs` never reads C[20]; only the external `invent_check`
harness enforces it. With first_lit=9999 (not equal to s=1000),
`invent_try` still constructs, verifies, and PROMOTES (ans=2000,
check=0). One of the six advertised constraints does not drive
construction at all; it is enforced by the test harness, not the
search.

## What the red team did NOT break

- Construction is genuinely from facts: no existing MAP is selected or
  modified in the invention path (mirror + winner fact-id traces
  confirm fact-level construction).
- The trial control gap is real: trial remains form-blind (not
  re-attacked; the H3 NO-INVENT arm stands).
- Termination on contradiction (Attack 2) and determinism (3/3
  byte-identical on both binaries) hold.
- The mirror cross-validation (winner fact ids == mirror seq#1 on 4/4
  worlds) means every count above is a measurement of the real
  mechanism's traversal, not of a reimplementation.

## Recommended follow-ups (for the parent, not decided here)

1. If H3 is kept as a subsystem: add continued search after
   verify-fail (backtrack into `invent_dfs` rather than returning -2),
   enforce `first_lit` (or drop it from the constraint language), and
   add a quality criterion or explicit tie-breaking policy so teach
   order does not silently decide forms.
2. The honest next experiment for "invention": the goal supplies
   constraints it could know WITHOUT knowing the answer, and the
   mechanism must still produce a non-degenerate form. Attack 1 shows
   the current mechanism cannot pass that.
3. Depth cap: any claim beyond plen 7 needs a redesigned search
   (memoization, heuristic ordering, or iterative deepening), not a
   raised constant.

## Files

- `NAMECHECK.md`: toolchain guard (Step 0 PASS, zero forbidden
  executables), identity, base/mechanism provenance.
- `rt_base.zag`: frozen base copy (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  matches `../composition_C/cc_base.zag`).
- `rt_mech.zag`: frozen mechanism copy (SHA-256
  4fc5493061363bc8ab9a228cb6a67db17f080a01114a5a920efcc87ced47d0bf,
  matches `../invention_constraint/invent_patch.zag`). Never modified.
- `rt_driver_main.zag`: attacks 1, 2, 4, 5 (new, adversarial).
- `rt_driver_scale.zag`: attack 3 (new, adversarial).
- `rt_full_main.zag`, `rt_full_scale.zag`: assembled sources.
- `rt_bin_main`, `rt_bin_scale`: binaries (pinned znc).
- `rt_compile_main.txt`, `rt_compile_scale.txt`: build logs
  (warnings only, same analyzer class as the H3 build).
- `rt_run1/2/3.txt`: main transcripts, 3/3 byte-identical.
- `rt_scale_run1/2/3.txt`: scale transcripts, 3/3 byte-identical.
- `rt_timing.txt`: attack 3 table + extrapolation.

Architecture accounting: 0 lines changed in frozen sources, 0 new
modes/bridges/handlers, 0 new semantic cases. Pure Zag. Paper untouched.
Nothing pushed.
