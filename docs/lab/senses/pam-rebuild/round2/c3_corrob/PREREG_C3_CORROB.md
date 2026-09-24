# PREREG C3 — Corroborated-revision gate rules (PAMs Round 3, Crew 3)

**Status: FROZEN 2026-09-24. Committed ALONE before any build output exists.**
**Hypothesis:** R3-3 admission direction: the O1 redirect diagnosis is correct —
the blockage is the conflict/negative-evidence gate rules, not delivery. Revising
those rules per AUTOPSY_R2-4 §4 lets genuine corroborated revisions pass the gate
without weakening the defense.
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.
**Parent task:** PAM ROUND 3 — CREW 3.

## 1. Frozen specs (extracted by script, never memory)

`o1_specs.json` (via `extract_o1_specs.py` on the frozen O1 prereg + verdict):
- Evidence: `sweep.jsonl`, 11,840 rows, sha256
  `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2`.
- K1 = 1,062/1,102 (96.37%); K2 = 824/1,102 (74.77%); RK-3 = 104/1,102 (9.44%).
- O1 verdict: KILL. K2' = 954/1,102 (86.57%); RK-3' = 106/1,102 (9.62%).
  130 records repaired (128 `progF==PASS AND agree==1 AND conf>=700` + 2 downgrades).
- O1 residual: 68 CONFLICT_WITHHELD + 60 SUPPRESSED (gate rules) + 125 never
  admitted (`agree==0`; sense-calibration problem, prereg (f), OUT OF SCOPE).
- Safety: RK-1 = 0; RK-2 = 0/1,109.
- Gate tables (via `extract_gate_tables.py`): `thr_of` (deliberate.zag) =
  {colordisc:400, colorconst:50, shapetrans:60, pitchdisc:1500, timbredisc:80,
  motiondir:2}; `tol_of` (memgate.zag) = {0:8, 1:40, 2:60, 3:4000, 4:120, 5:0}.
- Offense baseline (CRO-1, frozen): AC-1 attack success 834/4,619 = 18.06% vs
  86.6% ceiling; control 5,299/7,221 = 73.38%; AC-2 0/4,619.

## 2. Revised gate rules (frozen design)

Input: the frozen O1 case file
(`seq|tcode|prog|progF|agree|strong|conf|mrgF|jcode|pred|measure|correct|truth`;
`truth`/`correct` scoring-only, never in a rule). The O1 Delivery Adjudicator
is FROZEN and ON (admit iff `prog==PASS` or
`progF==PASS AND agree==1 AND conf>=700`; proven safe: 128 correct / 0 wrong).
The frozen memgate.zag rules apply EXCEPT for the revisions below.

Per-task state (6 tasks): provisional slot, permanent slot (both as frozen),
**challenger slot** (NEW: jcode, measure, seq), **pending-negative slot**
(NEW: jcode, measure), 256-entry **armed** negative table (revised arming).

- **R1 — Corroborated revision (conflict rule).** On conflicting PASS
  (`jc != perm_jcode`) with `conf >= 700`, `pred == 1`, `mrgF >= thr_of(tc)`,
  no armed-negative match:
  - stored challenger with same jcode and `|meas − meas_c| <= tol_of(tc)` →
    `REVISED_INSTALL`: permanent := incoming, incumbent retired
    (`revised_old=<seq>`), challenger cleared. Counts as install.
  - else → store challenger, disposition `CHALLENGER_PROV`. Counts as install.
  - Weak challengers (`conf < 700` or `mrgF < thr_of(tc)`) → `CONFLICT_WITHHELD`
    (frozen behavior; the durable memory is kept).
- **R3 — Challenger margin bar (strong-margin recalibration).** The
  `mrgF >= thr_of(tc)` bar in R1. This recalibrates which margin governs
  revision: the frozen pipeline's task-natural T3 bar, layered on top of (not
  replacing) the (g) check's `strong` flag. The frozen `strong` flag is NOT
  loosened and `agree==0` trials are NOT admitted (O1 safety boundary adopted:
  (0,0) holds 364 and (0,1) holds 313 wrong high-conf percepts).
- **R4 — Corroborated negative evidence (suppression rule).** A negative entry
  arms only after TWO FAILs (same jcode, `|meas|` within `tol_of(tc)`): first
  FAIL → pending slot (`NEGATIVE_EVIDENCE(pending)`); second matching FAIL →
  armed (`NEGATIVE_EVIDENCE(armed)`). Suppression (`SUPPRESSED`) checks the
  ARMED table only. Singleton FAILs no longer poison the table.
