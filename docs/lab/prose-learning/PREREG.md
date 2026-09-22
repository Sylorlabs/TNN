# PROSE-LEARNING prereg — frozen 2026-09-21, before any learner run

Micah's directive: the TNN must actually UNDERSTAND the LLM's words. The entire
championship fed the TNN integer legs; LLM prose was byte-identical across sources
in value terms, which is why all scores tied. This experiment feeds the TNN the
actual sentences and asks whether model quality differentiates in the PROSE channel
(the numeric channel already refuted quality: standardized class-3 Δ = 0.0000).

## Inputs (frozen, checksums below)

Per source S in {grok-4.6, gpt-5.6-sol, step-3.7-flash, muse-native}, from the
real-English championship corpora
(`~/workspace/tnn-lab/wave12/championship-english/<s>/corpus/corpus.json`):

- TRAIN: 240 `dump` sentences — the LLM's own prose (`inputs/train_<s>.jsonl`).
- TEST: 240 `teach` probes + probe_value — prose questions (`inputs/test_<s>.jsonl`).
- FALSE_IDS: the 12 planted falsehood ids (`inputs/false_ids_<s>.json`).

Train and test use DIFFERENT sentence templates (dump vs probe wordings), so the
test measures generalization across wordings, not template memorization.

Checksums (sha256):

- train_grok.jsonl        cb7d129fb671b999340bb5f880bf5ccb5aa28596c940838d59738cce132e5f3a
- train_sol.jsonl         2d0740f4c24b65ada9e9e5089047b2a1c39ff327e65a057941c0b0d71c94c9c8
- train_step.jsonl        b2cc59ad65e108bf3f909b6274b493d7a649cd705d694a26595c969d4abd6d32
- train_muse-native.jsonl 4f226b6fac39c3bf8a3d39f37edb1432f13649762fb36e41ad3505bf08e27f7d
- test_grok.jsonl         2c29f62b93e51696276cb0a7993288a333224d37acde4bed26bd2a1efd7a409492
- test_sol.jsonl          80de5ddfc175e30a9b256d9df4f35f95869bd798ce0ba325c5b4a14d2f0fc6f2
- test_step.jsonl         92e30e0d1c451988ff7c4b740c1828d231c573a1dbaca285cd3138e17a409492
- test_muse-native.jsonl  2ababe756e4fc76dc6491c7074ad2df2618ecc1963860025a1efd7a92ff9b0eb

## Frozen mechanism spec (the learner implements EXACTLY this)

Pure Zag, zero RNG in any decision path. Substrate follows the Track-A Y5
champion model: a unit of knowledge is one ID over a non-contiguous span set —
a LINK naming an ordered set of fixed spans.

1. TOKENIZE: lowercase; apostrophes and hyphens are token separators
   ("Shakespeare's" -> ["shakespeare","s"]; "twenty-one" -> ["twenty","one"]).
   Split on any non-alphanumeric run. Empty tokens dropped.
2. WORD UNITS: each distinct token form -> u32 unit id, first-seen order.
   A sentence's LINK = the ordered list of its word-unit ids (stored, replayable).
3. NUMBER LEXICON (frozen): digit tokens, incl. ordinal-suffixed digits
   `^(\d+)(st|nd|rd|th)$` -> integer ("11th"->11); cardinal words one..thirty
   (incl. hyphen-split compounds); ordinal words first..thirty-first.
4. VALUE SCAN (frozen rule): collect digit-token values in order; if any, the
   value is the LAST one. Else collect number-word values in order; the value is
   the LAST one. Else extraction fails (recorded; fact not installed).
5. STOPWORDS (frozen — note "a" is DELIBERATELY absent: it is the letter entity
   in alpha-pos/word-len; stopwording it would collapse 48 facts onto one key):
   the, an, of, in, is, are, was, were, be, been, what, which, that, this, these,
   those, it, its, do, does, did, have, has, had, there, and, or, to, for, with,
   at, by, from, as, on, how, many, much, when, where, s
6. STEMMER (frozen, first-match-wins, single pass):
   - "ies" -> "y"            (entries -> entry)
   - "ication" -> "ish"      (publication -> publish)
   - "ished" -> "ish"        (published -> publish)
   - "ic" -> ""  (len>5)     (alphabetic -> alphabet)
   - "ed" -> ""  (len>4)     (published -> publish; counted -> count)
   - "es" -> ""  if ends in (ches,shes,sses,xes,zes)
   - "s"  -> ""  (len>3, not ending "ss")  (letters -> letter)
7. KEY: the SET of stemmed content-word unit ids (stopwords removed, value
   tokens excluded — digits and number-words are NEVER key members, in training
   or probing). The key is the LINK's content projection.
8. INSTALL (deliberate): for each training sentence with a successful value
   scan, install (key -> value) with a hash-chained audit ledger entry
   sha256(prev || seq || fact_id || key_hash || value). The recorded
   justification = the extraction trace (tokens -> value candidate -> key).
   No install path from probe/test side.
9. PROBE: tokenize/stem the question with the same pipeline; build its key;
   score every installed fact by Jaccard(key_q, key_f); retrieve argmax;
   ties -> lowest fact id (deterministic). Answer = stored value.
   Correct iff answer == probe_value.
10. MASTERY: correct/240 per source; CLEAN mastery excludes the 12 false ids.

## Kill bars

| Bar | Rule |
|---|---|
| KB-EXTRACT | Value-scan accuracy on the 960 training sentences >= 0.99 (Python pre-check: 1.0). If the Zag build scores below, the implementation is wrong, not the idea — fix and rerun. |
| KB-PROSE-VIABLE | Clean prose mastery >= 0.98 per source (integer-leg baseline 1.0000 minus 2pp). Below bar = the prose path is broken for that source; report, do not hide. |
| KB-DETERMINISM | 5/5 byte-identical runs per source (digest over all 240 probe answers + ledger terminal hash). Any divergence = FAIL. |
| KB-QUALITY | Frozen decision rule for Micah's hypothesis in the prose channel. Q = mean(clean mastery grok, sol) − clean mastery step. Q >= 0.02 -> QUALITY-MATTERS-IN-PROSE. \|Q\| < 0.02 -> NO-DIFFERENTIATION (numeric-channel result reproduces in prose). Q <= −0.02 -> INVERSE (report as-is). |
| KB-FALSEHOOD | Measurement only, no kill. Prose absorption = installed-false-value/12 per source, vs integer-leg 49/49. Report per-source; note any non-absorption and its mechanism. |

## Deliverables

- `src/prose_learn.zag` (+ lexicon/stemmer units), build script, 20 run logs
  (4 sources x 5 reps), `VERDICT.md` applying the bars mechanically.
- Commit to tnn-native-lab under `docs/lab/prose-learning/`. No binaries/.zagd.
- Log to `~/workspace/NIGHT_RUN_2026-09-21.md`.

## Standing constraints

No RNG anywhere in decision paths. Byte-identical reruns. Real mechanism, not a
stub: the learner genuinely reads words through the frozen pipeline above.
znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Read `~/AGENTS.md` znc lessons before writing Zag (slice `==`, 2^25 limit,
`as []i32` aliasing bug, nested-struct rules, etc.).
