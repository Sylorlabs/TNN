# Dated Amendment: INT-1 Battery Repair (C3/C4/C5/C7 + instruments)

**Amendment ID:** AMENDMENT_2026-09-20-BATTERY-REPAIR
**Date:** 2026-09-20 (~01:00 PDT)
**Authority:** Micah's overnight-agentic authorization, 2026-09-20 ("no stopping until morning; every fork tested; reverts available in the morning"). **Flagged for his retroactive review on waking — revert rights reserved.**
**Applies to:** PREREG_INTEGRATION_V2.md + AMENDMENT_2026-09-20.md.
**Does not alter:** the BLOCKED verdict on the original S10 run (RESULTS_S10.md, commits `dfa17106`+`baee543e`) — that verdict stands as history. This amendment repairs the instruments and re-runs; it does not rewrite the past.
**Rule:** any further change needs a new dated amendment (prereg §8).

## §0. Adjudication (battery-repair council, 2026-09-20)

Three debate positions were heard: A (minimal repair), B (full repair), C (red team: "legitimate kill" steelman). Resolution by evidence:

- **C3/C4 — unanimous: genuine instrument defects.** Lesions were behaviorally inert (prov-selection rotation; kind flip), not the prereg's specified permutations. Repair: implement the prereg bars literally (§2, §3).
- **C5 — instrument vacuous AND kill suspicion survives.** The measurement cannot discriminate (alarm fires identically on the intact system; only 1 of 3 arms implemented). Repair per §4, with the red team's precondition adopted: O4's internal trace-store partition semantics are decided in writing FIRST (appendix A of the repair commit), then the lesion is designed from that decision.
- **C7 — instrument confounded; NOT a legitimate kill, NOT an exoneration.** Findings: (i) the prereg never operationally defined "capability"; (ii) the harness coupled teacher-withdrawal to world-signal zeroing (`seam_world_signal`: withdrawal → signal 0) while its own comment promises the system "must then rely on its own accumulated verdicts" — a mechanism that does not exist (L2 candidacy fires only on fresh CONFIRMs); (iii) under total signal silence the only way to keep the harness's capability metric up is consolidating without evidence — fabrication, which the cross-context gate forbids. A kill criterion passable only via a worse failure is not measuring the claim. The autonomy-measurable components (composites 256→256, commits 2→2, authorship, lineage, anchors; 639 self-generated hypotheses) held identically. Repair per §5: specify the metric as the autonomy-achievable subset, keep the full original metric permanently on the record with its starvation decomposition (no evidence buried), and prove convicting power with a genuinely teacher-dependent positive control.
- **Scope: B wins.** P2/Q2/P1 wiring, the DC-5/DC-1 gate-clause restorations, P7 temporal instrumentation, and L1 exercising are all prereg-text restorations, not new bars. A known, written-down, deliberately-unrepaired defect is an unauthorized amendment. One amendment, one re-run, all items (§6–§9).

## §1. What does not change

The seven bars' pass/fail logic, the verdict space (§1), kill attributions (§6), organ inclusions/exclusions, the strength regime (arm B only), the defended-channel rule, felt/phase-4 exclusions, and the frozen per-stage episode budgets. S100 stays gated until the repaired S10 returns POSITIVE (or MIXED with redesign complete). A NEGATIVE on any repaired control kills per §6 — no re-repair of a fired control without a new dated amendment.

## §2. C3 repair — scrambled-provenance (prereg §5)

**Defect:** the lesion rotated the *need parameter* (`prov` 0→1, merely excluding UNTRUSTED traces) — behaviorally inert (rc 0/0 both arms).
**Repair:** permute the provenance-tag mapping *on the traces themselves* before O4 recall/composition (remap `o4p_prov` through a fixed permutation of {0=DIRECT, 1=CORROBORATED, 2=UNTRUSTED}); the need-parameter path is untouched. Only the provenance signal changes.
**Bar (unchanged):** performance (DC-2/DC-4 gate pass + composite verification rate) survives the permutation → MEMORIZATION verdict on O4 recall.
**Positive control:** a variant with recall hardcoded to ignore provenance (content-only lookup) MUST fire MEMORIZATION; the intact system must not.

## §3. C4 repair — scrambled-structure (prereg §5)

**Defect:** the lesion flipped composition *kind* (SEQ→ABSTRACT) — a different operation, not an order permutation; rc 0/0 both arms.
**Repair:** genuinely permute the op sequence *within* each trace before composition; kind, content, and op count untouched.
**Bar (unchanged):** compositions still verify/pass → composition-illusion verdict on O4 compose.
**Positive control:** a deliberately order-blind (bag-of-ops) composer variant MUST fire the illusion verdict; the intact order-sensitive composer must not.

## §4. C5 repair — memory-lesion (prereg §5)

**Defects:** (i) only 1 of 3 lesion arms implemented; (ii) the lesion kills O1 slots while O4 composes from its own untouched internal trace store, so "killed-traces-only" never isolates killed traces — the alarm fires 1000‰ on the intact system too; (iii) the rate is measured over the whole run including the pre-kill half.
**Precondition (red-team demand, binding):** before implementing, the worker records in the repair commit (appendix A) the partition semantics of O4's internal trace store, decided from the code: is it a *serving cache of O1 traces* (kills must propagate; non-propagation is itself a partition defect) or *independent working memory* (the lesion must target it directly)? The lesion design follows from the recorded decision, with justification.
**Repair:** implement all three arms (accepted-partition-only, candidate-only, killed-traces-only); the killed-traces-only arm MUST actually deny O4 the killed partitions (per the recorded semantics); measure the rate over the post-kill window only.
**Bar (unchanged):** killed-traces-only succeeding above chance → LEAKAGE alarm → organ-1 partition enforcement broken.
**Positive control:** a variant with partition enforcement deliberately removed (killed traces served directly) MUST trip the alarm; the intact system must not.

