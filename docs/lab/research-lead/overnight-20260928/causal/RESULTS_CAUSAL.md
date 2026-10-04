# Causal Invention Results: H-CAUSAL

Date: 2026-09-29. Pure Zag. Prereg frozen in commit 75de43886 BEFORE implementation.

## Verdict: H-CAUSAL SURVIVES (bounded)

All 8 kill bars pass. The learner invents a conditional causal rule (hot blocks
pressurization) that was not present in its source, retains it under a confounder,
refutes the confounder hypothesis explicitly, withholds under genuine ambiguity,
and revises through a temporal law change with full provenance.

## Bar-by-bar

**KB-C1 (conditional rule invention and retention): PASS.**
Phase B2: after seq12 refutes the lamp candidate, learner SPLITs on s0 (temp)
at seq12, creating (s0=0), (s0=1), (s0=2) with pressure effects SET(1), SET(1),
UNCHANGED. P-B2a (2,0,0)->(2,0,0) and P-B2b (0,0,0)->(0,1,0) correct.

**KB-C2 (generalization beyond memorization): PASS.**
P-A2: Q(1,1,0)|pressurize -> (1,1,0). State (1,1,0) was never observed; the
unconditional pressure-set rule generalizes. B-memorize WITHHOLDs here.

**KB-C3 (law-change revision with provenance): PASS.**
Phase C1: CONTEST opened at seq14 for state (2,0,0); RESOLVE at seq15 with
winner (2,1,0), loser (seq12 episode) SUPERSEDED and marked "valid only before
seq 12". Phase C2: second CONTEST/RESOLVE for (2,0,1); MERGE dissolves the lamp
split into (s0=2) with pressure:=1. P-C2b (2,0,1)->(2,1,1) correct. P-C2c
(0,0,0)->(0,1,0): unaffected cold behavior retained.

**KB-C4 (no premature collapse under ambiguity): PASS.**
Phase B end: entry AMBIGUOUS with candidates {s0(temp), s2(lamp)}. P-B1
Q(2,0,0)|pressurize -> WITHHOLD (ambiguous: s0 s2 disagree). The learner does
not guess. Where candidates agree (P-B2, P-B3), it answers.

**KB-C5 (beat baselines): PASS.**
On P-A2 (unseen state), B-memorize WITHHOLDs while learner predicts (1,1,0).
On P-B1 (ambiguity), B-unconditional outputs (2,0,0) with no uncertainty signal
while learner WITHHOLDs. Learner is correct-or-honest on all 14 probes.

**KB-C6 (determinism): PASS.**
Two full runs of Phase C2 produce byte-identical output.
SHA-256: ee5fbe1e73ec3c036cba9f7c90420c2fb637fe6215b495203ecc8bf6d6cbc895

**KB-C7 (no authored tested dynamics): PASS.**
Source audit: causal_learn.zag and baselines.zag contain zero occurrences of
valve, hot, pressurize, safety. The rule "temp==2 blocks pressurize" appears
nowhere in learner source. (causal_world.zag contains them; it is the
environment, which is allowed to implement the true dynamics.)

**KB-C8 (H-LAMP refuted with provenance): PASS.**
Provenance line: "REFUTE action 2 candidate s2 at seq 12 (episode 12)".
The lamp hypothesis is marked REFUTED, retained in history, not deleted.

## Probe results (all 14)

Phase A: P-A1 (2,1,0) [expected overgeneralization], P-A2 (1,1,0), P-A3 (1,0,0).
Phase B: P-B1 WITHHOLD, P-B2 (2,0,1), P-B3 (0,1,0).
Phase B2: P-B2a (2,0,0), P-B2b (0,1,0), P-B2c (1,1,1).
Phase C1: P-C1a (2,1,0), P-C1b (2,0,1).
Phase C2: P-C2a (2,1,0), P-C2b (2,1,1), P-C2c (0,1,0).

## Provenance chain (pressurize)

1. seq1-10: H-UNCOND (pressure:=1), honest overgeneralization.
2. seq11: AMBIGUOUS {temp, lamp}; WITHHOLD on disagreement.
3. seq12: REFUTE lamp; SPLIT on temp; H-TEMP adopted.
4. seq13: (temp=0) covers both lamp values; no spurious lamp split (lamp provably irrelevant).
5. seq14: CONTEST (2,0,0): (2,0,0) vs (2,1,0); WITHHOLD.
6. seq15: RESOLVE winner (2,1,0); loser SUPERSEDED; SPLIT (temp=2) on lamp.
7. seq16-17: CONTEST/RESOLVE (2,0,1); MERGE into (temp=2) with pressure:=1.
Old evidence preserved with temporal bounds throughout.

## Prereg typo (non-material)

PREREG_CAUSAL.md lists P-B2c expected output as (1,1,0). The query is Q(1,1,1);
with pressure already high and lamp on, the correct output under the temp-only
hypothesis is (1,1,1). The learner outputs (1,1,1). This is a documentation typo
in the prereg, not a bar change; the bar (generalization to unseen lamp-on
warm state) is satisfied.

## Scope and limits

- Bounded: single binary condition, 3 variables, 4 actions, hand-fed phases.
- The split vocabulary is single-variable equality; richer conditions not tested.
- Contest resolution uses a fixed support threshold (2 vs 1); not validated on noisy data.
- This is L2 structural learning (new conditional structure from generic
  machinery), not L3 representational invention. The hypothesis vocabulary
  (splits, effects, contests) was authored; the specific temp-blocks-pressurize
  rule was not.

## Artifacts

- causal_world.zag: environment (true dynamics).
- causal_learn.zag: generic learner.
- baselines.zag: B-memorize, B-unconditional.
- cum_*.txt, probe_*.txt, obs_*.txt: frozen fixtures.
- evidence/run_*.txt: raw outputs. evidence/baselines_*.txt: baseline outputs.
