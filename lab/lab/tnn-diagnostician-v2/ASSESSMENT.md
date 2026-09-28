# TNN Diagnostician v2 — Assessment: templates removed, retrained, discovery tested

Micah order 2026-09-26: *"do the next wall for TNN, crash through it, get rid of
its templates and retrain it. Also give me numbers: how long does training take
and for what?"*

## What changed from v1

v1 (`docs/lab/tnn-diagnostician/`, kept as a historical negative control) matched
**crew-coded symptom codes** to **crew-extracted patterns** (`patterns.dat`) and
applied **crew-authored fix templates**. It could never discover anything the
crew hadn't already diagnosed.

v2 (`tnn_diag2.zag`, this directory) removes all three:
- No `patterns.dat`. No symptom codes. No fix-template library.
- The crew teaches **only** 9 labels of the form `(file, line-range, defect-class)`
  over **raw evidence bytes** (source files + audit prose, never paraphrased).
- TNN **induces** each defect class's signature itself: which structural features
  are *required* (true in all its labels), *forbidden* (true in none), *optional*,
  which identifiers *discriminate* (in ≥half its labels, <half of all others),
  and the match *bar* (from its weakest training label). Nothing crew-set except
  the feature extractors (the machinery) and the labels (the teaching).
- Discovery scans a **novel raw file** TNN never trained on, extracts candidate
  loci line by line, names the mechanism from the induced signature, and
  **composes** a fix direction from computed slots (`[COMPOSED]` = fixed per-class
  reporter wording + extracted line numbers, literals, call names — the crew
  never diagnosed this file).
- A class whose induced signature is **vacuous** (no required feature, bar ≤ 1 —
  it would match nearly every line) **abstains** instead of firing spuriously.
  TNN says NO_MATCH for that class (standing law).

Defect-class vocabulary (taught): HC=HARDCODED-CONSTANT, OD=OPERATOR-DRAW,
MR=MIXED-REGIMES, NS=NO-SYNTHESIS.

## Training numbers (what Micah asked for)

| Measure | Value |
|---|---|
| Compile (pinned znc, one-time) | ~2.7 s |
| **Train wall-clock** (3 runs) | **0.086 / 0.058 / 0.057 s** |
| Discovery wall-clock (681-line novel file) | ~0.06–0.07 s |
| Raw evidence consumed | **199,269 bytes / 4,186 lines / 4 files** |
| — pigfront_prefix.zag (pre-fix pigfront, parent of c5d01683cdea) | 113,275 B / 2,397 lines |
| — azupscale.zag | 64,333 B / 1,393 lines |
| — azoutpaint.zag | 14,433 B / 331 lines |
| — generation_audit/AUDIT.md | 7,228 B / 65 lines |
| Labels taught → validated | **9 → 9/9** (2 HC, 5 OD, 1 MR, 1 NS) |
| Signatures induced | 4 classes: required/forbidden/optional masks, 14 discriminative identifiers total, bars 2/1/8/1 |
| Knowmap SHA-256 (3/3 runs) | `68363e3b…f254` — **byte-identical** |
| Discovery trace SHA-256 (2/2 runs) | `cd1f4268…e16` — **byte-identical** |
| RNG | zero. Determinism: pure functions of the evidence bytes. |

**What training teaches, concretely** (from `DIAG2_TRAIN_TRACE_AFTER.txt`):
- HC: required={nonstructural literal}, forbidden={branch,comment,string},
  optional={call, ≥2-numeric-args, literal-assignment, assignment},
  disc={h_put64, PLAN, hcy}, bar=2.
- OD: required=∅, bar=1 → **ABSTAIN** (vacuous; would match nearly every line).
- MR: single-label over-specific signature (required={call,comment,string},
  bar=8) → silent on the novel file.
- NS: degenerate (tokenizer skips comment words; required={comment}, bar=1,
  achievable score 0) → silent. See "where the logic stops."

**Validation** (intake recomputes from raw text): locus exists and is in range;
locus non-blank; HC labels must re-extract a nonstructural literal (a
hardcoded-constant claim with no literal is self-contradictory). 9/9 pass.
The class association itself is the crew's teaching claim — validated only by
the before/after discovery test below.

## Before/after discovery test

Held-out novel file: `gentex.zag` (681 lines) — TNN never saw it in training,
and its diagnosis was withheld (crew ground truth: `VERDICT_delib.md:81`,
*"gentex geometry (160,112,86,86), (182,173,73,49), (74,26,11,21),
(246,26,11,21)… geometry was hand-placed"* — read **only** for scoring, after
discovery ran).

| | Before training (empty labels) | After training |
|---|---|---|
| Classes | 0 | 4 (1 abstains, 2 silent) |
| Result on gentex.zag | **NO DEFECT FOUND** | **61 hits → 27 regions, all HC** |

**The four withheld constant tuples were independently recovered** (lines TNN
extracted itself, with the exact tuples the crew later enumerated):

