# BUILDLOG — SR ROUND, ARM LOSS (proper scoring + anti-collapse)

## 0. Inherited state (RESUME after daemon restart, 2026-09-24)

Predecessor (killed by daemon restart; final message lost) left
`training/sr_round/loss/` EMPTY — fresh start. Directory convention created:
src/, logs/, params/, results/, analysis/ (+ polbuild/ for the policy build).

## 1. Pins (recorded BEFORE first training run, per §10/§12)

- Prereg: PREREG_SR.md FROZEN v1, SHA-256
  `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
  (verified by direct computation, not copied from another arm's log).
- Kill-bar table (§10; bytes from `## §10 Kill-bar table` through the byte
  before `## §11`): SHA-256
  `2243447e5efacdf36af066712662974aed57f86a844dda5ef6a5365c507b0260`
- Weight init: w1=1000, w2..w8=0, b=0, DIV2=40000, GS=500000000,
  gradient-cap p∈[0.1,0.9], Cp∈[1,999], C̄=phase-cells@epoch-start frozen.
  Canonical string `LOSS_INIT v1 w1=1000 w2=0 w3=0 w4=0 w5=0 w6=0 w7=0 w8=0
  b=0 DIV2=40000 GS=500000000 GCAP_LO=100 GCAP_HI=900 CP_LO=1 CP_HI=999
  CBAR=phase-cells-epoch-start-frozen` SHA-256
  `fa8eed0f451b20dd5f6c85565cdfe268ceb39b9a3412f8ed0d0f72c1120f0b40`
- ln table (src/ln_table.zag, deterministic Python math.log generation,
  1001 entries, chunked 11×91 for the znc lexer line limit): SHA-256
  `b734c1ab5391eabfff4aef931656a704e67c1afc7b9898b9a87c31b649868fd3`
- features.tsv SHA-256
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  — matches frozen pin (PREREG_SR §2).
- Toolchain (pinned ONLY):
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
- Trainer binary A/B: SHA-256
  `e52228fd21bc477bafc6174c0ab9b9f8c8aa9222ba1468183aae37d6734f674b`
  (src/train_loss_bin_a == src/train_loss_bin_b, cmp-verified).
- Eval mech id: **m17** (M0–M8=0–8, MT2-CONF=13/14 taken; no other SR arm
  has claimed m17 in its build log as of this writing). Results tags
  `loss10x` / `loss100x`.

## 2. Design decisions (LOSS arm, PREREG_SR §8)

- **Loss:** L = −[Y·ln(C/1000)+(1−Y)·ln(1−C/1000)] − (C−C̄)²/4000000
  + 4·[V2rise]·(C−Cprev)². Theater term identical to v2 (indicator form,
  ×4 held constant). G-batch identical to v2. Curriculum/phases/scale/
  DIV2/head-form(8 inputs) identical to v2.
- **C̄ (crew design choice, recorded):** epoch's mean released confidence
  over the current PHASE's released training cells, computed with
  EPOCH-START weights, frozen within the epoch. Deterministic.
- **Integer gradient (frozen):**
  - core: dL/dp = −Y·1000/Cp + (1−Y)·1000/(1000−Cp), Cp=clamp(C,1,999);
    gradient cap: denominator clamp(Cp,100,900) resp. clamp(1000−Cp,100,900)
    (p∈[0.1,0.9]) — bounds single-cell steps to ≤125, inside v2's theater
    envelope (200). Mid-range parity: at Cp=500, f_i=1000 the core step is
    25, identical to v2's symmetric core at (C=500,Y=1000).
  - GS = 500000000. num_core_i = tdiv(GS·f_i·(Y==1?−1000:1000), 10⁶·q).
  - num_ac_i = tdiv(GS·f_i·(C̄−C), 2·10⁹) — max |step| ≈ 6; the frozen
    0.25-vs-O(1) loss ratio is preserved in update space.
  - num_th_i = 8·rise·f_i (v2, unchanged).
  - w_i ← w_i − tdiv(num_core_i+num_ac_i+num_th_i, DIV2); bias analogously.
  - Overflow bound: |GS·f_i·1000| = 5·10¹⁴ < 2⁶³. ✓
- **Loss telemetry (millionths of nats):** ll = −LT[Cp] (Y=1) /
  −LT[1000−Cp] (Y=0); ac = −tdiv((C−C̄)²,4) (max −250000 = −0.25 nats ✓);
  th = 4·rise² kept in v2 squared-thousandths units, separate column.
  loss (plateau) = ll+ac.
- **§14 item 2 (table vs series):** table chosen. A/B byte-identical by
  construction (frozen file, parsed deterministically at startup).
- **Arenas:** []u8 with au_get32/au_put32/au_get64/au_put64 throughout; no
  `as []i32` casts (ZNC-2026-09-21-007); no slice > 2^25 bytes; no function
  named `zalloc`; slice fields via pointer indirection (AGENTS.md).
- **10× go/no-go (§8):** (a) weights ≠ init; (b) epoch Var(C) never below
  40000 (thousandths²) after epoch 10; (c) meanConfCorrect ≥ 0.30.
- **§14 item 4 (μ-scale) check:** over the 10× run, mean|ac|/mean|ll| must
  lie in [1%, 50%]. Outside → STOP, report, prereg amendment required —
  never a silent constant change.

## 3. Build notes

- znc lexer rejects the 8KB single-line table literal (E0002); table
  regenerated as 11 chunk literals of 91 entries (max line 833 chars).
- Analyzer warnings only (A0101 short-circuit-|| false positive in
  tl_parse_chunk — same idiom as v2's tr_split; E0101 `+0` from v2's
  arena-indexing idiom, kept verbatim).
- Every training log opens with `# prereg_sha=<f55d1dbb…>` (first line).

## 4. Run record (append-only)

- 2026-09-24: 10× A/B: `train_loss_bin_{a,b} ../../features/features.tsv 10
  params/loss_params_10x_{a,b}.zag logs/log_loss_10x_{a,b}.tsv` — both RC=0.
  Params A/B byte-identical (cmp); logs A/B byte-identical (cmp).
  Final weights: w=[555154,−11709,0,254922,437683,−243336,507499,160],
  b=151339.
- 10× go/no-go: (a) PASS (weights≠init); (b) FAIL (Var(C)=0 after epoch 10);
  (c) PASS (meanConfCorrect=1.0). §14 item 4 μ-check: 0.1039% < 1% → DEAD.
  → STOP: no 100×, no silent rescaling.
- Policy build: polbuild/ (v2 policy.zag + harness + 10× params as
  mt_params.zag), binaries policy_loss_{a,b} A/B byte-identical
  (build artifacts only, not committed).
- Eval: `run_eval.sh loss10x polbuild/policy_loss_a 17 0` — 37/37 legs
  A/B byte-identical; M4 refs copied. TSVs in results/ (74 files).
- Analysis: `analyze.py results_loss10x 17` → analysis/analyze_m17.txt;
  guards → analysis/GUARDS_LOSS.md; verdict → VERDICT_LOSS.md.
- Verdict: **LOSS KILLED** — failing bars **B3** (2 strict G-rises,
  redteam), **B5** (separation 0.000 < 0.20), **B8** (vacuous G-flatness).
  Degenerate fixed point conf≡1000.
