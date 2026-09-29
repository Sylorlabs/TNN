# RT2 Red Team Report: Procedure Invention Follow-up Attacks

**Date:** 2026-09-29
**Agent:** RT2 (Procedure-Invention Red Team)
**Authority:** Parent task directive
**Status:** COMPLETE. All three attacks executed.

## Summary

| Attack | Result | Verdict |
|--------|--------|---------|
| RT2-A (Family X authoritative) | 8/8, X1-X5 all pass | **PASS** |
| RT2-B (Semantic collapse) | 85 distinct of 1055 | **PASS** (but note collapse) |
| RT2-C (Extraction robustness) | Vacuous on repeated chars | **FAIL** (vulnerability confirmed) |

**Overall:** The "bounded L3" claim SURVIVES RT2-A and RT2-B, but RT2-C
exposes a severe robustness limitation that narrows the scope significantly.

---

## RT2-A: Authoritative Family X Verification

**Method:**
- Compiled Builder's FROZEN source from commit `8fa0fe2a3`
  (training-data substitution only, per assignment).
- Verified binary finds `[N C1 SUB]` (SUB(N,C1)) at index 38.
- Generated 4 hidden inputs with fresh seed `123456789012345678`
  via `pi_adversary/gen_hidden_inputs.sh` (ascii-lower):
  1. "q" (len 1)
  2. "ptc" (len 3)
  3. "s" (len 1)
  4. "eghjjupazbnf" (len 12)
- Applied discovered program via independent Zag harness (`apply_fx.zag`).
- Tested all 8 cases (4 disclosed + 4 hidden).

**Results:**

| Input | Expected | Got | Result |
|-------|----------|-----|--------|
| "zag" | "ggg" | "ggg" | PASS |
| "12" | "22" | "22" | PASS |
| "q" | "q" | "q" | PASS |
| "hello" | "ooooo" | "ooooo" | PASS |
| "q" (hidden) | "q" | "q" | PASS |
| "ptc" (hidden) | "ccc" | "ccc" | PASS |
| "s" (hidden) | "s" | "s" | PASS |
| "eghjjupazbnf" (hidden) | "ffffffffffff" | "ffffffffffff" | PASS |

**Bars:**
- X1 (correctness >=7/8): **PASS** (8/8)
- X2 (no crash): **PASS** (all 8 produced output)
- X3 (N-dependence): **PASS** (program is SUB(N,C1), references N)
- X4 (no undeclared changes): **PASS** (diff confirms only training-data
  substitution: out0 "cba"->"ccc", out1 "yx"->"yy", added third pair,
  added fits2 check; primitives/enumeration/selection unchanged)
- X5 (no memorization): **PASS** (4/4 on generator inputs with novel
  characters; lookup table would score 0)

**Verdict:** RT2-A **PASS**. The Family X discovery is AUTHORITATIVE,
not projected. The "bounded L3" claim is RESTORED for the mechanism
within its documented scope.

**Note:** Initial test harness had a typo in expected output
("fffffffffff" 11 chars vs correct "ffffffffffff" 12 chars).
The program output was correct; the harness expectation was wrong.
Fixed and re-ran: 8/8. This is documented as a test-harness bug,
not a mechanism issue.

---

## RT2-B: Semantic Collapse

**Hypothesis (Adversary):** 1055 syntactic programs collapse to ~6
semantic functions (K, N-1-K, C0/C1/C2, N-1). If true, K-P2 ("not a menu")
FAILS on the semantic reading.

**Method:**
- Enumerated all 1055 programs (same enumeration as proc_learn.zag).
- Evaluated each on (k,n) for n=1..6, k<n (21 points).
- Counted distinct signatures via pairwise comparison.
- Implemented in pure Zag (`collapse.zag`).

**Result:** **85 distinct semantic behaviors** (not ~6).

**Analysis:**
- The Adversary's "~6" prediction was WRONG.
- However, 1055 -> 85 is still a 12x collapse.
- All 85 are affine functions f(k,n) = ak + bn + c.
- The space includes: k, n, constants, 2k, n-1, n-2, k+1, 2k+n, etc.

**Verdict:** RT2-B **PASS** (distinct count 85 > 20 threshold).
The "menu" is larger than the Adversary feared, but it IS still a
finite enumerated menu of 85 affine functions. The mechanism is
fundamentally "enumerate and select smallest fitting," not constructive
invention. This is documented as a scope limitation, not a kill.