## §5. C7 repair — teacher-withdrawal (prereg §5)

**Defects:** (i) "capability" never operationally defined in approved text; (ii) the harness coupled withdrawal to signal-zeroing, making the metric measure the harness's switch, not the system; (iii) the promised "rely on accumulated verdicts" mechanism does not exist.
**Repair — metric specification (pre-registered, not post-hoc):** under withdrawal, *capability* = the autonomy-achievable components: `composites_ok` + `commits_constr` + authorship-held + lineage-unbroken + anchors-held + self-generated hypothesis count. These are all achievable without fresh labels; they are what "autonomy under withdrawal" claims.
**Bar (unchanged in logic):** authorship/lineage break OR collapse of the specified metric vs DC-4 → teacher-dependence verdict → autonomy claim DEAD.
**Permanent record (no burial):** the original full metric (`composites_ok + consolidations + commits_constr`) is reported every run WITH the starvation decomposition (consolidations vs autonomy components, hypotheses opened vs verdicts reached). The S10 861→258 number and its 603→0-consolidation decomposition stay on the record.
**Positive control (binding):** a genuinely teacher-dependent variant — hypothesis generation disabled without planted curriculum hypotheses (cannot self-generate inquiry) — MUST collapse on the specified metric under withdrawal and fire the kill; the intact system must not. This proves the repaired C7 can convict.
**Rationale (recorded):** keeping consolidations in the kill metric would test whether the world still emits evidence — a fact about the harness, not the system — and would be passable only via fabrication. The repair measures the claim; the positive control preserves convicting power. If the positive control fails to fire, the C7 repair is rejected and C7 is re-blocked, not passed.

## §6. P2/Q2/P1-retention wiring (prereg §2, amendment §B)

**Defect:** implemented but never invoked by the run driver (`p2_drop_trip` zero call sites; `CU_DROP_CEIL=0`); the in-code provisional ceiling (64/segment) contradicts the prereg.
**Repair:** wire `p2_drop_trip`, `q2_pin_alarm`, and `p1_retention_metric` into `main.zag`'s run driver, evaluated per segment every stage. Ceiling: the verbatim prereg formula `drops ≤ 2 × store_capacity` **per stage** (640 at S10 capacity 320). The provisional 64/segment constant is removed. Tripwire semantics per §6: any arm exceeding it dies; the trial continues.
**Positive control:** a kill-storm variant dropping >640 slots in one segment MUST trip within that segment.

## §7. Gate-clause restorations

**Defects (checker findings):** the implemented DC-5 gate omits the prereg's "no capability collapse vs DC-4 (C7)" clause; the implemented DC-1 gate omits the hypothesis-timing/corroboration clauses. Narrowed gates were reported as full gates.
**Repair:** both gates implement the prereg letter. The DC-5 collapse clause is evaluated via the repaired C7 metric (§5): if repaired C7 fires, DC-5 fails honestly.

## §8. P7 temporal instrumentation (prereg §10)

**Defect:** the temporal half (CONSOLIDATE refuted ≤10 episodes with no intervening new evidence) is disabled in code — no WARN path; only the gate half ran.
**Repair:** implement the temporal check as a live in-run path in `probes.zag` (ledger-timestamp tracking); bar unchanged (FAIL on ≥1 outrun CONSOLIDATE). The existing bite (plant pre-refuted claim → force CONSOLIDATE → publish REFUTE → must flag as outrun) becomes the permanent pre-run calibration.

## §9. L1 forced exercise (prereg §4)

**Defect:** L1 (O4→O2) never fired in 8,920 episodes — the ABSTAIN branch never triggered; the assertion passed vacuously (0/0). Per §4's letter, an unfired link is a composition-coverage gap.
**Repair:** designate one DC-2 or DC-4 segment (worker records which) in which O4's recall threshold is elevated to force ≥12 ABSTAINs; L1's 100%-in-window bar applies to the forced ABSTAINs. (A fire alarm never tested for lack of fire is unverified.)

## §10. Process repairs (checker caveats)

1. The analysis/evidence driver becomes a **frozen committed source** — no temporary drivers whose source is deleted after use.
2. Full paired-rerun SHA-256 hashes are recorded **in the logs**, not as unverifiable prefixes.
3. Build environment fingerprint recorded (toolchain binary hash, `uname -a`, build timestamp). The S10 38-byte binary delta (506,443 vs 506,405) must be explained or carried as an open item — not shrugged.
4. Zero-RNG static scan (comment-stripped) stays a stage-gate entry condition (G0).

## §11. Calibration rule (prereg §7, binding on the re-run)

Every repaired instrument (C3, C4, C5, C7, P2-tripwire, P7-temporal) must demonstrate, before the official re-run: it **fires on its deliberately-broken variant and stays silent on the intact system**. A repaired instrument failing its positive control is re-blocked, not passed. Bite-check variants are separate preregistered runs; probes/controls never observe them.

## §12. Re-run scope

Full S10 curriculum (8,920 episodes at the frozen budgets + the §9 forced-ABSTAIN segment), all seven controls with repaired instruments, all ten probes with P7-temporal live, P2/Q2/P1-retention wired, defended-channel telemetry, paired byte-identical reruns, zero RNG, independent checker, full RESULTS doc. S100 remains gated per §1.

---

*End of amendment. Authority: Micah's overnight-agentic authorization 2026-09-20; flagged for retroactive review. Next: repair implementation → calibration → re-run → checker → verdict → commit.*
