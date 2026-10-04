# Preregistration: Causal Structure Invention, Independent Arc (CAUSAL2)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before implementation of world2)
**Researcher:** Causal2 Researcher (subagent, independent arc)
**Branch:** tnn-native-lab

## Core Question

Can the generic competing-hypothesis learner invent a conditional causal rule
from a law family that is DIFFERENT from the safety valve of the first arc,
with no authored tested dynamics reachable from the learner?

## Hypothesis

**H-CAUSAL2:** The same generic machinery (episode storage, per-variable
effect induction over {UNCHANGED, SET, ADD-with-clamp}, contradiction-driven
splitting, competing-hypothesis tracking with ambiguity, refutation, contests
with temporal revision) can, from (state, action, next-state) observations:

1. Invent a **conditional causal rule of a new family** (the "thermal lock":
   cool fails iff pressure==high) that is not enumerated in its source;
2. Maintain **competing hypotheses** (H-pressure vs H-lamp) without premature
   collapse when evidence is ambiguous;
3. **Kill the spurious hypothesis** on discriminating evidence with provenance;
4. **Revise** through a law change (lock breaks) with temporal validity,
   including a genuine contest phase where WITHHOLD is the honest output.

## Critical Rule

**NO authored model containing the tested dynamics in the learner.**
The world generator (`world2.zag`, the environment) implements the true
dynamics. The learner is `learn2.zag`, a BYTE-IDENTICAL copy of the first
arc's `causal_learn.zag` (inherited generic component, zero modifications),
and must contain zero occurrences of the law's variables/values/task words.
(Authorship separation: the learner for this arc is the exact file that ran
the first arc, so it cannot have been tuned to the new law. Verified by
sha256 equality.)

Task words for the K2-7 audit: lock, thermal, chill, freeze, vent, exchanger,
pressure, cooling, blocked, guard.

## World Dynamics (ENVIRONMENT ONLY, not in learner)

State variables: temp in {cold=0, warm=1, hot=2}, pressure in {low=0, high=1},
lamp in {off=0, on=1} (lamp is causally irrelevant; set by demonstrator).

Actions: heat=0, cool=1, pressurize=2, depressurize=3.

True transition function:
- heat:         temp := min(2, temp+1);                  pressure, lamp unchanged.
- cool:         IF pressure==1 THEN no change (THERMAL LOCK)
                ELSE temp := max(0, temp-1);             lamp unchanged.
- pressurize:   pressure := 1;                           temp, lamp unchanged.
- depressurize: pressure := 0;                           temp, lamp unchanged.

Law change (broken=1): thermal lock disabled; cool always reduces temp.

This law differs from the first arc in three ways: the gated action is cool
(not pressurize), the gating variable is pressure (not temp), and the effect
is a blocked decrement (not a blocked set). It is expressible by the generic
machinery (single-variable equality split on s1).

## Observation / Probe Format

`T <t> <p> <l> | <a> | <nt> <np> <nl>` (one observed transition).
`Q <t> <p> <l> | <a>` (prediction query).
Lines starting with `#` are comments (skipped).

Learner invocation: `learn2 <obs.txt> <probe.txt>`.
Observations are cumulative per phase (the log is the persistent record);
sequence number = order of T lines. The learner rebuilds hypotheses from the
cumulative log each run (deterministic).

## Competing Hypotheses (tracked explicitly)

- **H-UNCOND:** "cool always sets temp:=temp-1 (clamped)" (formed Phase A).
- **H-PRESS:** "cool reduces temp iff pressure==low; no change iff pressure==high"
  (candidate from Phase B split).
- **H-LAMP2:** "cool reduces temp iff lamp==off; no change iff lamp==on"
  (spurious candidate from Phase B split; must be REFUTED in Phase B2,
  not silently dropped).

## Observation Sequences (FROZEN)

### Phase A, baseline, lock never observed, lamp always off (seq 1-10)

