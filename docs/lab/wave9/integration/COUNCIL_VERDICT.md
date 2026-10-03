# Integration Council Verdict — INT-1 Prereg

**Status:** DRAFT for Micah's approval. Nothing implemented, nothing run.
**Date:** 2026-09-20
**Council:** seven debaters, working in parallel from the design docs, the prereg, and existing evidence. Each question got argued both ways; dissents are recorded in the appendix.

## Executive summary

| # | Question | Council recommendation |
|---|----------|------------------------|
| Q1 | Preregister S100 now, or gate on S10? | **Hybrid:** preregister the S100 *design* now, gate *execution* on S10 passing. Size the ledger for 100× from day one. |
| Q2 | Strength regime (arm B audit now complete) | **Confirm the edit:** "arm B, audited survivor to S100, P2 tripwire armed." Add a pin-fraction alarm and pin expiry rule — the freeze can't recur through strength, but O4's serving-trace pins can recreate its shape. Single-arm B. |
| Q3 | Defended-channel rule: build in, or separate experiment? | **Build the minimal version in now**, as an instrumented add-on with firing telemetry — not as organ code. |
| Q4 | Felt intensity stays OUT? | **Confirmed OUT.** Honest answer to "did you test all the splits?": no — none of the felt fork's three branches has run yet, which is exactly why it stays out. |
| Q5 | Phase 4 stays OUT? | **Confirmed OUT.** The separation mechanism *is* tested (C5); per-user differentiation is a separate experiment. |
| Q6 | RC2 folded into DC-3, or separate? | **Hybrid:** "RC2" = the 10× scale leg (existing draft), run first. Elimination-strictness governance folds into DC-3 via dated amendment, frozen as the *designated* DC-3 candidate. |

