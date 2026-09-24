# Dumb-Stuff Audit (WORKSTREAM D, §4 of PREREG.md)

Date: 2026-09-24. Standing rule: "Intelligence should never be fooled by
dumb stuff." Three legs: A1 (K6 paraphrase battery on the three-worlds
scale model), A2 (canonical `gl_learner` paraphrase), A3 (static review
of the actual RT-B–F winning mechanisms for hardcoded fragility).

## A1. K6 battery on the scale model — PASS

Perturbations, applied to every fixture × mechanism (224 runs):

- **D1** all steps shifted +7 (world events only; learner constants fixed).
- **D2** one silence step (44) duplicated.
- **D3** probe identities reordered (20/25/30 → 30/20/25 logical order).

Results (verified by `verify.py` against predicted tables):

- **Zero verdict flips**: CLASSIFY identical across all 168
  fixture×mechanism×perturbation cells. No mechanism changed its
  three-world verdict under any paraphrase.
- All 672 perturbed K1–K4 cells matched the predicted tables. D2/D3 are
  pure paraphrases (all cells identical to canonical). D1's +7 shift
  moves F-W1a/F-W1f evidence across the LEASE boundary (45→52 vs LEASE
  48) — a genuine timing change, not a paraphrase — and the mechanisms
  respond exactly as the frozen decision procedure prescribes
  (abandon-then-stale instead of wait-then-uninstall; the three K2
  flips were predicted before being observed, see RESULTS.md §4).
- D3 note: the harness observes probes in chronological order regardless
  of logical probe identity, so D3 tests identity-reordering, not
  chronology-reordering — documented as a limitation of the compact
  model, not a mechanism defect.

**Verdict: no mechanism was fooled by dumb stuff. No fixes needed.**

## A2. Canonical gl_learner paraphrase — PASS

Experiment: copy of canonical
`training_paradigms/scaffold_release/gl_default/` compiled and run
against a copy with a semantics-preserving paraphrase — the values of
two persist-novel episodes swapped (`ep=49: 649→653`, `ep=53: 653→649`).
ET_PN keys are never contradicted and no check reads their values, so
the paraphrase is semantics-preserving by construction.

Result: **byte-identical stdout** —
`sha256 c45ea5cccff592039e3a970eadc6bccb750067381c0ae62580bf2857b87b90ba`
both runs, 78 TN_CHECK lines, `TN_FAILURES,0` both runs. The canonical
learner is not fooled by key/value-assignment paraphrases.

Caveat (honest): the canonical binary prints check lines, not the raw
audit ledger, so byte-identical stdout is a weaker proxy than a ledger
hash. No instrumentation was added; the check-line comparison stands as
reported, not overstated. Evidence: `a2_base_out.txt`, `a2_pert_out.txt`
(build dirs removed after the run; only the two outputs are committed).

**Verdict: PASS. No fix needed.**

## A3. Static review of the RT-B–F winning mechanisms — no defects found

Reviewed the actual winning fork sources for the classic dumb-fragility
patterns: hardcoded episode constants, id whitelists, exact
episode/order assumptions, fixed probe schedules that a trivial
renumbering or reordering would defeat. Mechanism-level defects would be
fixed; none were found. Findings filed below.

### RT-B winner: F1 endogenous retrievability law-check (`rtb/build.py`)

Core: after acting, the taught `(k,v)` must be retrievable from the
learner's **own** store (`tn_main_has(...) || tn_quar_has(...)`); if not,
the same eliminative survivor machinery uninstalls. Names no rule,
names no episode, names no id — it checks the actual acted `(k,v)`.
**Robust to renumbering, reordering, and paraphrase.** (Known
non-dumb limitation, already in the RT-B report: retrievable-yet-wrong
remains uncatchable — inherited RT2 limitation, not dumb-fragility.)

### RT-C winner: F1 act→verify→interpret (`rtc/forks/f1/gl_learner.zag`)

Core: `gl_effect_landed(act,k,v,...)` — one predicate per executable
policy (CONTEST/REKEY/OVERWRITE); no contradiction signal is valid
until the acted policy's expected world effect is confirmed present. No
calendar constants in the fix logic (the `ep==14/48` occurrences are the
inherited canonical lifecycle, not the fix). **Robust.** Note: a
genuinely *new* policy needs a new predicate branch — that is an
architecture change, not a paraphrase; filed, not fixed.

### RT-D winner: F2 refuse-new-entries-loudly (`rtd/forks/f2/gl_learner.zag`)

Core: on store pressure, refuse the insert, audit loudly
(`TN_PRESSURE`), represent degraded state as a fact about itself
(`pressured` flag → verification DEFERRED, not failed). No calendar
constants in the fix logic. **Robust.** The rigid R1 alternative was
already killed on scope (byte-identical to canon on the generalization
probe) — the exception-list failure the debate predicted.

### RT-E winner: F1 executable-repertoire invariant (`rte/build_rte.py`)

Core: `gl_can_execute(pol)` = `0 <= pol < GL_NACT`, where `GL_NACT` is
the build's actual executable repertoire (each id names a procedure the
learner can execute). Parametric, not a whitelist — proven to
generalize beyond the attacked id (RT-E2, id 13). The rigid R1 id
whitelist `{0,1,2}` was killed on rigidity (withholds genuinely
executable policies). **Robust.**

### RT-F winner: F2 promotion escrow (`rtf/sources/f2_atk/`)

Core: escrow at E48, released after **8 consecutive clean** kind-3
verifies; any fire rejects the escrow (uninstall + commit survivor).
The "8" is a tunable policy parameter (how much clean history buys
release), not an episode whitelist or calendar position — it counts
events, so renumbering/reordering episodes cannot change its behavior.
**Robust; the constant is a parameter, not a defect.** Filed as a
parameter, not fixed.

### Own scale-model mechanisms (`tw.zag`)

- M-PROBE's probe schedule (20/25/30) is a fixed learner-side schedule —
  a documented parameter, not dumb-fragile: D3 (probe-identity
  reordering) showed invariance, and a hostile renumbering of the
  *world's* lie window is an attack redesign, not a paraphrase.
- M-COMBO's claim rejection looks up the exact cited step in the
  learner's own ledger; renumbering one side of the citation without
  the other is a different world, not a paraphrase. No defect.
- Matter-coupling of probes is asserted in comments/logging but not
  represented as data in the compact model — documented limitation
  (RESULTS scope note), not a mechanism defect.

## Summary

| Leg | Target | Result |
|-----|--------|--------|
| A1 | three-worlds scale model, D1/D2/D3 | PASS — 0 verdict flips, all perturbed cells match predicted tables |
| A2 | canonical gl_learner, ET_PN paraphrase | PASS — byte-identical stdout |
| A3 | RT-B/C/D/E/F winning mechanisms, static | no dumb-fragility defects found; 3 notes filed (RT-C new-policy predicate, RT-F "8" as parameter, probe-schedule as parameter) |

**No mechanism-level failures to fix. Nothing was fooled by dumb stuff.**
