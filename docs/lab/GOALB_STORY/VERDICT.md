# GOAL-B VERDICT — story composition from preregistered word sets

Question (verbatim): "test whether TNN can write a unique story from preregistered 5–12 word sets or fucks it up."

Short answer: the existing TNN dialogue machinery fucks it up completely; two new deterministic composers built for this goal write grammatical, complete, arc-structured stories on all 8 sets. The success demonstrates **bounded compositional machinery**, not general intelligence and not a separate expressive faculty.

**Run honesty note (red-team enforced):** the preregistered implementation's first full run scored B1 **13/16** — three DEL trials dropped their climax pivot (F2 below). A code defect was found and fixed (no design, bar, or template-logic change), and the second run scored **16/16**. All numbers below are the post-fix run; the 13/16 first run is part of the record, not hidden.

## 1. Bars vs results

| Bar | Criterion | Result |
|---|---|---|
| B1 coverage | every input word verbatim, ≥7/8 per composer | **PASS 16/16** (POS 8/8, DEL 8/8) |
| B2 arc | blind judges, mean ≥3.5 on ≥6/8 per composer | **PARTIAL — one judge only.** gpt-5.6-sol (blind): run1 DEL 7/8 ≥3.5, run2 DEL 6/8 ≥3.5; POS 0/8 ≥3.5 both runs. Second judge (grok-4.6) UNEVALUATED — both LLM APIs hard-down mid-track (FALLBACK_LOG.md). Two-judge bar cannot be met tonight; reported honestly, not waived. |
| B3 novelty | no story sentence verbatim in defined corpora | **PASS 16/16** |
| B4 leakage | kb.txt unchanged, no ≥16B story substring in it, no belief-write path | **PASS** (sha256 identical; 0/16 substrings; source audit: O_RDONLY reads only) |
| B5 determinism | 3 fresh-process byte-identical reruns | **PASS** (cmp clean on all three) |
| Positive control | hand-written story scores ≥4.0 both judges | sol: 5/5 both runs (grok unevaluated) |
| Negative control | deleted-word story must fail B1 | PASS (missing word correctly flagged) |

Controls liveness confirmed: the B1 checker fails when a word is deleted; the B2 judge gives the positive control 5/5 (sol, both runs).

**B2 supplementary (native, non-blind experimenter rating, NOT bar evidence):** `evidence/b2_native_supplementary.md`. Means: POS 2.00, DEL 3.25, CTRL 5. The DEL>POS direction agrees with the blind LLM judge; absolute levels are harsher. Inter-rater spread (sol vs experimenter on DEL: 3.9 vs 3.25) further confirms B2 is a coarse instrument.

## 2. The two composers

- **C-POS**: fixed positional mapping of the word list into setup/complication/climax/resolution chunks. Every story is grammatical and complete (B1 8/8), but the blind judge rates its arcs 2/5 across the board: the sentences are connected only by position, not by role. It reads like a list wearing a story's clothes.
- **C-DEL**: fixed class-based planner (PERSON→setup anchor, PLACE→setting, EVENT→complication, ABSTRACT→climax pivot, etc.) plus a decision trace with reason codes (CLASS_SLOT / FALLBACK_ORDER / REPAIR_SPILL / POSITIONAL), coverage verification, and bounded repair (spill one word from the fullest beat into an empty one). The judge rates its arcs 3–5: a real setup→complication→climax→resolution shape.

Example (S2, DEL): "The baker lived near the desert. Every morning the baker polished the submarine. Then the eclipse struck without warning. The violin was caught in the chaos. Then the chase returned, worse than before. The baker held the letter tight. In the end, the baker kept going. The mirror waited quietly."

## 3. Failure autopsy

**F1 — baseline retrieval collapse (the "fucks it up" case).** The existing dialogue QA system, asked "write a story using these words: …" on S1–S4, answered all four with "The Louvre opened as a museum in 1793." Zero words used, no story, pure retrieval of an irrelevant fact. Machinery cause: the QA system has no generative mode; an open-ended prompt falls through to the nearest answer template and emits a retrieved fact. This is the negative result the goal asked for: **retrieval + templates alone cannot compose.**

