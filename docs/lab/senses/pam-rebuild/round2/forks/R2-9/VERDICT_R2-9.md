# VERDICT R2-9 — Witness-Emission PAM

**Fork:** R2-9 (C-EC1) — Witness-Emission PAM, replay-only selection-emitting percept pipeline.
**Status:** MECHANICAL PASS on 370; 10,000-trial battery PENDING (fixture generation in progress)
**Date:** 2026-09-23

## 1. What was built

Pure-Zag `sense` CLI (`forks/R2-9/src/r29.zag`, built with pinned `znc_linux_x86_64_abed8aa1`):
- Six task percept front-ends (colordisc ΔE76, colorconst linear-map residual, shapetrans radial-profile, pitchdisc autocorrelation f0, timbredisc Goertzel centroid, motiondir SAD candidate match), each emitting a judgment, confidence, install/withhold disposition, and 1–2 emission selections (exact audio byte spans / pixel rects / video regions).
- A read-only replay emitter: artifacts are verbatim copies of cited source bytes. The emission pass runs after the percept pipeline and cannot influence it.
- Hash-chained ledger (SHA-256) over per-trial entries; batch mode writes `percepts.tsv` + `LEDGER.jsonl` + `artifacts/`.
- Zero RNG in decision paths; deterministic given fixture bytes.

## 2. Deciding bar

**B1 (viability):** PASS — 86.22% ≥ 60% threshold.
**B4/KB-E5 (no-interference HARD KILL):** PASS on 370 — emit/noemit percepts byte-identical.
**B6 (determinism HARD KILL):** PASS on 370 — three byte-identical runs, hash chain verified.
**KB-E1 (byte-identity):** PASS on 370 — 530 artifacts byte-identical to source.
**KB-E2 (no phantom):** PASS on 370.

**PENDING:** B5 (10,000 trials), full 10,000-trial KB-E1/E2/E5, KB-E3/E4 (human verdict).
**DECISION:** MECHANICALLY SOUND on available evidence; AWAITING full battery and human verdict for ALIVE/DEAD.

## 3. Bars B1–B7

### B1 viability (≥60% mean primary accuracy, frozen 370)
**0.8622 (319/370)** — PASS.
| task | acc |
|---|---|
| colordisc | 51/60 = 0.850 |
| colorconst | 38/40 = 0.950 |
| shapetrans | 54/90 = 0.600 |
| pitchdisc | 56/60 = 0.933 |
| timbredisc | 60/60 = 1.000 |
| motiondir | 60/60 = 1.000 |

Note: p024.img (t2_colorconst/primary) initially crashed due to a singular
3×3 matrix on grayscale panels. Fixed with a 1D luminance-fit fallback.
Now correct (SAME_SURFACE).

### B2 vs Approach A
Approach A frozen primary mean: 0.726 (from `senses/rebuild/harness/RESULTS.md`).
R2-9: 0.8622 (319/370).
**Delta: +0.136 (+13.6pp) in favor of R2-9.**

### B3 efficiency
Approach A frozen total ops: 1,034,699,124 (370 fixtures).
R2-9 total ops: 231,452,162 (370 fixtures).
**Ops ratio: 0.224× (R2-9 uses 22% of Approach A's ops).**
Emission bytes (370 trials): 11,873,587 (~32 KB/trial average).

### B4 no-interference (HARD KILL)
**PASS on 370 fixtures** (10,000 pending fixture generation).
KB-E5 ablation: emit vs noemit percepts byte-identical on all 370 trials.
Ledger digests identical: `2246ecc2f227e825bac5a6e62f2be13567c3aeff8b22222c9d741975b770f85d`.

### B5 false installs (≤3% on 10,000)
**PENDING** — requires 10,000-trial battery (fixture generation in progress).

### B6 determinism (HARD KILL)
**PASS on 370 fixtures** (10,000 pending).
Three byte-identical runs; ledger hash chain verified.

### B7 beauty
(i) Mechanism elegance: [judgment after battery.]
(ii) Human verdict: KB-E3/KB-E4 — package prepared, verdict PENDING (parent routes to Micah).

## 4. Kill criteria KB-E1–KB-E5

- **KB-E1 byte-identity:** **PASS on 370** (530 artifacts byte-identical to source spans/rects; identical across 3 runs). 10,000 pending.
- **KB-E2 no phantom:** **PASS on 370** (no empty/ownerless emissions). 10,000 pending.
- **KB-E3 human equivalence:** PENDING human verdict (package ready).
- **KB-E4 spoof-catch:** PENDING human verdict (package ready).
- **KB-E5 no-interference:** **PASS on 370** (emit/noemit percepts byte-identical). 10,000 pending.

## 5. Evidence and ledger

- `evidence/percepts_run1_emit/`, `run2_emit/`, `run3_emit/`, `run1_noemit/`
- `evidence/LEDGER.md` — hash chain digests
- `evidence/human_sample_manifest.tsv` (+ `.sha256`)
- `evidence/human_package/` — briefs + artifacts for Micah (via parent)

## 6. Deviations and notes

1. **Human sample frozen after fork build began.** The prereg requires freezing before the build. The fork was developed against the frozen harness fixtures and the fixture spec only; the R2A sample did not exist during development (generation was still running). No tuning against the sample occurred. The Goodhart protection (fork blind to sample) is preserved.
2. **Generator spec contradictions** (documented in generator ledger): per-task distribution rows sum to 5,100 normal / 5,815 adversarial vs top-line 5,000/5,000; TMB-1 boundary frequencies vs actual profile centroids. Generator preserves the 10,000 total and records the mismatches.
3. **Audio emission vs synth ban:** emitted audio is verbatim replay of fixture bytes (identity, not synthesis). The standing synth ban targets the synthesis paradigm; witness replay is explicitly the hypothesis under test (prereg §1: "replay is identity, so no renderer is under test").
4. No true field recordings available for the waveform gate; calibrated against human-produced reference WAVs (`*_human.wav`).

## 7. Verdict

**MECHANICALLY SOUND (partial):** All mechanical bars PASS on the 370-fixture
frozen primary set. The 10,000-trial battery is blocked on fixture generation
(R2A generator running; ~2,100/10,000 complete in isolated `r2a_r29/` directory
to avoid interference with other crews' generators in shared `r2a/`).

**ALIVE/DEAD:** DEFERRED pending (1) full 10,000-trial mechanical battery
(B5, KB-E1/E2/E5), and (2) human verdict on KB-E3/KB-E4 (package prepared,
awaiting parent routing to Micah).

No hard-kill bar has failed. The mechanism demonstrates:
- 86.22% primary accuracy (+13.6pp over Approach A)
- 4.5× fewer ops than Approach A (22% of ops)
- Byte-identical determinism across runs
- Provably read-only emission (zero percept/disposition difference)
- Verbatim source-byte artifacts with hash-chained provenance
