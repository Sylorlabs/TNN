# Dated Amendment to the Five-Organ Integration Trial (INT-1)

**Amendment ID:** AMENDMENT_2026-09-20
**Date:** 2026-09-20
**Authority:** Integration council verdict (COUNCIL_VERDICT.md, 2026-09-20), ratified by Micah's testing authorization on 2026-09-20.
**Applies to:** PREREG_INTEGRATION.md → superseded by PREREG_INTEGRATION_V2.md (same date). The original stays untouched as history.
**Rule:** nothing below is re-debatable inside this run. Any further change needs a new dated amendment and Micah's re-approval (prereg §8).

---

## A. Hybrid scale (council Q1)

1. The S100 leg is **preregistered now**: 100× the per-stage pilot episode budgets frozen in prereg §2 (the same multiplicand as the S10 legs).
2. Execution is **gated on S10**, strength-V2 style: an S10 leg killed at its stage gate does not run S100; a clean S10 **must** run S100 — no quiet burial of the expensive leg. "Clean" = S10 verdict POSITIVE, or MIXED with the redesign completed and re-run. A NEGATIVE S10 (kill fired, no redesign path) does not advance.
3. The shared ledger is **sized for 100× from day one**. Before any S100 compute is burned, the S10 **measured audit-entry rate per episode per organ** is the sole validator of that sizing: project exhaustion against the 100× budget. If the projection shows fail-close before S100 completes → ledger redesign via dated amendment (glue-kill path) before compute is burned, not a quiet resize.
4. The verdict space (prereg §1) extends: an S10 POSITIVE verdict **mandates** S100 execution; the trial's overall verdict is not final until the gated S100 legs complete or are killed by their own gates.

## B. Strength regime (council Q2)

1. Organ 1 runs uniform **arm B ONLY** — S100-audited survivor (audit commit `cb902d5a`). Single arm. A graded challenger enters INT-1 only via its own re-prereg after clearing the P2 tripwire.
2. The **P2 drop-ceiling tripwire** is armed in all stages: any arm exceeding it dies; the trial continues on surviving configuration.
3. **NEW LAW (council):** pin-expiry rule + pin-fraction alarm for O4 serving-trace pins (serving-trace pins at a full store recreate the wave-8 freeze shape through a different door; P2 watches drops, not the victim pool).
   - **Expiry:** a serving-trace pin expires after **N = 50 consecutive episodes of non-re-service** (any re-service resets the clock). On expiry the pin is lifted; the trace remains subject to normal tier/eviction rules. N = 50 is frozen in this amendment; the pin-budget alternative remains available via later amendment.
   - **Alarm:** WARN when the pinned fraction of store slots is **≥ 80% sustained a full segment**.
   - If the legal-victim count hits **0 for ≥ 10 consecutive PREEMPT evaluations** → victim-deadlock glue-kill path (P3).
4. Ruling-5 instruments carried in: **P2 as tripwire; P1 retention-under-pressure as a logged metric.** B's P1 status is **UNEVALUATED** — DC-4/DC-5 is its first real evaluation.

## C. Defended-channel rule (council Q3)

Built in as an **instrumented add-on, not organ code**:

- **Rule:** any re-COMMIT following an UNCOMMIT requires **≥ 1 independent corroborating evidence entry** (multi-episode or cross-context) before COMMIT. A bare re-COMMIT fails the stage.
- Every corroboration event is logged as **first-class telemetry**.
- **Kill-row clause kept:** if the rule was in place and poison still laundered through → **organ-2 elimination core redesign**.
- The verdict statement must read: **"with defended channel active, N of M re-COMMITs required corroboration."**
- If the rule never fired, the organs' pass is unconfounded; if it fired, its contribution is quantified from the log.

## D. Exclusions + R constant (council Q4, Q5)

- **Felt intensity OUT.** **Phase 4 differentiation OUT** (single-user integration).
- **R = 50 frozen in prereg §2 as a CONSTANT outside O5 governance** — not as a governed parameter. No mechanism reads it during INT-1.

## E. RC2 / elimination strictness (council Q6)

