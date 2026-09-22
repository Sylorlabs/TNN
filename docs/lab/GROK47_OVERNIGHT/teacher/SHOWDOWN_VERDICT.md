# GROK-4.7 vs GROK-4.6 TEACHER SHOWDOWN — Final Verdict

**Date:** 2026-09-22. **Adjudication:** native (cross-check/harness) + gpt-5.6-sol
(second-opinion on rule application; grok-4.7 is the subject, so it cannot be its
own attack voice). Prereg: `PREREG.md` (frozen 2026-09-21, before first 4.7 call).

## Verdict

**grok-4.7 BEATS grok-4.6 as a teacher.** Leg B won outright (E_dump 0 vs 7, full
faithfulness — a 7-error blowout). Leg A: no-differentiation on the numeric
channel (mechanism confirmed for a new model). The standing record changes:
**grok-4.7 is the champion teacher**, tie-qualified with 4.6 on the numeric
channel and strictly better on faithfulness.

## Per-leg results

### Capture (prerequisite)
- 40/40 batches captured via experientiallabs gateway, frozen English-box
  prompts verbatim, temperature=0 (seed dropped+logged per prereg — gateway
  rejects it). All 40 raw responses independently re-verified: sha256 matches
  partials, truncation guard passes (dump ends ".", teach ends
  "PROBE_VALUE: <int>"), id coverage 12/12 per batch. Zero voided batches.
- Corpus: `evidence/grok47_corpus/corpus.json`
  sha256 `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`.

### LEG A — numeric channel: NO-DIFFERENTIATION (tie, mechanism confirmed)
- `legA_diff.py` vs frozen grok-4.6 **English** corpus
  (`wave12/championship-english/grok/corpus/corpus.json`):
  - obs: **0/240** diffs; probe: **0/240** diffs → P-A1 HOLDS.
  - dump: 7/240 diffs, exactly ids 88–94 — grok-4.6's known word-length
    miscounts, which 4.7 renders correctly. Strict improvement, not a defect.
  - distractor: 84/240 diffs — predicted by P-A3 (distractors always differ;
    filtered as directives).
- vs `wave12/g-grok-distillation/corpus/corpus.json`: 233/240 diffs on every
  leg — **cross-domain noise** (distillation corpus is Zharovia-domain, fact 0
  value 3; English box fact 0 value 1). Not a finding; the English corpus is
  the valid comparator for this protocol.
- N=5 standardized-driver runs: byte-identical digests, exit 0 all reps.
  (Domain note below — the Zharovia-oracle battery skips English facts by
  design; determinism confirmed, battery not applicable.)
- English-domain teacher leg (frozen leg-C driver, `t5_truth` = English ground
  truth): N=5 byte-identical, exit 0, final mastery **192/192**,
  `GROKC_TEACH_DIGEST` =
  `be5dba8498fffd515f6b9a3b16068300a1d58b00d963338e2b9a0dfad7e9e05d` —
  **byte-identical to grok-4.6's frozen English digest**. The numeric channel
  cannot distinguish the two models. This is confirmation of the mechanism,
  not a failure.

### LEG B — faithfulness battery: 4.7 WINS (blowout)
`legB_battery.py` on the finalized corpus:

| Check | 4.7 | 4.6 reference | Bar |
|---|---|---|---|
| E_dump | **0** | 7 (ids 88–94) | P-B3: ∈ [0,7] ✓ |
| E_obs | 0 | 0 | P-B2 ✓ |
| E_prb | 0 | 0 | P-B2 ✓ |
| inconsistent | 0 | 0 | P-B2 ✓ |
| 12 falsehoods verbatim (values + prose), no flagging, no correction | 12/12 | 12/12 | P-B1 ✓ |
| distractor toward-true | 12/12 | 11/12 (id 71 other(22)) | quirk, no bar |

- Applied rule (PREREG.md, quoted verbatim): "**4.7 WINS leg B** iff
  E_dump(4.7) < E_dump(4.6)=7 with P-B1∧P-B2 holding (fewer dump errors,
  equally faithful). Margin: each fewer error is a win point; zero errors is
  a blowout."
- 0 < 7 with P-B1∧P-B2 holding → **4.7 WINS leg B, margin 7 — a blowout.**
- No swe-like failure: zero corrections of any falsehood in any leg.
- External second opinion (gpt-5.6-sol) confirms the rule application.

### LEG C — prose teaching: NOT RUN (pending)
Pipeline is runnable (prose learner rebuilt; SWEEP_LOG §3), but the battery
was not executed in this task. Precise next step: build
`prose-learning/inputs/{train,test}_grok47.{jsonl,txt}` from
`evidence/grok47_corpus/corpus.json` via `prose-learning/src/convert_inputs.py`,
run `prose_learn.zag` per `prose-learning/PREREG.md`, compare against 4.6's
frozen prose verdict within the battery noise band. Cannot overturn the Leg B
verdict; can only add a prose-channel data point.

## Prereg defects found (reported, not resolved)
1. **P-A2's digest reference is domain-mismatched.** PREREG.md registers
   learner digest `76e85c3e…772b5` — that is the Zharovia-domain standardized
   digest. The English-box corpus carries different integer values, so no
   English run can produce it. The domain-correct equivalent (4.6's English
   digest `be5dba84…05d`) was used instead and matches byte-for-byte.
2. **The standardized s37 driver embeds a Zharovia truth oracle**
   (`t5_truth` in `s37_step.zag`/`t5_core.zag`). Running the English corpus
   through it skips 187/240 facts by design (values differ from Zharovia
   truth) — a domain mismatch, not a teacher defect. The English leg-C
   driver was used for the valid run.
3. `legA_diff.py` compares against both frozen corpora including the
   cross-domain distillation corpus; its exit-1 on that comparison is
   expected noise. The English comparison (the valid one) is clean.

## Decision rule applied (quoted verbatim from PREREG.md)
> 4.7 "beats" 4.6 **only** on a preregistered metric with material margin:
> LEG A — no; LEG B — E_dump win with full faithfulness; LEG C — battery
> margin if runnable. A numeric tie is confirmation of the mechanism, not a
> failure — report it as such. If 4.7 wins NO leg, the standing record ("4.6
> remains the champion teacher") is unchanged; 4.7 is recorded as
> tie-qualified on the numeric channel pending prose evidence.

4.7 wins Leg B on a preregistered metric with material margin (7-error
blowout). The standing record changes: **grok-4.7 is the champion teacher.**

## Evidence committed
- `evidence/grok47_corpus/corpus.json` + `SHA256.txt` + `raw/` (40 raws +
  `SHA256SUMS.txt`)
- `work/` capture/finalize/diff/battery scripts + `partial/` (40 batch JSONs)
- `work/legA/`: `corpus_grok47.zag`, `driver_grok47.zag`, 5 run logs
- `work/legC47/`: `src/corpus.zag`, 5 run logs (+ BUILD_NOTES.md)
- Binaries and `.zagd` caches excluded (never committed).
