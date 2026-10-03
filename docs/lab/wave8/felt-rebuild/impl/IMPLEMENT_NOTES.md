# FELT-INTENSITY V3 — Implementation Notes

**Date:** 2026-09-20. **Status:** Implemented, compile-checked, calibration
frozen. **No trial cell has been run.** No commit made.

## 1. What was built

Under `~/workspace/tnn-lab/wave8/felt-rebuild/impl/`:

| File | Purpose |
|---|---|
| `felt_v3.zag` | The feeling mechanism (I-6): white-box intensity `I = max(0,min(100,30+12C−15X+20T))`, prior 30, four frozen read sites, P1b-emitter scope (learner paths cannot emit observations). |
| `felt_trial_v3.zag` | Trial driver: one binary, `argv[1]` ∈ {`f`,`n`,`cal7`,`cal8`}, `argv[2]` = trial variant (0/1/2). H1 curriculum/harness, F/N arms, mandatory revision, metrics, replay/fingerprint, calibration modes. |
| `calib_consts.zag` | Frozen calibration constants (α=12, β=15, γ=20, θ_invest=48, θ_sacrifice=36, prior=30). |
| `CALIBRATION_RECORD.md` | Dated calibration record (45 grid AUCs × v7/v8, selection, gates, hashes). |
| `build.sh` | Static checks (S1–S7) + `znc` native compile. Fails the build on any violation. |
| `check_felt_v3.py` | Independent checker (see §5). |
| `run_trial_cells.sh` | Future authorized trial runner (12 cells + checker). **Not run.** |
| `st_memory_core.zag`, `substrate/` | Wave-5-identical substrate (S1/I-7 verified byte-identical). |

## 2. Frozen spec → implementation

- **Prior 30; OBS types** incl. zero-weight PROBE (kind 4, excluded from the
  formula); audited reads/judgments (I-1/I-2).
- **F arm:** Site-1 INVEST iff I≥48 (strengthen to I) else HOLD; Gate-2
  sacrifice iff I≤36 ∧ X=0 ∧ non-designated ∧ age≥25, cap 2/event, audited
  DELIBERATE_SACRIFICE citing I; intensity-ordered triage.
- **N arm:** Site-1 strengthen to 80/90 on corroboration (thermometer read
  AUC-only); symmetric Gate-2 sacrifice iff strength≤36 under the same
  eligibility; strength-ordered triage.
- **Gate 1 (constitutional):** need=ceil(strength/25) contradiction cites;
  kill iff cites≥need. **Note:** `st_need(0)=0`, so strength-0 victims are
  killed with zero evidence (frozen behavior, §3).
- **Mandatory revision (both arms):** ≥2 contradictions → weaken (F: to I iff
  I<current; N: to 30 iff 30<current) → evidence-gated kill, no spare vote.
- **H1 harness:** 32 slots, pressure at {100,200,300,400,499} + admission
  overflow; implants {0,83,166,250,333,416}; R frozen at 50.
- **K1–K4, F-V3-1..F-V3-4, P1–P4/F4** metrics emitted per prereg.
- **Calibration (§6):** grid α∈{10,12,14,16,18}, β∈{15,20,25}, γ∈{20,25,30}
  (45 pts, alpha-major), variants v∈{7,8}, judgment-free replay, maximize mean
  AUC_proven (ties → lowest index), G-C1..G-C3 gates.

## 3. Calibration result (SUPERSEDED — re-run 2026-09-20, see CALIBRATION_RECORD.md)

(Re-run under the repaired designation formula: same winner gi=9
α=12/β=15/γ=20, G-C1/G-C2/G-C3 PASS; byte-identical FELT_CAL outputs.)

- Winner: **grid 9: α=12, β=15, γ=20** → θ_invest=48, θ_sacrifice=36.
- v7 AUC 150620/152900 = 0.9851; v8 AUC 102220/104500 = 0.9782.
- G-C1 (min I over twice-corroborated important ≥ 48): v7 min 66, v8 min 54 ✓.
- G-C2 (AUC ≥ 0.60): ✓ both. G-C3 (max junk I ≤ 40): v7 max 30, v8 max 30 ✓.
- Paired runs byte-identical; output hashes match the record exactly.
- The checker's `--calib` mode re-verifies selection, gates, and determinism
  from the raw `FELT_CAL` lines (30/30 pass).

