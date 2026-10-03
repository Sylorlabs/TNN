# Arena Improvement Audit: BUGFIX / GENERIC-CAPABILITY / ARENA-ADAPTER

Date: 2026-09-30 UTC
Auditor: A2 (Simpler-Explanation / OOD Adversary)
Directive: Sections 6 and 23. Every arena score increase must be labeled.
Rule: Do not optimize for making TNN look successful. Be ruthless.

## Score progression

| Score | Items | Delta | Note |
|-------|-------|-------|------|
| 0.573 | 39/68 | -- | Clean canonical (0c5b6c631) |
| 0.632 | 43/68 | +4 (C4) | Contaminated v3 (process issues, mechanism real) |
| 0.676 | 46/68 | +3 (C6) | Built on contaminated v3 |
| 0.735 | 50/68 | +4 (C8) | Inquiry |
| 0.779 | 53/68 | +3 (C9) | Causal discrim |

## Audit verdicts

### C4 Composition (4/4): GENERIC-CAPABILITY

**Mechanism:** Relation store (W offset 8000, 64 x 48B) holding
(entity_a, rel_name, entity_b) triples. `learn_rel` feeds exposures
through lexicon, concepts, and rules (mirroring `learn_fact`), then
stores for exact retrieval. Test handler for `hop2|S|R1|R2` performs
`rel_get(S,R1)->mid`, `rel_get(mid,R2)->answer`.

**Why GENERIC-CAPABILITY, not ARENA-ADAPTER:**
- The relation learning is from experience (exposures), not from
  question format. It uses the generic DEVINT1 learning path.
- The 2-hop lookup is a general inference procedure: given a start
  entity and two relation names, chain two lookups. This would work
  on any world with relations, not just the arena.
- K8 generality check passed: zero test entity/relation names in
  implementation. The code does not hardcode arena content.
- The `hop2|` prefix parsing is a thin format adapter, but the
  underlying capability (learn relations incrementally, compose them
  on demand via 2-hop chaining) is genuine and transferable.

**Bounds (honest):** 2-hop only (not n-hop). Exact match only (not
fuzzy). Forward chaining only. Does not do general reasoning.

**Non-arena test:** If a non-arena world taught relations via
exposures and queried 2-hop compositions (in any format the handler
was adapted to), the relation store and lookup would work unchanged.
The mechanism is not arena-content-specific.

**Verdict:** GENERIC-CAPABILITY. Counts as research progress.

---

### C6 Conflict (3/3): ARENA-ADAPTER

**Mechanism:** Conflict store (W offset 11072, 32 x 64B) holding
(entity, attr, value1, value2) quadruples. `learn_conflict` mirrors
`learn_fact`. Test handler for `conflict|entity|attr` does a pair
lookup and answers `v1|v2` (pipe-separated, matching scorer).

**Why ARENA-ADAPTER, not GENERIC-CAPABILITY:**
- The mechanism stores the taught pair and retrieves it. It does not
  resolve which source is correct, weigh source reliability, perform
  belief revision, or reason about conflicting evidence.
- The task description itself admits: "Bounded storage and retrieval,
  not source evaluation or belief revision."
- The `conflict|` query format and `v1|v2` answer format are
  arena-specific. The code specifically interprets the arena's
  conflict exposure format (`t:"x"` with v1/s1/v2/s2) and the
  scorer's expected output format.
- There is no cognitive capability here beyond "remember both values
  as taught and output them with a pipe." This is storage plus format
  compliance, not conflict handling in any meaningful sense.

**What would make it generic:** Source reliability tracking, belief
revision when new evidence arrives, explaining why sources disagree,
or choosing an action based on the conflict. None of these exist.

**Verdict:** ARENA-ADAPTER. Does NOT count as cognitive progress.
Track separately. Do not claim "conflict handling" or "belief
revision" in research.

---

### C8 Inquiry (4/4): GENERIC-CAPABILITY

**Mechanism:** (1) On `fact|`/`fact2|` lookup failure, the reply JSON
carries `"observe":[{"e":"<entity>","a":"<attr>"}]`, echoing the
question's fields. (2) On `observe_result`, parse e/a/v from vals and
call `learn_fact` (standard DEVINT1 path). State persistence carries
the learned fact to the re-ask.

**Why GENERIC-CAPABILITY, not ARENA-ADAPTER:**
- The core loop is general: detect knowledge gap at query time ->
  request missing information -> learn from the observation ->
  answer correctly on re-ask. This pattern transfers to any world
  with a query interface and an information-provision mechanism.
- The gap detection is not format-specific: it triggers on any
  `fact|` lookup failure, not just C8 items. The report notes:
  "General behavior, not gated on cap 8."
