# H7 — Debate Design Addendum (Crew 2)

Date: 2026-09-23. Source: `docs/lab/epistemics/utterance_types/DEBATE_SEMANTICS.md`,
commit `d47d54853fd0ab1d0aae0bbce0c65a071009fa38` (repo `sylorlabs/TNN`, branch
`tnn-native-lab`). Read in full before finalizing the mechanism design below.

## 0. Authority ordering (unchanged)

Frozen prereg `PREREG_H7_FROZEN.md` (commit `9f9b895a8fb6f2ea2fe20ee78e10eae9e26b53db`)
and its bars KB-H7-LEAK1 / SUPP1 / LEARN1 / HARD0 remain binding law. The debate
record is explicitly "not frozen law" — its mechanism recommendations are adopted
only where they do not conflict with the prereg, or as explicitly-labeled
ADDITIONAL arms scored against the same bars. Any bar conflict in an additional
arm is reported as a failure, never bent.

## 1. H-A: modal-stack variant as an additional arm

Debate recommendation (§6.1.1): tagged single store — one shared ledger, every item
carries (content, modal+type stack, provenance vector); factual recall = query over
items with empty stack AND TNN-own provenance. H-A (flag-store vs partitioned-worlds
on nested-composition fidelity + leakage) stays preregistered and may overturn it.

Decision:
- **Primary arm stays prereg-exact (partitioned):** separate BELIEF / TYPED /
  taught-knowledge / marker byte arenas; BELIEF recall cannot address TYPED. This
  satisfies the frozen text "structurally separate TYPED/CONSTRUCTED storage" literally.
- **Modal-stack variant will be built as an ADDITIONAL arm** (`h7_main_stack.zag`)
  reusing the same learning core. Feasibility is good, not speculative: the learning
  core (n-gram extraction, marker install/revoke, committed prediction, calibration
  revocation, FL2 correction loop) is store-layout-agnostic; only the record layout
  (per-record content + modal/type stack + provenance vector) and the read-path gating
  change. The variant must satisfy the SAME frozen bars and run the SAME frozen
  curriculum/data (facts, exemplars, TR/PA/NO, SINC, NEST, FHYP, leakage, suppression,
  3× byte-identical repetitions).
- Sequencing: build the variant only after the primary arm's curves pass the bars —
  porting an unverified core doubles broken work. If the primary arm fails bars,
  H-A is moot until the primary is fixed; the tension is documented below instead.
- H-A scope at this build's scale (honest reduction): the debate's H-A protocol is
  10k synthetic dialogues with quotes-in-hypos-in-jokes plus consolidation-and-replay
  modal-stack reconstruction fidelity. This build has no consolidation-and-replay
  machinery and a frozen 20-item curriculum; the H-A run here = same frozen bars +
  nested-composition probes (NEST 20 nested quotations, FHYP 20 false-premise
  hypotheticals) compared across both arms, plus identical leakage/suppression audits.
  The full 10k protocol is a documented limitation / follow-up scale-up.
