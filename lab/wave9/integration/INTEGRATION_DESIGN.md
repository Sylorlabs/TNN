# Five-Organ Integration — Architecture Design

**Status:** DRAFT for Micah's approval. Not implemented, not run.
**Date:** 2026-09-20
**Scope:** integrate the five validated post-toy organs into ONE native developmental system.

## Table of contents

1. [The five organs and what each proved](#1-the-five-organs-and-what-each-proved)
2. [Composition principle](#2-composition-principle)
3. [Who owns which decision](#3-who-owns-which-decision)
4. [The developmental loop](#4-the-developmental-loop)
5. [Arbitration rules (seam contracts)](#5-arbitration-rules-seam-contracts)
6. [Ledger architecture](#6-ledger-architecture)
7. [Staged activation across the curriculum](#7-staged-activation-across-the-curriculum)
8. [What is deliberately excluded](#8-what-is-deliberately-excluded)
9. [Known integration risks](#9-known-integration-risks)

---

## 1. The five organs and what each proved

| # | Organ | Validated result | Latest implementation |
|---|-------|------------------|----------------------|
| 1 | Deliberate memory substrate | MA1 58/58 native; MA4 signed values 18/18; audit + replay exact; zero RNG in memory path | `wave7/felt-intensity/st_memory_core.zag` |
| 2 | Eliminative hypothesis logic | Wave-6 ablation: eliminative hypothesis-state verification + learner-initiated `SIGNAL_DISCONNECT` + deliberative standards are load-bearing for integrity; corroborated elimination 35/35 vs sustained spoofing | Minimal core derived from `wave3/hypothesis-driven-exploration/` + `wave6/attribution-ablation/VERDICT.md` |
| 3 | Deliberate consolidation/promotion | CONSOLIDATE/CONDEMN/PREEMPT/REVIVE over fast/slow tiers; beats automatic baseline on all curricula; 3,392-episode 4× leg | `wave3/r27-consolidation/impl/psm.zag` |
| 4 | Symbolic recall + trace composition | Boolean need-scan (P1∧P2∧P3∧P4), deliberate ABSTAIN, serving-trace pinning; composition-time verification (`comp_seq`/`comp_branch`/`comp_abstract`) | `wave3/deliberate-recall/`, `wave3/trace-composition/comp.zag` |
| 5 | Native structural revision | RC1 40/40: inspect/propose/commit/refuse/rollback over reasoning parameters; lying self-change caught by verification and rolled back; 100% of reasoning machinery governable, 0% of constitution | `wave7/reasoning-control/` |

**Honesty note on organ 2:** HDE v1 itself was trialed NEGATIVE (test-storms, partition pollution). What is validated — and what this design integrates — is the wave-6 ablation-derived minimal core: corroborated elimination, learner-initiated disconnect, deliberative standards. The fuller HDE machinery is NOT integrated.

**Prior art:** `wave5/integ-1/` already composed one learner (scaffold-release) with the IL checker and trap suites: 137/137, POSITIVE. Its lessons are designed in here: preregistered instrument disagreement, the sensor-hole finding, calibration load-bearing, and "integration defects live in the glue."

---

## 2. Composition principle

The organs compose through **one shared append-only audit ledger as the single system of record**, with strict decision ownership (section 3) and seam contracts (section 5). The rule:

> **Organs publish verdicts and requests; only organ 1 mutates state; only organ 5 mutates reasoning parameters; the constitution mutates nothing from inside.**

No organ reaches into another organ's internals. Every cross-organ effect is a named, ledgered call across a seam. This is what makes integration failures attributable instead of mush: a failure at a seam names the two organs and the contract violated.

---

## 3. Who owns which decision

| Decision | Owner | Executes via |
|----------|-------|--------------|
| All state mutation (add/kill/pin/promote/demote/strength writes) | **Organ 1** | Its own op API; enforces effort gates, pin/force-pin law, staged autonomy. Organ 1 never decides *policy* — it enforces it. |
| Belief verdicts (CONFIRM/REFUTE/ARCHIVED over claims) | **Organ 2** | Publishes verdicts with cited evidence. Does NOT kill memories or write strength — verdicts are *inputs* to organs 1 and 3. |
| Tier movement (CONSOLIDATE/CONDEMN/PREEMPT/REVIVE) | **Organ 3** | Executes through organ 1 ops only. Victim selection MUST be pin- and strength-aware (see risk 1). Triggered by organ 2 verdicts (corroborated confirmations feed CONSOLIDATE). |
| Read-time behavior (need formation, scan, composition, ABSTAIN) | **Organ 4** | Reads organ 1; pins serving traces via organ 1 pin. Composition preconditions verified at composition time; `comp_apply` executes blind by design. |
| Reasoning-parameter governance (verification bars, elimination strictness, disconnect criteria, calibration R, self-model cadence) | **Organ 5** | `REASON_INSPECT/PROPOSE/COMMIT/REFUSE/ROLLBACK`, gated by direction. Other organs may *request* parameter changes (ledgered); they cannot self-apply. |

Organ 5 governs parameters the other organs run on; it does not govern organ *policies*. Organ 2's verdicts never override organ 1's effort gates: a REFUTE cites evidence, but a kill still needs the graded effort `n(s)=⌈s/25⌉` distinct citations plus justification.

---

## 4. The developmental loop

Per episode, the organs compose as a loop (not a pipeline — organ 5 closes it):

1. **Perceive/need.** World presents observation or task. Organ 4 forms a declared need, recalls traces (Boolean scan), composes or deliberately ABSTAINS.
2. **Hypothesize/eliminate.** Surprises — negative outcomes on live claims, unsatisfied needs (organ 4 ABSTAIN is a surprise signal) — go to organ 2. Claims enter OPEN; corroborated elimination produces CONFIRM/REFUTE/ARCHIVED verdicts.
3. **Record.** Organ 2 verdicts become organ 1 evidence cites (`st_evidence`) and deliberate strength-affecting judgments. Corroborated confirmations trigger organ 3 CONSOLIDATE evaluation.
4. **Consolidate.** Organ 3 moves tiers through organ 1 ops: CONSOLIDATE (ver ≥ 6 across ≥ 2 distinct verified contexts), CONDEMN (tombstone), PREEMPT (pin/strength-aware victim), REVIVE.
5. **Govern.** Organ 5 inspects reasoning parameters with provenance, proposes changes with predicted effects (counterfactual self-simulation over its own ledger), gates decide, verification checks every prediction, rollback on mismatch.
6. **Curriculum advances.** Stage gates (DC-0 → DC-5) ratify organ activation and autonomy stages; the loop continues at the next stage.

The loop is where "not just coexist" is tested: organ 4's abstentions must actually drive organ 2's hypotheses; organ 2's verdicts must actually move organ 3's tiers; organ 5's parameter changes must actually alter organs 2–4's behavior measurably. The prereg's loop-closure checks (§4 of PREREG_INTEGRATION.md) assert each link independently — a loop that doesn't close is a composition failure, attributed to the broken link.

---

## 5. Arbitration rules (seam contracts)

1. **State-mutation seam (all → organ 1):** every state change goes through organ 1's op API. Direct writes are statically asserted illegal (the four legal strength-write paths). A cross-organ call that organ 1 refuses (pin conflict, effort unpaid, stage insufficient) returns a refusal code — the caller must handle it, never bypass it.
2. **Verdict seam (organ 2 → organs 1, 3):** verdicts carry cited evidence episodes. Organ 1 converts REFUTE verdicts into evidence cites, not kills. Organ 3 converts CONFIRM verdicts into CONSOLIDATE candidacy, not automatic promotion (the cross-context corroboration gate still applies).
3. **Tier seam (organ 3 → organ 1):** PREEMPT victim selection skips pinned/force-pinned slots and accounts for overwrite effort (Micah's law: overwriting a strong memory costs the full erase price). If no legal victim exists, PREEMPT refuses audibly — it never deadlocks silently (see risk 1).
4. **Read seam (organ 4 → organ 1):** recall never mutates except serving-trace pins. ABSTAIN is a first-class output, ledgered, and routed to organ 2 as a surprise.
5. **Parameter seam (all → organ 5):** parameter-change requests are ledgered proposals. Organ 5's gates classify by direction (constructive/neutral/destructive); destructive changes need stage FULL + ≥2 cited ledger entries + non-degrading integrity prediction.
6. **Constitution seam (none):** ledger append-only semantics, the `il_check` verdict function, the gate rules, the staging ladder, and external force authority are not addressable by any organ. Attempts are `REFUSED_CONSTITUTION` (204).

---

## 6. Ledger architecture

One shared append-only ledger, **organ-tagged entries**, with the integ-1 sealed-segment + digest-chain pattern from the start (not retrofitted):

- Every entry carries an organ tag (O1..O5) and a monotonic clock.
- Sealed segments (fixed episode count) with digest chains; replay must reproduce exact state (`st_replay_check` extended across all five organs' state).
- Audit caps sized **∝ episodes × organs** at design time; fail-close preserved. Per-organ trials never shared one ledger — the 10× horizon with five auditing organs is the first test of the budget math.
- Cross-organ calls are ledgered at both ends (request + verdict), so any seam dispute is replayable.

---

## 7. Staged activation across the curriculum

Organs activate progressively across the developmental curriculum (DC-0 → DC-5), matched to organ 1's staged autonomy ladder (NONE → ADD → MANAGE → KILL → FULL):

| Stage | Curriculum phase | Active organs | Autonomy |
|-------|-----------------|---------------|----------|
| DC-0 | Deliberate memory | O1 | NONE → ADD |
| DC-1 | Situated belief | O1, O2 | ADD → MANAGE |
| DC-2 | Trace composition | O1, O2, O4 | MANAGE |
| DC-3 | Structural revision | O1, O2, O4, O5 | MANAGE → KILL |
| DC-4 | Learner-driven inquiry | O1–O5 + O3 consolidation | KILL |
| DC-5 | Autonomy under withdrawal | All; teacher withdrawn | KILL → FULL (evidence-gated petition) |

Each stage has entry and exit gates (PREREG_INTEGRATION.md §3). A stage exit gate failure is attributed to the newly activated organ first (it is the only changed variable), then to seam contracts.

---

## 8. What is deliberately excluded

- **Felt intensity.** Its own trial is unresolved (rebuild-vs-retire-vs-reposition decision pending with Micah). It stays out of the integrated system until its verdict lands. The calibration knob R exists in organ 5's parameter space but stays fixed during integration.
- **Phase 4 differentiation** (per-user knowledge). CORE/USER separation is enforced by organ 1, but the integration trial is single-user.
- **Full HDE v1 machinery.** Only the wave-6-validated elimination core is integrated (see honesty note §1).
- **RL as training.** RL remains red-team only, per program law.
- **Strength arm:** organ 1 runs the **uniform arm B** (the S1 survivor), provisionally — pending the open audit on whether B must complete S10/S100 scale legs. The P2 drop-ceiling tripwire is armed in all stages: any freeze kills the arm, not the trial.

---

## 9. Known integration risks

1. **Emergent interference between validated organs.** Each organ passed in isolation; their combination is untested. Concrete interference points: organ 3 PREEMPT vs organ 1 pin/strength gates (victim deadlock); organ 5 parameter changes invalidating organ 2's elimination thresholds mid-run; organ 4's serving-trace pins vs organ 3's victim pool. **Precedent:** the wave-8 strength freeze — a protection mechanism with no cost, no expiry, and no audit trail produced a store freeze that no single-organ trial predicted. Emergent pathology is the base rate, not the exception.
2. **The sensor-hole transfers and amplifies.** Integ-1 arm C proved committed mechanisms trust the verification channel absolutely. In the integrated loop, poisoned pre-disconnect evidence flows organ 2 (committed hypothesis) → organ 1 (high-strength memory with audited justification) → organ 3 (consolidated to slow tier) → organ 4 (composed into traces) — a full pipeline for laundering poison into permanent structure. The defended-channel rule (corroborating evidence required before any re-COMMIT following an UNCOMMIT) must be designed into the prereg now.
3. **Ledger-budget multiplication.** Five auditing organs × 10× horizon × per-step ops (organ 3's CONSOLIDATE/CONDEMN/PREEMPT evaluations plus organ 1's evidence/justify/kill sequences) will blow any cap sized from single-organ experience. Sized at design time (§6) or it fail-closes mid-trial.
4. **Attribution mush.** Five organs, one curriculum, one ledger — a failure can be blamed on "the integration." The prereg pre-commits per-control kill criteria naming which organ's claim dies on which failure, plus integration-glue defects (deadlock, ledger overflow, cross-organ livelock) as their own kill category with redesign outcomes.

---

## Open questions for Micah (see PREREG_INTEGRATION.md §7)

1. Scale definition and whether S100 is preregistered now or gated on S10.
2. Strength regime for the integrated substrate (B provisional, pending audit).
3. Defended-channel rule: build into this prereg or run separately first?
4. Whether the reposition-track felt experiment runs in parallel.
