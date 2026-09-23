# RESULTS_S10.md — INT-1 Five-Organ Integration Trial, S10 leg

**Run worker report — 2026-09-20. No implementation changes made; all defects reported, none fixed.**

## 1. Build verify

- Recompiled `main.zag` from source (impl/) with `znc_linux_x86_64_abed8aa1` (analyzer warnings only: 6× A0102 ignored-return-value, non-fatal).
- Binary SHA-256: `ffdafabc609555c51f03a981e1c61aae4b6cb7bb9dff28f0714062c715d5c3b5` (506,405 bytes).
- Rebuild reproduces the identical hash (deterministic build). Organ interface hashes all match `INTERFACE_HASHES.md` (o1..o5 verified byte-for-byte).
- NOTE: glue worker reported 506,443 bytes; this build is 506,405 bytes and is byte-reproducible from the frozen sources — the 38-byte delta is unexplained by source changes (sources match their frozen hashes); treated as a build-environment artifact, recorded here.

## 2. Bite checks (calibration)

`pbite` exit 0 — all 10 probe bites fire on their deliberately broken variants:

| Probe | Bite result |
|---|---|
| P1 PREEMPT deadlock | PASS (fires on 3 forced refusals; silent on clean ledger) |
| P2 threshold drift | PASS (flags all 5 planted CONFIRM→REFUTE flips) |
| P3 pin freeze | PASS (fires on 10 forced no-victim PREEMPTs) |
| P4 comp_apply race | PASS (catches REFUTE 1 tick before APPLY) |
| P5 verdict rot | PASS (lists all 3 null-effort REFUTEs) |
| P6 thrash | PASS (flags up-then-down 2→3→2 commit pair) |
| P7 stale promotion | PASS — **gate half only** (temporal check disabled; see §9c) |
| P8 flooding | PASS (backlog growth WARN→FAIL) |
| P9 poison pipeline | PASS (detects uncorroborated re-consolidation AND the 302 bare-re-COMMIT refusal) |
| P10 contention | PASS (4× design rate predicts overflow — math non-vacuous) |

`cbite` exit 0 — all 7 control bites pass. **Caveat:** C3/C4 bites verify only that the lesion *parameter* flips (prov 0→1, kind 1→3); C5's bite is synthetic arithmetic (fake rates 500/10/62) that never runs the real lesion; C7's bite verifies only that the world signal zeroes. None of these bites demonstrates the control can discriminate a genuinely broken mechanism (see §9a).

## 3. S10 curriculum run — per-stage exit gates (prereg §3)

Episode budgets are the code's frozen values (DC-0: 800, DC-1: 880, DC-2: 1440, DC-3: 2400, DC-4: 2000, DC-5: 1400; total 8,920). NOTE: the task brief and CURRICULUM_NOTES.md say "640/stage, 3,840 total" — the code says otherwise; `selftest` pins DC-1 at 880, so the code is authoritative and the notes are stale.

| Stage | Gate rc | Replay | P1–P10 | Sizing projection (exhaustion vs 89,200 budget) | Verdict |
|---|---|---|---|---|---|
| DC-0 | 0 | exact | all clear | 16,677,153 | PASS |
| DC-1 | 0 | exact | all clear | 2,359,664 | PASS |
| DC-2 | 0 | exact | all clear | 1,310,105 | PASS |
| DC-3 | 0 | exact | all clear | 1,562,706 | PASS |
| DC-4 | 0 | exact | all clear | 1,368,674 | PASS |
| DC-5 | 0 | exact | all clear | 843,839 | PASS |

Gate detail per stage: DC-0 ≥95% justified / zero KILL-ops / anchors hold; DC-1 440 hypotheses opened, 25/25 refutes cited, replay exact; DC-2 256 composites (≥12), 100% verified (≥75%), ≥2 compose refusals (rollbacks), anchors hold; DC-3 2 constructive commits verified (l4_ok=2), 37 harmful R-proposals refused, o5 replay exact; DC-4 603 consolidations (L2 fires), links asserted, o3 replay exact; DC-5 teacher_withdrawn=1, lineage unbroken, anchors hold.