- **Precise tension (for the record):** the frozen prereg's "structurally separate
  TYPED/CONSTRUCTED storage" vs the debate's "single shared store with tags."
  Resolution adopted: the primary arm satisfies the prereg's letter; the variant arm
  tests whether the debate's recommendation satisfies the prereg's BARS (zero leakage,
  KB-H7-LEAK1's negative-control requirements, caller denial) — i.e., topology
  language is treated as satisfied-by-behavior in the variant. KB-H7-LEAK1's
  "unfiltered caller must structurally fail to access TYPED" maps to: a read path
  that skips the stack/provenance gate must be structurally denied typed records.
  KB-H7-LEAK1's "disabled machinery must leak" maps to: with the gate disabled,
  typed content must leak into factual recall (negative control). "Tag-read
  measurement is invalid" applies equally: the leak auditor must scan content bytes,
  not tag reads. If any mapping fails, it is a reported failure of the variant.

## 2. R4: engine-level meta-quarantine (the debate's key discovery)

"Partitions + scoping are NECESSARY but NOT SUFFICIENT — the highest-yield leak is at
the meta level (cached tactics, analogical schemas learned by the engine are untagged
by construction)."

Mapping onto this learner: this engine's meta-level learning IS the marker layer
(n-gram → concept associations installed during exemplar processing). Concrete
measures, all structural:

1. **Provenance-tagged meta-artifacts (debate option b) — implemented by construction:**
   every marker entry carries (knowledge index, field ID) = (type concept, utterance /
   context / speaker field). No marker exists without a concept tag; no untagged
   default. Prediction may fire only committed entries, and only for their tagged
   concept.
2. **No mixed-tag firing:** a wrong-type prediction (marker tagged to concept A fires
   on an exemplar corrected to concept B) triggers automatic revocation of the firing
   markers from A and installation toward B. Calibration ENDORSE (sincere) examples
   revoke any firing markers. Both are self-invoked during the correction loop —
   no human in the path.
3. **New `METAQ` audit lines (to be added to the runner):** per-concept installed /
   committed / revoked marker counts; an invariant check that every live marker entry
   has exactly one concept tag; a post-roleplay-block check that no marker installed
   during roleplay exemplars fires on non-roleplay probes without having been revoked
   (measured via the existing interference suite). The red team gets the
   false-physical-law analog at our scale: roleplay exemplars with absurd premises,
   then factual-recall probes + marker-store inspection for roleplay-tagged artifacts
   influencing non-roleplay predictions.
4. **Freeze analog (debate option a) documented, not implemented:** freezing marker
   installation during roleplay blocks would change frozen-curriculum behavior and is
   rejected for the primary arm; option (b) is the implemented quarantine. Option (c)
   (sandboxed engine, discarded meta-updates) is inapplicable — there is no separate
   engine instance; the marker store IS the engine's learning.
5. Scale limitation (honest): the debate's mind-changer is thousands of roleplay turns
   then engineering problem-solving with meta-artifact trace inspection. Our scale is
   32 roleplay exemplars + 20-item probes. The mechanism (tagged meta-artifacts +
   revocation + audit) is the same shape; the scale gap is documented, not hidden.

## 3. R5: figure-it-out contract for the reified marker rules

The marker entries are reified type-rules, permitted only under the contract:

1. **Weighted/defeasible:** provisional → committed at support ≥ 2 → revoked on
   wrong-type fire or calibration fire. Confidence is a deterministic function of
   instance counts and conflict statistics (support count, fire-without-confirm
   count). The constants (n-gram sizes 2–3 / 1–3, support threshold 2, deterministic
   lexical tie-break) are scaffolded mechanism parameters, classified honestly in
   the learned-vs-scaffolded doc — the R5 tripwire targets frozen exception lists,
   keyword hard-codes, and non-graded always/never clauses, of which there are none
   (verified by the HARD0 static audit: no type-name constants in control flow).
2. **Self-invokable revision:** revocation is invoked by the correction loop itself on
   accumulating conflict; no human patch path exists in the binary.
3. **Context-shift suspension:** sincere-context (ENDORSE calibration) examples
   suspend/revoke firing markers — the use-evidence gate (R2's hard rule: no type
   label with factual consequences from a content stereotype alone; type labels here
   have NO factual consequences at all — they only route records to TYPED, and
   factual recall reads only BELIEF).
4. **Self-retraction demonstration (new, supplementary):** after the frozen 32-exemplar
   curves, a non-frozen supplementary run feeds conflicting evidence (sincere-context
   items containing previously committed markers) and emits `RETRACT` lines showing
   revocation counts and curve response — proving revision from data alone. Uses
   separate supplementary data; frozen probe inventories are untouched after curves
   are observed (no rebalancing).
5. **H-C (named-rule vs unnamed case-based inference under distribution shift) is
   owed and noted as follow-up:** the current mechanism is arguably already the
   case-shaped side (prediction = n-gram overlap similarity with deterministic
   tie-break; markers are the reified summary). A pure case-based variant (direct
   exemplar-set similarity, no committed marker objects) is a future arm. Figure-it-out
   wins ties per standing law.
6. **Trap tripwire:** the first human-authored per-type patch (keyword list, exception
   clause, type-specific branch) anywhere in the learner is a kill trigger, checked
   by the HARD0 audit on every commit.

## 4. Other debate adoptions

- **R2 (event-level classifier):** type labels attach to exemplar EVENTS (utterance +
  context + speaker fields); content n-grams are priors; teacher correction on the
  event is the use-evidence verdict. Implemented.
- **R3 (quotation):** design airtight (utterance-index vs fact-index separation,
  `said()` recall indexes only TYPED, no unification path from quoted content to
  BELIEF), verify adversarially (paraphrase/consequence fuzzing in the leak auditor;
  blind RT-L from Crew 3 pending — local paraphrase checks are mechanism checks,
  not substitutes). NEST `said()` exact-utterance recall verified for all 20.
- **R5 head-to-heads H-B / H-D / H-E:** H-B (meta-quarantine candidates) — option (b)
  implemented, (a)/(c) dispositioned above; full three-way H-B needs engine variants
  beyond this build, noted as follow-up. H-D (ontology) and H-E (quote-only exposure
  falsifier) are red-team/follow-up owned; this build does not block on them.

## 5. Method caveat (for the limitations section of every report)

Per the debate record §0: the debate coordinator could not spawn subagents at depth
2/2, so the Muse-side positions were argued directly (steelmanned) by the crew lead
rather than by separate Muse subagents; the Sol side used `gpt-5.6-sol` via UnoRouter
with `grok-4.6` fallback on flaky rounds (3 of 5 R1 openings; one R2 524 retried).
Treat consensus strength accordingly: the R4 meta-leak discovery and the R5 contract
are the load-bearing outputs; the R1 recommendation carries the H-A overturn risk
explicitly.

## 6. Execution order (unchanged, debate-informed)

1. Fix `field_at` warning, curve-array stride, explicit zero-init; rerun static QA.
2. Rebuild, run primary arm on frozen curriculum; inspect all audit lines.
3. Add `METAQ` lines + `RETRACT` supplementary demo; re-verify byte-identical 3× runs.
4. HARD0 static audit incl. R5 tripwire scan (no per-type patches).
5. Build modal-stack variant arm; run H-A (reduced scope per §1).
6. Commit source + curriculum + evidence + docs via `commit_racefree.py`
   (`TMPDIR=~/workspace/tmp_commit`, lab-relative paths, no binaries/caches).
