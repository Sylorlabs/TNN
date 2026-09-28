# RUNLOG — D2 instrument spec (A7 gate), 2026-09-27

## Task
Write-only spec task: produce `D2_INSTRUMENT_SPEC.md` (exact filename per
tasking, typo included) defining the D2 instrument to the D1 bar — parts,
generator, scoring rule, chance arms, phase analogs, K1–K6 adjudication,
taxonomy mapping, open questions. No code, no runs, no frozen-file edits,
no commits.

## What was read (in order)
1. `~/workspace/comp_b4/enacted/AMENDMENT_2026-09-27_A7.md` — the gate
   requirement: generator, scoring rule, chance arms, phase analogs,
   kill-bar adjudication.
2. `~/workspace/AGENTS.md` — workspace tool notes (read per runtime
   house-rules notice; no action needed for this task).
3. Frozen prereg `docs/lab/composition/PREREG.md` @ commit
   `6ca9e042110ca` (extracted via `git archive` to /tmp — the working
   checkout `tnn-native-lab-work` does not carry `docs/lab/composition/`
   on its current branch): §§1, 2 (D2 paragraph), 3 (phases), 4
   (generator), 5 (novelty), 6 (taxonomy), 7 (kill bars) in full.
4. `docs/lab/composition/pilot/REDTEAM_REPORT.md` @ same commit — full
   read, esp. "D2 (sim) gap" and Families 1–5 (wrong-order K1 defeat,
   scoring/classification decoupling 3a, P4 reclassification fix 3b,
   Caesar-shift lesson 1a/5a, K6 coverage 1c).
5. `docs/lab/composition/AMENDMENT_PROPOSAL.md` (proposed A1–A7, for
   context on what each amendment resolved).
6. Enacted `AMENDMENT_2026-09-27_A1.md` (wrong-order in chance, principle
   applied to D2), skimmed A2 (salt formula), A3 (P1/P2 protocol,
   interleaving, elig reporting), A4/A5/A6 (K6 scope, limitations, P0
   numbers) headers.
7. TIDELOCK machinery: `docs/lab/invention/survival/src/world.zag` — full
   read (action codes, EAT/dormancy, recipe table incl. crystal+crystal→WARD,
   DROP placement, sheltered(), storm_active(), costs, r_policy, slot
   layout, world_init 33-int format); `docs/lab/invention/survival/PREREG.md`
   §3 (TIDELOCK sketch: storms taught as physics, shelter strategies not
   taught); `worlds/v00.txt` (variant file format example).
8. `~/workspace/comp_b4/crewD_brief_DRAFT.md` — context on how the D1
   amended battery is being built (reused its A2/A3 resolutions as the
   model for the D2 analogs; did not copy anything verbatim).

## Design decisions worth recording
- D2 P2 scoring is per-episode PASS/FAIL against semantic criteria, NOT
  literal exact-match on action strings (many optimal paths exist). Only P3
  keeps literal exact-match (all-WAIT string). Flagged in §13 as possibly
  needing a dated amendment (frozen §3 says "Exact-match scoring").
- K6's bigram mechanism declared N/A with justification; replaced by
  committed N1–N3 novelty checks + red-team trace-replay and
  schedule-memorization attacks (the D2 analog of the shift-memorizer).
  Flagged in §13.
- P4's unit moves from ordered part-pairs to FW-vs-WF order templates,
  same 0.25/0.75 numbers, elig-set only, reclassify actual-(c)-items only
  (red-team 3b fix). Flagged in §13 as interpretation.
- Every P2 scenario must fail all three chance arms and pass REF-OK-D2
  (§11 gate) — NULL/SINGLE-RULE fail by construction (starvation; the
  WARD-placed criterion), WRONG-ORDER fails via documented calibration.
  Scenarios that can't satisfy the gate are discarded, never the criteria.
- S3-in-isolation is probed with a provisioned ward (intrinsic TIDELOCK
  coupling documented, not hidden).
- All TIDELOCK mechanics cited to world.zag function/section; scenario
  record extends the 33-int variant format with EPISODE/PREWARD lines
  (instrument-level, no mechanics change).

## Arithmetic spot-checks (done by hand, no runs)
- Appendix A worked example: k=48, salt=107 → void_a=11, start=5,
  s0=125 — recomputed 2026-09-27, matches the spec text.
- Energy budgets: F (120t, n_eat=4 → final exactly 100 ✓); W (90t,
  sheltered 30t → 40 at end ✓); T (200t, 30 sheltered, n_eat=4 → 50 ✓);
  FW/WF (200t, n_eat=4 → 50 ≥ 40 ✓); FWF (320t, 60 sheltered, n_eat=7 →
  50 ≥ 30 ✓); N (80t all-WAIT → 20 ✓).

## What remains PENDING (for the build crew / governance)
1. Real-learner per-tick episode interface feasibility (90–320 tick
   dialogue episodes) — open question 1.
2. Teaching protocol design (constrained to the 24 training scenarios) —
   open question 2.
3. S3 separability from S2 — documented limitation, empirical.
4. K6-D2 red-team attacks — defined, to be executed at battery time.
5. Scenario-record extension serialization — semantics fixed, text format
   for build crew.
6. §13 items 1–3 need governance's word (scoring rule wording, K6
   mechanism, P4 unit) before D2 construction.

## Output
- `~/workspace/comp_b4/d2spec/D2_INSTRUMENT_SPEC.md` (the spec)
- `~/workspace/comp_b4/d2spec/RUNLOG.md` (this file)

Nothing committed, no frozen files touched, no code written, no runs
executed — per tasking.
