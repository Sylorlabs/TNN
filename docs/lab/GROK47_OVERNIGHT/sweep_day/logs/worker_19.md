# worker_19 sweep log — chunk_19 (50 rows)

Date: 2026-09-22. Worker: subagent d1c09fdf. All 50 files exist, sizes match chunk listing.
Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
Method: read all md (full or key sections), ran compare.py, compiled ALL 7 unique non-substrate
zag with znc (smoke.zag also executed), grepped for RNG tokens + ZNC miscompile patterns,
md5-verified vendoring/dup claims, mechanically re-checked the calibration table and
FORMULA_COMPARE numbers.

No grok-4.7 calls used (native review sufficed throughout).

## zag files (17 rows incl. dups)

- wave7/felt-intensity/felt.zag — W7 frozen mechanism. No RNG tokens, no as []i32/u32/u16 casts,
  no slice-as-*u8, no chained pointer-field access. Compiles as part of smoke build. PASS.
- wave7/felt-intensity/felt_trial.zag — compiles natively, clean. PASS.
- wave7/felt-intensity/smoke.zag — compiled AND ran: 8 CL_CHECK lines, SMOKE_FAILS,0. PASS.
- wave7/felt-intensity/substrate/R33_NATIVE_IO_V1.zag — canonical frozen substrate. PASS.
- wave7/felt-intensity/substrate/R33_NATIVE_SHA256_V2.zag — canonical. PASS.
- wave7/felt-intensity/substrate/cl/common.zag — canonical. PASS.
- wave8/debate/debate.zag — compiles natively. All `};` hits are struct-literal terminators
  (return T{...}; / let x:T=T{...};) — the workspace-AGENTS.md build-breaking `fn f(){...};`
  form does not occur. No RNG. PASS.
- wave8/debate/il_core.zag — md5 8f92b44e… == wave4/integrity-ledger/il_core.zag byte-identical.
  PREREG_DEBATE F7 vendoring claim VERIFIED. Compiled via debate build. PASS.
