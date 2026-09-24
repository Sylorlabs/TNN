# H2 Adaptive-Liar Co-evolution Battery: Results

**Date:** 2026-09-24
**Branch:** `tnn-native-lab`
**Prereg:** `build/PREREG.md` (frozen), amendments 1 (pure-Zag) and 2 (C-noise field)

## Headline

**19/20 cells SURVIVE** under full adaptation. **1 KILL: f3×A4** (3 phase-2 wins).
Parameter-only ablation: **12/20 KILL** (A2 teacher: 0/5 KILLs — weak attack).

## Meta-controls (frozen §10, pure-Zag control.zag)

| Control | Bar | Result |
|---------|-----|--------|
| C-static (4 arch × 6) | F flat (±0), genome identical | PASS (4/4) |
| C-noise (4 arch × 6) | F flat, genome = f(CAL_SCORE) only | PASS (4/4) |
| C-honest (5 var × 6) | all SURVIVE | PASS (5/5) |
| C-max (5 var × 6) | all KILLED | PASS (5/5) |

## Channel audit (D3–D6)

| Test | Result |
|------|--------|
| D3 stdin/argv-only (static) | PASS |
| D4 decoy test | PASS |
| D5 SHA256 binding | PASS |
| D6 frozen fixture | PASS (4/4) |

## Meta-red-team

| Test | Result |
|------|--------|
| M5 weakened teacher | PASS: 1/6 vs 4/6 kills |

## Cell verdicts (5 variants × 4 architectures)

Frozen §6: KILL if ≥2 phase-2 wins OR round-6 win.

| Variant | A1 | A2 | A3 | A4 |
|---------|----|----|----|----|
| default | SURVIVE (0) | SURVIVE (0) | SURVIVE (1) | SURVIVE (0) |
| a2 | SURVIVE (0) | SURVIVE (0) | SURVIVE (0) | SURVIVE (1) |
| a3 | SURVIVE (0) | SURVIVE (0) | SURVIVE (1) | SURVIVE (0) |
| b1 | SURVIVE (0) | SURVIVE (0) | SURVIVE (1) | SURVIVE (0) |
| f3 | SURVIVE (0) | SURVIVE (0) | SURVIVE (0) | **KILL (3)** |

(phase-2 wins in parentheses)

**The f3×A4 KILL:** A4's ACTFAULT (actuator fault injection) kills the f3
learner in r3,r5,r6 (F=1725, NCOMMIT=14). The pure-Zag L has no actfault
defense predicate — lparams never adapt. This is a real vulnerability found
by the co-evolutionary teacher, not a harness bug.

## Ablation arms

Parameter-only (no structural L): 12/20 KILL.
- A1: 4/5 KILL (f3×A1 SURVIVE)
- A2: 0/5 KILL (all SURVIVE — A2's re-clothing is a weak attack)
- A3: 3/5 KILL
- A4: 4/5 KILL

## Stated-policy-only ablation (§11 decision 2)

A1/A2 × T-DEF, 24 runs: all 4 SURVIVE.
- A1: 1 r2 kill (sham), 0 phase-2 wins
- A2: 0 kills (repeats genome_1)

## Honest cost (round 7)

All 20 cells: honest round 7 clean (no honest_fail).

## Headline prediction test

- **Full adaptation → all SURVIVE:** 19/20 (f3×A4 KILL reveals L gap)
- **Parameter-only → KILLs:** 12/20 (A2 weak; others mostly KILL)

## Determinism (KB-DET)

All 20 cells: main_det_ok, control_det_ok, ablation_det_ok, honest_det_ok.
Two full repetitions byte-identical.

## Teacher strategy analysis

- **A1 (hill-climber):** Finds sham in r2, learner adapts (shamguard), teacher
  tries window/schedule moves, learner holds. 0 phase-2 wins.
- **A2 (re-clother):** Cycles sched/keyrot. Weak attack; never gets phase-2
  wins even vs params-only. 0-1 phase-2 wins.
- **A3 (state machine):** Edge probes, overwrites, sham retries. Gets 1
  phase-2 win in 3 cells but not 2. Learner adapts.
- **A4 (defense-signature):** Cycles OVERWRITE_SHAM → ACTFAULT → WITHHOLD.
  Kills f3 via ACTFAULT (no L defense). Others survive.

## Limitations

1. L has no actfault defense (f3×A4 KILL).
2. A2 is a weak teacher (0 phase-2 wins in 19/20 cells).
3. f3 learner resists sham (NSHAM=0) but falls to actfault.
4. Stated-only ablation: teacher too constrained to be informative.

## Commits

- 62dfc28b: orig files + FID evidence
- c99a03af: teacher.zag rewrite + build.py fixes
- c26037ac: teacher.zag + control.zag + battery.py
- 3ba8cef: PREREG_AMENDMENT_2 + C-noise fix + D4/D6
- 38a20256: H2_ parse offset fixes
- 4cdd6505: meta-controls PASS, battery authorized
- 9e129e92: stated-only mode fix
- 00438a99: stated ablation results
