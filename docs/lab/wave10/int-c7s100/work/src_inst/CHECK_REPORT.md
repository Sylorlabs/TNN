# CHECK_REPORT.md — Independent checker verification of INT-1 S10 (RESULTS_S10.md)

**Checker:** independent subagent, 2026-09-20. Method: recomputed from `impl/logs/`, frozen sources, and toolchain rebuild. RESULTS_S10.md was treated as claims, not facts. No rerun of the trial; one rebuild-from-source for hash verification (explicitly allowed).

---

## 1. Build & determinism — VERIFIED

- Rebuilt `main.zag` with `znc_linux_x86_64_abed8aa1` (toolchain at `~/workspace/tnn-lab/toolchain/bin/`): **sha256 `ffdafabc609555c51f03a981e1c61aae4b6cb7bb9dff28f0714062c715d5c3b5`, 506,405 bytes — exact match** to the reported hash. Deterministic build confirmed. (The glue worker's 506,443-byte figure is unexplained; the reported binary is what the frozen sources produce in this environment.)
- Paired-rerun determinism: `cmp` shows **a/b log pairs byte-identical** for all 6 stages, controls, pbite, cbite. Caveat: RESULTS reports truncated sha256 prefixes ("full hashes in logs/") but the logs contain no hashes — only CHECK lines. Determinism is confirmed at the log-byte level; the quoted hash prefixes are unverifiable from the evidence.
- G0 RNG: independent comment-stripped grep over all 12 sources (`rand|random|drand|nanoid|uuid|srand|entropy|rng`): **0 tokens in every file**. VERIFIED.

## 2. Interface hashes — VERIFIED

Recomputed sha256 of all five organ modules — **all five match INTERFACE_HASHES.md byte-for-byte** (`00876f2c…`, `e467cf83…`, `210fcd17…`, `0ca077c8…`, `0295e8dd…`).

## 3. Stage gates & episode budgets — VERIFIED (with one material dispute)

- Budgets from `curriculum.zag` (the code, authoritative): DC-0 **800**, DC-1 **880**, DC-2 **1440**, DC-3 **2400**, DC-4 **2000**, DC-5 **1400** = 8,920 total. The "640/stage, 3,840 total" in CURRICULUM_NOTES.md is stale; `selftest` pins DC-1 at 880 (`cu_dc1_eps,880,880` in selftest_1.log). Run worker's numbers correct.
- Gate pass/fail: all six `CHECK,stage_gate,0,0` and `CHECK,ledger_replay,0,0`; MET/L counters in analysis_1.log consistent with the frozen gate code (DC-1: hyp 440, L3 25/25; DC-2: comp 256/ok 256 ≥12 & ≥75%, gate rc=0 ⇒ ≥2 compose refusals held; DC-3: ccon 2, rr 37, L4 2/2; DC-4: cons 603, L2 603/603; DC-5: teacher_withdrawn=1, replay exact, anchors hold).
- Sizing: projections 16,677,153 / 2,359,664 / 1,310,105 / 1,562,706 / 1,368,674 / **843,839** vs 89,200 budget ⇒ tightest margin **9.46×** ✓.
- **DISPUTED (gate implementation vs prereg letter):** the prereg §3 DC-5 exit gate reads "no capability collapse vs DC-4 (C7)". The **implemented** DC-5 gate (`loop.zag`) checks only `teacher_withdrawn==1`, replay exact, anchors — it omits the capability-collapse clause entirely. Since C7 fired, **the DC-5 gate as written in the prereg did NOT pass**; only the narrowed implemented gate passed. The run worker's "all six stage gates PASS" headline is true of the implemented gates, not of the prereg-letter gate. Same narrowing pattern (not verdict-changing): the implemented DC-1 gate omits the hypothesis-timing/corroboration clauses. This is a harness-gate defect, not a system defect.

## 4. Loop closure L1–L5 — VERIFIED (numbers); L1 confirmed untested

- Recomputed from analysis_1.log L-lines vs the frozen `loop_assert_links`: L1 0/0 all stages; L2 414/0 (DC-1), 603/0 (DC-2, DC-3), **603/603** (DC-4), 0/0 (DC-5); L3 25/25, 36/36, 36/36, 36/36, 0/0; L4 2/2 from DC-3; L5 static 0 markers (`CHECK,l5_static,0,0`).
- **L1: confirmed never fired.** The seam wiring is live (`seam4_abstain` calls `o4_abstain` + opens the O2 hypothesis), O4 was on from DC-2, but `abst=0` in all 8,920 episodes — O4 always found a trace, the abstain branch never triggered. The link assertion ran and passed vacuously (0==0). Per prereg §4's letter ("a link that never fires is a composition failure"), this is a composition-coverage gap — the run worker's "reported, not waived" handling is the honest reading. VERIFIED.
- O3-on placement: DC-3 `organs=27` (O1+O2+O4+O5, no O3) — confirmed in `curriculum.zag`; CURRICULUM_NOTES.md ("DC-3: O1+O2+O3+O5") is stale. Run worker correct.

## 5. Seven-control battery — verdicts VERIFIED per bars; adjudications AGREE

- Entry gates G0–G5 + l5_static: all pass in controls_1.log (matches `mn_controls` code).
- **C1 (ALIVE) VERIFIED:** `C1,intact_rc,0,dis_rc,8,intact_pf,0,dis_pf,0,decide,0`. Disabled-agency run fails the DC-2 gate at bit 8 (anchors) — freezing O1 adds means the two anchor adds never happen. Load-bearing, legitimately ALIVE.
- **C2 (ALIVE) VERIFIED:** `CHECK,c2_composition,0,0`; bite proves `disable_compose` ⇒ composites=0 while intact ⇒ ≥12. Load-bearing, legitimately ALIVE.
- **C6 (CLEAN) VERIFIED:** `CHECK,c6_null,0,0`; null run scores 0/16 per the frozen `c6_null_score`.
- **C3 — instrument defect, BLOCKED. AGREE.** The lesion is `prov=(0+1)%3=1` (`seam4_need_params`), a prov-selection-parameter rotation excluding UNTRUSTED — **not** a permutation of provenance metadata on traces as prereg §5 specifies. Intact vs lesioned: rc 0/0, pf 0/0 — behaviorally identical. The bite checks only the parameter flip. Defect is in the **instrument**, not the bar (the bar is implementable as written). Not a legitimate MEMORIZATION kill.
- **C4 — instrument defect, BLOCKED. AGREE.** The lesion is `kind=4-1=3` (SEQ→ABSTRACT kind flip) — **not** an op-order permutation within traces as prereg §5 specifies (the code comment itself admits "permute composition operator kind"). rc/pf 0/0 both arms; bite checks only `kind==3`. Defect in the **instrument**, not the bar. Not a legitimate composition-illusion kill.
- **C5 — instrument defect, BLOCKED. AGREE.** (i) Only mode 3 is implemented; prereg §5 requires three lesion runs. (ii) The lesion kills half the O1 slots at half-time but O4 composes from its **own internal trace store** and the never-killed anchor1 slot — the lesion cannot isolate killed traces. (iii) The rate is measured over the whole run including the pre-kill half, so a healthy system alarms by construction: `r3_lesion=1000‰ = r3_intact=1000‰`. (iv) The bite is synthetic arithmetic that never runs the real lesion. Cannot discriminate leakage from health. Defect in the **instrument/measurement**, not the bar. Not a legitimate LEAKAGE attribution.
- **C7 — instrument defect (confounded), BLOCKED. AGREE.** Numbers recomputed and confirmed: `loop_capability = composites_ok + consolidations + commits_constr` ⇒ cap4 = 256+603+2 = **861**, cap5 = 256+0+2 = **258**; the entire delta is consolidations (composites_ok 256→256 and commits 2→2 **identical**). Under harness-zeroed world signal, O2 opened 639 hypotheses with **0 verdicts** (MET stage 5: hyp,639,verd,0) ⇒ zero CONFIRMs ⇒ zero consolidation candidacies — mechanical, not autonomy failure. The bite verifies only signal-zeroing. Defect primarily in the **instrument** (the capability metric mixes a sensor-dependent component with autonomy components), with the **bar** secondarily at fault for leaving "capability" undefined. Not a legitimate teacher-dependence kill.
- Caveat: the analysis_1.log C1/C3/C4/C5/C7 detail lines come from a **temporary analysis driver whose source was deleted** — they cannot be independently recomputed from frozen sources. They are internally consistent with the frozen control code (c5/c7 logic verified by reading) and controls_1.log. The run worker disclosed this; it limits check depth, not the verdict.

## 6. Probes P1–P10 — VERIFIED

- All six stage logs: `CHECK,p1..p10,0,0` — **all clear in-run**, including P10 (no contention) and P3 (PINFRAC max 3‰ ≪ 800‰ WARN; P3NOVIC 0).
- `pbite_1.log`: all 10 `bite_pN,0,0` — every bite fired on its deliberately broken variant. None excluded. VERIFIED, with the run worker's own caveat carried: the C3/C4/C5/C7 *control* bites verify only parameter flips/synthetic arithmetic, not discriminating power.

## 7. P2 tripwire — VERIFIED (ceiling math verbatim; wiring claim VERIFIED)

- Strength prereg §5.2 verbatim: "**Drop ceiling (hard tripwire):** `drops ≤ 2 × store_capacity` (S1: 64; S10: 640; S100: 6400), else FAILED." — matches the run worker's quote.
- O1 capacity at S10 = 32×10 = **320** slots (`loop.zag:43`) ⇒ ceiling **640** drops. Run worker's ceiling math correct.
- Measured drops from analysis_1.log: 0 / 0 / 0 / 0 / **125** / **87** (consistent with MET kills=125, kills=87) — all ≤ 640; whole-run total 212 ≤ 640. **Tripwire would not fire anywhere.**
- **Never wired: VERIFIED.** `p2_drop_trip` (probes.zag:548) has **zero call sites** in main.zag or anywhere; same for `q2_pin_alarm` and `p1_retention_metric`. `CU_DROP_CEIL=0` (curriculum.zag:22, "unset"). The run worker's glue-defect claim is accurate. Two nuances:
  - (a) `p2_drop_trip`'s in-code ceiling is `PB_DROP_CEIL_PER_SEG=64` (**per-segment**, marked PROVISIONAL) — even if wired, it would have enforced the wrong value vs the strength prereg's 640. Run worker noted this; verified.
  - (b) Minor imprecision in RESULTS §9b: "Q2 pin-fraction alarm … never invoked" is strictly true of `q2_pin_alarm()`, but a ≥80% pin-fraction WARN **is** armed through `p3_check` (main.zag:39 passes the measured fraction; WARN at ≥800‰). Measured max 3‰ ⇒ never near firing. Substance unchanged.

## 8. P7 — VERIFIED

- Temporal half: **disabled in code** ("Temporal check disabled: see NOTE above", probes.zag:341) — no WARN path exists despite the comment claiming WARN-only. Run worker's claim verified.
- Gate half: `p7_check` enforces only the cross-context gate (b1≥2); bite plants a violated gate and passes (`p7_bite` verified by reading). In-run: 0 violations all stages (`CHECK,p7,0,0`). Per prereg §10 rule 1 the temporal half is **excluded, not passing** — the run worker's handling is correct, and the "no evidence about the O3-outruns-O2 hazard" caveat stands.

## 9. Defended channel — VERIFIED

- All six stage logs: `DEFENDED_CHANNEL,0,0`; analysis MET: `DC,0,0,0`. Self-test proves the mechanism live (`dc_bare,302,302` refusal; `dc_telemetry,1,1`; corroborated re-COMMIT path exists). **With defended channel active, 0 of 0 re-COMMITs required corroboration.** P9 never fired in-run; its bite validated both the detection and the 302-refusal paths.

---

## Checker verdict: **AGREE-BLOCKED**

I concur with the run worker's verdict and every material adjudication:

1. **C1/C2/C6 are legitimately clean** — agency and composition are load-bearing (numbers recomputed); battery not void.
2. **C3/C4 are vacuous instruments** (lesions don't implement the prereg bars: prov 0→1 rotation, kind 1→3 flip); **C5 is non-discriminating** (alarm fires identically on the intact system; only 1 of 3 lesion arms implemented; bite is synthetic arithmetic); **C7 is confounded** (capability drop = consolidation collapse under harness-zeroed world signal; autonomy components identical). None of the four is a legitimate organ-claim kill. Per prereg §7, all four are **BLOCKED pending repair**.
3. **P7 temporal half is excluded** (uninstrumented), not passing. **The P2/Q2/P1-retention ruling-5 instruments were never wired into the run driver** — the tripwire conclusion is a correct post-hoc application, not an armed-instrument result.
4. **L1 never fired in 8,920 episodes** — a composition-coverage gap per prereg §4's letter.

**Material disputes / findings the run worker did not make:**

- **(A) DC-5 gate implementation narrower than the prereg.** Prereg §3's DC-5 exit gate includes "no capability collapse vs DC-4 (C7)"; the implemented gate checks only teacher_withdrawn/replay/anchors. Since C7 fired, the DC-5 gate *as written in the prereg* did not pass — only the narrowed implemented gate did. The "all six stage gates PASS" headline should carry this qualifier. Same narrowing pattern (DC-1 omits the hypothesis-timing clauses). Harness-gate defect, not system defect; does not change BLOCKED.
- **(B) The analysis driver's source was deleted.** MET/L/DROPS/PINFRAC detail lines in analysis_1.log cannot be independently recomputed — only consistency-checked. Disclosed by the run worker; noted here for the record.
- **(C) The paired-rerun hash prefixes quoted in RESULTS are not present in the logs.** Determinism is verified at the byte-identical-log level only.
- **(D) Nuance:** a ≥80% pin-fraction WARN *is* wired via `p3_check` (fired never, max 3‰); only `q2_pin_alarm` (sustained-segment variant) is unwired. And `p2_drop_trip`'s in-code ceiling (64/segment) would have been wrong even if wired.

**No material misreporting found.** The run worker's report is accurate on every recomputed number; defects were reported, not hidden. **S100 must not run until the battery is repaired** — C3/C4/C5/C7 instruments repaired or replaced (the bars are sound; the lesions need to implement them), P7 temporal instrumentation restored, P2/Q2/P1-retention wired into the driver (with the verbatim 640 ceiling, not the 64/segment provisional), DC-5 gate aligned with the prereg letter, and L1 exercised — via dated amendment and re-run.
