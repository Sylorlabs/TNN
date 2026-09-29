# Procedure Transfer Test Results (PI-5)

**Date:** 2026-09-29
**Tester:** Procedure Transfer Tester (independent)
**Target:** Builder v1 `n-1-k` procedure from `fb6ab328a`
**Method:** Hardcoded the invented program as persisted state; tested WITHOUT re-running search.
**Implementation:** `sem_l3/proc_transfer.zag` (pure Zag)

## Test Design

The critical transfer question: **Does the ALREADY-INVENTED procedure work on new domains, or must the learner re-invent it?**

We simulated the persisted learner state by hardcoding `n-1-k` (nodes `[N K C1 ADD SUB]`, decoded as `SUB(N, ADD(K, C1))`) and applied it to transfer cases without search.

## Results

### PI-5a: Different Symbol Set

**5a-1:** High bytes [200, 201, 202] → [202, 201, 200] — **PASS**
**5a-2:** Control chars [10, 20, 30, 40] → [40, 30, 20, 10] — **PASS**

The procedure operates on indices (k, n), not on symbol values. Transfer across symbol sets is trivial because the index mapping is representation-agnostic.

### PI-5b: Different Domain (Numeric Array)

**5b-1:** Numeric bytes [1, 2, 3, 4, 5] → [5, 4, 3, 2, 1] — **PASS**
**5b-2:** Single numeric [42] → [42] — **PASS**

The "domain" is still byte sequences, but the content is numeric rather than textual. The procedure works because it never inspects content, only positions.

### PI-5c: Composition

**5c-1:** Manual double-apply (reverse twice = identity) — **PASS**
**5c-2:** Learner-automatic composition — **NOT IMPLEMENTED** (v1 limitation)

The v1 learner has no composition operator. It cannot combine `n-1-k` with another procedure automatically. Manual composition works, proving the procedure is composable in principle, but the learner cannot do this itself.

## Summary: 5/5 PASS (with 5c-2 as documented limitation)

## Honest Interpretation

### What this proves

The `n-1-k` procedure is **reusable** across:
- Different symbol encodings (ASCII, high bytes, control chars)
- Different content types (text, numeric data)
- Different sequence lengths

It is **not** tied to the string-reversal training distribution. The training used ("abc", "xy"); the tests used byte values never seen in training.

This satisfies L3 criterion #9 (transfers across changed surface representation) at the byte-sequence level.

### What this does NOT prove

1. **Shallow transfer.** The procedure is index arithmetic. It doesn't "understand" reversal; it computes positions. Transfer is almost tautological given the representation.

2. **Same underlying structure.** All tests are still on indexed byte sequences. True cross-domain transfer (e.g., to action sequences, tree structures, or temporal plans) was not tested and would require a different representation.

3. **Learner-driven reuse.** The learner does not recognize when to apply `n-1-k`. It would re-run the full 1055-program search on new examples. The "persistence" is storage, not intelligent retrieval.

4. **Composition.** The learner cannot compose procedures. This is a hard v1 boundary.

### Adversarial note

A skeptic could argue: "You proved that `n-1-k` works on different bytes. But `n-1-k` is just subtraction. Of course subtraction works on different bytes. This doesn't prove the learner invented a 'procedure' in any cognitively interesting sense; it proves the learner found an arithmetic formula that happens to describe index reversal."

This is a fair critique. The v1 mechanism invents **index-mapping formulas**, not **general procedures**. The L3 claim should be bounded accordingly: "bounded L3 for index-mapping procedure invention," not "general procedure invention."

## Verdict

**PI-5 TRANSFER: PASS (bounded).**

The procedure transfers across surface representations. The transfer is real but shallow, limited to the index-mapping domain. Composition and cross-structural transfer remain open.

## Limitations for v2

1. Test transfer to non-sequential structures (trees, graphs).
2. Implement learner-driven procedure retrieval (not just storage).
3. Implement composition operator.
4. Test whether the learner can recognize "this new task needs n-1-k" without re-search.
