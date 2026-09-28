# FL2 Other-Kills — White-Box Diagnosis Mini-Prereg

Status: **FROZEN** — committed before any learner internals are instrumented.
Date: 2026-09-23. Operator: Muse (subagent, FL2 other-kills diagnosis task).

## 1. Objective

Diagnose-only root-cause analysis of the five T-DEF kills from FL2 Red Team R2
(`~/workspace/fl2rt/RESULTS.md`, prereg `~/workspace/fl2rt/prereg/PREREG.md`).
Target: the current default learner only (T-DEF = `arm_gl` in
`training_paradigms/scaffold_release/gl_default/`, canonical commits
`c93b9d48` + `d5b945c7`). No fixes are designed, built, or tested here; fork
crews will do that from the diagnosis.

Micah's laws in force: deep-dive behavior (instrument internals, find root
causes, never surface-patch); figure-it-out machine, not rigid-policy-per-edge-case.

## 2. Non-goals / out of scope

- RT-A's sentinel defect already has a proper structural fix (`f3_survivor`
  skips the acted slot, no 99 default) — NOT in scope; referenced only where it
  compounds another kill's causal chain.
- The proposed upgrades (a2, a3, b1, F3) are not diagnosed; F3/a3 behavior is
  cited only as existence evidence where relevant.
- No canonical source is modified in place. All work on patched copies.

## 3. Method (frozen)

1. **Patched copies**: `orig` canonical sources copied to
   `~/workspace/fl2other/diag/build/<attack>/`; the exact RT2 attack patches
   re-applied (schedule wrapper `rt_ep_info` with RT_MODE, RT-C actuator-fault
   block, aa-line gate, per-attack `main`). Canonical branch files untouched.
2. **Instrumentation (DIAG lines, metrics-only, zero behavior change)**: pure-Zag
   trace prints inside `arm_gl` —
   - per kind-3 episode: `DIAGK3,ep,act,aa,sig_live,sig0,sig1,sig2,survivor,quar_used,provisional,committed,permanent`
   - E14 gate: `DIAGPIN,ep,stated,provisional`
   - E48 promote check: `DIAGPROM,ep,revoke_step,provisional,permanent` (inputs,
     whether or not promotion fires)
   - wedge events: `DIAGWEDGE,ep,quar_used` when a kind-3 action returns non-OK.
   
   Instrumentation uses a hand-rolled integer formatter (no behavior dependency
   on `_zag_i64_to_str` newline quirks); it reads state only, mutates nothing.
3. **Fidelity gate**: the instrumented binary with standard config (original
   `main`: arm_a + honest + lying arms) must reproduce the committed canonical
   numbers — `TN_FAILURES=0`, audit totals 267 / 269 / 271 — and its TN_CHECK
   lines (DIAG lines stripped) must be byte-identical to the committed
   `gl_default/evidence_run1.txt`.
4. **Determinism**: every binary runs twice; byte-identical stdout required
   (`cmp` clean), else the trace is discarded.
5. **Reproduction check**: each instrumented attack binary must reproduce the
   RT2 verdict metrics for its kill (nuninstall/ncommit/npromote/badep/
   revoke_step/policies per `~/workspace/fl2rt/evidence/default_<X>_run1.txt`).
6. **Purity**: pure Zag for instrumentation and runs; Python only for
   patch/run/diff glue. No `rng`/`rand`/`seed` tokens in any Zag source.

## 4. Verdicts to emit (per kill: RT-B, RT-C, RT-D, RT-E, RT-F)

For each kill the diagnosis delivers:
- **Causal chain**: episode-by-episode trace of the exact mechanism —
  which episodes, which signal values (`sig_live`, `sig0/1/2`, `aa`, `act`),
  which gate/branch fired, with DIAG line references.
- **Classification** (exactly one):
  - `MISSING KNOWLEDGE` — the learner lacks a truth/rule it could be taught
    (it has or could have the facts; the rule connecting them is absent).
  - `MISSING MECHANISM` — a general capability is absent (a whole channel of
    perception/action/verification the design never built).
  - `GENUINE ARCHITECTURAL ANNOYANCE` — inherent to the design; must be lived
    with or designed around, not fixed.
- **Evidence**: audit-trace excerpts, exact signal values, exact episode
  numbers grounding the classification.
- For `MISSING MECHANISM` verdicts: a sketch of the **general** mechanism
  (general, never per-edge-case) — sketched only, NOT built.

## 5. Kill bars reused (reproduction only, from RT2 prereg §4)

- KB-B1: silent-world lie must not promote (`nuninstall>=1 AND npromote==0`).
- KB-C1: zero false revocations on the honest stream.
- KB-D1: no wedge (`badep==0`); KB-D2: `nuninstall==0`.
- KB-E1: `pinstall_policy ∈ {0,1,2}`; KB-E2: non-policy gone by E16.
- KB-F1: promoted lie displaceable by later teaching + evidence.

## 6. Deliverables and commit order

1. **This prereg alone** (this commit).
2. `DIAGNOSIS.md` (per-kill causal chains + classifications + mechanism
   sketches) + `traces/` (byte-identical run pairs per attack) + the
   instrumented patched sources — committed to branch `tnn-native-lab` under
   `docs/lab/training_paradigms/scaffold_release/forks/gl_otherkills/diag/`
   via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`.
   No binaries, no `.zagd` caches, no `.zag-cache` committed.

## 7. Limitations

- White-box diagnosis (sources and RT2 report studied first); the traces
  confirm/refine hand-derived mechanism traces, they do not blind-discover.
- RT-C's fault model and RT-D's dense schedule are adversarial worlds, not
  observed ones; the diagnosis is about the learner's machinery, not the
  worlds' plausibility.
- Trace volume: per-episode DIAG lines for kind-3 episodes only (E15+); the
  E1–E14 teaching/calibration path is unchanged from the canonical runs and is
  covered by the fidelity gate.
