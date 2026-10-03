# WAVE NOTES: wave-20260927-0221pdt (Experiment 1b retune)

## Outcome

H1 KILLED by K4 and K6. K1 passes on arithmetic (I-survive median 380 >
R median 376, margin 3.5-4 ticks, about 0.6 percent) but the invention
claim is dead: K4 fires (trivial recombination, no composed multi-step
strategy), K6 fires (no novel-composition steps exist; the clean ablation
shows drop 0 in all 12 variants). K5 was audited by the independent
red-team reviewer and did not fire. C1, C2, C3 pass; K2, K3 pass. H2 is
null by construction (I-survive and I-invent traces byte-identical in
all 12 variants: the B0 novelty bonus dominates for the full 600-tick
budget, so both arms execute the same fixed enumeration).

## What changed from EXP1 (wave-20260926-2321pdt)

- Stationary-mote ceiling removed: no stationary motes, all six move
  with |v|=1 or 2, none spawn at home. R median falls from 600 to 376.
- Literal primitive-action I arm: 2800 plans (lengths 1-4) over the
  seven primitive actions, deterministic lowest-index tiebreak, myopic
  mean-delta-E credit, novelty bonus B0=40/80. No schema-level plans.
- World retuned 3 times within the frozen M1 rules. Stopping rule was
  stated as C1/C3 passage, but retunes 1-2 left no artifacts, so the
  claim is unverifiable; K1-shopping cannot be ruled out.
- Pure Zag: no Python in any committed artifact. One incidental Python
  invocation edited a /tmp debug probe; no evidence was processed.
  (EXP2's worker had a separate pre-prereg Python breach; see wave record.)

## Key findings (independent red-team review)

1. The recorded K1 PASS depends on a void-safety reflex added during
   implementation that is absent from the frozen M2 text (which lists
   exactly two taught reflexes). Counterfactual: without it, I median
   drops to 102 with 9/12 void deaths, and K1 would KILL. The reflex is
   parity-preserving (R and P avoid void through their own machinery;
   0 void deaths each), but it is load-bearing for the recorded K1.
2. I builds a LAMP in 6/12 variants and places it in 5/12. These are
   emergent enumeration accidents, never selected or exploited, and
   causally inert (clean ablation drop 0 everywhere). They do not
   disturb K4/K6.
3. The A2 ablation as first committed was mis-specified and misreported;
   corrected in A2_ABLATION.md (clean ablation, reflex preserved).
4. Architectural lesson: with B0 dominating for the full 600-tick budget,
   I's machinery never actually selects anything. This design cannot test
   invention. Any future wave must shrink the plan space, extend the
   horizon, or decay B0 so exploitation (and genuine compositional
   choice) can occur. This is consistent with Task 1: composition is the
   broken link.
5. EXP1's published record correction: the world.zag identity-reflection
   bug (hi-side reflection algebraically the identity, motes escaping to
   infinity) was introduced in the wave-20260926-2321pdt reimplementation
   (commit 74565859f), not in the original EXP1 commit (19f97c6cb, which
   had correct bounce). EXP1's published medians describe the degenerate
   world (only the stationary mote remained edible); K1's KILL verdict is
   arithmetically valid and its direction unchanged, but the world did
   not implement its specified physics. A correction note is appended to
   EXP1's BAR_RESULTS.md.

## Commits

- Prereg 7e0326d2c, implementation 938d188cb, evidence 1010a63c3
  (branch wave-20260927-0221pdt-exp1, merged to tnn-native-lab).
- Red-team-mandated corrections: this wave's coordinator commit
  (A2_ABLATION.md rewrite, false-build-claim fixes, heuristic label
  fixes, retune-2 verifiability note, reflex-dependency record).
- Determinism: two full 60-run outputs byte-identical, SHA-256
  cb6f42af00bac4d99527b48f9039ac9878b77a79daa20fac348fd3f9ace1e11a;
  reviewer reproduced with a fresh compile (third run, same SHA).

## Queued

- EXP1c or a future wave with a real compositional-choice design
  (shrunk plan space, longer horizon, or decaying B0).
- Retune history artifacts must survive from now on (stopping-rule
  verifiability is a standing requirement).
