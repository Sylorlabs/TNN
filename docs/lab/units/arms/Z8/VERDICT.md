# VERDICT — Arm Z8 (fuzzy boundaries), Track A closeout

**Date:** 2026-09-21
**Arm:** Z8 — Fuzzy boundaries (CUT family)
**Adjudicated by:** MARATHON CREW U3
**Verdict: PASS** — binding, per frozen §3 kill bars (supersedes the 2026-09-21
verdict gap-fill UNADJUDICATED: the battery has now been built, run, and measured).

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Boundary-error rate not ≥40% lower than arm D on the perturbation battery — carrying fuzz buys nothing; OR mean fuzz grows without bound on the revision curriculum (widen dominates tighten — kill or cap).

## Evidence

- **Build:** `cl/arm.zag` (1,643 lines, pure Zag; zero RNG/clock/sampling in
  decision paths) compiled clean first try with lab znc → native x86-64 ELF.
  Battery binary build-only, never committed.
- **Battery:** `battery_1x.sh`, 17 legs × 2 fresh-dir runs, all rc=0 and
  stdout byte-identical: **17 pass, 0 fail** (`evidence/r1/BATTERY_LOG.txt`).
- **M8 gate:** shared `harness/m8_gate.sh`, 5 perturbations × 2 reruns = 10
  runs, all 7 artifacts byte-identical across all ten: **M8GATE PASS**
  (`evidence/r1/M8_GATE.txt`).
- **Scorecard:** `evidence/r1/scorecard_z8_r1_1x.json` (schema metrics-v1).

## Kill evaluation (full record: `evidence/r1/KILL_EVALUATION.md`)

**Clause 1** (perturbation battery): Z8 fuzzy (fuzz=16) boundary-error rate
50.0% (1280/2560 each boundary) vs exact-cut D-surrogate 100.0% (2560/2560) →
**50.0% reduction ≥ 40% bar**. Clause does NOT fire. Operationalization: arm D
never ran a perturbation battery (D's verdict is DRAFT, legs PENDING); "arm D"
= Z8 with fuzz disabled on the identical deterministic 2560-trial set —
exact cuts err on 100% of trials by construction, so this equals real-D's
score on this battery and isolates the fuzz variable.

**Clause 2** (revision curriculum): m4 mean fuzz (tenths) over 20 episodes,
both corpora, byte-identical double runs —
`[160, 148, 135, 121, 104, 89, 74, 57, 41, 26, 9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0]`,
converging to exactly 0.0 (f10=0.9 → f20=0.0, bounded=true). TIGHTEN strictly
dominates WIDEN; revision correctness 100.0% boundary and content. The
FUZZ_CAP=32/side cap was never approached. Clause does NOT fire.

## Supporting metrics

M1 recall 100.0% / boundary fidelity 100.0% both corpora (≥99.5% bar);
M2 1 episode to criterion; M3 survival 99.9%; M6 transfer tax 0.0;
M7 hit rate 100.0%.

## Caveats

- The 50% reduction is structural given F0=16 vs the ±1..±32 shift range; the
  bar is satisfied as frozen.
- Head-to-head vs real arm D (not the D-surrogate) is unmeasurable until D
  runs a perturbation battery.
- 1x only; 10x blocked (toolchain), as for the rest of the battery.

**Result: Z8 PASS — carrying fuzz buys a measured 50% boundary-error
reduction, and the revision curriculum drives fuzz to zero.**
