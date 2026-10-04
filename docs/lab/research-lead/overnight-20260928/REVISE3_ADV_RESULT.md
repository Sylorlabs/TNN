# H-REVISE3 Red Team: Adversary Report

**Date:** 2026-09-29
**Researcher:** H-REVISE3 Red Team (subagent, independent)
**Status:** COMPLETE
**Branch:** tnn-native-lab
**Prereg:** PREREG_REVISE3_ADV.md (53c5a5732, frozen before any attack execution)
**Attack code:** revise3_adv.zag (mechanism functions verbatim from revise3.zag lines 1-401; only main() replaced)
**Raw evidence:** revise3_adv_raw.txt (60 lines, md5 13fff6b55f7e98815eda8f7ab7e511d1, byte-identical across 3 runs)

## Verdict

**H-REVISE3 DOWNGRADED.** Two of three executable attacks succeed.
X-RV3-4 (source audit) passes. The frozen K-RV3-1..K-RV3-5 bars are
NOT retroactively altered (chained revision composes, the 'q' fixture
is diagnosed correctly, the withhold path is complete on the tested
fixtures). The downgrade bounds the scored-diagnosis heuristic and
documents the capacity limit.

## Attack results

### X-RV3-1 (Scoring gaming): SUCCEEDS (downgrade)

**Fixture:** Hidden true rule "IF input[2]=='y' (121) THEN identity
ELSE broadcast-last". Passing set ("abc"->"ccc"), ("def"->"fff"),
("ghi"->"iii"), ("jkl"->"lll"). Counterexample ("xqy"->"xqy"):
P0 predicts "yyy", DETECT.

**Mechanism behavior:**
- Pextract("xqy","xqy"): 'x' unique at 0, 'q' unique at 1, 'y' unique
  at 2. Extraction seq = [0,1,2].
- Discovery from {("xqy"->"xqy")}: P1 = [K] (identity),
  [[0,255,255],[1,255,255],[1,255,255],[6,1,2],[5,0,3]].
- Diagnosis candidates (all discriminate):
  - (0,120) 'x': output-relevance ('x' in "xqy") +1;
    program-consistency (0 in [0,1,2]) +1. Total: 2.
  - (1,113) 'q': 'q' in "xqy" +1; 1 in [0,1,2] +1. Total: 2.
  - (2,121) 'y': 'y' in "xqy" +1; 2 in [0,1,2] +1. Total: 2.
- Tie-break (strict `>`, lowest position wins): (0,120) selected.
- Truth: (2,121). Diagnosis is WRONG.

**Held-out (both fail as predicted):**
- ("aqy"->"aqy"): true rule gives identity "aqy". With wrong
  diagnosis (0,120): input[0]=='a' != 'x', so P0 broadcast-last gives
  "yyy". FAIL.
- ("xbc"->"ccc"): true rule (input[2]=='c') gives P0 "ccc". With
  wrong diagnosis: input[0]=='x', so P1 [K] gives "xbc". FAIL.

**Classification:** DOWNGRADE. The prereg explicitly states the scored
diagnosis is "a stated heuristic ranking, not a guaranteed causal
identification." The result doc names this exact surface as "the most
attackable." A success here bounds the heuristic; it does not
invalidate the three repaired failure classes. The 'q' fixture from
the original red team still works because 'x' does NOT appear in
"qqq" (output-relevance 0) and pos 0 is NOT in seq [1,1,1]
(program-consistency 0). The gaming requires the incidental byte to
appear in the output AND its position to be read by the discovered
program. When the discovered program is identity [K] (seq covers all
positions), any incidental byte present in the output will tie.

**What this means:** The scored diagnosis is strictly better than
lowest-position (it fixes the 'q' case), but it is not a causal
guarantee. An adversary who controls the counterexample can craft an
identity-mapping case where the tie-break decides. The honest claim is
"heuristic that fixes the demonstrated gaming fixture," not "causal
feature identification."

### X-RV3-2 (Overlapping conditions): BOUNDARY (informational)

**Fixture:** R1: ("xab"->"xxx"), cond (0,120), P1=[N N SUB].
R2: ("xqc"->"qqq"), cond (1,113), P2=[N C2 SUB].
Overlap input "xqc" satisfies BOTH (input[0]=='x' and input[1]=='q').

**Mechanism behavior:**
- "xqc" -> "qqq" via slot 2 (most-recent-first confirmed).
- "xab" -> "xxx" via slot 1 (slot 2 condition false, no overlap).
- Deterministic, matches the stated rule.

**Classification:** BOUNDARY. Most-recent-first is the STATED rule in
the prereg ("the newest revision wins ties"). This attack had no kill
criterion. The behavior is documented for users: overlapping
conditions resolve to newest. This is a semantic choice with
tradeoffs, not a bug. A future revision could add explicit
conflict detection, but that is outside the frozen claim.

