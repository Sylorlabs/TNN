# GOAL-B VERDICT — story composition from preregistered word sets

Question (verbatim): "test whether TNN can write a unique story from preregistered 5–12 word sets or fucks it up."

Short answer: the existing TNN dialogue machinery fucks it up completely; two new deterministic composers built for this goal write grammatical, complete stories on all 8 sets with full word coverage, novelty, zero belief leakage, and byte-identical reruns.

**Second-judge amendment (2026-09-22, §7):** the missing second blind judge is now complete (grok-4.7, same frozen prompt, same blind TIDs). The preregistered two-judge B2 bar is **NOT MET** — C-DEL reaches 4/8 trials at two-judge mean >=3.5 (bar: >=6/8), C-POS 0/8. Both judges agree the planner-shaped stories out-arc the positional ones (head-to-head gap 1.75) and both give the hand-written control 5/5, but the second judge calibrates ~1.5 points harsher across the board (DEL 2–3, POS 1) than the first (DEL 3–5, POS 2). The "arc-structured stories" claim from the first verdict is therefore **downgraded**: compositional success stands on the mechanical bars (B1/B3/B4/B5), but a satisfying narrative arc at the preregistered 3.5 level is not established by two-judge consensus. B2 final verdict: **FAIL**.

**Run honesty note (red-team enforced):** the preregistered implementation's first full run scored B1 **13/16** — three DEL trials dropped their climax pivot (F2 below). A code defect was found and fixed (no design, bar, or template-logic change), and the second run scored **16/16**. All numbers below are the post-fix run; the 13/16 first run is part of the record, not hidden.

## 1. Bars vs results

| Bar | Criterion | Result |
|---|---|---|
| B1 coverage | every input word verbatim, ≥7/8 per composer | **PASS 16/16** (POS 8/8, DEL 8/8) |
| B2 arc | blind judges, mean ≥3.5 on ≥6/8 per composer | **FAIL (two-judge bar not met).** Judge #1 gpt-5.6-sol (blind): DEL 6/8 ≥3.5, POS 0/8 ≥3.5 (committed evidence). Judge #2 grok-4.7 (blind, 2026-09-22, same frozen prompt + blind TIDs): DEL 0/8 ≥3.5, POS 0/8 ≥3.5. Two-judge per-trial mean ≥3.5: DEL **4/8**, POS **0/8** (bar: ≥6/8). Positive control 5/5 both judges (apparatus valid). Max inter-rater |diff| = 2, none >2 flagged. Head-to-head: sol DEL 4.00 vs POS 2.00; grok DEL 2.50 vs POS 1.00; combined DEL 3.25 vs POS 1.50. Full table: evidence/b2_combined.md. See §7 amendment. |
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
- Not a claim that B2 passed — the two-judge bar is now EVALUATED and FAILED (DEL 4/8, POS 0/8 at two-judge mean ≥3.5; see §7). The arc-quality claim is downgraded; only the mechanical composition bars (B1/B3/B4/B5) stand.
- Not a claim that deliberation equals reflection — the planner is feedforward; it does not critique or revise.
- Not a claim of semantic leakage-freedom — only file-level partition discipline.
- Not a claim that C-DEL's planning (vs its repair step) caused the arc gain — full-pipeline intervention, per prereg.

## 7. Second-judge amendment — two-judge bar evaluated, NOT met (2026-09-22 ~07:20 PDT)

### 7.1 Method (substitution documented)

