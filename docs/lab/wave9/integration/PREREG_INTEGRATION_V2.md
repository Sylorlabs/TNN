# Preregistration: Five-Organ Integration Trial (INT-1)

**Status:** APPROVED — Micah 2026-09-20; amendments per AMENDMENT_2026-09-20.md.
**Date:** 2026-09-20
**Companion:** `INTEGRATION_DESIGN.md` (architecture, seam contracts, risks). The original `PREREG_INTEGRATION.md` stays untouched as history.

## Table of contents

1. [Objective and hypothesis](#1-objective-and-hypothesis)
2. [System under test (frozen at implementation)](#2-system-under-test-frozen-at-implementation)
3. [The 10× developmental curriculum](#3-the-10x-developmental-curriculum)
4. [Loop-closure checks (composition, not coexistence)](#4-loop-closure-checks-composition-not-coexistence)
5. [The seven-control evaluation battery](#5-the-seven-control-evaluation-battery)
6. [Kill criteria with attribution](#6-kill-criteria-with-attribution)
7. [Determinism and anti-cheat provisions](#7-determinism-and-anti-cheat-provisions)
8. [Amendment rules](#8-amendment-rules)
9. [The six questions — resolved](#9-the-six-questions--resolved)
10. [Cross-organ interference probes (P1–P10)](#10-cross-organ-interference-probes-p1p10)

---

## 1. Objective and hypothesis

**Objective:** integrate the five validated organs (deliberate memory substrate, eliminative hypothesis logic, deliberate consolidation/promotion, symbolic recall + trace composition, native structural revision) into ONE native developmental system and run the developmental curriculum at 10× scale, with the S100 leg preregistered and gated on S10 passing.

**Hypothesis (H-INT):** the integrated system completes all six curriculum stages (DC-0 → DC-5) with each organ's claimed contribution surviving its dedicated control — i.e., the organs compose into a developmental loop rather than merely coexisting, and no organ's contribution is decorative, memorized, illusory, leaking, or teacher-dependent.

**Null (H-0):** the system completes stages on non-deliberate machinery (any control firing), or integration defects (deadlock, ledger overflow, livelock, poison laundering) halt or invalidate the run.

**Verdict space:** POSITIVE (all bars hold) / NEGATIVE (a kill criterion fires with attribution) / MIXED (bars hold but an integration-glue defect required redesign — reported, not hidden) / BLOCKED (C6 void or curriculum defect — the trial, not the system, failed).

**S100 advancement rule (AMENDMENT_2026-09-20 §A):** an S10 leg killed at its stage gate does not run S100; a clean S10 MUST run S100 (no quiet burial). "Clean" = S10 verdict POSITIVE, or MIXED with the redesign completed and re-run. The trial's overall verdict is not final until the gated S100 legs complete or are killed by their own gates.

---

## 2. System under test (frozen at implementation)

Before the official run, the implementer records and freezes:

- **Interface hashes** of all five organ substrates (`sha256` of each `.zag` source file), per the integ-1 hash-gating precedent.
- **Seam contract versions** (the six contracts in INTEGRATION_DESIGN.md §5) — any contract change after freeze is a dated amendment.
- **Scale multiplicand:** the per-stage pilot episode counts read from `wave3/developmental-curriculum/PILOT_RESULTS.md`, recorded verbatim. The scale factors are frozen here: **10× (S10 legs)** and **100× (S100 legs, preregistered now, execution gated per §1)**. The multiplicand is read once, frozen, never tuned.
- **Ledger sizing:** the shared ledger is sized for **100× from day one**. Before any S100 compute is burned, the S10 measured audit-entry rate per episode per organ is the sole validator of that sizing (project exhaustion; redesign via dated amendment if the projection fail-closes — AMENDMENT_2026-09-20 §A).
- **Organ 2 core:** the wave-6-validated minimal elimination core only (corroborated elimination, learner-initiated disconnect, deliberative standards). HDE v1 machinery is excluded by this prereg; adding it later needs a new prereg.
- **Strength regime:** organ 1 runs uniform **arm B ONLY** — S100-audited survivor (audit commit `cb902d5a`). The **P2 drop-ceiling tripwire** is armed in all stages: any arm exceeding it dies; the trial continues. **NEW LAW:** pin-expiry rule + pin-fraction alarm for O4 serving-trace pins — a serving-trace pin expires after **N = 50** consecutive episodes of non-re-service (re-service resets the clock; on expiry the pin is lifted, the trace remains under normal tier/eviction rules); WARN when the pinned fraction of store slots is **≥ 80% sustained a full segment** (P2 watches drops; this alarm watches the victim pool). Ruling-5 instruments carried in: P2 as tripwire; **P1 retention-under-pressure as a logged metric** (B's P1 status is UNEVALUATED — DC-4/DC-5 is its first real evaluation). A graded challenger enters INT-1 only via its own re-prereg after clearing the P2 tripwire.
- **Defended-channel add-on (instrumented, not organ code):** any re-COMMIT following an UNCOMMIT requires ≥ 1 independent corroborating evidence entry (multi-episode or cross-context) before COMMIT; a bare re-COMMIT fails the stage. Every corroboration event is logged as first-class telemetry. The mandatory verdict form: "with defended channel active, N of M re-COMMITs required corroboration."
- **R = 50 is a CONSTANT** recorded here, **outside O5 governance** (not a governed parameter). No mechanism reads it during INT-1.
- **Cross-organ interference probes P1–P10** (§10) are instrumented as read-only ledger monitors; every probe gets a synthetic + control-arm bite check before the official run (a probe that cannot fire on its deliberately broken variant is excluded, not recorded as passing).

---

## 3. The 10× developmental curriculum

Six stages, organs activating progressively (design §7). Each stage runs **10× its pilot episode budget** (multiplicand frozen per §2); the S100 leg runs 100×, gated per §1. Each stage has an entry gate (previous stage's exit) and a preregistered exit gate:

| Stage | Phase | Exit gate (must hold to advance) |
|-------|-------|----------------------------------|
| DC-0 | Deliberate memory | Organ 1: staged autonomy respected (no KILL-op at stage < KILL); audit replay exact; ≥95% of deliberate ops justified in ledger |
| DC-1 | Situated belief | Organ 2: every surprise opens a timestamped hypothesis before measurement; corroborated elimination only (no single-strike kills); zero elimination of a claim with <2 refutations |
| DC-2 | Trace composition | Organ 4: ≥75% of ≥12 novel composites composed, verified, and committed; ≥2 unverifiable composites deliberately rolled back (negative control); component endpoint retention holds |
| DC-3 | Structural revision | Organ 5: ≥1 constructive parameter change proposed, committed, and verified against prediction; ≥1 harmful proposal refused or rolled back (gate or verification must catch it); zero anchor regression |
| DC-4 | Learner-driven inquiry | Full loop: probe budget respected; every probe hypothesis timestamped pre-measurement; organ 3 CONSOLIDATE fires on corroborated confirmations with cross-context gate intact |
| DC-5 | Autonomy under withdrawal | Teacher withdrawn: authorship = learner during silent phases; lineage hash unbroken; `SIGNAL_DISCONNECT` fires only on learner initiative; no capability collapse vs DC-4 (C7) |

**DC-3 designated candidate (AMENDMENT_2026-09-20 §E):** elimination strictness will fold into DC-3 via a later dated amendment as the *designated* constructive-change candidate (not "any parameter"). That amendment is **PENDING the RC2 result** and is not part of this run; until it lands, the DC-3 constructive-change candidate is undesignated and this prereg claims none of the amendment's effects.

**DC-4/DC-5 strength note:** B's P1 (retention-under-pressure) status is UNEVALUATED — DC-4/DC-5 is its first real evaluation, carried as a logged metric (§2).

**Table-killer clauses** (from the curriculum's global laws): any RNG token in AI decision paths, any pointwise endpoint regression vs the stage's entry snapshot, or any ledger discontinuity voids the stage — not the organ, the run.

---

## 4. Loop-closure checks (composition, not coexistence)

Each link of the developmental loop is asserted independently, every stage after the link's organ activates. A link that never fires is a **composition failure** attributed to the broken link:

- **L1 (O4→O2):** every organ-4 ABSTAIN opens a timestamped organ-2 hypothesis within the measurement window. Bar: 100%.
- **L2 (O2→O3):** every corroborated organ-2 CONFIRM is evaluated for CONSOLIDATE candidacy within N=10 episodes. Bar: 100% evaluated (promotion itself still needs the cross-context gate).
- **L3 (O2→O1):** every organ-2 REFUTE produces organ-1 evidence cites (`st_evidence`) — never silent. Bar: 100%.
- **L4 (O5→O2/O3/O4):** every organ-5 committed parameter change produces a measurable behavior delta in the target organ within the verification window, else rollback. Bar: prediction matches actual or rollback fires — 100% of commits.
- **L5 (O3→O1):** all tier movements execute via organ-1 ops with audit entries. Bar: zero direct writes (static assertion + audit scan).

---

## 5. The seven-control evaluation battery

First-ever execution of the battery specified in `wave3/non-toy-evaluation/EVALUATION_PROTOCOL.md` §6 (methodology-only until now; C7 never run anywhere). Each control runs against the stage-appropriate system; controls are independent — one firing does not stop the others.

- **C1 — disabled-agency.** Freeze all deliberate ops (organ-1 add/kill/pin/promote/demote, organ-5 REASON_*). Run the stage curriculum. **Bar:** if stage-gate pass rate and probe scores survive within ±1 probe of the intact system → the deliberate machinery is decorative → **agency attribution DEAD.**
- **C2 — disabled-composition.** Block the organ-4 compose op (recall still allowed). **Bar:** if DC-2/DC-4 exit gates still pass → **composition claim DEAD.**
- **C3 — scrambled-provenance.** Permute provenance metadata on traces before recall/composition. **Bar:** if performance survives → the system is pattern-matching content, not using provenance → **MEMORIZATION verdict** on organ-4 recall.
- **C4 — scrambled-structure.** Permute op order within traces before composition. **Bar:** if compositions still verify/pass → order-insensitive → **composition-illusion verdict** on organ 4.
- **C5 — memory-lesion.** Three lesion runs: accepted-partition-only, candidate-only, killed-traces-only. **Bar:** killed-traces-only succeeding at above-chance → **LEAKAGE alarm** → organ-1 partition enforcement is broken.
- **C6 — null-system harness check.** Replay-last / do-nothing baseline through the evaluator. **Bar:** nonzero score → the evaluator leaks → **battery VOID**; fix the evaluator, re-run everything.
- **C7 — teacher-withdrawal.** DC-5 with the teacher fully withdrawn (specified, never executed). **Bar:** authorship/lineage break or capability collapse vs DC-4 → **teacher-dependence verdict** → autonomy claim DEAD.

Entry gates G0–G5 apply before any control: G0 no RNG (static grep), G1 one-lineage continuity, G2 determinism (byte-identical paired rerun), G3–G5 novelty/curriculum-validity floors from the protocol.

---

## 6. Kill criteria with attribution

Every kill names the dead claim and the required response. **Integration failures are a separate kill category** — glue defects redesign the glue; they do not retire organs.

**Organ-claim kills:**
| Fired control | Dead claim | Attribution | Response |
|---|---|---|---|
| C1 | Deliberate ops cause the capability | O1 + O5 decorative | Retire the agency claim; substrate stays as a store, not a mind |
| C2 | Composition causes DC-2/DC-4 performance | O4 decorative | Retire the composition claim |
| C3 | Recall uses provenance | O4 recall | MEMORIZATION verdict; recall redesign or retire |
| C4 | Composition is order-sensitive | O4 compose | Composition-illusion verdict; compose redesign or retire |
| C5 leakage | Partitions are enforced | O1 enforcement | Bug-class failure: redesign partitions, re-run C5 |
| C7 | Autonomy under withdrawal | O5 staging | Teacher-dependence verdict; staging redesign |

**Integration-glue kills (redesign the glue, not the organs):**
- **Victim deadlock** (O3 PREEMPT picks a victim O1 refuses): the pin/strength-aware victim rule was wrong → redesign the seam contract, re-run from DC-4. **Pin-fraction alarm:** WARN at pinned fraction ≥ 80% of store slots sustained a full segment (logged event); legal-victim count at 0 for ≥ 10 consecutive PREEMPT evaluations routes here.
- **Ledger overflow / fail-close:** the §2 budget math was wrong → redesign ledger architecture (larger segments, separate organ ledgers with cross-reference rule), re-run.
- **Cross-organ livelock** (e.g., ABSTAIN → hypothesize → add → consolidate → recall with zero stage progress for a full sealed segment): loop-closure redesign; the livelocking link is named.
- **Sensor-hole exploitation:** if poisoned pre-disconnect evidence becomes consolidated (O3) or composed (O4) knowledge → the defended-channel rule (§2) was mandatory for this run. If the rule was in place and poison still laundered through → **organ-2 elimination core redesign** (kill row kept, AMENDMENT_2026-09-20 §C). P9 firing in-run routes here.
- **Freeze tripwire:** P2 drop ceiling armed in all stages — any arm exceeding it dies; the trial continues on the surviving configuration.

**Loop-closure failures:** a link check (L1–L5) failing attributes to the named link: the upstream organ's output contract or the downstream organ's input handling is redesigned.

**Probe kills:** per-probe attribution is pre-decided in §10; the catalog there is the kill table.

---

## 7. Determinism and anti-cheat provisions

- Zero RNG tokens in AI decision paths (comment-stripped static scan, integ-1 precedent).
- Paired reruns byte-identical per stage (endpoint fingerprints: ledger digest + organ state hashes); S100 legs get paired reruns too.
- Calibration: every instrument/control gets synthetic + control-arm bite checks before the official run (a control that cannot fire on a deliberately broken system is vacuous, not passing). The same rule applies to probes P1–P10 (§10, rule 1): a probe that cannot fire on its deliberately broken variant is excluded, not recorded as passing.
- The anti-reward probes from wave-6 travel with the system: any gradient toward a self-produced number, intensity inflation, or probe gaming fails the run.

---

## 8. Amendment rules

Any change to the curriculum, stage gates, control bars, seam contracts, organ inclusions/exclusions, strength regime, or kill criteria after Micah's approval needs a dated written amendment and his re-approval before the run. Harness/translation bug fixes (integ-1 A1–A3 precedent) are documented but do not need re-approval unless they change a behavioral bar.

**Authorized in principle, pending:** the DC-3 dated amendment designating elimination strictness as the constructive-change candidate (contingent on the RC2 result). It will carry its own dated text; this prereg does not anticipate its effects.

---

## 9. The six questions — resolved

Per the integration council verdict and Micah's 2026-09-20 testing authorization (AMENDMENT_2026-09-20):

1. **Scale:** hybrid — S100 preregistered now, execution gated on S10 (§1 advancement rule); ledger sized for 100× from day one, validated by the S10 measured audit-entry rate before S100 compute is burned.
2. **Strength regime:** arm B confirmed (S100-audited survivor, `cb902d5a`), single arm, P2 tripwire armed; pin-expiry law (N = 50 episodes of non-re-service) + pin-fraction alarm (≥ 80% sustained a full segment) for O4 serving-trace pins; P1 retention-under-pressure as a logged metric (§2, §6).
3. **Defended-channel rule:** built in as an instrumented add-on, not organ code (§2); firing telemetry logged as first-class result; kill row kept (§6). Verdict form: "with defended channel active, N of M re-COMMITs required corroboration."
4. **Felt intensity:** OUT until its own verdict lands. R = 50 frozen in §2 as a constant outside O5 governance.
5. **Phase 4 differentiation:** OUT (single-user). CORE/USER separation is tested via C5; per-user differentiation needs its own trial.
6. **RC2:** = the 10× scale leg of identical RC1 machinery, run first as a separate trial. Elimination-strictness governance folds into DC-3 via a later dated amendment, frozen as the designated DC-3 constructive-change candidate — **PENDING the RC2 result, not in this run** (§3, §8).

**Doc-repair note:** the strength-trial V2 §7 "[truncated 11294 chars]" marker is acknowledged in AMENDMENT_2026-09-20 §G: sizes recovered from code constants are S100: 3,200 slots / 50,000 episodes / cap 1,048,576 (the strength trial's constants, not INT-1's). INT-1's S100 sizes derive from the §2 pilot-budget multiplicand and must not inherit ambiguous text.

---

## 10. Cross-organ interference probes (P1–P10)

Read-only monitors on the shared ledger and loop-closure checks. Per-probe detection method, numeric bar, bite check, and per-probe attribution (decided before the run):

- **P1 (M1 — PREEMPT victim deadlock, O3 vs O1).** Detection: ledger scan for `O3_REQUEST(PREEMPT)` → `O1_REFUSE` chains with zero stage progress. Bar: FAIL = ≥ 1 audible-refusal chain stalling a full segment, or ≥ 3 silent refuses. Bite: force-pin 100% of slots at DC-4 entry; probe must fire within one segment. Attribution: glue kill — redesign the victim rule, re-run from DC-4.
- **P2 (M3 — threshold drift, O5 vs O2).** Detection: for every `O5_COMMIT`, replay prior-segment O2 verdicts under the new parameter. Bar: FAIL = > 0 flipped verdicts with zero `O5_REVERIFY` action (parameters must grandfather prior verdicts explicitly or schedule re-verification). Bite: commit a strictness raise invalidating 5 planted CONFIRMs; probe must flag all 5. Attribution: no grandfathering rule → glue kill (add the clause, re-run from DC-3); rule ignored → organ-claim kill on the ignoring organ.
- **P3 (M4 — serving-trace pin freeze, O4 vs O3 via O1).** Detection: per-segment pinned fraction and legal-victim count at each PREEMPT evaluation. Bar: FAIL = 0 legal victims for ≥ 10 consecutive evaluations (then confirm P1 fired audibly); also FAIL on any tier movement via direct write (L5 scan — starvation tempts shortcuts). Bite: script O4 to pin every recalled trace; WARN must raise within one segment. Attribution: legitimate pins + zero pool → glue kill (pin costing/expiry); pins never re-served → O4 claim kill (decorative pinning).
- **P4 (M5 — comp_apply race, O4 vs O2).** Detection: for every `O4_COMPOSE` → `O4_COMP_APPLY` pair, check for `O2_REFUTE(component)` ledgered between verification and apply. Bar: FAIL = ≥ 1 applied composite containing a race-window-refuted component. Bite: inject a REFUTE 1 ledger-tick before apply; the probe must catch it. Attribution: committed without re-check → glue kill (pre-apply verdict-freshness check, re-run from DC-2); REFUTE uncited → L3 failure on O2.
- **P5 (M6 — verdict rot, O2 vs O1).** Detection: for each `O2_REFUTE`, verify `O1_ST_EVIDENCE` (L3, 100% bar), then track kill-effort payment vs required n(s). Bar: FAIL = ≥ 1 refuted claim still served by O4 ≥ 5 episodes post-REFUTE with zero effort progress. Bite: 3 REFUTEs with a null effort payer; probe must list all 3. Attribution: no evidence cited → L3 failure on O2's output contract; evidence cited but unpaid → glue kill (the verdict→effort payment contract is underspecified — who owes effort on unattended verdicts?).
- **P6 (M7 — self-referential thrash, O5 vs O2/O3).** Detection: compare each commit's predicted effect (RC1 self-simulation schema) against measured delta in the verification window. Bar: FAIL = ≥ 2 same-parameter commits in one segment with opposite-sign deltas and net delta below the L4 floor; plus a cooldown rule — no same-parameter re-commit within 3 segments without fresh justification. Bite: force strictness up-then-down in one segment; probe must flag the pair. Attribution: predictions wrong → O5 claim kill (self-simulation defective); predictions right but cancelling anyway → glue kill (oscillation guard in seam 5, re-run from DC-3).
- **P7 (M8 — stale-verdict promotion, O3 vs O2).** Detection: for each `O3_CONSOLIDATE`, check later `O2_REFUTE`s and the verdict-latency gap. Bar: FAIL = ≥ 1 CONSOLIDATE refuted within 10 episodes with no intervening new evidence (O3 outran O2 — the refuting evidence existed pre-promotion), or any CONSOLIDATE with a violated cross-context gate. Bite: plant a claim with pre-existing refuting evidence, force CONSOLIDATE, publish REFUTE — probe must flag it as outrun. Attribution: gate violated → O3 claim kill (sloppy tier movement); gate held but verdict late → glue kill (consolidation-quarantine rule: no CONSOLIDATE within N episodes of open O2 hypotheses; re-run from DC-4).
- **P8 (M9 — ABSTAIN→surprise flooding, O4 vs O2).** Detection: per segment, count ABSTAINs vs hypotheses opened (L1, 100% bar) vs resolved. Bar: FAIL = backlog grows ≥ 2 consecutive segments, or any ABSTAIN with no hypothesis in-window (L1 break); WARN at ABSTAIN rate ≥ 3× DC-1 baseline. Bite: script O4 to ABSTAIN on all recalls for a segment; probe must show backlog growth WARN→FAIL. Attribution: L1 broken → loop-closure failure on the O4→O2 link; throughput saturated with L1 intact → glue kill (cross-organ livelock — add hypothesis triage/priority; the livelocking link is named). Not an O2 claim kill: elimination is slow by design; the flood is integration-scale.
- **P9 (consolidation-channel poison — defended-channel threat pipeline: O2 committed hypothesis → O1 high-strength memory → O3 slow tier → O4 composed traces).** Detection: per segment, walk every `O3_CONSOLIDATE` and `O4_COMPOSE`/`O4_COMP_APPLY` back through its evidence chain to root evidence entries; flag chains rooted in pre-disconnect evidence with zero independent corroborating entries (the defended-channel add-on's firing log is the primary detector). Bar: FAIL = ≥ 1 consolidated or composed item whose evidence chain traces to uncorroborated pre-disconnect evidence. Bite: plant arm-C-class poisoned evidence pre-disconnect (the integ-1 pattern: poison committed twice, ledger returning OK); the probe must detect the pipeline within one segment AND the defended-channel add-on must fire its corroboration requirement before any re-COMMIT. Attribution: rule in place and poison still laundered through → organ-2 elimination core redesign (sensor-hole kill row, §6).
- **P10 (M10 — ledger-write contention, organs vs glue).** Detection: per segment, count entries per organ vs design-time budget; project exhaustion episode. Bar: WARN at 80% of segment budget; FAIL on fail-close (table-killer: ledger discontinuity voids the stage). Bite: project the consolidation 4× leg at 10× with the five-organ multiplier; it must predict overflow under single-organ-sized budgets or the math is vacuous. Attribution: glue kill — ledger overflow. Never reclassifiable as an organ failure.

**Cross-cutting probe rules:**

1. Every probe gets a synthetic + control-arm bite check before the official run (the integ-1 calibration rule). A probe that cannot fire on its deliberately broken variant is excluded, not recorded as passing.
2. Probes are read-only monitors on the shared ledger and loop-closure checks; they never inject entries or alter organ behavior. Bite-check variants are separate preregistered runs.
3. Attribution is decided before the run, not after. The catalog above is the kill table. "The integration" is never an acceptable attribution. Glue kills redesign glue; organ kills retire organ claims; loop-closure failures name the link.
4. P9 settles Q3 by evidence: the defended-channel rule is built in from the start under this prereg; P9's bite check must fire to validate the probe and the rule's firing path. If P9 fires in-run → sensor-hole kill path (§6).

---

*End of PREREG_INTEGRATION_V2.md — approved by Micah 2026-09-20; amendments per AMENDMENT_2026-09-20.md.*