**F2 — pivot omission (caught by the verifier, fixed).** In `r_climax`, when the climax pivot was a PLACE or THING (no EVENT/ABSTRACT/PERSON available), the template branch rendered the protagonist and opponent but dropped the pivot word entirely — 3/16 trials (S3/S4/S8 DEL) failed B1 with the pivot missing. Machinery cause: the emitter had no coverage self-check; the planner's assignment guarantee was silently broken downstream. The composer did not notice; the external verifier did. Fix: render the pivot in all branches ("stood alone against the wolf in the library", "clutched the compass and stood alone"). After fix: 16/16. Lesson: template-bound emission without a closed-loop check can silently drop constraints — the planner and the emitter must be verified as one pipeline, which the prereg already required.

**F3 — judge non-determinism.** gpt-5.6-sol scored the identical frozen prompt twice and differed by ±1 on 5/17 items (e.g. T04: 5→4, T10: 5→4). B2 is a coarse instrument, not a precise meter. The DEL>POS gap survives the noise; fine-grained rankings do not.

## 4. Intelligence verdict

**What the failure says:** the dialogue QA subsystem, as tested (4 story prompts, S1–S4), shows no compositional behavior at all — not weak composition, none: every prompt collapsed to the same irrelevant retrieved fact. Scoped honestly: this is one QA mode under one prompt format, and the later success shows compositional machinery *can* be built alongside it. But within the tested subsystem, retrieval is not composition — this experiment makes that concrete rather than philosophical. The negative result stands: **retrieval + templates alone cannot compose.**

**What the success says:** a deterministic planner that assigns words to narrative roles by class, plus a fixed set of sentence templates, satisfies every bar. That is **bounded compositional machinery**: real composition under constraints (all words used, arc shape present, deterministic, no leakage), but with no understanding, no alternatives considered, no draft-and-revise, no aesthetic judgment. The system never evaluates its own output — F2 proves it: the composer shipped broken stories and an outside checker caught them.

**Is it general intelligence?** No. Nothing here generalizes beyond the fixed planner and templates; the "writing" is slot-filling. A general intelligence would notice F2 itself, would vary its approach, would judge its own drafts.

**Is it a separate expressive faculty?** No — and this matters for the constructed-mode question. The composer is a planner plus templates, built for this task. It is not evidence that the pinned prose path, or any existing TNN subsystem, possesses open-ended imagination. It is evidence that *a* deterministic mechanism can be built that composes under constraints.

**Did deliberative machinery help?** Yes, within bounds — but the bound is tighter than it looks. The C-DEL pipeline produces clearly better arcs than C-POS (sol: DEL 3–5 vs POS 2 across all 8 sets; experimenter: 3.25 vs 2.00) — but C-POS (blind positional chunking) is a weak comparator, so this is evidence that role-aware templates beat role-blind ones more than it is evidence for deliberation in general. C-DEL also bundles class-based planning, role-specific templates, and the repair step, so this experiment does not isolate which part caused the gain (see §6). What can be said: role-aware placement — events in complications, abstracts as climax pivots, persons as anchors — is the structural difference most plausibly behind the arc shape, and every placement is inspectable in the trace (word, class, rule — the actual assignment log, no post-hoc confabulation). The "deliberation" is a single feedforward pass with fixed rules. There is no search, no backtracking, no self-critique. It helps composition the way a good outline helps an essay: structurally, not intellectually.

**Constructed-mode separation under creative load:** holds at the level tested. Story bytes exist only in stdout and the runs/ logs. `dialogue/kb.txt` is byte-identical before and after (sha256). No story shares a ≥16-byte substring with kb.txt. The composer source has no write path to the belief store (all file opens are O_RDONLY on inputs/; audit in evidence/). The partition discipline survives generating 16 stories. What this does NOT establish: semantic non-leakage (a story could still influence later retrieval conceptually) — frozen as a known limitation.

## 5. Red-team of these conclusions

(Recorded before generation in PREREG_AMENDMENT_A1; re-checked after results, plus a post-results pass by gpt-5.6-sol, `evidence/redteam_sol.txt`.)

