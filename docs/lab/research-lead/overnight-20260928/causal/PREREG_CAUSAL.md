# Preregistration: Causal Structure Invention (L3 Secondary Frontier)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before implementation)
**Researcher:** Causal-Invention Researcher (subagent)
**Branch:** tnn-native-lab

## Core Question

Can TNN construct predictive causal structure that does not already exist in source?

## Hypothesis

**H-CAUSAL:** A learner equipped only with generic transition machinery
(episode storage, per-variable effect induction, contradiction-driven splitting,
competing-hypothesis tracking) can, from (state, action, next-state) observations:

1. Invent a **conditional causal rule** (the "safety valve": pressurize fails iff temp==hot)
   that is not enumerated in its source;
2. Maintain **competing hypotheses** (H-temp vs H-lamp) without premature collapse
   when evidence is ambiguous;
3. **Kill the spurious hypothesis** on discriminating evidence while preserving provenance;
4. **Revise** a previously-correct rule when the world changes (law change),
   with temporal validity — not silent overwrite.

**Mechanism family:** Competing-hypothesis causal induction with contradiction-driven
refinement. Not copied from standard PGMs/RL: the hypothesis objects, ambiguity
retention, and provenance-tracked revision are the novel architectural content
under test.

## Critical Rule

**NO authored model containing the tested dynamics in the learner.**
The world generator (`causal_world.zag`, the environment) implements the true
dynamics. The learner (`causal_learn.zag`) contains only generic machinery:
episode tables, effect vocabulary {UNCHANGED, SET(c), ADD(d) with clamp},
condition conjunctions, split/merge/ambiguity/contest logic.
The learner source must not reference valve, hot, pressurize, or any
task-specific regularity. (Self-audit via grep: KB-C7.)

## World Dynamics (ENVIRONMENT ONLY — not in learner)

State variables: temp in {cold=0, warm=1, hot=2}, pressure in {low=0, high=1},
lamp in {off=0, on=1} (lamp is causally irrelevant; set by demonstrator).

Actions: heat=0, cool=1, pressurize=2, depressurize=3.

True transition function:
- heat:        temp := min(2, temp+1);               pressure, lamp unchanged.
- cool:        temp := max(0, temp-1);               pressure, lamp unchanged.
- pressurize:  IF temp==2 THEN no change (SAFETY VALVE)
               ELSE pressure := 1;                  temp, lamp unchanged.
- depressurize: pressure := 0;                       temp, lamp unchanged.

## Observation / Probe Format

`T <t> <p> <l> | <a> | <nt> <np> <nl>` — one observed transition.
`Q <t> <p> <l> | <a>` — prediction query.
Lines starting with `#` are comments (skipped).

Learner invocation: `causal_learn <obs.txt> <probe.txt>`.
Observations are cumulative across phases (the log is the persistent record);
sequence number = order of T lines. The learner rebuilds hypotheses from the
cumulative log each run (deterministic).

## Competing Hypotheses (tracked explicitly)

- **H-UNCOND:** "pressurize always sets pressure:=1" (formed Phase A).
- **H-TEMP:** "pressurize sets pressure:=1 iff temp!=hot; no change iff temp==hot"
  (candidate from Phase B split).
- **H-LAMP:** "pressurize sets pressure:=1 iff lamp==off; no change iff lamp==on"
  (spurious candidate from Phase B split; must be REFUTED in Phase B2, not silently dropped).

## Observation Sequences (FROZEN)

### Phase A — baseline regularities, no valve evidence (seq 1-10)