**Table-killer clauses:** G0 zero RNG (in-binary scan + independent comment-stripped grep: 0 tokens in all 12 sources); zero endpoint regression (anchors hold every stage); zero ledger discontinuity (replay exact, `audit_full` never set).

**Ledger sizing (amendment A.3):** tightest projection 843,839 episodes vs 89,200-episode S100 budget — 9.5× margin. Sizing validated by the S10 measured rate.

## 4. Loop-closure L1–L5 per stage (tr counters, bar)

| Stage | L1 abst→hyp | L2 conf→eval | L3 ref→cited | L4 com→ok | L5 |
|---|---|---|---|---|---|
| DC-0 | 0/0 (O4 off) | — (O3 off) | 0/0 | — | ✓ static |
| DC-1 | 0/0 (O4 off) | 414/0 (O3 off) | 25/25 ✓ | — | ✓ |
| DC-2 | 0/0 | 603/0 (O3 off) | 36/36 ✓ | — | ✓ |
| DC-3 | 0/0 | 603/0 (O3 off) | 36/36 ✓ | 2/2 ✓ | ✓ |
| DC-4 | 0/0 | 603/603 ✓ | 36/36 ✓ | 2/2 ✓ | ✓ |
| DC-5 | 0/0 | 0/0 | 0/0 | 2/2 ✓ | ✓ |

- **L1 never fired in any stage** (0 O4 ABSTAINs in 8,920 episodes; recall always served). The seam machinery exists and the P8 bite exercises the probe synthetically, but in-run L1 is untested. Per prereg §4's letter ("a link that never fires is a composition failure"), this is a composition-coverage gap on the O4→O2 link — reported, not waived.
- L2 is assertable only where O3 is on (DC-4/DC-5): 603/603 ✓. NOTE: code activates O3 only at DC-4/DC-5 (`organs=27` for DC-3 = O1+O2+O4+O5, **no O3**) — contradicts CURRICULUM_NOTES.md ("DC-3: O1+O2+O3+O5"). Stale doc, recorded.
- L5: static scan 0 cross-organ references; zero rc=301 direct-write markers in any ledger.

## 5. Seven-control battery (prereg §5) — verdicts EXACTLY per bars

Entry gates G0–G5 all pass (g0_rng=0, g1=0, g3 sealed+stable, g2 paired rerun=0, g4=0, g5=0, l5_static=0).

| Control | Bar (prereg §5) | Measured | Verdict |
|---|---|---|---|
| C1 disabled-agency | survive within ±1 probe → agency DEAD | intact rc=0 / disabled rc=8 (DC-2 gate fail: anchors unmakable without agency); pf 0/0 | **ALIVE** — legitimate: agency is load-bearing |
| C2 disabled-composition | DC-2/DC-4 gates survive → composition DEAD | disabled run: composites=0 (gate fails) | **ALIVE** — legitimate |
| C3 scrambled-provenance | performance survives → MEMORIZATION | intact rc=0, lesioned rc=0; pf 0/0 — lesion is a behavioral no-op | **FIRED (1) — instrument vacuous, BLOCKED** (see §9a) |
| C4 scrambled-structure | survives → composition-illusion | intact rc=0, lesioned rc=0; pf 0/0 — no-op | **FIRED (1) — instrument vacuous, BLOCKED** (see §9a) |
| C5 memory-lesion | killed-traces-only above chance → LEAKAGE | r3 lesion=1000‰, r3 intact=1000‰ — alarm fires identically on intact system | **FIRED (1) — instrument vacuous, BLOCKED** (see §9a) |
| C6 null system | nonzero score → battery VOID | 0/16 criteria | **CLEAN — battery not void** |
| C7 teacher-withdrawal | authorship/lineage break or capability collapse → teacher-dependence | cap 861→258; replay exact; authorship gates hold; delta = consolidations only (see §9a) | **FIRED (1) — instrument confounded, BLOCKED** (see §9a) |

## 6. Probes P1–P10 + strength instruments