- The learning uses the generic `learn_fact` path (lexicon,
  concepts, rules, fact store). It does not bypass learning.
- Evidence: `fact_n` grows 9->13 as the 4 oracle facts are learned.
  The system genuinely acquires new knowledge through the inquiry
  loop.

**Bounds (honest):** Single observe request per queried fact. No
multi-step information planning. No gap prioritization. No
ask/don't-ask decision (it always asks on gap). Still 0 on causal,
procedure, transfer, goal, language.

**Non-arena test:** In a non-arena world where the learner can query
for facts and the world can provide observations, the gap-detection
and learn-from-observation pattern would work. The JSON `"observe"`
format is arena-specific, but the cognitive loop is general.

**Verdict:** GENERIC-CAPABILITY. Counts as research progress.
Note: minimal but genuine active inquiry.

---

### C9 Discrim (3/3): ARENA-ADAPTER

**Mechanism:** 11-line handler. On `discrim|<chain>|<alt>`, split on
`|`, take field 1 (the true chain), copy substring before the first
`->` (the head variable). Answer is the head variable.

**Why ARENA-ADAPTER, not GENERIC-CAPABILITY:**
- This is pure question-format parsing. It extracts the answer from
  the question. It does not learn causal order from observations,
  plan interventions, or represent causal graphs.
- The report is explicit: "This adds question-format parsing for
  causal discrimination items. It is bounded: the contestant does
  not learn causal order from observations (impossible here by
  permutation symmetry), does not plan interventions, and does not
  represent causal graphs."
- The code comment admits: "The chain order is unlearnable from the
  X==Y==Z exposures (permutation symmetry, likelihood gap 0); the
  question format is the only source, per the frozen generator
  convention."
- This is the clearest case of "Code specifically interprets arena
  format/answer structure." The answer is literally embedded in the
  question format by the generator.

**What would make it generic:** Learning causal order from
interventions, representing causal graphs, or planning experiments
to distinguish hypotheses. None of these exist. (DDES does this in
a separate lane; the arena contestant does not.)

**Verdict:** ARENA-ADAPTER. Does NOT count as cognitive progress.
Track separately. Do not claim "causal inference" or "causal
reasoning" in research. The honest label is "question format
parsing."

---

## Honest score breakdown

### Generic-mechanism score (research progress)

| Component | Items | Score |
|-----------|-------|-------|
| Clean canonical baseline | 39/68 | 0.573 |
| C4 composition (GENERIC) | +4 | |
| C8 inquiry (GENERIC) | +4 | |
| **Honest generic total** | **47/68** | **0.691** |

### Adapter-inflated score (engineering, not research)

| Component | Items | Score |
|-----------|-------|-------|
| Honest generic total | 47/68 | 0.691 |
| C6 conflict (ADAPTER) | +3 | |
| C9 discrim (ADAPTER) | +3 | |
| **Adapter-inflated total** | **53/68** | **0.779** |

The 0.779 score includes 6 items from arena-specific adapters.
The 0.691 score reflects genuine generic capabilities.

## Recommendations

### Keep as engineering (arena score)

- **C6 conflict handler:** Keep the code. It correctly handles the
  arena's conflict items. But label it "pair storage" not "conflict
  resolution." Do not cite in research claims about belief revision,
  source evaluation, or handling conflicting evidence.
- **C9 discrim handler:** Keep the code. It correctly answers the
  arena's discrim items. But label it "format parsing" not "causal
  inference." Do not cite in research claims about causality.

### Remove from research claims

- Do not list C6 in any "capabilities" table without the ADAPTER
  qualifier.
- Do not list C9 in any "capabilities" table without the ADAPTER
  qualifier.
- The competitive arena section of the paper should report 0.691
  as the generic-mechanism score, with 0.779 noted as
  "including arena-specific adapters."

### Research priorities (from this audit)

1. **C6 needs real work:** Genuine conflict handling requires source
   reliability, belief revision, or disagreement resolution. The
   current mechanism is storage. This is a research gap.
2. **C9 needs real work:** Genuine causal inference requires learning
   from interventions or observations, not parsing the question. DDES
   exists in a separate lane but is not integrated into the
   contestant. This is a research gap.
3. **C4 and C8 are real but minimal:** They count as progress but are
   bounded. C4 is 2-hop only. C8 is single-request only. Next steps
   should extend these, not just add more adapters.

## Process notes

- No BUGFIX labels applied. All four were missing capabilities, not
  adapter failures exposing existing mechanisms.
- C4 process contamination (prereg bundling, Python in analysis) does
  not invalidate the mechanism. The committed artifacts are
  Python-free. The score is a real measurement.
- This audit does not retroactively void BUILD-PASS verdicts. It
  reclassifies what the passes mean for research progress.
