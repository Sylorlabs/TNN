# Treadmill Guard Integration into the TNN-3 Preregistration Structure

**Status: DRAFT integration spec.** This document specifies where the
treadmill guard belongs in the TNN-3 preregistration and drafts the
integration text for each insertion point. It does not edit the
preregistration structure or the guard. It governs nothing until
Micah reviews the preregistration and a TNN-3 preregistration
freezes the bars it covers.

**Inputs:**
- Treadmill guard: commit `1646b9732`
  (`treadmill_guard/TREADMILL_GUARD.md`). A 5-check development
  discipline document. Explicitly not a kill bar.
- TNN-3 preregistration structure: commit `206499c03`
  (`tnn3_prereg_struct/PREREG_STRUCTURE.md`). 10-section outline,
  17-bar inventory, dependencies, order, gaps, 6 open questions.
  DRAFT-NOT-FROZEN.

---

## 1. Design decision: one reference, four insertions, two notes

The guard is a discipline document, not a bar, so it does not get
its own preregistration section. Instead it is referenced once at
the preregistration's identity level (so it is visible from the
top) and woven into the four sections where it has operative
content, plus two cross-reference notes where it reinforces
existing material.

| # | Location | Kind | What it does |
|---|---|---|---|
| A | Section 1, new 1.5 | Reference | Names the guard as the governing development discipline |
| B | Section 2, end-of-section note | Note | Points builders to the per-capability treadmill analyses |
| C | Section 3, Step 4 row | Note | Attaches warning sign 5 to the H1-widening constraint |
| D | Section 6, new 6.9 | Insertion | Menu check becomes an architecture-accounting line item |
| E | Section 8, new 8.6 | Insertion | The five checks, in full, as a verification procedure |
| F | Section 10, new 10.4 | Insertion | Treadmill guard audit in governance |

Rationale for this placement: Section 8 is where the checks live
because they are verification procedures run on every proposed
change. Section 1.5 is where the reference lives because the guard
conditions the whole preregistration. Section 6.9 is where the menu
check lives because counting researcher-enumerated schema families
is architecture accounting. Section 10.4 is where the audit lives
because the guard-gaming modes (guard section 5) are audit
material. The Section 2 and Section 3 notes are reinforcements, not
new obligations.

What this does NOT do: it does not turn the guard into kill bars,
it does not add new bars to the inventory, it does not change any
bar text, and it does not resolve Micah's 6 open questions.

---

## 2. Insertion A: Section 1, new subsection 1.5

Insert after 1.4 ("What this preregistration covers"). Existing 1.5
does not exist, so no renumbering is required.

Draft text:

> ### 1.5 Development discipline: treadmill guard
>
> This preregistration references the treadmill guard (commit
> `1646b9732`,
> `treadmill_guard/TREADMILL_GUARD.md`), which is a development
> discipline document, not a kill bar. Every proposed TNN-3 change
> must pass the guard's five checks (guard section 3): (1) SUF
> check, (2) anti-gaming check, (3) generality check, (4) property
> check, (5) menu check. A change that fails check 1 or 2 is
> rejected. A change that fails check 3, 4, or 5 is returned for
> redesign with the failure named. The guard's warning signs
> (guard section 2) and guard-gaming modes (guard section 5) are
> part of the review discipline for every change. The five checks
> are stated in full in section 8.6 of this preregistration, and
> the guard audit is specified in section 10.4.

---

## 3. Insertion B: Section 2, end-of-section note on floor capabilities

Section 2 lists the frozen kill bar text. Append the following note
at the end of section 2 (after 2.8), so builders see it before
implementing anything the floor tests cover.

Draft text:

> ### Note on floor capabilities and the treadmill guard
>
> Each of the seven floor capabilities (F1/F2/F3/G1/G2/G3, floor
> spec commit `f383dd11c`) has a documented treadmill form and a
> named guard mechanism in the treadmill guard (commit `1646b9732`,
> section 4). The floor tests keep the floor; the guard names how
> each floor test could be gamed. For example: F1 recall can be
> gamed by pre-loading answers or world-ID-indexed fact tables
> (caught by the anti-gaming check, guard check 2); G3 inquiry
> discrimination can be gamed by hardcoding CHOICE 30 for test
> keys (caught by novel-key probes under check 2), and presenting
> G3's constant act as FW6 contingent inquiry is failure-mode
> preservation (guard section 1). Builders should read the
> per-capability treadmill analysis before implementing any
> change that touches a floor capability.

---

## 4. Insertion C: Section 3, Step 4 row note

