# Continuing Learner PoC: Streaming Concept Learner

**Date:** 2026-09-29 ~04:30 PDT
**Status:** WORKING (5/5 on interleaved stream)

## What was built

`mini_stream.zag`: A streaming version of the SEM-L3 concept learner.
Processes interleaved T (teach) and Q (query) lines in order.
Maintains incremental signatures and unifications. No reset between inputs.

## Test Stream

```
T norpal | sqz_emit | glimx
T squeezer | sqz_emit | glimx
Q PARA squeezer | sqz_emit | glimx          -> glimx OK (direct)
T norpal | sqz_glow | glowx
T squeezer | sqz_glow | glowx               -> (unification fires here)
Q PARA norpal | sqz_glow | glowx            -> glowx OK (direct)
T norpal | sqz_heat | velx
Q PARA squeezer | sqz_heat | velx           -> velx OK (via concept!)
T norpaline | sqz_heat | ferx2
Q NEAR norpaline | sqz_emit | WITHHOLD      -> WITHHOLD OK (distinguished)
Q NEAR norpaline | sqz_heat | ferx2         -> ferx2 OK (distinct recall)
```

**Score:** 5/5

## Continuing-Learner Properties

1. **Persistence:** Concept nodes (norpal~squeezer) persist across the stream.
   No reset, no relearning from scratch.
2. **Incrementality:** Unification fires as soon as Jaccard threshold is met
   (after the 4th fact). Later facts extend the concept.
3. **Transfer in stream:** The (squeezer, sqz_heat) probe arrives AFTER the
   concept is formed, and is answered via the concept (not taught directly).
4. **Near-miss robustness:** norpaline is distinguished and not merged,
   even though it arrives late in the stream.

## Architecture Notes

- **State:** signatures (per-surface), parent pointers (union-find), fact store.
- **Update:** On each T, update signature, recompute unifications (brute force;
  production would be incremental).
- **Query:** Resolve via concept, lookup, answer/withhold.
- **Pure Zag:** No Python, deterministic.

## Limitations (PoC scope)

- Brute-force reunification on each T (O(n^2); fine for PoC, not for scale).
- No lesson memory (kbc integration pending).
- No contradiction ledger (CONTRA-L3 pending).
- No active inquiry (ask-on-uncertainty pending).
- Fixed array sizes (64 surfaces, 256 facts).

## Next

- Integrate with kbc lesson memory (install lesson on prediction failure).
- Add contradiction detection (mark uncertain on conflict).
- Scale test: 100+ facts, measure reunification cost.
- Design the scheduler (event loop for fact/query/ask).
