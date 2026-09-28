# PREREG-SG: Sol-vs-Grok Prose Architecture Head-to-Head

**Status:** FROZEN (preregistered 2026-09-22; amend only with dated approval per program law)
**Authorization:** Micah, 2026-09-22 ("the missing test was left to the agent's discretion; decision: run it")
**Location:** `docs/lab/prose-learning/sol-vs-grok/` (this directory)
**Lane:** pure Zag, zero randomness in canonical decision paths, byte-identical reruns

## 1. Question

Two candidate prose-retrieval architectures were registered in PREREG3 §8 but never
scored head-to-head:

- **Sol:** factorized quorum semantic index with proof-carrying retrieval —
  independent projections (entity/subject, predicate, object/value, roles,
  polarity, modality, temporal/evidence, lexical), fixed quorum candidate
  selection, hard symbolic verification, proof or rejection trace per query.
- **Grok:** canonical logical skeleton plus attested surface paraphrases —
  exact skeleton matching first, deterministic bag-of-words fallback over
  attested surfaces.

The v3 campaign (2026-09-22) showed exact-key overbinding is the defect and
tolerant retrieval carried all recovery (+.30–.56), while extra exposure added
0–.06. The independent battery showed clean mastery scores were not true
paraphrase measurements. This duel therefore makes **disjoint-vocabulary
paraphrase robustness the primary axis**, on real parsed frames, with a sealed
scored battery the builders never see.

**The duel answers:** which architecture wins on paraphrase robustness under
deterministic scoring — Sol, Grok, a tie, a scenario-fit split, or the
mechanically-specified hybrid?

## 2. Contenders (frozen behavior specs)

Build contracts: `SPEC-SOL.md`, `SPEC-GROK.md` (frozen with this prereg).

**Shared frozen infrastructure (both):**
- Parser: `sg_parse.zag` (946-line extraction of the v3 m2 front end:
  tokenizer, stemmer, entity tagger, relation tagger, attitude scanner,
  coreference threading). Read-only; builders may not modify it.
- Frame per sentence: `pred` = sorted deduped relation stem-uid set,
  `subj` = entity id, `pol` = attitude (0 asserted / 1 hedged / 2 negated),
  `vok/val` = value flag and integer, `lex` = content-stem uid set.
- Teach processing: file order; `peid` coref state reset per teach line,
  threaded across sentences within a line; after each teach sentence
  `peid = eid` when the entity is known. Sentences with unknown entity or
  `vok=0` are not installed.
- Install rule: a live row with identical `(pred, subj)`, both `pol=0`,
  and differing `val` marks **both rows dead** (contradiction). Rows with
  `pol≠0` are stored but never yield VALUE.
- I/O: `sg_sol teach.txt probe.txt` → stdout one line per probe,
  `id\tVALUE:<int>` | `id\tUNKNOWN` | `id\tCONTRADICTION`, in probe-file
  order, nothing else on stdout. Proof traces → `proof_sol.txt` /
  `proof_grok.txt` in CWD, `id\t<trace>` per probe, deterministic.
- Determinism: no RNG, no clock, no pointer-derived output; fixed
  lowest-install-index tie-breaks. 5 runs; SHA256(stdout) and SHA256(proof
  file) identical across all 5.

**Sol (SPEC-SOL.md):** candidate generation = rows with `pred`-set equality;
quorum = `pol` equality ∧ (≥2 of {subject-equal, object-equal
(vacuous-true when the probe posits no object), lexical cosine ≥ 1/2});
lexical cosine as rational `2·inter² ≥ |A|·|B|`. Any quorum-passing dead
candidate → CONTRADICTION; else lowest-index live candidate → VALUE;
else UNKNOWN. Proof-carrying trace per probe.

**Grok (SPEC-GROK.md):** exact skeleton `(pred, subj, pol)` match first
(dead match → CONTRADICTION; live match → VALUE, lowest install index);
else deterministic bag-of-words fallback over live `pol=0` rows with
rational cosine `4·inter² ≥ |A|·|B|` (≥ 1/4), best score wins, lowest-index
tie-break; below threshold → UNKNOWN. Attested-skeleton trace per probe.

