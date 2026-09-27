# Experiment 1b — Follow-up Verdict (VERDICT2)

**Date:** 2026-09-27 | **Phase-2 commit:** `9c79065d02` | **Prereg:** `docs/lab/invention/survival/PREREG2.md` (commit `20c5302e2`, frozen)

Three independent workers completed: (1) trace+hardcode auditor, (2) six-family red
team, (3) generalization worker. This verdict synthesizes all three. Frozen bars are
unchanged — qualifications are documented, not silently amended.

## The three questions

### 1. Does recall harm TNN broadly?

**YES — the evidence is now stronger than the committed result.**

| Domain | Harm evidence |
|---|---|
| D2 SHIFT | R_home=-1500 vs R_true=4500 (below chance) — severe |
| D3 TOOL | R_home=45084 vs R_true=52000 — moderate |
| D1 new shifts (4) | R=10–70 ticks vs R_true=600 — severe, 4/4 |
| D4 RELAY (new domain) | Strict harm 2/6 shifted; milder degradation 6/6 |

The R_true probe is optimal everywhere (600/600 D1, =P on D4): with correct content,
reflexive application is fine. The D_wrongKB probe (actively false KB on D4) shows the
module recovers to 81% closure. The failure is **stale/false content applied
reflexively** — replicated across four domains and nine harming shifts.

Correction to the committed record: the original D1 legs were void or mismeasured —
storm-invert *did* harm R in energy terms (the 600-tick metric hid it), and move-rot was
non-informative by construction (R's policy contains zero moves). The four new D1
shifts are the first D1 shifts that actually bite.

### 2. Does the candidate-not-reflex repair generalize?

**As a mechanism: YES. As committed deployment: PARTIAL — D1 bar-equivalent KILLED.**

| Domain | Gap closure (D_home) | Module |
|---|---:|---|
| D2 | 90.0% | shared, unmodified |
| D3 | 80.7% | shared, unmodified |
| D4 RELAY (unseen) | 87–93% on 6/6 shifted | shared, unmodified |
| D_wrongKB (false content) | 81% | shared, unmodified |
| D1 new shifts, committed agent | **0%** (D≈R or worse) | **module never wired in** |
| D1 combine-tax, exploratory wiring | full (600 ticks) | shared, unmodified |

Home-regime parity holds everywhere (D/R = 1.000, no >10% regression).

**The kill:** `agent_d_d1.zag` never imports `recall_delib.zag` — D1 shipped without the
repair (a second copy of R's policy with extra logging, not deliberation). The committed
"one shared module for all domains" claim is factually false for D1, and the committed
"ALL BARS PASS" verdict is untenable as stated. Frozen §3 ("ALL THREE domain agents
import it") is violated by the committed artifact.

**Open failure modes of the current gate (no bar fire, documented for follow-up):**
- **Speed limit:** the 10-sample distrust threshold cannot save agents killed in fewer
  exposures (D1 storm-trap; exploratory wiring confirms).
- **Mediocre trap:** a plausible heuristic with an untaught better alternative is applied
  uncritically forever — 0% closure, D≡R all 600 turns.
- **Late-onset shift:** lifetime-mean gate never fires while the tool dies for 200 ticks —
  0% closure. Fix efficacy depends on the shift arriving early.
- **Distrust cliff:** a 1-point world change at the boundary flips 0% → 82% closure
  (590-point score discontinuity).

### 3. Is the consciousness trace causal?

**QUALIFIED: the gate is causal; the three-check story is not.**

- Binding: the unmodified phase-2 agents rebuild byte-identically (40/40 RESULT lines,
  24,000/24,000 per-tick decisions); all 24,000 decisions replay from traces with
  **0 mismatches**; the shared module has no scenario/branch hardcodes.
- Qualification: the implemented evaluator is **one check** (effect-expectation
  distrust), not the preregistered three. The precondition EVAL is stored but never
  read; the conflict EVAL is vacuous by construction. The TSV precondition/conflict
  lines are emitter-computed from `trace_emit.zag`, which was never committed — they
  are non-causal lines presented as deliberation.
- Bottom line: the trace genuinely determines the action through the implemented
  gate (the audit trail is real), but PREREG2 §2's evaluator description was silently
  narrowed. "Conscious every step" currently rests on one causal check.

## Kill-bar verdicts

| Bar | As written | Qualification |
|---|---|---|
| K1 harm <2/3 domains | PASS | Evidence stronger than claimed (new D1 4/4, D4); original D1 legs void/mismeasured |
| K2 closure <50% | PASS (90.0%, 80.7%; D4 87–93%) | T2/T3 0%-closure modes bound the "broad" claim |
| K3 decorative consciousness | PASS (0/24,000 mismatches) | Evaluator narrowed 3→1 checks; non-causal trace lines from uncommitted emitter |
| K4 hardcodes / held-out | PASS (module clean) | **Closest to a fire:** §3 violated by D1 agent (outside module audit scope); held-out "family" = 1 unique world per domain |
| K5 home regression | PASS (1.000 everywhere) | — |
| K6 content vs application | PASS | Strengthened by R_true + D_wrongKB probes |

**No frozen bar fires.** The honest kills are: (a) the committed D1 repair claim —
KILLED, 0% closure, module never deployed; (b) the "all bars pass" verdict as stated —
untenable; (c) the variant-count framing — restated as unique worlds (D2: 2 in-sample +
1 held-out; D3: 2 + 1).

## Repairs made in this commit

- `traces/README.md`: amended to record that `trace_emit.zag` was never committed —
  the TSVs are audit-grade and bound to the scores (0/24,000 mismatches, 40/40
  byte-identical rebuilds) but the documented reproduction path is not executable as
  written; precondition/conflict lines are emitter-computed, not decision-causal.
- Evidence committed: `followup/audit/TRACE_AUDIT2.md`,
  `followup/redteam/REDTEAM2.md`, `followup/generalization/GENERALIZATION2.md` plus
  the generalization run evidence (sources, worlds, KBs, result+SHA logs).

## Recommended follow-ups (not executed)

1. **Rebuild the D1 agent** on the shared module (unmodified), re-run D1 home + the 4
   new shifts, commit as new evidence. The committed D1 kill stands until this lands.
2. **Re-derive and commit `trace_emit.zag`**, or regenerate audit-grade traces with a
   committed emitter whose precondition/conflict lines are decision-causal or labeled.
3. **Gate hardening** against the T2/T3/T4a failure modes (mediocre-trap scrutiny,
   recency-weighted distrust, boundary smoothing) — new prereg, new bars.
4. A second-opinion question on the K1 denominator legitimacy was filed to the z.ai
   relay (`recall-harm-q1`); the answer will be amended into this verdict if it changes
   anything. The new D1/D4 evidence largely answers it already.
