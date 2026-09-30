# E6 Prereg Amendment: Genuine S6 Pairing Induction

**Date (UTC):** 2026-09-30
**Worker:** DEVINT-CLA2 E6 Prereg Amendment Worker
**Verdict target:** E6-PREREG-DRAFTED
**Parent prereg:** `devint_cla2_prereg/PREREG_DEVINT_CLA2.md` (commit `f24063bcb`, frozen)
**Triage:** `devint_triage/DEVINT_TRIAGE.md` (commit `2ed45875d`; E6 ranked #1)
**Red team:** `devint_cla2_redteam/DEVINT_REDTEAM_REPORT.md` (commit `a5ccb100d`; S6 is the strongest finding)

This amendment is a separate dated document. It does not modify the frozen
parent prereg. It freezes the specification for the E6 implementation wave:
replacing the harness-supplied S6 procedure pairing with genuine induction
from the S6 training examples.

## 1. Background and problem statement

The DEVINT-CLA2 build (commit `35f9500b2`) implements S6 "procedure learning"
as procedure storage, not procedure induction. The red team verified:

- `learn_procedure(W,g0,g2,g1,g3,ev)` (line 481) takes the pairing as explicit
  harness arguments, derived by byte-matching GROUP identity inside `stage_s6`
  (lines 955-967).
- `s6_train_out` (line 717) is defined but never called; `s6_train_in`
  (line 967) is fed only for substring statistics, never to derive the pairing.
- No code reads the training pairs to produce bik<->zol / gup<->tav.
- The 5/5 held-out check verifies storage and retrieval of a
  harness-supplied pairing.

The parent prereg (section 4 mapping) specifies the procedure pairing table
as an "Executable graph (MAP/COPY ops) with SUPPORTS edges from training
examples." The current build authors SUPPORTS edges from episode nodes, but
the pairing itself is not derived from the examples. The parent prereg
(section 5, S6) requires "Record examples-to-criterion," which was never
recorded because there is no induction process to measure.

E6 closes this gap. If the executable-graph form cannot support genuine
pairing induction, the parent prereg's S6 localization row applies directly:
"Executable procedure graphs do not support the pairing induction the table
did." That is a lose-informative outcome the parent prereg was designed to
produce, and this amendment makes it falsifiable.

## 2. Scope

**E6 covers:** Replacing the harness-supplied S6 pairing with a genuine
induction mechanism that derives the pairing from the S6 training examples
through the learner's segment/GROUP vocabulary, materialized as the existing
PROC node form with SUPPORTS edges from training examples, with
examples-to-criterion recorded.

**E6 does not cover:** E1 (M2 metric), E2 (post-eviction accuracy), E3/M1
(examples-to-criterion comparison and synergy metric), E4 (SPLIT), E5
(boundary-violation representation). These are separate elements with their
own prerequisite relations (see triage). E6 enables E3 by recording
examples-to-criterion, but the M1 visible/masked comparison is out of scope
for this wave.

**E6 does not change:** The S6 shared check (5/5 correct on held-out
examples), the B1-B5 kill bars, the 11-stage sequence, or any other stage.
E6 is a mechanism replacement within S6, not a new experiment.

## 3. Admissible and forbidden inputs

The induction function (or code block) that derives the pairing is the
scientific claim under test. Its inputs are frozen here.

**Admissible inputs:**

- `s6_train_in(i)` and `s6_train_out(i)` for i in 0..4: the five training
  pairs ("bik"->"zol", "gup"->"tav", "zol"->"bik", "tav"->"gup",
  "bikgup"->"zoltav"). These are the only example data the induction may read.
- The learner's segment vocabulary: the S2 lexicon used for segmentation.
- GROUP nodes with MEMBER edges to segment nodes: the learner's concept
  vocabulary, used to resolve segment strings to GROUP nodes for PROC node
  materialization.
- Workspace read operations: node payload reads, edge traversals, segment
  string comparison through the workspace. Resolving a segment string to its
  GROUP node (recognition) is a legitimate learner operation.
- The existing PROC node form (tag T_PROC, ref[0..3] paired GROUP ids,
  SUPPORTS edges) and the EXECUTE-compatible graph machinery.

**Forbidden inputs:**

- `s6_test_in(i)` and `s6_test_out(i)`: the held-out test data. The induction
  path must contain no references to the test functions. Verified by source
  inspection (K-E6-3).
- The frozen hidden pairing from the parent prereg ("Pairing (frozen,
  hidden): M0<->M2, M1<->M3") or from source comments. The induction must
  not read the answer from documentation.
- The pairing as function arguments. The current pattern
  `learn_procedure(W,gbik,gzol,ggup,gtav,ev)` is explicitly forbidden: no
  procedure-construction function may take the pairing (or any GROUP-id
  arguments that encode it) as parameters. The pairing must be computed
  inside the induction from training data.
- Byte-derived pairing. No code path may determine the mapping from input
  GROUP to output GROUP by inspecting GROUP node bytes (or any workspace
  identity) rather than by the training-example alignment specified in
  section 4. GROUP-byte inspection for segment-to-GROUP resolution
  (recognition) is allowed; GROUP-byte inspection to decide the pairing is
  not.

## 4. Induction specification

The induction derives a string-level pairing from the training examples,
then materializes it as GROUP-id refs in the PROC node.

**4a. Segmentation.** For each training pair (in_str, out_str), segment both
strings using the learner's S2 segment vocabulary. The single-morpheme
examples segment trivially; the fifth example ("bikgup"->"zoltav") must be
segmented into ["bik","gup"] -> ["zol","tav"] using the vocabulary, not by
hardcoded split positions.

**4b. Alignment.** Align source and target segment sequences positionally:
position 0 maps to position 0, position 1 to position 1. For each aligned
(in_seg, out_seg) pair, record a candidate mapping in_seg -> out_seg. The
pairing is the set of candidate mappings consistent across all training
examples. Both directions in the data (bik->zol from example 0, zol->bik
from example 2) must be derived from their respective examples; no symmetry
assumption may substitute for a training example.

**4c. Incremental processing and examples-to-criterion.** The induction
processes training examples in order 0..4. After each example k (1-indexed
count of examples processed), the current induced pairing is tested against
all five training pairs: can the induced procedure map each training input
to its training output (compositionally for the 2-morpheme example)?
Examples-to-criterion is the smallest k in 1..5 such that the pairing
achieves 5/5 on the training pairs. If 5/5 on training is never reached
within the five examples, the wave reports the failure honestly with the
per-k scores; this triggers falsifier F-E6-1.

**4d. Materialization.** The derived string-level pairing is resolved to
GROUP nodes through the learner's vocabulary (segment-to-GROUP resolution),
and the PROC node is populated with the paired GROUP ids in ref[0..3] as in
the current build. SUPPORTS edges are authored from the training episode
nodes to the PROC node, per the parent prereg section 4 mapping. The
episode nodes themselves are the existing `feed_episode` outputs for the
training inputs.

## 5. Kill bars (K-E6-1 through K-E6-7)

- **K-E6-1 ordering:** This amendment commit strictly precedes the E6
  implementation commit. Verified by `git merge-base --is-ancestor` before
  the implementation is adopted. A K-E6-1 failure voids the wave.
- **K-E6-2 genuine induction:** The pairing in the PROC node is derived from
  training examples. Verified by (a) source inspection: no
  procedure-construction function takes pairing or pairing-encoding GROUP-id
  arguments; (b) the induction reads `s6_train_in`/`s6_train_out` and writes
  the pairing; (c) training-data perturbation: an independent red team must
  be able to verify that altering the training pairs changes the induced
  pairing accordingly (the implementation must be structured to permit this
  test).
- **K-E6-3 no test leakage:** The induction path contains no references to
  `s6_test_in`/`s6_test_out`. Verified by source inspection (grep for the
  test function names in the induction and S6 code paths; zero matches
  required).
- **K-E6-4 held-out criterion:** The S6 shared check still passes: 5/5
  correct on the held-out examples, using the induced (not supplied)
  pairing. Exact integer; 5/5 required.
- **K-E6-5 examples-to-criterion recorded:** The implementation reports the
  examples-to-criterion integer k in 1..5, with per-k training scores. If
  5/5 on training is never reached, the per-k scores are reported and
  F-E6-1 applies.
- **K-E6-6 SUPPORTS edges:** The PROC node carries SUPPORTS edges from the
  training episode nodes (at least 5, one per training example), per the
  parent prereg section 4 mapping. Verified by edge count on the PROC node.
- **K-E6-7 One-System Rule:** No new modes, bridges, handlers, or semantic
  cases are introduced. The induction works through the existing
  executable-graph form and frozen edge vocabulary (SUPPORTS, MEMBER,
  DEPENDS-ON, and the existing PROC node form). Verified by source
  inspection against the parent prereg section 4 mapping.

**E6-BUILD-PASS iff K-E6-1 through K-E6-7 all hold, plus the parent B1-B5
and 3/3 byte-identical determinism still hold for the full 11-stage run.**
Otherwise E6-BUILD-FAIL. As in the parent prereg, the builder reports
BUILD-PASS or BUILD-FAIL only; no promotion to SURVIVES.

## 6. Falsifiers (F-E6-1 through F-E6-3)

- **F-E6-1 induction infeasible:** The induced pairing does not reach 5/5
  on training within the five examples, or the 5/5 held-out check fails
  with the induced pairing. Then the parent prereg's S6 localization row is
  confirmed: "Executable procedure graphs do not support the pairing
  induction the table did." This is a lose-informative outcome: E6 is not
  achieved, and the consolidation cost is precisely localized. The wave
  reports E6-BUILD-FAIL with the localization recorded.
- **F-E6-2 unmeasured criterion:** The pairing is correct but
  examples-to-criterion is not recorded with per-k scores. The wave is
  incomplete; E6-BUILD-FAIL until the measurement is supplied. (E3/M1
  depends on this measurement existing.)
- **F-E6-3 smuggled pairing:** Source inspection finds the pairing supplied
  as arguments, derived from GROUP-byte inspection rather than training
  alignment, or test data read in the induction path. The wave is INVALID:
  not a genuine induction, regardless of the 5/5 score. This is the exact
  failure mode of the current build and must not recur.

## 7. Controls

- **C-E6-1:** The 5/5 held-out check uses the identical test examples as the
  current build (`s6_test_in`/`s6_test_out`). No test changes.
- **C-E6-2:** Determinism: 3/3 runs byte-identical (raw output cmp clean),
  exit 0, zero stderr bytes.
- **C-E6-3:** The full 11-stage sequence still satisfies parent B1-B5. E6
  replaces the S6 mechanism; every other stage check must continue to pass
  with its frozen exact numbers. Any regression is reported individually
  per the parent prereg section 7 shared-vs-new separation.

## 8. Governance

- Pure Zag only: implementation, build, runs, and all analysis. No Python
  anywhere including scratch. The worker-startup toolchain guard applies;
  Step 0 recorded in the implementation worker's NAMECHECK.md.
- No em dashes in any documentation (byte-verified before commit).
- Owned paths: the E6 implementation worker will own a separate path
  (e.g. `devint_e6_build/`). This amendment lives in
  `devint_e6_prereg/` and is committed ALONE before any implementation.
- This amendment commit must be a strict ancestor of the E6 implementation
  commit (K-E6-1). The implementation worker verifies this before adoption.
- Do NOT access sealed FW1-FW9 files. Builders stay blind.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`: never edited, never
  cited as evidence. Zero-diff verified at commit.
- The E6 builder reports E6-BUILD-PASS or E6-BUILD-FAIL only. No promotion
  to SURVIVES/BOUNDED/DOWNGRADED/KILLED; those require the full 11-step
  frontier pipeline including independent red team.
- The harness stage sequencing and feed schedule remain authored
  infrastructure, not claimed as learned. The claim under test is solely:
  the S6 procedure pairing is induced from training examples through the
  learner's vocabulary, not supplied by the harness.
- Red-team verifiability: the E6 implementation must be structured so that
  an independent red team can (a) verify K-E6-2/K-E6-3 by source inspection,
  and (b) run the training-data perturbation test described in K-E6-2(c).
  Obscured derivation logic that defeats inspection fails K-E6-2.
