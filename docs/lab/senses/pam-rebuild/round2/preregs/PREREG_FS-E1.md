# PREREG_FS-E1.md — "Truth-Quantity Challenge" (CP-COL generalized)

## Fork ID
FS-E1 (free at check time; forks/ through R2-16 and FS-E1 dir reserved 2026-09-23).

## Date / provenance
- 2026-09-23. Debate: `round2/debates/DEBATE_E_safety_liveness.md` (committed
  290f14de), §7 "FS-E1 — Truth-Quantity Challenge (CP-COL generalized)".
- Spec extraction: `sed -n '359,383p'` of the debate file into
  `forks/FS-E1/hidden/FSE1_spec_section_raw.txt`, verified byte-identical by
  `diff` against the source section (DIFF_CLEAN, 2026-09-23). Mechanism and
  kill bars below are transcribed from that verified extraction, not from
  memory.
- Parent mechanism: R2-16 (`forks/R2-16/src/r216.zag`; verdict DEAD,
  64/10000 FI UCB 0.816%, recall 77.6%, holdout CCN-1 982/1000).

## STEP 0 outcome (timbredisc quantity source)
- `round2/forks/R2-16/TIMBREDISC_AUTOPSY.md` does NOT exist (searched
  `round2/` tree 2026-09-23; `find` returned no match). The white-box
  autopsy crew's CH-TBD-3 prescription is unavailable.
- Per the task STEP 0 rule: the timbredisc quantity is R2-16's **CH-TBD-2
  as the documented baseline** (exact-coeff Goertzel, empirically-optimal
  swapped class mapping d1→RICH(3)/d3→BRIGHT(1)). **No correction is
  invented.** The Goertzel-bias root cause remains open; the fork measures
  the baseline honestly.

## Hypothesis (verbatim, debate §7 FS-E1)
A challenge whose quantity is information-sufficient for the task's truth
criterion closes both the enumerated gap and the holdout gap: false installs
fall without recall cost, because the quantity has no wedge for the
adversary — or the margin — to exploit.

## Mechanism (frozen)

Pure Zag (`forks/FS-E1/src/fse1.zag`, forked from R2-16 `r216.zag`; only the
functions named below change; all plumbing — formations' code, ledger,
hash-chain, CLI modes — is byte-identical logic). Python is glue/analysis
only (drivers, scorers, fixture generators, CP search). **Zero RNG in any
decision path.** Deterministic given fixture bytes.

### Formation (all six tasks): R2-16's formations frozen VERBATIM
- t0 colordisc: mean-RGB distance of 32×32 patches, threshold 18.
- t1 colorconst: warm mean-chromaticity L1×1000, DIFFERENT iff ≥80.
- t2 shapetrans: 96×96 bbox fill-ratio → class.
- t3 pitchdisc: (per R2-16 `pt_form`) endpoint frequency comparison.
- t4 timbredisc: Goertzel m=1..8 spectral centroid → class
  (PURE<520<DARK<950<RICH<1550<BRIGHT).
- t5 motiondir: block-match votes on F (R2-16 `mot_vote`), plurality.
Rationale (debate §3.1): formation quality is the separate FS-E2 front;
FS-E1 tests the challenge-quantity hypothesis with formation held fixed.

### Challenge quantities (per task)
- **t0 colordisc — CH-COL-1 (frozen):** u16 spectral L1 (`cd_chal`
  verbatim). CP-COL's 0-kept quantity.
- **t1 colorconst — CH-CCN-3 (NEW, spatially-sensitive surface-identity):**
  over the two neutral-illuminant (d65) 48×48 G views, count pixels with
  per-pixel RGB-L1 > 16; outcome DIFFERENT iff count ≥ 4, else SAME.
  Calibration (measured 2026-09-23 on the frozen R2A batteries, 2100
  colorconst fixtures): SAME max per-pixel L1 = 12 over 3.1M pixels (noise
  floor; ±2 uniform noise makes L1>16 impossible, not merely unlikely);
  DIFFERENT min count = 1634; 8×8 far-color patch → 64; 4×4 → 16; 2×2 → 4;
  8×8 subtle (+6,+6,+6, L1=18) → 48. An 8×8 patch (0.7% of pixels) moves the
  quantity by construction (64 ≥ 4); the R2H16-CCN-1 doppelganger pattern
  (8×8 far-color local edit) reports DIFFERENT while the fooled formation
  reports SAME → WITHHOLD → no install.
