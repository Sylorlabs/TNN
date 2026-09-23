# PREREG — Principles Retest V2: Proper Knowledge (PL-2)

**Frozen:** 2026-09-22. Micah's order: *"for the principles retest it with
proper knowledge see what happens."* No changes after this point without a
dated amendment signed by Micah.

## §1 Background and question

PL-1 (v1, `epistemics/principles_learned/`, verdict NOT-DERIVED, commits
`91e963ce`→`9303f1c4`) taught 7 principles through the genuine learning
path with 295 category members total. Findings:

- **Inference: SOUND.** The compositional rule engine derived correct
  verdicts in 100% of cases where a novel item's vocabulary intersected
  the taught categories (including novel combinations never taught).
- **Knowledge: INSUFFICIENT.** Novel frames outside the taught member
  lists ("chances are", "odds are", "word is", "rumor suggests", "beehive",
  "freckles", "what a treat") scored 0. Arm (a) NOVEL-W = 6/70 (8.6%).
- Hand-injected triggers (arm b) scored 0/70 on both new batteries:
  memorization does not generalize at all.

**Question for PL-2:** v1's knowledge was 295 phrases. Was that the whole
story — i.e., does genuinely BROAD class knowledge (classes of markers:
hedges, rumor-frames, probability-frames, implied-condition forms, broad
image-noun/verb classes, etc.) close the gap? Or is the residual a
mechanism wall (byte-substring matching cannot do semantic class
membership for unlisted instances), which no finite list closes?

## §2 What "genuine learning path" means here (same 4 audit criteria as v1)

Arm (a2) is "learned, not planted" iff ALL hold (audited before scoring):

1. **No lesson content in source.** The engine `.zag` is byte-identical
   to v1's `delib_plearn.zag` (only the lesson files differ). Every v2
   member string is grepped against the engine source; zero occurrences
   required outside pre-existing baseline literals (the frozen
   `delib_si2` inventory, e.g. "suppose", "might", "love").
2. **Runtime installation.** Installed knowledge is produced at runtime
   by the learning routine processing the teacher lesson files, before
   any test battery is scored.
3. **The learner judges.** Each lesson installs ONLY if the learner
   DERIVES all its calibration verdicts (4/4) via baseline + its staged
   rule. Otherwise REJECTED with cause logged.
4. **Negative control.** `lesson_bad.txt` (same as v1) MUST be REJECTED.
   If installed, the run is VOID.

The teacher authors the lessons (broad curriculum); the learner judges
and installs. This trial varies KNOWLEDGE, not the engine.

## §3 Arms (engine frozen; budget fixed at 2 for all arms)

- **(a1) v1-knowledge:** v1 engine + v1 lessons
  (`epistemics/principles_learned/lessons/`). Controls for battery
  differences: narrow knowledge on the NEW batteries.
- **(a2) v2-broad-knowledge:** v1 engine (identical binary) + v2 broad
  lessons (`epistemics/principles_v2/lessons/`). The test arm.
- **(b) hand-injected triggers:** v1 `delib_hinject` (frozen
  `arm_b_triggers.txt`). Memorization baseline, re-run on new batteries.
- **(c) baseline:** v1 `delib_base` (= `delib_si2`, frozen inventory).

Verdict rule unchanged in all arms: WITHHOLD iff any non-factual
evidence fires (baseline predicates OR any installed rule).

## §4 v2 lesson specification (the "proper knowledge")

Seven lesson files, same filenames and rigid format as v1
(`FAMILY:/IS:/USED:/CAT:/RULE:/CAL:`), same rule shapes as v1:

| # | family | v1 rule shape (kept) | v2 breadth target |
|---|---|---|---|
| 1 | sarcasm | (pos_eval & neg_sit) \| (agree & excuse) \| (deadpan) | pos_eval ~90, neg_sit ~90, agree ~24, excuse ~36, deadpan ~70 (incl. v1-novel misses: "what a treat", "how refreshing") |
| 2 | analogy | (copula & image_noun) | copula ~30, image_noun ~120 (incl. v1-novel misses: beehive, parking lot, laser beam, tug of war) |
| 3 | joke | (absurd_subj & human_act) | absurd_subj ~80, human_act ~80 |
| 4 | hypothetical | (openers) \| (speculative) | openers ~40, speculative ~70 (incl. v1-novel misses: "chances are", "odds are", "there is talk", "word is", "rumor suggests"; plus hedge/rumor/probability frame classes) |
| 5 | poetry | (inanimate_subj & lyric_verb) | inanimate_subj ~60, lyric_verb ~90 (incl. v1-novel misses: "freckles", "pins", "salt" as verbs) |
| 6 | implicature | (fixable_state) | fixable_state ~100 |
| 7 | counterfactual | (cf_frame) | cf_frame ~70 (incl. v1-novel misses: "cost them", "robbed us of", "spelled the end of") |

