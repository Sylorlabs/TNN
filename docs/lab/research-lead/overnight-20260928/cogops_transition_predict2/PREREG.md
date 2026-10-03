# PREREG: COGOPS-TRANSITION-PREDICT-2 (c22)

## Hypothesis
The leadership-transition inequality from COGOPS-LEADERSHIP-TRANSITION
is genuinely predictive, not post-hoc. With score_s = [(c+8)·rb +
(f+1)·ra]/(u+2), write mean failure cost m_s and failure rate φ_s.
Challenger W dethrones incumbent N iff:

  ra/rb < (m_N − m_W)/(φ_W − φ_N)

where ra=rt+2, rb=rc+2 are the global rescue-ledger rates.
The inequality predicts the transition stage is monotone in the
incumbent's win count k: fewer wins → higher φ_N → higher
threshold → earlier transition. More wins → lower threshold →
later or no transition.

## Why c21 did not test this (design flaws, fixed here)
c21 BUILD-FAIL (informative). Two flaws:
1. The probe hardcoded setup outcomes ("PW,WHOLE fail / NEED wins")
   without simulating selection. With nn=4,k=2 the second setup
   stage is an exact PW/NEED argmin tie (56/3 = 56/3 at ra=8,rb=4),
   firing the hedge; the probe never modeled it. FIX: the c22 probe
   simulates full selection (argmin + hedge gate) in EVERY stage,
   and updates the rescue ledger WITHIN each stage (the within-stage
   ra/rb update changes the selection order; c21 P1b1's observed
   ALT,PW,NEED,WHOLE order requires it).
2. Strategy tables are keyed by (nn, need1-rel), not by arc. c21's
   P2/Q1 arcs inherited (4,613) history from P1. FIX: each c22 arc
   uses a FRESH (nn,rel) context via new need1 rels (617, 619, 621,
   623) with world facts mirroring rel 613's 3-fact pattern, so
   per-need dynamics are identical and only the context key differs.

Additionally, c22 uses nn=3 for all arcs: the nn=4 setup-stage-2
exact tie (structural: (nn-2)*rb = ra after one setup win iff
nn=4) is avoided by construction, and the probe predicts zero
hedge firings (K8).

## Probe (frozen, committed: c22_probe.zag)
Standalone Zag formalization of the score race:
- Exact score: nsc(s) = (c+8)·rb + (u-w+1)·ra; argmin of
  nsc/(u+2) by exact integer cross-multiplication, lower-id
  tie-break (transcribed from c20h strat_sel).
- Hedge: at initial selection, PW+NEED exact tie for the argmin
  with c1>0 and c3>0 (in-context evidence) selects ALT=4.
- Per-turn (u,w,c) updates; rescue ledger: the first strategy's
  turn accrues nothing; each later strategy's turn adds (tc,1)
  to (rt,rc) BEFORE the next selection within the same stage.
- Turn-cost model (calibrated on c21 DET evidence, exact):
  SETUP (NEED-winnable): PW (fail,2)/(fail,3); WHOLE (fail,1)/
  (fail,2); NEED (win,nn); ALT (win,2+nn)/(win,3+nn)
  [first / non-first].
  TEST (unwinnable): PW (fail,2)/(fail,3); WHOLE (fail,1)/
  (fail,2); NEED (fail,nn)/(fail,2nn); ALT (fail,2+2nn)/
  (fail,3+2nn) [first / non-first].
- Assumptions: vr==3 (quiescence) never occurs; prior does not
  change calibrated costs; goal kinds behave as labeled.

VALIDATION (pre-freeze, not fitted to c22): the probe replays
c21's full 69-stage battery observed history (shared (4,613)
context across P1/P2/Q1, fresh (3,613) for Q2, global ledger).
Result: probe predicts c21's observed DET-STRAT chosen value at
ALL 69 battery stages (byte-exact), including the P1a2 and P1b1
hedge firings (2 predicted, 2 observed) and the P1b1
ALT,PW,NEED,WHOLE within-stage order. The probe is validated on
data it was not fitted to (the selection/hedge/ledger logic is
transcribed from source, not fitted; turn costs are calibrated
on disjoint DET comparison counts).

PILOT (pre-freeze): new rels 617/619/621/623 verified
NEED-winnable (setup) / unwinnable (test) with costs identical
to the 613 versions (see pilot output in REPORT).

