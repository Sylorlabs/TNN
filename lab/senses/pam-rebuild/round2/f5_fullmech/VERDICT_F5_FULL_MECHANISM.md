# VERDICT — F5 full mechanism: predicate + fast confirmation machinery

Date: 2026-09-24. Arm: F5 confirmation crew (Crew 4, subagent session
1f9bd76d, hypothesis H-PAM-3).
Prereg: `docs/lab/senses/pam-rebuild/round2/f5_fullmech/PREREG_F5_FULL_MECHANISM.md`
(prereg commit `d156a60a38417c64070138fbe306bd43b67c8f59`, committed alone
before any code, 2026-09-24).

## Measured result

| Bar | Rule | Measured | Outcome |
|-----|------|----------|---------|
| (a) Delay bar (REAL mechanism) | ≤ 25% of the 300 delayed > 50 trials (installed delay>50, or withheld) | **60/300 = 20.0%** | **PASS** |
| (b) Far-control bar | 0/60 far controls blocked | **0/60** | **PASS** |
| (c) Backtest retention | 8 blocked false accepts still withheld; 0/34 true blocked | **8/8 withheld** (9th escapes predicate by design); **0 true blocked** | **PASS** |
| (d) Confirm-install rate (reported) | — (no frozen threshold) | **50/110 = 45.5%** of blocked-corrects confirmed-and-installed | — |

**Verdict: SURVIVE.** The full mechanism passes all three frozen bars where
the predicate alone was KILLED (red-team: 94/300 = 31.3% delayed > 50 under
the queue model).

## Detail (pure Zag, 3 byte-identical runs per battery)

- Battery: 360 fixture trials (`fixtures_ledger.txt`, SHA re-verified
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`):
  300 NEAR (TMB-5, RICH/RICH, conf 650–940 × measure 2200–6700) + 60 FAR
  (20 COL + 20 TMB-outside-windows + 20 PTC), all truth-correct, all
  `DISP=ACCEPT_INSTALL`. Zero CORRUPT lines (judgment == truth asserted on
  every battery line).
- Bank = the 6 frozen exemplars (`exemplars.tsv`, SHA
  `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`).
- NEAR: **110/300 BLOCKED** by the frozen predicate (reproduces the
  red-team count exactly), then confirmation: **50 CONFIRM+INSTALL**
  (delay 3 trials each), **60 WITHHOLD** (terminal, delay ∞).
- FAR: **0/60 BLOCKED** — predicate unchanged, confirmation never engaged.
- Delay histogram (real mechanism, NEAR):
  `0:190 | 1–3:50 | 4–10:0 | 11–50:0 | 51–100:0 | 101–300:0 | 301+:0 |
  WITHHELD:60`.
- Sensitivity S-serial (1 re-inspection/trial globally, FIFO — reported, not
  the verdict): 104/300 delayed > 50. Under-provisioned deliberation
  re-fires the bar; the verdict rests on the preregistered provisioned fast
  path. Independently cross-checked in Python from the per-trial lines:
  confirmed=50, withheld=60, delay-bar=60/300, serial=104 — exact match.
- Backtest replay (43 candidates, same binary): 8 TMB-5 false accepts
  BLOCKED → all 8 WITHHELD by confirmation (≥2/3 crops reproduce the false
  signature in every case); COL-4 false escapes the predicate by design
  (family rule); 0/34 true accepts blocked.

## Determinism

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Binary `f5_full` built from `f5_full.zag` (+ byte-identical copy of
  `R33_NATIVE_IO_V1.zag`, SHA
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
- Battery stdout SHA-256:
  `d287b4ee67ca546ff4433fe245ad36fbd19f577b432939a15ef0d9ed13b78327`
  (run1.out = run2.out = run3.out, byte-identical). Zero RNG.
- Backtest-replay stdout SHA-256:
  `5c9eea9d8f5dbb84ea95d9c4b7ee9255ac355f95828bcb08ae41729a02a8b93f`
  (bt1.out = bt2.out = bt3.out, byte-identical).
- The binary self-checks the frozen prereg §4 expectations
  (110/50/60, 0/60 far, 8/1/0 backtest) and fails loud (rc=13) on mismatch:
  all six runs printed `SANITY OK`, rc=0.

## Truth firewall (code-reviewed)

The decision path (`f5_block` → temporal crops → `core_hit` → quorum)
receives only (family stem, conf, measure). The truth field is parsed after
the decision, solely for scoring counters and the battery's
judgment==truth construction assert. No decision-path function takes a
truth argument. The mechanism never peeks.

## Reading the SURVIVE honestly

What changed vs the KILL: the red-team's delay numbers rested on a queue
model of unbuilt machinery (1 re-inspection/trial globally → delay 3k).
The built machinery provisions the fast confirmation path (3 parallel
re-inspections, 3-trial latency), so every confirmed percept installs at
delay 3, and the delay bar becomes a joint test of speed and precision:
60/300 = 20.0% ≤ 25% → PASS.

What did NOT change: the predicate still over-blocks (110/300 = 36.7%
window occupancy — the red-team's predicate-level fact stands). The
confirmation recovers 50 of the 110 (45.5%) and withholds 60 (20.0% of the
300). The 60 withheld are the documented residual:

- 7 withheld percepts sit exactly inside the known-false bounding
  rectangle (conf 770–830 × measure 2200) — geometrically
  indistinguishable from the 8 frozen false accepts on the mechanism's
  only axes. No deterministic (conf, measure)-only mechanism can separate
  them without truth-peeking; withholding them is the honest price of
  keeping the 8 falses out.
- The other 53 are inside the jitter-expanded confirmation core
  (Tc=130, Tm=950) but outside the exact false rectangle — the margin cost
  of covering the false cluster.

The confirmation core was derived from the 8 frozen false accepts only
(max Δconf=114, max Δmeas=730, + crop jitter, ceiled to 130/950) — the
110's geometry was never consulted. The 20.0% vs the 25% bar is the
mechanism's measured outcome, not a tuned one.

## Caveats (frozen in the prereg, not post-hoc)

- Synthetic crops re-derive only (conf, measure); judgment re-derivation
  from real sense traces is future work (§3a limitation).
- `measure` substitution carried exactly as the backtest (NOT the margin
  mrgF); true-margin replay remains the documented upgrade path.
- The 300-grid measures window occupancy over the anchored region; no
  real-world over-block frequency claim is made.
- S-serial shows the mechanism needs provisioned deliberation bandwidth:
  under the red-team's scarcity model the bar re-fires (104/300).

## Salvageability reading (bar (d))

The trap IS salvageable as predicate + fast confirmation: all frozen bars
pass, the 8 known false accepts stay out, and nearly half the over-blocked
correct percepts are recovered within 3 trials. The residual is 20% of
near-exemplar correct percepts withheld — concentrated where correct
percepts are geometrically coincident with known false accepts. Whether
that residual is acceptable for a live gate is a governance call (Micah's
word per standing governance); the mechanism question this battery was
asked is answered: SURVIVE.
