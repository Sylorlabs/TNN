# WAVE RAW-VS-HUMAN — Preregistration (RDTDT TEST phase), 2026-09-22

Micah's question: (1) WHY does raw-values (A) beat human-style percepts (B) at every
budget T0–T4; (2) HOW could human-style beat raw; (3) IS IT WORTH IT.

## Frozen background

Rematch verdict commit `1c01a1ad` (branch `tnn-native-lab`): A 83.8% vs B 56.6% at
T4; B−A = −27.1pp; B never crossed A, never reached 60%; both plateaued at T1
(A steps +11.7/0/0/0; B +3.9/+0.3/+0.4/0). KB4 failed on BOTH (48–59% false
installs). B2 vocabulary growth explicitly out of scope for the rematch.

Frozen and NOT changed by this wave: KB1–KB6, the battery, the fixture
generators, A's numbers. If the battery is found rigged, that becomes a dated
amendment PROPOSAL for Micah — never a unilateral change.

## Causal hypothesis under test (H-mech, from REVIEW)

B's deficit = **frozen coarse quantization whose bin edges are misaligned with
the fixtures' raw-space truth boundaries**, plus threshold-only fitting over
frozen families.

Evidence:
- t1 colordisc: generator truth boundary is ΔE ≈ 2.3 (`gen.py::gen_t1`: SAME at
  de 0.4–1.6, hard DIFFERENT at de 2.4–4.0). B's color vocabulary = 12 hue
  bins (≈30° each) × 3 lightness × 2 sat. Two colors ΔE 2.4 apart (DIFFERENT)
  routinely share one handle → `pc_color_dist` = 0 → B says SAME, unfixable by
  any k ∈ {0..4}. A fits RGB-unit threshold t=10 at the generator boundary.
- t4 pitchdisc: fixture hard cases are 0.5–0.8% relative pitch difference
  (`gen.py::gen_t4`). B's pitch = 48 semitone bins (12-TET ≈ 5.9%/bin).
  Sub-semitone differences stay inside one bin → B says SAME → B frozen at 85%
  (k=0). A fits dppm threshold t=5000 → 100%.
- Plateau mechanism: "training" in the rematch = threshold calibration only.
  Once the threshold sits at the best point the frozen family can express, more
  data is inert by construction. A: +11.7pp T0→T1 (threshold reaches the
  generator boundary), then flat. B: +3.9pp (k=1→0), then flat. The gap is
  structural (in the frozen transducer/family), not a data shortage — so 100×
  data cannot close it.
- t3 shapetrans: A = nearest-prototype on ratio (geometric truths) 100%; B =
  votes over (corners, curvature, symmetry) 38.9% — family expressivity, not
  resolution. t6 motiondir: both catastrophic (A 33.3%, B 18.3%) — neither
  fitted family expresses the task.

### Diagnostic D1 (cheap; runs BEFORE any fork is built)

On TRAIN_T2, for B's colordisc errors: fraction where the pair straddles the
ΔE 2.3 boundary (recomputed from the frozen generator code + fixture params —
no new data) yet shares a color handle. Same for pitchdisc: fraction of errors
where the relative difference is < one semitone yet both tones share a bin.
**Gate: if D1 < 50% on BOTH modalities, H-mech is weakened — DO NOT BUILD.
Report back and return to debate.** If D1 ≥ 50% on either, proceed with that
modality in scope (scope = modalities where the gate passes).

## Fork B2 — vocabulary growth through experience (standing untested fork)

Scope: color + pitch (tasks where D1 shows resolution is the binding
constraint). Shape/timbre/motion excluded: their failures are family
expressivity, which growth cannot fix (documented above).

Mechanism (pure Zag, deterministic, zero RNG):
1. EMIT mode: judgment binary emits per TRAIN stimulus
   (modality, bin id, within-bin position per-mille ∈ [0,1000), fixture id).
   NO truth labels in EMIT output.
2. GROW binary (Zag): for each splittable bin (12 hue bins on lightness
   per-mille; 48 pitch bins on within-bin frequency per-mille), try candidate
   cuts at {200,400,600,800} per-mille. For each candidate, define refined
   handles and compute TRAIN accuracy on the relevant task maximizing over the
   rematch decision grids (color k ∈ 0..6, pitch k ∈ 0..3). Adopt the best cut
   iff it beats no-split by ≥ 10 per-mille (1pp); tie-break = smallest cut;
   else no split. At most ONE split per bin (vocabulary stays human-scale).
3. The grown vocabulary is emitted as a Zag const table (generated source),
   compiled into the judgment binary. Table + growth log committed.
4. Standard protocol: fit decision thresholds per budget on TRAIN; evaluate
   on TEST-FRESH (seed 20260923, never touched during growth/fitting).

Determinism: growth is a pure function of frozen TRAIN fixtures; full pipeline
rerun from deleted caches ×2 must be byte-identical (compare grown-table
sha256 + result digests).

## Fork B3 — graded (fuzzy) percept membership

Same scope and protocol as B2. Attacks the same mechanism from the other side:
instead of splitting bins, remove the hard information cliff at bin edges.

Mechanism (pure Zag, deterministic, zero RNG):
1. Transducer computes within-bin per-mille position (already needed for B2's
   EMIT). If within margin m of a bin edge (hue edges for color; semitone
   edges for pitch), emit TWO handles with per-mille weights linear in
   distance from the edge: (h1, w), (h2, 1000−w). Otherwise single handle.
2. Pair distance = membership-weighted mean over the 4 handle-pair
   combinations of `pc_color_dist` / `pc_pitch_dist`, divided by 1e6, rounded
   half-up (deterministic). SAME iff weighted d ≤ k.
3. Margins m_h (color), m_p (pitch) fitted on TRAIN over grid
   {0,100,200,300,500} per-mille. **Validation gate: m=0 must reproduce frozen
   B's judgments byte-identically on all round-1 fixtures before any fitting.**

## Protocol

- Data: frozen TRAIN_T1 / TRAIN_T2 (+ TRAIN_T3 best-effort, 24h rule).
  TEST-FRESH never touched during growth/fitting. No new fixtures, no
  generator changes.
- Budgets: T1 + T2 required; T3 best-effort. Adjudicate at highest completed
  ≥ T2 (rematch curves froze after T1; the mechanism question resolves by T2).
- Comparison: fork vs A at the same budget on TEST-FRESH. A numbers frozen
  from the rematch (cite commit; no rerun).
- Fitting: rematch deterministic protocol (grids + tie-breaks) unchanged.
- Commit everything to `sylorlabs/TNN`, branch `tnn-native-lab`: big files via
  `~/workspace/commit_big_files.py`; lab-relative paths NOT starting with
  `docs/lab/`; verify via GitHub API; never commit binaries or `.zagd`.
  Read `~/AGENTS.md` Zag lessons before writing code.

## Kill bars (binding, mechanical)

- **B2: ALIVE iff (B2−A ≥ +2pp AND B2 ≥ 60%) on TEST-FRESH at the adjudication
  budget. Else DEAD.** Diagnostic: B2 must beat frozen-B by ≥ 3pp overall, else
  the growth mechanism did nothing (report mechanism-fail even if crossover
  somehow met).
- **B3: ALIVE iff (B3−A ≥ +2pp AND B3 ≥ 60%) at the adjudication budget. Else
  DEAD.** Diagnostic: B3 must beat frozen-B by ≥ 3pp on (colordisc+colorconst)/2
  (the hard-edge tasks), else the fuzzy mechanism did nothing.
- No bar bent, no rescue language. Report per-task tables, grown-vocabulary
  size, ops counts, and the D1 numbers.
