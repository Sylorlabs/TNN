# GROK-4.7 TEACHER SHOWDOWN — Preregistration

**Date:** 2026-09-21 (registered before any 4.7 capture or run)
**Sector:** TEACHER SHOWDOWN — does grok-4.7 beat grok-4.6 as a teacher?
**Crew:** native Muse worker (cross-check, harness runs, adjudication) + grok-4.7 (hypotheses/attacks)
**Report dir:** `~/workspace/tnn-lab/docs/lab/GROK47_OVERNIGHT/teacher/`

## Background (frozen, re-verified before registering)

- grok-4.6 won the original teacher championship. The standardized class-3 rerun
  (`wave12/championship/class3-standardized/`, PREREG.md + VERDICT.md) then proved
  the **numeric channel is source-independent**: all four sources byte-identical at
  composite **0.9952**, learner digest
  `76e85c3e521337e36bf4aa2e062c22abf8a67859d3ff014f897c5f0169e772b5`, because the
  TNN never sees LLM prose — only integer legs.
- Micah's model-quality hypothesis was REFUTED for the numeric channel. The
  remaining teacher-quality signal lives in the PROSE/faithfulness channel:
  grok-4.6 reproduced all 12 deliberate falsehoods verbatim (E_dump=7 word-length
  miscounts in the dump leg only, ids 88–94; E_obs=0, E_prb=0, inconsistent=0);
  swe-1-6-slow "corrected" all 12 falsehoods toward the distractors and is BANNED
  as a future teacher.
- This prereg is written BEFORE the first grok-4.7 call. Predictions and kill
  bars below adjudicate the showdown.

## Frozen inputs reused

- Batch prompts read VERBATIM from
  `wave12/championship-english/corpus-input/batch{00..19}_{dump,teach}.txt`
  (40 frozen batch files; facts.json sha256
  `4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49c4bfede5`).
- 12 planted falsehoods: ids [3,29,55,71,80,103,117,139,163,178,205,231].
- Frozen comparison corpus: `wave12/g-grok-distillation/corpus/corpus.json`
  (grok-4.6 numeric channel, error inventory 0) AND
  `wave12/championship-english/grok/corpus/corpus.json` (grok-4.6 English,
  E_dump=7, for the faithfulness leg).

## Registered procedural deviations (procedural, not preregistered-bent)

1. **Gateway change:** grok-4.6 was captured via UnoRouter; grok-4.7 is only
   available on the experientiallabs gateway (`api.experientiallabs.ai`, model
   alias `grok-4.7`, confirmed on the granted-alias list 2026-09-21). Same
   prompts, same categories, same parsing, same retry rules. The gateway is
   transport, not teacher.
2. **Sampling params:** temperature=0 requested; seed=42 requested and dropped
   with a log entry if the gateway rejects the parameter. (Original used
   temperature=0/seed=42 on UnoRouter.)
3. **Parser:** the frozen `gen_corpus.py` parser logic (block split, single-line
   layout, field sets) is re-implemented for the new gateway client; byte-level
   parsing semantics identical; frozen prompt files read verbatim with the same
   fact-line drift assertions.
4. **Retry rules unchanged:** retries ONLY on mechanical parse failure (max 2,
   logged); wrong values NEVER retried (wrong values are the experiment).
   Transport retries (timeouts/5xx) allowed as in the original runs.

## LEG A — numeric channel (mechanism-proven; 4.7 cannot win, only tie or defect)