In the Section 3 order summary table, the Step 4 row already
carries the treadmill warning ("This step must not precede Step
1, per the treadmill warning"). Append a precise citation so the
warning is auditable.

Draft text to append to the Step 4 row's Prerequisites cell:

> Treadmill guard warning sign 5 (commit `1646b9732`, section 2)
> applies: widening the constructor while the oracle still supplies
> answers through verification is the treadmill's favorite move.
> Step 1 (H2 probes) must be complete and recorded before Step 4
> begins. A Step 4 proposal that cannot show the Step 1 results
> fails guard check 3 (generality) and is returned for redesign.

---

## 5. Insertion D: Section 6, new subsection 6.9

Insert after 6.8 ("ISA freeze attestation"). Existing 6.9 does not
exist, so no renumbering is required.

Draft text:

> ### 6.9 Researcher-enumerated schema families (menu check)
>
> Count of researcher-enumerated schema families (templates,
> operators, fixed wirings, literal bounds) in each affected
> mechanism, recorded before and after the change (treadmill guard
> check 5, commit `1646b9732`, section 3). A real advance moves
> schema decisions into learner state; it does not increase the
> menu. A menu increase with no corresponding SUF gain is the
> treadmill's signature move (guard warning signs 1 and 7). This
> count is recorded alongside the capability-source delta statement
> (6.7) and is part of the architecture accounting for every
> adopted change.

---

## 6. Insertion E: Section 8, new subsection 8.6

Insert after 8.5 ("No weakening after results"). Existing 8.6 does
not exist, so no renumbering is required. This is the primary
operative insertion: the full five-check text.

Draft text:

> ### 8.6 Treadmill guard: five checks on every proposed change
>
> Before any proposed TNN-3 change is adopted, run the five
> treadmill guard checks (commit `1646b9732`, section 3).
>
> **(1) SUF check (primary).** Run the SUF operational test
> (commit `64eec921f`, section 5) on the new or changed mechanism:
> list every structural decision the learner can make that the
> source cannot (topology, wiring, operator arrangement, ordering,
> bounds, acceptance criteria that select among forms). If the
> list is empty, the mechanism cannot move any cluster, and the
> change is treadmill by definition. No score movement overrides
> this.
>
> **(2) Anti-gaming check.** Run the seven floor tests (floor spec
> commit `f383dd11c`, section 4) with no more researcher
> scaffolding than TNN-2 needed: same teaching sequences, no
> manual state resets between probes, same determinism requirement
> (three runs, byte-identical transcripts). If any test needs a
> crutch TNN-2 did not need, that is a regression in learner
> autonomy per floor spec criterion 4, even if the score matches.
>
> **(3) Generality check.** Name every freeze/GW world the change
> is expected to move, and name the shared architectural cause it
> addresses (re-clustering commit `ed2357141`, cause clusters
> R1/R2/R3 plus the C0-D shadow). A change expected to move
> exactly one world must name the general mechanism it reveals;
> otherwise it is a one-world patch and is rejected.
>
> **(4) Property check.** State the property the change adds, not
> just the capability. Map it to the target cluster's SUF
> sub-property: FW3 history-parameterized generativity, FW6
> epistemic-state-contingent discrimination with a resolution
> transition, FW7 goal-conditioned composition, FW8 combinatorial
> novelty, FW9 learner-scaled search (commit `64eec921f`,
> section 4). If the preregistration names only a capability
> ("add construction"), it is underdetermined and treadmill-risky;
> it must name the property. The property statement must be
> falsifiable: state what observation would show the property
> absent (guard section 5, gaming mode 2).
>
> **(5) Menu check.** Count researcher-enumerated schema families
> (templates, operators, fixed wirings, literal bounds) in the
> affected mechanism before and after the change. A real advance
> moves schema decisions into learner state; it does not increase
> the menu. A menu increase with no corresponding SUF gain is the
> treadmill's signature move.
>
> Disposition: fail check 1 or 2 means reject; fail check 3, 4,
> or 5 means return for redesign with the failure named. Record
> the five-check outcome for every adopted change in the
> governance log (section 10.4).

---

## 7. Insertion F: Section 10, new subsection 10.4

Insert after 10.3 ("Contamination checks"). Existing 10.4 does not
exist, so no renumbering is required.

Draft text:

> ### 10.4 Treadmill guard audit
>
> The governance audit verifies that the treadmill guard was
> applied to every adopted TNN-3 change:
>
> - The five-check outcomes (section 8.6) are on record for every
>   adopted change, with the disposition (adopted, rejected,
>   returned for redesign) and the named failure where applicable.
> - The warning signs (guard section 2) were reviewed for every
>   change. Two or more warning signs is a strong presumption of
>   treadmill and must be answered in the governance log, not
>   waved through.
> - The guard-gaming modes were watched for (guard section 5):
>   (a) SUF theater, running the check on the selector knob rather
>   than the schema set; (b) checklist compliance without
>   property, vague property statements that match any outcome;
>   (c) floor-only optimization, all effort going into keeping the
>   seven floor tests green while no kill bar moves.
>
> Track kill-bar movement alongside floor status. A flat kill-bar
> count across two consecutive build cycles with a green floor is
> the treadmill running quietly; the audit flags it and the
> program must explain why the next cycle will differ.

---

## 8. Consistency notes for the preregistration author

1. **No renumbering needed.** All six insertions use subsection
   numbers that do not currently exist (1.5, 6.9, 8.6, 10.4) or
   are end-of-section notes (B, C). No existing text moves.
2. **Guard stays a discipline, not a bar.** None of the insertions
   promote the guard to kill-bar status. It conditions how changes
   are reviewed; the bars condition what passes.
3. **The guard's own status line is preserved.** The guard states
   it "governs TNN-3 work only if a frozen preregistration
   references it." Insertion A is that reference. Until Micah
   reviews the preregistration and a TNN-3 preregistration freeze
   commits, the guard governs nothing.
4. **Interaction with the 6 open questions.** The insertions do
   not resolve any of Micah's 6 open questions (section 7 of the
   prereg structure). The property check (8.6.4) requires a
   falsifiable property statement per change; that is orthogonal
   to the bar-text questions.
5. **Interaction with gap 5a.1 (H2 has no kill bar).** The guard
   does not add a K-H2 bar. Warning sign 5 and the Step 4 note
   (insertion C) are the guard's H2-related content; a dedicated
   K-H2 bar remains a separate drafting decision (bar inventory
   commit `1722884ad` tracks K-H2-1..4 as DRAFT-NOT-FROZEN).

## Verdict

GUARD-INTEGRATION-COMPLETE.

Six integration points specified (one reference, two notes, three
operative insertions), with draft text for each, ready for the
preregistration author to apply once Micah's review lands.
