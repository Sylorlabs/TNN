# POSITION 2 — Detection can win the race

A5's hole is timing-and-cover: the kill path (≤4 eps) outran detection (≥5 eps) because detection waited on a unilateral signal while the gate admitted the attack. Fix the clock and the signal; detection fires at ~astart+1.

## 1. M: 5 → 3

`CHANNEL_DISTRUSTED` at **M = 3 consecutive** source-vs-T0 disagreements; §5.4 re-distrust follows.

Evidence: A4 — 72/72 revised, zero distrusts (T0∥T1 agree in genuine shifts; nothing genuine to catch; latency 3.0 untouched). A2 — only distrusts were spoofed channels; M=3 moves `distrust_ep` from `astart+4` to `astart+2`, inside the kill path. N0 — 0/36 spontaneous flags. A0 caveat: M=3 distrusts honest T1 at astart+2 under T0 spoof — LOUD, measurement-only. Gap: re-trial needs a staggered-flip genuine campaign (no sensor-lag treatment exists).

## 2. Redesign the COLLUSION_SUSPECT agreement rule

Defect: blind while a *counted* {T0,T1} citation agrees with the colluders — in A5 the spoofed T1 is counted from `astart` until distrust. Cover by construction.

**RULE 2':** suspicion evaluates **all** {T0,T1} citations. When ≥2 distinct T2/T3 sources agree on a contradicted value within W: (a) no {T0,T1} citation on it → `COLLUSION_SUSPECT` (as now); (b) some {T0,T1} citation on it **and T0 contradicts T1** → `COLLUSION_SUSPECT`, severity HIGH, naming the split (the A5 signature — heightens suspicion, never grants cover); (c) some {T0,T1} citation on it **and T0 ∥ T1 agree** → no suspicion (the A4 case).

Effects: A5 — suspect at ~astart+1, freeze before `rev_ep`. A4 — consensus bypasses it. A3 — unchanged. N0-target2 — fires as today (bar-scope, A.7).

## 3. Quorum-composition tripwire

**Rule:** any episode with a {T0,T1} contradiction citation **and** a T2/T3 contradiction citation on the same memory, **while T0's reading contradicts T1's citation** → `GATE_SPLIT_TRIPWIRE`, freeze kill/revision for the window, escalate.

**False-positive analysis (A.7):** the A.7 pathology (100% flagged on N0-target2) lives in the *no-{T0,T1}-presence* domain, which this tripwire never enters — disjoint domains. Background same-memory T0/T1 splits were **0 everywhere** in genuine cells (N0 main 0/36; splits only in A2/A5/A0). Threshold sits on an observed zero.

## 4. Harness fixes

- **A.5:** emit `rev_ep` and audit episodes (ledger logical clock on kill ops and detection audits).
- **A.3:** reset the L freeze clock **only** on a *contradiction citation by a named source toward the frozen memory*. Predicted: A1-MS freeze duty 0.904 → ~0.1; SRR stays 100%.

## Predicted effects

A5 (arm T): 36/36 HELD, DEGRADED-GRACEFUL, **LOUD**. A1/A1-MS: 100% SRR. A3: FCR 0%. A2: CONTAINED, distrust at astart+2. A4/N0-target: 36/36 genuine revised, latency 3.0. A6: HOLD. A0: LOUD, measurement only. §8: SRR → ~100%; silent corruption → 0; denial stays 0%. BLIND / genuine-flagged still fail literally — needs the dated amendment scoping those bars (A.2/A.7), not mechanism. **No-rescue:** every change makes the attacker's path strictly harder; the genuine path untouched.

## Red-team objection

*"Detection will always lag; faster thresholds just move false positives around."* — This redesign changes *what the signal is*: the required leg forces one high-tier citation from the attacker, and honest-by-construction T0 necessarily disagrees with it. The spoofed citation *is* the tripwire — a structural bind, not a threshold race. The A.7 pathology lives in the no-high-tier domain the new rules never touch; the tripwire threshold sits on an observed background of zero. The adaptive ladder terminates: drop the spoofed high-tier leg and the attack becomes A3, defeated at FCR 0%. Boundary: the bind holds only while T0 is honest-by-construction; under T0 spoof it inverts — A0 measures loudness, not immunity.

## Verdict

**REDESIGN → re-trial** of the amended mechanism (RULE 2', split tripwire, M=3, A.3/A.5 fixes) plus the dated §8 amendment scoping those bars. **Do not retire:** timing-and-cover defect, structurally fixable. If re-trial A5 cells corrupt again, the hole is fundamental and trust tiers retire per §8.
