# VERDICT — F5 correctness-aware gate (repair fork), 300-percept battery + backtest replay

Date: 2026-09-24. Arm: F5-gate crew, PAM round-2 swarm crew 3
(parent session 0c8c1318).
Prereg: `docs/lab/senses/pam-rebuild/round2/f5_gate/PREREG_F5_CORRECTNESS_GATE.md`
(prereg commit `2df95a8ad23d87b640a110c3c2666b747f524037`, committed ALONE
before any code, 2026-09-24).

## Measured result

| Bar | Rule | Measured | Outcome |
|-----|------|----------|---------|
| (a) Delay bar | ≤ 25% of the 300 delayed > 50 trials (primary model) | **0/300 = 0%** | **PASS** |
| (b) Far-control bar | 0/60 far controls blocked | **0/60** | PASS |
| (c) Over-block report | blocked / 300 NEAR (baseline 110/300 = 36.7%) | **7/300 = 2.3%** | reported |
| (d) Backtest retention | ≥ 8/9 false accepts blocked (replay) | **8/9** | PASS |

**Verdict: SURVIVE.** Go for the F5 live-gate build on predicate + gate,
with the documented residual risk (§"Reading the SURVIVE honestly").

## Detail (frozen gate + frozen predicate, pure Zag, 3 byte-identical runs per mode)

Gate (frozen §3): BLOCK ⟺ trap_fires ∧ gate_fails, where gate_fails ⟺
(conf, meas) ∈ Box A ∪ Box B —
Box A (exemplar wrongness): conf [701,718] × meas [2618,2647];
Box B (backtest-false wrongness): conf [764,832] × meas [1888,2373].

**Mode rt300** — 360 frozen fixtures (`fixtures_ledger.txt`, SHA
`0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`;
bank = 6 frozen exemplars, SHA
`13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`):
- NEAR: **7/300 BLOCKED** (conf {770,…,830} × meas {2200} — Box B;
  Box A contains zero grid points), **0 delayed > 50**.
- FAR: **0/60 BLOCKED**.
- Delay histogram: `0:293 | 1–3:1 | 4–10:2 | 11–50:4 | 51–100:0 |
  101–300:0 | 301+:0` (delays 3, 6, …, 21).
- S1 (15k): 4 delayed > 50. S2: 0.
- All numbers reproduce the preregistered §8 sanity expectations exactly.

**Mode backtest** — replay over the 43 `DISP=ACCEPT_INSTALL` lines of the
frozen `v2/redteam/evidence/ledger_d_withhold.txt`
(SHA `63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1`):
- FALSE: **8/9 blocked** — all 8 `rt4_TMB-5_*` RICH/DARK in Box B;
  `rt4_COL-4_0000` (DIFFERENT/SAME) ALLOWED, same as the backtest (family
  stem never matched; no box was drawn for a single point).
- TRUE: **0/34 blocked** — the 6 true TMB-5 (conf 869–952, meas 4000–6000)
  sit outside both boxes; all other trues outside the trap's stem rule.

**Mode exemplars** — the 6 bank rows re-fed as candidates: **6/6 BLOCKED**
(Box A; exact exemplar repeats still block — mechanism sanity holds).

## Determinism

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Binary `f5_gate` built from `f5_gate.zag` (+ byte-identical copy of
  `R33_NATIVE_IO_V1.zag`, SHA
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`);
  binary NOT committed (build artifact; reproducible from source).
- Three runs per mode, stdout SHA-256 byte-identical:
  - rt300: `b859e6656928102e88f5e74af50527cd10224287313b071f81a41f1f656d7822`
  - backtest: `426609f54e5a41f6357da2d84512b45468876c78913b287a2b05a0b47d525e9e`
  - exemplars: `1c02a861481d9d89d21452f68b25c9042c844dd21a648ccc5a3ab45da4a15d02`
- Zero RNG.

## Reading the SURVIVE honestly

Three facts, kept separate:

1. **The gate works on the frozen battery because the observed wrongness
   has a stable, tight signature.** 14 documented wrong RICHs (6
   exemplars + 8 backtest falses) occupy two small boxes; 293/300
   synthetic corrects and 34/34 real trues lie outside them. The
   conjunction cuts over-block 36.7% → 2.3% and delay 31.3% → 0% while
   keeping every recall the trap ever had (8/9 falses, 6/6 exemplar
   repeats, 0/34 true-blocks).
2. **On these fixtures the gate does the discriminating work.** Both
   fail-boxes lie strictly inside the trap's wide window, so the block
   decision equals the signature boxes; the wide window is retained only
   as the suspicion region for the unbuilt confirmation machinery. This
   was stated in the prereg (§5), not discovered after the fact.
3. **The SURVIVE is scoped, and the scope is the residual risk.** The
   gate withholds the block where no wrongness precedent exists. A NOVEL
   wrong percept inside the wide window but outside the two boxes will
   NOT be blocked — trap-alone would have blocked it. This is the
   deliberate price of the over-block cut (prereg §4.5, §5). Against an
   adaptive byte-spoofer the whole F5 mechanism was already bypassable;
   the gate adds no new vulnerability class. If the error signature
   drifts, the boxes must be re-derived under a new prereg — the 7/300
   must never be "improved" by silent re-tuning.

## Go / no-go for the F5 live-gate build

**GO, on predicate + gate as frozen here,** with the §4.5 residual risk
carried as a documented limitation: the live gate must log every
gate-pass inside the trap window (suspicion without block) so novel
wrongness is visible and the boxes can be re-derived under a new prereg
if the signature drifts. The unbuilt three-re-inspection confirmation
path remains the backstop for novel error modes.

## Caveats (frozen in the prereg, not post-hoc)

- `measure` substitution carried exactly as the backtest/red-team (raw
  task quantity, not the classification margin mrgF); a true-margin
  replay remains the documented upgrade path.
- The delay numbers rest on the preregistered queue-model assumption
  about the unbuilt confirmation machinery (same as the red-team).
- The 300-grid measures signature-box occupancy over the anchored region;
  no real-world over-block frequency claim is made.
- The gate never certifies correctness: "gate passes" = "no documented
  wrongness precedent at these coordinates," explicitly not "correct."