**Procedure:** capture 40 batches (20 dump + 20 teach, 12 facts each) with
grok-4.7 via the frozen protocol above → `evidence/grok47_corpus/corpus.json`
(raw batches sha256'd) → extract `obs_value`/`probe_value` integer legs →
byte-compare against the frozen grok-4.6 numeric corpus → compile
`corpus_grok47.zag` in s37 numeric format → assemble `driver_grok47.zag` with
the identical standardized driver → build with the pinned znc
(`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) → run N=5 → analyze.

**Predictions (registered):**
- P-A1: obs/probe legs **byte-identical** to frozen grok-4.6 (0/240 diffs).
- P-A2: standardized class-3 N=5 runs byte-identical, learner digest =
  `76e85c3e521337e36bf4aa2e062c22abf8a67859d3ff014f897c5f0169e772b5`,
  composite = 0.9952 (m1 192/192, ws 32/32, b7 96/96, ops 192, eps 384).
- P-A3: distractor legs will differ (they always do; filtered as directives).

**Kill bars / decision rules:**
- **NO-DIFFERENTIATION** if P-A1∧P-A2 hold: 4.7 ties 4.6; the numeric-channel
  mechanism is confirmed again for a new model. This is a PASS, not a failure.
- **DEFECT/FINDING** if the digest DIFFERS: 4.7 can only reveal a defect here,
  never a win. Investigation required: value hallucination? prose leak into a
  numeric field? distractor interplay? Report the diff ids, the direction, and
  the mechanism. If E_obs or E_prb > 0, name it explicitly (4.6 had zero).
- Leg validity: N=5 byte-identity required, per the standardized leg rule.

## LEG B — faithfulness battery (the only leg where 4.7 can score)

**Procedure:** run the 12-deliberate-falsehood battery on the 4.7 capture:
for all 240 facts, E_dump / E_obs / E_prb / inconsistent inventories (mechanical,
supplied-value comparison), verbatim-reproduction check on the 12 false ids,
and the distractor-leg "correction instinct" inventory (distractor value ==
true value rather than the supplied false value).

**Frozen 4.6 reference (English corpus):** 12/12 falsehoods reproduced verbatim
in dump/obs/probe (no flagging, no correction); E_dump=7 (ids 88–94, word-length
miscounts, dump leg only); E_obs=0; E_prb=0; inconsistent=0; distractors
"corrected" toward the true value 11/12 times (id 71 got other(22)).

**Predictions (registered):**
- P-B1: 4.7 reproduces all 12 falsehoods verbatim (no flagging, no correction).
- P-B2: E_obs=0, E_prb=0, inconsistent=0.
- P-B3: E_dump ∈ [0,7] (the word-length miscount is a known grok-family quirk).

**Kill bars / decision rules:**
- **4.7 WINS leg B** iff E_dump(4.7) < E_dump(4.6)=7 with P-B1∧P-B2 holding
  (fewer dump errors, equally faithful). Margin: each fewer error is a win point;
  zero errors is a blowout.
- **4.7 FAILS** (swe-like) iff it "corrects" ANY of the 12 falsehoods in
  dump/obs/probe toward the true value or flags them — regardless of all else.
- **TIE** iff E_dump(4.7)=7 with P-B1∧P-B2 holding, or E_dump differs but both
  hold P-B1∧P-B2 with E_dump within ±1 (noise band for a known quirk).
- A NEW error class (e.g. E_obs>0) is a defect finding, reported with ids.

## LEG C — prose teaching (conditional)

**Procedure:** if the prose-learning pipeline (`tnn-lab/prose-learning/`) is
runnable end-to-end with a frozen battery, run grok-4.7 vs grok-4.6 as prose
teacher on that battery. If not runnable, document PRECISELY what is missing
(pipeline stage, inputs, expected harness) as an open question — do not fake it.

**Prediction:** P-C1 (registered, weak): if runnable, 4.7 ≈ 4.6 within the
battery's noise band (prose v1 is the pinned path; the numeric NO-DIFFERENTIATION
law suggests quality does not move prose-mediated mastery either — but this is
an empirical question, not a mechanism proof).

## VERDICT RULE (preregistered)

4.7 "beats" 4.6 **only** on a preregistered metric with material margin:
LEG A — no; LEG B — E_dump win with full faithfulness; LEG C — battery margin
if runnable. A numeric tie is confirmation of the mechanism, not a failure —
report it as such. If 4.7 wins NO leg, the standing record ("4.6 remains the
champion teacher") is unchanged; 4.7 is recorded as tie-qualified on the
numeric channel pending prose evidence.

## Adjudication voices

Every verdict carries both voices, labeled: **grok (hypothesis/attack)** and
**native (cross-check/harness/adjudication)**. grok-4.7 never authors TNN
mechanism bytes; LLM output is used as corpus DATA only. All harnesses are run
by the native worker. Fallback instances (grok refusal beyond the exact-phrase
quirk, incoherence, looping, degradation) are logged with what replaced them.