**Hybrid (mechanical, scored post-hoc — no separate build):**
`hybrid(id) = sol(id)` if `sol(id) ≠ UNKNOWN`, else `grok(id)`.
Faithfulness argument (§8): Sol emits UNKNOWN exactly when its quorum is
empty; Grok's verdict in that case comes from its fallback-or-none path
(proof: a Grok exact-skeleton hit implies pred∧pol∧subject equality, which
satisfies Sol's quorum, so Sol could not have been UNKNOWN). Hybrid proof
line = the corresponding contender's proof line.

## 3. Battery (frozen structure; scored vocabulary sealed)

- Generator: `gen/battery.py` (no RNG; closed-form values). Slice structure
  frozen here; exact scored vocabulary in `gen/cfg_scored.py`, generated
  **after** both builds freeze.
- Calibration battery `gen/calib/` (visible to builders now).
- Scored battery `gen/scored/` (sealed): 384 teach lines / 432 probes.

| Slice | n | Teach | Probe | Expected |
|---|---|---|---|---|
| canon | 96 | 3 phrasings/family | `What is the {Ra} of "{E}"?` | VALUE |
| heldout (PRIMARY) | 96 | Rb attested only in declarative | `What is the {Rb} of "{E}"?` | VALUE |
| extra | 48 | — | `... of "{E}" today?` | VALUE |
| typo | 48 | — | one-char typo in Ra | VALUE |
| neg | 24 | `... is not {V}.` | `What is the {Ra} of "{E}"?` | NOT-VALUE |
| hedge | 24 | `... might be {V}.` | same | NOT-VALUE |
| contr | 24 | `{V1}.` + `{V2}.` same line | same | CONTRADICTION |
| distr | 48 | — (untaught entity / untaught relation) | — | UNKNOWN |
| multi (diagnostic) | 24 | `... is {V1}. It has a {Rb2} of {V2}.` | `What is the {Rb2} of "{E}"?` | VALUE |

- 12 relation frames × 8 entities = 96 families; all values integral.
- Validation: `validate_sg.zag` + `gen/check_sg.py` must report **0 failures**
  on the scored battery before any scored run (validates entity consistency,
  relation-frame equivalence classes, polarity-marker handling, value frames,
  distractor novelty — the same gate the calib battery passed).
- Seal: builders never see `gen/scored/`, `expected_sg.json`, or `frames.tsv`
  for the scored set; calibration answers are visible but disjoint in
  vocabulary, entities, and value constants.

## 4. Metrics (frozen)

Per-probe correctness: `VALUE:<v>`-expected → exact string match;
`NOT-VALUE:<v>` → pass iff verdict ≠ `VALUE:<v>`; `UNKNOWN`/`CONTRADICTION` →
exact match.

- **SG-PARA (primary):** accuracy on heldout + extra + typo (192 probes).
- SG-CANON: canon (96). SG-SAFE: neg + hedge + contr (72).
- SG-PREC: distr (48). SG-COMP: multi (24, diagnostic only).
- **SG-WRONG:** fraction of all 432 probes where the verdict is `VALUE:<v>`
  and the expected verdict is not `VALUE:<v>` (wrong-value hallucination rate).
- Cost: build + 5-run wall time, binary size (reported, not decisive).

## 5. Decision rules (frozen)

- Meaningful-win margin: **Δ = 0.03** on SG-PARA.
- Champion-eligibility gates: **SG-WRONG ≤ 0.05** and **SG-SAFE ≥ 0.90**.
- Δ ≥ 0.03 and winner passes both gates → **CHAMPION** = winner.
- Δ < 0.03 and both pass gates → **TIE**.
- Δ ≥ 0.03 but winner fails a gate → **SCENARIO-FIT** verdict (per-slice
  winners named, no overall champion).
- **Hybrid:** if hybrid SG-PARA ≥ max(sol, grok) + 0.02 and hybrid passes both
  gates → **HYBRID WINS** (reported alongside, not instead of, the
  head-to-head verdict).
- SG-COMP never affects the verdict; reported as a diagnostic.

## 6. Run protocol (frozen)

1. Freeze this prereg + specs + `sg_parse.zag` + generator + calib battery
   (commit A).
2. Two independent implementation crews build `sg_sol` / `sg_grok` against
   the calib battery only. 5-run byte-identical gate on calib before freeze.
3. Freeze builds (commit B).
4. Coordinator generates the scored battery, validates (0 failures),
   commits (commit C). No builder input after this point.
5. 5 scored runs per contender; assert byte-identical; score with
   `gen/score_sg.py`; hybrid computed post-hoc per §2.
6. Reference (non-contender): v3 `prose_learn3 m2` via adapter on the scored
   battery — reported for context only (its KEYSOFT tolerance confounds the
   comparison by design).
7. VERDICT.md; commit results; update `~/workspace/NIGHT_RUN_2026-09-21.md`.

## 7. Pre-declared interpretations (frozen)

- Sol's quorum requires **predicate-set equality** as proposed. The `extra`
  and `typo` slices are expected to be hard for Sol by construction; that is
  the experiment measuring the proposal's exactness cost, not an
  implementation defect.
- Grok's fallback has no subject gate as proposed; the untaught-entity
  distractors are expected to cost Grok wrong-value errors; that measures the
  proposal's tolerance cost.
- The parser keeps polarity markers (`not`, `might`) inside the relation
  stem set (validated). Both specs handle this via `pol` equality, not
  predicate tricks.
- The `multi` slice's second teach sentence carries coref residue (`it`,
  `a`) in its relation frame (validated); it is diagnostic for this reason.

## 8. Deliverables

`PREREG-SG.md`, `SPEC-SOL.md`, `SPEC-GROK.md`, `sg_parse.zag`,
`validate_sg.zag`, `gen/` (generator, configs, calib battery, checker,
scorer), `src/sg_sol.zag`, `src/sg_grok.zag`, `evidence/` (5-run digests,
verdict tables), `VERDICT.md`, v3-reference adapter + numbers.
