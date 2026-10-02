# No-Arbitrary-Limits Hunt

**Date:** 2026-09-27 (overnight wave, hunter line A6)
**Ordered by:** Micah's standing law — TNN must not carry arbitrary hard limits.
**Source:** `origin/tnn-native-lab @ 5b661730d` (read-only sweep of committed sources; no code changed)
**Method:** grep sweep across the live decision engines (dialogue round-4, deliberation, one-brain v3,
chunker/intake, image upscale, video composer, pig-front, audio planner, memory_org, pricing governance,
native epistemics), then read-context verification of every candidate. **No phantom listings:** each
entry below was read in its source file; the "22px" precedent (observed error, not a literal) was the
standard — anything not confirmed in code is not listed.

**Adjudication standard:**
| Verdict | Meaning |
|---|---|
| LOAD-BEARING | Physical, toolchain, or format-spec necessity — cite the constraint. Do not "fix". |
| ARBITRARY | Crew-authored choice TNN could make itself. Gets a conversion work order. |
| DECLARED SCAFFOLD | Arbitrary but honestly labeled in code/docs as a trial parameter. Convert later, no deception now. |
| FIXTURE | Trial-test geometry, not a TNN architectural claim. |

**Authorship boundary (from the decoration audit):** a GENUINE mechanism can still be CREW-SCAFFOLDED
in its policy. This hunt targets the policy layer: thresholds, menus, tie-breaks, taxonomies, weights.

---

## 1. Dialogue line — frozen English in code

### 1.1 Frozen morphology tables — ARBITRARY
`docs/lab/dialogue/round4/dialogue.zag` (mirrored in `docs/lab/dialogue/deliberation/deliberate.zag`):
- `stem_inplace` (~line 271): frozen suffix-strip table (`ies/ication/ished/ic/ed/ches/shes/sses/xes/zes/s`),
  header comment: "stemmer (frozen, first-match-wins, single pass)".
- `irregular_norm` (~line 303): closed irregular-form list — birth/born/borne, taught/teaching,
  ran/running, spoke/spoken/speaking, thought/thinking, built/building, won/winning, plus one-offs
  `upscale`, `reproduce` added 2026-09-27.
- `numword_val` (~line 219): frozen English number-word table (one..twenty, thirty, ordinals first..nineteenth).
- Comparative list (~line 342): exactly 7 words — taller/older/longer/bigger/smaller/earlier/later.
  Comment: "Closed list only."

The *mechanism* (suffix stripping, normalization) is fine scaffolding. The *content* — which English
forms exist — is crew-authored linguistic knowledge frozen in code. TNN never learned any of it.
**Native direction:** morphology as TNN-learned/taught knowledge (the units mechanism in round-4
already proved taught-fact derivation works for units; same treatment for word forms).

### 1.2 Closed relation vocabulary `is_relkey` — ARBITRARY
`dialogue.zag` ~line 2400: 20 hardcoded words
(wrote/written/bear/build/publish/discover/win/capital/tall/long/open/dedicate/complete/landmark +
TNN-domain upscal/reproduc/detect/learn/paint/invent). The G6 repair's own comment calls it a
"closed relation vocabulary (is_relkey)". The repair generalized *around* it; the list remains.
**Native direction:** derive relation-hood from taught facts (a predicate is a relation iff the KB
teaches it as one), not from a crew list.

### 1.3 Frozen pragmatic word lists — ARBITRARY
- `is_meta_verb`: tell/give/show/describe (4 words).
- `is_discourse`: please/ok/okay/yo/hey/hi/oh/ah/um/uh (10 words).
- One-brain v3 reading triggers (`docs/lab/onebrain3/impl/onebrain_v3.zag`, `rd_trig` ~line 234):
  10 readings × crew-authored English trigger words ("no/actually/meant/correction", "knock"→joke, …).