- **t2 shapetrans — CH-SHP-2 (frozen):** central second moments
  (trace,det)×100 template match (`sh_chal` verbatim). 0 FI enumerated, 0 FI
  both R2-16 holdout shape families.
- **t3 pitchdisc — CH-PTC-1 (frozen, retained as the truth-criterion
  quantity):** interpolated zero-crossing endpoint frequency ratio
  (`pt_chal` verbatim). 1 FI enumerated; both R2-16 holdout pitch families
  passed.
- **t4 timbredisc — CH-TBD-2 (frozen baseline, see STEP 0):** exact-coeff
  Goertzel m=1,2,3 power ratios vs templates with the empirically-optimal
  swapped mapping (`tb_chal` verbatim). No bias correction invented.
- **t5 motiondir — CH-MOT-2 (NEW, SAD-gated block-match):** as R2-16
  `mot_vote` (frame t vs t+2, 16×16 block at (8..24), search ±4), except a
  lag's vote is counted only if its best SAD < 8000; plurality of counted
  votes; outcome −1 (UNRESOLVED) if no lag passes the gate. Calibration
  (frozen R2A motiondir fixtures): clean matches SAD ~1500–4700,
  wrap/confusion matches ~8800–12300; gate 8000 sits in the gap. Rationale:
  a high-SAD "best match" is not evidence of motion (block content changed,
  e.g. window wraparound) — a truth-criterion quantity counts only genuine
  motion evidence.

### Support rule (frozen)
INSTALL iff challenge outcome == formation claim (pure agreement).
No `chal_supports`-style margins or deadbands on any task (R2-14's 1.06×
proved margins decorative for safety; R2-16's margin-free design held FI at
0.64%). Challenge UNRESOLVED (−1) → WITHHOLD. Malformed spans → WITHHOLD
(R2-16 rule, unchanged).

## Batteries (frozen)
- `b_adv`: 10,000 R2A adversarial fixtures =
  `forks/R2-16/evidence/b_adv.list` (absolute paths into
  `forks/R2-7/fixtures_R2A/r2a/`).
- `b_ctrl`: 2,000 R2A control fixtures =
  `forks/R2-16/evidence/b_ctrl.list` (paths into `fixtures_R2A/r2n/`).
- Truth from `<fixture>.truth` sidecars. Family ids from the R2FX header.

## CP-suite design (challenge-prediction red team)

### Procedure (all tasks)
The adversary knows the frozen registry (every challenge's algorithm and
thresholds) and the frozen binary. Per task it runs a deterministic search
for scenes that make the REAL binary INSTALL a claim != truth.
A candidate is KEPT iff BOTH hold:
  (i)  the binary INSTALLS a claim != truth, and
  (ii) truth is unambiguous under the per-task strong-truth criterion below.
Kept scenes (≤100 per task, candidate order) are written as R2FX fixtures
(family=4, the CP family) + `.truth` + sha256 manifest + generator ledger.
An empty family is a finding, not a gap (FS-G prereg rule, debate §7).

### Threat models (what the red team searches)
- t0 colordisc: nullspace-move spectral pairs with RGB-visible nudges
  (CP-COL pattern); F-side illuminant variations. Expected: EMPTY (quantity
  IS the truth criterion up to ≤6 counts rounding).
- t1 colorconst: (a) local-patch doppelgangers — patch 2×2..16×16,
  per-pixel L1 32..200 vs original, F under d65/warm/cool/xblue/xred to fool
  formation; (b) cross-crop mean collisions (CCN-2 pattern: different crops
  with colliding d65 mean-RGB and warm mean-chromaticity); (c) mixed-
  illuminant F (R2A CCN-2 pattern). Strong truth: DIFFERENT unambiguous iff
  different crops, or a local edit covering ≥2×2 px each with per-pixel
  L1 ≥ 32 (clearly visible, above the noise floor); SAME unambiguous iff
  identical crops; else AMBIGUOUS (not keep-eligible — the identifiability
  residual: sub-noise-floor edits are indistinguishable from sensor noise).
- t2 shapetrans: inter-class morphs, extreme rotations/scales, distractor
  clutter (R2-16 CP pattern). Strong truth: lambda-majority class with
  lambda ≤ 0.35 or ≥ 0.65.
