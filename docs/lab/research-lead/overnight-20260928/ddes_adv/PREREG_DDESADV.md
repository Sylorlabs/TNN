# PREREG: DDES Adversary (DDESADV)

Frozen before any attack implementation or sealed-world execution.
Target: DDES implementation commit 56db8d606 (ddes/ddes.zag), whose own
prereg d42294620 and BUILD-PASS result are already frozen.

## Stance

Assume the BUILD-PASS claim is false. The builder's own classification is
strong L2 (guided generation), not L3, so this adversary does not attack
an L3 claim. It attacks: (a) the "zero enumeration" claim, (b) the
soundness of the derivation on sealed inputs, (c) the authorship reading
of "guided."

## Kill bars

- K1 (hidden enumeration): static audit of ddes.zag plus the builder's
  own K-NX2 instrumentation (plans_built). KILL (attack succeeds) if any
  routine generates more than one candidate complete plan and compares
  candidates before selection, or if plans_built exceeds one per
  discriminating config on the builder's worlds. If exactly one plan is
  assembled per config and the variable loop is an inline argmin over
  derived arrivals with no candidate list, the attack FAILS on this
  vector (claim stands).

- K2 (sealed soundness world): World F, designed after the DDES freeze.
  H0 = [(X,Y,0)] (0-delay rule). H1 = [(X,Z,7)]. Both truth configs run.
  Analytic expectation under the builder's own arrival model: H0 arrivals
  [0,INF,0]; H1 arrivals [0,7,INF]; frontier selects (Y, t=0); synthesized
  plan is [S,OY] with zero waits. KILL (attack succeeds) if DDES reports
  CONVERGE-OK while eliminating the true hypothesis in either config
  (silent wrong convergence), or reports NO-DISCRIMINATING-PLAN. This
  world is outside the frozen K-NX bars, so a kill here does not
  retroactively void BUILD-PASS; it blocks promotion until repaired and
  downgrades the derivation from "sound" to "sound except at t*=0."

- K3 (authorship): static audit. DOWNGRADE-CONFIRM (attack succeeds as
  clarification) if the plan is a pure deterministic function of the
  hypothesis pair with zero learner-persistent state across worlds and
  all guidance logic researcher-written. The builder discloses this
  residual authority, so this confirms the L2 ceiling rather than killing
  BUILD-PASS. It kills any future L3 reading of DDES.

## Method

Pure Zag only. No Python. No em dashes. The K2 sealed world reuses the
frozen DDES functions verbatim (copied, not modified) with a new main;
this tests the frozen logic, not a reimplementation. Commits local, owned
path docs/lab/research-lead/overnight-20260928/ddes_adv/ only. This
prereg is committed alone before any attack code is written.

## Verdict mapping

- ATTACK-SUCCEEDS if K2 kills (soundness hole demonstrated).
- ATTACK-PARTIAL if K2 fails but K3 confirms researcher authorship
  beyond the builder's disclosure (it is already disclosed; expect
  confirmation only).
- ATTACK-FAILS if K1 finds no enumeration, K2 converges correctly on
  both configs, and K3 finds learner-authored guidance.