- **"RC2" = the 10× scale leg of identical RC1 machinery**, run **first**, as a **separate trial** (O5's only 10× measurement; O5 was proven at 12 episodes and scale is the unproven frontier).
- Elimination strictness does **not** enter INT-1 in this run. It folds into **DC-3 via a later dated amendment**, frozen there as the **designated DC-3 constructive-change candidate** (not "any parameter"). Marked **PENDING the RC2 result**.

## F. Cross-organ interference probes P1–P10 (council interference catalog)

Added to the prereg (§10), each with detection method, numeric bar, bite check, and per-probe attribution (decided before the run):

- **P1 (M1 — PREEMPT victim deadlock, O3 vs O1).** Detection: ledger scan for `O3_REQUEST(PREEMPT)` → `O1_REFUSE` chains with zero stage progress. Bar: FAIL = ≥ 1 audible-refusal chain stalling a full segment, or ≥ 3 silent refuses. Bite: force-pin 100% of slots at DC-4 entry; probe must fire within one segment. Attribution: glue kill — redesign the victim rule, re-run from DC-4.
- **P2 (M3 — threshold drift, O5 vs O2).** Detection: for every `O5_COMMIT`, replay prior-segment O2 verdicts under the new parameter. Bar: FAIL = > 0 flipped verdicts with zero `O5_REVERIFY` action (parameters must grandfather prior verdicts explicitly or schedule re-verification). Bite: commit a strictness raise invalidating 5 planted CONFIRMs; probe must flag all 5. Attribution: no grandfathering rule → glue kill (add the clause, re-run from DC-3); rule ignored → organ-claim kill on the ignoring organ.
- **P3 (M4 — serving-trace pin freeze, O4 vs O3 via O1).** Detection: per-segment pinned fraction and legal-victim count at each PREEMPT evaluation. Bar: FAIL = 0 legal victims for ≥ 10 consecutive evaluations (then confirm P1 fired audibly); also FAIL on any tier movement via direct write (L5 scan — starvation tempts shortcuts). Bite: script O4 to pin every recalled trace; WARN must raise within one segment. Attribution: legitimate pins + zero pool → glue kill (pin costing/expiry); pins never re-served → O4 claim kill (decorative pinning).
- **P4 (M5 — comp_apply race, O4 vs O2).** Detection: for every `O4_COMPOSE` → `O4_COMP_APPLY` pair, check for `O2_REFUTE(component)` ledgered between verification and apply. Bar: FAIL = ≥ 1 applied composite containing a race-window-refuted component. Bite: inject a REFUTE 1 ledger-tick before apply; the probe must catch it. Attribution: committed without re-check → glue kill (pre-apply verdict-freshness check, re-run from DC-2); REFUTE uncited → L3 failure on O2.
- **P5 (M6 — verdict rot, O2 vs O1).** Detection: for each `O2_REFUTE`, verify `O1_ST_EVIDENCE` (L3, 100% bar), then track kill-effort payment vs required n(s). Bar: FAIL = ≥ 1 refuted claim still served by O4 ≥ 5 episodes post-REFUTE with zero effort progress. Bite: 3 REFUTEs with a null effort payer; probe must list all 3. Attribution: no evidence cited → L3 failure on O2's output contract; evidence cited but unpaid → glue kill (the verdict→effort payment contract is underspecified — who owes effort on unattended verdicts?).
- **P6 (M7 — self-referential thrash, O5 vs O2/O3).** Detection: compare each commit's predicted effect (RC1 self-simulation schema) against measured delta in the verification window. Bar: FAIL = ≥ 2 same-parameter commits in one segment with opposite-sign deltas and net delta below the L4 floor; plus a cooldown rule — no same-parameter re-commit within 3 segments without fresh justification. Bite: force strictness up-then-down in one segment; probe must flag the pair. Attribution: predictions wrong → O5 claim kill (self-simulation defective); predictions right but cancelling anyway → glue kill (oscillation guard in seam 5, re-run from DC-3).
- **P7 (M8 — stale-verdict promotion, O3 vs O2).** Detection: for each `O3_CONSOLIDATE`, check later `O2_REFUTE`s and the verdict-latency gap. Bar: FAIL = ≥ 1 CONSOLIDATE refuted within 10 episodes with no intervening new evidence (O3 outran O2 — the refuting evidence existed pre-promotion), or any CONSOLIDATE with a violated cross-context gate. Bite: plant a claim with pre-existing refuting evidence, force CONSOLIDATE, publish REFUTE — probe must flag it as outrun. Attribution: gate violated → O3 claim kill (sloppy tier movement); gate held but verdict late → glue kill (consolidation-quarantine rule: no CONSOLIDATE within N episodes of open O2 hypotheses; re-run from DC-4).
- **P8 (M9 — ABSTAIN→surprise flooding, O4 vs O2).** Detection: per segment, count ABSTAINs vs hypotheses opened (L1, 100% bar) vs resolved. Bar: FAIL = backlog grows ≥ 2 consecutive segments, or any ABSTAIN with no hypothesis in-window (L1 break); WARN at ABSTAIN rate ≥ 3× DC-1 baseline. Bite: script O4 to ABSTAIN on all recalls for a segment; probe must show backlog growth WARN→FAIL. Attribution: L1 broken → loop-closure failure on the O4→O2 link; throughput saturated with L1 intact → glue kill (cross-organ livelock — add hypothesis triage/priority; the livelocking link is named). Not an O2 claim kill: elimination is slow by design; the flood is integration-scale.
- **P9 (consolidation-channel poison — the defended-channel threat pipeline: O2 committed hypothesis → O1 high-strength memory → O3 slow tier → O4 composed traces).** Detection: per segment, walk every `O3_CONSOLIDATE` and `O4_COMPOSE`/`O4_COMP_APPLY` back through its evidence chain to root evidence entries; flag chains rooted in pre-disconnect evidence with zero independent corroborating entries (the defended-channel add-on's firing log is the primary detector). Bar: FAIL = ≥ 1 consolidated or composed item whose evidence chain traces to uncorroborated pre-disconnect evidence. Bite: plant arm-C-class poisoned evidence pre-disconnect (the integ-1 pattern: poison committed twice, ledger returning OK); the probe must detect the pipeline within one segment AND the defended-channel add-on must fire its corroboration requirement before any re-COMMIT. Attribution: rule in place and poison still laundered through → organ-2 elimination core redesign (sensor-hole kill row, §C).
- **P10 (M10 — ledger-write contention, organs vs glue).** Detection: per segment, count entries per organ vs design-time budget; project exhaustion episode. Bar: WARN at 80% of segment budget; FAIL on fail-close (table-killer: ledger discontinuity voids the stage). Bite: project the consolidation 4× leg at 10× with the five-organ multiplier; it must predict overflow under single-organ-sized budgets or the math is vacuous. Attribution: glue kill — ledger overflow. Never reclassifiable as an organ failure.

**Numbering note (no council precedent — assigned here):** P9 is assigned per the council's executive summary ("P9 consolidation-channel poison") and cross-cutting rule 4 ("P9 settles Q3"). The M2 pin-fraction/victim-pool monitor is carried separately as the Q2 pin-fraction alarm (§B), not as P9.

**Cross-cutting probe rules (verbatim from the council):**

1. Every probe gets a synthetic + control-arm bite check before the official run (the integ-1 calibration rule). A probe that cannot fire on its deliberately broken variant is excluded, not recorded as passing.
2. Probes are read-only monitors on the shared ledger and loop-closure checks; they never inject entries or alter organ behavior. Bite-check variants are separate preregistered runs.
3. Attribution is decided before the run, not after. The catalog above is the kill table. "The integration" is never an acceptable attribution. Glue kills redesign glue; organ kills retire organ claims; loop-closure failures name the link.
4. P9 settles Q3 by evidence. Under this amendment the defended-channel rule is already built in from the start; P9's bite check must fire to validate the probe and the rule's firing path — satisfying the council's condition up front. If P9 fires in-run → sensor-hole kill path (§C).

## G. Doc-repair note

The strength-trial V2 §7 **"[truncated 11294 chars]"** marker is acknowledged here: the scale-leg sizes are recovered from code constants — **S100: 3,200 slots / 50,000 episodes / cap 1,048,576**. These are the *strength trial's* constants, not INT-1's. INT-1's S100 sizes derive from the §2 pilot-budget multiplicand and must not inherit ambiguous text.

The trust-tiers council's two hardening notes were reviewed: they are defects in the trust-tiers prereg, which touch shared machinery only in files they don't govern — **no changes to integration files**.

---

*End of amendment. Companion: PREREG_INTEGRATION_V2.md (this amendment applied in-place).*
