# H2 Adaptive-Liar Co-evolution Battery: Results

**Date:** 2026-09-24
**Branch:** `tnn-native-lab`
**Prereg:** `build/PREREG.md` (frozen), amendments 1 (pure-Zag) and 2 (C-noise field)

## Headline

[To be filled after full battery]

## Meta-controls (frozen §10, pure-Zag control.zag)

| Control | Bar | Result |
|---------|-----|--------|
| C-static (4 arch × 6) | F flat (±0), genome identical | PASS (4/4, pure-Zag control.zag) |
| C-noise (4 arch × 6) | F flat, genome = f(CAL_SCORE) only | PASS (4/4, pure-Zag control.zag) |
| C-honest (5 var × 6) | all SURVIVE | PASS (5/5, pure-Zag control.zag) |
| C-max (5 var × 6) | all KILLED | PASS (5/5, pure-Zag control.zag) |

## Channel audit (D3–D6)

| Test | Result |
|------|--------|
| D3 stdin/argv-only (static) | PASS: teacher.zag uses only `_zag_raw_syscall(0,...)` (stdin read) and `_zag_print` (stdout); no file opens |
| D4 decoy test | PASS: teacher output identical with/without decoy file |
| D5 SHA256 binding | PASS: teacher echoes latest SHA256 as SEEN_SHA |
| D6 frozen fixture | PASS: 4/4 arch outputs match EXPECTED.md |

## Meta-red-team

| Test | Result |
|------|--------|
| M5 weakened teacher | PASS: forgetful A1 scores 1/6 vs frozen (full A1: 4/6) |

## Cell verdicts (5 variants × 4 architectures)

[Frozen §6: KILL if ≥2 phase-2 wins OR round-6 win. Round-7 honest cost can invalidate SURVIVE.]

| Variant | A1 | A2 | A3 | A4 |
|---------|----|----|----|----|
| default | [pending] | [pending] | [pending] | [pending] |
| a2 | [pending] | [pending] | [pending] | [pending] |
| a3 | [pending] | [pending] | [pending] | [pending] |
| b1 | [pending] | [pending] | [pending] | [pending] |
| f3 | [pending] | [pending] | [pending] | [pending] |

## Ablation arms

[Parameter-only and frozen-learner control results]

## Honest cost (round 7)

[Results]

## Determinism (KB-DET)

[Two-run cmp results]

## Limitations

[To be filled]

## Commits

[List of commit SHAs]