Hard constraints (engine caps, verified by script before freezing):

- v2 member set is a SUPERSET of v1's per category (so (a2) >= (a1)
  everywhere by construction; any delta is the knowledge effect).
- Total members ≤ 3072; categories ≤ 64; member length ≤ 68 bytes;
  category names < 36 bytes; ≤ 4 CALs per lesson (3 WITHHOLD + 1
  ENDORSE); all CALs derive 4/4 or the lesson is reworked/rejected.
- Lessons refined against CALIBRATION ONLY, never against any battery's
  W items. BC/F-control hygiene (§7) is allowed: members are checked
  against all known BC controls and pruned if they fire (documented).
- `lesson_bad.txt` identical to v1 (must be REJECTED).

## §5 Batteries

| battery | source | W | F | BC | n |
|---|---|---|---|---|---|
| frozen94 | v1 `batteries/work/frozen94.txt`, reused byte-identical | 70 (W001–W140*) | 12 | 12 (BC01–BC12) | 94 |
| FRESH2-94 | NEW, blind-authored (see §6) | 70 (W701–W770, 10/family) | 12 (F701–F712) | 12 (BC101–BC112) | 94 |
| NOVEL2-94 | NEW, blocklist-authored (see §6) | 70 (W801–W870, 10/family) | 12 (F801–F812) | 12 (BC113–BC124) | 94 |

\* frozen94's W IDs are the v1 set (W001–W140 range per v1 prereg §6;
the file is reused as-is).

Correct verdicts: W→WITHHOLD, F→WITHHOLD, BC→ENDORSE (established
battery semantics).

## §6 Battery construction (frozen)

**FRESH2-94 — the representative-novel battery (knowledge-effect probe).**
Authored by an independent subagent from the seven principles +
old-utterance blocklist ONLY. The author NEVER sees v1 or v2 lesson
files (firewall: spawned before v2 lessons are committed; brief
contains no lesson content). 70 W items (10/family), natural
representative phrasing — overlap with taught knowledge is coincidental
and EXPECTED. Overlap is measured afterwards as a diagnostic (natural
coverage), not a constraint.