```
T 0 0 0 | 0 | 1 0 0    # 1: (cold,low,off) heat -> (warm,low,off)
T 1 0 0 | 0 | 2 0 0    # 2: (warm,low,off) heat -> (hot,low,off)
T 2 0 0 | 0 | 2 0 0    # 3: (hot,low,off) heat -> (hot,low,off) [saturate]
T 2 0 0 | 1 | 1 0 0    # 4: (hot,low,off) cool -> (warm,low,off)
T 1 0 0 | 1 | 0 0 0    # 5: (warm,low,off) cool -> (cold,low,off)
T 0 0 0 | 2 | 0 1 0    # 6: (cold,low,off) pressurize -> (cold,high,off)
T 1 0 0 | 2 | 1 1 0    # 7: (warm,low,off) pressurize -> (warm,high,off)
T 0 1 0 | 3 | 0 0 0    # 8: (cold,high,off) depressurize -> (cold,low,off)
T 2 1 0 | 2 | 2 1 0    # 9: (hot,high,off) pressurize -> (hot,high,off) [valve masked: already high]
T 0 0 0 | 1 | 0 0 0    # 10: (cold,low,off) cool -> (cold,low,off) [saturate]
```

### Phase B — valve revealed, lamp confounded (seq 11)

```
T 2 0 1 | 2 | 2 0 1    # 11: (hot,low,ON) pressurize -> (hot,low,on) [VALVE; lamp on]
```

### Phase B2 — discriminating evidence (seq 12-13)

```
T 2 0 0 | 2 | 2 0 0    # 12: (hot,low,off) pressurize -> (hot,low,off) [valve, lamp OFF: kills H-LAMP]
T 0 0 1 | 2 | 0 1 1    # 13: (cold,low,on) pressurize -> (cold,high,on) [works, lamp ON: kills H-LAMP]
```

### Phase C1 — law change: valve breaks, lamp off (seq 14-15)

```
T 2 0 0 | 2 | 2 1 0    # 14: (hot,low,off) pressurize -> (hot,high,off) [VALVE BROKEN]
T 2 0 0 | 2 | 2 1 0    # 15: (hot,low,off) pressurize -> (hot,high,off) [confirmation]
```

### Phase C2 — discriminating: valve broken, lamp on (seq 16-17)

```
T 2 0 1 | 2 | 2 1 1    # 16: (hot,low,on) pressurize -> (hot,high,on) [broken, lamp ON]
T 2 0 1 | 2 | 2 1 1    # 17: (hot,low,on) pressurize -> (hot,high,on) [confirmation]
```

## Probes and Expected Learner Outputs (FROZEN)

### Probe set A (obs seq 1-10)

- **P-A1:** `Q 2 0 0 | 2` -> expect `(2,1,0)`.
  Honest overgeneralization from H-UNCOND (true world: (2,0,0)). Records the
  pre-revision prediction; not scored as pass/fail, documents the rule's content.
- **P-A2:** `Q 1 1 0 | 2` -> expect `(1,1,0)`.
  Generalization to unseen state via invented effects. (KB-C2)
- **P-A3:** `Q 0 0 0 | 0` -> expect `(1,0,0)`. Recall.

### Probe set B (obs seq 1-11)

- **P-B1:** `Q 2 0 0 | 2` -> expect `WITHHOLD (ambiguous)`.
  H-TEMP predicts (2,0,0); H-LAMP predicts (2,1,0). Must NOT collapse. (KB-C4)
- **P-B2:** `Q 2 0 1 | 2` -> expect `(2,0,1)`. Recall of seq 11.
- **P-B3:** `Q 0 0 0 | 2` -> expect `(0,1,0)`. Candidates agree; predicts despite ambiguity.

### Probe set B2 (obs seq 1-13)

- **P-B2a:** `Q 2 0 0 | 2` -> expect `(2,0,0)`. H-TEMP adopted. (KB-C1)
- **P-B2b:** `Q 0 0 0 | 2` -> expect `(0,1,0)`. Old knowledge retained. (KB-C1)
- **P-B2c:** `Q 1 1 1 | 2` -> expect `(1,1,1)`. Generalization; lamp correctly ignored.

### Probe set C1 (obs seq 1-15)

- **P-C1a:** `Q 2 0 0 | 2` -> expect `(2,1,0)`. New law (lamp-off branch). (KB-C3)
- **P-C1b:** `Q 2 0 1 | 2` -> expect `(2,0,1)`. Old law retained (lamp-on branch).
  Documents the conditional-refinement hypothesis.

