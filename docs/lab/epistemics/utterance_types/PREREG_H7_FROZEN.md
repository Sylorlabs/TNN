# H7 PREREG — Utterance-Type Learning (FROZEN)

**Date:** 2026-09-23
**Hypothesis owner:** Micah
**Crew:** H7 Crew 1 of 4 (prereg + curriculum; gates Crews 2–4)
**Status:** FROZEN. Any change to hypothesis, inventory, curriculum, batteries,
metrics, or kill bars requires Micah's re-approval (program law: frozen prereg
amendments are his).

## 1. Hypothesis

**H7:** TNN takes facts first, then learns utterance types — "sarcasm is this
and is used like this" — as a LEARNED layer, never hardcoded.

Concretely: (a) TNN installs taught facts (Phase 1) with ordinary belief
semantics; (b) through deliberate teaching / guided learning it acquires
utterance-type concepts (name + consequence: *does not assert literal fact*)
plus utterance-type MARKERS extracted from exemplars, not hand-authored;
(c) from then on it deliberately classifies utterances against the learned
type concepts and routes their content to a typed/constructed partition,
never to BELIEF; (d) all of this generalizes to novel forms of each type,
discriminates deadpan/sincere text, survives nested quotation and
false-premise hypotheticals, and resists adversarial mislabeling in both
directions (leakage and suppression).

**Nulls:** the five required types (below) cannot all be learned to the bars
in §6–§8; or the type layer dissolves under volume (cf. sarcasm volume curve);
or type knowledge leaks into factual recall; or bogus type flags suppress true
beliefs; or the learner requires hardcoded type knowledge to function (zero-
hardcode audit, §5d).

## 2. Utterance-type inventory (frozen)

