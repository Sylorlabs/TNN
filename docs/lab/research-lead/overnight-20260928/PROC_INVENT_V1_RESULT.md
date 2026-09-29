# Procedure Invention v1 Results

**Date:** 2026-09-29 07:45 PDT
**Status:** H-PROC SURVIVES (bounded)
**Implementation:** `sem_l3/proc_learn.zag` (pure Zag)

## Mechanism

**Compositional Index-Program Search:**
1. Extract index sequences from (input, output) examples.
2. Enumerate 1055 compositional programs (K, N, C0/C1/C2, ADD, SUB) up to size 5.
3. Select smallest program reproducing all sequences.
4. Apply to novel inputs.

## Results

### PI-1a: Reverse (primary)
- **Training:** ("abc"→"cba"), ("def"→"fed"), ("xy"→"yx")
- **Sequences:** [2,1,0] (n=3), [2,1,0] (n=3), [1,0] (n=2)
- **Invented program:** Index 608, 5 nodes: `[N K C1 ADD SUB]`
- **Decoded:** `SUB(N, ADD(K, C1))` = `n - (k+1)` = `n-1-k`
- **Hidden tests:** 3/3 PASS
  - "hello" → "olleh" ✓
  - "12345" → "54321" ✓
  - "q" → "q" ✓ (single char, K-P5)

### PI-1b: Identity (generality control)
- **Training:** ("abc"→"abc")
- **Sequence:** [0,1,2] (n=3)
- **Invented program:** Index 0, 1 node: `[K]`
- **Decoded:** `K` (identity)
- **Hidden test:** 1/1 PASS ("hello"→"hello" ✓)

## Kill Bar Verdicts

**K-P1 (Reverse-specificity):** PASS. Mechanism found different programs for
different training data (reverse → n-1-k, identity → k). Not reverse-tuned.

**K-P2 (Menu):** PASS. Search space = 1055 programs (5 + 50 + 1000), not a menu.
The specific solution emerged from search.

**K-P3 (Memorization):** PASS. Memorization baseline (store pairs, WITHHOLD on
unseen) scores 0/3 on hidden (inputs not in training). H-PROC scores 3/3.
Clear advantage.

**K-P4 (Source contamination):** PASS. Source contains primitives (K,N,ADD,SUB)
and search logic. Does NOT contain "reverse", "n-1-k", or the specific solution.
The program emerged from enumeration + verification.

**K-P5 (Single-character):** PASS. "q"→"q" correct. Program handles edge case.

## L3 Criteria Assessment

1. ✓ Not in source: The n-1-k program is not written as a solution.
2. ✓ Not enumerated: 1055 compositional programs, not a named menu.
3. ✓ Created after experience: Selected based on training sequences.
4. ✓ Persistent: Program stored as data (nodes array), printable.
5. ✓ White-box trace: Search log shows 1055 candidates, selection of #608.
6. ✓ Hidden solved: 3/3 reverse, 1/1 identity.
7. ✓ Ablation: Without program, cannot transform (memorization baseline 0/3).
8. ✓ Reused: Applied to 4 distinct hidden inputs.
9. ✓ Transfers: Works on letters ("hello") and digits ("12345").
10. ✓ Beats memorization: 3/3 vs 0/3.
11. ⏳ Red team: Pending (independent adversary not yet run).
12. ✗ Revision: Not implemented (documented limitation).

**Result:** 10/12 criteria met. Bounded L3 for procedure invention.

## Limitations

1. **Training requires unambiguous examples.** The extractor fails if characters
   repeat in ways that create ambiguous mappings. "hello" was used as hidden
   (not training) for this reason.
2. **No revision.** If a counterexample arrives, the mechanism cannot update
   the program. It would need to re-run search from scratch.
3. **Limited operator set.** Only ADD/SUB. Cannot learn procedures requiring
   multiplication, division, or conditionals (e.g., swap needs IF).
4. **Fixed size bound.** Programs up to size 5 only. More complex procedures
   out of scope for v1.
5. **String-only.** The index-mapping representation assumes output length
   relates to input length. Not general to all procedures.

## What This Proves

The learner invented a reusable procedure (`n-1-k`) that:
- Was not in source
- Was not a menu selection
- Generalizes to unseen inputs
- Works across alphabets
- Beats memorization

This is **genuine L3 procedure invention** (bounded).

## What It Does Not Prove

- General procedure invention (only index mappings)
- Revision (cannot update on counterexample)
- Composition (cannot combine procedures)
- Open-ended invention (limited to size-5 arithmetic)

## Next Steps

1. Independent red team (separate agent).
2. Test on swap (requires IF — will fail, documenting boundary).
3. Test on rotate (requires MOD — will fail, documenting boundary).
4. Implement revision (re-search on counterexample).