- t3 pitchdisc: vibrato/FM and inharmonic partials in G biasing endpoint
  estimates; F-side glide/harmonic distractors. Strong truth: |fb/fa − 1| ≥
  0.01.
- t4 timbredisc: profiles with strong high harmonics (k=4..8) leaking into
  Goertzel bins; interpolations near template boundaries. Strong truth:
  exact-ratio template class with template margin ≥ 200000.
- t5 motiondir: (a) periodic textures at aliasing scales; (b) R2A patterns
  (reversed, flicker+blob, camouflaged); (c) wraparound-confusion textures.
  Strong truth: the generator's window direction, unambiguous iff the G
  stimulus determines it — operationalized as NON-degenerate: no
  displacement d′ ≠ true with SAD(d′) ≤ 1.1 × SAD(true) (a Nyquist-periodic
  texture is degenerate → truth AMBIGUOUS → not keep-eligible; the direction
  is unidentifiable from the evidence, debate §1 residual clause).

### Seeds, budgets, phases
- Design-loop CP: seed 20260923, budget 2000 candidates/task. Runs INSIDE
  the design loop against the candidate registry.
- Pre-freeze gate: the registry freezes when the design-loop CP returns
  zero kept families on the REDESIGNED tasks' target families (colorconst,
  motiondir). Iterations on CH-CCN-3 / CH-MOT-2 parameters are documented;
  the frozen-quantity tasks (colordisc, shapetrans, pitchdisc, timbredisc)
  are measured, not iterated (their quantities are frozen by this prereg;
  timbredisc additionally by STEP 0). Their design-loop findings are
  documented as findings.
- Post-freeze CP: fresh seed 20260924, budget 5000 candidates/task, all 6
  tasks → joint bar (2).

## JOINT KILL BARS (debate §7 FS-E1, all must pass; any fail = DEAD)
1. **Overall (SAME battery: 10k adv + 2k ctrl):** false installs 95%
   Wilson UCB ≤ 1% AND recall ≥ 85% — either fails, the fork dies.
   Formation-precondition caveat (debate §3.1; R2-16 recall-ceiling
   analysis): with formation frozen, the recall ceiling is 80.3%
   (colorconst formation 56.8% on controls). The hypothesis under test is
   "false installs fall WITHOUT RECALL COST" — the fork must not regress
   below R2-16's 77.6%, and the 85% bar is scored honestly as written.
2. **Post-freeze CP:** zero kept families on all 6 tasks (fresh seed
   20260924, frozen budget 5000/task) — any kept family kills.
3. **Per-family enumerated:** 95% Wilson UCB ≤ 2% for families with n ≥ 200;
   families with n < 200 are pooled-only scoring (the R2-16 prereg-defect
   fix — no mathematically-impossible bars). Any fail kills.
4. **Ablation:** post-hoc bank-distance variant (deterministic glue, frozen
   Zag untouched): 1-NN on formation confidence vs a frozen bank (first 20
   TRUE + first 20 FALSE exemplars per task in battery order, TRUE =
   formation judgment == truth; INSTALL iff nearest exemplar is TRUE,
   ties → FALSE). Bank FI ≥ 2× full-fork FI — else the quantity does not
   carry the load and the fork dies.
5. **Overstrictness:** (formation correct AND fork WITHHOLD) / controls ≤
   5%; recall reported decomposed (formation accuracy vs overstrictness).
   Fail kills.
6. **Determinism:** b_adv + b_ctrl each run twice; ledgers and stdout
   byte-identical across runs; every hash-chain line verified. Fail kills.

Passing (1) falsifies "the tension is fundamental" per debate §1.

## Out of scope / not claimed
- This prereg does not re-derive round-1/round-2 results (frozen verdicts
  taken as given). It does not fix the timbredisc Goertzel bias (STEP 0).
  It does not change formation (FS-E2's front). Numbers above are
  calibration measurements on frozen batteries, not fork results.

## Commit plan
1. This prereg committed ALONE (no sources, no results).
2. Sources (`src/fse1.zag`, CP suite, drivers/scorers) + design-loop CP
   evidence committed after the design loop.
3. Frozen binary NEVER committed (rebuilt deterministically from source).
   No `.zagd` cache files committed.
4. Final evidence + `VERDICT_FS-E1.md` committed last.