---

## RT2-C: Extraction Robustness

**Hypothesis (Adversary):** `extract_seq` returns vacuous (-1) on
ambiguous inputs, creating a robustness kill vector.

**Method:**
- Implemented `extract_seq` in isolation (`extract_robust.zag`).
- Tested on repeated-character and ambiguous inputs.
- Pure Zag. No Python.

**Results:**

| Input | Output | Extraction | Status |
|-------|--------|------------|--------|
| "aaa" | "aaa" | VACUOUS (-1) | **FAIL** |
| "aba" | "aba" | VACUOUS (-1) | **FAIL** |
| "abc" | "ccc" | [2,2,2] | OK |
| "hello" | "ooooo" | [4,4,4,4,4] | OK |
| "q" | "q" | [0] | OK |
| "abc" | "xyz" | VACUOUS (-1) | **FAIL** |
| "aab" | "aba" | VACUOUS (-1) | **FAIL** |

**Analysis:**
`extract_seq` requires EVERY output character to appear EXACTLY ONCE
in the input. If:
- Input has any repeated character that appears in output -> VACUOUS
- Output contains a character not in input -> VACUOUS
- Any ambiguity in character-to-index mapping -> VACUOUS

**This is a SEVERE robustness limitation:**
1. The simplest identity case ("aaa"->"aaa") FAILS at extraction.
2. Real-world strings almost always have repeated characters.
3. Family X succeeded only because the training inputs ("abc", "xy",
   "defg") happened to have all-unique characters. This was luck,
   not robust design.
4. If the Adversary had assigned "aab"->"bbb" as training, the
   mechanism would have failed before search even began.

**Verdict:** RT2-C **FAIL**. Vulnerability CONFIRMED.

**Impact on "bounded L3" claim:**
This does NOT retroactively invalidate RT2-A (Family X passed within
its scope). However, it NARROWS the scope significantly. The mechanism
only works when:
- All input characters are unique, AND
- Every output character appears exactly once in input.

The "bounded" in "bounded L3" must now explicitly include:
"requires unambiguous character-to-index extraction; fails on any
input with repeated characters."

---

## Overall Assessment

**The "bounded L3" claim SURVIVES but with narrowed scope.**

What survives:
- Family X (broadcast-last) was discovered on an undisclosed family.
- 8/8 authoritative hidden tests pass.
- No undeclared source changes.
- Not memorization (generalizes to novel characters).
- Semantic space (85 functions) is larger than feared.

What is now documented as limitations:
1. **Extraction fragility (RT2-C FAIL):** Requires unique characters.
   Cannot handle "aaa"->"aaa", the simplest possible case.
2. **Enumerate-and-select (RT2-B note):** The mechanism searches a
   finite menu of 85 affine functions. This is not constructive
   invention; it is selection from a pre-enumerated (though not
   pre-named) space.
3. **Affine-only:** All discoverable procedures are f(k,n)=ak+bn+c.
   No conditionals, no loops, no composition beyond size-5.

**Recommendation:**
The claim should be restated as:
> "Bounded mechanism validation: The index-program search discovers
> affine index transformations from unambiguous examples. Demonstrated
> on reverse (pre-named, downgraded) and broadcast-last (undisclosed,
> 8/8). Scope: requires unique input characters; limited to 85 affine
> functions; enumerate-and-select, not constructive invention."

This is honest. It is not L3 in the full 12-criterion sense, but it
is a validated bounded mechanism.

---

## Artifacts

- `/tmp/rt2/proc_learn_frozen.zag` - frozen source from 8fa0fe2a3
- `/tmp/rt2/apply_fx.zag` - RT2-A independent test harness
- `/tmp/rt2/collapse.zag` - RT2-B semantic enumeration
- `/tmp/rt2/extract_robust.zag` - RT2-C extraction tests
- `/tmp/rt2/hidden_inputs.txt` - generated hidden inputs
- Seed: `123456789012345678` (published for reproducibility)

All test code is pure Zag/shell. No Python.

---

## Commits

This report will be committed to `tnn-native-lab` as:
`RT2: Family X authoritative 8/8, semantic 85/1055, extraction vulnerability`