- Judge #2 = **grok-4.7 via ExperientialLabs** (wrapper `grokchat.py` path, max_tokens 1500), run 2026-09-22 ~07:20 PDT after verifying API recovery with a substantive probe.
- SAME frozen prompt text (`evidence/b2_prompt.txt`, byte-identical md5 7e79199cadb2e08367376750445c7357, not regenerated), SAME blind TID labels T01–T17 (stories only, no composer labels, no scores visible), single call — identical presentation to judge #1.
- **Substitution note:** Amendment A1 specified Judge B as grok-4.6 via UnoRouter (grok-4.7 was 429/insufficient_credits). The parent task explicitly directed grok-4.7 via ExperientialLabs as judge #2 once the API recovered. This also restores PREREG §3's original rater choice (grok-4.7). One retry/hard-stop rule honored: the call succeeded first attempt; no retry burn.
- Raw output: 17/17 scores parsed from a clean 17-line response (`evidence/b2_raw_grok-4_7.txt`). No empty choices, no truncation.

### 7.2 Scores (per-story, per-judge)

| trial | set | variant | sol | grok-4.7 | two-judge mean | |diff| |
|---|---|---|---|---|---|---|---|
| T01 | S1 | POS | 2 | 1 | 1.5 | 1 |
| T02 | S1 | DEL | 3 | 2 | 2.5 | 1 |
| T03 | S2 | POS | 2 | 1 | 1.5 | 1 |
| T04 | S2 | DEL | 4 | 3 | 3.5 | 1 |
| T05 | S3 | POS | 2 | 1 | 1.5 | 1 |
| T06 | S3 | DEL | 3 | 2 | 2.5 | 1 |
| T07 | S4 | POS | 2 | 1 | 1.5 | 1 |
| T08 | S4 | DEL | 5 | 3 | 4.0 | 2 |
| T09 | S5 | POS | 2 | 1 | 1.5 | 1 |
| T10 | S5 | DEL | 4 | 2 | 3.0 | 2 |
| T11 | S6 | POS | 2 | 1 | 1.5 | 1 |
| T12 | S6 | DEL | 4 | 3 | 3.5 | 1 |
| T13 | S7 | POS | 2 | 1 | 1.5 | 1 |
| T14 | S7 | DEL | 4 | 2 | 3.0 | 2 |
| T15 | S8 | POS | 2 | 1 | 1.5 | 1 |
| T16 | S8 | DEL | 5 | 3 | 4.0 | 2 |
| T17 | CTRL | — | 5 | 5 | 5.0 | 0 |

### 7.3 Bar evaluation (prereg §3 / A1, no waiving)

| Reading | Result |
|---|---|
| Two-judge per-trial mean ≥3.5 on ≥6/8 (prereg wording) | DEL **4/8** — FAIL; POS **0/8** — FAIL |
| Per-judge independent ≥6/8 | sol: DEL 6/8 ✓, POS 0/8; grok-4.7: DEL 0/8, POS 0/8 — FAIL |
| Positive control, both judges ≥4.0 | sol 5, grok 5 — **PASS** (B2 apparatus valid) |
| Disagreements >2 points flagged | none (max |diff| = 2) |

**B2 final verdict: FAIL for both variants under the preregistered two-judge bar.**

### 7.4 What the judges agree on vs where they split

Agreement (substantive):
- Ordering: within each judge's own scale, every DEL story outscores every POS story on its set pair, and both judges score the hand-written control 5/5. Inter-rater rank agreement is perfect; no >2-point disagreement anywhere.
- Head-to-head direction: sol DEL 4.00 vs POS 2.00 (gap 2.00); grok-4.7 DEL 2.50 vs POS 1.00 (gap 1.50); combined DEL 3.25 vs POS 1.50 (gap 1.75). Role-aware placement beats positional chunking by both judges' lights.

Split (calibration):
- Grok-4.7 anchors ~1.5 points lower across the board: all POS = 1 ("no discernible arc"), DEL = 2–3, CTRL = 5. Sol: all POS = 2, DEL = 3–5, CTRL = 5.
- This is systematic scale use, not noise: grok used only {1,2,3} for the 16 machine stories and reserved 5 for the hand-written control; its scores are perfectly internally consistent (all POS identical, DEL 2 on odd sets / 3 on even sets).
- The red-team's pre-existing "judge variance undermines B2" concern is now quantified: intra-judge ±1 (sol run1/run2) was already known; inter-judge calibration divergence is ±1.5 systematically with perfect order agreement.

