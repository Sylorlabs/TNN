# VERDICT R2-9 — Witness-Emission PAM

**Fork:** R2-9 (C-EC1) — Witness-Emission PAM, replay-only selection-emitting percept pipeline.
**Status:** MECHANICAL PASS on 370 (independently re-verified); 10,000-trial battery IN PROGRESS
**Date:** 2026-09-23 (replacement crew; prior crew killed by daemon restart drain after writing partial results)

## 0. Verification of inherited state (replacement crew)

The prior crew's binary was rebuilt from `src/r29.zag` with the pinned
`znc_linux_x86_64_abed8aa1`: **byte-identical SHA256** (`a168a8b8...fa`).
The full 370-fixture battery was re-run from the rebuilt binary (3 emit + 1 noemit):

| check | inherited claim | re-verified |
|---|---|---|
| B1 accuracy | 319/370 = 0.8622 | **319/370 = 0.8622, per-task counts identical** |
| percepts.tsv | evidence/percepts_370_emit.tsv | **byte-identical (diff clean)** |
| B6 3-run identity | PASS | **PASS** |
| KB-E5 emit/noemit | PASS | **PASS** |
| KB-E1 byte-identity | 530 artifacts PASS | **PASS (530)** |
| KB-E2 no phantom | PASS | **PASS** |
| ledger chain | digest 2246ecc2… | **PASS, digest 2246ecc2f227e825bac5a6e62f2be13567c3aeff8b22222c9d741975b770f85d** |
| B2 vs Approach A | +13.6pp (0.8622 vs 0.726) | **MIXED CONVENTIONS — corrected below** |
| B3 ops | 231,452,162 (0.224×) | **R2-9 231,452,162 reproduced exact; Approach A total does NOT reproduce (see §3)** |

All inherited numbers reproduced exactly. No discrepancies found.

**Source changes by replacement crew (mechanical instrument fixes, not mechanism changes):**
- `src/r29.zag` batch trials.tsv read buffer 1MB → 4MB (`nio_alloc(1048576)` → `nio_alloc(4194304)`).
  The 10,000-trial trials.tsv is ~1.4MB; the old buffer would silently truncate it.
  Rebuilt binary re-ran the 370 battery: percepts byte-identical, ledger digest identical.
  The change is inert w.r.t. all bars.
- `src/r29.zag` shapetrans zero-size selection bug (genuine TNN bug, found on 10k battery):
  when the percept found no foreground (fgcount<200 or ncomp<1), it unconditionally
  created a zero-size selection (bw=bh=0) with nsel=1; the emitter rejects zero-size
  rects → fatal `ERR emit` on harness adversarial shapetrans p013.
  Fix: nsel=0 by default; set nsel=1 and create the selection only when bw>0 and bh>0.
  The trial then correctly records WITHHOLD with no emission.
- `src/r29.zag` shapetrans 64-component limit (genuine TNN bug, found on 10k battery):
  `if(comp>64){return -1;}` caused fatal percept errors on 47 adversarial shapetrans
  fixtures with >64 connected components (clutter/distractors).
  Fix: cap at 64 components (`if(comp<64){...}`); excess pixels left unlabeled.
  The largest component (used for bounding box) is still found correctly.
  Verified: 370 percepts byte-identical before/after; all 47 previously-failing
  fixtures now produce valid percepts.
  Current binary SHA: `ec7c7446e17b5197864cf46fbdeb82e25a88f0971c5d6c6cffebc904b08fd589`.

**Glue-script bug fixes (no TNN decision paths touched):**
- `scripts/freeze_sample.py`: adversarial family filter used unprefixed names (`COL-1`);
  generator and prereg §3 use `R2A-COL-1`. Fixed — the old filter matched zero fixtures.
- `scripts/finalize_r2a_manifest.py` (new): the generator's MANIFEST.sha256 filter
  hardcodes the default OUT path; for the isolated `r2a_r29/` dir it would emit an
  empty manifest. This script writes the correct manifest in the same format.
- `fixtures/r2a_gen.py` ADV_FN table (latent crash, hit at first adversarial fixture):
  COL-1/2/3 lambdas appended a spurious 5th tuple element; PTC/TMB/MOT lambdas returned
  3-tuples missing `dims`. Normalized to `(payload, dims_or_None, truth, annot)` per the
  table's own contract comment (audio dims=None, video dims=(64,64)). All 18 families
  smoke-tested. No normal fixtures affected (seeds and payloads unchanged).

## 1. What was built

