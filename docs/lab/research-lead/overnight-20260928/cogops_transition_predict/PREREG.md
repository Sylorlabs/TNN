# PREREG: COGOPS-TRANSITION-PREDICT (c21)

## Hypothesis
The leadership-transition inequality from COGOPS-LEADERSHIP-TRANSITION
(BUILD-FAIL informative) is genuinely predictive, not post-hoc.
With score_s = [(c+8)·rb + (f+1)·ra]/(u+2), write mean failure cost
m_s and failure rate φ_s. Challenger W dethrones incumbent N iff:

  ra/rb < (m_N − m_W)/(φ_W − φ_N)

where ra=rt+2, rb=rc+2 are the global rescue-ledger rates.
The inequality predicts that the transition stage is monotone in
the incumbent's win count k: fewer wins → higher φ_N → higher
threshold → earlier transition. More wins → lower threshold →
later or no transition.

## Prediction method (frozen)
A minimal Zag probe (/tmp/tpv/probe.zag, throwaway, NOT committed)
formalizes the score race:
- Exact score: nsc(s) = (c+8)·rb + (f+1)·ra, f = u−w;
  argmin of nsc/(u+2) by exact integer cross-multiplication,
  lower-id tie-break (transcribed from c20h_strat_additive.zag).
- Per-position turn costs (c20-validated from DET evidence, exact):
  first@pass2: PW=2, WHOLE=1, NEED=nn;
  non-first: PW=3, WHOLE=2, NEED=2·nn, ALT=3+2·nn;
  NEED win (setup): nn.
- Setup arc: stage1 PW,WHOLE fail / NEED wins (ledger rt+=2+nn,
  rc+=2); stages 2..k NEED wins (ledger unchanged).
- Test arc: 10 stages, all fail, order by exact scores.

Probe VALIDATED on c20 (known outcomes, not used for fitting):
- D2 repro (nn=4,k=4, rt=145,rc=32): predicts transition at t7.
  c20 OBSERVED D2-7. EXACT MATCH.
- B repro (nn=3,k=3, rt=5,rc=2): predicts 0 transitions in 10.
  c20 OBSERVED 0 transitions in B1-B10. EXACT MATCH.

## Battery c21 (NEW worlds)
Builds on c20h (c20_base, c18_world, c20h_learn, strat additive).
Uses PROVEN kinds only (2,4 = setup/winnable; 8,9 = test/unwinnable).
The worlds are NEW in (k, ledger-trajectory) parameter space:
the inequality was derived from (nn=3,k=3) Block B and (nn=4,k=4)
Block D2; c21 tests (nn=4,k=2), (nn=4,k=3), (nn=4,k=12),
(nn=3,k=12), none of which appear in c20.

- c20-setup: S1A..S6B (30 stages, byte-identical to c20).
- P1a1-P1a2: 2× kind 4 in (4,613). NEED wins both.
- P1b1-P1b10: 10× kind 9 in (4,613). Unwinnable.
- P2a1-P2a3: 3× kind 4 in (4,613). NEED wins all.
- P2b1-P2b10: 10× kind 9 in (4,613). Unwinnable.
- Q1a1-Q1a12: 12× kind 4 in (4,613). NEED wins all.
- Q1b1-Q1b10: 10× kind 9 in (4,613). Unwinnable.
- Q2a1-Q2a12: 12× kind 2 in (3,613). NEED wins all.
- Q2b1-Q2b10: 10× kind 8 in (3,613). Unwinnable.
Total: 99 stages.

## Frozen predictions (from probe, deterministic)
- P1b: NEED first at t1,t2; WHOLE first at t3..t10.
  TRANSITION NEED→WHOLE at P1b-3.
- P2b: NEED first at t1..t6; WHOLE first at t7..t10.
  TRANSITION NEED→WHOLE at P2b-7.
- Q1b: NEED first at t1..t10. ZERO transitions.
- Q2b: NEED first at t1..t10. ZERO transitions.
Full per-stage orders in c21_stages_predicted.txt (frozen).

## Kill bars (frozen, must all pass)
- K1 (P1 transition): DET-STRAT chosen=2 at P1b-3; chosen=3 at
  P1b-1 and P1b-2. Direction NEED→WHOLE.
- K2 (P2 transition): DET-STRAT chosen=2 at P2b-7; chosen=3 at
  P2b-1..P2b-6. Direction NEED→WHOLE.
- K3 (Q1 no-transition): DET-STRAT chosen=3 at all Q1b-1..Q1b-10.
  Zero leadership changes in Q1b.
- K4 (Q2 no-transition): DET-STRAT chosen=3 at all Q2b-1..Q2b-10.
  Zero leadership changes in Q2b.
- K5 (k-monotonicity): P1 transition stage (3) < P2 transition
  stage (7). More incumbent wins → later transition.
- K6 (determinism): 3/3 runs byte-identical (sha256), empty stderr.
- K7 (setup identity): S1A..S6B output bytes identical to
  c20h_run1.txt stages S1A..S6B.
- K8 (clean): 0 argmin ties, 0 hedge firings across all 99 stages.

## Falsification
If K1 or K2 fails (no transition, wrong stage, or wrong direction),
the inequality's predictive claim is FALSIFIED (not merely weakened).
If K3 or K4 fails (spurious transition), the inequality's
no-transition condition is FALSIFIED. If K5 fails but K1,K2 pass,
the monotone-k prediction is revised (the threshold mechanism stands
but the k-lever is weaker than predicted).

## Constraints
Pure Zag. Safebin mandatory. Commits local, never push, explicit
pathspecs. Prereg committed before any implementation file.
3/3 byte-identical. Build on c20h (frozen learn prefix + strat).