### Probe set C2 (obs seq 1-17)

- **P-C2a:** `Q 2 0 0 | 2` -> expect `(2,1,0)`. New law.
- **P-C2b:** `Q 2 0 1 | 2` -> expect `(2,1,1)`. New law; lamp hypothesis dead. (KB-C3)
- **P-C2c:** `Q 0 0 0 | 2` -> expect `(0,1,0)`. Unaffected knowledge. (KB-C3)

## Kill Bars (FROZEN — all must pass for H-CAUSAL to survive)

- **KB-C1 (conditional rule invention + retention):** P-B2a `(2,0,0)` AND P-B2b
  `(0,1,0)` both correct. The valve rule is invented and old knowledge survives.
- **KB-C2 (beats memorization):** P-A2 `(1,1,0)` correct. B-memorize withholds
  (state unseen). The invented effects generalize.
- **KB-C3 (law-change revision with provenance):** P-C2a `(2,1,0)`, P-C2b `(2,1,1)`,
  P-C2c `(0,1,0)` correct AND provenance log shows the full chain:
  H-UNCOND -> SUPERSEDED-by-split -> H-TEMP/H-LAMP ambiguous -> H-LAMP REFUTED ->
  contest on valve-break -> resolution with temporal validity
  (old valve episodes marked SUPERSEDED, not deleted).
- **KB-C4 (no premature collapse):** P-B1 is WITHHOLD(ambiguous), not a guess.
  Both H-TEMP and H-LAMP present in provenance at end of Phase B.
- **KB-C5 (beats unconditional baseline):** After Phase B2, on P-B2a, learner
  predicts `(2,0,0)` while B-unconditional predicts `(2,1,0)`
  (pressure majority=1). Learner correct, baseline wrong.
- **KB-C6 (determinism):** Two full runs byte-identical (SHA-256).
- **KB-C7 (no authored dynamics in learner):** `grep -iE "valve|hot|pressurize|safety"`
  on `causal_learn.zag` returns nothing task-specific (generic var indices only).
  Learner must not name the regularity it is supposed to discover.
- **KB-C8 (spurious hypothesis killed, provenance kept):** After Phase B2,
  provenance contains H-LAMP marked REFUTED (with refuting sequence numbers),
  not silently deleted.

**Verdict rule:** H-CAUSAL SURVIVES iff KB-C1..KB-C8 all pass.
Any single failure kills H-CAUSAL as stated (may survive in weakened form,
documented explicitly).

## Baselines (committed predictions)

- **B-memorize:** exact (S,A)->NS table; WITHHOLD if unseen; most-recent on conflict.
  - P-A2: WITHHOLD (unseen). P-B2a: (2,0,0) (seen seq12). P-C2b: (2,1,1) (seen seq16).
- **B-unconditional:** per (action, variable): majority next-value; tie -> "?".
  - After B2, pressurize pressure majority = 1 -> P-B2a predicts (2,1,0): WRONG.
  - After A, pressurize temp majority: values {0,1,2} tie -> P-A2 WITHHOLD.

Baselines implemented in `baselines.zag` (two modes) and checked against these
committed predictions.

## Scope and Non-Claims

- This experiment does NOT claim full L3. It tests whether a specific
  architectural mechanism (competing-hypothesis causal induction) can invent a
  conditional rule, handle a confounder, and revise on law change.
- The effect vocabulary {UNCHANGED, SET, ADD-with-clamp} is generic machinery,
  documented as a design choice and open to red-team attack.
- Variable ranges (temp 0-2 etc.) are machinery parameters, not dynamics.
- The 3-variable world is minimal by design; scaling is future work.
- P-A1's expected "wrong" output is intentional: it documents honest
  overgeneralization, a falsifiable prediction of the mechanism.

## Governance

- Prereg frozen before implementation (this commit).
- Implementation, results, and verdict in separate commits.
- Adversary/governance review by independent agents (not this researcher).
- No thresholds adjusted post-hoc. Any deviation documented as amendment.