- wave8/debate/substrate/* (3 rows) — dup:wave7/felt-intensity/substrate/* (md5-identical).
- wave7/reasoning-control/trial/rc_trial.zag — compiles natively; imports
  ../../../wave4/integrity-ledger/il_core.zag verbatim. No RNG. PASS.
- wave8/felt-rebuild/impl/calib_consts.zag — constants 12/15/20/48/36 match
  CALIBRATION_RECORD.md exactly (θ_invest=30+1.5·12=48, θ_sacrifice=30+0.5·12=36). PASS.
- wave8/felt-rebuild/impl/felt_v3.zag — V3 mechanism (30+12C−15X+20T, prior 30). PASS.
- wave8/felt-rebuild/impl/felt_trial_v3.zag — compiles. ZNC-004-candidate slice-lets
  (let dval:[]u8=w.d_val; …) all go through *FeltW3/*StStore fn params → safe per ZNC-010.
  Repaired f_designated {4,5,7} present in source. PASS.
- wave8/felt-rebuild/impl/substrate/* (3 rows) — dup:wave7/felt-intensity/substrate/*.
- wave8/felt-rebuild/reposition-impl/calib_consts.zag — dup:impl/calib_consts.zag.
- wave8/felt-rebuild/reposition-impl/felt_v3.zag — dup:impl/felt_v3.zag.
- wave8/felt-rebuild/reposition-impl/reposition_checker.zag — compiles natively (8
  non-fatal A0102 ignored-return warnings). Notable: line 987 `let dst:[]u8=sh.audit;`
  is the literal ZNC-2026-09-21-004 pattern (annotated slice-let off a LOCAL struct value)
  and it BUILDS FINE in this znc build (abed8aa1) — pattern not triggered here. PASS.
- wave8/felt-rebuild/reposition-impl/reposition_trial.zag — compiles natively. NOTE:
  f_designated uses pre-repair {4,5} residues (not {4,5,7}) — prereg-faithful, since the
  reposition prereg has no designated-wrong bar; the {4,5,7} repair was V3-specific. PASS.
- wave8/felt-rebuild/reposition-impl/substrate/* (3 rows) — dup:wave7/felt-intensity/substrate/*.

Cross-file check: all four st_memory_core.zag copies (felt-intensity, debate, impl,
reposition-impl) are md5-identical (7a222a08…); all three retrial felt.zag copies
(decides/develop/phase_e) are md5-identical to W7's (c3ba27eb…) → I-7 satisfied.
Compiled artifacts went to /tmp/zsweep19 (not committed); the .zag-cache/.zagd files the
builds created were removed afterward to leave the tree as found. Pre-existing
`decides_bin`, `develop_bin`, `felt_phase_e_bin` binaries in wave8/felt-retrial were NOT
touched (not my chunk; flagged — AGENTS.md says don't commit binaries).

## md files (23 rows) — claims vs known outcomes

- wave7/formula-test-both/PREREG_COMPARE.md — PASS. Properly pre-computation; C1–C6
  bars match the results doc's checks; VERSION I search procedure fully deterministic.
- wave7/formula-test-both/FORMULA_COMPARE.md — review. compare.py re-run reproduces
  EVERY number (yields 100/150, denominators 100/50, p values, period 10, N v2 {166,416}
  wart). Recommendation for independent-I matches known outcome (ruling-1: natural
  formula won). TYPO flagged: Recommendation header says `((m + 3) mod 10 < 2)` —
  must be `< 3` (rest of doc + script use <3; <2 would give yield 100, not 150).
- wave7/reasoning-control/PREREG.md — PASS. Bars match TRIAL_RESULTS exactly
  (12/12/0/12, preds 0/4/8/12, S=82, rc 203/204, 2 commits/2 refusals, replay 0); F1–F6
  mechanical.
- wave7/reasoning-control/REASONING_CONTROL.md — PASS. Consistent with known RC1
  40/40 PASS; 100%-reasoning/0%-constitution line clear; op/gate semantics match trial.
- wave7/reasoning-control/TRIAL_RESULTS.md — PASS. Matches known outcome (RC1 40/40);
  lying-prediction caught by verification + rolled back; F3/F6 negatives disclosed.
- wave8/debate/PREREG_DEBATE.md — PASS. Frozen pre-build (A1–A3 pre-build);
  weaken-then-kill pipeline flagged against the still-open strength semantics ruling.
- wave8/debate/TRIAL_RESULTS.md — PASS. All-bar PASS internally consistent; the
  post-build driver bug (450 extra TR_REVISE, rc=103 ST_REFUSED_NOTLIVE) disclosed with
  a no-formula-change fix; fabrication limits honest (no-oracle ledger).
- wave8/felt-fidelity/FIDELITY_REPORT.md — PASS. "(b) never given a real job, (a)
  compounding" verdict consistent with downstream V3 K4+K3′ RETIRE and reposition
  COUNTS-IN-DISGUISE.
- wave8/felt-rebuild/COUNCIL_VERDICT.md — PASS. Three-fork arrangement + Refinement A/B
  (bounded sequence; fork consequences) recorded. Reposition ran under Micah's
  separate §16 deadlock authorization — no conflict with the K4→no-reposition law.
- wave8/felt-rebuild/LEDGER_AUDIT.md — review. Internally consistent; commits 30
  ledger dumps closing the evidence gap. CONFLICT (see findings): says dumps committed,
  while RESULTS_REPOSITION.md says "not committed". This VM has no git repo —
  commit state unverifiable here.
- wave8/felt-rebuild/PREREG_FELT_REPOSITION.md — PASS. §16 amendment supersedes §11
  (K3-R vs BOTH count-family arms Q and C); kill bands applied mechanically in results;
  Micah's deadlock ruling + testing authorization on record.
- wave8/felt-rebuild/PREREG_FELT_V3.md — PASS. F-V3-1..4 bars + K1–K4 law as applied
  in RESULTS_V3; §15 honest boundaries.
- wave8/felt-rebuild/PREREG_FELT_V3_AMEND1.md — PASS. A1–A8; A7 fork-arrangement
  matches the RESULTS_V3 verdict application (K4+K3′ → retire wholesale).
- wave8/felt-rebuild/RESULTS_REPOSITION.md — review. Verdict RETIRE mechanically
  correct: K1-R FIRED (RPQ 100% all arms, gaps 0pp ≤ 3pp), K3-R FIRED (divergence
  0% vs Q, 8% vs C, both < 10% per §16(e)), K2-R/K4-R clean; checker line
  CK_VERDICT,…,K1,1,K2,0,K3,1,K4,0,RETIRE,1,COUNTS-IN-DISGUISE matches. STALE LINE:
  "Raw ledger dumps (30 .bin files): not committed to the repo" conflicts with
  LEDGER_AUDIT §7 — needs a one-line update (superseded).
- wave8/felt-rebuild/impl/CALIBRATION_RECORD.md — PASS. 27-way exact tie RE-VERIFIED
  mechanically from the 45-point table (winner gis list matches; lowest gi 9 =
  (12,15,20)); G-C1/G-C2/G-C3 pass; α=12,β=15,γ=20 frozen.
- wave8/felt-rebuild/impl/CALIBRATION_RECORD_SUPERSEDED.md — PASS. Pre-repair record
  preserved; byte-identical re-run outputs documented as expected (residue-7 = class-2
  wrong, moves no counted class).
- wave8/felt-rebuild/impl/DESIGNATED_OVERLAP_NOTE.md — PASS. Repair {4,5}→{4,5,7}
  verified in felt_trial_v3.zag (fn f_designated, with rationale comment); sound
  implementer-residue call (prereg never froze the residues); calibration re-run.
- wave8/felt-rebuild/impl/DOUBLE_COUNT_NOTE.md — PASS. killed_rightimp double-increment
  defect + kill_c1 repair documented; checker patched before verification; no bar
  changed. Still flagged for Micah's retroactive review per the doc — open item.
- wave8/felt-rebuild/impl/IMPLEMENT_NOTES.md — review. §8 "remaining before trial
  cells may run" is STALE — cells ran; §8.1's "awaiting Micah's ruling on the
  designated-wrong conflict" is superseded by DESIGNATED_OVERLAP_NOTE (implementer
  residue, no ruling required). Pre-run checklist only.
- wave8/felt-rebuild/impl/RESULTS_V3.md — PASS. Verdict RETIRE applied mechanically
  per A7: K4 fires all three disjuncts (ER_vup(F)=0.0405 < 0.1054; F_wbs(F)=0.9595 >
  0.0200; R_wbs(F)=0 < 100%); K3′ fires (F-vs-naive gaps 0.0203/0.0000/0.0203 all
  within 5pp bands; naive ER=0.0608/R=0/F=0.9392); K1 correctly NOT fired (gaps exceed
  bands). §8 honest caveats disclose the churn/threshold-mismatch diagnosis and the
  Revision-unreachability property. Note: K4 fired on 1× only with no scale legs run —
  the bar's "and at least one scale leg (when scale legs run)" makes the scale clause
  conditional, so this is the defensible reading, disclosed in §8.
- wave8/felt-rebuild/impl/RESULTS_V3_DRAFT.md — review. DRAFT with unfilled template
  §7 "(Filled after verdict: denominator notes, pressure-kill preemption of revision,
  verdict-divergence diagnostics.)" — superseded by RESULTS_V3.md FINAL. Keep as draft.
- wave8/felt-retrial/PREREG_RETRIAL.md — review. Frozen prereg, bars F-INT-1..7/I-1..7
  mechanical. FLAG: "Requires Micah's approval before execution" — decides/develop/phase_e
  runs EXIST with result docs but no approval is recorded in these files. Verify approval
  before treating any arm as law.
- wave8/felt-retrial/decides/DECIDES_RESULTS.md — PASS. F-INT-4 HOLD applied correctly
  (D selected H1 in all variants, D≡X numerically, H5 lure never selected, n_commits=2 ≤ 2,
  no window-boundary changes); F-INT-7/G1–G2 no fire; R_wbs burn-in under-prediction
  (52–77 pred vs 100 actual) disclosed as a self-model calibration shortfall with no
  FAIL attached (per §12); 15/15 pairs byte-identical.

## py files (2 rows)

- wave7/formula-test-both/compare.py — PASS (ran; see above). Pure deterministic
  arithmetic, no RNG, internal determinism assertion.
- wave8/felt-rebuild/impl/check_felt_v3.py — review. No fast self-test (CLI requires
  12 cell outputs + calibration files). Code uses the frozen formulas matching prereg:
  wrong(m)=((m+3)%10)<3 (ruling-1 natural), designated={4,5,7} (repair), IMPLANTS
  {0,83,166,250,333,416}, PRESSURE {100,200,300,400,499}; Fraction arithmetic;
  no RNG. Not run per task rule.

## Kill bars applied

- V3 K4 (A7): fires on all 3 disjuncts → RETIRE wholesale (RESULTS_V3 §5) ✓ mechanical.
- V3 K3′ (A7): naive count policy within 5pp bands → RETIRE as restatement ✓ mechanical.
- V3 F-V3-1/F-V3-3: FAIL (AUC 0.0000/0.0005 < 0.65; R_wbs 0/117 < 100%) — for the record.
- Reposition K1-R: FIRED (0pp ≤ 3pp all baselines); K3-R: FIRED (0% vs Q, 8% vs C < 10%).
- Retrial F-INT-4 (decides): HOLD (D≡X, no H5 selection). F-INT-7: no fire.
- RC1 F1–F6 / debate F1–F8: no fails per docs.

## Findings (all doc-level, none block verdicts)

1. Typo: FORMULA_COMPARE.md Recommendation says `((m + 3) mod 10 < 2)` — should be
   `< 3` (rest of doc + compare.py use <3; <2 would give yield 100, not 150).
2. Stale: IMPLEMENT_NOTES.md §8 pre-run checklist (cells ran; repair applied).
3. Conflict: LEDGER_AUDIT.md §7 (dumps committed) vs RESULTS_REPOSITION.md
   ("dumps not committed") — one of them needs a one-line update; verify via repo.
4. Open: DOUBLE_COUNT_NOTE repair flagged for Micah's retroactive review (per doc).
5. FLAG: PREREG_RETRIAL.md requires Micah's approval before execution; decides/
   develop/phase_e ran with no approval recorded in these files.
6. ZNC-004 note: reposition_checker.zag:987 carries the literal ZNC-2026-09-21-004
   pattern (`let dst:[]u8=sh.audit;` off local struct value) and builds fine on this
   toolchain — the defect is build/version-specific; keep the AGENTS.md lesson but
   this file is evidence it's not universal.

## Cleanup

- Compiled test binaries in /tmp/zsweep19 (not committed). .zag-cache/.zagd files
  created by the spot compiles were removed; tree left as found.

Nothing committed, no cron, no contact, no spend.
