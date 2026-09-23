# F2 APPEAL VERDICT — KB4 judgment-side channels

**Date:** 2026-09-23. **Verdict:** **WRAPS** (final and binding per the appeal mandate).
**Prereg:** `f2appeal/PREREG_FROZEN_F2APPEAL.md` (frozen commit `b02beb9e8859b46da7aa3dcc0ee9b7b26707d`).
F2 permanent retirement of C2/C3-class judgment-side channels **STANDS** for the frozen threat model.

## What was tested

PACKAGE 3 (verdict commit `a6b9d999`) measured three judgment-side members dead:
C2 deterministic transform-consistency 0.0000 bits (F1+F4 fired), C3 honest noisy
re-observation 0.0049 bits pooled, confidence 0.0797 bits — while C1 (non-judgment-side)
scored 0.9968 bits. Micah reversed the no-appeal ruling and ordered this appeal battery:
four new preregistered tests, frozen before execution, crew verdict final and binding.

| Test | Design | Members |
|---|---|---|
| G0 | Reproduction gate: both frozen senses, all 185 fixtures, judgment+confidence vs frozen records, 2× byte-identical | gate |
| R1 | C3 noise idea at 7 amplitudes (±50…±2400 pcm, ±1…±64 img/vid), frozen seeds | L0–L6 |
| R2 | 5 independent re-observations, majority agreement at L3/L5 | L3, L5 |
| R3 | C2 transform idea, 3 NEW transforms (vflip, signflip, fshift); byte-level involution checks; ≥95% calibration-legibility gate (F3) | 3 transforms |
| R4 | Structured noise: block/frame-correlated drift (V1), ternary {-A,0,+A} (V2) | V1, V2 |

All mechanisms (noise draws, transforms, majority votes, channel verdicts, contingency
counts) are pure Zag; Python is glue only. truth.json opened only at score time.

## Integrity

- G0: **PASS** — 370/370 frozen judgment+confidence reproductions, pass1==pass2 byte-identical.
- All 14 members: run1/run2 verdict files byte-identical; generation SHA256 manifests byte-identical.
- Scorer: pure-Zag contingency counts vs independent Python recompute — **0 mismatches** (14/14).
- R3 involution T(T(x))==x byte-verified on every applicable fixture; 0 failures.
- R3 F3 legibility gates identical across runs: vflip A 48/48 PASS / B 37/48 VOID;
  signflip A+B 30/30 PASS; fshift A 4/15 VOID / B 6/15 VOID. VOID cells excluded per the frozen rule.

## Results (pooled TEST adversarials; H(Y) prior = 0.9958 bits)

| Member | bits | false-install | RECOVERY |
|---|---|---|---|
| R1 L0–L6 (best: L4) | 0.0144–0.0296 | 0.420–0.456 | null ×7 |
| R2 L3 / L5 | 0.0173 / 0.0000 | 0.442 / 0.463 | null ×2 |
| R3 valid cells (A/vflip, A/signflip, B/signflip) | 0.0000 | 0.267–0.489 | null |
| R4 V1 / V2 | 0.0102 / 0.0167 | 0.443 / 0.436 | null |

Maximum pooled bits 0.0296 (5× below the 0.15 bar); maximum per-sense bits 0.0541
(R1-L3 sense A, 2.8× below bar); every false-install ≥ 0.267 against a bar of < 0.15.
No amplitude separates fooled from correct judgments (R1 curves flat; L5–L6 collapse
to ~0 bits). Majority voting squeezes bits to exactly 0.0000 at L5 (R2). The DPI
identity J(T(x))==L(J(x)) holds on every new transform where the judge stayed legible —
signflip 60/60 agreement, vflip-A 47/47 (R3). Structured noise changes nothing (R4).

## Mechanical rule (§6)

RECOVERY fires iff any member clears bits > 0.15 AND false-install < 0.15 with 2×
byte-identical reruns and 0 cross-check errors. **No member cleared either conjunct,
let alone both: 14/14 NULL → WRAPS.**

## Debate record

- D1: native PRO-WRAPS and CON position papers (pre-result, with falsifiers).
- D2: gpt-5.6-sol steelmanned both camps pre-result (verbatim).
- D3: post-result updates — CON **signed WRAPS** (all four recovery mechanisms refuted;
  all three D1 evidence demands met); PRO confirmed predictions, owned its R2
  false-install miss (predicted ≥0.90, measured ~0.44).
- D3 Sol adjudication: "WRAPS, mechanically and conclusively under §6 for the frozen
  threat model"; G1 sufficient governance; strongest remaining objection is
  finite-battery non-exhaustion (a scope limit, not a verdict-changer).
- D4: one rebuttal round per camp (see debate/).

## Governance (amendment G1, frozen)

F2 auto-execution is scoped to the frozen threat model ONLY — one adversary
construction (δ ≲ σ band), two frozen senses, six tasks. A new adversary construction,
new sense, or new task family requires a NEW preregistered battery; automatic
extrapolation is forbidden. Any C* reopening applies member-by-member. This verdict
is not a universal theorem that no judgment-side channel can exist.

## Bottom line

The appeal Micah ordered returned a decisive, comprehensive NULL across 14
member-configs: maximum signal 5× below the bar, every false-install far above it,
determinism and scorer integrity airtight, both native camps and the external
adjudicator aligned. **F2 stands. The judgment-side channel family (C2/C3-class)
remains permanently retired for the frozen threat model. WRAPS.**
