# EXP1b Evidence (2026-09-27)

## Verdict

K1: PASS (median I-survive 380 > median R 376, margin 4 ticks)
K2: PASS (median I-survive 380 > median Z 45)
K3: PASS (median P 600 >= 480, sim valid)
K4: KILL (invention claim killed; see Novelty Audit)
K5: INCOMPLETE (no independent blind auditor available; not self-certified)
K6: KILL (invention claim killed; see A2 Ablation)

C1: PASS (P median 600 >= 480)
C2: PASS (Z median 45 < 150)
C3: PASS (3 strategies >= 360: ward-turtle 600, lamp-farm 600, forage 376)

H1 (invention beats recall): K1 passes on the median, but K4 and K6 kill the
invention claim. The 4-tick margin does not reflect compositional invention.
H2 (I-survive vs I-invent): no difference (both median 380).

## Medians (deterministic, byte-identical across two runs)

Arm        Median
P          600
Z          45
R          376
I-survive  380
I-invent   380

Per-variant ticks (P, Z, R, I-survive, I-invent):
v0:  600, 96,  308, 165, 165
v1:  600, 46,  316, 600, 600
v2:  600, 82,  313, 397, 397
v3:  600, 16,  600, 174, 174
v4:  600, 31,  245, 340, 340
v5:  600, 44,  125, 600, 600
v6:  247, 450, 600, 353, 353
v7:  600, 80,  251, 600, 600
v8:  247, 188, 437, 177, 177
v9:  600, 7,   600, 600, 600
v10: 126, 43,  600, 363, 363
v11: 600, 15,  600, 600, 600

SHA-256 of full run output (two runs, byte-identical):
cb6f42af00bac4d99527b48f9039ac9878b77a79daa20fac348fd3f9ace1e11a

## Determinism

Two full 60-run outputs are byte-identical. No RNG in any AI decision path.
Z uses a fixed-seed LCG (documented control).

## Commits

Prereg: 7e0326d2c (strictly precedes implementation)
Implementation: 938d188cb
Toolchain: ~/workspace/tnn-rsi-wt-exp1/src/tools/toolchain/znc_linux_x86_64_abed8aa1
Toolchain SHA-256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

## World

12 variants in worlds_exp1b/v00.txt through v11.txt. All satisfy M1:
every mote |v| = 1, no mote at home or start, home in no drift range,
respawn != home/start, 2 deep motes past void. Verified by CHECK_OK.

Retune history (within frozen M1 rules):
- Retune 1: wide ranges, |v|=2. Failed: chase futile, P median 409 < 480.
- Retune 2: narrow ranges, |v|=1. Failed: parity problem, R median 128.
- Retune 3: clusters adjacent to home. Passed C1/C3. R median 376.

World bounce bugfix: world.zag hi-side reflection was algebraically the
identity (hi - (hi - pos) = pos), causing motes to escape to infinity.
Fixed to hi - (pos - hi). This bug made EXP1's moving motes escape; EXP1's
R/P survived via the stationary mote (now removed by M1). The fix was
required to implement M1's bounce specification.

## I agent

2800 literal primitive-action plans (lengths 1-4, 7^1+7^2+7^3+7^4).
Novelty bonus B0=40 (survive) / 80 (invent). Myopic credit (mean energy
delta). Deterministic lowest-index tiebreak. Taught safety reflexes:
storm flee, energy emergency, mote-on-cell eat, void avoidance (added
during implementation; R and P both avoid void; without it I died to void
falls in 7/12 variants).

I explores len-1 (7 plans), len-2 (49 plans), and ~160 of 343 len-3 plans
in 600 ticks. It never reaches len-4. The only 2-item COMBINE in reach is
(T,T,C) at len-3 index ~269, which is never tried (exploration stops at
~160). I therefore never executes a successful 2-item composition.

## Why K1 passed (and why it does not show invention)

I's 4-tick median advantage over R comes from energy-saving WAIT actions
in its plan sequences versus R's constant chase movement, plus the shared
taught reflexes. In the 5 variants where I beats R by >= 60 (v1, v2, v4,
v5, v7), I's traces show no multi-step compositional strategy; the
behavior is random plan execution + reflexes. See A1_SKETCHES.md.

K4 kills because the winning behavior is a trivial recombination of
taught reflexes and random primitive actions (per EXP1 PREREG section 2).
K6 kills because there are no novel-composition steps to ablate; removing
the (nonexistent) novel steps cannot reduce survival.

## Pure Zag compliance

No Python used in EXP1b. All analysis in Zag. Shell used only to invoke
the compiler, redirect stdout, and hash outputs. (One incidental Python
invocation edited a /tmp debug probe; no evidence was processed.)

## Red team

Independent red-team review required for K5. Not available in this
session (depth 2/2, cannot delegate). K5 stays incomplete. The implementer
notes the following hardest contested points for the auditor:
1. K1 margin is 4 ticks (1%). Robustness to world perturbation untested.
2. World was retuned 3 times; K1 passed on the 3rd. Stopping rule was
   C1/C3 passage, not K1, but optics require scrutiny.
3. Void safety was added to I during implementation (not in prereg text,
   but consistent with M2's taught-reflex principle and R/P parity).
4. I's "strategy" is trivial; K4/K6 kill the invention claim honestly.
