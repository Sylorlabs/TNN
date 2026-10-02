# Preregistration: H-REVISE3 Red Team (Adversary)

**Date:** 2026-09-29
**Researcher:** H-REVISE3 Red Team (subagent, independent)
**Status:** FROZEN (commit before any attack execution)
**Branch:** tnn-native-lab
**Target:** H-REVISE3 (revise3.zag, PREREG_REVISE3.md 54790d0d2, REVISE3_RESULT.md)

## Mission

Independently attack the H-REVISE3 repair claim. Assume it is false.
H-REVISE3 SURVIVES (45/45) with three repairs:
- F-RV1: appendable condition list (4 slots), vs_revise appends, most-recent-first dispatch
- F-RV2: scored diagnosis (+1 output-relevance, +1 program-consistency, tie-break lowest)
- F-RV3: bounds-respecting length guard

## Attacks

### X-RV3-1: Scoring gaming (incidental feature outscores causal)

**Theory:** The scored diagnosis can select an incidental feature if the
incidental byte also appears in the expected output AND its position
appears in the extraction index sequence. The result doc explicitly
names this as the most attackable surface.

**Fixture construction:**
- Hidden true rule: IF input[2]=='y' (121) THEN identity ELSE broadcast-last (P0).
- Passing set: ("abc"->"ccc"), ("def"->"fff"), ("ghi"->"iii"), ("jkl"->"lll").
  All have input[2] != 'y', so P0 (broadcast-last) is correct for them.
- Counterexample: ("xqy"->"xqy"). Input[2]=='y', so true rule gives
  identity. P0 predicts "yyy". DETECT.
- Pextract("xqy","xqy"): 'x' unique at 0, 'q' unique at 1, 'y' unique
  at 2. seq=[0,1,2].
- Discovery from {("xqy"->"xqy")}: P1=[K] (identity), fits seq [0,1,2].
- Diagnosis candidates (all discriminate against passing set):
  - (0,120) 'x': output-relevance? 'x' in "xqy": YES (+1).
    program-consistency? 0 in [0,1,2]: YES (+1). Total: 2.
  - (1,113) 'q': 'q' in "xqy": YES (+1). 1 in [0,1,2]: YES (+1). Total: 2.
  - (2,121) 'y': 'y' in "xqy": YES (+1). 2 in [0,1,2]: YES (+1). Total: 2.
- Tie-break (lowest position, `>` not `>=`): (0,120) wins.
- Truth: (2,121). Diagnosis is WRONG.

**Kill criterion:** If diagnosis returns (0,120) instead of (2,121),
AND at least one held-out case fails as a result, X-RV3-1 SUCCEEDS.

**Held-out probes:**
- ("aqy"->"aqy"): true rule (input[2]=='y') gives identity "aqy".
  With wrong diagnosis (0,120): input[0]=='a' != 'x', so P0:
  broadcast-last gives "yyy". FAIL (expected "aqy").
- ("xbc"->"ccc"): true rule (input[2]=='c' != 'y') gives P0 "ccc".
  With wrong diagnosis (0,120): input[0]=='x', so P1 [K]: "xbc". FAIL.

**Expected outcome:** Diagnosis (0,120), both held-out FAIL. This
demonstrates the scored heuristic selects an incidental feature when
the incidental byte appears in the output and at a program-read
position.

**Classification if succeeds:** DOWNGRADE (not kill). The prereg
explicitly states the scoring is a heuristic, not a causal guarantee.
The result doc names this as the attackable surface. A success bounds
the heuristic; it does not invalidate the three repaired failure
classes (chained revision still composes; the 'q' fixture still works;
the withhold path is still complete).

### X-RV3-2: Overlapping conditions (most-recent-first semantics)

**Theory:** The version store dispatches most-recent-first (stated
rule). When two revisions have overlapping (non-identical) conditions,
the newest wins. The prereg acknowledges this "may not be the intended
semantics in all cases."

**Fixture construction:**
- R1: counterexample ("xab"->"xxx"), diagnosis (0,120), P1=[N N SUB].
  Slot 1: IF input[0]=='x' (120) THEN P1 ELSE P0.
- R2: counterexample ("xqc"->"qqq"), diagnosis (1,113), P2=[N C2 SUB].
  Slot 2: IF input[1]=='q' (113) THEN P2 ELSE (slot 1).
