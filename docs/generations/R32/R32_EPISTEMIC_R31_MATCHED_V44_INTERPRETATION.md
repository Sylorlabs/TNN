# R32 V44 — Oracle-Beneficial Fresh-Stream Option Audit

Status: **REFERENCE_ONLY / OPTION-COMPLETION FAILURE CONFIRMED**

V44 replays the exact 1,400 fresh V41 episodes and computes, for evaluation only, the optimal initial reusable-evidence option advantage under actual delayed resource opportunity loss. Delayed consensus, desired answer, resource regime, and future option value never enter V38/V40 decisions.

## Economic boundary

Only **232 / 1,400 = 16.57%** of initial states have positive multi-trial evidence-option value under the sampled resource contexts. Mean initial option advantage across all episodes is **-0.4031**. Thus a high overall initial inspection rate would be irrational; much of V41's abstention is economically correct rather than an architectural failure.

## Initial recognition

Among the 232 evaluator-confirmed beneficial starts:

- V38 initiates evidence acquisition on **29.74%**;
- V40 initiates on **36.64%**.

For resolvable beneficial starts alone:

- V38 initiation recall: **31.65%**;
- V40 initiation recall: **38.99%**.

The V40 horizon state therefore produces a real initiation gain.

## Completion failure

The gain does not reach behavior:

- V40 final success on all oracle-beneficial starts: **6.90%**;
- V40 final success on resolvable oracle-beneficial starts: **0.92%**;
- V40 success conditional on having initiated: **2.35%**.

V38 is similarly weak: **7.33%** overall beneficial-start success and **4.35%** success conditional on initiation.

The cause is visible in temporal depth. The retained terminal controller often needs approximately:

- **3–5 trials** for unstable-then-stable cases;
- **7–9 trials** for replacement/reversal cases;

before it chooses the correct terminal state. V40 acquires only **0.694** trials on average even among oracle-beneficial starts, then re-evaluates the one-step action and abandons the evidence sequence.

## Safety boundary

V40's extra initiation is not catastrophic:

- non-beneficial false acquisition: **0.2046**;
- non-beneficial final UNKNOWN: **0.9127**;
- no-unique final UNKNOWN: **0.8850**;
- no runaway acquisition in V41.

## Causal classification

**Temporally extended option execution / commitment failure.** Initial option recognition is imperfect but directionally improved by V40. The dominant loss occurs after initiation: the controller treats every evidence trial as a fresh isolated action and exits during the transient negative-value valley before replacement/reversal evidence can stabilize.

This does not justify a fixed probe count. The required mechanism is a TNN-controlled evidence option with:

- an internal `option_active` state created by its own initiation decision;
- a separately learned continuation/termination value;
- termination from delayed regret, resource shadow price, and horizon hazard;
- no condition label or externally imposed duration.

## Decision

- Retain V40 for option initiation.
- Retain the terminal UNKNOWN controller.
- Do not increase a global action threshold or impose a minimum number of trials.
- Next causal arm: collect on-policy continuation states only after V40 itself initiates. Train a continuation/termination value model from delayed option regret. Deploy it as a temporally extended reusable-evidence option and compare against V40's current per-step re-initiation on fresh streams.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
