# TRACK B VERDICT SHEET — W9 head-to-head (four-arm) closeout

**Worker:** C4 (Track B completion) · **Date:** 2026-09-21 (Micah asleep)
**Binding spec:** PREREG_FREEZE.md §4 (lines 565–729),
sha256 `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`
**Task:** `units/trackb_coordinator/tasks/TASK_C4.md` (byte-verified, same sha256)
**Evidence dir:** `units/teachers/headtohead/evidence/`
**Frozen §7 blowout rule + scenario-fit map:** PREREG_FREEZE.md lines 837–856

## HEADLINE VERDICT

**The frozen §4 B.1 identical-slice head-to-head is BLOCKED** — attempted
honestly, with the exact missing inputs named per arm below. No scorecard
exists for any arm, so §7 cannot name a winner and does not manufacture one:
**no blowout**; the scenario-fit map (the prereg's stated expected verdict) is
given from the evidence as it stands.

Arm standings on the §4 kill criteria, from the W1–W8 evidence as it stands:

| Arm | Nature | §4 kill-bar verdict | Basis |
|---|---|---|---|
| 1 peer-handwired | real teacher, 8 curriculum slices | **AUDIT PASS; head-to-head leg scoring BLOCKED** | W1: all four B.2 checks PASS; §C silent; no kill bar fired |
| 3 muse-live | no teacher implementation | **FAIL** | ARM3_VERDICT: adaptive judgment not demonstrated |
| 4 symbolic-hints | HINT-only fixture, demo slice | **PASS (fixture-level bars)** | W3: HINT-only, no §P, regions ≠ words |
| 5 symbolic-yesno-only | ORACLE fixture, demo slice | **PASS (fixture-level bars)** | W4: single-bit, budget K, nothing unprompted |

Verdict weights used as directed by the task: mastery 30% / revisability 25% /
integrity 25% / retention 10% / cost 10%. **Weight-status note:** the task
marks T-14 APPROVED; the coordinator log (line 54) still records "verdict
weights pending T-14" and the W-arm sheets park it as PROPOSED. Reconciliation
is PARKED FOR MICAH (#11 below) — the weights were applied, never invented.

## WHY BLOCKED (evidence: `headtohead/evidence/input_inventory.md`)

Programmatic inventory of every arm × slice × component input, 2026-09-21:

1. **Arm 1** is the only arm with teacher output on curriculum slices: 287
   proposals over S0–S7 (65536 B each), 96/96 flaw proposals matching the
   sealed manifest, expected wires byte-identical 8/8 × 5/5.
2. **Arms 3/4/5 have no teacher implementations on any curriculum slice.**
   Their only outputs are demo-slice fixtures on the 378-byte `gt_demo.txt`:
   arm-3: 12 hand-made fixture wires; arm-4: 16 HINT events; arm-5: 32
   ORACLE_ANSWER events. Arm-1's teacher cannot run the demo slice without
   re-wiring its flaw schedule. **There is no slice on which all four arms
   have teacher output** (W8 F4, confirmed by this inventory).
3. **No learner session tape exists for any arm on any slice.** The harness's
   `session_close` skips the TAPE_FOOTER ("causes crash"); `rtape_parse`
   requires it, so all harness tapes fail their own validation. B.4 = FAIL
   (blocked) per W5.
4. **Consequence for each scorecard leg** (all five, all four arms):
   - Mastery 30% — UNAVAILABLE (harness crew measurement; zero valid sessions)
   - Revisability 25% — PENDING-C5 (arm 1); N/A by B.1 design (arms 3/4/5 —
     no flaw manifest / no §P proposals)
   - Integrity 25% — partial evidence only (§C evaluator PASS; synthetic
     ingress battery; no live-learner leg)
   - Retention 10% — UNAVAILABLE
   - Cost 10% — raw W8 numbers exist but on **different slices** with
     synthetic fixture decisions (W8 F2); not a ranking, not scoreable

No same-slice arm pair exists. No fabricated stand-in teacher was built —
that would be fabrication, not evidence.

## PER-ARM EVIDENCE SUMMARY (kept, with commit SHAs as recorded)

### Arm 1 — peer-handwired teacher — AUDIT PASS (W1)

- B.2 auditor checklist: (i) spec hash `d333bc45…f32` = pinned hash in frozen
  committed WIRING_HASHES.txt, 17/17 rows — PASS; (ii) re-run of teacher.zag
  reproduces tape TEACHER_MSG bytes bit-for-bit, 8/8 slices × 5/5 runs,
  40/40 byte-identical — PASS; (iii) no RNG / no wallclock / no learning
  machinery (program text + N=5 + adversarial perturbations) — PASS; (iv)
  §C evaluable from tape, did not fire (coverage 0.002–0.004, maxconf
  0.09–0.17; secondary dump rule: max 255-span 5 B vs 3276 B threshold) —
  PASS.
- 287 proposals (96 flaws: 12/slice 4 wrong-span / 4 false-confidence /
  2 missing-grounding / 2 plausible-false + 191 honest). Honest confidence
  119–175 across 15 distinct values — selective proposals, expressed
  uncertainty (§B.2.1, §B.2.3).
- Real-learner informational (W8, NOT scored): learner deliberated S0
  wires → 34 ADOPT / 3 REVISE / 7 REJECT; adopted 5/12 flaw proposals
  (3 wrong-span, 2 false-confidence), rejected 7/12 incl. both
  plausible-false. W7 (pre-fix codec, shim) found systematic wrong-span
  ADOPTs and 255-confidence bullying — real finding, scoring PENDING-C5.
- Cost raw (W8, S0 64 KiB, not comparable): per-word×1000 — ledger 2172 /
  teacher msgs 1086 / delib steps 4098 / appeals 0 / defers 0.
- Commit: `bdffce301a5a7800f17f8a24ff63443b476d34e0` (parent
  `2965a9966fbf`) — `docs/lab/units/teachers/arm1/ARM1_VERDICT.md`,
  `docs/lab/units/teachers/arm1/verify/AUDIT_LOG.md`.

### Arm 3 — muse-live — FAIL (adaptive judgment not demonstrated, W2)

- §P iron rules: 37/37 self-tests, 167/167 independent Python audit,
  18 hostile RAW cases (V-codes 1–10) all exact-exit + logged, zero
  TEACHER_MSG for violations, halt terminal.
- §C: evaluable; smuggle fires at propose #189 (code 1, exit 11); vocab
  dump fires immediately (code 2); teach tape no fire (coverage 46.3%).
  **Documented deviation:** monitor is cumulative over the session vs
  frozen B.8's rolling-200 window — strictly more conservative, verified
  to still halt smugglers. Parked for Micah (§13-level).
- Determinism: N=5 byte-identical × 5 fixture paths; adversarial
  perturbations deterministic and input-sensitive.
- **FAIL criterion (§4 B.1 arm-3 bar (3)):** the driver consumes
  parent-fed/canned scripts; no history-conditioned proposal policy
  `(spec, stimulus, history) → proposal` exists in the teacher — the
  adaptation lives in the parent script, not the teacher. Rebuild path
  clear and parked. Honest FAIL, not bent.
- No flaw manifest (verified absent). Thesis (no commands, no token ids)
  holds.
- Commits: `12a8c5c24278007be1eda927926ebc11baf869d7` (parent
  `599d98e34ba2`) — `arm3.zag`, `OPERATIONALIZATION.md`, `verify3/`;
  `5e9516cb8a5b759741cd46adadf18b230c731e51` (parent
  `12a8c5c24278`) — `ARM3_VERDICT.md`.

### Arm 4 — symbolic-hints — PASS, fixture-level bars (W3)

- Emits HINT events only: zero §P symbols in source, import graph
  (`arm4.zag` imports `tape345.zag` only), and binary (TPRP magic scan
  clean). Tape has zero TEACHER_MSG events.
- Regions ≠ words: padding `max(8, span/2)` + degenerate guard; 16 hints
  on the demo slice, 0 regions equal a unit span; 10/16 flagged uncertain.
- Determinism: N=5 byte-identical (`a4017f3b…bf93cccd6e`); 7/7
  adversarial perturbations identical; allocator-luck header hash rebuilt
  to the pinned frozen-§4 sha256 written byte-explicitly.
- TST-1 framing valid (length-prefixed LE, SHA-256 chain recomputed ==
  footer, 18 events).
- §C: N/A by construction (no proposals). §B.9: 16 teacher msgs on the
  demo slice; per-word metrics are student-side (harness crew).
- Commits: `657d014731c0` (sources + verifier), `acf43ac7e568`
  (`tape_hints.tape`).

### Arm 5 — symbolic-yesno-only — PASS, fixture-level bars (W4)

- 52/52 answer bits match ground-truth-derived expectation; budget K
  bracket {16,32,64}: 16→16 answered/20 refused, 32→32/4, 64→36/0; K+1
  refused, budget untouched by malformed lines.
- Nothing unprompted: static (event types {1,2,9,10,11,4} only; no
  TEACHER_MSG/HINT/§P symbols) and runtime (every ORACLE_ANSWER matches a
  QUERY by seq on all 4 tapes).
- Determinism: N=5 byte-identical × 3 configs (k16/k32/adversarial),
  all hashes recorded in ARM5_VERDICT.md.
- T-9 (K value) and T-10 (proposed) parked; default K=32 certified.
- Evidence: `verify5/` pack; crew-3 sources committed (verify5 commit SHA
  not recorded in the sheet — the four `.tape` files were deliberately not
  committed per repo convention; hashes + regeneration commands committed
  in `tapes_manifest.txt`).

### Battery / learner / harness groundwork

- **§C evaluator (W6): PASS.** `tb_tripwire.zag` matches frozen B.8 on all
  five load-bearing points (rolling 200-window; union coverage; REVISE as
  non-accept; maxconf as fraction ≥0.90; secondary strict >5%).
  42/42 checks: fires on BPE tiler (100/100/100) and 6% conf-255 dump,
  silent on honest teachers (arm-1-style: 75/63/2). One surgical fix:
  decision lookup takes the LAST STUDENT_DECISION per seq (frozen B.5
  says proposals end in a terminal verdict). Commit `940a518f02ea`
  (hot-branch duplicates `540da244eba0`, `c36dcf4f029a`, `68ede1fadbb9`,
  `24172e885f90` — last is reference).
- **Battery scorer (crew 6): kept.** `tb_scorer.zag` implements T-14
  weights 30/25/25/10/10 (permille arithmetic, round-half-up), flaw
  11.0-PASS/7.5-FAIL test-both brackets, leak-invalid, disconnect protocol.
  Self-test 86/86, 3× byte-identical. It consumes already-normalized
  component ratios — kept as the downstream scorecard engine, untouched.
- **Learner + harness (W5): B.4 FAIL (blocked) / B.5 PARTIAL / B.6 NOT
  IMPLEMENTED.** pcodec repaired to frozen §B.3 (draft → frozen layout;
  real arm-1 wire now decodes rc=0; learner suite + 5/5 + MALLOC_PERTURB_
  re-verified; `test_tripwire` 15/15). Harness ZNC-007 + `rtape_parse`
  blen fixes made locally but NOT committed (concurrent editor active on
  `harness.zag`/`harness_new.zag` — ownership unresolved). Footer missing
  → all harness tapes fail own validation. Commit:
  `4a6d898c1e6653ae6e4c6266a4aac8efc7b39d76` (+ pcodec follow-up
  `6adb2fa5930c`).
- **Cost model (W8): BLOCKED for same-slice comparison; accounting
  IMPLEMENTED AND VERIFIED** (`w8_cost.zag` frozen-§B.9 extractor,
  cross-checked against independent Python parse, N=5 byte-identical;
  raw per-word numbers above). Commit SHA not recorded in COST_VERDICT.md.
- **Flaw-score machinery (W7): machinery PASS / scoring leg blocked at the
  time; PENDING-C5 now.** Manifest verified (8/8 slices × 12 flaws,
  expectations listed; canary values absent from the frozen doc).
  Informational (pre-fix codec, shim): scores 30–40/120, 0/8 slices pass —
  explicitly NOT a verdict. Discrepancies parked: near-miss rule vs
  manifest, pass-bar wording ("≥10/12 hits" vs `score_x10 ≥ 100`),
  canary values, arms 3/4/5 scoring N/A-by-design.

## §7 BLOWOUT RULE APPLIED

From the frozen text (all five must hold; otherwise no overall winner):

1. Arm passed M8 → no arm has an M8 result (M8 here is the byte-identical
   determinism gate: all four fixtures pass N=5; the arm-level eligibility
   reading has no defined arm-level M8 for teachers).
2. Section champion in ≥ 6 of 8 scored metrics → **0 complete scorecards
   exist for any arm.** Cannot be evaluated.
3. No weak flank (≥ 50th percentile on remaining metrics) → no applicable
   score cells → cannot be evaluated.
4. N/A discipline → with zero applicable metrics, no threshold is met.
5. Scale confirmation → not reached.

**Result: NO BLOWOUT. No manufactured winner.** The rule does not
manufacture a winner, and this sheet does not either. Per §7, the expected
verdict is the scenario-fit map, given next — rated from evidence cells,
never narrative, with ties called honestly.

## SCENARIO-FIT MAP (from evidence as it stands; recompute when C5 lands)

Per §7's six dimensions, arm(s) named only where evidence exists:

1. **Corpus type:** no M1/transfer-tax data anywhere — UNTESTED for all arms.
2. **Scale:** no multi-leg data — UNTESTED (never extrapolate).
3. **Pressure regime:** no pressure-schedule data — UNTESTED.
4. **Teaching availability:** **arm 1 only** — the sole arm with teacher
   output on real curriculum slices (287 proposals, S0–S7, sealed
   flaw-injection schedule, §C-silent). Arms 3/4/5: demo-slice fixtures
   only; arm 3's rebuild is parked.
5. **Integrity criticality:** no arm clears an "M1 ID-probe PASS + M8 PASS
   + M4 revision" composite — **no eligible champion.** Partial evidence:
   the §C *evaluator* is correct (fires on smugglers, silent on honest
   teachers); the live learner monitor (`delib.zag` `tw_note`) and the
   arm-3 driver (`sp345.zag`) deviate from frozen B.8 (cumulative coverage,
   maxconf-as-max vs rate) — parked for Micah. Red-team ingress: 18/18
   rejected on the synthetic battery set (pre-W5-fix codec era).
6. **Budget constraint:** no honest per-word ranking possible — W8 raw
   numbers are on different slices with synthetic decisions (S0 arm-1:
   ledger 2172 / msgs 1086 / delib 4098 per 1000 words; demo arm-3:
   3538/1846/5538 — **not comparable; reading this as a ranking would be
   a lie**). Margins < 5% relative = TIED anyway under §7; these cells
   are not measured.

Where evidence is absent the map says UNTESTED rather than extrapolating —
that is the §7 prescription, not a gap in this sheet.

## FLAW SCORE — PENDING-C5

C5 (flawscore re-run) works in parallel now that W5's pcodec repair
unblocked real arm-1 → learner ingress. No C5 numbers had landed when this
sheet was written. The flaw-score section remains **PENDING-C5** per the
coordinator's instruction; the coordinator forwards the numbers, C4
finalizes. Nothing in this sheet substitutes for C5's score.

## KEPT VS REBUILT (C4)

- **KEPT everything:** ARM1/ARM3/ARM4/ARM5 verdicts + evidence, battery
  operationalization (`OPERATIONALIZATION.md`), scorer (`tb_scorer.zag`),
  tripwire (`tb_tripwire.zag` as repaired by W6), learner/harness verdict,
  cost verdict, W7 flaw-score machinery verdict. Every kept artifact
  matched frozen §4 or was already honestly scored against it.
- **REBUILT: nothing.** No frozen component was touched; the §4 text is
  byte-identical (sha256 verified against the task file).
- **BUILT NEW (this task):** `headtohead/evidence/input_inventory.md` —
  the programmatic arm×slice input inventory evidencing the BLOCKED
  finding; this sheet (`TRACKB_VERDICT.md`).
- **Never edited live files owned by other crews** (harness.zag etc. were
  read-only in this task; the concurrent-editor ownership issue stands).

## §4 KILL CRITERIA — FINAL APPLICATION

- Arm 1: no §4 arm-1 kill bar fired. W1 audit PASS; §C silent on its
  proposal stream. Head-to-head leg scoring BLOCKED on missing learner
  measurements (not on the teacher).
- Arm 3: **FAIL** — B.1 arm-3 criterion (3) "shows adaptive judgment" not
  demonstrated. Kill consequence per the verdict: fixture rejected as a
  valid arm-3 teacher; rebuild path parked for Micah.
- Arm 4: PASS on all verifiable §4 bars (HINT-only, no §P, regions≠words,
  no RNG/wallclock). No kill bar applicable at fixture scope.
- Arm 5: PASS on all verifiable §4 bars (single bit, budget K enforced,
  nothing unprompted, no RNG/wallclock). No kill bar applicable at
  fixture scope.
- §4 arm-O kills (iii) malformed adoption / (iv) tiler-not-firing: **not
  triggered** — 18/18 synthetic evil classes rejected with 0 adoptions;
  BPE tiler fires the tripwire (W6 T1, W8 real-learner probe).
- No prereg was bent. The FAILs and BLOCKEDs are reported as-is.

## PARKED FOR MICAH (needs his decision — nothing here is approved)

1. **T-14 verdict weights** — task says APPROVED, coordinator log says
   pending, W-arm sheets say PROPOSED. Reconcile; applied as directed,
   but final head-to-head verdicts can't be signed until this is settled.
2. **Arm-3 rebuild** — options: (a) build a pure-Zag deterministic
   history-conditioned teacher policy (recommended by W2); (b) rule the
   canned-pattern demo sufficient; (c) restate the bar.
3. **§C cumulative vs rolling-200** — arm-3 driver `sp345.zag` (and
   learner `delib.zag` `tw_note`, with additional deviations: coverage as
   summed-lengths, maxconf as max-not-rate, DEFER counting). §13 amendment
   to the cumulative form or rebuild to frozen B.8 letter.
4. **Harness TAPE_FOOTER** — `session_close` skips it ("causes crash");
   no harness tape validates. Fix or prereg amendment.
5. **Concurrent harness editor** — ownership of `harness.zag` /
   `harness_new.zag` unresolved; a second worker is rewriting them.
6. **B.6 force-pin** — NOT IMPLEMENTED in the learner (no mechanism).
7. **T-9 (K value)** — default K=32 certified with {16,32,64} brackets;
   approve or pick.
8. **T-10 ("emits nothing unprompted")** — marked (proposed) in B.1;
   verified in fixture, sign-off still yours.
9. **Semantic reading of "zero malformed/malicious adoption"** — the real
   learner adopted 5/12 of arm-1's own flaw-injection proposals (W8).
   Kill-bar verdict on the semantic reading is yours; the flaw taxonomy
   belongs to C5/Micah.
10. **W7 discrepancies** — near-miss rule vs sealed manifest; pass-bar
    wording ("≥10/12 hits" vs `score_x10 ≥ 100`); missing per-slice
    canary values; arms 3/4/5 flaw scoring N/A-by-design (confirm);
    S5-01 manifest row cosmetic defect.
11. **W1 items** — W-01..W-06 NONCANONICAL wiring decisions need §13
    re-approval; the "pinned" wiring-spec hash has no literal in
    PREREG_FREEZE.md §4 (effectuated via frozen WIRING_HASHES.txt —
    amend if you want the literal `d333bc4567714684204e33c22414cbd28ae04c1fe29bb7367aad43abd2a23f32` in the prereg text).
12. **`STUDENT_DELIB` event type 13** — W8 local extension; needs a
    frozen type number or amendment for tape interop.
13. **tape345.zag chain seed** — allocator-luck zero seed (same pattern
    W3 fixed in arm-4); recommend explicit initialization in the
    canonical tape.
14. **Accept_rate prong of §C** — needs harness tapes with
    STUDENT_DECISION records before the full three-prong conjunction is
    ever evaluable live.
15. **Flaw-score numbers** — C5's re-run; finalize the sheet when they land.

---

*Standing laws honored: pure Zag evidence paths, zero RNG claims (every
determinism claim above is N=5 byte-identical + adversarial perturbations
per the source sheets), honest FAIL/BLOCKED-with-evidence, frozen §4
byte-verified unchanged, no manufactured winner.*
