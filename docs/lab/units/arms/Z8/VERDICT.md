# VERDICT — Arm Z8 (fuzzy boundaries), Track A closeout

**Date:** 2026-09-21
**Arm:** Z8 — Fuzzy boundaries (CUT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: UNADJUDICATED** — battery never run; comparison target missing (missing items below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Boundary-error rate not ≥40% lower than arm D on the perturbation battery — carrying fuzz buys nothing; OR mean fuzz grows without bound on the revision curriculum (widen dominates tighten — kill or cap).

## Why UNADJUDICATED

- **Battery never executed.** `battery_1x.sh` (17 legs × 2 runs incl.
  `z8-perturb` and `z8-perturb-d`) is prepared at the arm root, but no
  binary was ever built from `cl/arm.zag` (1,643 lines), `docs/` is
  empty, and no work/output artifacts exist. There are zero measurements.
- **Comparison target missing.** Both clauses are comparative against
  arm D on the perturbation battery; D has published no verdict and no
  boundary-error baseline.
- **Battery definition unfrozen.** A-58 (per-chunk fuzz cap value;
  boundary-perturbation battery definition; 40% boundary-error-reduction
  bar) is an open sign-off item in frozen §12 — the perturbation battery
  the criterion names is not a frozen instrument yet.

Running the battery now would still not adjudicate: the D baseline and
the frozen A-58 definition are both absent.

## What exists

- Source: `cl/arm.zag` (1,643 lines, pure Zag); shared R33 substrates.
- Battery script: `battery_1x.sh` (mode list: m1–m7, z8-perturb,
  z8-perturb-d; double-run with stdout diff).

## What's missing (to adjudicate)

1. A built Z8 binary and a completed `battery_1x.sh` run (byte-identical
   double runs).
2. Arm D's boundary-error rate on the same perturbation battery.
3. Frozen A-58: per-chunk fuzz cap value + perturbation-battery definition.

**Result: Z8 UNADJUDICATED — specified and scripted, but never built or
measured; both kill clauses need D and a frozen perturbation battery.**
