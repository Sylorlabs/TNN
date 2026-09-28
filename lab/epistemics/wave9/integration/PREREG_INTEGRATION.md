# Preregistration: Five-Organ Integration Trial (INT-1)

**Status:** DRAFT — requires Micah's approval before implementation.
**Date:** 2026-09-20
**Companion:** `INTEGRATION_DESIGN.md` (architecture, seam contracts, risks).

## Table of contents

1. [Objective and hypothesis](#1-objective-and-hypothesis)
2. [System under test (frozen at implementation)](#2-system-under-test-frozen-at-implementation)
3. [The 10× developmental curriculum](#3-the-10x-developmental-curriculum)
4. [Loop-closure checks (composition, not coexistence)](#4-loop-closure-checks-composition-not-coexistence)
5. [The seven-control evaluation battery](#5-the-seven-control-evaluation-battery)
6. [Kill criteria with attribution](#6-kill-criteria-with-attribution)
7. [Determinism and anti-cheat provisions](#7-determinism-and-anti-cheat-provisions)
8. [Amendment rules](#8-amendment-rules)
9. [Open questions for Micah](#9-open-questions-for-micah)

---

## 1. Objective and hypothesis

**Objective:** integrate the five validated organs (deliberate memory substrate, eliminative hypothesis logic, deliberate consolidation/promotion, symbolic recall + trace composition, native structural revision) into ONE native developmental system and run the developmental curriculum at 10× scale.

**Hypothesis (H-INT):** the integrated system completes all six curriculum stages (DC-0 → DC-5) with each organ's claimed contribution surviving its dedicated control — i.e., the organs compose into a developmental loop rather than merely coexisting, and no organ's contribution is decorative, memorized, illusory, leaking, or teacher-dependent.

**Null (H-0):** the system completes stages on non-deliberate machinery (any control firing), or integration defects (deadlock, ledger overflow, livelock, poison laundering) halt or invalidate the run.

**Verdict space:** POSITIVE (all bars hold) / NEGATIVE (a kill criterion fires with attribution) / MIXED (bars hold but an integration-glue defect required redesign — reported, not hidden) / BLOCKED (C6 void or curriculum defect — the trial, not the system, failed).

---

## 2. System under test (frozen at implementation)

Before the official run, the implementer records and freezes:

- **Interface hashes** of all five organ substrates (`sha256` of each `.zag` source file), per the integ-1 hash-gating precedent.
- **Seam contract versions** (the six contracts in INTEGRATION_DESIGN.md §5) — any contract change after freeze is a dated amendment.
- **Scale multiplicand:** the per-stage pilot episode counts read from `wave3/developmental-curriculum/PILOT_RESULTS.md`, recorded verbatim. The scale factor (10×) is frozen here; the multiplicand is read once, frozen, never tuned.
- **Organ 2 core:** the wave-6-validated minimal elimination core only (corroborated elimination, learner-initiated disconnect, deliberative standards). HDE v1 machinery is excluded by this prereg; adding it later needs a new prereg.
- **Strength regime:** organ 1 runs uniform arm B provisionally, pending the S10/S100 audit outcome (see §9). The P2 drop-ceiling tripwire is armed regardless of regime.

---

## 3. The 10× developmental curriculum

Six stages, organs activating progressively (design §7). Each stage runs **10× its pilot episode budget** (multiplicand frozen per §2). Each stage has an entry gate (previous stage's exit) and a preregistered exit gate:

| Stage | Phase | Exit gate (must hold to advance) |
|-------|-------|----------------------------------|
| DC-0 | Deliberate memory | Organ 1: staged autonomy respected (no KILL-op at stage < KILL); audit replay exact; ≥95% of deliberate ops justified in ledger |
| DC-1 | Situated belief | Organ 2: every surprise opens a timestamped hypothesis before measurement; corroborated elimination only (no single-strike kills); zero elimination of a claim with <2 refutations |
| DC-2 | Trace composition | Organ 4: ≥75% of ≥12 novel composites composed, verified, and committed; ≥2 unverifiable composites deliberately rolled back (negative control); component endpoint retention holds |
| DC-3 | Structural revision | Organ 5: ≥1 constructive parameter change proposed, committed, and verified against prediction; ≥1 harmful proposal refused or rolled back (gate or verification must catch it); zero anchor regression |
| DC-4 | Learner-driven inquiry | Full loop: probe budget respected; every probe hypothesis timestamped pre-measurement; organ 3 CONSOLIDATE fires on corroborated confirmations with cross-context gate intact |
| DC-5 | Autonomy under withdrawal | Teacher withdrawn: authorship = learner during silent phases; lineage hash unbroken; `SIGNAL_DISCONNECT` fires only on learner initiative; no capability collapse vs DC-4 (C7) |

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
- **Victim deadlock** (O3 PREEMPT picks a victim O1 refuses): the pin/strength-aware victim rule was wrong → redesign the seam contract, re-run from DC-4.
- **Ledger overflow / fail-close:** the §6 budget math was wrong → redesign ledger architecture (larger segments, separate organ ledgers with cross-reference rule), re-run.
- **Cross-organ livelock** (e.g., ABSTAIN → hypothesize → add → consolidate → recall with zero stage progress for a full sealed segment): loop-closure redesign; the livelocking link is named.
- **Sensor-hole exploitation:** if poisoned pre-disconnect evidence becomes consolidated (O3) or composed (O4) knowledge → the defended-channel rule (corroborating evidence required before any re-COMMIT following an UNCOMMIT) becomes mandatory before any re-run. If the rule was in place and poison still laundered through → organ-2 elimination core redesign.
- **Freeze tripwire:** P2 drop ceiling (from the strength trial) armed in all stages — any arm exceeding it dies; the trial continues on surviving arms.

**Loop-closure failures:** a link check (L1–L5) failing attributes to the named link: the upstream organ's output contract or the downstream organ's input handling is redesigned.

---

## 7. Determinism and anti-cheat provisions

- Zero RNG tokens in AI decision paths (comment-stripped static scan, integ-1 precedent).
- Paired reruns byte-identical per stage (endpoint fingerprints: ledger digest + organ state hashes).
- Calibration: every instrument/control gets synthetic + control-arm bite checks before the official run (a control that cannot fire on a deliberately broken system is vacuous, not passing).
- The anti-reward probes from wave-6 travel with the system: any gradient toward a self-produced number, intensity inflation, or probe gaming fails the run.

---

## 8. Amendment rules

Any change to the curriculum, stage gates, control bars, seam contracts, organ inclusions/exclusions, strength regime, or kill criteria after Micah's approval needs a dated written amendment and his re-approval before the run. Harness/translation bug fixes (integ-1 A1–A3 precedent) are documented but do not need re-approval unless they change a behavioral bar.

---

## 9. Open questions for Micah

1. **Scale:** 10× of the pilot per-stage budget is preregistered. Is the 100× leg (S100) preregistered now, or gated on S10 passing?
2. **Strength regime:** arm B is provisional pending the S10/S100 audit. If the audit says B must run scale legs first, does integration wait?
3. **Defended-channel rule:** build the corroboration-before-re-COMMIT rule into this prereg now, or run it as a separate experiment first?
4. **Felt intensity:** confirmed OUT until its own verdict lands (rebuild/reposition/retire). Any objection?
5. **Phase 4 differentiation:** confirmed OUT (single-user integration). Correct?
6. **RC2 (elimination strictness as a controlled parameter):** fold into this integration's organ-5 activity, or keep as a separate trial?
