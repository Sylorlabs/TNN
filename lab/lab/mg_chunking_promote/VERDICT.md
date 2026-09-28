# Magnifying-glass chunker — PROMOTION VERDICT (Phase 1+2, 2026-09-26)

Plain-English verdict: **the learned chunking policy is promoted into live intake.**
The frozen learned policy (derived from 9 chunkers x 57 questions: 57/57 correct,
57/57 native, 0 fallbacks) replaced the hand-authored Phase-1 rule table as the
live entry point `tnn_intake(...)`. The fixed C/W/S arms remain retired — they
survive only in `negcontrol.zag` as negative controls, untouched by this change.

## What changed (Phase 1 v1 -> Phase 2 v2)

| | Phase 1 (v1) | Phase 2 (v2, this commit) |
|---|---|---|
| Policy source | hand-authored deliberative D rules | frozen learned policy table (measured, 57Q x 9 chunkers) |
| Classifier | kinds 1-9, original vocabulary | extended classifier, kinds 0-17 + text-shape addressing |
| Zoom machinery | hand-written | frozen learned zoom/addressing (word locate -> char magnify) |
| Fixed C/W/S arms | absent from production | absent from production (unchanged) |
| Candidates in production | 1 (D) | 9 (all measured candidates, dispatcher picks only the frozen winner) |

`intake.zag` v2: classifies the question, detects text shape, looks up the frozen
measured winner for that (kind, shape) class, executes ONLY that winner, and emits
the derived reason plus all zoom traces. Empty measured classes explicitly default
to candidate 3 (the deliberative magnifier) and say so in the trace.

## Regression gate (the bar Micah set: anything breaks, it doesn't ship)

| Gate | Result |
|---|---:|
| Production questions | 57 |
| Correct | **57 / 57** |
| Native (no fallback) | **57 / 57** |
| Fallbacks | **0** |
| Choice lines carrying a derived reason | 57 / 57 |
| Rerun | byte-identical |
| Rebuild-from-source rerun | byte-identical |

RUN_LIVE1.out / RUN_LIVE2.out SHA-256:
`0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268`

Pure Zag. Zero RNG. Deterministic.

## The q22 trap (still held through production)

"What is the 2nd letter of fox" over "the quick brown fox" -> `o`. The live trace
shows `WORD>CHAR`: locate `fox` at word scale, zoom to its 2nd character.

## Provenance (how intake.zag v2 was built)

Assembled from the frozen learned fork `docs/lab/mg_chunking_learned/` (byte-identical
copies of `base.zag`, `hand_a.zag`, `hand_b.zag`, `hand_c1/2/3.zag` verified against
origin on 2026-09-26) plus the frozen measured policy table from `derive.zag`
(RUN_D1.out SHA-256 `45780575...eadcb`, 57/57 correct, 57/57 native, 0 fallbacks).
Selection law: most correct -> most native -> fewest ops -> coarser chunking -> lower
candidate id. No policy value was invented or tuned during assembly.

## Honest boundary

This is a measured policy derivation, not unconstrained runtime invention: the
policy was derived over a finite 57-question authored battery and a finite
9-candidate set, and the parser/classifier remains hand-designed. What shipped is
the *measured winner per class*, executed natively. See the next-wall verdict
(`../mg_chunking_nextwall/VERDICT.md`) for where the frozen policy breaks on
never-seen questions.

## Files

- `intake.zag` — live entry point `tnn_intake(...)` with the frozen learned policy.
- `battery1.zag` — 57-question production regression driver (extracts the frozen
  questions from the learned `derive.zag` and runs them through production).
- `negcontrol.zag` — UNCHANGED; retired fixed C/W/S arms as negative controls.
- `build.sh` — repo-relative build + full verification (gates 57/57/57/0).
- `evidence/RUN_LIVE1.out`, `evidence/RUN_LIVE2.out` — the two byte-identical runs.
- `SHA_MANIFEST.md` — checksums.
- `gen_phase1.py` — Phase-1 generator (kept for history; v2 battery assembled by script, see provenance).

## Addendum 2026-09-26 — degenerate-input panic fix (W25)

The next-wall battery exposed a deterministic panic in the production intake:
empty text on a whole-text position question (kind 2/8/9) hit `cand_zoom_19`
with a zero-length located span and indexed an empty slice (`t[-1]` /
`t[0]`). Root cause: `zoom_locate` returns `loc=0` (not `<0`) for the
whole-text shortcut even when `ll==0`, and the kind-2/8/9 branches only
guarded `loc<0`. Fix (in `hand_c2.zag`, `intake.zag` regenerated via
`assemble.py`, diff = exactly 3 lines): `if (loc<0 || ll==0)` answers `'?'`
like a miss — the same degenerate-answer pattern the kind-12 path already
used. No behavior change on any valid input: the 57Q production battery is
byte-identical pre/post fix (RUN_LIVE1 == RUN_LIVE2, 57/57/57/0).

New regression: `regress_degen.zag` + `build_regress.sh` — empty text across
all six position kinds (2, 8, 9, 12, 14, 15, W25 verbatim as D0):
6/6 correct, 6/6 native, 0 fallbacks, rc=0, byte-identical reruns
(`evidence/DEGEN1.out`, `evidence/DEGEN2.out`).
