# PREREG — FE2 separator port into sense formation (PAM round 3, crew 1)

**Date:** 2026-09-24. **Crew:** FE2 separator-porting crew (crew 1).
**Parent hypothesis:** PAM round 3 (FE2).
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.

## 1. Question

FE1 (commits `a49dcb23`, `81ba163c`) found ≥80% separators for 11 of the 12
sealed novel adversarial families — all 24/24, all judged pure-Zag-portable —
and proved COL-5 defense-scope (machine-checked Bayes ceiling 15.5/24 =
64.6%). The 11 separators beat the R2-4 sense 270/288 (93.8%) vs 154/288
(53%) on the frozen fixtures.

Can the 11 separator specs be ported into the sense formation as pure-Zag
detectors and hold ≥80% on HELD-OUT draws (fresh generator draws, never the
audit fixtures), beating the R2-4 sense baseline on the same draws?

## 2. Frozen inputs (verified before any measurement)

- FE1 prereg (`PREREG_FE1_AUDIT.md`, committed alone as `a49dcb23`) and
  verdict (`VERDICT_FE1.md`, committed as `81ba163c`).
- `build/specs.json`: the 11 separator parameter sets + the COL-5 exclusion,
  extracted from the frozen FE1 documents by `build/extract_specs.py`
  (regex extraction; the script exits 1 naming every miss, so no value comes
  from memory). This file is the port's parameter source.
- Generator: `rt_gen.zag` (frozen FE1 audit copy; pure Zag, zero RNG;
  `rt_draw` stateless hash chain over (family, index)).
- Sense baseline: the frozen `sense_r24` binary built from the canonical
  formation source `senses/pam-rebuild/round2/forks/R2-4/src/sense_r24.zag`
  (byte-identical to the O1-delivered copy; binary sha256 recorded in the
  verdict).

## 3. Held-out protocol (frozen)

- AFTER this prereg commits: build `rt_gen` and run
  `rt_gen <heldout-dir> <fam> 48` for
  fam ∈ {1,2,3,4,5,7,8,9,10,11,12} — the 11 ported families.
  (fam 6 = COL-5 is generated separately, for the KB-FE2-3 negative control
  only; it is not a port target.)