```
T 0 0 0 | 0 | 1 0 0    # 1: (cold,low,off) heat -> (warm,low,off)
T 1 0 0 | 0 | 2 0 0    # 2: (warm,low,off) heat -> (hot,low,off)
T 2 0 0 | 1 | 1 0 0    # 3: (hot,low,off) cool -> (warm,low,off)
T 1 0 0 | 1 | 0 0 0    # 4: (warm,low,off) cool -> (cold,low,off)
T 0 0 0 | 1 | 0 0 0    # 5: (cold,low,off) cool -> (cold,low,off) [saturate]
T 0 0 0 | 2 | 0 1 0    # 6: (cold,low,off) pressurize -> (cold,high,off)
T 0 1 0 | 3 | 0 0 0    # 7: (cold,high,off) depressurize -> (cold,low,off)
T 2 0 0 | 0 | 2 0 0    # 8: (hot,low,off) heat -> (hot,low,off) [saturate]
T 1 1 0 | 2 | 1 1 0    # 9: (warm,high,off) pressurize -> (warm,high,off) [masked: already high]
T 2 1 0 | 3 | 2 0 0    # 10: (hot,high,off) depressurize -> (hot,low,off)
```

### Phase B, lock revealed, lamp confounded (seq 11)

```
T 2 1 1 | 1 | 2 1 1    # 11: (hot,high,ON) cool -> (hot,high,on) [LOCK; lamp on]
```

### Phase B2, discriminating evidence (seq 12-13)

```
T 2 1 0 | 1 | 2 1 0    # 12: (hot,high,off) cool -> (hot,high,off) [lock, lamp OFF: kills H-LAMP2]
T 2 0 1 | 1 | 1 0 1    # 13: (hot,low,on) cool -> (warm,low,on) [works, lamp ON: kills H-LAMP2]
```

### Phase C1w, law change begins, lamp off (seq 14 only)

```
T 2 1 0 | 1 | 1 1 0    # 14: (hot,high,off) cool -> (warm,high,off) [LOCK BROKEN]
```

### Phase C1, law change confirmed, lamp off (seq 15)

```
T 2 1 0 | 1 | 1 1 0    # 15: (hot,high,off) cool -> (warm,high,off) [confirmation]
```

### Phase C2, law change, lamp on (seq 16-17)

```
T 2 1 1 | 1 | 1 1 1    # 16: (hot,high,on) cool -> (warm,high,on) [broken, lamp ON]
T 2 1 1 | 1 | 1 1 1    # 17: (hot,high,on) cool -> (warm,high,on) [confirmation]
```

## Probes and Expected Learner Outputs (FROZEN)

### Probe set A (obs seq 1-10)

- **P-A1:** `Q 2 1 0 | 1` -> expect `(1,1,0)`.
  Honest overgeneralization from H-UNCOND (true world: (2,1,0)). Records the
  pre-revision prediction; not scored as pass/fail, documents the rule's content.
- **P-A2:** `Q 0 1 0 | 1` -> expect `(0,1,0)`.
  Generalization to an unseen state via invented effects. (K2-2)
- **P-A3:** `Q 0 0 0 | 1` -> expect `(0,0,0)`. Recall.

### Probe set B (obs seq 1-11)

- **P-B1:** `Q 2 1 0 | 1` -> expect `WITHHOLD (ambiguous)`.
  H-PRESS predicts (2,1,0); H-LAMP2 predicts (1,1,0). Must NOT collapse. (K2-4)
- **P-B2:** `Q 2 1 1 | 1` -> expect `(2,1,1)`. Recall of seq 11.
- **P-B3:** `Q 1 0 0 | 1` -> expect `(0,0,0)`. Candidates agree; predicts despite ambiguity.

### Probe set B2 (obs seq 1-13)

- **P-B2a:** `Q 2 1 0 | 1` -> expect `(2,1,0)`. H-PRESS adopted. (K2-1)
- **P-B2b:** `Q 0 0 0 | 1` -> expect `(0,0,0)`. Old knowledge retained. (K2-1)
- **P-B2c:** `Q 1 0 1 | 1` -> expect `(0,0,1)`. Generalization; lamp correctly ignored.

### Probe set C1w (obs seq 1-14)

- **P-C1w:** `Q 2 1 0 | 1` -> expect `WITHHOLD (contested)`.
  Law-change contradiction under test; honest withholding required.

### Probe set C1 (obs seq 1-15)

- **P-C1a:** `Q 2 1 0 | 1` -> expect `(1,1,0)`. New law (lamp-off branch). (K2-3)
- **P-C1b:** `Q 2 1 1 | 1` -> expect `(2,1,1)`. Old law retained (lamp-on branch).
  Documents the conditional-refinement hypothesis.

### Probe set C2 (obs seq 1-17)