Micah's standing direction is that utterance types ("I think", politeness markers, discourse particles)
are *learned* knowledge. Hardcoding them is the exact vision violation.
**Native direction:** learned utterance-type knowledge (queued behind the native-epistemics verdict).

### 1.4 Event precedence ordering — ARBITRARY
`dialogue.zag:2239`: `born->built->published->dedicated->opened->completed->won, first KB hit wins`.
A frozen precedence chain over life-event predicates, crew-ordered.
**Native direction:** derive ordering from taught facts or deliberate the precedence per question.

### 1.5 Typo tolerance constants — ARBITRARY (constants; principle reasoned)
`typo_near` (~line 2532): `tol=2`, dropping to `tol=1` when word length ≤ 4. The length-scaling
principle is documented and root-caused (the "eat"/"bear" incident); the constants 2 and 4 are
crew-chosen. **Native direction:** learn tolerance from observed typo confusions, or derive from the
vocabulary's own collision statistics.

### 1.6 Stopword list — ARBITRARY (minor)
`is_stop` (~line 296): single-letter stopwords only — a/i/s/t. A frozen minimal list; harmless at
current scale, but it is crew linguistics, not TNN knowledge.

### 1.7 Levenshtein cap — MIXED
`word_dist` (~line 2492): distance "capped at 3 with early exit" — crew accuracy/speed trade
(ARBITRARY). The 40-char word truncation (`if(al>40){al=40;}`) follows the 164-byte DP buffer
geometry (41 cells × 4 bytes) — **LOAD-BEARING**.

---

## 2. Tie-breaks — existence load-bearing, choice arbitrary

Micah's determinism law makes *a* fixed tie-break LOAD-BEARING. *Which* order is crew-chosen
everywhere:

| Site | Rule | File |
|---|---|---|
| Fact/entity lookup | lowest fid / lowest eid wins ties | dialogue.zag:1112,3034; deliberate.zag:1057,2482 |
| Deliberation ARGMAX | max score; ties → lowest hid | deliberate.zag:2683,3230-3231 |
| Joke stock | greatest height-contrast first, then lower eid (crew aesthetic: why contrast-first?) | ROUND4_HARDCODE_COMPLETION.md; dialogue.zag:3062 |
| memory_org | "fewer levels, then lowest index" — code literally names it `scheme_levels_frozen`, comment "argmax with frozen tie-break" | memory_org/arms/lib.zag:599,764; fn at :323 |
| Video composer | "tie on total; lowest plan index wins (deterministic tiebreak)" | composer_base.zag:1436,1488 |
| Chunker policy | selection law "most correct → most native → fewest ops → coarser chunking → lower candidate id" | mg_chunking_batteryfix/intake.zag:14-17 |

**Native direction:** TNN-deliberated (or at minimum TNN-recorded and auditable) ordering policy.
Lowest-ID-wins is the zeroth choice, not a reasoned one.

---

## 3. Frozen candidate menus

### 3.1 Deliberation GEN menu — ARBITRARY
`deliberate.zag:2675`: "GEN: 10 readings (hid 0..9) + up to 3 fact candidates (hid 10..12)".
One `gen_*` function per reading kind. The GEN→ELIM→ARGMAX pipeline is genuine, but GEN can only
ever propose the crew's 10 kinds. TNN never invents a candidate.
**Native direction:** TNN-generated candidate hypotheses (the invention program's territory).

### 3.2 Video composer plan menu — ARBITRARY
`docs/lab/imagination/video-fusion-step6/src/composer_base.zag:798`: "plan indices (fixed
enumeration, every run)": 18 fixed plans across 5 families (OVERLAY/PIP/SPLIT/INTERLEAVE/XFADE),
with INTERLEAVE k=2 and XFADE n=8 baked in. The composer can never propose a 19th plan.
**Native direction:** TNN-composed plans from observed footage (see-its-result WO-1 is adjacent).

