# Preregistration: Bridge Adversary Attacks (B-A1..B-A6)

**Date:** 2026-09-29
**Status:** FROZEN (committed before running attacks)
**Role:** Bridge Adversary (independent, assumes H-BRIDGE false)
**Target:** H-BRIDGE claim in BRIDGE_RESULT.md (commit 06f5e2b5a),
  implementation bridge_learn.zag, prereg 17d5de9f7.

## Method

Attack file `bridge_attack.zag` = lines 1-458 of bridge_learn.zag
(everything before `fn main`), byte-verified identical via diff,
plus an independent attack `main`. This tests the SAME learner with
new tasks. Pure Zag, no Python. Toolchain znc 2026.07.0-dev.

## Attacks

### B-A1: Source inspection (zero byte literals in learner)

Claim under test (K-B2): bridge_learn contains no byte literal equal
to trigger values, and learns (pos, val) from data.

Procedure: grep bridge_learn.zag for `120`, `113`, `'x'`, `'q'`
restricted to the learner region (before `fn main`, line 460).
Any condition-value literal inside bridge_learn (lines 315-458)
or its callees = FAIL. Literals in the test main are evaluator
expectations, not learner hardcoding, and do not count.

Predicted: PASS (preliminary grep shows 120/113 only in main).

### B-A2: Generality (discriminating position in the middle)

The builder tested pos=0 (Task A) and pos=1 (Task B). Attack: put
the discriminating byte at pos=2 (middle of a 4-char input).

Task D training:
- ("abx" -> "xxx")  [broadcast-first, input[2]=='x']
- ("cdx" -> "xxx")  [broadcast-first, input[2]=='x']
- ("aby" -> "yyy")  [broadcast-last,  input[2]!='x']
- ("cdy" -> "yyy")  [broadcast-last,  input[2]!='x']

Expected if mechanism is general: bridge learns
IF input[2]==120 THEN proc_first ELSE proc_last.
Dispatch: bridge_apply("zzx") == "zzz" (all map to index 0 = 'z'),
bridge_apply("zzy") == "yyy" (all map to index 2 = 'y').

Note: pos=0 and pos=1 both fail to split here (values at pos 0/1
do not separate the classes), so success requires the search to
actually reach and use pos=2. If bridge fails or picks a wrong
position, B-A2 FAILS and generality is bounded to edge positions.

### B-A3: Three-way split (binary-only boundary)

Builder admits binary conditions only (prereg scope note 1).
Attack: verify the boundary is real, not just undocumented luck.

Task E training:
- ("xab" -> "aaa")  [input[0]=='x' -> broadcast-first]
- ("yab" -> "bbb")  [input[0]=='y' -> broadcast-last]
- ("zab" -> "ccc")  [input[0]=='z' -> broadcast-middle? or identity?]

Use outputs that need three distinct procedures:
- ("xab" -> "aaa")  [first]
- ("yab" -> "bbb")  [last]
- ("qab" -> "aba")  [identity]

Expected: bridge returns a binary rule that is WRONG on at least
one class, or returns -1. Either outcome documents the boundary.
If the bridge somehow handles 3-way correctly, B-A3 PASSES
unexpectedly (strong result for builder). Predicted: bridge learns
a binary split (e.g. 'x' vs rest) and mis-dispatches one class.

Scoring: B-A3 is a BOUNDARY PROBE, not a kill bar. Document exact
behavior. A wrong-but-confident binary rule is worse than -1;
note which occurs.

### B-A4: Two-position conjunction

Task F training (condition needs input[0] AND input[1]):
- ("xyab" -> "aaaa")  [0=='x' AND 1=='y' -> broadcast-first]
- ("xycd" -> "aaaa")  [0=='x' AND 1=='y' -> broadcast-first]
- ("xzab" -> "bbbb")  [0=='x', 1!='y' -> broadcast-last]
- ("zyab" -> "bbbb")  [0!='x' -> broadcast-last]

