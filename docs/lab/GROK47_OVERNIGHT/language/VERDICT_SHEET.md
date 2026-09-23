# GROK47_OVERNIGHT — Language sectors (PROSE / DIALOGUE / CODING) — Verdict Sheet

**Native worker:** Muse (depth-2 subagent) · **Engine:** grok-4.7 (analysis/design/red-team only)
**Night:** 2026-09-21→22 PDT · **Law:** no RNG in decision paths; byte-identical reruns; pure Zag;
grok never authors TNN mechanism bytes; tests decide; no external/irreversible actions.

> Verdicts carry both voices, labeled: **(grok)** = engine claim, **(native)** = repo/harness-verified.

## 0. Sector starting state (verified 2026-09-21 ~23:15 PDT, not trusted blind)

| Sector | State |
|---|---|
| PROSE | v1 PINNED. v3 repair crew DONE: KB3-VIABLE FAILS 2/4 (A3 beats v1 on step, muse-native only); C4 carried recovery (+0.30–0.56), C1 ≤+0.06, C2 0 on championship but CORE 11/24→22/24. Sol H2 (oracle-vs-production parse amplification) **untested, registered**. Defects known: wordlen curly-quote tokenizer gap; tier-3 near-tie precision (22 extra wrong values); NEG semantic overlap; dense-input summary defect. |
| DIALOGUE | Trial VERDICT 369/370 (99.7%), 5/5 byte-identical. Open: WE-09 honest gap (birth↔born stemmer); COMPOSE-NOVEL self-attested (N14/K17 proposed). |
| CODING | Coding trial done (KB-C2 FAIL honest). Bug-blindness crew DONE: 24/24 compiler parity + 30/30 + 0/8 + 30/30 via `inspect.zag` BUT through **authored text→fact parser** (declared boundary). Q2 audit: no bug knowledge ever taught; classification in Python driver; stateless loop; `patch_brace` doubling defect; gen 1/6 on unseen ops. Recommendations 1–5 = this loop's work queue. |

## 1. Hypotheses (engine; grok degraded → sol per §7)

### ROUND 1 — PROSE (sol, 2026-09-22 ~06:35 PDT)
- **P-H1: Oracle Parse Separates Sol-H2.** Production parse/order errors cause symbolic retrieval to amplify upstream failures. Test: stratify probes by probe-entity vs train-entity agreement; compare miss rates. Predicted: misses concentrate in mismatch subset. Kill: miss rates indistinguishable.
- **P-H2: Curly Quotes Recover Missed Sol Cases.** Normalize curly→ASCII quotes in tokenizer; replay 13 curly-quote sol probes. Predicted: ≥2 recover, ≤1 regression. Kill: <2 recoveries or regressions ≥ recoveries.
- **P-H3: Tier-3 Tie-Breaking Improves Precision.** Deterministic tie-break (exact phrase coverage before Jaccard). Predicted: top-1 precision +10pp on near-tie subset, recall unchanged. Kill: any source unreachable or no precision gain.
- **P-H4: Clause-Order Invariance Predicts Reliability.** Swapped-clause paraphrase pairs; invariant pairs ≥90% agreement. Kill: invariance doesn't predict agreement.

### ROUND 1 — DIALOGUE (sol, 2026-09-22 ~06:40 PDT)
- **D-H1: Deep stack return targets wrong frame.** 3 nested topics + digression in 3rd; return cue → wrong frame. Kill: answers Orwell, continues 1984 correctly.
- **D-H2: Correction fails to replace active referent.** "No, I meant the other one" → stale referent persists. Kill: correction selects non-current entity consistently.
- **D-H3: Hedged contradiction leaves stale belief.** Pluto hedged correction → stale/incorrect merge. Kill: adopts later classification, marks first outdated.
- **D-H4: Same-type distractor breaks coref chain.** Orwell/Huxley + "He was born in Motihari" → Huxley misresolution. Kill: Orwell referent survives.

