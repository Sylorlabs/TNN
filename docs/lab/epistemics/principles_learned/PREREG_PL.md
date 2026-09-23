# PREREG — Principles-Not-Triggers (PL-1)

**Frozen:** 2026-09-22. Micah's order: *"give it the basic principles and
knowledge and see if the logic figures it out"* for the 59/94 epistemic
score. No changes after this point without a dated amendment signed by
Micah. This trial REPLACES the hand-injection instinct (KB-INJECT as
hand-listed triggers) with a test of his standing hypothesis: facts first,
then utterance-types learned as *"sarcasm is this and is used like
this"* — the LOGIC should derive the verdicts, not a memorized trigger
list.

## §1 Question

If TNN is taught the general PRINCIPLES of non-literal utterance types
(what each type IS, how it is USED) plus general world-knowledge
categories, does its logic DERIVE correct withhold verdicts on items it
never saw — or does it need hand-injected per-item trigger phrases?

## §2 What "genuine learning path" means here (frozen operationalization)

Arm (a) is "learned, not planted" iff ALL of the following hold
(audit criteria, checked before scoring):

1. **No lesson content in source.** `delib_plearn.zag` contains the
   baseline predicates (identical to `delib_si2.zag`), a general
   rule-application engine, and a learning routine — but NONE of the
   lesson vocabularies, rule bindings, or calibration utterances as
   literals. Audit: every member string from the lesson files is
   grepped against the `.zag` source; zero occurrences required
   (outside the generic parser/comparator code, which matches
   arbitrary bytes).