No single (pos, val) separates the classes:
pos 0: 'x'->{first,last}, 'z'->{last} -> split on 'x' gives
  {first,last} vs {last}: subset 1 contradictory.
pos 1: 'y'->{first,last}, 'z'->{last}: same problem.
Expected: bridge returns -1 (no single split works).
If bridge returns a WRONG binary rule instead of -1, that is a
worse failure mode (confident error beats honest -1).
Predicted: -1 (honest failure). Document.

### B-A5: Failure detection (no spurious trigger)

Task G: a task direct discovery CAN solve, but with an
accidental byte correlation present:
- ("abc" -> "cba")  [reverse]
- ("def" -> "fed")  [reverse]
- ("xgh" -> "hgx")  [reverse; input[0]=='x' coincides]

Direct discovery should find reverse ([N K C1 ADD SUB]-family
program) and return a proc slot with ZERO bridge rules.
If bridge triggers here (because it never tries direct first,
or mis-detects failure), B-A5 FAILS: the bridge is not
failure-gated, it is trigger-happy.

Note: extraction requires unique chars; "abc"->"cba" etc. have
unique chars, so extraction succeeds. Predicted: PASS (direct
succeeds, 0 rules).

### B-A6: Slot waste / exhaustion

Builder admits: failed split attempts consume proc slots
("first-working-split-wins wastes proc slots on failed attempts",
PROC_MAX=16).

Attack: construct a task where MANY values are tried before the
working one, exhausting slots so the final store fails.

Task H: 8 training pairs, input[0] in {'a','b','c','d','e','f',
'g','x'}, only 'x' is the true trigger:
- 7 pairs ("abb"->"bbb", "cbb"->"bbb", ...) broadcast-last variants
  with distinct first bytes, all with unique chars.
- 1 pair ("xzz"->"zzz") broadcast-first? No: need broadcast-first
  output distinct: ("xab"->"aaa").

Wait: broadcast-first of "xab" is "aaa"; the 7 others must be
broadcast-last with distinct pos-0 values and otherwise consistent
so that only the 'x' split yields two fittable subsets.

Simpler deterministic version: at pos=0, values tried in data
order 'a','b','c','d','e','f','g' before 'x'. Each failed value v:
subset {input[0]==v} is a single broadcast-last pair (fits, slot
consumed), subset {rest} is contradictory (7 pairs mixing last
with the one 'x'->first pair... wait the rest contains 'xab'->"aaa"
which is broadcast-first, contradicting broadcast-last) so fails.
Each failed attempt wastes 1 slot (the s1 store). 7 failures = 7
wasted slots. Then 'x' succeeds: needs 2 more slots (s1, s2).
Total 9 slots < 16, so no exhaustion, but waste is measurable:
count proc slots used vs the 2 needed.

Then the exhaustion variant: 14 distinct failing values before
'x' (PROC_MAX=16): 14 wasted + 2 needed = 16, borderline; 15
failing values -> the final s2 store returns -1 -> bridge fails
despite a learnable rule existing. If demonstrated, B-A6 shows a
denial-of-learning bug, not just inefficiency.

Predicted: waste confirmed (measurable); exhaustion reachable
with enough distractors. Scoring: waste = boundary documented;
exhaustion = FAIL-grade bug if the rule is learnable but slots
run out.

## Kill criteria

- B-A1 FAIL (literal in learner) => K-B2 retroactively FAILS =>
  H-BRIDGE KILLED.
- B-A2 FAIL (cannot use pos=2) => generality claim dies; H-BRIDGE
  downgraded to edge-position-only.
- B-A5 FAIL (spurious trigger) => K-B1 retroactively FAILS =>
  H-BRIDGE KILLED.
- B-A6 exhaustion demonstrated => H-BRIDGE survives but with a
  documented denial-of-learning bug; repair required before any
  integration use.
- B-A3, B-A4 are boundary probes: document exact behavior.

## Commit order

1. This prereg (frozen).
2. bridge_attack.zag (learner lines 1-458 verbatim + attack main).
3. Raw output + this report's results section.
