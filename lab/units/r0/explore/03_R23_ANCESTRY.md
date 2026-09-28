# EXPLORE 03 — R23 ancestry: the teaching experiments behind the taught-vocabulary arm

**Status: EXPLORATORY / NON-BINDING.** Historical analysis from the recovered exact
R23 source (`r23_experiments.py`, SHA-256 `517eb325…`, recovered 2026-09-17; read
from the Drive shadow copy — the pre-git session-file hunt itself stays cancelled
per Micah's ruling). Nothing here changes frozen bars. If pursued, it would amend
**T-14** (teacher-arm verdict weights), **T-11** (curriculum slice design), and the
A-33/T-1 judgment-held-vs-force-pin decision's supporting evidence.

**Frozen context:** Track B has four teacher arms (peer-handwired, RESERVED-invalid,
muse-live, symbolic-hints, sym-yesno-only — T-2); taught words arrive judgment-held
at provisional strength, force-pin only by visible audited trainer action (A-33/T-1);
the 2026-09-21 amendment fixed the installed-vs-learned rule (trainer determines
installed-vs-learned; default is learned; learner can reverse everything except a
visible audited force-pin).

---

## What R23 actually ran

`english_apprenticeship_inversion_experiment(strong_master_payload, seed=23601, n=500)`:

- **Two teachers, one anonymous child.** The child (`AnonymousGroundedLearner`) stores
  only generic parameters + replay. Its boundary contract is explicit: *"English
  strings/labels live in the teacher/evaluator"* and *"no English dictionary
  installed into child."* The teacher owns the English curriculum and grounding;
  the child's weights are generic byte-to-event mappings.
- **Master-taught lane:** a strong master teaches 500 items in fixed curriculum order
  (cycling the foundation list), each item delivered at weight 0.75 (`'MASTER'`) plus
  a direct-world consequence at weight 1.0 (`'DIRECT_WORLD'`).
- **TNN-taught lane:** a mature TNN teaches by **uncertainty-first selection** — each
  step it probes the child, finds the concept with the *lowest prediction margin*,
  and teaches that one (weight 0.6 `'SIBLING'` + 1.0 `'DIRECT_WORLD'`); every 4th
  step it additionally varies the surface form from its own learned neighborhood.
- **Verdict rule:** `'ENGLISH_APPRENTICESHIP_INVERSION': 'PASS_BOUNDED'` iff the
  TNN-taught child beats the master-taught child overall; else `'PARTIAL'`.
  The recorded verdict constant is `PASS_BOUNDED` — the inversion held within the
  tested bounds: **the peer teacher choosing by the child's own uncertainty beat
  the authoritative master teaching a fixed curriculum.**
- **Trust hierarchy, in the code:** `source_rel = {'DIRECT_WORLD':1.0, 'MASTER':.75,
  'SIBLING':.55}` — teacher testimony is *always* discounted relative to direct
  consequence. The sibling teacher's per-item weight (0.6) is below the master's
  (0.75), and the sibling wins anyway — through *selection* (what to teach when),
  not authority.

Supporting boundary statements in the same source:
- Teacher surfaces are *"curriculum data, never copied into learner state as a
  dictionary"* — the ancestor of A-33/T-1's judgment-held (not installed) rule.
- The learner is *"learned byte motifs + recurrent surface generator + separately
  learned raw-byte semantic interpreter; no mutable-TNN English dictionary or
  grammar engine; situation dimensions/world are researcher supplied."*
- The sibling-sharing experiment's boundary: *"same-source repetition is low
  authority relative to direct consequence"* — the ancestor of Z7's trust tiers
  and the §C tripwire's 0.95/0.95/0.90 fire condition.

---

## What this suggests that the frozen design should eventually face

1. **The inversion is a prediction about Track B, and it favors the peer arm.**
   R23's result says uncertainty-first peer teaching beats fixed-curriculum master
   teaching. Track B's arm 1 is the hand-wired peer teacher (Muse does the wiring
   deliberately); arm 3 is muse-live. The frozen design treats all four arms
   symmetrically (T-14 verdict weights unset — Micah hasn't signed them). R23
   predicts the peer arm wins on *episodes-to-criterion* (M2) specifically through
   better selection, not better content. **Proposed amendment (T-14):** when the
   verdict weights are set, include a selection-efficiency component (episodes
   saved by teaching the lowest-margin item first) rather than scoring only final
   mastery — otherwise the design can't see the mechanism R23 found.

2. **"No dictionary installed" is stricter than "judgment-held."** R23's child never
   receives a word→meaning mapping as data; every taught item arrives as a
   *grounded experience* (surface + world event + consequence weight). The frozen
   A-33/T-1 says taught words arrive "judgment-held at provisional strength" —
   which still permits the *form* of a dictionary entry (span + gloss) held weakly.
   R23 suggests the intake format matters: taught vocabulary should arrive as
   experience-shaped updates (surface variation + consequence), never as
   installed entries even weakly held. **Proposed amendment (T-11/T-8):** the
   curriculum slice format should require each taught word to appear in ≥2 surface
   forms with grounded consequences (R23's `SURF` lists give 5 per concept; the
   mature teacher varied them deliberately) — a single canonical gloss per word
   is the dictionary pattern wearing a provisional-strength costume.

3. **The trust hierarchy wants to be a frozen integer schedule.** R23's
   1.0 / 0.75 / 0.55–0.6 weighting (direct > master > sibling) is the direct
   ancestor of Z7's trust tiers and the teacher-touch metric (R-ii). The frozen
   design has the tiers (Z7) but the *numeric* discount schedule for teacher
   testimony vs direct consequence is not yet a sign-off item. **Proposed
   amendment:** add a T-item fixing the testimony-discount ladder (direct
   consequence = 1.0 by definition; teacher weights < 1.0, frozen integers),
   with R23's 0.75/0.6 as the proposed values to approve-or-amend.

4. **A question R23 leaves open that the frozen design must not dodge:** in R23,
   the *teacher* knew English and the *world* supplied grounding; the child was
   anonymous. In Track B, who plays "world"? If the teacher is also the
   consequence-giver (as in the flaw-manifest setup, T-3), the 1.0-weight
   `'DIRECT_WORLD'` channel doesn't exist independently — and R23's result
   depended on that channel being present and heaviest for *both* lanes. If the
   frozen teacher track can't separate "teacher says" from "world shows," the
   ancestry suggests the taught arm is testing a weaker claim than R23 tested.
   **Proposed amendment (T-11):** curriculum slices must include a
   teacher-independent grounding channel (the analog of `'DIRECT_WORLD'` at
   weight 1.0), or the trial records that it omitted R23's heaviest channel.

5. **Learned-vs-installed, R23's version:** R23's learner could and did revise
   taught mappings (the misinformation-trap leg: five repeated sibling copies of
   a wrong mapping vs one direct consequence — recovery measured). That is the
   2026-09-21 installed-vs-learned amendment's "learner can reverse everything
   except a visible audited force-pin" in ancestral form, *with a measured
   recovery rate*. The frozen design should face the same measurement: **proposed
   amendment (arm O kill criterion):** add R23's misinformation-recovery leg
   (repeated teacher testimony for a false mapping vs one direct consequence —
   does the learner recover?) as an explicit sub-bar of O-(ii)/(iii).

---

## Relation to frozen bars

| Ancestry point | Frozen bar it would amend (if pursued) |
|---|---|
| Inversion → selection-efficiency scoring | T-14 (verdict weights) |
| Surface-variation requirement for taught words | T-11 (slice design), T-8 (hint format) |
| Testimony-discount ladder as frozen integers | new T-item (propose T-17) |
| Teacher-independent grounding channel | T-11 (slice composition) |
| Misinformation-recovery leg for taught mappings | A-33 / arm O kill criterion (ii)/(iii) |

All EXPLORATORY. The frozen teacher track is untouched; these are dated
amendment proposals awaiting Micah's word, per §0 RULE-9.