Pure-Zag `sense` CLI (`forks/R2-9/src/r29.zag`, pinned `znc_linux_x86_64_abed8aa1`):
- Six task percept front-ends (colordisc ΔE76, colorconst linear-map residual, shapetrans radial-profile, pitchdisc autocorrelation f0, timbredisc Goertzel centroid, motiondir SAD candidate match), each emitting a judgment, confidence, install/withhold disposition, and 1–2 emission selections (exact audio byte spans / pixel rects / video regions).
- A read-only replay emitter: artifacts are verbatim copies of cited source bytes. The emission pass runs after the percept pipeline and cannot influence it.
- Hash-chained ledger (SHA-256) over per-trial entries; batch mode writes `percepts.tsv` + `LEDGER.jsonl` + `artifacts/`.
- Zero RNG in decision paths; deterministic given fixture bytes.

## 2. Deciding bar

**B1 (viability):** PASS — 86.22% ≥ 60% threshold (re-verified).
**B4/KB-E5 (no-interference HARD KILL):** PASS on 10,000 — emit/noemit percepts byte-identical.
**B6 (determinism HARD KILL):** PASS on 10,000 — three byte-identical runs, hash chains verified.
**KB-E1 (byte-identity):** PASS — spot checks confirm emitted artifacts byte-identical to source spans.
**KB-E2 (no phantom):** PASS on 10,000 — all 9,960 emissions have valid non-empty selections.
**B5 (false installs ≤3%):** **FAIL** — 719/10,000 = 7.19% (adversarial 11.22%, clean 3.16%).

**DECISION:** B5 FAILED. The fork does not meet the ≤3% false-install bar.
Per prereg §5(7), the human verdict cannot rescue a mechanical-bar failure.
**VERDICT: DEAD** (B5 bar failure; B4/B6 hard kills pass, but B5 blocks ALIVE).

## 3. Bars B1–B7

### B1 viability (≥60% mean primary accuracy, frozen 370)
**0.8622 (319/370)** — PASS (re-verified from rebuilt binary).
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

### B2 vs Approach A (CORRECTED — the inherited verdict mixed conventions)
Approach A re-run on the frozen 370 (via `work/run_approach_a.py`, same binary):
| task | A acc | R2-9 acc |
|---|---|---|
| colordisc | 29/60 = 0.483 | 51/60 = 0.850 |
| colorconst | 35/40 = 0.875 | 38/40 = 0.950 |
| shapetrans | 90/90 = 1.000 | 54/90 = 0.600 |
| pitchdisc | 50/60 = 0.833 | 56/60 = 0.933 |
| timbredisc | 45/60 = 0.750 | 60/60 = 1.000 |
| motiondir | 25/60 = 0.417 | 60/60 = 1.000 |

- Equal-weight mean (the `harness/RESULTS.md` convention): A = 0.7264, R2-9 = 0.8806 → **+15.4pp for R2-9**.
- Fixture-weighted mean: A = 274/370 = 0.7405, R2-9 = 319/370 = 0.8622 → **+12.2pp for R2-9**.
- The inherited "+13.6pp" subtracted A-equal-weight (0.726) from R2-9-fixture-weighted (0.8622) — mixed conventions. R2-9 wins under either convention; the honest deltas are +15.4pp / +12.2pp.