| Line(s) | Literals TNN extracted | Crew ground truth |
|---|---|---|
| 602 `xfer_part(...)` | 160,112,86,86 | (160,112,86,86) ✓ |
| 606 `xfer_part(...)` | 182,173,73,49 (+110,136,261,239) | (182,173,73,49) ✓ |
| 610–611 `xfer_part(...)` | 74,26,11,21 and 246,26,11,21 | both ✓ |

Composed fix direction (example, L602): *"mechanism=HARDCODED-CONSTANT. Numeric
literal(s) 160,112,86,86 are hand-placed geometry in xfer_part at line(s) 602,
standing where measured values should be. FIX-DIRECTION (composed from evidence,
not a template): replace the literal(s) with values from a TNN-deliberated
placement rule grounded in held measurements — the rule itself must be
TNN-chosen, never crew-picked. Then hunt the class…"*

Bonus class-true hits (same defect class, not in the crew's enumerated tuples):
L575 `y = 16`, L577 `x = 231` (hand-placed ear measurement-window bounds —
231/274/16/57 reappear as literals in L611's `xfer_part` args, so the "measured"
ear means are computed over hand-placed windows); L482 `head_mask(..., 70, 175)`
(the disclosed vision band thresholds); L542/544/560/562 (more window bounds).

## Scorecard (honest)

- **Recall on the 4 withheld `xfer_part` loci: 4/4 (100%).**
- Recall on all 8 crew-enumerated loci: 4/8 (50%) — the four `in_ellipse` mask
  lines (625, 627, 628, 629, same constants) were **missed**: they sit inside
  `if` conditions, and HC's induced signature forbids BRANCH (neither of the 2
  HC training labels had one) — a sparse-label artifact, named below.
- **Precision: ~10–16%** — 61 hits, ~6–10 class-true. The false positives are
  benign numeric literals the signature can't distinguish from geometry:
  `nio_alloc(1048576)` buffer sizes, `h_put64` struct offsets (8,16,24…),
  PPM header magic (80,54,10), image dims (320, 240, 76800).

## Verdict: genuine discovery — noisy detector, exact wall mapped

v1 could not discover anything new by construction. v2, taught only 9 labels on
raw evidence from *other* files, independently extracted the exact four
hand-placed geometry tuples from a file it had never seen, named the mechanism
(HARDCODED-CONSTANT: literal geometry bypassing measured layout), and composed
a fix direction from computed evidence. That is genuine diagnostic discovery.

It is a **noisy** detector (10–16% precision) with a **named miss** (the mask
lines). Both are measured, not hidden.

## Exactly where TNN's logic stops (the next walls)

1. **Branch-forbidden artifact (the mask miss).** HC forbids BRANCH only because
   2 training labels happened to have none. The same constants inside `if`
   conditions are invisible to it. Fix: more labels, or forbid-features need
   negative evidence (labels of what the class is *not*), not just absence.
2. **No notion of "geometry".** The signature detects *a nonstructural literal
   in code* — it cannot tell a coordinate argument from a buffer size, a struct
   offset, or image dimensions. ~50 of 61 hits are this confusion. Fix needs
   argument-role / data-flow features (does the literal flow into a position?),
   which the current lexical-structural extractors don't compute.
3. **OD abstention (prose evidence unusable).** The audit prose labels (T8/T9)
   carry no code-structural features, so OD induced a vacuous signature and
   correctly abstained instead of hallucinating. The audit *names*
   `tl_bres_list`/`bicubic2x`/`blend` — the same identifiers as the code
   labels — but the machinery has no cross-modal identifier linking. Prose
   needs its own feature family.
4. **Comment words discarded.** The tokenizer stops at `//`, so NS's teaching
   signal ("edge-column continuation") never entered the signature; NS is
   degenerate (required={comment}, bar unreachable). Tokenizing comment text
   (words, no calls) is the repair.
5. **Composed fixes are shallow.** The mechanism *name* comes from taught
   vocabulary; the *loci* are TNN's own; but the fix direction is generic
   per-class wording + slots. It does not yet derive *why* the literal is
   wrong from surrounding evidence (e.g., noticing 231/274/16/57 appear both
   as window bounds and as `xfer_part` args).

## Files

- `tnn_diag2.zag` — the diagnostician (pure Zag, zero RNG).
- `evidence/` — raw training evidence (byte copies), `train_labels.dat`,
  `empty_labels.dat` (before-control), `discovery_issue.txt` (the test question),
  `knowmap_after.dat` / `knowmap_before.dat`, and all four traces.
- v1 (`docs/lab/tnn-diagnostician/`) untouched as the negative control.

## Provenance / anti-leakage

`gentex.zag` and its diagnosis appear nowhere in training: not in the evidence
bytes (grep: 0 hits for the constants in all 4 training sources), not in the
labels (9 labels, none gentex). "gentex" occurs only in a *withholding comment*
in `train_labels.dat` and in the discovery question. The crew ground truth
(`VERDICT_delib.md:81`) was read only after discovery completed, for scoring.