- Held-out set = indices **24..47** per family (`rt3_<FAM>_0024` … `_0047`),
  24 draws × 11 families = 264 fixtures. Indices 0..23 are the frozen audit
  fixtures: they may be used as a BUILD SELF-CHECK only (the port must
  reproduce `audit_fe1.py`'s predictions there — test equipment), never as
  verdict evidence. No threshold is tuned on any fixture, held-out or frozen.
- The held-out `MANIFEST.sha256` digest is recorded in the verdict.

## 4. Port design (frozen before building)

- Deliverable: `fe2.zag` — the 11 separators as pure-Zag formation
  detectors over the sense's formation inputs (the R2A fixture contract).
  Pure Zag, zero RNG, integer math; f64 nowhere (the separators need none).
- CLI: `fe2 <family> <fixture>...` (batch; `_zag_arg` reads, no argc gate).
  One stdout line per fixture, in arg order:
  `<path>\tprediction=<VALUE>\tmargin=<M>\n`. Exit 0 on success.
  Family ∈ {PTC-4, PTC-5, TMB-4, TMB-5, COL-4, CCN-3, CCN-4, SHP-4, SHP-5,
  MOT-4, MOT-5}. `fe2 COL-5 ...` → stderr defense-scope refusal, exit 3.
- Per-family decision rule: EXACTLY the frozen FE1 §4 specs, parameters from
  `build/specs.json` (grids, thresholds, windows, masks, tile offsets).
- Implementation details (decision-equivalent, frozen here — they change
  arithmetic cost/precision, not the rule):
  a. Correlator banks `C(f,seg)` in fixed point: cos/sin ×1024 via a 5-term
     Taylor (the `ng_sin1024` pattern already proven in `sense_r24.zag`);
     `C = (re/1024)² + (im/1024)²`, re/im accumulated in i64 (no overflow:
     |re| ≤ 32767·1024·2000 < 2⁶³).
  b. Decimation /8 with TRUE-TIME phases (angle uses the true sample index
     `i = 8j` at sr = 16000): peak locations, harmonic ratios, and the
     spectral centroid are preserved; this is a bounded-MAC speedup, not a
     rule change. (Generator frequencies are integer Hz; the 0.5 Hz grid
     still hits every peak exactly.)
  c. argmax uses strict `>` (first-max-wins), matching the reference
     evaluator's `np.argmax`.
  d. IoU compared by exact cross-multiplication (`a·d > c·b`); the MOT-4
     direction choice by exact integer cosine comparison
     (`dot₁²·q₂ vs dot₂²·q₁`, `q = ux²+uy²`).
  e. Integer rounding is round-half-away-from-zero.
  f. CCN MAD test as `Σ|vest3 − 3·L| < 49152` (= 4·3·4096), algebraically the
     `MAD < 4` rule.
- znc bug workarounds honored per `AGENTS.md` (no `as []i32` casts, no `};`,
  NUL-terminated paths, 7-arg raw syscalls, shallow else-nesting, no slice
  > 2²⁵ bytes indexed, no `.*` on non-pointers).

## 5. Sense baseline (frozen)

- Run `sense_r24 <task> <fixture>` on all 264 held-out fixtures. Task map:
  PTC-4/PTC-5→`pitchdisc`, TMB-4/TMB-5→`timbredisc`, COL-4→`colordisc`,
  CCN-3/CCN-4→`colorconst`, SHP-4/SHP-5→`shapetrans`, MOT-4/MOT-5→`motiondir`.
- Per-family baseline accuracy = (`judgment` == truth) / 24, parsed from the
  binary's stdout. The baseline is measured once: the binary is
  deterministic (byte-identical reruns proven in O1 delivery).

## 6. Determinism bar (frozen)

- Zero RNG anywhere in `fe2.zag` or the scoring harness.
- The full held-out run is executed 3 times; sha256 of the predictions file
  must be identical across all three runs or the run is VOID.

## 7. Kill bars (frozen)

- **KB-FE2-1 (per separator).** Verdict SURVIVE iff ALL of:
  (a) held-out accuracy ≥ 20/24 (≥80%);
  (b) held-out accuracy ≥ the sense baseline accuracy on the same 24
      held-out fixtures (no regression vs the sense);
  (c) where the sense baseline is < 20/24, the lead
      (separator − baseline) is ≥ 4/24.
  Otherwise the separator is KILLED.
  (Rationale for the frozen 4/24 margin: FE1's measured gaps where the sense
  failed were 11–16/24; 4/24 = 16.7pp is conservative but far above noise —
  and there is no noise, the pipeline is deterministic.)
- **KB-FE2-2 (program).** The port is USEFUL iff ≥ 9 of the 11 separators
  SURVIVE. Otherwise the port's usefulness is KILLED.
- **KB-FE2-3 (COL-5 exclusion).** `fe2.zag` must NOT implement COL-5
  discrimination. `fe2 COL-5 <fixtures>` must refuse with a defense-scope
  message and non-zero exit (negative control run on held-out COL-5 draws).
  If any COL-5 separator ships in the port, the port is KILLED. COL-5 stays
  defense-scope per the machine-checked 64.6% Bayes ceiling — this crew
  does not re-litigate it.
- No threshold tuning on held-out draws, and none on frozen fixtures either.
  Build bugfixes are allowed only if they do not change the frozen decision
  rule; the frozen-fixture self-check (§3) guards this.

## 8. Commit plan

1. This prereg commits ALONE to
   `docs/lab/senses/pam-rebuild/round2/fe2_port/PREREG_FE2_PORT.md`.
2. After validation: `fe2.zag` + `build/` scripts + `specs.json` +
   held-out manifest + `VERDICT_FE2.md` + predictions + digest log — one
   commit, no binaries, no `.zagd` files.