### ROUND 1 — CODING (sol, 2026-09-22 ~06:42 PDT)
- **C-H1: Raw stderr classification from sequence evidence.** Token stream of raw stderr suffices; removing stderr causes large drop. Kill: fails on held-out variants.
- **C-H2: Abstract fault schemas beat concrete patches** on novel-shape repair. Kill: concrete matches/exceeds.
- **C-H3: Composition generates held-out operations** better than per-op emitters (current 1/6). Kill: no better than baseline.
- **C-H4: Persistent repair episodes reduce repeat cost.** Kill: no reduction or identical-string-only.
- **C-H5: Negative teaching reduces harmful repairs** under contradictory observations. Kill: same/more harm or clean-case degradation.

## 2. Preregistered kill bars

<!-- frozen per round BEFORE scored runs; no post-hoc movement -->

## 3. Results (native-verified)

### ROUND 1 — R1-CODE-BRACE (patch_brace fix) — TESTED, PASSES
- Mislabeled PARSE on balanced 52-byte source: output 51 bytes, `fn dbl` ×1 (was 295 bytes ×4 before fix). **No doubling.**
- Genuine missing brace: `}` inserted, compiles clean, binary runs rc=0.
- Determinism: 2/2 byte-identical.
- Bar: **PASSES** both directions.

### ROUND 1 — C-H1 (raw stderr classification pilot) — TESTED, PASSES (12/12)
Method: new pure-Zag `stderr_classify` (taught token→class associations, general 1/df-weighted overlap mechanism; zero per-class string literals in the mechanism — verified by literal audit; knowledge lives entirely in `teach.txt`). Taught 1 example/class (5 classes); 12 held-out variants (different identifiers, types, arities, line numbers).
- **12/12 correct** (E0203×3, UNKNOWNFN×3, ARITY×2, PARSE×2, DUPFN×2).
- Ablation: uninformative input → UNKNOWN (sc=0) / tie→UNKNOWN — classification genuinely depends on stderr content.
- Determinism: 2/2 byte-identical.
- Bar (≥10/12): **PASSES**.
- Artifacts: `~/workspace/grok47/language/stderr_pilot/` (stderr_classify.zag, teach.txt, tests.txt, binary).
- Next: wire stderr-as-observation into the learner's repair loop (replaces driver `eclass_of` regexes).

