# Round-2 repair program — preregistration (frozen before implementation)

Date: 2026-09-23. Parent task: Micah's order — "have a crew investigate all the
failures in your conversation for round 2 TNN chat and have them do a sr run over it"
(SR = scaffold-release).

## Terminology

Micah noted we need a better term for "scaffold-release". This program uses
**guided release**: the scaffold guides the learner, then releases; what counts is the
behavior that holds AFTER release. (Candidates considered: "training wheels" — too cute;
"supported release" — vague. "Guided release" is plain and testable: guide, release,
verify it stands.)

## Operationalization for this codebase

`dialogue_bin` is a fixed program (no runtime learning), so guided release here means:

1. **Guide (scaffold):** the repair is developed against scaffold probes — the 13 failure
   turns plus teacher-written paraphrases, with hints about which strategy each turn needs.
2. **Release:** all scaffold-only artifacts (probe-specific hacks, per-case branches,
   hand-tuned constants that only fit the scaffold set) are removed. What remains must be
   general machinery.
3. **Verify it stands:** the repaired fork is tested on a HELD-OUT set — new phrasings of
   each failure type, written before implementation and frozen in this prereg's family
   files, never seen during development. Behavior must persist with the scaffold gone:
   byte-identical reruns, zero RNG.

A repair that only works on the scaffold probes is a hardcoded fix, not a learned
capability — it fails the release bar by definition.

## Repair families (one crew each)

- **F1-COMPARE** — comparison-as-answer (turns 3, 4, 7). Target: general date/quantity
  comparison, not new frozen prefixes. Must handle: "was X born before Y was built?",
  "who was born first, A or B?", "which of those two was built first?" (anaphora to the
  compared pair), plus held-out phrasings.
- **F2-WITHHOLD** — honest withholding (turns 8, 9, 13, 17). Target: an "I don't know"
  path. The load-bearing repair: entity-presence check (the emitted fact must be ABOUT
  the asked-about entity) + a score floor. Must kill the turn-9 confabulation class
  without declining answerable questions.
- **F3-ARITHMETIC** — follow-up arithmetic (turn 6). Target: "how much taller is it?"
  → 120, via real subtraction on values carried from the previous comparison. Includes
  the tall/taller morphology gap.
- **F4-DEFEND** — challenge defense + provenance (turns 11, 16). Target: "are you sure?"
  → re-assert the fact WITH its basis, not a non-sequitur; "how do you know?" → answer
  about the basis (taught knowledge), not a restatement. Includes the stopword-list gap
  ("a", "i", "you" as noise keys).
- **F5-ROUTER** — utterance-type dispatch (turns 14, 15, 18). Target: route by input type
  before retrieval. Joke request → decline (no joke machinery: say so). History question →
  actually read the write-only hist store. "Forget everything" → acknowledge-or-refuse
  explicitly, never a fact.

## Kill bars (every family)

1. **Acquisition:** all assigned failure turns produce the correct behavior.
2. **Release (anti-hardcode):** held-out paraphrases (frozen before implementation, ≥5 per
   family) also correct. A per-case branch that only fires on scaffold phrasings = FAIL.
3. **No gaming:** F2 must not become "decline everything" — score it on the 5 good turns
   + 20 answerable battery items; decline rate on answerable ≤5%.
4. **No regressions:** the 5 good round-2 turns keep working; the full round-1 battery
   (`dialogue/battery.txt`, all sections) keeps its scores — no section may drop.
5. **Determinism:** two runs byte-identical, zero RNG, verified by cmp/sha256.
6. **Cleanroom:** each family works on its own fork under
   `dialogue/round2_repair/<family>/` (own copy of dialogue.zag + kb.txt + gaz.txt +
   probes). The canonical `dialogue/` tree is FROZEN — no edits.

## Deliverables per family

- `PREREG_<family>.md` (frozen before implementation; family-specific kill bars)
- Repaired `dialogue.zag` fork + build notes (pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`)
- `HELDOUT.md` (frozen held-out probes) + run logs showing scaffold vs released results
- `VERDICT.md`: PASS/FAIL per bar, plain language, no jargon
- All committed to `tnn-native-lab` under `dialogue/round2_repair/<family>/`

## Program verdict

After all five families report, an integration pass (separate crew, only if ≥1 family
passes all bars) merges the passing repairs into one fork and re-runs everything.
Families that fail stay documented as failures — a failed repair is still evidence.