### X-RV3-3 (Slot exhaustion): SUCCEEDS (downgrade, capacity boundary)

**Fixture:** Five sequential genuine revisions, distinct pos-0 bytes,
all broadcast-first [N N SUB]:
R1 ("xab"->"xxx") cond (0,120); R2 ("yzb"->"yyy") cond (0,121);
R3 ("qab"->"qqq") cond (0,113); R4 ("wab"->"www") cond (0,119);
R5 ("vab"->"vvv") cond (0,118).

**Mechanism behavior:**
- R1..R4: vs3_revise returns 1, vcount increments to 4.
- R5: vs3_revise returns 0 (vc>=4), vcount stays 4. Revision silently
  dropped.
- Query "vab": no slot matches (118 not in store), P0 broadcast-last
  gives "bbb". WRONG (expected "vvv").
- Sanity: "xab"->"xxx" still PASS (earlier revisions intact).

**Classification:** DOWNGRADE (capacity boundary). The 4-slot limit is
disclosed in the prereg ("Max 4 revision slots in the current store
layout"). However, the SILENT drop is a design gap: vs3_revise returns
0, but there is no eviction policy, no error to the user, no
"store full" signal in the query path. A continuing learner will
eventually need more than 4 revisions. The honest claim should be
"at most 4 chained revisions" stated explicitly, not just in the
prereg. Recommended: explicit capacity policy (LRU eviction, error on
full, or dynamic growth) for the next revision.

### X-RV3-4 (Source audit): PASS (attack fails; mechanism passes)

**Checks performed:**
1. `vs3_revise` append-only: writes to `56+vc*60`, increments vc,
   never overwrites an existing slot. Verified by inspection.
   Returns 0 if `vc>=4`. No overwrite path exists.
2. `diagnose_scored` iterates ALL positions: `while(p<fail.len)`,
   no early exit, scores each discriminating candidate. Verified.
3. Bounds-respecting guard: `if(plen>p)` skips short inputs; the
   discrimination test only runs when the passing input is long
   enough. Verified.
4. No byte-value literals in mechanism functions: grep for
   120/113/121/118/119 in `diagnose_scored` finds none outside
   emit/comments. All compared values come from `fail[p]`, `fail_out`,
   `D[off+p]`, i.e., from the data. Verified.
5. Tie-break is lowest position: `if(score>best_score)` uses strict
   `>`, not `>=`. The first (lowest p) candidate achieving the max
   score wins. Verified.
6. Mechanism functions verbatim: `diff <(head -n 401 revise3.zag)`
   vs the attack file head returns IDENTICAL. Only main() was
   replaced.

**Classification:** PASS. No spoofing. The 45/45 SURVIVES verdict on
the frozen bars was earned. The implementation matches the prereg.

## Summary table

| Attack | Result | Classification |
|--------|--------|----------------|
| X-RV3-1 (scoring gaming) | SUCCEEDS | DOWNGRADE (heuristic bounded) |
| X-RV3-2 (overlap) | DOCUMENTED | BOUNDARY (stated rule) |
| X-RV3-3 (slot exhaustion) | SUCCEEDS | DOWNGRADE (capacity limit) |
| X-RV3-4 (source audit) | PASS | No spoofing |

## What still stands

The three H-REVISE2 failure classes remain repaired on their
demonstrated fixtures:
- F-RV1: Chained revision composes (R1 survives R2, vcount=2).
- F-RV2: The 'q' gaming fixture is diagnosed correctly (1,113).
- F-RV3: No spurious UNRESOLVABLE on mixed-length sets.

The 45/45 frozen bars are not retroactively altered.

## What is bounded

1. **Scored diagnosis is a heuristic, not causal identification.**
   When the discovered program reads all positions (e.g., identity)
   and the incidental byte appears in the output, the tie-break
   (lowest position) can select an incidental feature. The honest
   claim: "fixes the demonstrated 'q' gaming fixture," not "identifies
   causal features."

2. **Capacity: at most 4 chained revisions.** The 5th is silently
   dropped. A continuing learner needs an explicit capacity policy.

3. **Overlap semantics: newest wins.** Documented, not buggy, but
   users should know.

## Recommended follow-ups

1. For the scoring heuristic: consider a tie-break that prefers
   higher positions when scores tie on identity-like programs, or an
   explicit "ambiguous diagnosis" withhold when top candidates tie.
   Alternatively, state the positional prior explicitly as a
   limitation.
2. For capacity: implement an explicit policy (evict oldest, error on
   full, or growable store) rather than silent drop.
3. For overlap: consider emitting a warning when a new revision's
   condition overlaps an existing one.

## Pure Zag compliance

Attack code, compilation (znc 2026.07.0-dev), and execution in Zag
only. No Python used. No em dashes in this document.

## Determinism

Three consecutive runs byte-identical (md5
13fff6b55f7e98815eda8f7ab7e511d1, verified with cmp).