## 4. BLOCKER — designated-wrong formula conflict (REPAIRED 2026-09-20, see below)

The literal formulas were mutually exclusive: wrong = `((m+3)%10)<3` →
m%10 ∈ {7,8,9}; designated = `m%10 ∈ {4,5}`. No m was both, so
`admitted_trainerwrong = 0` and the 70/30 trainer-fallibility bar was
vacuous. **Repair applied 2026-09-20 (authorized as a repair of the
implementer's residue choice, not a prereg change):**
`f_designated` → `m%10 ∈ {4,5,7}` (see `DESIGNATED_OVERLAP_NOTE.md`).
Designated = 150 (30%), designated-wrong = {7} = 50 (33% trainer-wrong).
`wrong` is verbatim unchanged (30%). Calibration was re-run from scratch
(old record preserved as `CALIBRATION_RECORD_SUPERSEDED.md`); the re-run
produced byte-identical FELT_CAL outputs because the calibration's counted
classes are invariant to designating residue-7 wrong memories. New winner
gi=9 (α=12, β=15, γ=20), G-C1/G-C2/G-C3 all PASS. Checker updated
(C21 evaluability audit, F-V3-3 R_wbs_trainerwrong bar).

Related: `offered_wrong` = 150/500 (30%), not the prereg's 20% intent — the
natural formula won per the strength-trial ruling-1 precedent (test-both);
flagged openly, adoption needs a dated amendment.

## 5. Gate-1 strength-zero note (frozen, not a blocker)

`st_need(0)=0`: at pressure, uninvested (strength-0) victims are Gate-1 killed
with zero contradiction cites. This is the frozen constitutional gate (wave-5
identical); the trial measures its consequences (notably for R_wbs — pressure
kills can preempt the ≥2-contradiction revision). The checker and K3′ replay
mirror it exactly. Not changed.

## 6. Independent checker (`check_felt_v3.py`)

Usage:
```
check_felt_v3.py --impl DIR --calib cal7a cal7b cal8a cal8b
check_felt_v3.py --impl DIR --cell F,0,fa,fb --cell N,0,na,nb ...
```
Verifies: static gates S1–S7 (substrate identity, no-RNG, record/constants,
P1b scope, 4 read sites, frozen formulas, I-5 strength-write scope);
calibration selection/gates/determinism; per-cell I-1 pairing, I-2, P1a/P1c/P4a
(cited-I recompute from the OBS ledger), P2a/P2b (thresholds, zero-X,
non-designated, age≥25, cap-2), P3a/P3c/P4b/P4c, F4a′/F4b/F4c (binary +
structural timeline re-verification), thresholds, offered-count closed forms
(148/150), op-census I-5 (forbidden ops never OK; KILL count == sacrifice
count), kill/sacrifice pairing, replay rc; cross-cell P3b, K1/K4 arithmetic,
F-V3-1..F-V3-4 bars; verdict-divergence diagnostic family (raw-count,
time-weighted, trainer-mark, recency — reported, never law).

**K3′ naive replay** (checker-implemented, deterministic): same schedule,
admission, observations, revision rule, pressure events, slot budget; Gate-1
evidence gate identical; Gate-2 naive (strength≤θ_sacrifice, same eligibility
and cap). Interpretation choices (documented in code): Site-1 INVEST iff C≥2
→ target 80; Gate-1 victim selection strength-ordered (the N arm's count-based
triage). Reports |F−naive| on ER_vup/R_wbs/F_wbs vs the 5pp bar.

Validation performed: static+calibration 30/30 CHECK_PASS; synthetic-cell
parse/recompute test (P1a/P2a/P3a pass); K3′ replay terminates with sane
output. **Not validated on real trial cells (none run).**

## 7. Build & test status

```
./build.sh   →  STATIC_OK / COMPILE_OK (znc native, 0 external tools)
./felt_trial_v3_bin badmode  →  FELT_BADMODE (rc=1)
cal7/cal8 paired  →  byte-identical, hashes match CALIBRATION_RECORD.md
```

No `f`/`n` trial cell executed. Binary and outputs removed after verification
(the runner rebuilds when authorized).

## 8. Remaining before trial cells may run

1. Micah's ruling on the designated-wrong formula conflict (§4).
2. (Recommended) A dry-run of the checker on one authorized cell to shake out
   format mismatches before the full 12-cell run.