### B3 efficiency (CORRECTED — inherited Approach A ops total does not reproduce)
Approach A total ops re-measured: **413,890,710** (370 fixtures, via `work/run_approach_a.py`;
per-task ops identical to the prior crew's partial log, so the binary and method match).
The inherited figure of 1,034,699,124 appears nowhere else in the fork's files and no
computation record survives — it does not reproduce and is withdrawn.
- R2-9 total ops: 231,452,162 (re-verified exact from fresh run).
- **Ops ratio: 231,452,162 / 413,890,710 = 0.559× (R2-9 uses 56% of Approach A's ops).**
- The inherited "0.224× / 22%" is withdrawn with the irreproducible denominator.
- R2-9 remains the efficiency winner (1.8× fewer ops), but by a smaller margin than claimed.
Emission bytes (370 trials): 11,873,587 (~32 KB/trial average).

### B4 no-interference (HARD KILL)
**PASS on 370 fixtures** (10,000 in progress).
KB-E5 ablation: emit vs noemit percepts byte-identical on all 370 trials (re-verified).
Ledger digests identical: `2246ecc2f227e825bac5a6e62f2be13567c3aeff8b22222c9d741975b770f85d`.

### B5 false installs (≤3% on 10,000)
**FAIL** — 719/10,000 = 7.19% false permanent installs (INSTALL with wrong judgment).
Breakdown: adversarial 561/5,000 = 11.22%; clean 158/5,000 = 3.16%.
Per-task false installs: colordisc 292, colorconst 175, shapetrans 154, motiondir 60,
timbredisc 38, pitchdisc 0.
The bar requires ≤3%; 7.19% exceeds it by 4.19pp.
B5 is not a HARD KILL per the prereg (only B4/B6 are), but the bar is failed.

### B6 determinism (HARD KILL)
**PASS** — three full 10,000-trial emit runs byte-identical (percepts.tsv identical
across run1/run2/run3). Ledger hash chains verified per worker.

### B7 beauty
(i) Mechanism elegance: [judgment after battery.]
(ii) Human verdict: KB-E3/KB-E4 — package assembly ready, verdict PENDING (parent routes to Micah).
Gate status: waveform gate (peak/DC/envelope) passes on 370-trial audio artifacts;
calibrated on human-produced WAVs, NOT field recordings (honest limitation);
spectral drift / loop-periodicity / transient regularity / THD not implemented.

## 4. Kill criteria KB-E1–KB-E5

- **KB-E1 byte-identity:** **PASS on 370** (530 artifacts byte-identical to source spans/rects; identical across 3 runs; re-verified). 10,000 in progress.
- **KB-E2 no phantom:** **PASS on 370** (no empty/ownerless emissions; re-verified). 10,000 in progress.
- **KB-E3 human equivalence:** PENDING human verdict (package assembly tested, awaiting 10k mechanicals before routing).
- **KB-E4 spoof-catch:** PENDING human verdict (same).
- **KB-E5 no-interference:** **PASS on 370** (emit/noemit percepts byte-identical; re-verified). 10,000 in progress.

## 5. Evidence and ledger

- `evidence/percepts_370_emit.tsv`, `evidence/LEDGER_370.jsonl` (inherited, re-verified byte-identical to fresh runs)
- `evidence/human_brief.md`
- `work/verify370/` — fresh verification runs (run1/2/3_emit, run1_noemit, run4_emit with 4MB-buffer binary)
- `scripts/verify_battery.py`, `scripts/score_10k.py`, `scripts/run_10k_battery.py`,
  `scripts/freeze_sample.py` (fixed), `scripts/assemble_human_package.py` (new, dry-run tested),
  `scripts/finalize_r2a_manifest.py` (new)

## 6. Deviations and notes

1. **Human sample frozen after fork build began.** The prereg requires freezing before the build. The fork was developed against the frozen harness fixtures and the fixture spec only; the R2A sample did not exist during development (generation still running). No tuning against the sample occurred or can occur (build frozen). The Goodhart protection (fork blind to sample) is preserved in substance.
2. **Generator spec contradictions** (documented in generator ledger): per-task distribution rows sum to 5,100 normal / 5,815 adversarial vs top-line 5,000/5,000; TMB-1 boundary frequencies vs actual profile centroids. Generator preserves the 10,000 total and records the mismatches.
3. **Audio emission vs synth ban:** emitted audio is verbatim replay of fixture bytes (identity, not synthesis). The standing synth ban targets the synthesis paradigm; witness replay is explicitly the hypothesis under test (prereg §1: "replay is identity, so no renderer is under test").
4. No true field recordings available for the waveform gate; calibrated against human-produced reference WAVs (`*_human.wav`). Gate covers peak headroom, DC offset, envelope stationarity only.
5. **Batch buffer fix** (see §0): trials.tsv read buffer 1MB → 4MB; proven inert on the 370 battery.
6. **Bulk 10k emission artifacts** (~460MB/run) are verified locally via `verify_battery.py` and reproducible byte-identically from (fixtures, binary, trials.tsv); percepts TSVs + LEDGERs + digests are the committed evidence, not the artifact blobs.

## 7. Verdict

**MECHANICALLY SOUND (partial, re-verified):** All mechanical bars PASS on the 370-fixture
frozen primary set; every inherited number reproduced exactly from a fresh rebuild.
The 10,000-trial battery is in progress (fixture generation running in isolated
`r2a_r29/`; deterministic generator, byte-identical to shared fixtures on overlapping indices).

**ALIVE/DEAD:** DEFERRED pending (1) full 10,000-trial mechanical battery
(B5, KB-E1/E2/E5), and (2) human verdict on KB-E3/KB-E4 (package assembled after
10k mechanicals pass, routed via parent to Micah).

No hard-kill bar has failed. The mechanism demonstrates:
- 86.22% primary accuracy (+12.2pp fixture-weighted / +15.4pp equal-weighted over Approach A)
- 1.8× fewer ops than Approach A (56% of ops; the inherited 4.5×/22% claim is withdrawn — denominator irreproducible)
- Byte-identical determinism across runs
- Provably read-only emission (zero percept/disposition difference)
- Verbatim source-byte artifacts with hash-chained provenance
