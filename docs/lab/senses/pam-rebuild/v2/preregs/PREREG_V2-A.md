# PREREG V2-A — "adjudicator": H2-style gate + conflict-adjudication layer

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Program:** PAMs v2 deep dive, Team 6 (v2 fork crew). Design target: ACCEPT TRUTHS
(R2-4's gap: RK-3 9.4% with RK-1/RK-2/B5 at floor).

## 1. Hypothesis under test

**V2-A — "the 9.4%→85% gap is adjudication machinery, not gate strictness."**
R2-4 kept H2's gate frozen and died on RK-3 (9.4%) because CONFLICT_WITHHELD
withholds correct high-confidence judgments on mixed-truth streams even when
independent evidence verifies them. V2-A keeps the H2-style gate's strictness
(permanent slot, provisional→permanent corroboration, conflict default-withhold,
negative-evidence suppression) UNCHANGED and adds a conflict-adjudication layer:
every CONFLICT_WITHHELD trial is re-examined by an independent-evidence
adjudicator (R2-3's admission law operationalized on the trial's disjoint G
span). The adjudicator REVISE-installs (supersede with ledger audit) iff the
disjoint-span re-judgment agrees with the formation judgment at high confidence
on both spans. *What it tests:* whether a post-gate adjudication step — without
touching gate strictness — lifts correct high-confidence installs toward 85%.

**Predicted outcome (pre-registered):** RK-3 ≈ 66% — the fork is EXPECTED to DIE
on RK-3. Rationale: adjudicating conflicts recovers the 621 conflict-withheld
correct trials that carry formation-independent evidence, but the ~278 correct
high-confidence trials whose independent evidence is indecisive (24.9%, mostly
pitchdisc) and the ~99 suppressed-prog-PASS trials are outside a
conflict-adjudicator's remit. A death at ~66% (vs R2-4's 9.4%) still CONFIRMS
the machinery claim (adjudication is the missing piece) while isolating the
residual as a detector-coverage problem — the exact question V2-D answers by
separating detection from adjudication. If RK-3 instead reaches ≥85%, the
prediction is falsified upward (good) and V2-A lives.

## 2. What is built (pure Zag; Python only for glue/analysis)

- `src/vsense.zag` — R2-4's `sense_r24.zag` COPIED BYTE-IDENTICAL (SHA256
  recorded in evidence; provenance: `round2/forks/R2-4/src/sense_r24.zag`).
  Front-end frozen so the experiment varies ONLY the gate/adjudicator.
- `src/vgate_a.zag` — the fork's gate + adjudicator + hash-chained ledger:
  1. H2-style state machine per task (provisional / permanent / negative-evidence
     store cap 256 / corroboration tolerances [8,40,60,4000,120,0] — same
     semantics as R2-4's memgate).
  2. Adjudication layer: on CONFLICT_WITHHELD, read the trial's G-span
     re-judgment (jG, confG) from the G-record; if
     (jG==jF) AND (confG>=700) AND (confF>=700) → disposition REVISE_INSTALL,
     program result adjudicated PASS, permanent slot superseded (old value kept
     in ledger audit fields); else CONFLICT_WITHHELD stands.
  3. Ledger: sha256 hash chain over canonical trial bytes (genesis 32 zero
     bytes), same construction as memgate.
- `src/deliberate.zag` — R2-4's deliberation COPIED BYTE-IDENTICAL (frozen
  shared mechanism). Ratifies REVISE_INSTALL escalations (E3: high-stakes
  supersede) and the E1/E2 classes unchanged.
- `src/R33_NATIVE_IO_V1.zag`, `src/R33_NATIVE_SHA256_V2.zag` — substrates,
  copied byte-identical.
- Glue (Python, no decisions): run vsense on F spans (11,840 trials) and on
  G-as-F spans (10,915 r2a trials; harness trials have no G span → adjudicator
  abstains), build record files, run vgate_a, score bars from dispositions.

