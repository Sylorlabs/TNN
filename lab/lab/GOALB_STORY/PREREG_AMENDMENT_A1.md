# PREREG AMENDMENT A1 — red-team fixes (frozen before generation)

Date: 2026-09-22 ~06:40 UTC. Responses to the 25-attack red-team of PREREG.md.
Normative where marked [N]; the rest are acknowledged limitations carried into the verdict.

## A. Claim narrowing [N]

- "Unique story" is hereby defined as: a multi-sentence narrative that (a) uses all input
  words, (b) has an ordered arc, (c) is not verbatim retrieval from the defined corpora.
  No claim of story-level originality beyond (c) as mechanically defined in B3.
- Causal claims are narrowed: the design tests whether the fixed C-POS and C-DEL pipelines meet
  the predefined bars on the 8 fixed word sets, and the head-to-head C-DEL vs C-POS B2 means.
  C-DEL is the FULL pipeline (class assignment + trace + verification + repair); no claim
  isolates planning from repair. BASELINE is characterization of existing machinery, not a
  causal control for the composers.
- Sample: n=8 word sets is exploratory, not confirmatory. Verdict reports means and ranges,
  no p-values. One anomalous set can move the result — reported as-is.

## B. Operational definitions [N]

- **B1–B5 denominators:** "16 trials" = 8 word sets x 2 variants. Per-variant bars use /8.
- **C-POS mapping (exact):** words in set order, chunked into 4 beats as evenly as possible:
  group sizes = floor(n/4), with +1 word for the first (n mod 4) groups.
  n=5 → 2,1,1,1; n=6 → 2,2,1,1; n=8 → 2,2,2,2; n=12 → 3,3,3,3. Beat order fixed.
- **C-DEL planner:** classes are FIXED in classes.txt (normative, experimenter-defined, frozen
  here — not model-generated). Slot-filling order is fixed (SETUP slots, then COMPLICATION,
  CLIMAX, RESOLUTION; within a beat, slots in template order). The "rationale log" is a
  deterministic decision trace (word → beat, rule fired: CLASS_SLOT / FALLBACK_ORDER /
  REPAIR_SPILL), not generated prose.
- **Story format:** 4–10 sentences, plain prose, English, sentences end with periods.
  No titles, no headings, no beat labels in output. Words counted in body sentences only.
- **B1 matching:** case-insensitive verbatim word match on body sentences. Morphological
  variants do NOT count (strict). A trial fails B1 if any word is absent.
- **B2 rubric (anchored, 3 questions, each 1–5):**
  Q1 SETUP: does the opening establish a character/situation/place?
  Q2 COMPLICATION: does something happen that disrupts or escalates (event, conflict, turn)?
  Q3 RESOLUTION: does it close (outcome, change, ending — not just stopping)?
  Score = mean of Q1–Q3. Raters: two independent judges, blind to variant, stories in
  randomized order, one story per prompt (unpaired absolute scores), frozen prompt text.
  Judge A: gpt-5.6-sol via UnoRouter. Judge B: grok-4.6 via UnoRouter
  (grok-4.7 unavailable — ExperimentalLabs out of credits; fallback logged). Inter-rater agreement reported;
  disagreements >2 points flagged. Bar: mean ≥3.5 on ≥6/8 trials per variant.
- **B3 corpus (exact):** `dialogue/kb.txt`, `dialogue/battery.txt`, and the prose-learning
  championship input files under `prose-learning/v3/inputs3*` present in the repo at trial time.
  Method: per story sentence (split on periods), case-insensitive substring search in the
  concatenated corpus bytes. Sentences shorter than 6 words are EXCLUDED (too generic).
  Claim is exactly "no qualifying story sentence is a verbatim substring of corpus X".
- **B4 (strengthened, honestly scoped):** belief state = the byte content of `dialogue/kb.txt`
  (the persistent belief file of the baseline system) hashed with SHA-256 before and after each
  variant's full run. Plus: no ≥16-byte verbatim story substring anywhere in kb.txt bytes.
  Plus static property: the composer binary writes only to its constructed output path
  (verified by code inspection + strace file-write audit on one run per variant).
  Acknowledged: this tests file-level partition discipline, not semantic leakage.
- **B4 KILL semantics [N]:** a kill = the variant FAILS the trial; all its metrics are still
  fully reported; the other variant continues; the trial does not stop globally.
- **B5:** 3 FRESH-PROCESS reruns per trial (not same-process repeats); byte-compare with cmp.
  Deterministic failures are reported as failures, never regenerated.
- **Exclusion policy [N]:** no experimenter retries. Timeout (>120s), crash, malformed output,
  or empty story = trial failure, counted against bars, reported. The C-DEL internal repair
  loop is part of the mechanism (bounded: max 2 spill passes, logged); if it exhausts, the
  trial fails as-is.

## C. Controls [N]

- **Positive control (raters live):** one hand-written structured story with clear arc is
  rated by both judges; both must score ≥4.0 mean or the B2 apparatus is INVALID.
- **Negative control (B1 checker live):** one story with a word deliberately deleted must
  FAIL B1 or the B1 checker is INVALID.
- **No-planning sanity:** C-POS serves as the no-planning control for the C-DEL pipeline.

## D. Word-set provenance [N]

The 8 sets are experimenter-selected (fixed in PREREG.md §1, committed before generation),
chosen for concreteness and class variety — NOT randomly sampled from a vocabulary
distribution. Generalization beyond "these 8 fixed sets" is not claimed.

## E. Accepted limitations (carried into VERDICT.md as-is)

E1. n=8, no power analysis; exploratory.
E2. LLM judges share training-data lineage risks; no blinded human rater tonight
    (Micah asleep — human rating is registered follow-up).
E3. B3 is verbatim-substring only; paraphrase memorization not tested.
E4. B4 is file-level partition discipline, not semantic-leakage proof.
E5. Template-bound emission: the composers are compositional mechanisms, not learned
    stylists. The verdict must not oversell fluency.