## Battery c22 (NEW worlds)
Builds on c20h (c20_base, c18_world, c20h_learn, strat additive;
frozen). Uses NEW goal constructors mk_goal2r/mk_goal8r
(c22_world_add.zag) with fresh need1 rels per arc. All arcs nn=3.
The (k, ledger-trajectory) parameters are NEW: the inequality was
derived from (nn=3,k=3) Block B and (nn=4,k=4) Block D2; c22 tests
(nn=3,k=2), (nn=3,k=3), (nn=3,k=12) x2, none of which appear in
c20/c21 as fresh-context arcs.

- c20-setup: S1A..S6B (6 stages, byte-identical to c20/c21).
- P1a1-P1a2: 2x mk_goal2r (3,617). NEED wins.
- P1b1-P1b10: 10x mk_goal8r (3,617). Unwinnable.
- P2a1-P2a3: 3x mk_goal2r (3,619). NEED wins.
- P2b1-P2b15: 15x mk_goal8r (3,619). Unwinnable.
- Q1a1-Q1a12: 12x mk_goal2r (3,621). NEED wins.
- Q1b1-Q1b10: 10x mk_goal8r (3,621). Unwinnable.
- Q2a1-Q2a12: 12x mk_goal2r (3,623). NEED wins.
- Q2b1-Q2b10: 10x mk_goal8r (3,623). Unwinnable.
Total: 6 + 12 + 18 + 22 + 22 = 80 stages.

## Frozen predictions (from probe, deterministic; full per-stage
## table in c22_stages_predicted.txt)
- P1: setup a1 chosen=1 (PW), a2 chosen=3 (NEED), 0 hedge.
  Test: chosen=3 (NEED) at t1..t7; chosen=2 (WHOLE) at t8..t10.
  TRANSITION NEED→WHOLE at P1b-8. ntrans=1.
- P2: setup a1 chosen=1, a2..a3 chosen=3, 0 hedge.
  Test: chosen=3 at t1..t11; chosen=2 at t12..t15.
  TRANSITION NEED→WHOLE at P2b-12. ntrans=1.
- Q1: setup a1 chosen=1, a2..a12 chosen=3, 0 hedge.
  Test: chosen=3 at all t1..t10. ZERO transitions.
- Q2: setup a1 chosen=1, a2..a12 chosen=3, 0 hedge.
  Test: chosen=3 at all t1..t10. ZERO transitions.
- Hedge firings predicted: 0 (all arcs, all stages).

## Kill bars (frozen, must all pass)
- K1 (P1 transition): DET-STRAT chosen=3 at P1b-1..P1b-7;
  chosen=2 at P1b-8..P1b-10. Exactly one leadership change,
  NEED→WHOLE, at P1b-8.
- K2 (P2 transition): DET-STRAT chosen=3 at P2b-1..P2b-11;
  chosen=2 at P2b-12..P2b-15. Exactly one leadership change,
  NEED→WHOLE, at P2b-12.
- K3 (Q1 no-transition): DET-STRAT chosen=3 at all Q1b-1..Q1b-10.
  Zero leadership changes in Q1b.
- K4 (Q2 no-transition): DET-STRAT chosen=3 at all Q2b-1..Q2b-10.
  Zero leadership changes in Q2b.
- K5 (k-monotonicity): P1 transition stage (8) < P2 transition
  stage (12). More incumbent wins → later transition.
- K6 (determinism): 3/3 runs byte-identical (sha256), empty stderr.
- K7 (setup identity): S1A..S6B output bytes identical to
  c21h_run1.txt stages S1A..S6B.
- K8 (clean): 0 DET-HEDGE events across all 80 stages.
- K9 (probe fidelity): the probe's per-stage chosen predictions
  match observed DET-STRAT at every battery stage (74 stages);
  0 mismatches. (K1-K4 imply this for test stages; K9 extends it
  to setup stages, where the probe predicts a1 chosen=1 then
  NEED.)

## Falsification
If K1 or K2 fails (no transition, wrong stage, or wrong
direction), the inequality's predictive claim is FALSIFIED (not
merely weakened). If K3 or K4 fails (spurious transition), the
inequality's no-transition condition is FALSIFIED. If K5 fails
but K1,K2 pass, the monotone-k prediction is revised (the
threshold mechanism stands but the k-lever is weaker than
predicted). If K9 fails while K1-K5 pass, the probe's setup model
is wrong but the inequality's test-block predictions stand.

## Constraints
Pure Zag. Safebin mandatory. Commits local, never push, explicit
pathspecs. Prereg committed before any implementation file.
3/3 byte-identical. Build on c20h (frozen learn prefix + strat).
