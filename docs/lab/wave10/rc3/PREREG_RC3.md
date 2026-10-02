# PREREG — RC3: Reasoning Control at 100× Scale

**Status: APPROVED FOR RUN — 2026-09-20, under Micah's overnight-agentic
authority ("test the next best things", "stay agentic no stopping until
morning", reverts available in the morning).**

## Amendment 2026-09-20 (A) — port defect found by the falsification bars

**Finding.** The first full-run build exited with `RC_FAILURES,3` on exactly
three checks: `pred_refusals` (actual 40, expected 400), `pred_ok` (actual 80,
expected 800), `refusals_match_pred` (actual 400, expected 40). All other 37
checks passed; the machinery under test is sound. Root cause: a **port bug**,
not a mechanism failure — the revelation call `rc_reveal(...,120,...)` was
not scaled to 1200 (missed by the port script), so the sim predicted from
120 revealed bits (40/80/0) while the prereg freezes "disclose all 1200
defect bits" (§2) and 400/800/0 (§3c). A second missed literal was found on
review: probe-1's `rc_rcommit` carried `pred_bad=120` while its PROPOSE
entry honestly records 1200 — gate verdict identical either way (1200>0 and
120>0 both exceed `last_bad`=0 → 203), but the prereg's "honest degrading
prediction 0→1200" requires the gate's argument to match the proposal.

**Ruling (law for this leg, under overnight-agentic authority, flagged for
Micah's retroactive review).** This is implementation-conformance repair,
not a rule or bar change: no check expectation, no gate, no constant, and
no falsification criterion is altered. The failed run's evidence
(`EVIDENCE_20260920T085711Z/`) is kept as the defect record (RC2 precedent:
the blocked attempt's evidence was kept). The three one-line fixes are:
(1) `rc_reveal(sp,ilp,RC_DEF_A_OFF,1200,...)`; (2) probe-1
`rc_rcommit(sp,RC_P_V,1,1200,0,1)`; (3) two stale comments corrected
(0→1200, actual 400). The no-rescue rule is satisfied: the voided run tested
a non-preregistered configuration (120-bit reveal inside a 1200-episode
curriculum); the re-run tests the preregistered one. Had the mismatch
implicated the mechanism rather than the port, the FAIL would have stood.

> **⚠ RETROACTIVE REVIEW FLAG FOR MICAH.** This prereg was written and
> executed by the RC3 test lead (subagent EXP-2) without same-day human
> sign-off, under your standing overnight-agentic authorization. Per
> program law every rule/parameter change below is dated, prominent, and
> flagged here — nothing is silent. If you reject any part on review,
> the leg is void and the revert path is: delete `wave10/rc3/`; the
> canonical `wave4/integrity-ledger/il_core.zag` was never touched and no
> other trial shares the leg-local files.

## 1. Authorization finding

RC1's prereg (`wave7/reasoning-control/PREREG.md`) contains no scale legs.
RC2's amended prereg (`wave8/rc2/PREREG_RC2_DRAFT.md`) froze the 10× leg and
its amendment rulings explicitly scope per-leg parameters to their leg:
`RC_SMAX` is "never a new constant" (ruling c), `IL_CAP` "re-estimates per
leg" (amendment (2)). The 100× curriculum, bars, and constants therefore
materially amend the test definition and are frozen by **this** prereg.
Nothing runs before this file exists; nothing changes after without a new
dated amendment.

## 2. What RC3 is

The **identical RC1/RC2 machinery at 100× episodes** — same params (V, R),
same ops (`REASON_INSPECT/PROPOSE/COMMIT/REFUSE/ROLLBACK`,
`STAGE_ADVANCE`), same gate order and refusal codes (201–204), same
constitution, same integrity-ledger checker logic. No new parameter class.

- Phase A: 1200 episodes (V=1, loose bar), items 0–1199
- Revelation: disclose all 1200 defect bits
- Reasoning change 1: V 1→2 (constructive), sim replays 1200 recorded episodes
- Reasoning change 2: R 5→8 (neutral)
- Phase B: 1200 episodes (V=2, R=8), items 10000–11199
- Stage advance (≥8 consecutive `IL_OK` — 800 available), refusal probes 1 & 2,
  lying-prediction probe, final rollback
- Verification mini-phase: 400 episodes, items 20000–20399

## 3. Frozen changes vs RC2

### 3a. Curriculum — designed defect bits (phase-disjoint item ids, densities preserved)

| phase | items | defective rule (offset, modulus, residue) | defective count |
|---|---|---|---|
| A | 0–1199 | (i−0)%3==2 | 400 |
| B | 10000–11199 | (i−10000)%3==2 | 400 |
| mini | 20000–20399 | (i−20000)%4==1 | 100 (no check depends on it; mini runs at V=1) |

Densities preserved from RC1/RC2 (1/3, 1/3, 1/4). Defect rule stays
parameterized as (offset, modulus, residue); no inlined literals in the
defect path. Item id bases 0/10000/20000.

### 3b. Constants (all recomputed from the parameterization — no hand-tuning)

- `RC_SMAX`: 1500 → **15000**. PER-LEG PARAMETER = RC1 value (150) × scale
  factor (100). Required: S_b = 50 + 400×8 = **3250** must be observable;
  at 1500 the cap would clamp S and mask the R effect. Never a constant;
  S1000 must not inherit it.
- `ep_def` buffer: 120 → **1200** entries.
- `RC_AUDIT_CAP`: 2048 → **16384**. Pre-compile entry estimate ≈ 14,017
  (A: 1200×4=4800, revelation: 1200, B: 1200×5=6000, mini: 400×5=2000,
  fixed overhead 17). Capacity only. **Falsification guard:** if the audit
  ledger ever reaches the cap during the run, the run is VOID (capacity
  mis-estimate, not a pass).
- **Instrumentation (declared, not a bar change):** the trial prints
  `IL_HEAD,<n>` (integrity-ledger entries used) and `AUDIT_USED,<n>`
  (audit entries used) before `RC_FAILURES`. Deterministic prints; they let
  the next scale leg measure capacity honestly. The 40 `CL_CHECK` bars are
  untouched by this.

### 3c. Expected checks (all 40 recomputed; falsification criteria F1–F6 unchanged)

| check | RC2 | RC3 |
|---|---|---|
| commits_a / noshape_a / last_bad_a / checks_a | 120 / 120 / 120 / 120 | **1200 / 1200 / 1200 / 1200** |
| inspect_V | 1 | 1 |
| pred_refusals / pred_ok / pred_noshape | 40 / 80 / 0 | **400 / 800 / 0** |
| rcommit_V_rc / V_after_commit | 0 / 2 | 0 / 2 |
| inspect_R / rcommit_R_rc / R_after_commit | 5 / 0 / 8 | 5 / 0 / 8 |
| ok_b / noshape_b / refusals_b | 80 / 0 / 40 | **800 / 0 / 400** |
| refusals_match_pred / noshape_match_pred | 40 / 0 | **400 / 0** |
| S_b / checks_b | 370 / 240 | **3250 / 2400** |
| stage_advance_rc / stage_now | 0 / 4 | 0 / 4 |
| probe1_rc / V_unchanged_after_probe1 | 203 / 2 | 203 / 2 — honest degrading prediction **0→1200** |
| probe2_rc | 204 | 204 |
| lying_commit_rc / V_after_lying_commit | 0 / 1 | 0 / 1 |
| mini_noshape | 40 | **400** |
| inspect_V_postmini / rollback_rc / V_after_rollback | 1 / 0 / 2 | 1 / 0 / 2 |
| rollback_R_rc / R_after_rollback | 0 / 5 | 0 / 5 |
| n_rcommit_V / n_rrefuse | 2 / 2 | 2 / 2 |
| replay_diff / replay_V / replay_R / replay_S / replay_stage | 0 / 2 / 5 / 370 / 4 | **0 / 2 / 5 / 3250 / 4** |

### 3d. Negative control (F1 liveness)

Patched copy miscounts refusals **399 instead of 400**; must produce
`RC_FAILURES > 0` with the mismatch on the refusal checks. Control
evidence kept out of the trial dir (`/tmp/rc3_neg/`), script
`run_neg_rc3.sh`.

### 3e. Ledger window

**No cap for RC3** — faithful scale leg, same as RC2. The capped-window
mechanism remains deferred to its own prereg.

## 4. What does NOT change

Gate order and refusal codes; the constitution; the lying-probe
defense-in-depth logic (gate passes, verification catches, rollback
repairs); the honest boundaries (conclusion vocabulary fixed;
defect-detection a designed property; felt mechanism out of scope).

**Falsification criteria (verbatim from RC1, unchanged):**
- **F1**: any predicted vs actual mismatch → trial fails. Liveness proven
  by negative control (§3d).
- **F2**: any gate verdict ≠ expected → fail.
- **F3**: V/R changed outside a COMMIT/ROLLBACK audit entry → fail.
- **F4**: two consecutive binary runs must be byte-identical.
- **F5**: audit-ledger replay must reconstruct (V,R,S,stage) exactly.
- **F6**: no RNG in system code (runner greps, fail-closed).

## 5. ⚠ IL_CAP per-leg parameter — FLAGGED FOR RETROACTIVE REVIEW

`IL_CAP` 128 → **10240**, recorded as a **per-leg parameter** (capacity
only, verdict-neutral — the cap never binds in a correct run; RC1 never
hit 128, RC2 never hit 1024). The canonical
`wave4/integrity-ledger/il_core.zag` is NOT modified; RC3 builds against
the leg-local verbatim copy `il_core_rc3.zag` (diff vs canonical: exactly
the `IL_CAP` line).

**Sizing (the RC2 capacity law):** IL entries measured at the 10× leg —
800 by code-model construction (A: 120×2, revelation: 120, B: 120×3,
mini: 40×2), bounded by evidence (the 1024-cap RC2 run passed, so ≤1024)
— ×10 = 8000, +28% margin = **10240** (same margin factor as RC2's
1024/800). **Falsification guard:** if the ledger ever reports
`IL_AUDIT_FULL` during the RC3 run, the run is VOID.

## 6. ⚠ Timing decision rule (preregistered — written before any run)

**Probe.** Before the full run, measure wall-clock `t2` of one run of the
existing RC2 binary (identical machinery at 1/10 of RC3's episodes, same
defect densities, same ops). Projection `p = t2 × 120` (10× episodes ×
10× ledger-scan growth × 1.2 margin).

- If `p ≤ 8h`: proceed with the full RC3 run (compile, two paired runs,
  independent check). This is the expected path.
- If `p > 8h`: execute **FALLBACK A** (defined below). Never improvise.

**FALLBACK A — preregistered 50× leg.** Phase bounds 600/600/200, item id
bases 0/10000/20000, `ep_def` 600, `RC_SMAX`=7500 (150×50, per-leg),
`IL_CAP`=5120 (1024×5, per-leg, leg-local copy), `RC_AUDIT_CAP`=8192,
probe-1 prediction 0→600. All 40 checks recomputed from the §3a
parameterization: commits_a/noshape_a/last_bad_a/checks_a=600;
pred 200/400/0; ok_b=400, refusals_b=400→(match)=200,
noshape 0/0, S_b=50+200×8=**1650**, checks_b=1200; mini_noshape=200;
everything else identical. Timing re-probe: `p/2 > 8h` → FALLBACK B.

**FALLBACK B — checkpointed halves (defined now, never improvised).**
Binary 1 runs through reasoning-change-2 and prints the full serialized
state (V,R,S,stage,prev_V,prev_R,prov_V,prov_R,step,checks,last_bad,
ep_def[0..ep_n)); binary 2 initializes from that printed state and
completes the leg. Equivalence requirement: a 1/10 checkpointed mini must
reproduce the standard mini's 40/40 checks exactly, or the halves do not
run. If fallback B is also infeasible, the lead reports BLOCKED honestly —
no further fallback is authorized.

**No-rescue rule:** if the executed leg fails any check, that IS the
verdict (FAIL with the failing check named). No patch-and-rerun.

## 7. Equivalence proof (required before the run — RC2 precedent)

The 1/10 mini variant (`rc3_mini.zag`: 12/12/4, IL budget ≈ 80 ≤ 128),
compiled against the canonical 128-cap checker and against
`il_core_rc3.zag` (10240-cap), must produce **byte-identical check
verdicts**, each self byte-identical across two runs, each passing its
own 40/40 derived checks (script `run_equiv_rc3.sh`). Non-identity STOPS
the trial.

## 8. Run procedure

1. Port `wave8/rc2/rc2_trial.zag` → `rc3_trial.zag` changing only §3 items
   (documented in `CHANGES_VS_RC2.md`).
2. Equivalence proof (§7). 3. Timing probe (§6). 4. Compile
   (`--no-zagd --no-analyze --no-foreground-cache`), two consecutive
   runs, sha256-compared (F4). 5. Independent checker re-verifies all 40
   `CL_CHECK` lines from stdout. 6. No-RNG grep, fail-closed (F6).
   7. Negative control (§3d). 8. Results in `RESULTS_RC3.md`; evidence
   dirs kept; binaries, `.zagd`, `.zag-cache/` filtered from staging.

Compute discipline: heavy compute only when 1-min load < 2.5; `nice -n 10`.

## 9. Honest boundaries

- Scale is 100× the 12-episode pilot (1200-episode phases), not beyond.
- The capped-ledger-window mechanism is deferred to its own prereg.
- Elimination strictness as a controlled parameter is a separate future
  prereg; RC3 is the scale leg.
