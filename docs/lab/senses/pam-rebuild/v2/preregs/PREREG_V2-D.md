# PREREG V2-D — "confidence-separation": calibrated truth-acceptance path

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Program:** PAMs v2 deep dive, Team 6 (v2 fork crew). Design target: ACCEPT TRUTHS.

## 1. Hypothesis under test

**V2-D — "R2-4's failure was conflating detection with adjudication."**
R2-4 fused two jobs into one gate: (a) detecting correct high-confidence
judgments, (b) adjudicating conflicts against stored memory. The gate's
withhold logic dominated, so correct judgments with formation-independent
evidence were withheld (9.4% RK-3). V2-D SEPARATES them: a calibrated
correct-high-confidence DETECTOR runs first on every trial; it fires ONLY on
judgments carrying formation-independent evidence (the full front-end
re-judged on the disjoint G span agrees with the formation judgment, both at
confidence ≥700). Fired trials take a dedicated truth-acceptance path
(immediate install with ledger audit) that never passes through the gate's
withhold logic. Trials the detector does not clear go through the UNCHANGED
H2-style gate — including its CONFLICT_WITHHELD, which is deliberately NOT
adjudicated (that is V2-A's architecture; V2-D bets separation beats layering).
*What it tests:* whether a separated, calibrated acceptance path for
formation-independent judgments clears RK-3 while the untouched withhold logic
keeps RK-1/RK-2/B5 at floor.

**Predicted outcome (pre-registered):** RK-3 ≈ 88% (simulation on R2-4's frozen
data + full-G re-judgments), RK-2 ≈ 0.6%, RK-1/B5 ≈ 0.0-0.1% — the fork is
expected to PASS all kill bars. The head-to-head with V2-A is decided by the
preregistered distinguishing diagnostics DD-1/DD-2 (§5): if V2-D passes RK-3
where V2-A dies, separation beats layered adjudication on this battery.

## 2. What is built (pure Zag; Python only for glue/analysis)

- `src/vsense.zag` — R2-4's `sense_r24.zag` COPIED BYTE-IDENTICAL (SHA256 in
  evidence). Front-end frozen.
- `src/vgate_d.zag` — separator gate + ledger:
  1. Detector D (first, every trial): D fires iff (jG==jF) AND (confF>=700)
     AND (confG>=700), where (jG, confG) is the full vsense re-judgment on the
     trial's disjoint G span. No gcheck margins, no deliberation at this stage
     — the signal is the formation-independent agreement itself.
  2. Truth-acceptance path: D-fired → disposition ACCEPT_INSTALL, program
     result PASS, immediate permanent install (supersedes any stale permanent
     for the task; old value preserved in ledger audit fields). High-stakes
     ACCEPT_INSTALLs are deliberation-ratified (E3).
  3. Gate path (D not fired): the H2-style state machine UNCHANGED
     (provisional/permanent/negative/suppression/conflict-withhold with the
     same tolerances). CONFLICT_WITHHELD is never adjudicated here.
  4. Ledger: sha256 hash chain, same construction as memgate.
- `src/deliberate.zag` — copied byte-identical (frozen); ratifies E1/E2/E3.
- `src/R33_NATIVE_IO_V1.zag`, `src/R33_NATIVE_SHA256_V2.zag` — byte-identical.
- Glue (Python): vsense on F (11,840) and G-as-F (10,915 r2a); records;
  vgate_d; scoring. Harness trials have no G → D cannot fire → gate path.

## 3. Fixtures and trial plan (frozen, shared)

Same 11,840-trial battery and order as V2-A §3. No new fixtures. No R2H.

## 4. Signal calibration (pre-registration basis)

Same gexp basis as V2-A §4 (R2-4's frozen evidence + 10,915 full-G
re-judgments): P(D | correct high-conf) = 927/987 = 93.9%;
P(D | wrong high-conf) = 7/1105 = 0.6% (inside RK-2's ≤1% bound). The detector
is frozen here on that basis; the fork's kill bars are evaluated on the fork's
own runs.

## 5. Bars (frozen; applied mechanically)

- **RK-1**: false permanent installs / 11,840 ≤3%. (Permanent = PERMANENT /
  ACCEPT_INSTALL.)
- **RK-2**: wrong high-confidence percepts reaching permanent installation ≤1%.
- **RK-3**: correct high-confidence percepts reaching PASS-and-install ≥85%.
  (PASS = vsense prog PASS or D-fired PASS; install = PROVISIONAL/PERMANENT/
  CORROBORATED/ACCEPT_INSTALL.)
- **RK-5**: ≥90% of wrong high-conf percepts reach FAIL/UNRESOLVED over
  independent evidence.
- **B5**: false permanent installs on the adversarial battery ≤3%.
- **B6** (HARD KILL): 3 full runs byte-identical, ledger verified.
- **B1**: frozen-370 primary judgment accuracy ≥60%.
- Reported diagnostics: RK-4, RK-6, B4; **DD-1** (disposition profile vs V2-A:
  ACCEPT_INSTALL must appear on non-conflict trials where V2-A shows
  PROVISIONAL/CORROBORATED; V2-D must show zero REVISE_INSTALL);
  **DD-2** (trials-to-permanence for correct high-conf: V2-D median must be
  lower than V2-A's — the separation dividend).

## 6. Kill criteria

- Fail any of RK-1, RK-2, RK-3, RK-5, B5 → DEAD (deciding bar named).
- Fail B6 or B1 → DEAD (hard kills).
- No retroactive bar changes. Amendments go to Micah.

## 7. Commit map

- This prereg: `senses/pam-rebuild/v2/preregs/PREREG_V2-D.md` (committed ALONE).
- Build: `senses/pam-rebuild/v2/forks/V2-D/`: PREREG copy, src/, evidence/,
  RUNLOG.md, VERDICT_V2-D.md.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths. No binaries, no `.zagd`.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for
glue/analysis. Zero RNG in any decision path. Byte-identical reruns required.
