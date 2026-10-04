# CLN-1 — Code Cleanliness Audit (FROZEN PREREG)

**Frozen:** 2026-09-22 · **Order:** Micah — "how clean is its code" — as a preregistered measurement, not an opinion.
**Branch:** `tnn-native-lab` · **Dir:** `coding/reflection/cleanliness/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 0. The question, operationalized

Cleanliness = the rubric in §1. Two families, scored separately:
- **Mechanical (M1–M3):** measured deterministically by a pure-Zag checker. No taste involved.
- **Taste (T1–T4):** scored by blind LLM judges on a 0–2 anchored scale.

## 1. Rubric (0–2 per dimension, anchored)

### Mechanical (checker.zag, deterministic)
- **M1 — Dead code.** 2 = zero instances of (a) defined-never-called functions
  (except `main`), (b) statements after `return` in the same block,
  (c) declared-never-used locals. 1 = 1–2 instances. 0 = 3 or more.
- **M2 — Function length.** 2 = longest function ≤ 25 non-blank lines.
  1 = 26–50. 0 = any function > 50 lines.
- **M3 — Nesting depth.** 2 = max brace depth ≤ 3. 1 = 4. 0 = ≥ 5.

### Taste (blind judges, 0–2)
- **T1 — Naming clarity.** 2 = names reveal role (`total`, `found_index`);
  1 = mostly clear, 1–2 cryptic; 0 = systematically cryptic (`a`,`b`,`x2`) or misleading.
- **T2 — Comments where non-obvious.** 2 = non-obvious logic explained,
  obvious code uncommented; 1 = sparse but present where needed; 0 = none where
  needed, or noise comments restating the code.
- **T3 — Error handling completeness.** 2 = failure modes handled or honestly
  surfaced; 1 = partial; 0 = silent wrong behavior possible.
- **T4 — Idiom.** 2 = uses Zag's own patterns (`_zag_print`, i64 arithmetic,
  `while` loops, slice access); 1 = works but fights the language;
  0 = transliterated from another language's idioms.

## 2. Battery (SPECS.json, frozen here)

20 fresh specs, disjoint from `loop/battery.json`, `speed_intel` batteries, and the curriculum:
- **R1–R8 (repair):** broken Zag seeds, one per defect class
  (TYPE, NAME, ARITY, SYNTAX, DUPFN, OUTPUT_FORMAT, LOGIC_VALUE off-by-one, LOGIC_VALUE value).
  Spec text: "Repair the broken program so it compiles and passes its tests."
- **G1–G8 (write-from-spec):** T1|FUNC max2, T1|LOOP range_sum n=50, T1|STR count_ch,
  T1|SLICE sum_arr, T2|SORT bubble_asc, T2|MATH gcd, T2|STR reverse, T1|STRUCT manhattan.
- **T1–T4 (small tools):** T4|GOAL lcm(15,25), 3^7, sum 1..20, 2^16.

Every spec has frozen tests (args/stdout/rc). Specs are byte-frozen in SPECS.json.

## 3. Arms (per spec, 4 implementations)

- **TNN:** pinned learner binary `loop/work/learner`
  (sha256 recorded in RESULTS; binary rebuilt only if source changes, then re-pinned).
  Gen items (G/T): `learner gen '<spec>' '<patterns>' '<demo>'`.
  Repair items (R): full `driver.py` loop on the seed; artifact = final source.
  If an arm fails to produce compiling+passing code after the loop budget, one
  retry; then record FAIL and exclude that spec from judging (report the failure).
- **HUMAN:** clean-room Zag by the auditor, written from SPECS.json ONLY,
  BEFORE any TNN generation is run or viewed. Committed before TNN gen.
- **SOL:** `gpt-5.6-sol` via unorouter. Prompt = ZAG_PRIMER.md + spec text +
  "Write a clean, complete, compilable Zag program. Output code only."
- **GROK:** `grok-4.6` via unorouter, identical prompt. Model labeled explicitly everywhere.

All four arms' sources land in `sources/<spec>/{tnn,human,sol,grok}.zag`, each
verified to compile and pass its frozen tests before judging.

## 4. Blind judging protocol

Per spec, the 4 sources are shuffled and labeled W/X/Y/Z. The mapping is sealed in
`sealed_mapping.json`, committed BEFORE any judging call. Judges:
- **sol** (gpt-5.6-sol) and **grok-4.6**, each scores every snippet on T1–T4 (0–2,
  anchored rubric quoted verbatim in the judge prompt) AND guesses the source
  (tnn / human / llm) with a confidence 0–1.
- Judge prompt contains the rubric and the code only — no spec, no arm labels.

Report: per-dimension mean per arm (each judge separately + pooled), and the
3-way source-attribution confusion matrix.

## 5. Mechanical checker

`checker.zag` (pure Zag, zero RNG) computes M1–M3 per source. 3 runs;
byte-identical output required. Report per-arm per-dimension means.

## 6. Self-critique arm

Question: can TNN itself tell clean from dirty — is cleanliness something it
*knows*, or just something it *does*?

- For each of the 20 TNN outputs, 3 dirtied variants by DETERMINISTIC
  transformation (fixed, no RNG):
  (a) **dead-code injection:** append one uncalled fn + one post-return statement;
  (b) **name scrambling:** rename all locals to v1..vn (fixed order);
  (c) **nesting inflation:** wrap each function body in `if(1==1){ ... }`.
- A Zag judge binary (`judge.zag`, deliberative scoring over the frozen rubric
  features with scored evidence + traces, zero RNG) ranks each clean-vs-dirtied
  pair (60 pairs). It is calibrated on 3 held-out practice pairs
  (`practice/`), NOT from the battery.
- The blind-judge majority ranking is the oracle (dirt is designed to be
  obvious; unanimous clean>dirty expected — verified, not assumed).
- **Score:** agreement fraction. ≥ 0.80 = knows clean; 0.60–0.80 = partial;
  < 0.60 = does not know.

## 7. Kill bars

- **TNN code is CLEAN** iff ALL of:
  (i) |mean_TNN − mean_HUMAN| ≤ 0.25 on EACH of M1–M3 (quarter-step noise bar), AND
  (ii) judges' 3-way source-attribution accuracy on TNN snippets ≤ 0.40
  (chance = 0.333).
- **DIRTY on dimension D** iff |mean_TNN − mean_HUMAN| > 0.50 on D — then the
  verdict MUST name the dimension and the mechanism (from trace/artifact
  inspection, e.g. "repair loop appends patch fns instead of restructuring").
- Taste gaps > 0.75 on any T-dimension are flagged (not kill-barred; taste is noisier).

## 8. Commitments

- This prereg + SPECS.json + ZAG_PRIMER.md frozen and committed BEFORE any generation.
- `sources/*/human/*.zag` committed BEFORE any TNN generation.
- `sealed_mapping.json` committed BEFORE any judging call.
- Commit via `~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
  lab-relative paths (no `docs/lab/` prefix). No binaries, no `.zagd`, no `.zag-cache`.
- Determinism: checker 3× byte-identical. LLM judge raw outputs committed verbatim.
- Final: RESULTS_CLN1.md with the blind-judge table, mechanical table,
  self-critique score, and the CLEAN/DIRTY verdict.
