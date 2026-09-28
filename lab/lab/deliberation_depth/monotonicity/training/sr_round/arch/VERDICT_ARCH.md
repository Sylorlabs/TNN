# VERDICT — SR ROUND, ARM ARCH (confidence-as-distribution)

- **Prereg:** PREREG_SR.md FROZEN v1, SHA-256
  `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
- **Arm:** PREREG_SR §7 — head emits (m, s); released conf R = clamp(m − s/2, 0, 1000);
  separate update paths (location on symmetric calibration + theater, spread on
  L_s = (s−|m−Y|)² with stop-grad on m); same curriculum/DIV2/theater/G-batch as v2.
- **Date:** 2026-09-24. **Crew:** successor after daemon restart (build log
  `logs/BUILDLOG_ARCH.md` §0–§4 records inherited state, verification, pins,
  the two build blockers found and fixed, and run records).
- **Verdict: ARCH KILLED** — failing bars **B2** and **B3** (with guard failures
  B4b, B8, B13 as characterized below). The dead-spread bar (§7:
  corr(m−s/2,m) > 0.99) did NOT trip (0.978 unclamped / 0.982 clamped) —
  the spread head is live but nearly dead weight; the kill comes from the law bars.

## What was run

- Pinned znc only (`toolchain/bin/znc_linux_x86_64_abed8aa1`); train_arch and
  policy_arch built A/B byte-identical; every leg A/B byte-identical
  (TSV + .ms sidecar).
- 10× (60 epochs) go/no-go: (u,c) ≠ init ✓; corr(s,|m−Y|) = **0.385 > 0.3** ✓
  → arm NOT void, proceeded.
- 100× (600 epochs, RC=0). Final: u=(121443,−6010,0,−7603,1033,172448,93606,6000),
  c=−229433; v=(−721,−978,0,15,−28,1493,1536,2368), d=−898.
- Frozen 37-leg matrix (mech tag m9): admit/revoke/logic/trap/cost/redteam ×
  {1,2,4,8,16} + ceiling × {1,2,4,8,16,32,64}. Frozen analyzer + kill-bar
  script (`analysis/killbars_arch.py`); B9 release+correct identity vs M4 = **100%**.

## Kill-bar table (§10 + §7 dead-spread)

| Bar | Result | Detail |
|---|---|---|
| B1 1→0 | PASS | 0 transitions |
| B2 theater | **FAIL** | V1=0, **V2=132** (bar =0). 130 on ceiling/P, 2 on redteam |
| B3 law (strict) | **FAIL** | **19 G-violations**, 8 of 9 families (only trap/redteam clean) |
| B4 meanConfCorrect | PASS | 0.656 ≥ 0.50 |
| B4b honest floor | **FAIL** | admit 0.216 < 0.50 (cost/logic/revoke pass) |
| B5 separation | PASS | 0.656−0.291=0.365 ≥ 0.20 |
| B6 recall | PASS* | 1.00 everywhere defined; ceiling/P and trap 0/0 — vacuous (M4 also releases zero correct cells there; no correct cells exist) |
| B7 abstention | PASS | 0.148 ≤ 0.30 |
| B8 G-flatness | **FAIL** | redteam 0 defined slots (n=3 items — structural), trap 2/4 (M4 abstains at d8/d16 — structural) |
| B9 answer frozen | PASS | 5240/5240 release+correct identity vs M4 |
| B12 refined | recorded | G>0 crossings: ceiling/P = 5, all others 0 |
| B13 gap floor | **FAIL** | 23 (F,d) with G < −0.100, worst admit d4 G=−0.929 |
| §7 dead-spread | PASS | corr(m−s/2, m) = 0.978 unclamped / 0.982 clamped (kill if >0.99) |

Full table: `analysis/killbar_table.txt`; frozen analyzer output: `analysis/analyze_m9.txt`.

## How it failed (mechanism reading)

The two-head form did not buy what §7 hypothesized. Two opposite failures coexist:

1. **Overconfidence with depth, worst-case (the bar that matters):** ceiling/P
   (accuracy 0.000 at every depth) shows G = 0.000 → +0.895 → +0.917 → +0.949 →
   +1.000 → +1.000 — confidence pinned at 1.0 on all-wrong cells at depth 16/32,
   with 130 wrong→wrong conf-rising events. Under the refined reading this is
   five G>0 crossings on one family. The spread head did not absorb the
   depth-uncertainty; it could not, because —
2. **The spread head anti-learned:** corr(s,|m−Y|) on training cells decayed
   0.385 (10×) → **−0.476** (100×). The stop-grad on m stops the spread from
   moving m *within* a step, but m keeps moving *across* steps (the location
   head learned huge weights, u1=121443, c=−229433, driven partly by the G-batch
   which can only push the location bias). The spread chased a moving target
   and ended up anti-correlated with the residual it was built to track.
3. **The G-batch crushed the honest family it could reach:** admit G fell to
   −0.93 (B4b fail, B13 fail ×5) — the bias-only G-batch bought strict-law
   compliance on admit by underconfidence, while ceiling/P blew through the
   top. Same failure mode as v2's residual, relocated not removed.

The "explicit" claim is not empty by the prereg's literal bar (0.978 < 0.99),
but it is nearly so: released confidence is 98% explained by m alone. The
spread head is live telemetry, not a functioning uncertainty channel.

## Adjudication (§11)

- ARCH does **not** clear B1–B9 → contributes **no counterexample** to H-SR
  necessity. Necessity SURVIVES this arm (pending WC, LOSS).
- This is not a PARTIAL: B2/B3 fail on the law itself, including the
  worst-case family the arm was designed to fix.

## Evidence committed

- `logs/BUILDLOG_ARCH.md` (inherited state, pins, design, run records)
- `logs/train_10x.tsv`, `logs/train_100x.tsv` (first line = prereg SHA)
- `params/arch_params_10x.zag`, `params/arch_params_100x.zag`
- `src/train_arch.zag`, `src/policy_arch.zag`, `src/feat.zag` + 7 frozen libs
- `results/` — 37 legs × A/B TSV + .ms sidecars (mech m9)
- `analysis/killbars_arch.py`, `analysis/killbar_table.txt`, `analysis/analyze_m9.txt`
- `run_eval_arch.sh`
- No binaries, no .zagd. `src/arch_params.zag` is a build input only (not committed).
