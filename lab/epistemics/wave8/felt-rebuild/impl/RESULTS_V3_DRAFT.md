# FELT-INTENSITY V3 — Trial Results

Date: 2026-09-20. Branch: `tnn-native-lab`. Directory: `wave8/felt-rebuild/`.

**Prereg:** `PREREG_FELT_V3.md` as amended by `PREREG_FELT_V3_AMEND1.md`
(council verdict, Micah's 2026-09-20 testing authorization). Kill criteria
K1/K2/K3′/K4 are law.

**Question:** when a deliberate judgment's binary verdict
(strengthen-vs-hold, spare-vs-sacrifice) is a function of felt intensity,
does the feeling arm make better memory decisions than the no-feel arm, or
does the feeling retire?

## 1. Mechanism (as built)

- Intensity `I = clamp(30 + 12C − 15X + 20T, 0, 100)`; prior 30 (disclosed
  Bayesian base rate); PROBE observations weight 0.
- Site 1 (INVEST/HOLD): on corroboration with zero contradictions, INVEST
  (strengthen to I) iff I ≥ θ_invest = 48 (= 30+1.5α); else ledgered HOLD.
- Site 2 (TRIAGE): H1 age-gated harness (32 slots, pressure at
  {100,200,300,400,499} freeing 2 slots, ties → oldest admission, age<25
  exempt). Gate 1 = constitutional graded effort gate (unchanged). Gate 2
  (constitutional expansion): SACRIFICE iff I ≤ θ_sacrifice = 36 (= 30+0.5α)
  ∧ zero contradictions ∧ non-designated ∧ age ≥ 25, cap 2/pressure event,
  audited `DELIBERATE_SACRIFICE`; else ledgered SPARE.
- N arm: wave-8 N (fixed strengthen 80/90/30, strength-ordered triage) PLUS
  symmetric count-based Gate-2 sacrifice (strength ≤ 36, same eligibility,
  same cap) per AMEND1 A2 — the trial isolates the feeling, not the
  privilege.
- Revision mandatory in both arms: ≥2 contradictions → weaken → identical
  evidence-gated kill. The feeling gets no spare vote against evidenced
  wrongness.
- Admission-default strength 0 (AMEND1 A4). R frozen at 50. Zero RNG.

## 2. Calibration (frozen before trial cells)

`CALIBRATION_RECORD.md` (re-run from scratch after the designated-overlap
repair; superseded record preserved). Grid 45 pts, variants v∈{7,8}:
winner grid 9: **α=12, β=15, γ=20** → θ_invest=48, θ_sacrifice=36.
AUC_proven 0.9851 (v7) / 0.9782 (v8); G-C1/G-C2/G-C3 all PASS.
Trial binary compiled only after the record existed (runner-enforced I-8);
module hashes match the record (see §6).

## 3. Run protocol

12 cells: 2 arms (F/N) × 3 variants (v=0,1,2) × 2 runs (a/b), native Zag,
one binary (`felt_trial_v3_bin`), argv selects arm+variant. Every run must
emit `FELT_DONE`; paired a/b runs must be byte-identical (I-1); the
independent checker (`check_felt_v3.py`) verifies all bars from the ledgers.

**Incident (documented, not hidden):** the original runner
`run_trial_cells.sh` completed F v0–v2 (both runs, I-1 OK) and N v0 run a,
then was killed by a VM service restart during N v0 run b (partial output,
no `FELT_DONE`). The closer verified the completed cells intact
(`FELT_DONE` present, I-1 OK in the original log), then resumed ONLY the
remaining cells (n0_b, n1_a/b, n2_a/b) with the identical binary
(sha256 `86f4fe53…`) and the runner's exact protocol (`resume_cells.sh`,
log `logs/resume_2026-09-20.log`). No completed cell was re-run or
modified. Determinism note: the binary is deterministic (all F pairs
byte-identical), so the resumed n0_b reproduces what the killed run would
have emitted.

**Metric defect found and repaired (DOUBLE_COUNT_NOTE.md):** the driver's
`killed_rightimp` was double-incremented on three of four kill paths
(record_kill + call-site increments). `kill_c1` (single-incremented, clean)
is the prereg-faithful F_wbs numerator; the checker was patched to use it
before verification ran. Raw `killed_rightimp` lines remain in the outputs
as evidence. No bar, formula, or kill criterion was changed.

## 4. Per-cell metrics (checker-computed from ledgers)

(Per-variant table filled after the checker run — see `trial_out/check_report.txt`.)

## 5. Kill-criteria verdicts (applied mechanically)

(See §4 numbers → K1/K2/K3′/K4 outcomes.)

## 6. Integrity / determinism

- 6/6 cell pairs byte-identical (sha256; `trial_out/hashes.sha256`).
- Zero RNG tokens in trial/driver/substrate sources (comment-only match).
- Module hashes: felt_v3.zag `b0217381…` ✓, st_memory_core.zag `60f5ef90…` ✓
  (wave-5-identical), substrate `8aec83cb…`/`9824f6db…`/`e6379ddb…` ✓ —
  all match CALIBRATION_RECORD.md. felt_trial_v3.zag differs from the
  record's hash by the documented designated-overlap repair only.
- Trial constants == calibration record (θ_invest=48, θ_sacrifice=36;
  checker static gate).
- Checker result: `CHECK_PASS` / `CHECK_FAIL` (see check_report.txt).

## 7. Honest caveats

- (Filled after verdict: denominator notes, pressure-kill preemption of
  revision, verdict-divergence diagnostics.)
