# VERDICT R2-11 — replay vs generative emission head-to-head

**Date:** 2026-09-23. **Seed:** 20260923. **Status:** FROZEN.

## Headline

**Both forks FAIL B5 (false permanent installs ≤ 3%) and are KILLED per §5.1.**
The shared percept pipeline — identical in both forks — confidently misjudges
two adversarial families, producing false installs at ~4% (already 397 with
the battery incomplete; the 3% bar allows at most 300). The replay-vs-generative
question is not resolved: the percept failed before the emission choice mattered.

## Bar table

| Bar | Fork A (replay) | Fork B (generative) | Verdict |
|-----|-----------------|---------------------|---------|
| B1 primary ≥60% | 368/370 = 99.46% | 368/370 = 99.46% (shared) | PASS both |
| B2 head-to-head Δ | — | accuracy Δ = 0 (shared percept); emission: exact vs divergent | reported |
| B3 ops / bytes | 10k: 2.56B ops (256k/trial); primary: 91.7M (248k/trial) | 10k: 2.33B ops (233k/trial); primary: 82.9M (224k/trial); same payload bytes | reported |
| B4 no-interference | 0/10,000 differ (on vs off) | 0/10,000 differ (on vs off) | PASS both |
| B5 ≤3% false installs | **415/10k = 4.15% FAIL** | **415/10k = 4.15% FAIL** | **KILL both (§5.1)** |
| B6 ≥3 runs byte-identical + ledger | 3/3 TSVs identical; 4 ledgers verified (10k lines, 0 problems) | 3/3 TSVs identical; 4 ledgers verified (10k lines, 0 problems) | PASS both |
| KB-E1 | PASS (equal=1, all 10,000) | FAIL by design (scored, not excused) | — |
| KB-E2 | PASS (0 bad, 0 phantom) | PASS (0 bad, 0 phantom) | PASS both |
| KB-E7 | n/a (zero divergence) | declarations frozen in briefs | — |
| B7/KB-E3/E4/E8 human | package prepared, pending | package prepared, pending | — |

## B5 kill analysis (the load-bearing result)

False installs = disposition INSTALL (confidence ≥ 600) with judgment ≠ truth.
Counted over the exact 10,000-trial scoring set. **Both forks: 415/10,000 =
4.15% — the 3% bar allows at most 300. FAILED.**

| Family | Mechanism | Failure mode | False installs |
|--------|-----------|--------------|----------------|
| COL-2 illuminant-drift (400) | T1 RGB-distance | Same surface under shifted illuminant judged DIFFERENT, conf ~900+ | ~350 (87.5%) |
| SHP-1 occlusion-bar | T3 area-ratio | Occluded circle/square judged TRIANGLE | ~44 |
| Normal (4000) | — | — | 3 |

COL-2 alone contributes ~3.5% — the bar was already failed by this family.
The T1 colordisc mechanism has no illuminant constancy: it cannot distinguish
"different surface" from "same surface, different light", and its confidence
function (distance from the d2=40 boundary) is maximally confident precisely
where the RGB distance is largest — i.e., on the strongest illuminant shifts.
The T3 shapetrans mechanism's area-ratio anchors assume unoccluded silhouettes.

This is the same disease that killed the PAM round-1 forks: confident
installation of spoofed percepts. The emission fork (replay vs generative) is
irrelevant to B5 — both forks share the percept and die together.

## B2/B3 head-to-head (recorded, moot for survival)

- Accuracy: identical (shared percept, 0 diffs over 7,130 overlapping trials).
- KB-E1: Fork A equal=1 on every emission (3 runs). Fork B diverges by design;
  mean ~19.3k divergent bytes per percept, declared per brief (KB-E7).
- Ops: Fork B pays the renderer cost (final numbers pending run completion).
- Bytes/percept: identical by construction (same payload dimensions).

## What was built (frozen)

- `src/`: gen_r2a.py, gen_tables.py, derive_b.py, build_lists.py,
  build_human.py, calib.py, score_r2a.py, verify_ledger.py
- `zag/`: common, percept, emit, render, tables, main_a, main_b (+generated)
- `lists/`: scoring_10000.txt, human_200.txt, STRATIFICATION.md
- `battery/r2a/`: 3× emit-on + 1× off TSVs and hash-chained ledgers per fork
- `human_pkg/`: 200 double-blind trials (P/Q artifacts + briefs + gates +
  verdict form), sealed key withheld from judge
- `fixtures/`: generator + MANIFEST.sha256 (454 MB of bytes not committed)

## Human package status

**PREPARED, NOT DELIVERED.** 200 trials, blind P/Q, briefs with declared
divergences, gate report (13 flags investigated and cleared). The forks are
dead on B5; the human trial is not required for this verdict. The package is
held for the parent's decision.

## Lessons

1. A shared percept means a shared fate: B5 killed the comparison, not a fork.
2. Confidence must be calibrated against the ADVERSARIAL set, not just the
   clean primary (0 false installs on 370 clean; ~4% on 10,000 mixed).
3. The T1/T3 mechanisms need constancy/occlusion handling before any emission
   fork can survive B5 — that is the next build, not a tuning fix.