Observed regularity (no causal claim, n=8): grok-4.7 scored DEL stories on even-numbered sets (S2/S4/S6/S8) = 3 and odd-numbered sets (S1/S3/S5/S7) = 2. No pattern was preregistered; carried as an observation only.

### 7.5 Revised intelligence verdict (prereg decision rule)

Per prereg §4, the questions are answered with evidence, and the bars decide:

1. **Mechanical composition stands:** B1 16/16 (every word verbatim), B3 16/16 (novel sentences), B4 PASS (file-level partition discipline), B5 PASS (3/3 byte-identical fresh-process reruns). A deterministic planner + templates does compose complete, novel, non-leaking stories. That much is evidence-determined and unchanged.
2. **The arc claim is downgraded:** the first verdict's "arc-structured stories" is NOT sustained by two-judge consensus. One blind judge reads 6/8 DEL stories as arc-bearing (≥3.5); the second reads 0/8 as arc-bearing. The honest claim is now: the composers emit *beat-structured* stories (setup/complication/climax/resolution slots by role) that one judge reads as arcs and another reads as fragmentary-but-directed (2–3). The preregistered 3.5-level arc claim FAILS.
3. **"Is it general intelligence?"** Even more firmly no — a general intelligence's arc quality would not hinge on which blind judge holds the ruler. The failure is now two-sided: F1 (retrieval collapse) and B2 (no two-judge consensus that the stories read as arcs).
4. **"Did deliberative machinery help?"** Yes, within the same tight bound as before, but the absolute bar moved: the planner-shaped pipeline beats the positional one by both judges (gaps 2.00 and 1.50), yet neither variant clears the two-judge 6/8 bar. It is evidence that role-aware placement structures narratives better than position-blind chunking — not evidence of arc quality at the preregistered level.
5. **Constructed-mode separation under creative load:** unchanged — holds at the level tested.

### 7.6 Red-team additions (post-second-judge)

- "The two-judge bar failure is calibration, not substance." Partially accepted: order agreement is perfect and the head-to-head gap survives, so the planner>positional direction is robust. But the bar is absolute (≥3.5), not relative — calibration is part of what the bar measures. The verdict does not re-bend the bar.
- "Grok-4.7 may be a systematically harsh judge (scale compression)." Accepted and quantified: grok's machine-story range {1,2,3} vs sol's {2,...,5}. Both judges passed the positive control (5/5), so both scales are live — they simply calibrate machine output differently. This is exactly why the prereg demanded two judges.
- "The odd/even DEL split in grok's scores suggests story-level confounds." Noted: even sets got 3, odd sets 2 from grok. No word-count, n-class, or position confound is visible in the 8 sets (even sets: n=8,7,6,12; odd: 6,5,9,11). Carried as an unexplained regularity; n=8 makes any pattern speculative.

## Evidence

- `evidence/TRIAL_TABLE.md` — per-trial B1/B2/B3 results (two-judge amended)
- `evidence/b2_prompt.txt` — frozen judge prompt (md5 7e79199cadb2e08367376750445c7357)
- `evidence/b2_raw_gpt-5_6-sol.txt`, `evidence/b2_raw_grok-4_7.txt` — raw judge outputs
- `evidence/b2_combined.md` — combined two-judge table and counts
- `evidence/b2_item_key.txt` — blind ID → set/variant key
- `runs/rep1.log` (+ rep2, rep3 byte-identical) — all 16 stories with planner traces
- `runs/baseline.log` — retrieval-collapse baseline
- `runs/kb_before.sha256`, `runs/kb_after.sha256` — B4 hash evidence
- `src/story_all.zag` — the composer (pure Zag, deterministic)
- `src/verify_goalb.py`, `src/judge_b2.py`, `src/judge_b2_grok47.py`, `src/score_b2_combined.py` — verifiers/scorers
