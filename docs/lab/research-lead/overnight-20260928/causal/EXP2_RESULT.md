# Experiment Invention Results: H-EXP2

Date: 2026-09-29. Pure Zag. Prereg frozen in commit 5584811a4 BEFORE
implementation. No Python at any stage.

## Verdict: H-EXP2 SURVIVES (bounded)

The learner invents discriminating experiments for its own competing
hypotheses. Given an AMBIGUOUS causal entry, it enumerates the state
space, simulates each candidate hypothesis with its own pred_under(),
and selects the unobserved state where the resolved predictions disagree.
All four kill bars pass.

## Bar-by-bar

**K-E1 (selects a discriminating experiment): PASS.**
On S1 (cum_B.txt), the invention emits 3 ranked experiments; the TOP
PICK is state (0,0,1) | action 2. Its state has no exact episode in the
action-2 entry (episodes there: (0,0,0), (1,0,0), (2,1,0), (2,0,1)), both
candidates resolve, and their predictions differ on v1 (pressure):
s0 -> (0,1,1), s2 -> (0,0,1). This matches the preregistered prediction.

**K-E2 (inspectable trace): PASS.** Output for the top pick names each
candidate variable with its predicted next-state and the differing
variables:
```
TOP PICK: state (0 0 1) | 2
TRACE top pick:
  candidate s0: group s0==0 episodes: (0 0 0)->(0 1 0) ; predicts (0 1 1)
  candidate s2: group s2==1 episodes: (2 0 1)->(2 0 1) ; predicts (0 0 1)
  differ on: v1
```

**K-E3 (not hardcoded, not heuristic): PASS.**
(a) Source audit: the invention code (lines 1002+, new main and helpers)
contains no literal triple encoding (0,0,1) or (0,0,0); enumeration uses
vmax() bounds and the learner's own pred_under. Verified by grep.
(b) On S0 (exp_null.txt, no ambiguity) the program emits
"NO AMBIGUITY: no competing hypotheses, nothing to invent." and no pick.
(c) On S2 (exp_obs2.txt, mirror) the same binary picks (0,0,0) | 2,
a different answer: ranked list is [(0,0,0), (2,0,1)]. Hardcoding of the
S1 answer is refuted.

**K-E4 (determinism): PASS.** 3 consecutive runs byte-identical per
fixture (md5: S1 a8d9e86defe445bba4d9eaa1a380be53,
S2 d8b5a64949de00f524c51ee79f398f1b,
S0 737a0a4eafe8a8be54c824630e05cb4f).

## Correctness against the true world (exploratory, not a bar)

The true Phase-B dynamics (causal_world.zag): pressurize sets pressure:=1
unless temp==2 (safety valve). The invented S1 experiment (0,0,1) | 2 has
temp cold, so the true outcome is (0,1,1): it matches s0's prediction and
refutes s2's. The experiment genuinely discriminates, and s0 (temp) is the
true hypothesis.

Notable correspondence: the original H-CAUSAL researcher hand-supplied
Phase B2's discriminating episode as `T 0 0 1 | 2 | 0 1 1`. The learner
independently re-invented exactly that experiment from the Phase-B
ambiguous state, with no knowledge of Phase B2.

## Theoretical result (pre-registered, confirmed by construction)

Two genuinely competing single-variable candidates always admit a
discriminating state in the enumerated space (proof sketch in
PREREG_EXP2.md). Corollary: an "ambiguity with agreeing predictions
everywhere" null fixture is unconstructible; the honest null is
abstention on unambiguous input, which S0 tests. The S2 mirror further
confirms the mechanism is not tied to one variable pair.

## Scope and limits

- Bounded L2: the hypothesis vocabulary (splits, fx codes), the
  candidate set, and the enumeration space are authored. What the learner
  contributes is new: using its own uncertainty to select the missing
  observation (Level D, self-directed evidence). This is experiment
  SELECTION from enumerated candidates, not experiment CONSTRUCTION
  (no new actions or variables invented). Not L3.
- Setup planning out of scope: the invention selects (state, action),
  not the action sequence to reach the state. In this domain the lamp is
  demonstrator-controlled (no lamp-toggle action exists), so the
  experiment is necessarily posed hypothetically.
- One ambiguous entry per action assumed; fixtures contain exactly one.
- Ranking is (ndiff DESC, state index ASC); ndiff never exceeded 1 in
  these fixtures, so index order decided. Adversarial fixtures could
  probe ranking pathologies.

## Artifacts

- causal/exp_invent.zag: implementation (machinery copied verbatim from
  causal_learn.zag; new main + 3 helpers; 0 em dashes).
- causal/exp_obs2.txt, causal/exp_null.txt: frozen fixtures (prereg).
- causal/cum_B.txt: reused frozen fixture (S1).
- evidence/exp2_s1.txt, exp2_s2.txt, exp2_s0.txt: raw outputs.
- PREREG_EXP2.md: frozen prereg (commit 5584811a4).

## Red-team / follow-up notes

- Mirror variants with ambiguity on other variable pairs (e.g. s0 vs s1).
- Adversarial fixtures: top pick unreachable, or ndiff ranking gamed by
  degenerate predictions.
- Port into the unified learner: route -> invent -> execute -> revise
  closed loop (the researcher currently supplies the discriminating
  episode by hand; H-EXP2 is the active counterpart).
- Experiment construction: inventing new actions or variables, not just
  selecting states.