- Overlap input: "xqc". Satisfies BOTH slot 2 (input[1]=='q') and
  slot 1 (input[0]=='x'). Most-recent-first: slot 2 wins, output "qqq".

**Kill criterion:** This attack does NOT have a kill criterion because
most-recent-first is the STATED rule. Instead, I will DOCUMENT the
behavior and assess whether it is reasonable.

**Documentation:** I will verify that:
1. "xqc" -> "qqq" via slot 2 (most-recent-first confirmed).
2. "xab" -> "xxx" via slot 1 (no overlap, slot 2 condition false).
3. The behavior is deterministic and matches the stated rule.

**Classification:** BOUNDARY (informational). The rule is explicit.
A user should understand that overlapping conditions resolve to newest.
This is not a bug; it is a documented semantic choice with tradeoffs.

### X-RV3-3: Slot exhaustion (5th revision)

**Theory:** The version store has max 4 revision slots (disclosed in
prereg: "Max 4 revision slots in the current store layout").
`vs3_revise` returns 0 when full. The 5th revision is silently dropped
(no error propagated to user beyond return code; main() emits
"REVISE FAILED" but continues).

**Fixture construction:** Five sequential genuine revisions:
- R1: ("xab"->"xxx"), cond (0,120)
- R2: ("yzb"->"yyy"), cond (0,121)
- R3: ("qab"->"qqq"), cond (0,113)
- R4: ("wab"->"www"), cond (0,119)
- R5: ("vab"->"vvv"), cond (0,118)
All are broadcast-first [N N SUB] cases with distinct pos-0 bytes.
Each is a genuine counterexample under the current dispatch.

**Kill criterion:** If the 5th revision is dropped (vs3_revise returns
0, vcount stays 4) AND a query requiring the 5th revision gives the
wrong answer, X-RV3-3 SUCCEEDS as a demonstrated capacity limit.

**Expected outcome:** vcount=4 after R5 attempt. Query "vab":
- Slot 4? input[0]=='v' (118)? No, slot 4 is (0,119) 'w'.
- Slot 3? (0,113) 'q'? No.
- Slot 2? (0,121) 'y'? No.
- Slot 1? (0,120) 'x'? No.
- P0: broadcast-last gives "bbb". WRONG (expected "vvv").

**Classification if succeeds:** DOWNGRADE (capacity boundary). The 4-slot
limit is disclosed. However, a continuing learner will eventually need
more than 4 revisions. The silent drop (vs. explicit error or eviction
policy) is a design gap. This bounds H-REVISE3 to "at most 4 chained
revisions," which should be stated explicitly.

### X-RV3-4: Source audit

**Theory:** Verify the implementation matches the prereg and contains
no spoofing (hardcoded test answers, bypassed logic).

**Checks:**
1. `vs3_revise` appends (writes to 56+vc*60, increments vc), never
   overwrites an existing slot. Verify by code inspection.
2. `diagnose_scored` iterates ALL positions (p from 0 to fail.len),
   scores each discriminating candidate, no early exit. Verify.
3. Bounds-respecting guard: `if(plen>p)` skips short inputs, does not
   veto. Verify.
4. No byte-value literals in mechanism functions: `diagnose_scored`,
   `vs3_revise`, `vs3_apply`, `discover` must not contain hardcoded
   120, 113, 121, etc. String literals in main() are test fixtures,
   not mechanism logic.
5. The tie-break is lowest position: `if(score>best_score)` (strict
   `>`, not `>=`), so first (lowest p) with max score wins. Verify.

**Kill criterion:** If any check fails (e.g., a hardcoded literal is
found in the diagnosis path, or vs_revise overwrites), X-RV3-4
SUCCEEDS as a kill (spoofing invalidates the SURVIVES verdict).

**Expected outcome:** All checks PASS. The implementation is faithful.
This is the "attack fails" case; it strengthens confidence in the
45/45 result.

## Commit Order

This prereg is committed BEFORE any attack code is written or executed.
Attack implementation will be a separate file (revise3_adv.zag) that
imports/copies mechanism functions from revise3.zag verbatim, with only
main() replaced to run the adversarial fixtures.

## Pure Zag Compliance

All attack code in Zag. No Python. Compilation with znc 2026.07.0-dev.

## Documentation Style

No em dashes in any loop documentation.