- "16/16 is meaningless with n=8 sets." Accepted: exploratory, not statistical. The claim is existence ("a deterministic mechanism can do this"), not generality.
- "Template-bound emission is not writing." Accepted and stated: the verdict claims bounded compositional machinery, explicitly not open-ended writing or imagination.
- "The judge gap DEL>POS could be style bias." Partially accepted: the POS stories are choppier by construction; judges may reward the DEL templates' fluency rather than true arc. The control (hand-written, 5/5) shows the rubric can recognize a real arc, which bounds this worry but doesn't eliminate it.
- "F2's fix was experimenter intervention." Accepted in the strong form: the first preregistered run was 13/16, and the reported 16/16 is the repaired composer. The fix changed no bar, rule, or template logic — only a missing render that the frozen design already required (coverage) — but it was informed by observed failures, so the headline number is post-fix, stated as such in the run-honesty note.
- "The 'no compositional faculty' claim overreaches." Accepted: scoped to the tested QA subsystem and prompt format; the experiment does not survey all TNN machinery.
- "DEL's arc gain is causally unattributed." Accepted: C-DEL is a bundled pipeline (planner + role templates + repair); the experiment does not isolate the planner. §4 no longer claims otherwise.
- "Judge variance undermines B2." Accepted: B2 is coarse. Intra-judge ±1 (sol run1 vs run2) and inter-rater spread (sol DEL mean 3.9 vs experimenter 3.25) both confirm it.
- "B2 is only single-judge." Accepted and structural: both LLM APIs went hard-down mid-track (grok-4.7 429 insufficient_credits; sol/grok-4.6 via UnoRouter 524/timeout). The two-judge bar is UNEVALUATED, not passed — stated in §1, not waived. A second judge can complete the bar when APIs recover (max one recovery probe/hour per parent directive).
- "C-POS is a strawman." Accepted: positional chunking with no role awareness was never going to produce arcs, so DEL beating it is weak evidence for "deliberation helps" specifically. What the comparison actually shows is that role-aware templates beat role-blind ones — the deliberation claim rests on the traceable class→beat mapping, not on a fair fight. A real test would pit C-DEL against equally fluent non-deliberative templates.
- "The class table is fitted to the test sets." Accepted: classes.txt covers exactly the 57 words in the 8 sets — the planner has never seen an unclassified word. On a new set, unknown words fall through to THING/fallbacks and the "deliberative" advantage is unproven. Generalization beyond these sets is not established.
- "B1 measures presence, not integration." Accepted: the bar is verbatim appearance. The templates integrate words grammatically, but nothing in the bars tests whether the integration is meaningful vs decorative. A list with verbs would pass B1.
- "B5 is a no-RNG check, not robustness." Accepted and stated plainly: byte-identical reruns of a pure function of fixed inputs prove the absence of randomness/threading (which is Micah's law and the actual point), not resilience to anything.
- "No human rating." Accepted: Micah's later human judgment remains the real validation; LLM scores are a proxy.

## 6. What this does not claim

- Not a claim that TNN "can write stories" in any general sense — only that these two fixed composers pass the frozen bars on these eight sets.
- Not a claim that B2 fully passed — the two-judge bar is unevaluated; only the single-judge reading (DEL meets ≥6/8 at 3.5 on both sol runs, POS does not) is reported.
- Not a claim that deliberation equals reflection — the planner is feedforward; it does not critique or revise.
- Not a claim of semantic leakage-freedom — only file-level partition discipline.
- Not a claim that C-DEL's planning (vs its repair step) caused the arc gain — full-pipeline intervention, per prereg.

## Evidence

- `evidence/TRIAL_TABLE.md` — per-trial B1/B2/B3 results
- `evidence/b2_prompt.txt` — frozen judge prompt
- `evidence/b2_raw_gpt-5_6-sol.txt`, `evidence/b2_raw_grok-4_6.txt` — raw judge outputs
- `evidence/b2_item_key.txt` — blind ID → set/variant key
- `runs/rep1.log` (+ rep2, rep3 byte-identical) — all 16 stories with planner traces
- `runs/baseline.log` — retrieval-collapse baseline
- `runs/kb_before.sha256`, `runs/kb_after.sha256` — B4 hash evidence
- `src/story_all.zag` — the composer (pure Zag, deterministic)
- `src/verify_goalb.py`, `src/judge_b2.py` — verifiers