### 3.3 Chunker policy table — ARBITRARY (owned by B2)
`docs/lab/mg_chunking_batteryfix/intake.zag:2150` `policy_winner`: frozen 22-kind → candidate table
(derived by `mg_chunking_learned/derive.zag` from 9 candidates × 57 questions), `classify` with
frozen English phrase triggers ("how many words in", "backwards", "'s in", …), and frozen
`policy_why` explanatory prose. The native-authorship program (B2) already owns this conversion;
recorded here for completeness.

---

## 4. Audio planner — constants on the hear→plan path

### 4.1 `clamp_f0` — ARBITRARY (and contradicts its own docs)
`docs/lab/audio_longhorizon/planner_vocab/src/plan_main.zag:513`: heard f0 clamped to
60000..2000000 (mHz). It is genuinely on the decision path (:809, :1402-1403). Meanwhile the
self-cal section's header claims "No frozen gain constant. No clamp constant." — the claim is
false; a clamp constant exists three hundred lines above it.
**Native direction:** derive the operating range from the extractor's and renderer's *measured*
capability (the self-cal machinery already measures; use it).

### 4.2 Envelope taxonomy — ARBITRARY
`print_env_name` (:284): the planner's entire envelope vocabulary is three crew-named bins —
flat/rise/decay. Every heard envelope is forced into one.
**Native direction:** TNN-developed envelope descriptors from its own hearings.

### 4.3 Error weights — ARBITRARY
`native_err_pm` (:548): `+500` for env mismatch, `+500` for cv outside ±25%, f0 term gated on
`f0ref>=125000`. The 500s price an envelope error against a pitch error by crew fiat.
**Native direction:** learned error weighting — thermometer before thermostat (measure first).

### 4.4 Vocab cap — DECLARED SCAFFOLD
`vocab_add` (:523): 32-entry cap, but the code says so loudly — "a trial memory-size parameter,
NOT a deliberative limit" — and journals `VOCAB_FULL` instead of silently dropping. Honest.
**Conversion note:** dynamic growth when the trial needs it.

### 4.5 Calibration knots — ARBITRARY (minor, declared)
`bias_ppm_at` (:569): piecewise-linear bias with knots at 90/220/1010 Hz. The *values* are
self-measured (good); the *knot frequencies* are crew-chosen probe points.

---

## 5. Memory / pricing