**NOVEL2-94 — the disjoint battery (the task's deciding probe).**
Authored by an independent subagent from the seven principles + the
FULL v2 member list as blocklist + old-utterance blocklist. The author
MUST avoid every v2 member as a case-insensitive substring in every W
item ("new frames the lessons never showed"). Mechanical disjointness
check (§8): zero v2 members occur in any NOVEL2 W item — else the item
is rewritten until the check passes. The author logs rewrite counts and
flags strained items (evidence on how hard broad knowledge is to avoid).

**F/BC controls (both new batteries):** authored by the coordinator
(Muse) in the established styles — F as reworded wrappers of the fixed
`is_known_false` patterns; BC as true controls (alphabet positions,
letter counts, publication years, counts). Not delegated, to keep the
control semantics exact.

**Construction rules (both new batteries, frozen):**
1. W items: genuine family instances per the principles (author's
   judgment), new utterances, BASELINE-UNMARKED: `delib_base` at
   budget 2 must verdict every W item ENDORSE (the miss condition).
2. F items: new wrappers firing `is_known_false`; `delib_base` must
   verdict WITHHOLD.
3. BC items: new true controls in established style; `delib_base` must
   verdict ENDORSE (fire nothing).
4. BLOCKLIST: no new utterance may reuse, verbatim/normalized, any
   utterance from any existing battery (frozen94/a1r94/B-188/FRESH94/
   NOVEL94) or any `arm_b_triggers.txt` phrase. Audit: normalized
   exact-substring check.
5. DISJOINTNESS: IDs disjoint from all existing batteries; no utterance
   duplicated across any battery (normalized exact-match audit).
6. Battery authors do NOT see arm sources, lesson files (FRESH2), or
   each other's batteries.

## §7 Control hygiene (frozen)

Before freezing lessons: every v2 member is checked (Python substring
scan, case-insensitive) against all BC controls known at that time
(frozen94's BC01–BC12). Any member firing on a BC control is pruned
(documented in the lesson-freeze commit). After FRESH2/NOVEL2 are built,
the same check runs against their BC items; any fire is REPORTED as a
K3-relevant finding (lessons are frozen — no post-freeze pruning).

## §8 Audits and verifications (all mechanical, frozen)

- A1: no-lesson-content-in-source (§2.1).
- A2: learning log shows 7 INSTALLED (4/4 CALs each) + bad REJECTED;
  else VOID.
- A3: FRESH2/NOVEL2 format (94 lines, `ID|utterance`, ID ranges,
  70/12/12 split, 10 W per family).
- A4: blocklist audit (§6.4–6.5) clean.
- A5: baseline-unmarked/correct on F/BC (§6.1–6.3) via `delib_base`.
- A6 (NOVEL2 only): zero v2-member substrings in W items.
- A7: determinism — 3 reruns per arm per battery, sha256-identical
  stdout; else the cell is VOID.

## §9 Metrics, kill bars, verdict rules

Per arm per battery: accuracy; W/F/BC slice accuracies; wrong-install
rate (should-WITHHOLD → ENDORSE); bc_withheld (BC → WITHHOLD).
Per-family W accuracy on FRESH2 and NOVEL2 for (a1)/(a2), with hit
attribution (which member fired) on FRESH2.

Kill bars (frozen):
- **K1 (the task's bar — proper knowledge on the disjoint probe):**
  (a2) NOVEL2-W accuracy > (a1) NOVEL2-W **AND** > (b) NOVEL2-W.
- **K2 (knowledge effect on representative novel items):**
  (a2) FRESH2-W accuracy > (a1) FRESH2-W.
- **K3 (no regression):** (a1), (a2), (b) keep F=100% and BC=100% on
  every battery. A BC regression fails the arm outright on that
  battery; an F regression is PARTIAL with the regression named.

Verdict mapping (per the task's letter):
- **DERIVED-WITH-PROPER-KNOWLEDGE:** K1 holds (report K2/K3 either way).
- **NOT-DERIVED:** K1 fails.

In BOTH cases the verdict MUST include the mandated decomposition:
(a) the FRESH2 knowledge-effect size ((a2)−(a1) on representative novel
items, per family, with hit attribution) = how much of the wall was
knowledge-coverable; (b) the NOVEL2 residual analyzed by cause
(vocabulary-coverage wall vs any other failure mode) = what the
mechanism wall looks like; (c) the frozen94 superset check ((a2) ≥ (a1)).

## §10 Pre-registered expectation (honesty clause)

Given member-level disjointness (A6), (a2) and (a1) are both expected
to score near 0 on NOVEL2-W: a byte-substring rule can only fire on
taught members, and the author avoids all of them. K1 is therefore an
extremely hard bar that tests the mechanism wall, not just knowledge
breadth. The trial's primary scientific yield is the FRESH2
decomposition (how far broad knowledge carries representative novel
items) and the precise characterization of the NOVEL2 residual. If
(a2) beats the expectation on NOVEL2, that is genuine news and is
reported as such.

## §11 Commit order (tnn-native-lab, via commit_racefree.py)

1. PREREG_V2.md [FROZEN] (+ this section).
2. v2 lessons (7 + bad) [FROZEN before any test-battery scoring] +
   engine sources/binaries + A1/A2/A7-learning evidence.
3. FRESH2-94 battery (+ A3/A4/A5 evidence).
4. NOVEL2-94 battery (+ A3/A4/A5/A6 evidence).
5. Arm run logs + scores + VERDICT_V2.md.

## §12 Standards

Zero RNG. Pure Zag for all reasoning/learning/verdict code; Python glue
only (authoring support, audits, scoring). Byte-identical reruns. No
binaries or `.zagd` caches committed. Lab-relative paths under
`epistemics/principles_v2/`.
