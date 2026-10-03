# Red Team Preregistration: H-CAUSAL Adversarial Attacks

**Date:** 2026-09-29 PDT
**Role:** Causal-Invention Adversary (independent)
**Status:** FROZEN before execution
**Target:** H-CAUSAL claim (commits 75de43886 prereg, 0df42f648 impl, 8ead2ca68 fixtures, 902e92330 verdict)

## Hypothesis under attack

H-CAUSAL: A learner with only generic transition machinery induces the
conditional rule "pressurize fails iff temp==hot", holds competing hypotheses
without premature collapse, refutes a spurious confounder hypothesis, and
revises on law change with temporal provenance.

Researcher verdict: SURVIVES (bounded L2), 14/14 probes, KB-C1..KB-C8 PASS.

## Adversarial attacks (frozen)

### C-A1: Source inspection for smuggled dynamics
- Grep causal_learn.zag for task-specific strings: valve, hot, pressurize,
  safety, and for hardcoded variable-index/value magic numbers that could
  encode the rule (e.g., literal 2 comparisons tied to action 2).
- Read the split/refute/contest logic: does the learner DISCOVER the
  condition, or does the code path assume a particular shape (single-variable
  equality on the state) that makes the specific rule the only expressible one?
- PREDICTION: source will be name-clean but the split vocabulary
  (single-variable equality) may be narrow enough that the "invented" rule is
  the only one the machinery can express. If so, document as scope limit.

### C-A2: Hypothesis vocabulary authored
- The researcher admits the vocabulary (splits, effects, contests) was authored.
- Attack: enumerate the hypothesis space the machinery can express for this
  world: 3 variables x (UNCHANGED, SET, ADD) effects x single-var splits.
  Count distinct rules expressible. If the true rule is one of a small handful
  the vocabulary makes salient (e.g., single-var equality splits with
  UNCHANGED vs SET), the "invention" is selection from a small menu.
- PREDICTION: expressible space is small (dozens of rules); document the count
  and whether the target rule is privileged by the vocabulary design.

### C-A3: Hand-fed phases
- The researcher admits phases are hand-fed (A, B, B2, C1, C2 in order).
- Attack: construct an INTERLEAVED observation file: merge all 17 T-lines in a
  shuffled order (deterministic seed via shell), re-run the learner, and check
  whether the same final rule is induced. If the mechanism depends on phase
  ordering (e.g., the contest/support logic assumes recency patterns the phases
  engineer), interleaving should break it.
- Also: remove seq 11 (the single ambiguous valve reveal). Does the learner
  still find the valve rule from seq 12-13 alone?
- PREDICTION: interleaved order may break contest resolution or ambiguity
  tracking. Document PASS/FAIL honestly.

### C-A4: Simpler baseline reproduction
- Independently re-run baselines.zag (both modes) on all probe sets and verify
  the researcher's committed baseline predictions (B-memorize WITHHOLDs on
  P-A2; B-unconditional wrong on P-B2a).
- Then implement a THIRD baseline the researcher did not: B-majority-conditional
  (per (action, state-variable=value) majority next-value table). Check whether
  it matches all 14 probes. If a simple conditional-majority table reproduces
  14/14, the "competing hypotheses + provenance" machinery adds nothing
  observable over a lookup table.
- PREDICTION: B-majority-conditional will match 13-14/14 probes. Document exact
  count and which probes (if any) require the researcher's machinery
  (candidates: P-B1 WITHHOLD under ambiguity, provenance chain).

### C-A5: Law-change revision vs re-run
- Inspect the contest/resolve code path: when seq14-15 contradict the (s0=2)
  UNCHANGED entry, does the mechanism (a) mark old episodes SUPERSEDED with
  temporal bounds and keep them queryable, or (b) effectively overwrite?
- Attack: after Phase C2, query a probe about the OLD law explicitly, e.g.
  add a probe "Q 2 0 0 | 2 @seq12" style if supported; if not supported,
  document that temporal provenance is write-only (logged but not usable).
- Check: does any probe actually REQUIRE the old episodes to be retained?
  If all 14 probes are answerable from the newest entries alone, the
  "provenance" is decorative.
- PREDICTION: provenance is logged but no probe exercises it; revision is
  functionally a re-run with a log line.

### C-A6: Stronger confounder
- The lamp confounder at seq 11-13 is weak: lamp correlates with the valve
  exactly once (seq11) and is then cleanly separated by seq12-13.
- Attack: construct a STRONGER confounded fixture where lamp==on accompanies
  EVERY valve-blocked episode for 4 consecutive sequences before the
  discriminating evidence arrives. If the learner's refutation logic requires
  only a single counterexample, it passes; if the ambiguity machinery
  collapses or the support threshold misfires under sustained confounding,
  document the failure.
- PREDICTION: learner handles it (single counterexample suffices), but the
  test is worth running to confirm the refutation is evidence-driven rather
  than phase-driven.

## Kill criteria

- H-CAUSAL is KILLED (as stated) if any of:
  - K-CA1: task dynamics found in learner source (hardcoded rule).
  - K-CA2: B-majority-conditional matches 14/14 (machinery adds nothing).
  - K-CA3: interleaved observations break induction (phase-dependent).
  - K-CA4: a probe answer requires machinery the baselines lack AND the
    learner fails it on the stronger confounder.
- H-CAUSAL is DOWNGRADED (not killed) if:
  - Vocabulary space is small but the rule was still induced from data
    (bounded L2 stands, "invention" language weakened).
  - Provenance is decorative (logged, unused by any probe).

## Governance

- This prereg is committed BEFORE any attack execution.
- All attack code in pure Zag/shell. No Python.
- Raw outputs committed. Verdict in a separate commit.