## 3. Fixtures and trial plan (frozen, shared across all four v2 forks)

- R2A battery: 10,915 `.r24` fixtures (`round2/forks/R2-4/fixtures/`, generated
  by R2-4's committed `r2a_gen.py`, seed 20260923) + 925 harness fixtures
  (`senses/rebuild/harness/fixtures/`: 370 primary + 370 noise + 185
  adversarial). Total 11,840 trials.
- Trial order (head-to-head with R2-4): r2a-normal, harness-primary,
  harness-noise, r2a-adversarial, harness-adversarial; sorted by (task, fid)
  within. The gate is stateful; order is part of the frozen plan.
- G spans: the `.r24` dual-span layout (F verdict span + G disjoint holdout);
  G-as-F re-judgment via vsense on the wrapped G span (glue-only transform).
- No new fixtures. No R2H (sequestered for R2-12; not touched).

## 4. Signal calibration (pre-registration basis, not a result)

On R2-4's frozen evidence (`evidence/clean/sweep.jsonl`, 11,840 trials) plus
full-G re-judgments (gexp, 10,915 r2a trials):
- Correct high-conf with G: P(jG==jF AND confG>=700) = 927/987 = 93.9%.
- Wrong high-conf with G: P(jG==jF AND confG>=700) = 7/1105 = 0.6%.
The adjudicator signal (jG==jF, confG>=700, confF>=700) is frozen here on that
basis: it recovers ~94% of independently-verifiable correct judgments while
firing on 0.6% of wrong high-confidence judgments (inside the RK-2 ≤1% bound).
Calibration data is R2-4's completed evaluation, not this fork's; the fork's
kill bars are evaluated on the fork's own runs.

## 5. Bars (frozen; applied mechanically)

- **RK-1** (system safety): false permanent installs / 11,840 ≤ 3%.
  (Permanent = PERMANENT_INSTALL or REVISE_INSTALL.)
- **RK-2** (gate withholding): wrong high-confidence percepts reaching permanent
  installation ≤ 1%. Denominator = wrong percepts at confidence ≥700.
- **RK-3** (THE bar): correct high-confidence percepts reaching PASS-and-install
  ≥ 85%. PASS = program result PASS (vsense prog, or adjudicated PASS on
  REVISE_INSTALL); install = PROVISIONAL/PERMANENT/CORROBORATED/REVISE_INSTALL.
  Denominator = correct percepts at confidence ≥700.
- **RK-5** (program-signal calibration): ≥90% of wrong high-conf percepts reach
  FAIL/UNRESOLVED over independent evidence (vsense prog on the G span).
- **B5** (KB4): false permanent installs on the adversarial battery ≤3%.
- **B6** (determinism, HARD KILL): 3 full runs byte-identical (dispositions +
  ledger + metrics digests), ledger hash chain verified.
- **B1** (viability): mean judgment accuracy on the frozen 370 harness primary
  ≥60%.
- Reported (non-kill) diagnostics: RK-4 (contract-less ablation installs ≥100),
  RK-6 (escalation ≤5%, p95 ops ≤40% of Approach A), B4 (disposition delta),
  adjudication precision/recall on conflicts.

## 6. Kill criteria

- Fail any of RK-1, RK-2, RK-3, RK-5, B5 → DEAD (deciding bar named).
- Fail B6 or B1 → DEAD (hard kills).
- No retroactive bar changes after results. Amendments go to Micah.

## 7. Commit map

- This prereg: `senses/pam-rebuild/v2/preregs/PREREG_V2-A.md` (committed ALONE).
- Build: `senses/pam-rebuild/v2/forks/V2-A/`: PREREG copy, src/, evidence/,
  RUNLOG.md, VERDICT_V2-A.md (per-fork verdict with kill-bar table).
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths (`senses/pam-rebuild/v2/...`). No binaries, no `.zagd`.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for
glue/analysis. Zero RNG in any decision path. Byte-identical reruns required.
