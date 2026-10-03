# P1 Redesign Prototype Results

## Summary

The behavioral beam search prototype implements the frozen preregistration design:
- Full-stack behavioral signatures (FNV-1a 64-bit)
- Global seen-set deduplication by signature
- BFS by program length
- Scores used only for CAP eviction

## Implementation

Source: `p1proto.zag`
- P1 stack VM (31 ops: PUSH -9..9, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, SWAP, DROP)
- Signature = concatenation of full stacks across all episodes
- Open-addressed hash table (1M slots) for global dedup
- Sorted insertion for top-CAP selection by (exact desc, mae asc)

## Results

### T0 (y=2x+1), 9 episodes, max_len=8, CAP=500

```
layer 1 cur=1 nxt=20 gen=31
layer 2 cur=20 nxt=401 gen=651
layer 3 cur=401 nxt=500 gen=13082
layer 4 cur=500 nxt=500 gen=28582
...
TASK 0 exact=2/9 len=6 prog=[IN0 PUSH:8 ADD PUSH:9 SWAP MOD]
```

- Runtime: 14 seconds
- Result: 2/9 exact (FAIL, kill bar K3 requires 9/9)
- The search finds a program with 2 exact matches, but not the solution.

### Analysis

The behavioral dedup works:
- Layer 1: 31 programs -> 20 distinct signatures (35% reduction)
- Layer 2: 651 programs -> 401 distinct signatures (38% reduction)

But the score-based retention prunes the critical stepping stone:
- [IN0, PUSH 2, MUL] has mae=1 (excellent, retained)
- [IN0, PUSH 2, MUL, PUSH 1] has mae=8 (poor, pruned from top 500)
- Without the length-4 prefix, the length-5 solution cannot be generated.

The design assumed signature dedup would preserve stepping stones, but the CAP eviction by (exact, mae) removes them before expansion. The mae score is deceptive for prefixes: a necessary prefix can have worse mae than its parent.

## Kill Bar Assessment

- K1 (preregistered): PASS (commit b236b28ff7420f64a49491e1d8d218e7689c68b4)
- K2 (pure-Zag builds and runs, zero Python, zero em-dash): PASS
- K3 (solve T0 9/9 within length 12): FAIL (achieved 2/9)

## Verdict: REDESIGN-BLOCKED

The prototype validates the behavioral signature mechanism but reveals a design flaw: score-based CAP eviction is incompatible with deceptive stepping stones. A revised design needs a retention criterion that preserves behaviorally novel prefixes even when their scores are poor.

## Proposed Next Steps

1. Investigate retention by behavioral novelty/diversity rather than score alone.
2. Consider expanding all retained programs (not just top by score) to ensure stepping stones are explored.
3. Alternatively, use a score that better predicts prefix usefulness (e.g., based on intermediate stack values, not just final output).

## Governance

- Zero Python used in implementation, testing, or analysis.
- Zero em-dash bytes in source and documentation.
- Preregistration (b236b28) strictly preceded implementation.
- No kill bar was weakened or altered.
