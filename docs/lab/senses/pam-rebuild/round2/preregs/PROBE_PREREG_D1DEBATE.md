# PROBE PREREG — intervention-family cheap probes (debate crew D-1)

Date: 2026-09-24. Committed BEFORE any probe code (same prereg commit as
PREREG_D1_DRAFT.md / PREREG_D4_DRAFT.md). Pure Zag, zero RNG, 3× byte-identical
runs with SHA-compare. Fixture basis: committed F5 fixture set
(`fixtures_ledger.txt`, SHA `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`).

The probes test the cheapest falsifiable claims in the H-PAM-7/8/10 debate.
Full-fork builds are OUT of scope.

## Probe 1 — perturbation-response warrant (H-PAM-7 core claim)

Mechanism under test: gate issues gate-chosen perturbation from repertoire
{CROP_SHIFT(k), GAIN(g)} with preregistered params; computes observed-transform
vs lawful-transform agreement within tolerance τ. Lawful model (frozen):
- GAIN g: meas' = meas·g (integer, g as fixed-point), conf' = conf.
- CROP_SHIFT k: meas' = meas, conf' = conf − edge_loss(k) (edge_loss frozen table).

Three fixture classes, generated deterministically (parameter sweeps, zero RNG):
- H (honest, n=360): the committed F5 fixtures; observed response = lawful model
  exactly. SUBCLASS Hc (complex scenes): fixtures with meas ≥ 6000 marked
  "geometrically complex" where the lawful model is wrong by construction
  (observed deviates > τ) — models F7b.
- A (static-frame injection, n=120): spoofed fixtures whose response function is
  absent — observed = perturbed bytes with NO lawful transform (meas' = meas + 997,
  conf' = conf). Models D1 Class A.
- B (driver-level spoof, perturbation-consistent renderer, n=120): spoofed fixtures
  whose observed response = lawful model exactly (adversary fakes the response).
  Models D1 Class B / F7a.

Warrant decision: WITHHOLD iff |observed − lawful| > τ for ANY perturbation in
the repertoire; else INSTALL.

COMMITTED PREDICTIONS:
- P1a: H install rate = 100%, Hc over-block = 100% of the Hc subclass (F7b
  tradeoff is real and priced in honest loss).
- P1b: Class A false-install rate = 0% (warrant withholds every static injection).
- P1c: Class B false-install rate = 100% — THE STEELMAN PREDICTION: the warrant
  cannot distinguish a perturbation-consistent renderer from honest data. If
  measured Class B install < 100%, the steelman is wrong and the mechanism has
  more discrimination than claimed.
- P1d: τ sensitivity: halving τ does not change Class B install rate (the fake
  is exact); doubling τ does not change it either. Falsifies "tune τ to fix F7a".

## Probe 2 — independence premium audit (H-PAM-8 / F8c)

Mechanism under test: two "paths" reading the same fixture record:
- Path A features = (conf, meas).
- Path B features = deterministic re-projection of the SAME record
  (conf' = (conf·3+meas) mod 9973, meas' = (meas·5+conf) mod 65521) — asserted
  "independent path", shared source by construction.
Audit: vote-conditional agreement P(agree | label) and effective-n over honest +
spoofed (Class A and B) fixtures.

COMMITTED PREDICTIONS:
- P2a: agreement = 100% on every class → independence premium = 0,
  effective-n = 1.0 (the F8c audit correctly reports "NOT INDEPENDENT —
  shared source record").
- P2b: a fusion-layer single-record spoof (one lie, consistent (conf,meas)) is
  accepted by BOTH paths → premium stays 0. If any subset shows agreement < 100%
  with premium > 0, the audit probe is broken (report as probe defect, not as
  evidence for independence).

## Probe 3 — discrimination-per-cost + repertoire coverage (H-PAM-10 / D4)

Mechanism under test: preregistered action repertoire
{REACH, PING, MOVE_SENSOR, ASK} with frozen per-class discriminating power over
the frozen percept classes {TMB-5-near, COL-4-far, TMB-backtest-wrong,
COL-backtest-wrong}. Unit costs (frozen): sensor read = 1, actuator command = 10,
latency cycle = 0.1. P10 discrimination per class = log2(install-rate ratio vs
no-intervention baseline) from the repertoire table; P7 discrimination from
Probe 1 measured rates (Class A) and 0 bits on Class B.

COMMITTED PREDICTIONS:
- P3a: repertoire coverage = classes with ≥1 discriminating action / 4 total
  < 50% with the 4-action repertoire → F10b kills by coverage alone (named,
  measured).
- P3b: discrimination-per-cost: P7 wins on cost (P10/P7 cost ratio ≥ 5× per
  check), P10 wins on Class S attacker-unpredictability — reproducing the D4
  prediction structurally. If P10's discrimination-per-cost exceeds P7's on the
  full battery, the D4 prediction is wrong.

## Kill bars for the probes themselves
- Any run's stdout SHA differing across the 3 runs → the probe is non-deterministic
  (violates the hard rule); result VOID, probe fixed or abandoned.
- Probe 1 P1c failing (Class B install < 100%) does NOT kill H-PAM-7 — it kills
  the STEELMAN's F7a formulation and narrows the debate toward "the renderer cost
  is the defense".
- Probe 2 P2a failing (premium > 0 from same-record paths) = probe defect, must
  be explained, not celebrated.
