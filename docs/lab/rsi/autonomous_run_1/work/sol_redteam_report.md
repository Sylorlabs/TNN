I’ll separate the claims the experiment actually establishes from the stronger claims in the brief. The key distinction is that real-battery verification can catch some regressions, while the constitution gate only protects one narrow transition and the proxy search only supports transfer across an assumed generator family.## Attack 1: C1 can majority-vote into the wrong install

Construct a conflict item:

- Old installed value: `10`
- Newly taught value: `20`
- Correction target: retain `10`
- Default policy verdict: `WITHHOLD`
- Evidence:
  - `20 > 10`, trusted, from source A
  - `20 > 10`, trusted, from source A's duplicated/stale record
  - `10 > 20`, trusted, from the authoritative correction record

C1 sees two trusted relations supporting `20` against the default and one opposing relation, so it overrides `WITHHOLD` and installs `20`. That is wrong: the correction target says the valid value is `10`.

The mechanism is not merely “bad data.” C1 assumes that a numerical majority among trusted relations is meaningful. It does not test independence, recency, provenance authority, duplication, or whether the relations answer the same question. Two correlated stale records can outvote one authoritative correction. The real battery result only shows that this failure was absent from those 24 items.

## Attack 2: V2 misses corruptions that preserve the install/withhold boundary

V2 only vetoes a candidate when a real-battery `WITHHOLD` becomes an `INSTALL`. Consider a candidate that changes the value-selection rule for cases where the current champion already decides `INSTALL`:

- Old installed value: `7`
- Newly taught value: `9`
- Correct verdict: install `9`
- Candidate behavior: still returns `INSTALL`, but installs `7`

This is a corruption, but V2 does not veto it because the verdict transition is `INSTALL -> INSTALL`, not `WITHHOLD -> INSTALL`.

The finite real-battery verifier may catch that particular instance if the battery contains it. It will not catch the same corruption on an unrepresented case. For example, the candidate could preserve every result on the 24 real items while reversing all installs for a new relation pattern. Thus V2 is not a general safety invariant; it protects one constitutional condition over one finite test set. It says nothing about wrong installed values, wrong correction targets, corrupted state updates, or latent out-of-distribution failures.

C4 has a related compositional risk. Because it decides whether to skip consultation using the current policy's verdicts, a later kept change can alter those verdicts without changing C4's skip logic. A future modification could therefore make C4 skip a consultation that is newly necessary. The current run did not demonstrate that this cannot happen; it merely stopped before such a composition was attempted.

## Attack 3: “No help” is false in the relevant sense

The candidate search space was human-designed. Humans analyzed the source, identified the five candidate shapes, selected the proxy-battery family, defined the acceptance bars, wrote the constitutional restriction, chose the verifier's fields and tolerances, and supplied the stopping rule. The deterministic deliberator then selected among five pre-shaped interventions.

That is autonomous execution and autonomous selection, but not autonomous discovery of the improvement space. The result is better described as human-shaped bounded search with no runtime consultation. Determinism does not change that classification. A deterministic optimizer over a manually selected set of hypotheses is still dependent on human hypothesis generation.

## Verdict: PARTIAL

**Why YES:** TNN did improve the measured champion without violating the tested constitutional rule. On the stated 24-item real battery, it went from `22/24` accuracy, `2` wrong installs, and cost `424` to `24/24`, `0` wrong installs, and cost `384`. The changes were deterministic, reproduced across five runs, composed successfully in this run, and did not alter the specified distractor batteries or files outside the run directory.

**Why NO:** The experiment does not establish that TNN improved itself generally or “without corrupting itself at all.” C1 encodes an unsafe majority heuristic, V2 covers only `WITHHOLD -> INSTALL`, C4 is not robust to later policy composition, and the search space, proxy distribution, safety criteria, and stopping condition were all human-specified. Exact prediction from the same `decide()` logic demonstrates implementation fidelity, not intuition; proxy-to-real transfer remains an unproven generalization from one handmade generator family. The three barren rounds show local exhaustion under the supplied candidates, not convergence over the hour or global safety.

**Final answer: PARTIAL.**