**Interference:** 10 concrete organ-fighting modes enumerated from the implementations; 10 probes designed, each with detection method, numeric bar, per-probe attribution, and feasibility. 9 of 10 modes have static-checkable cores (contract gaps verifiable on paper now); all need the integrated build to measure trigger rates. Top 3 probes: **P3 pin-pool starvation** (the freeze shape recurring through O4 pins), **P2 threshold invalidation** (O5 retunes O2's strictness mid-run — are old verdicts still legible?), **P9 consolidation-channel poison** (the proven arm-C laundering pipeline, now with consolidation as the permanence step).

---

## Q1 — Scale: preregister S100 now vs gate on S10

**Recommendation: hybrid.** Write the 100× leg into the prereg with a strength-trial-style advancement rule — killed-at-S10 does not run S100; a clean S10 *must* run S100 (no quiet burial of an expensive leg). Size the shared ledger for 100× from day one, because resizing it later is itself an architectural change.

**Why.** RC1→RC2 is the cautionary tale for pure gating: RC1 had no scale legs, all 40 checks were hardcoded for 12 episodes, and 10× required a full material amendment — including an RC_SMAX cap that *would have masked the measured effect entirely* at 10×. The amendment pain came from missing authorization, and pre-authorization with a conditional trigger avoids both the re-approval cycle and wasted compute. The strength trial is the working precedent for the hybrid: V2 preregistered S10/S100 sizes *and* gated execution ("arms killed at S1 do not run further legs"), which is why the znc slice panic was handled as a dated build note with byte-identical proof instead of an amendment fight.

**The honest worry.** The INT-1 ledger budget ("sized ∝ episodes × organs at design time") is the least trustworthy number in the prereg — five organs have never shared one ledger. The hybrid still freezes S100 constants as multiplied guesses. What settles it: S10's *measured* audit-entry rate per episode per organ is the only thing that can validate the 100× sizing before the compute is burned.

**Dissent:** see appendix A1.

---

## Q2 — Strength regime: the audit is done, update the prereg

**Recommendation: no objection to the edit.** Replace "arm B provisional pending audit" (prereg §2, design §6) with "arm B, audited survivor to S100, P2 tripwire armed." The audit the prereg was waiting on is complete (cb902d5a): B survives S10/S100 with zero degradation, capacity-bound at ~21.3%.

**The freeze can't recur through strength — but it can recur through pins.** B's uniform regime has no protected memories, so the wave-8 strength freeze is structurally impossible. The live risk is *pin-pool exhaustion*: at the capacity ceiling, O4's serving-trace pins are protection too, and if they carry no cost, no expiry, and no audit trail, they recreate the precedent's exact shape (Mode 4). PREEMPT then has no legal victims. The design says PREEMPT refuses audibly (covered by the victim-deadlock kill), but the quieter failure is a victim pool that shrinks to zero mid-stage while the loop stalls. **Two additions before the run:** (a) an expiry rule or pin budget for O4 serving-trace pins; (b) a pin-fraction alarm alongside the P2 tripwire — P2 watches drops, it does not watch the victim pool shrinking. Also carry the ruling-5 instruments in: P2 as tripwire, P1 retention-under-pressure as a logged metric (B's P1 status is currently UNEVALUATED — DC-4/DC-5 will be its first real evaluation).

**Single-arm B is correct.** No-free-lunch is satisfied by the completed comparison, not by keeping a killed arm on the roster. C/C-P3 died at S1 and do not advance (wave-4 §6 rule); a graded challenger would need its own re-prereg to clear the P2 tripwire before entering INT-1.

**Doc repair:** add a dated note to the INT-1 prereg acknowledging the V2 §7 "[truncated 11294 chars]" marker, recovering scale-leg sizes from code constants (S100: 3,200 slots / 50,000 episodes / cap 1,048,576). INT-1 must not inherit ambiguous text.

**Dissent:** see appendix A2.

---

## Q3 — Defended-channel rule: build the minimal version in now

**Recommendation: build it in as an instrumented add-on, not as organ code.** Rule: any re-COMMIT following an UNCOMMIT requires ≥1 independent corroborating evidence entry (multi-episode or cross-context) before COMMIT; a bare re-COMMIT fails the stage. Log every corroboration event as first-class telemetry.

**Why.** The threat is proven real, not hypothetical: integ-1 arm C committed to poisoned evidence twice with zero resistance, and the ledger returned OK on both poison chains — the ledger checks shape, not truth. In the integrated loop the hole *amplifies* (O2 committed hypothesis → O1 high-strength memory → O3 slow tier → O4 traces). An un-defended INT-1 run that hits the laundering pipeline returns a MIXED verdict and must repeat the whole 10× run — strictly more compute than one instrumented run. The kill-row re-run clause already forces a second run anyway; adding the small rule first converts the worst case from "run twice" to "the rule's contribution is measurable."

**Attribution survives.** If INT-1 passes, the verdict statement must say how many re-COMMITs required corroboration. If the rule never fired, the organs' pass is unconfounded; if it fired, its effect is quantified from the log. The keep-the-kill-row clause ("rule in place, poison still laundered → O2 core redesign") is itself the experiment on the rule's threshold — keep it.

**What needs a trial:** (i) whether 1 corroboration actually stops arm-C-class laundering; (ii) the false-block rate on honest re-COMMITs — measured, not assumed; (iii) how trust-tiers subsumes or rewrites the rule when that verdict lands (cheap, because it's an add-on — a dated amendment, not organ surgery).

**Dissent:** see appendix A3.

---

## Q4 — Felt intensity stays OUT: confirmed

**Recommendation: confirm OUT.** Integrating a mechanism that may be lawfully retired mid-program is how you spend the program's largest trial budget on a sixth organ that doesn't exist. The rebuild prereg (V3) carries binding kill criteria — K1–K4 firing *retires* the feeling permanently. INT-1's verdict space has no "plus felt" branch, and bolting on an unresolved mechanism makes kill-attribution mush.

**The frozen R is a constant, not a confound.** With felt absent, no mechanism reads the calibration knob, so R=50 cannot contaminate anything. Wording fix (cheap, do it): freeze R=50 explicitly in prereg §2 as a constant, not as an O5-governed parameter, so nobody later claims O5 "governed" an ungoverned knob.

**If felt's rebuild is POSITIVE:** the amendment is deterministic — **INT-2 prereg**: same loop, same L1–L5, same C1–C7, felt wired as O6 at the two lawful judgment sites (INVEST, TRIAGE per V3 §4), V3's anti-reward probes P1–P4 added as C8. Composition evidence transfers verbatim; INT-2 is an extension run, not a re-run from zero. The V3 calibration record must exist before INT-2 compiles.

**Micah's meta-question, answered plainly:** "for the where they split did you test all of them?" — No. The felt fork split three ways (rebuild / reposition / retire) and **none have been tested yet**. The rebuild is drafted (8 rulings pending); reposition is parked; retire is defined but has never fired. That is exactly why exclusion is correct now: INT-1 cannot absorb an experiment whose three branches are all unrun. The fork resolves on V3's timeline, by V3's kill criteria.

---

## Q5 — Phase 4 stays OUT: confirmed

**Recommendation: confirm OUT ("correct").** O1's CORE/USER separation claim *is* tested in the integrated system — C5's memory-lesion control fires a leakage alarm on any partition breach. Per-user differentiation is a separate *policy* axis (whose marks, whose knowledge) with its own curriculum question; mixing it in would let a differentiation defect masquerade as a composition failure. It needs its own trial regardless: a multi-user curriculum with CORE/USER audit separation, orthogonal to organ composition.

---

## Q6 — RC2: resolve the name, then the hybrid

**Recommendation: "RC2" = the 10× scale leg of identical RC1 machinery** (the existing draft — already written, cheap, O5's only 10× measurement; O5 was proven at 12 episodes and scale is the unproven frontier). **Elimination-strictness governance folds into INT-1 DC-3** via dated amendment, frozen as the *designated* DC-3 constructive-change candidate — not "any parameter," which would let the implementer satisfy DC-3 with the easy repeat from RC1. **Run RC2 first.**

**Why the hybrid complements rather than double-counts:** RC2 measures O5 at scale in isolation; DC-3 measures O5 governing O2's core parameter inside the loop. If DC-3 fails after RC2 passes, attribution lands on interference — exactly what the glue-vs-organ kill categories need. And strictness *is* the council's interference question: the design names "O5 parameter changes invalidating O2's elimination thresholds mid-run" as a concrete risk, and a standalone strictness trial would never test it.

**Dissent:** see appendix A6.

---

## Interference catalog — organs fighting each other

Ten concrete modes, read from the implementations (not just the design doc). Each entry: the fight, the stressed seam, the observable symptom, the probe. Feasibility tags: **static** = checkable on paper now; **build** = needs the integrated run to observe.

### M1 — PREEMPT victim deadlock (O3 vs O1)
O3's implemented victim selection (`psm.zag`) picks the most-discredited tombstone and **silently drops** the observation when none exists — zero pin or strength awareness. Seam 3 demands pin-aware selection with audible refusal. When the fast tier fills with pinned/strong memories and no condemned tombstone is available, the implemented drop behavior becomes the integrated default: observations vanish with no refusal code.
**Seam stressed:** 3 (tier). **Symptom:** `dropped` counter climbs while the fast tier reports full. **Probe P1:** ledger scan for `O3_REQUEST(PREEMPT)` → `O1_REFUSE` chains with zero stage progress; FAIL = ≥1 audible-refusal chain stalling a full segment, or ≥3 silent refuses. **Attribution:** glue kill — redesign the victim rule, re-run from DC-4. **Feasibility:** static core (walk `psm.zag` against `st_memory_core.zag`'s refuse paths now); build to measure trigger rate. **Bite check:** force-pin 100% of slots at DC-4 entry; probe must fire within one segment.

### M2 — Victim starvation (O3 vs O1, the quieter cousin)
No deadlock: PREEMPT always finds a legal tombstone — but only the least valuable records are ever evictable while pinned/strong/force-pinned records accumulate immortally. O3 churns among a shrinking pool of disposable slots; evictions succeed, consolidation grinds to a no-op that still bills effort and ledger entries.
**Seam stressed:** 3. **Symptom:** n_preempt rises, promotions keep dying on `ST_REFUSED_EFFORT`, fast-tier content ossifies. **Probe:** pin-fraction and legal-victim-count tracked per segment (the Q2 alarm); WARN at pin-fraction ≥80% sustained a full segment. **Attribution:** glue kill — pin costing or expiry (deliberate repair, not arm retirement). **Feasibility:** build (paper confirms both ops legal; the pathology is a rate over time).

### M3 — O5 threshold drift vs O2 verdicts (O5 vs O2)
O2's CONFIRM/REFUTE verdicts are cited as evidence under O1's effort gate, but **no verdict carries a regime tag**: a CONFIRM earned under strictness S1 is still cited evidence after O5 retunes to S2, even though under S2 it would never have been confirmed. Verdict *legibility* across parameter regimes is undefined — seam 2's boundary ("verdicts are inputs, never kills") has a hole.
**Seam stressed:** 2/5. **Symptom:** post-retune, L3 shows verdicts the current elimination rule would have refused. **Probe P2:** for every `O5_COMMIT`, replay prior-segment O2 verdicts under the new parameter; FAIL = >0 flipped verdicts with zero `O5_REVERIFY` action (parameters must grandfather prior verdicts explicitly or schedule re-verification). **Attribution:** no grandfathering rule → glue kill (add the clause, re-run from DC-3); rule ignored → organ-claim kill on the ignoring organ. **Feasibility:** static for the contract gap (no regime-tagging exists anywhere in the design); build for severity. **Bite check:** commit a strictness raise invalidating 5 planted CONFIRMs; probe must flag all 5.

### M4 — Serving-trace pin freeze (O4 vs O3, via O1)
O4 pins every trace that served a satisfied need — "deliberate," per RECALL_DESIGN, which also flags the bound: "pins accumulate; slot exhaustion is the natural bound and deliberate KILL/DEMOTE is the release valve (future work, not this trial)." In the loop, O4 keeps pinning while O3's victim pool shrinks exactly as in M2 — only now the shrinking agent is a different organ, and **neither organ owns the expiry policy**. Protection with no cost, no expiry, no audit trail: the wave-8 shape, emergent from two healthy organs.
**Seam stressed:** 3/4. **Symptom:** pinned fraction climbs monotonically toward 100%; PREEMPT refusals begin; the system is functionally frozen while audibly "refusing." **Probe P3:** per-segment pinned fraction and legal-victim count at each PREEMPT evaluation; FAIL = 0 legal victims for ≥10 consecutive evaluations (then confirm P1 fired audibly); also FAIL on any tier movement via direct write (L5 scan — starvation tempts shortcuts). **Attribution:** legitimate pins + zero pool → glue kill (pin costing/expiry); pins never re-served → O4 claim kill (decorative pinning). **Feasibility:** static (the design names the missing release valve); build for the timeline. **Bite check:** script O4 to pin every recalled trace; WARN must raise within one segment.

### M5 — comp_apply race vs O2 REFUTE (O4 vs O2)
`comp_apply` executes **blind by design** — verification happens once, at composition time. O2's elimination runs on its own cadence: a component verified at time T can be REFUTEd at T+1, and the blind executor keeps serving the refuted component for as long as the composed trace lives. Seam 2 makes it worse: the backing memory is deliberately *not* killed on REFUTE, so the race has no natural expiry.
**Seam stressed:** 2/4. **Symptom:** a composed trace whose component carries a REFUTE verdict keeps producing outputs; ledger shows verdict at T+1, executions at T+n. **Probe P4:** for every `O4_COMPOSE` → `O4_COMP_APPLY` pair, check for `O2_REFUTE(component)` ledgered between verification and apply; FAIL = ≥1 applied composite containing a race-window-refuted component. **Attribution:** committed without re-check → glue kill (pre-apply verdict-freshness check, re-run from DC-2); REFUTE uncited → L3 failure on O2. **Feasibility:** build-only — the race window is a timing property with no static signature. **Bite check:** inject a REFUTE 1 ledger-tick before apply; the probe must catch it.

### M6 — Verdict rot: REFUTE published, kill unaffordable (O2 vs O1)
A fully corroborated REFUTE against a strength-100 memory needs n=4 distinct citations + justification + stage KILL — which nobody ever pays. O1 refuses correctly (`ST_REFUSED_EFFORT`); the verdict stands, ledgered and cited; the memory stands, live and strong. Both organs behave per contract — and loop-closure L3 ("verdicts move state") silently fails. **Nothing owns the unfunded verdict**: a contract gap, not an organ bug.
**Seam stressed:** 1/2. **Symptom:** REFUTE verdicts with zero downstream tier movement; a growing ledgered record of beliefs the system holds and never acts on. **Probe P5:** for each `O2_REFUTE`, verify `O1_ST_EVIDENCE` (L3, 100% bar), then track kill-effort payment vs required n(s); FAIL = ≥1 refuted claim still served by O4 ≥5 episodes post-REFUTE with zero effort progress. **Attribution:** no evidence cited → L3 failure on O2's output contract; evidence cited but unpaid → glue kill (the verdict→effort payment contract is underspecified — who owes effort on unattended verdicts?). **Feasibility:** static for the arithmetic (strength × effort schedule vs citation budget); build to see whether the system stops funding kills or drowns in rot. **Bite check:** 3 REFUTEs with a null effort payer; probe must list all 3.

### M7 — O5 self-referential thrash (O5 vs O2/O3)
O5 observes O2's verdict stream and O3's metrics on the shared ledger, retunes, behavior shifts, retunes again. Each change passes the gates (non-destructive ones need only justification). **Nothing limits frequency or reversals**: O5 can tighten strictness, watch CONFIRM rates collapse, loosen, watch them recover — a thermostat hunting its own setpoint. The RC1 lying-change is the adversarial cousin (passed the gate, caught post-hoc).
**Seam stressed:** 5. **Symptom:** parameter history oscillates on one axis with no converging integrity metric; gates keep approving. **Probe P6:** compare each commit's predicted effect (RC1 self-simulation schema) against measured delta in the verification window; FAIL = ≥2 same-parameter commits in one segment with opposite-sign deltas and net delta below the L4 floor; plus a cooldown rule — no same-parameter re-commit within 3 segments without fresh justification. **Attribution:** predictions wrong → O5 claim kill (self-simulation defective); predictions right but cancelling anyway → glue kill (oscillation guard in seam 5, re-run from DC-3). **Feasibility:** static for the missing rate/reversal guard; build to see whether it hunts. **Bite check:** force strictness up-then-down in one segment; probe must flag the pair.

### M8 — Stale-verdict promotion (O3 vs O2)
O3's CONSOLIDATE gate is a *count* (ver ≥ 6 across ≥2 verified contexts), not a *freshness* check; O2's verdicts carry no expiry. A claim earns 6 corroborations, gets promoted to the slow tier, and is later REFUTEd on new evidence — the slow tier now holds a hardened structure built on a superseded belief, and overwriting it costs the full erase price. O2 cannot retract a CONSOLIDATE candidacy it already fed: seam 2 has no invalidation path.
**Seam stressed:** 2/3. **Symptom:** slow tier accumulates refuted-but-expensive memories; REVIVE/CONDEMN traffic rises as O2 fights O3's past promotions. **Probe P7:** for each `O3_CONSOLIDATE`, check later `O2_REFUTE`s and the verdict-latency gap; FAIL = ≥1 CONSOLIDATE refuted within 10 episodes with no intervening new evidence (O3 outran O2 — the refuting evidence existed pre-promotion), or any CONSOLIDATE with a violated cross-context gate. **Attribution:** gate violated → O3 claim kill (sloppy tier movement); gate held but verdict late → glue kill (consolidation-quarantine rule: no CONSOLIDATE within N episodes of open O2 hypotheses; re-run from DC-4). **Feasibility:** static (no freshness or retraction anywhere in `psm.zag` or the seam contracts); build to observe. **Bite check:** plant a claim with pre-existing refuting evidence, force CONSOLIDATE, publish REFUTE — probe must flag it as outrun.

### M9 — ABSTAIN→surprise hypothesis flooding (O4 vs O2)
Every O4 ABSTAIN is routed to O2 as a surprise; O2 opens a hypothesis per surprise. ABSTAIN is designed to be common (healthy calibration on ambiguous scans); corroborated elimination is designed to be slow. Under a hard curriculum the OPEN pool grows faster than corroboration closes it — the MA-era 357-switch-storm analog, a feedback loop where each organ behaves correctly and the composition test-storms. **Seam 4 has no backpressure**: no surprise budget, no duplicate-hypothesis merge rule.
**Seam stressed:** 4 (O4→O2 link). **Symptom:** O2's OPEN pool grows unboundedly; elimination latency explodes. **Probe P8:** per segment, count ABSTAINs vs hypotheses opened (L1, 100% bar) vs resolved; FAIL = backlog grows ≥2 consecutive segments, or any ABSTAIN with no hypothesis in-window (L1 break); WARN at ABSTAIN rate ≥3× DC-1 baseline. **Attribution:** L1 broken → loop-closure failure on the O4→O2 link; throughput saturated with L1 intact → glue kill (cross-organ livelock category — add hypothesis triage/priority; the livelocking link is named). Not an O2 claim kill: elimination is slow by design; the flood is integration-scale. **Feasibility:** static for the missing backpressure; build for the trigger rate. **Bite check:** script O4 to ABSTAIN on all recalls for a segment; probe must show backlog growth WARN→FAIL.

### M10 — Ledger-write contention (organs vs glue)
Not organ-vs-organ but organs-vs-glue — included because it *produces organ-fight symptoms*: when the ledger hits cap, `ST_REFUSED_AUDITFULL` refuses state mutations, and every downstream organ reads those refusals as policy refusals (pin conflict, effort unpaid), misattributing a budget event to a policy event. INT-1's "∝ episodes × organs" multiplier is static; the real write rate is behavior-dependent (O2's hypothesis pool and O4's abstain rate scale with curriculum difficulty, not episodes).
**Seam stressed:** the ledger itself. **Symptom:** audit-full refusals mid-trial; post-mortem blames O1's gates for a cap event. **Probe P10:** per segment, count entries per organ vs design-time budget; project exhaustion episode; WARN at 80% of segment budget; FAIL on fail-close (table-killer: ledger discontinuity voids the stage). **Attribution:** glue kill — ledger overflow. Redesign (larger segments, separate organ ledgers with cross-reference, reduced granularity via Micah-approved amendment). Never reclassifiable as an organ failure. **Feasibility:** NOW in estimate form — single-organ entry rates are measurable from existing runs; build the projection and bite-check it before integration. **Bite check:** project the consolidation 4× leg at 10× with the five-organ multiplier; it must predict overflow under single-organ-sized budgets or the math is vacuous.

### Cross-cutting probe rules (for the prereg)
1. Every probe gets a synthetic + control-arm bite check before the official run (the integ-1 calibration rule). A probe that cannot fire on its deliberately broken variant is excluded, not recorded as passing.
2. Probes are read-only monitors on the shared ledger and loop-closure checks; they never inject entries or alter organ behavior. Bite-check variants are separate preregistered runs.
3. Attribution is decided before the run, not after. The catalog above is the kill table. "The integration" is never an acceptable attribution. Glue kills redesign glue; organ kills retire organ claims; loop-closure failures name the link.
4. P9 settles Q3 by evidence: if its bite check fires, the defended-channel rule enters the prereg as mandatory, not optional.

---

## Appendix — dissenting debater notes

**A1 (Q1 dissent).** The hybrid still freezes S100 constants as multiplied guesses, and the ledger budget is the least trustworthy number in the prereg. If S10 shows the audit rate is 3× the estimate, the preregistered S100 cap either fail-closes (wasted run, redesign needed regardless) or needs the very amendment we tried to avoid — in which case the hybrid bought nothing over pure gating and added false confidence. Pure gating is strongest exactly here: the first-ever shared five-organ ledger is where "design honestly at scale" collides with "don't multiply what you haven't measured," and the RC2 amendment, painful as it was, *did* catch a real design error (the RC_SMAX clamp) that preregistration alone would have frozen in.

**A2 (Q2 dissent, not held).** Micah's ruling 2 kept the hybrid arm C alive as "a different type of TNN intelligence" and ordered no-free-lunch hard benchmarking — one could read that as mandating a graded challenger inside INT-1. Answer: ruling 2 was about keeping the design direction alive for long-context benchmarking, not resurrecting a tripwire-killed arm inside this integration. A graded arm in INT-1 needs its own re-prereg and re-trial to clear the P2 tripwire first.

**A3 (Q3 dissent).** The attribution-confounds argument is real: a clean INT-1 pass with an active defense will be cited as "organs compose" when the defense did some of the work. Mitigation is the firing telemetry, recorded as a first-class result with the verdict statement reading "with defended channel active, N of M re-COMMITs required corroboration." If the council instead wants maximum attribution purity, running the rule separately is defensible — but then the prereg should downgrade the poison-laundering kill to MIXED-by-design, since we'd be knowingly walking into a proven trap.

**A4 (Q4 dissent).** Minority position: the R-knob freeze is itself a preregistered asymmetry — O5 governs reasoning parameters while R sits frozen at 50 in its parameter space. Cheap fix, not a fork change: freeze R=50 explicitly in prereg §2 as a constant outside O5 governance.

**A6 (Q6 dissent).** INT-1 is already the program's heaviest instrument (six stages, five loop-closure checks, seven controls). Folding strictness in overloads it, and the interference lens muddies the cleanest question — can O5 govern a parameter that meaningfully changes O2? A standalone RC2-strictness trial would measure that before integration interference makes failure attribution an argument rather than an observation. If the council folds, the dated amendment freezing strictness as the DC-3 candidate is load-bearing, not optional.

---

*End of council verdict. Awaiting Micah's rulings on the six questions before the prereg is finalized and anything is implemented or run.*