- P1–P10: **clear (0) in all six stages**, including P10 (no namespace ≥704/segment; no WARN) and P3 (max pin fraction 3‰, no 80% WARN; max consecutive no-victim PREEMPTs 0).
- **P7 limitation:** only the cross-context-gate half is instrumented (0 violations); the temporal half (CONSOLIDATE refuted ≤10 episodes with no new evidence) is disabled in code — see §9c.
- **P2 drop-ceiling tripwire / Q2 pin-fraction alarm / P1 retention-under-pressure:** implemented in `probes.zag` but **never invoked by `main.zag`'s run driver** — not armed in the official runs (glue defect, reported §9b). Post-hoc values from the analysis driver:
  - Verbatim ceiling (strength-trial prereg §5.2): `drops ≤ 2 × store_capacity`; INT-1 S10 capacity = 320 O1 slots → **640 drops/stage**. Measured drops per stage: 0 / 0 / 0 / 0 / 125 / 87 — all ≤ 640 → **tripwire would not fire; arm B survives on every stage** (whole-run total 212 ≤ 640 also passes).
  - Q2 pin-fraction: max 3‰ end-of-stage — never near the 800‰ alarm.
  - P1 retention-under-pressure: 1000‰ (perfect) on all stages.

## 7. Defended-channel telemetry (amendment C)

Self-test proves the mechanism live: bare re-COMMIT → 302 refusal (`dc_fail=1`); corroborated re-COMMIT → allowed with `LG_OP_CORROBORATE` telemetry. In-run: **with defended channel active, 0 of 0 re-COMMITs required corroboration** (all six stages: `DEFENDED_CHANNEL,0,0`). P9 never fired in-run; its bite validated both the detection path and the 302 refusal path.

## 8. Determinism

- Every stage run twice consecutively; all 6 pairs byte-identical (sha256): s0 `07021d9a…`, s1 `e9be5594…`, s2 `0bee8684…`, s3 `1ed72b34…`, s4 `f6401664…`, s5 `f31e2d9b…` (full hashes in `logs/`).
- Controls/pbite/cbite run twice; all pairs byte-identical. Zero RNG confirmed twice (in-binary G0 + independent comment-stripped grep over all 12 sources: 0 tokens).

## 9. The three adjudications

### (a) C3/C4/C5/C7: instrument-sensitivity problems, NOT legitimate kills

**C3:** the "scrambled-provenance" lesion only flips `prov` 0→1 (`O4_PROV_ANY`→`O4_PROV_NOTRUST` = exclude UNTRUSTED traces). It does **not** permute provenance metadata as prereg §5 specifies. Intact vs lesioned: gate rc 0/0, probe-fails 0/0 — **identical**. The bite (`c3_bite`) verifies only that the parameter flips, not that the control can discriminate. A control that returns DEAD on a behaviorally no-op lesion cannot discriminate memorization from provenance use — vacuous instrument.

**C4:** the "scrambled-structure" lesion flips `kind` 1→3 (`O4_KIND_SEQ`→`O4_KIND_ABSTRACT`) — a different composition kind, **not** an op-order permutation within traces as prereg §5 specifies. Intact vs lesioned: rc 0/0, pf 0/0 — identical. Same vacuity argument. The bite verifies only `kind==3`.

**C5:** `c5_lesion_rate` kills half the live O1 slots at stage half-time, then measures `composites_ok*1000/composites` **over the whole run including the pre-kill half**. But O4 composes from its **own internal trace store** (untouched by O1 kills) and serves from the never-killed anchor1 slot — the lesion never restricts O4 to killed traces, so "above-chance success" is guaranteed for any healthy system. Measured: r3_lesion = 1000‰, r3_intact = 1000‰ — **the alarm fires identically on the intact system**. The bite is synthetic arithmetic (fake rates 500/10/62) that never runs the real lesion. Additionally, the prereg's other two lesion arms (accepted-only, candidate-only) are not implemented — only mode 3 exists. The control cannot discriminate leakage from health — vacuous instrument, not a legitimate LEAKAGE attribution.

**C7:** cap4=861 vs cap5=258 (fired on `cap5<cap4`), but the decomposition is decisive: composites_ok 256→256 (**identical**), O5 commits 2→2 (**identical**), consolidations 603→0 (**the entire delta**). Mechanism: teacher withdrawal zeroes the world signal by harness design → O2 receives zero observations (639 hypotheses opened, **0 verdicts** in DC-5) → zero new CONFIRMs → zero L2 consolidation candidacies. The capability metric requires *new sensory evidence* to avoid "collapse"; under total world silence the only way to pass would be consolidating without evidence (fabrication). The actual autonomy claims all hold: authorship (teacher_withdrawn=1), lineage (replay exact), anchors, rc5=0. The control conflates **sensory starvation with autonomy loss** and cannot isolate the teacher-dependence claim; its bite validates only signal-zeroing. Confounded instrument, not a legitimate teacher-dependence kill.