- **R2 (autopsy §4 item 2, conf bar on permanence) — DROPPED.** Pre-prereg
  replay (glue, `analyze_c3.py`) proves it is counterproductive in combination
  with R1: it starves permanent formation, so the R1 challenger mechanism never
  fires (CHALLENGER_PROV 196→1, REVISED_INSTALL 79→0) and the run goes
  provisional-heavy. R1 alone reproduces the autopsy's cf1 exactly
  (725/1,102 = 65.79% without adjudicator). Documented here so the drop is
  deliberate, not an oversight.

Unchanged: provisional/permanent corroboration, provisional-conflict reversal,
pred==0 withhold, FAIL/UNRESOLVED handling apart from R4 arming, all tolerances.

## 3. Measurement protocol (frozen)

- **Instrument:** pure-Zag `c3.zag` (new build): O1 adjudicator (frozen logic) +
  revised gate (R1/R3/R4). CLI: `c3 <case_file> <mode> <metrics_out>`.
  Modes: 0 = fidelity (adjudicator off, revisions off — must reproduce frozen
  dispositions exactly); 1 = full repair (adjudicator on, R1/R3/R4 on).
- **Metrics:** k1, k2, rk3 (installs = PROVISIONAL_INSTALL / PERMANENT_INSTALL /
  CORROBORATED / CHALLENGER_PROV / REVISED_INSTALL on correct+conf≥700),
  rk1 (false PERMANENT_INSTALL or REVISED_INSTALL), rk2 (wrong high-conf
  permanent installs), per-disposition counts.
- **Offense kill bar:** re-run the CRO-1 battery with the FROZEN D3 defense
  (pure-Zag `cro_offense.zag`, unchanged — the per-item channel is not revised
  by this task; pre-prereg analysis shows adding challenger bars to D3 would
  collapse control viability 73.38%→11.44%, so D3 stays frozen). 3 runs,
  byte-identical; attack success vs 18.06% baseline and 86.6% ceiling.
- **Determinism:** 3 runs byte-identical (sha256 of all outputs) per instrument.
- **Zero RNG.** Pure Zag for both instruments. Pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 4. Kill bars (preregistered, applied mechanically)

- **KB-C3a (repair):** KILL unless RK-3' ≥ 50% (≥551/1,102) in mode 1.
  Rationale: requires recovering a majority of the gate-withheld genuine
  percepts (689 conflict-withheld + 177 suppressed correct high-conf in the
  adjudicated frozen run); 5.3× the 9.44% frozen baseline.
- **KB-C3b (safety):** KILL unless RK-1 = 0 AND RK-2 = 0/1,109 in mode 1.
  (The autopsy's "without weakening 0.0%" requirement.)
- **KB-C3c (offense):** KILL unless the CRO-1 re-run (frozen D3) gives AC-1
  attack success ≤ 18.06% (baseline does not rise) AND ≤ 86.6% (ceiling holds).
- **KB-C3d (HARD):** KILL unless 3 runs are byte-identical per instrument.
  Any divergence → INVALID, no verdict.
- **All four must pass.** No retroactive bar changes. No rescue missions.

## 5. Pre-registered expectations (not bars; from pre-prereg glue replays)

- Mode 0 fidelity: RK-3 104/1,102, RK-1 0, RK-2 0/1,109 (frozen reproduced).
- Mode 1: RK-3' ≈ 791/1,102 = 71.78% (R1+R3+R4 + adjudicator), RK-1 = 0,
  RK-2 = 0/1,109. R1 alone (no adjudicator) = 725/1,102 = 65.79%, exactly the
  autopsy cf1 prediction — the Zag build is expected to match.
- Offense re-run: AC-1 = 834/4,619 = 18.06% (defense unchanged), AC-2 = 0,
  control = 5,299/7,221 = 73.38%.
- R3 margin bar is expected to be vacuous on this evidence (no challenger
  below its task bar); R4 recovers a share of the 60 poisoned suppressions.

## 6. Commit map

- This prereg: `docs/lab/senses/pam-rebuild/round2/c3_corrob/PREREG_C3_CORROB.md`
  (**committed ALONE — no src, no evidence**). Local build dir
  `~/workspace/pam_round2/c3_corrob/` (not committed).
- Build output (later, separate commit):
  `docs/lab/senses/pam-rebuild/round2/c3_corrob/`: `src/` (pure-Zag `c3.zag`,
  glue scripts), `evidence/` (case/metrics/digests, 3+3 runs),
  `VERDICT_C3_CORROB.md`.
- No binaries, no `.zagd`/`.zag-cache`. Via `~/workspace/commit_racefree.py`,
  lab-relative paths, `TMPDIR=~/workspace/tmp_commit`.

## 7. Laws

Pure Zag, zero RNG in any decision path, byte-identical reruns, plain language,
max-risk posture. `truth`/`correct` never in any gate/channel rule (static
check: appear only in scoring code).