- **P-C2a:** `Q 2 1 0 | 1` -> expect `(1,1,0)`. New law.
- **P-C2b:** `Q 2 1 1 | 1` -> expect `(1,1,1)`. New law; lamp hypothesis dead. (K2-3)
- **P-C2c:** `Q 0 0 0 | 1` -> expect `(0,0,0)`. Unaffected knowledge. (K2-3)

## Kill Bars (FROZEN, all must pass for H-CAUSAL2 to survive)

- **K2-1 (conditional law invention and retention):** P-B2a `(2,1,0)` AND P-B2b
  `(0,0,0)` both correct. The lock rule is invented and old knowledge survives.
- **K2-2 (generalization beyond memorization):** P-A2 `(0,1,0)` correct while
  B-memorize WITHHOLDs on that probe (state never observed).
- **K2-3 (law-change revision with provenance):** P-C2a `(1,1,0)`, P-C2b
  `(1,1,1)`, P-C2c `(0,0,0)` correct AND the provenance log shows the full
  chain: H-UNCOND -> AMBIGUOUS {s1,s2} -> REFUTE s2 -> SPLIT on s1 ->
  CONTEST on lock-break (with WITHHOLD at C1w) -> RESOLVE with winner ->
  old episodes SUPERSEDED (not deleted) -> SPLIT on s2 -> MERGE.
- **K2-4 (no premature collapse):** P-B1 is WITHHOLD(ambiguous), not a guess.
  Both H-PRESS and H-LAMP2 present in provenance at end of Phase B.
- **K2-5 (beats baselines):** After Phase B2, on P-B2a, learner predicts
  `(2,1,0)` while B-unconditional predicts `(1,1,0)` (pressure majority
  delta wins); learner correct, baseline wrong. On P-A2, learner predicts
  `(0,1,0)` while B-memorize WITHHOLDs. Learner is correct-or-honest on
  every scored probe.
- **K2-6 (determinism):** Two full runs of every phase byte-identical (SHA-256).
- **K2-7 (no authored tested dynamics in learner):** `grep -iE
  "lock|thermal|chill|freeze|vent|exchanger|pressure|cooling|blocked|guard"`
  on `learn2.zag` returns nothing; additionally sha256(`learn2.zag`) equals
  sha256 of the first arc's `causal_learn.zag`, proving zero task tuning.
- **K2-8 (spurious hypothesis killed, provenance kept):** After Phase B2,
  provenance contains an explicit REFUTE of the lamp candidate for action 1
  with refuting sequence numbers, not a silent deletion.

**Verdict rule:** H-CAUSAL2 SURVIVES iff K2-1..K2-8 all pass.
Any single failure kills H-CAUSAL2 as stated (may survive in weakened form,
documented explicitly).

## Baselines (committed predictions)

- **B-memorize:** exact (S,A)->NS table; WITHHOLD if unseen; most-recent on conflict.
  - P-A2: WITHHOLD (unseen). P-B2a: (2,1,0) (seen seq12). P-C2b: (1,1,1) (seen seq16).
- **B-unconditional:** per (action, variable): majority delta vote; tie keeps
  earlier delta; unresolvable -> 0.
  - After B2, cool temp delta: -1 x3, 0 x3; tie keeps -1 -> P-B2a predicts
    (1,1,0): WRONG against true (2,1,0).
  - After A, cool temp delta: -1 x2, 0 x1 -> P-A2 predicts (0,1,0)+? state
    (0,1,0): temp 0 + (-1) clamped -> (0,1,0): correct by luck of clamp.
Baselines implemented in `baselines2.zag`, a byte-identical copy of the first
arc's `baselines.zag` (verified by sha256).

## Scope and Non-Claims

- This arc does NOT claim L3. It tests whether the generic mechanism invents
  a conditional rule from an INDEPENDENT law family, handles a confounder, and
  revises on law change. Target: bounded causal invention.
- The learner is deliberately inherited unchanged so the "independent arc"
  requirement (no authored tested dynamics reachable from the learner) is
  satisfied by construction, not by audit alone.
- The 3-variable world is minimal by design; scaling is future work.
- P-A1's expected "wrong" output is intentional: it documents honest
  overgeneralization, a falsifiable prediction of the mechanism.

## Governance

- Prereg frozen before implementation (this file is written before world2.zag).
- Implementation, results, and verdict in separate files; coordinator commits.
- Adversary/governance review by independent agents (not this researcher).
- No thresholds adjusted post-hoc. Any deviation documented as amendment.
