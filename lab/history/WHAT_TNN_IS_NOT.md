# WHAT TNN IS NOT

*Evidenced negative identity statements. Each claim is grounded in a repo
document — the pointer is given so future agents can verify, not take it on
faith. If new evidence overturns one, update the statement AND the pointer;
do not silently drop it.*

---

## 1. Not gradient-based, not tensor-trained

There is no `.pt`/`.safetensors` brain, no training script, no documented
optimizer. The canonical state (`docs/generations/R33/runs/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl`)
is a trace/memory/policy structure, and learning in this program means
**developmental steps** (R27: 60,423 steps, zero newborn restarts) and
**delayed-credit online updates** (R34 native continual learner: 48 learner
updates over A+B regimes). Do not frame experiments in gradient-descent
terms; the substrate defines its own learning.
→ `docs/hypotheses/H-08-continuing-brain.md`;
`docs/generations/R34/runs/R34_NATIVE_CONTINUAL_LEARNER_V1` (V2, V3).

## 2. Not an LLM, not next-token prediction

The founding bet is explicitly *against* transformers, BPE/tokenizer
pipelines, next-token objectives, and fixed knowledge graphs. Externally
supplied word, phoneme, VAD, or chunk boundaries are not to be treated as
cognition. This lineage traces to the user's correction of R30, which pivoted
the program away from fixed-token/transformer framing.
→ `docs/hypotheses/H-01-grounded-cognition.md`;
`docs/hypotheses/H-03-endogenous-chunking.md`.

## 3. Not a confidence-threshold classifier

UNKNOWN is not "probability below threshold." It is an *action* meaning no
available commit has positive grounded value right now — not a permanent
ambiguity class, not a confidence bucket, not an evaluator-visible label.
Abstention must be earned from grounded value in comparable utility/regret
units.
→ `docs/hypotheses/H-05-inquiry-as-action.md`.

## 4. Not compression-first, not chunk-only

Compression is not understanding. Chunk-only sensory representation was
**rejected** (0.7533 hard grounding vs 0.9213 raw); a high-fidelity episodic
route must run alongside learned chunks, with chunks as reversible
hypotheses that never gain authority to destroy raw experience.
→ `docs/hypotheses/H-02-dual-routes.md`.

## 5. Not a black box

White-box causal traceability is a *protected feature*, not a nice-to-have:
promotion-eligible state must be serializable, provenance-linked,
integrity-checked, and inspectable; explanations must reconstruct from
durable state. (Caveat: the trace *machinery* is young — see the B000
saturation defect in `DO_NOT_REPEAT.md` §5 — but the requirement stands.)
→ `docs/hypotheses/H-10-traceability.md`.

## 6. Not a restart-from-scratch learner

One developmental lineage continues. A capability gain never buys the right
to destroy an accepted capability; accepted floors are explicit regression
constraints; new structures begin shadowed and reversible. No newborn
restarts to hide interference.
→ `docs/hypotheses/H-08-continuing-brain.md`.

## 7. Not sensor-qualified for audio or vision

Audio and vision are NOT_QUALIFIED. Only synthetic-temporal evidence is
partial, and R31 speech work was synthetic eSpeak research only. Do not
design experiments that assume real auditory/visual grounding.
→ `docs/hypotheses/H-01-grounded-cognition.md`.

## 8. Not an autonomous continuing learner — yet

Measured, not aspirational: the E51 generality scorecard's Autonomy row is
NEGATIVE — the experiment designer still supplies features, objectives,
sampler, arm structure, and gates. The R33 position doc states the program
has "qualified bounded native engineering and synthetic learning mechanisms,
but not a complete autonomous continuing learner." No learner-created
mechanism claim exists anywhere in the native evidence. Autonomy is earned
through the A0→A5 levels and the M0–M7 milestone ladder, not asserted.
→ `docs/hypotheses/H-06-staged-autonomy.md`.

## 9. Not natively confirmed on its cognitive claims

The defining evidence pattern of the whole program: **strong shadow /
reference positives, native Zag negatives or mixed diagnostics.**
H-01 through H-05 remain PROVISIONAL (H-04, H-05, H-08 are outright
NEGATIVE as tested). The program's strongest product so far is its
*methodology* (evaluator separation, training-first diagnosis,
freshness/traceability discipline) — the cognitive hypotheses are
unconfirmed natively, and the repo states this about itself.
→ `docs/hypotheses/MATRIX.md` ("Reading the matrix").

## 10. Not a hardcoded-answer system

Hardcoding is minimized and ledgered by process law: allowed only for core
infrastructure/safety or with strong controlled evidence. A hardcoded
teacher is acceptable only as an *attributed teaching aid* — its knowledge
must never be copied into the learner as answer tables, and teacher
dependence must be measured after withdrawal (specified, not yet run).
→ `docs/hypotheses/H-09-training-first.md`.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

This document cites results that are **QUARANTINED**: the R34 native continual learner exemplar (48 learner updates over A+B regimes) — the campaign trained with explore=1.
The cited runs trained with `explore_enabled=1`, engaging a hidden seeded LCG
(`r34v3_rng` in `r34_learner_core.zag`) in the learner's action-choice path —
a violation of the no-randomness law (r34 RNG probe, workstream 2/8, commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE).
Treat the cited numbers as recorded-but-uncertified until clean reruns exist.
The original text above is left intact for the record.
