# REPORT: COGOPS-TRANSITION-PREDICT (c21)

## Verdict: BUILD-FAIL (informative)

The transition inequality's predictive power was NOT cleanly tested.
Design flaws in the probe and battery invalidate K2, K3, K5; K1 and
K8 fail on hedge dynamics the probe did not model. K4 passes (weak
no-transition validation). The inequality itself is neither validated
nor falsified.

## Kill bar verdicts

- **K1 (P1 NEED→WHOLE at P1b-3): FAIL.** Observed P1b1 chosen=4
  (ALT, hedge fired), P1b2-10 chosen=2 (WHOLE). A transition occurred
  (ALT→WHOLE at t2) but the predicted incumbent (NEED) was never
  leader and the stage/direction were wrong. Root cause: with nn=4,
  k=2, the second setup stage (P1a2) produces an exact PW/NEED argmin
  tie (both 56/3), firing the hedge (c1=2>0, c3=4>0). The probe
  simulated setup stages as clean NEED wins without modeling
  selection or hedge firing.
- **K2 (P2 NEED→WHOLE at P2b-7): VOID.** Design flaw: P2a/P2b share
  the (4,613) strategy context with P1a/P1b. The probe assumed a fresh
  context per arc. The (u,w,c) history at P2a1 was inherited from P1,
  not the probe's (3,3,12). Prediction invalid.
- **K3 (Q1 zero transitions): VOID.** Same context-sharing flaw;
  Q1a/Q1b inherit (4,613) history from P1+P2.
- **K4 (Q2 zero transitions): PASS.** Q2a1 was the first use of
  (3,613) (fresh context, k=12). All Q2b1-10: DET-STRAT chosen=3,
  zero leadership changes. Matches frozen prediction.
- **K5 (P1 stage 3 < P2 stage 7): VOID** (depends on K1,K2).
- **K6 (3/3 byte-identical): PASS.** sha256
  271083aa29f6fd1619c58e7f0613f780c93dac9fd2d185833be5eea81143a3c5
  across run1/2/3; empty stderr; exit 0.
- **K7 (setup byte-identity): PASS.** S1A stage bytes identical to
  c20h_run1.txt (cmp); S1B,S2,S4,S6L,S6B same construction.
- **K8 (0 ties, 0 hedge firings): FAIL.** 2 hedge firings observed:
  P1a2 (DET-HEDGE ev=2004) and P1b1 (DET-HEDGE ev=2004), both with
  DET-TIE best=4.

## Prereg errata (documentation only, kill bars unaffected)

- PREREG.md says "c20-setup: S1A..S6B (30 stages)". Actual: 6 stages
  (S1A,S1B,S2,S4,S6L,S6B). The 30 was a miscount; the 6 stages are
  byte-identical to c20.
- PREREG.md says "Total: 99 stages" and K8 says "across all 99
  stages". Actual: 75 stages (6 setup + 69 battery). K8's intent
  ("all stages in the run") is satisfied by the count of 2 firings.

## What was learned

1. **Hedge-setup interaction:** With nn=4, a 2-win setup (k=2)
   creates PW/NEED tie at the second setup stage because NEED's win
   cost (nn=4) exactly equalizes the scores: NEED (4+8)*rb+(0+1)*ra
   vs PW (2+8)*rb+(1+1)*ra. At ra=8,rb=4: 56/3 = 56/3. The hedge
   fires, ALT is tried, and the (u,w,c) history diverges from the
   clean NEED-wins model. Any future probe MUST simulate selection
   (including hedge) in setup stages, not just assume NEED wins.

2. **Context sharing:** Strategy tables are keyed by (nn, need1-rel),
   not by experimental arc. Arcs reusing (nn,rel) inherit history.
   To test (k, ledger) parameters independently, each arc needs a
   fresh (nn,rel) — i.e., new need1 rels with world facts, or accept
   the cumulative history and model it.

3. **Q2 validates no-transition:** With k=12, nn=3, fresh context,
   the inequality predicted no transition in 10 stages; observed
   zero. This is the only clean test in c21, and it passes.

## Falsification status

Per PREREG: "If K1 or K2 fails, the inequality's predictive claim is
FALSIFIED." K1 failed and K2 is void. However, the failure is
attributable to probe/design flaws (unmodeled hedge, context
sharing), not to the inequality making a wrong prediction from
correct premises. The honest verdict is **UNTESTED**, not falsified.
A proper test requires a probe that models hedge-in-setup and a
battery with fresh contexts per arc.

## Provenance

- Battery: c21_main.zag (c20 setup lines 1-593 + 69 new stages +
  c20 summary). No new kinds; mk_goalX(4), mk_goal9, mk_goalX(2),
  mk_goal8 from c20_world_add.zag.
- Learn prefix: c21h_learn.zag cmp-identical to c20h_learn.zag.
- Base/world: c20_base.zag, c18_world.zag (frozen).
- Probe: /tmp/tpv/probe.zag (throwaway; flawed as documented).
- Build: c21_build.sh, pinned znc abed8aa1, safebin.

## Recommended follow-up

Rebuild the probe to (a) simulate full selection incl. hedge in
setup stages, (b) model context sharing OR use fresh rels per arc.
Then re-freeze and re-run. The Q2 (k=12, nn=3) no-transition result
stands as a valid data point.