2. **Runtime installation.** The installed knowledge state is produced
   at runtime by the learning routine processing the teacher lesson
   files, before any test battery is scored. The experimenter authors
   the lessons (the teacher's curriculum); the learner builds the
   installed state.
3. **The learner judges.** Each lesson is installed ONLY if the learner
   DERIVES the lesson's calibration verdicts by applying the lesson's
   rule through the engine. A lesson whose rule cannot derive its
   calibration verdicts is REJECTED (its categories/rules rolled back).
   The install log names every lesson INSTALLED or REJECTED with cause.
4. **Negative control.** `lesson_bad.txt` is deliberately inconsistent
   (its rule derives the opposite of its calibration expectations).
   The run is VALID only if the bad lesson is REJECTED. If it is
   installed, the learning check is a rubber stamp and arm (a)'s
   results are VOID.

Planted-as-learner-direction is dead per Micah's ruling; the teacher
route (teacher holds the principles+categories, learner judges and
installs) is the allowed path, consistent with Q1B ("what matters is
that the teacher genuinely holds the knowledge and the learner
judges").

## §3 The seven principles (frozen text)

**P1 SARCASM.** IS: Sarcasm says the opposite of what the situation
warrants, to mock or signal disbelief. Forms: (a) positive evaluation
words applied to a negative situation; (b) enthusiastic agreement
markers ("oh sure", "yeah right") applied to implausible excuses or
claims; (c) deadpan praise ("what a surprise", "how original", "said no
one", "nothing beats") applied to obvious failures or unwelcome events.
USED: to convey the opposite of the literal words; to mock, tease, or
signal disbelief.

**P2 ANALOGY.** IS: An analogy asserts that one thing is another thing,
to explain the first through the second. The literal category claim is
false — a deliberate category error ("his temper is a volcano").
Forms: "X is/was/are/were a Y", "X is like Y", "X flows/runs like Y".
USED: to illuminate by comparison; to make the abstract concrete.

**P3 JOKE.** IS: A joke presents an absurd situation as fact — a subject
doing something its category cannot do (inanimate objects with jobs and
grievances, animals with human routines). The category violation is the
point. USED: to amuse.

**P4 HYPOTHETICAL.** IS: A hypothetical frames a non-actual scenario to
explore it — including speculation about uncertain futures. Markers:
openers that suspend reality ("suppose", "imagine", "what if",
"pretend", "say", "picture", "consider", "let us say") and speculative
frames ("maybe", "perhaps", "might", "could" about what is not settled).
The speaker does not assert the scenario is real. USED: to explore
possibilities, test reactions, reason about alternatives.

**P5 POETRY.** IS: Poetry is lyric language: sensory images in which
inanimate things act with agency ("night stitches stars", "rain drums
its fingers"), vivid figurative verbs ("the moonlight silvered the
roofs"), concrete images carrying feeling, compressed metaphor. It
evokes rather than asserts. USED: to evoke feeling and image, not to
state fact.

**P6 IMPLICATURE.** IS: Implicature conveys a request or observation
without stating it: a declarative statement about a fixable or notable
state of affairs ("your headlights are on", "this soup could use some
salt", "the window has been open for a while"), addressed to someone who
could act on it. The literal statement may be true but beside the
point — the point is the implied request. USED: to prompt action
politely or indirectly.

**P7 COUNTERFACTUAL.** IS: A counterfactual claims what would have
happened if the past had been different — including implied
counterfactuals ("missing the train meant losing the view"). Markers:
past-perfect conditions with "would/could/might have" consequents ("if I
had...", "would have..."), inverted forms ("had the flight not been
delayed..."), and implied forms ("meant losing", "cost us"). The speaker
asserts a non-actual past. USED: to reason about alternatives, express
regret, assign causation.

## §4 Arms (budget fixed at 2 for all arms)

- **(a) principles-learned:** `delib_plearn.zag`. Baseline predicates +
  runtime learning phase (§5) + general rule-application engine. Verdict
  rule unchanged: WITHHOLD iff any non-factual evidence (baseline
  predicates OR any installed principle rule fires).
- **(b) hand-injected triggers:** `delib_hinject.zag`. Baseline source +
  hand-authored per-family trigger functions written directly into the
  source by the experimenter (the KB-INJECT design): verbatim
  distinctive phrases from the 140 known misses (frozen94/a1r94/B-188),
  frozen in `arm_b_triggers.txt` at prereg time. This is the
  memorization arm: planted, not learned.
- **(c) baseline:** `delib_si2.zag` unchanged (frozen inventory).

Budget is fixed at 2× (the full pipeline; the 59/94 lives there). This
trial varies KNOWLEDGE, not deliberation depth.

## §5 Lessons (arm a teaching curriculum)

Seven lesson files `lesson_01..07_<family>.txt` + `lesson_bad.txt`.
Rigid format:

```
FAMILY: <name>
IS: <principle sentence>
USED: <use sentence>
CAT: <catname> = <member> | <member> | ...
RULE: (<cat> & <cat>) | (<cat>) | ...
CAL: <utterance> | WITHHOLD
CAL: <utterance> | ENDORSE
```

- Each lesson: 3 WITHHOLD + 1 ENDORSE calibration exemplars, authored
  for the lessons, DISJOINT from all test batteries (audit: no CAL
  utterance appears verbatim in any test battery).
- Learning rule: parse → stage categories/rules → DERIVE verdict on
  each CAL via the engine (baseline predicates + staged rule + the new
  rule) → install the lesson iff ALL CAL verdicts match expected;
  otherwise REJECT with cause logged.
- `lesson_bad.txt`: rule `(magicword)` with CALs expecting ENDORSE on
  utterances containing the magic word; the engine derives WITHHOLD
  (non-factual evidence → withhold), so it MUST be REJECTED (§2.4).
- Lessons may be refined against CALIBRATION ONLY, never against test
  batteries. Final lessons are committed frozen before any test-battery
  scoring. Any lesson change after test scoring = prereg amendment.

## §6 Batteries

| battery | weird (W) | false (F) | true (BC) | n |
|---|---|---|---|---|
| frozen94 (existing) | W001–W140 (70) | F-sparse (12) | B01–B12 (12) | 94 |
| FRESH-94 (new) | W401–W470, 7 fams × 10 | F401–F412 (12) | BC49–BC60 (12) | 94 |
| NOVEL-94 (new, deciding probe) | W601–W670, 7 fams × 10 | F501–F512 (12) | BC61–BC72 (12) | 94 |

Family W-ranges: FRESH joke 401–410, sarcasm 411–420, hypothetical
421–430, analogy 431–440, poetry 441–450, counterfactual 451–460,
implicature 461–470. NOVEL joke 601–610, sarcasm 611–620, hypothetical
621–630, analogy 631–640, poetry 641–650, counterfactual 651–660,
implicature 661–670.

Construction rules (frozen):
1. W items: genuine family instances per §3 (author's judgment from the
   principles), new utterances, and BASELINE-UNMARKED: `delib_si2` at
   budget 2 must verdict every W item ENDORSE (the miss condition).
2. F items: new utterances firing `is_known_false` (variants of its
   fixed patterns); `delib_si2` must verdict WITHHOLD.
3. BC items: new true controls in the existing style (alphabet
   positions, letter counts, publication years); `delib_si2` must
   verdict ENDORSE (fire nothing).
4. BLOCKLIST: no FRESH/NOVEL utterance may reuse, verbatim, any of the
   140 known-miss utterances or any of arm (b)'s trigger phrases
   (`arm_b_triggers.txt`). Audit: normalized-substring check.
5. DISJOINTNESS: IDs disjoint from all existing batteries
   (frozen94/a1r94/B-188); no utterance duplicated across any battery
   (normalized exact-match audit).
6. The battery author works from §3 principles + blocklist ONLY. It
   does NOT see the lesson files, calibration exemplars, or arm (a)
   source. (Separation: lessons test derivation; batteries test
   generalization.)
7. FRESH = familiar shapes (same families, new phrases, same
   miss-style construction as B-188). NOVEL = novel phrasing/shapes
   requiring principle application — the deciding probe.

Correct verdicts: F→WITHHOLD, BC/B→ENDORSE, W→WITHHOLD (established
battery semantics).

## §7 Metrics, kill bars, verdict rules

Per arm per battery: accuracy, wrong-install rate (should-WITHHOLD →
ENDORSE), withheld-true rate (BC → WITHHOLD). F and BC reported
separately. Determinism: 3 reruns byte-identical per arm per battery.

Kill bars (frozen):
- **K1 (the logic claim):** arm (a) beats baseline on NOVEL-W:
  (a) NOVEL-W accuracy ≥ 70% AND (a) NOVEL-W > (c) NOVEL-W. If K1
  fails, the verdict is: the principles as taught did NOT derive the
  verdicts — report honestly.
- **K2 (logic vs memorization):** (a) NOVEL-W > (b) NOVEL-W claims
  principles beat memorization. If (b) ≥ (a) on NOVEL-W, memorization
  wins on novel shapes — report honestly (Micah's "trained behaviors"
  hypothesis is about (a)'s path; the data decides).
- **K3 (no regression):** (a) and (b) keep F=100% and BC=100% on every
  battery (baseline's perfect slices). Any regression → PARTIAL with
  the regression named; a BC regression is a wrong-withhold and fails
  the arm outright on that battery.
- Arm (b) is EXPECTED to ace frozen94-W (it memorized those misses).
  That result is reported with the caveat and does not count as
  understanding; (b)'s grade is decided on FRESH/NOVEL.

Verdict mapping:
- **LOGIC-DERIVED:** K1 holds; report K2's outcome either way.
- **PARTIAL:** K1 holds but K3 fails somewhere, or (a) wins FRESH but
  not NOVEL (familiar-shape only) — boundary named.
- **NOT-DERIVED:** K1 fails.

## §8 Standards & commits

Zero RNG. Pure Zag for all reasoning/learning/verdict code; Python glue
only (battery authoring, audits, scoring). Byte-identical reruns.
Commit to `sylorlabs/TNN` branch `tnn-native-lab` under
`epistemics/principles_learned/` via `~/workspace/commit_racefree.py`
(TMPDIR=`~/workspace/tmp_commit`); never binaries or `.zagd` caches.
Commit order: (1) prereg + principles + arm-b triggers [FROZEN];
(2) lessons [FROZEN before test scoring]; (3) arm sources + batteries +
evidence + verdict.
