# Bounded self-architecture revision in R6

## What happened

R6 executed a two-step revision sequence rather than accepting the first
improvement:

1. **Unprotected schema candidate:** large one-shot gain, unacceptable
   established-language regression; rejected.
2. **Protected support-gap candidate:** slightly lower immediate one-shot score,
   but no established-language regression, minimal sensory regression, better
   compute, deterministic save/reload; promoted on hidden seeds.

The controller scored candidates on new-label transfer, similar-label
interference, delayed retention, contradiction resistance, established-language
regression, sensory regression, memory, compute, and state reload.

## What is genuinely established

- A failure vector triggered architecture search rather than more blind training.
- Competing candidate continuations were evaluated without overwriting the
  accepted baseline.
- A tempting high-scoring branch was rolled back after regression.
- The accepted revision was re-tested on seeds unavailable to selection.
- The old and new mechanisms coexist contextually.
- The accepted state can be serialized and reloaded.

## What is not established

The mutation vocabulary and promotion objective are still supplied by the
research harness. TNN did not invent arbitrary new source code, prove the safety
of its own verifier, recursively redesign every layer, or improve itself without
an externally bounded candidate grammar.

Therefore:

```text
BOUNDED_SAR = PASS
CONTEXTUAL_ARCHITECTURE_REVISION = PASS_RESEARCH
OPEN_ENDED_RECURSIVE_SELF_IMPROVEMENT = NOT_MET
SAFE_ARBITRARY_SELF_REDESIGN = NOT_MET
```

## Next recursive step

R6 itself exposes the next target: repeated exposures improve immediate accuracy
but eventually damage delayed retention. The next self-revision loop should
infer a saturation variable from marginal information gain, cross-modal
agreement, novelty, source independence, and delayed replay, then choose whether
to consolidate, request another example, re-inspect the sensors, or stop.