### 5.1 Effort schedule divisor — ARBITRARY
`docs/lab/destruction-pricing-governance/src/strength_core.zag:390`: `n(s) = ceil(s/25)`.
Why 25? Crew constant pricing every unit of deliberative effort.
**Native direction:** calibrate from measured deliberation cost (ties to the pricing-weights
learn-them direction, audit P3 #10).

### 5.2 Pricing personalities taxonomy — ARBITRARY
`ST_PRICE_HIGHWATER/DELIB/METER`, `ST_DELIB_HIST/FRESH/METER`, 21–30 meter reason codes —
frozen crew taxonomy over pricing modes (strength_core.zag:90-110). Recorded; owned by the
weights-learning direction.

---

## 6. Native epistemics — thresholds in the "native" line

### 6.1 Verdict thresholds — ARBITRARY
`docs/lab/epistemic_native/implementation/epistemic.zag:89-99`, comment "// thresholds (committed)":
`con_fires`: neg&&ov≥28, num&&ov≥40, ent&&ov≥35; `sup_fires`: ov≥50 with no flags. This is the
*native-deliberation* line — born from Micah's correction that epistemic status must be TNN's own
deliberative judgment, not a crew pipeline — and it still carries four frozen numeric cutoffs on
an overlap score. **Native direction:** deliberative judgment over the evidence without fixed
cutoffs (the prereg's K6 bar governs outcomes, not the mechanism's constants).

---

## 7. One-brain v3 — evidence-gathering constants

`docs/lab/onebrain3/impl/onebrain_v3.zag`:
- Trigger window `qi-4` (~line 488): a trigger "counts" only within 4 tokens — crew window size. ARBITRARY.
- Topic cap `tc<20` (~line 484): max 20 topic tokens per reading — crew cap. ARBITRARY.
- `rd==7 || rd==9` special-casing (~line 487): hardcoded reading-kind exceptions. ARBITRARY.
- 25-row ledger geometry / 12-fact embedded KB — trial-fixture geometry. FIXTURE, not a TNN limit.

---

## 8. Load-bearing limits — correctly applied, do NOT convert

These look like arbitrary limits but are necessities. Mislabeling them would be as bad as the reverse.

| Limit | Why load-bearing | Where |
|---|---|---|
| 2^25-byte slice ceiling | znc toolchain: no single slice > 33,554,432 bytes can be indexed | `universal_intake/src/flac.zag:466` (`out_bytes >= 33554432` guard) — textbook correct |
| 40-char Levenshtein truncation | Follows the 164-byte DP buffer (41×4B); raising it needs a bigger buffer, not a policy change | dialogue.zag `word_dist` |
| Deterministic tie-break *existence* | Micah's determinism law: byte-identical reruns require a fixed order | everywhere in §2 — only the *choice* of order is arbitrary |
| Format-spec constants | The file format dictates them, not the crew (JPEG markers, PNG Huffman tables, Adler-32 65521, FLAC frame types) | `universal_intake/src/*` |
| Ledger/arena field offsets | Memory layout, not a decision limit | onebrain_v3.zag, dialogue.zag arenas |
| 25-row ledger / 12-fact KB | Frozen *test fixture* geometry for the round-3 trial | onebrain_v3.zag:371-379 |
| Upscale 256×92 survey geometry | Observation fixture size | azupscale.zag:608 |

---

## 9. Conversion work orders (for the native-authorship program, B2)

Ordered by decision-path impact. Hunt only — B2 owns design and kill bars.

| # | Arbitrary limit | Convert to | Owner |
|---|---|---|---|
| WO-1 | Frozen English morphology + relation/pragmatic vocabularies (§1.1–1.3) | TNN-learned/taught linguistic knowledge | B2 (dialogue) |
| WO-2 | Reading-trigger word lists (§1.3, §3.1 GEN menu) | Learned utterance types + TNN-generated candidates | B2 (dialogue/deliberation) |
| WO-3 | Chunker policy table + classify triggers (§3.3) | TNN-deliberated chunking choice | B2 (already first conversion) |
| WO-4 | Tie-break orders (§2) | TNN-recorded/deliberated ordering policy | B2 |
| WO-5 | Audio clamp/weights/envelope taxonomy (§4.1–4.3) | Measured/derived operating range, learned error weights, TNN envelope descriptors | B2 (audio) |
| WO-6 | Pricing effort divisor + weight taxonomy (§5) | Calibrated/learned pricing | B2 (memory) |
| WO-7 | Epistemic verdict thresholds (§6.1) | Cutoff-free deliberative judgment | B2 (epistemics) |
| WO-8 | Video 18-plan menu (§3.2) | TNN-composed plans | B2 (video; adjacent to see-its-result WO-1) |
| WO-9 | One-brain evidence constants (§7) | Deliberated or measured evidence bounds | B2 (one-brain) |

**Not work orders:** §8 load-bearing items, §4.4 declared scaffold (convert opportunistically),
fixture geometry, and the pig-front geometry (already audit P1 #4, comment-fix + native-authorship queue).

---

## 10. Notes and non-findings

- The "22px" case was correctly excluded: it was the observed head-placement *error*, never a literal.
  Every entry above was read in source.
- `docs/lab/dialogue/dialogue.zag` (top level) is a dead pre-round-4 artifact per the audit; its
  hardcodes were not inventoried (flagged for archival marking already).
- Historical trial variants (round-2 repairs, killed arms, superseded batteries) were not swept —
  only live/adopted decision paths.
- The joke-stock "greatest height contrast first" ordering (§2) deserves a second look by B2: it is a
  crew aesthetic (funniest = biggest contrast?) masquerading as a neutral order.
