# BUILDLOG — SR ROUND, ARM WC (worst-case OPTIMIZER)

## 0. Inherited state (RESUME after daemon restart, 2026-09-24)

Predecessor (killed by daemon restart; final message lost) left:
`training/sr_round/wc/` = src/ (9 files: R33_NATIVE_IO_V1.zag,
R33_NATIVE_SHA256_V2.zag, dlb_cfg/dlb_delib/dlb_json/dlb_ledger/dlb_util.zag,
mt_gate.zag, policy.zag), polbuild/ (EMPTY), logs/ (EMPTY), params/ (EMPTY),
results/ (EMPTY), analysis/ (EMPTY). No train_wc.zag — build unfinished.
No training ran. No commits landed (branch head still cab05d07).

Verified 2026-09-24 by successor (this crew):
- All 7 library files byte-identical to t05/v2/training copies
  (cmp -s against backlog/t05/src, v2/src, training/src — all SAME).
- mt_gate.zag byte-identical to t05's mt_gate.zag.
- policy.zag differs from t05's policy5.zag ONLY in `@import("mt_params.zag")`
  vs `@import("t05_params.zag")` — a correct adaptation (WC trainer emits
  mt_w0()..mt_w7(), mt_b() constants, same 8-input M4-release skeleton).
- features.tsv SHA-256 = 4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d
  — matches frozen pin (PREREG_SR §2). Correct frozen copy confirmed.
- T-05 pair construction (§14 item 1): T-05 has NO separate pair files —
  the polarity-clone construction is definitional over features.tsv:
  mirrorable families = {P, O} (family idx 4, 7); the two polarity grades
  on a released P/O cell are (Y, 1−Y) — exactly one wrong, always — so
  1000·min(y_p, y_o) = 0 on EVERY released P/O training cell. Byte form
  verified via the features.tsv frozen SHA above (recovery, not rebuild —
  the pairs are byte-recoverable; §14 item 1 satisfied).
- Branch head still cab05d07 at resume (no commits landed).

## 1. Pins (recorded BEFORE first training run, per §10/§12)

- Prereg: PREREG_SR.md FROZEN v1, SHA-256
  `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
- Kill-bar table (§10, bytes `## §10 Kill-bar table` … `## §11`): SHA-256
  `c4f5dfd8723efc3c46cb57f6c9a147449bc89ce4414ff7a146745304375be1d0`
- Weight init: w1=1000, w2..w8=0, b=0, DIV2=40000, λ=2, TRW=1000, TRB=5000.
  Canonical string `WC_INIT v1 w1=1000 w2=0 w3=0 w4=0 w5=0 w6=0 w7=0 w8=0
  b=0 DIV2=40000 LAMBDA=2 TRW=1000 TRB=5000` SHA-256
  `a6c3a61faf6637ad19b97e06e4ac4ea22794b5737cc4b588c77af919041d877a`
- Pair construction (rule string above): SHA-256
  `abd6cdfbc8082de2776f1381794e76bfcec3f8424ca1ebd4b45b6ed18d0c7ebd`
- Toolchain (pinned ONLY): ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## 2. Design decisions (WC arm, PREREG_SR §6)

- **Loss:** v2 symmetric core + FINITE-λ worst-case over polarity-cloned
  pairs. On released P/O training cells (mirrorable, either polarity wrong
  — always true since grades are (Y,1−Y)): L_wc = 2·(C−0)² (λ=2 frozen,
  replaces the symmetric term there). Elsewhere: (C−Y)² alone.
  NO theater term, NO G-batch (pure per-cell form; T-05's v2 amendment
  established theater/G-batch confounded the polarity attribution — a
  global-bias suppressor could masquerade as worst-case handling; the
  task spec is "v2 symmetric core + FINITE λ=2 worst-case", implemented
  literally).
- **Optimizer (the intervention):** TRUE BATCH per epoch. Weights
  snapshotted at epoch start; every cell's C computed with the snapshot
  weights; numerators accumulate over the epoch's phase cells:
  symmetric cells add 2(C−T)·f_i (bias: 2(C−T)·1000); worst-case cells add
  4(C−T)·f_i (bias: 4(C−T)·1000) — d/dw of 2(C−T)² is 4(C−T)·f_i/1000,
  same DIV2 convention as v2. Epoch end: ONE tdiv(num, DIV2) per weight,
  trust region |Δwᵢ|≤1000, |Δb|≤5000, then v2's anti-saturation clamp
  ±2,000,000 (frozen guard, unchanged).
- **Epoch definition:** same as v2/T-05 — one phase-pass = 1 epoch;
  1 pass = 6 epochs (2 per phase, A→B→C); 10× = 60, 100× = 600.
- **Trust-region bind counting:** an epoch counts as bound-hit iff any
  pre-clamp |tdiv(num_i,DIV2)| > 1000 or |tdiv(num_b,DIV2)| > 5000.
  Logged as trbind (count of i + bias hitting the bound that epoch);
  anti-saturation clamp bindings logged separately as satbind.
- **Phases:** A={admit,revoke,logic,cost} (fi≤3), B={P,D} (fi 4–5),
  C={trap,O,redteam} (fi≥6); heldout (odd replicates) never trained.
  Same as v2/T-05 tr_phase.
- **10× go/no-go (§6):** (a) weights ≠ init; (b) meanConfCorrect ≥ 0.30;
  (c) trust-region bound hit < 50% of epochs (else reported as the story).
  Fail → stop and diagnose.
- Arenas: []u8 with au_get32/au_put32/au_get64/au_put64 accessors
  throughout; no `as []i32` casts; no slice > 2^25 bytes; no function
  named `zalloc`; slice fields via pointer indirection only (AGENTS.md).

## 3. What this arm must NOT repeat (from VERDICT_T05.md)

T-05 Arm W crushed logic correct-cell mean conf 1000→67 (D1/D2 FAIL) via
the GREEDY ONLINE optimizer dragging the shared direction per-cell —
even though the f5 separation signal existed. This arm's finite λ=2 and
batch+trust-region optimizer are the intervention; the degenerate-crush
path (large single-direction swings) is blocked by construction.
If B1–B3 violated or any guard B4–B8/B13 fails → optimizer hypothesis
for this class is KILLED (reported as: crushed / still violated /
guard-failed).
