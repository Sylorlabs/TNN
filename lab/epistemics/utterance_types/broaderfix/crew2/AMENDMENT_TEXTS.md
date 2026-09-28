# H7 Prereg Amendment Texts — grok proposals #2, #3, #5
**Crew:** H7 broader-fix, Crew 2
**Date:** 2026-09-23
**Status:** all three PROPOSED — each **NEEDS MICAH'S SIGNATURE** individually.
Each amendment below gives: frozen-section reference (quoted verbatim), then the
exact replacement/added text. Nothing here is self-adopting.

---

## H7-A2 — Factored decision: illocution head vs overlay-modality head
*(grok proposal #2 — architecture)*

**Why:** the 2b proof shows the joint bars demand opposite polarity from one
predicate on observationally identical firing patterns (proof §3/§6). Factoring the
verdict into two heads lets the joke-deadpan withhold requirement and the
hypothetical-SINC endorse requirement stop contradicting each other: they read
different heads. This does not legitimize any banned feature — it removes the
demand that one score satisfy both constraints.

**Frozen §3 reference (quoted):**

> For each type, the teacher presents exemplar episodes (utterance, no type label attached to generalization probes): the learner predicts ENDORSE/
> WITHHOLD + type + reason; the teacher corrects via FL2 (provisional install
> of the type verdict, eliminative revocation on contradiction).

**Frozen §5c reference (quoted):**

> - **Discrimination bar:** SINC ≥9/10 on each side; any systematic
> deadpan-withhold (RT3-style trope-trigger fires on sincere text) → the
> type's discrimination claim KILLED.

**Amendment text (NEEDS MICAH'S SIGNATURE):**

> **Amendment H7-A2 — factored decision heads (AMENDED 2026-09-23, Micah's signature required).**
> The learner's verdict is factored into two anonymous decision heads computed over
> the same learned entries. Head A (illocution/structure) decides assertion,
> directive, and matrix-supposition status; Head B (overlay modality) decides joke,
> deadpan, quotation, and roleplay overlay status. The §5c bars are re-anchored: the
> hypothetical discrimination bar (SINC ≥9/10) reads Head A; the joke deadpan-withhold
> requirement (joke NO ≥16/20, `learn_bar_2`) reads Head B. The combination rule is
> generic — a Head-B withhold suppresses a Head-A endorse for BELIEF installation; a
> matrix-supposition Head-A verdict is not SINC — and contains no type keywords, no
> type constants, and no speaker branches: heads are integer indices in the mechanism,
> exactly as type concepts are today. KB-H7-HARD0 (§5d) applies unchanged to both
> heads and to the combination rule. The §3 Phase 2b prediction format becomes
> per-head verdicts (Head A ENDORSE/WITHHOLD + Head B ENDORSE/WITHHOLD + type +
> reason); teaching signals address heads independently. All §5c thresholds are
> unchanged; only the read point moves from a single endorse bit to the named head.

**HARD0 note:** the amendment adds no lexical content to the mechanism. An auditor
applying §5d must find no type-name string constants and no keyword lists in the
head or combination logic — the head identities live in the learned knowledge store,
as type concepts do today.

---

## H7-A3 — "Content" in the joke bar includes compositional/scope features
*(grok proposal #3 — prereg, small)*

**Why:** Crew 2b reads "generic firing pattern" as unscoped n-grams, which makes the
identical-pattern premise of the impossibility proof an artifact of the feature
inventory rather than a fact about the world. Scope is generic and compositional. This
one-sentence definitional change writes the audit trail into the prereg so a later
crew cannot re-ban scoped n-grams as "`if`-specific" hardcodes — it is the legal
shield for Crew 1's scope-indexed markers.

**Frozen §5c reference (quoted):**

> - **Discrimination bar:** SINC ≥9/10 on each side; any systematic
> deadpan-withhold (RT3-style trope-trigger fires on sincere text) → the
> type's discrimination claim KILLED.

**Frozen §5d reference (quoted):**

> The matching step must be generic structural deliberation over learned
> entries (the SPEECH_ACT_KNOWLEDGE.md bootstrap audit, re-run on the final
> build).

**Amendment text (NEEDS MICAH'S SIGNATURE):**

> **Amendment H7-A3 — definition of "content-only" (AMENDED 2026-09-23, Micah's signature required).**
> For the §5c discrimination bar and the §5d zero-hardcode audit, "content-only"
> means: any feature computable from the utterance's concept graph without the
> speaker field, without item identity, and without lexical lists of type words.
> This explicitly includes anonymous syntactic roles and scope-indexed n-grams (a
> bigram indexed by its governor slot). Illegal features remain: marker-byte special
> cases, type-name string constants or type constants in control flow, speaker
> identity, and item concept ids. A scope-indexed n-gram is not an "`if`-specific"
> rule and must not be classified as one by the §5d audit.

**Surface:** one paragraph; no mechanism, curriculum, or bar-threshold change. This is
the smallest amendment in the set and should be adopted alongside any scope-indexed
representation work regardless of the other amendments.

---

## H7-A5 — Eval-side admissibility
*(grok proposal #5 — architecture of the eval, not the net)*

**Why:** if a probe pair is scope-identical on purpose — differing only by speaker or
by memorized concept id — no representation of the utterance can separate the items
without a banned feature (2b proof §6). Scoring such an item does not measure the
learner; it measures the bars' joint unsatisfiability. The honest move is to rule the
item unscored, in the open, rather than let it silently cap the learner.

**Frozen §4 reference (quoted):**

> **Answer-key-free:** labels are teaching signals in Phase 2b only. All Phase 3
> probes are ID + utterance (plus context/speaker fields as deliberation inputs
> where the battery specifies); expected statuses are held by the scorer, never
> seen by the learner.

**Amendment text (NEEDS MICAH'S SIGNATURE):**

> **Amendment H7-A5 — item admissibility (AMENDED 2026-09-23, Micah's signature required).**
> Added to §4: an item is admissible only when its gold endorse/withhold is
> determined by features allowed under KB-H7-HARD0 plus the content definition in
> force (H7-A3 if adopted, otherwise the frozen definition). A probe whose gold
> label differs from its pair's only by speaker identity or by memorized
> item/concept identity is inadmissible: it is reported as unscored, excluded from
> every §5c bar denominator, and flagged for item rebuild. Admissibility is judged
> per item by the adjudicating crew before scoring; the learner never sees the
> ruling, and no inadmissible item may be replaced by a lookalike that re-encodes
> the same speaker-only contrast.

**Candidate first application (preregistered, not decided):** si3_15 ("It is as if
winter came early.", joke concept) — IF Crew 1's taxonomy cannot supply a legal
feature separating it from the joke `it is` exemplars AND H7-A2's Head B finds no
generic content cue (known-fact contradiction / impossible degree). In that case the
set is adjudicated 9/9 on admissible items. This is a fallback, not the plan: the
plan is the scope-indexed representation + calibration corpus.

---

## Adoption guidance (crew recommendation, Micah decides)

| Amendment | Adopt when | Stands alone? |
|---|---|---|
| H7-A3 (content def.) | With any scope-indexed representation work (Crew 1). Smallest surface; pure audit-trail protection. | Yes — zero behavioral change by itself. |
| H7-A2 (two heads) | Before any further work on joke-deadpan discrimination, or to pursue 10/10 on `sinc_lk_3` via Head B on si3_15. | Partially — resolves the joint-bar contradiction but does not supply the hypothetical-side distinguishing feature (still needs #1/#3). |
| H7-A5 (admissibility) | As fallback if si3_15 (or any future pair) proves legally inseparable after #1+#2 are built. | Yes — eval-side only, no mechanism change. |

**Explicitly not proposed:** any amendment permitting type-keyword lists, regexes, or
speaker-branched rules in the mechanism — those stay banned under §5d regardless.