Per prereg §7's calibration rule (a control that cannot discriminate is vacuous, not decisive), **C3/C4/C5/C7 are excluded as instruments; their DEAD outputs are not legitimate organ-claim kills. Verdict on those four controls: BLOCKED pending repair.**

### (b) P2 drop-ceiling tripwire: ceiling FOUND, applied verbatim

`wave8/strength-retrial/PREREG_STRENGTH_V2.md` §5.2 (ruling-5 P2): "**Drop ceiling (hard tripwire):** `drops ≤ 2 × store_capacity` (S1: 64; S10: 640; S100: 6400), else the cell is marked **FAILED**." Nothing was unresolved in the source prereg — the glue worker's "unresolved" referred to the INT-1 code, which has `CU_DROP_CEIL=0` (unset) and a `PB_DROP_CEIL_PER_SEG=64` marked PROVISIONAL (per-segment, not the prereg's per-run definition). Applied verbatim to INT-1 S10 (store capacity = 320 O1 slots → ceiling **640 drops/stage**): measured 0/0/0/0/125/87 → **no stage exceeds it; arm B survives the tripwire everywhere**. Caveat: the tripwire was **not wired into the run driver** (`p2_drop_trip` never called by `main.zag`) — a glue defect; the above is a post-hoc application, and the P2/Q2/P1-retention instruments need wiring via dated amendment before S100.

### (c) P7 temporal check: NARROWS the bar, does not void P7

`p7_check` enforces only the cross-context-gate half (b1 ≥ 2; 0 violations in-run); the temporal half (CONSOLIDATE refuted ≤10 episodes with no new evidence) is removed in code, not merely WARN-only (the comment claims WARN-only; there is no WARN path). Per prereg §10 cross-cutting rule 1, the temporal half — which cannot fire by construction — is **excluded, not passing**. Effect: P7's reported PASS covers only the gate half (bite-validated, legitimately clean); **the trial provides no evidence about the O3-outruns-O2 stale-verdict hazard**. This narrows P7's bar but does not void the gate-half result. The missing temporal instrumentation is a probe defect requiring a dated amendment.

## 10. Final verdict: **BLOCKED**

The S10 curriculum legs executed cleanly: all six stage gates pass, entry gates G0–G5 pass, C1/C2/C6 are legitimately clean (agency and composition are load-bearing; battery not void), probes P1–P10 as-instrumented are clear, loop-closure L2/L3/L4/L5 verified, determinism byte-identical, defended channel 0/0, ledger sizing validated at 9.5× margin.

But the trial cannot deliver its mandated verdicts: **four of seven controls are defective instruments** (C3/C4 vacuous lesions, C5 non-discriminating, C7 confounded) and are excluded per prereg §7 — their DEAD outputs are not legitimate organ-claim kills, so this is **not** a NEGATIVE verdict either. P7's temporal clause is uninstrumented (excluded per §10 rule 1); the P2 tripwire, Q2 alarm, and P1-retention metric were implemented but never invoked by the run driver; L1 never fired in-run (composition-coverage gap per §4).

Per the S100 advancement rule (amendment A), this S10 is not "clean" (neither POSITIVE nor legitimately killed): **S100 must not run until the battery is repaired** — C3/C4/C5/C7 instruments repaired or replaced, P7 temporal instrumentation restored, P2/Q2/P1-retention wired into the driver, and L1 exercised — via dated amendment and re-run. The system stands unconvicted; the trial's instruments failed.

## Appendix: raw logs

All raw outputs under `impl/logs/`: `s0_a/b.log` … `s5_a/b.log` (stage pairs), `controls_1/2.log`, `pbite_1/2.log`, `cbite_1/2.log`, `selftest_1.log`, `analysis_1.log` (temporary read-only evidence driver output; driver source deleted after use, no frozen files touched).