### ROUND 1 — Dialogue edge battery (D-H1..D-H4) — TESTED, adjudicated
Method: 24 fresh dialogues (6/hypothesis), E = correct behavior, run against rebuilt 370/370 binary; 2/2 byte-identical. Battery: `~/workspace/grok47/language/edge_battery/battery_edge.txt`.
- **D-H1 (deep stack): SUSTAINED.** Frame-return accuracy on 3-deep stacks: 3/6. Genuine wrong-frame returns: E1-03 T5 (Berlin→Austen), E1-04 T5 (Montparnasse→Eiffel), E1-05 T5 (Melville→Paris). Secondary finding: "Back to X: <specific question>" returns the frame's default fact, dropping the question focus (E1-01 T6, E1-02 T5, E1-06 T4).
- **D-H2 (correction): REFUTED for "the other one".** Entity switches correctly after a follow-up pronoun turn (E2-01, E2-02, E2-04) AND preserves the active question focus (answers height for the new tower — arguably better than my E). NEW finding: "the other &lt;category&gt;" phrasings ("other author/scientist/landmark") do NOT resolve (E2-03 entity ok but E2-05/E2-06 fail to switch).
- **D-H3 (hedged contradiction): REFUTED.** The system never NOTED hedged assertions — "I think X" is treated as a query and answered from KB. All 6 final answers correct. Capability gap (hedged beliefs aren't learned), but not the hypothesized stale-belief failure.
- **D-H4 (distractor coref): INCONCLUSIVE (bad E's).** My E's assumed gender-aware pronouns; the system is strictly recency-based ("he"→most recent person regardless of gender: E4-01/E4-02/E4-06). Proper test needs same-gender pairs pitting recency vs relation-selection — deferred.
- **Robustness bug (not fixed, frozen binary):** unknown battery section name → `stype_idx` returns −1 → negative index → `panic: slice index out of bounds`. A malformed battery file crashes the scorer instead of erroring cleanly.

### ROUND 1 — P-H2 (curly-quote pilot) — TESTED, PASSES (11/11, 0 regressions)
Method: folded U+201C/U+201D/U+2018/U+2019 → ASCII in the TEST probes only (input-stage normalization, frozen A3 binary untouched, m2 mode, dense inputs); per-probe diff vs frozen A3 log with scorer false-id mapping.
- **Recoveries: 11/11 clean curly-quote misses** (ids 48–54, 56–59; entity EMPTY→word, all VALUE correct).
- **Regressions: 0.**
- Bar (≥2 recoveries, ≤1 regression): **PASSES** decisively.
- Determinism: 2/2 byte-identical reruns.
- Note: probe 212 (13th curly probe) was already a hit in A3 via fallback tier (entity=books→trilogy after fold); id 55 is a false-fact probe, correctly excluded.
- **Recommendation:** fold curly quotes to ASCII in the tokenizer input stage as a preregistered follow-up (new prereg, not a frozen-v3 edit). Predicted A3 sol: 204→215/228 clean.
- Artifacts: `~/workspace/grok47/language/quote_pilot/` (inputs, run.log).

### ROUND 1 — P-H1 (Sol-H2 amplification) — TESTED, SURVIVES
Method: oracle3 (m2, verified 0-divergent vs frozen A3 binary) on A3 sol dense inputs. Production probe entity vs production train keys (all 3 phrasings) per fact; 228 clean probes (scorer false-id mapping: dense fid//3).
- ENTITY-MATCH (probe entity == ≥1 train key): 72 probes, **0 misses** (0.0%).
- ENTITY-NOMATCH: 156 probes, **24 misses** (15.4%).
- **100% of misses (24/24) fall in ENTITY-NOMATCH; 0% in ENTITY-MATCH.**
- Kill criterion was "miss rates indistinguishable or misses not concentrated": NOT met → H2 SURVIVES. Entity-parse agreement is a near-perfect necessary gate (match ⇒ hit, 72/72); mismatch raises miss risk 0%→15.4% (fallbacks rescue 132/156).
- Scripts: `~/workspace/grok47/language/h2_test.py`, entity-partition analysis.

### ROUND 1 — C1 mechanism decomposition (sol source, native) — NEW FINDING
Decomposed the frozen A1−A0 sol delta (+12, 65→77/228) probe-by-probe with the verified oracle (matches frozen logs 0-divergent):
- **Gain: 12 probes, 0 regressions.** 11 are ASCII-quote wordlen probes (ids 72–79, 81–83); 1 is open-domain (219, Lent).
- **Mechanism:** the dense builder's paraphrase templates include ASCII-quoted forms (`"X"`) that install the bare-word entity key the probe needs; the original phrasing 0 was quote-less and installed `word X`. C1's sol gain is **key repair via input variation, not generic redundancy**.
- Predicts (consistent with P-H2): curly-quote probes (48–59, entity=EMPTY) and quote-less probes (60–71, entity=`letters`) cannot be fixed by dense phrasing — and indeed remain misses through A3.
- Caution found en route: `inputs3/false_ids_sol.txt` lists dense TRAIN fids (36 entries), not probe pids; the binary's own clean summary (72/204) is wrong-denominator. The external scorer's `fid//3` mapping is the correct one. The v3 VERDICT §7 defect 2 already documents this; my analysis uses the scorer mapping throughout.
- Script: `~/workspace/grok47/language/c1_decomp.py`.

## 4. Red-team attacks (grok) + adjudication (native)

<!-- appended per round -->

## 5. Fixes landed

<!-- appended per round -->

## 6. Final verdicts (both voices labeled)

<!-- appended per round; headlined per sector -->

## 7. Fallback log

| Time | What happened | Status |
|---|---|---|
| 2026-09-21 23:16–23:25 PDT | "Truncated" grok-4.7 outputs (~50–90 bytes) on 4 probes | **VOIDED — tooling artifact, not model failure.** Stock `experientiallabs/bin/chat.py` hard-codes `"max_tokens": 16` (line 26, verified 2026-09-22). All conclusions drawn from those outputs are void. Fixed wrapper: `~/workspace/grok47/senses/grokchat.py` (default max_tokens 1500). |
| 2026-09-22 ~06:30 PDT | Substantive hypothesis generation moved to gpt-5.6-sol via UnoRouter (`~/workspace/grok47/language/sol_chat.py`, retries, 180s timeout) | Active. Prose/dialogue/coding R1 hypotheses captured in full. |
| 2026-09-22 23:30 PDT (coord) / verified ~06:45 | **grok-4.7 HARD DOWN**: gateway HTTP 429 `insufficient_credits`, org balance **$-0.02**. Credit top-up needs Micah. | grok-4.7 unusable for ANY output until top-up. Substantive generation: sol or native only. Worker EXEMPT from hourly grok re-probing (coordinator cron handles it). |

Impact of escalation on this worker: (a) the 4 voided truncation batches required no recapture — the sol R1 hypothesis sets (prose H1–H4, dialogue H1–H4, coding H1–H5) were captured independently via UnoRouter and are unaffected; (b) all remaining HTRF substantive generation proceeds via sol/native; (c) no grok short-output usage either (429 blocks everything).

## 8. Open questions (for coordinator / Micah's morning)

- Dialogue VERDICT.md (frozen 2026-09-22, digest bc7e19…) is now STALE: morphology-crew birth-year fix landed in dialogue.zag source but was never rebuilt; native rebuild+rerun scores 370/370 (WE-09 passes), 5/5 byte-identical, new digest 35aaae8a…. Recommend the dialogue crew re-freeze the verdict at 370/370 or amend.
- coding/src/learner.zag now differs from the frozen coding-trial binary (patch_brace doubling fix, this loop). Any re-run of frozen T3 must pin the old binary or re-freeze the new one.
- Micah's structural items (frozen-prereg amendments K17/K18/K19, N9/N14/N15, strength-trial rulings 3–5, integrity-doc sign-off) remain his.

## 9. ROUND 1 — preregistered bars (frozen before scored runs)

| ID | Bar | Kill criterion |
|---|---|---|
| R1-DIAL-370 | Rebuilt dialogue binary holds 370/370 and 5/5 byte-identical reruns | Any section < frozen score or any rerun mismatch → FAIL (revert binary) |
| R1-CODE-BRACE | patch_brace fix: mislabeled-PARSE on balanced source echoes unchanged; genuine PARSE still repaired | Doubling on echo case OR genuine-PARSE repair broken → FAIL |
| R1-PROSE-H2 | Sol H2 test design approved by engine; oracle-vs-production gap measured | Gap unmeasurable (gold frames unbuildable) → design FAIL, register lesson |
| R1-CODE-STDERR | stderr-as-untrusted-observation design: learner classifies ≥10/12 compiler classes from raw stderr text | <10/12 → design FAIL, document which classes resist |
| R1-DIAL-EDGE | Fresh dialogue edge battery (stacks depth-3, correction×referent, hedged-contradiction, distractor coref) | Any new category <70% → hypothesis SUSTAINED (gap real), fix proposed |
| R1-PROSE-PH2 | Curly-quote normalization pilot: replay 13 curly-quote sol probes with curly→ASCII folded in tokenizer input stage | <2 recoveries OR ≥1 regression → FAIL (do not pursue) |
| R1-PROSE-PH3 | Tier-3 deterministic tie-break pilot on near-tie subset | Precision gain <10pp OR any recall loss → FAIL |
| R1-DIAL-DH1..DH4 | Each sol dialogue hypothesis tested with ≥6 probe variants; category score reported | <70% per category → SUSTAINED; ≥70% → REFUTED for this battery |
| R1-CODE-CH1 | Raw-stderr classification pilot: ≥10/12 classes from stderr token stream, held-out variants | <10/12 or held-out collapse → design FAIL |
| R1-CODE-STDERR | stderr-as-untrusted-observation design: learner classifies ≥10/12 compiler classes from raw stderr text | <10/12 → design FAIL, document which classes resist |
| R1-DIAL-EDGE | Fresh dialogue edge battery (stacks depth-3, correction×referent, hedged-contradiction, distractor coref) | Any new category <70% → hypothesis SUSTAINED (gap real), fix proposed |