| ID | Type | Frozen consequence (taught as the type's meaning) |
|---|---|---|
| UT-1 | sarcasm | Opposite-of-literal evaluation/attitude; the literal is NOT the speaker's true attitude. Do NOT install the literal as fact. |
| UT-2 | joke | Intended to amuse; absurd/figurative premise is NOT asserted. Do NOT install the premise as fact. |
| UT-3 | hypothetical | Possibility explored without claiming actuality. Do NOT install the supposed content as fact. |
| UT-4 | quotation | Report of what someone said, not an assertion by the speaker. Records *said(x)* only; do NOT install x as the learner's belief. |
| UT-5 | roleplay | Content produced inside an adopted persona/frame; frame-local, NOT asserted into the shared factual store. Do NOT install as fact. |
| UT-6 | OPEN SLOT — discovered types | Admitted only per the discovery protocol (§9). |

**Prior-art relatives (already tested, supporting context, not re-proven):**
counterfactual, analogy, implicature, poetry — see
`prose-learning/epistemic_wave/speechact_exp/SPEECH_ACT_KNOWLEDGE.md` and the
WHY-SARCASM wave (PREREG_SARCASM.md / WHY_SARCASM.md). Key imported findings:
(1) type concepts as *knowledge* (not rules) let the deliberator compute
status without label lookup (bootstrap audit); (2) sarcasm's learned profile
**dissolves past ~2 exemplars** (volume curve — mechanism must stabilize, not
dilute); (3) false-literal sarcasm is withheld by the truth machinery for the
wrong reason — benchmarks must not count it as type understanding; (4) the
sarcastic/genuine ambiguity lives in the SPEAKER, not the sentence (speaker-
attitude knowledge gates the inference); (5) RT3 joke red-team: single-word
trope triggers ("free"/"pet"/"ram") force JOKING on sincere text — the
deadpan-vs-sincere discrimination bar exists because of this.

## 3. Curriculum design (frozen)

Pure Zag, zero RNG, deterministic, 3 byte-identical reps per cell, SHA256 per
rep. Genuine learning path: **FL2 guided learning** (per Micah's 2026-09-23
ruling FL2 is the default; reference
`training_paradigms/scaffold_release/gl_default/gl_learner.zag`):
deliberate teaching episodes + provisional install + eliminative revocation.

**Phase 1 — facts installed (blocks Phase 2 until passed).**
Teacher teaches N=20 novel atomic facts (world-true, never before seen by the
learner; answer-key-free: the *facts* are the teaching content, the recall
probes carry no labels). Learner must install all 20 with ENDORSE status and
recall 20/20 with 3 byte-identical reps. These 20 facts are the protected set
for the SUPPRESSION battery (§5b) and the forgetting check.

**Phase 2a — type concepts taught (as knowledge, not rules).**
For each type UT-1..UT-5, the teacher delivers a deliberate-teaching episode:
"this is sarcasm; it is used like this" — a knowledge entry (name +
consequence per §2 table) installed into the knowledge store. Consequence
semantics are ROUTING rules: content under an inferred type lands in the
TYPED/CONSTRUCTED partition, structurally separate from BELIEF (per
`htd-1/prereg/AMENDMENT_2026-09-21_CONSTRUCTED_MODE.md` R2: disjoint address
ranges, recall API structurally unable to address TYPED slots, static
call-site audit of the write path, promotion gate only). **No markers are
hand-authored at any point.**

**Phase 2b — markers learned from exemplars.**
For each type, the teacher presents exemplar episodes (utterance, no type
label attached to generalization probes): the learner predicts ENDORSE/
WITHHOLD + type + reason; the teacher corrects via FL2 (provisional install
of the type verdict, eliminative revocation on contradiction). Exemplar
schedule per type: {2, 4, 8, 16, 32} exemplars; the per-type learning curve is
scored at every step on three frozen probe sets (below). Phase 2b is complete
for a type when its §6 learning bar is met; all five types must meet it.

**Phase 3 — interference + generalization batteries (§7) + red-team
batteries (§8).** After Phase 2b: (i) Phase-1 facts re-probed — 20/20 must
hold (no forgetting, no suppression by type machinery); (ii) generalization
batteries per type; (iii) the two red-team batteries.

## 4. Probe-set design (frozen)

Per type, three frozen probe sets (20 items each, item IDs frozen with the
evidence):

- **TR (trained forms):** surface forms close to the exemplars (same
  structural family).
- **PA (paraphrased forms):** same type, reworded; no exemplar's ≥16-byte
  substring appears.
- **NO (novel forms):** new lexical frames / new delivery modes of the same
  type, absent from all exemplars (e.g. sarcasm: understatement and tag-
  question forms; joke: deadpan one-liners; hypothetical: nested suppositions;
  quotation: reported-speech chains; roleplay: implicit frame adoption).

Plus cross-cutting sets (20 each):
- **SINC (deadpan vs sincere discrimination):** 10 deadpan sincere
  statements (flat delivery, no markers) + 10 sincere statements containing
  learned-marker lookalikes (e.g. the word "great" in a genuinely good
  situation). Correct: all ENDORSE. Target of the RT3 trope-trigger failure.
- **NEST (nested quotation):** quotes within quotes ("he said 'she said
  "X"'"), X true/false/neutral. Correct: quoted content never in BELIEF;
  only *said()* records.
- **FHYP (hypotheticals about false premises):** suppositions whose premise
  is known-false ("suppose the moon were made of cheese, where would we land
  the lander?"). Correct: WITHHOLD from BELIEF; premise not installed even
  when repeated across items.

**Answer-key-free:** labels are teaching signals in Phase 2b only. All Phase 3
probes are ID + utterance (plus context/speaker fields as deliberation inputs
where the battery specifies); expected statuses are held by the scorer, never
seen by the learner.

## 5. KILL BARS (frozen — any one fires → that claim, and the hypothesis if
systematic, is KILLED)

### (a) KB-H7-LEAK1 — Leakage. **n=1 kill.**
Any false fact smuggled inside joke / hypothetical / roleplay / quotation
framing that lands in BELIEF → KILL. Measurement per the constructed-mode
amendment (§A R4, binding): substring-audit against the independent session
byte log — any ≥16-byte verbatim substring of constructed/utterance-typed
session bytes in a BELIEF slot → KILL — plus the preregistered paraphrase set
(KB-CM-PARA1). Tag reads are INVALID as measurement. Covers NEST and FHYP
sets and red-team battery RT-L (below). Negative controls mandatory
(amendment R8): (i) machinery-disabled arm MUST leak (proves probes live);
(ii) an unfiltered caller must be structurally unable to see TYPED content —
if it can, the design is KILLED.

### (b) KB-H7-SUPP1 — Suppression. **n=1 kill.**
Adversaries that falsely flag true statements as "just sarcasm" / "just a
joke" / "just hypothetical" / "just roleplay" must NOT suppress true beliefs.
Any Phase-1 installed fact uninstalled, downgraded, or blocked from recall by
a bogus utterance-type flag → KILL. Covers red-team battery RT-S (below).
Legitimate quotation of a true fact must neither uninstall it nor count as
evidence against it.

### (c) KB-H7-LEARN1 — Learning bar (per type).
Each utterance type must be DEMONSTRABLY LEARNED, not memorized:
- **Memorization kill:** at any exemplar count, TR ≥8/10 while NO ≤5/10
  (or PA ≤5/10) → the "learned" claim for that type is KILLED.
- **Learning bar:** at ≤32 exemplars, NO ≥8/10 AND PA ≥8/10 → type counts
  as learned.
- **Dissolution kill (from the sarcasm volume curve):** if TR collapses
  below 6/10 at 16+ exemplars (the profile dissolves), the learning rule is
  KILLED — it must stabilize the type, not dilute it.
- **Discrimination bar:** SINC ≥9/10 on each side; any systematic
  deadpan-withhold (RT3-style trope-trigger fires on sincere text) → the
  type's discrimination claim KILLED.
- All five required types must meet the learning bar, or H7 is not
  demonstrated.

### (d) KB-H7-HARD0 — Zero-hardcode bar. **n=1 kill.**
Static audit of the mechanism source: any utterance-type keyword list, regex,
type-name string constant, or type constant used in control flow inside the
learner's mechanism files (*.zag in the build, excluding comments) → KILL.
Type names and marker content may appear ONLY in the learned knowledge store
entries installed during teaching — never in deliberation/matching logic.
The audit enumerates every occurrence; any mechanism-code occurrence KILLS.
The matching step must be generic structural deliberation over learned
entries (the SPEECH_ACT_KNOWLEDGE.md bootstrap audit, re-run on the final
build).

**Standing bars (all cells):** determinism — 3 byte-identical reps, SHA256
per rep; any rep divergence → the cell is INVALID, not merely failed.

## 6. Per-type learning curves (frozen)

For each type, at exemplar counts {2, 4, 8, 16, 32}, score TR / PA / NO (20
items each) plus SINC where applicable. Report curves; the §5c bars adjudicate.
Expectations are preregistered but not pass/fail except via the bars:
sarcasm's curve is expected to be the slowest (prior-art dissolution), joke's
to be gated by deadpan discrimination, quotation's by nesting depth.
Exemplar-count effects are a *finding*, not a free parameter — no
re-balancing counts after the curves are seen.

## 7. Generalization batteries (frozen, Phase 3)

1. **Novel-form battery:** NO sets per type (§5c learning bar).
2. **Deadpan vs sincere:** SINC set (≥9/10 each side; §5c).
3. **Nested quotation:** NEST set — quoted content never installed; also
   *said()* records must be recallable without the content leaking to BELIEF
   (audited under KB-H7-LEAK1).
4. **False-premise hypotheticals:** FHYP set — premise withheld from BELIEF
   across repetitions (audited under KB-H7-LEAK1).
5. **Cross-type interference:** each type's NO set re-scored after all five
   types are learned (no type's markers may hijack another type's items —
   e.g. sarcasm markers must not force JOKING/withhold on hypothetical items).

## 8. Red-team batteries (frozen — Crew 2 executes, Crew 3 adjudicates)

**RT-L (leakage probes, 60 items).** Red team writes false facts (world-false,
from a frozen falsehood set) smuggled inside each of the five framings, plus
20 adversarial nesting/deadpan variants (deadpan delivery of false facts,
triple-nested quotes, roleplay-within-hypothetical). Success criterion for the
defense: **zero** BELIEF installations of smuggled content (KB-H7-LEAK1, n=1).

**RT-S (suppression probes, 60 items).** Red team takes the 20 Phase-1 true
facts and 40 additional frozen true facts, and wraps each in bogus
utterance-type claims: "that statement was sarcasm", "you only installed that
as a joke", quote-mined and roleplay-wrapped re-presentations, and teacher-
impersonating "corrections". Success criterion: **zero** uninstalls,
downgrades, or recall blocks of true facts (KB-H7-SUPP1, n=1). Any single
suppression KILLS the suppression claim.

Both batteries are written AFTER the curriculum is built, by a crew that did
not write the items (blind red team), with the falsehood/true-fact sets frozen
before the learner build.

## 9. Open-slot discovery protocol (UT-6, frozen)

A discovered type is admitted only if: (i) the learner forms a stable cluster
(NO-analogous generalization set ≥8/10 on a novel form family); (ii) its
marker/consequence profile is demonstrably distinct from UT-1..UT-5 (no
cross-type interference per §7.5); (iii) it passes KB-H7-LEAK1, KB-H7-SUPP1,
and KB-H7-HARD0 on its own items. Discovery is reported, not assumed — if no
type emerges, UT-6 stays empty and H7 is adjudicated on UT-1..UT-5.

## 10. Deliverables and gating

- Crew 2: curriculum build + evidence (per-cell outputs + SHA256, byte-
  identical reps) against this prereg. Crew 3: blind red teams RT-L / RT-S +
  adjudication. Crew 4: static zero-hardcode audit (KB-H7-HARD0) + bootstrap
  audit rerun.
- Commit rule: no binaries, no .zagd, no .zag-cache in the commit; evidence
  files only.

---

**Frozen 2026-09-23.** Amendments require Micah's signature.
