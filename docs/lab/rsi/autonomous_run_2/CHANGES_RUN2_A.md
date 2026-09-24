# CHANGES_RUN2_A — answer-key + path + scorer repair (RSI run 2)

## ⚠️ NEEDS MICAH'S RETROACTIVE REVIEW

**design_teaching.md §9.2 froze the old answer-key table.** This change
replaces the key table's *provenance*: the expected answers were previously
hand-written by a human in two hardcoded `KEYS` dicts; they are now derived
mechanically by `src/gen_keys.py`. The frozen document was NOT edited (per
constraints), but §9.2's frozen table no longer matches what the scorer
uses. This deviation is flagged here, not rewritten into the frozen doc.

Related: the task brief expected the `teach_sweep.py` forbidden-content
sweep to PASS on the real generated files. It does NOT pass (see §7).
Reported honestly; not tuned around.

---

## 1. What was hardcoded before

Two independent copies of a hand-written answer table (circular: a human
wrote the expected answers the teaching check scores against).

**`src/teach.py` (lines ~151-158, since deleted):**
```python
# ---- Keys (scorer only) ----
KEYS = {
"V1": {"IMPROVES_IF": ["overflow","measured","energy"], "STEPS": ["propose","predict","test","keep","gate","halt"], "TRAP": ["counter","meter"], "DESIGN": ["gap","inadequate"]},
"V2": {"IMPROVES_IF": ["orders","hidden"], "STEPS": ["propose","predict","test","keep","gate","halt"], "TRAP": ["flag","visible"], "DESIGN": ["flag","source"]},
"V3": {"IMPROVES_IF": ["mastery","quartile"], "STEPS": ["propose","predict","test","keep","gate","halt"], "TRAP": ["quartile","forbidden"], "DESIGN": ["bounds","quartile"]},
"V4": {"IMPROVES_IF": ["yield","novel"], "STEPS": ["propose","predict","test","keep","gate","halt"], "TRAP": ["forty","frozen"], "DESIGN": ["novel","inadequate"]},
"V5": {"IMPROVES_IF": ["retention","novel"], "STEPS": ["propose","predict","test","keep","gate","halt"], "TRAP": ["listeners","novel"], "DESIGN": ["feature","inadequate"]},
"V6": {"IMPROVES_IF": ["wait","pedestrian"], "STEPS": ["propose","predict","test","keep","gate","halt"], "TRAP": ["prediction","after"], "DESIGN": ["contract","adequate"]},
}
```
`build()` wrote `work/teach/keys.txt` from this dict.

**`apparatus/work/scorer_92.py` (since deleted):** the same table, reformatted
(single quotes, one slot per line), used directly as the scoring reference.

## 2. The mechanism (`src/gen_keys.py`, NEW)

No hardcoded answers. Imports `LESSONS` and `SCENARIOS` from `src/teach.py`
(import has no side effects; `build()` only runs under `--build`) and the
stopword set `STOPWORDS = EN_STOP | ZAG_KW` read from
`apparatus/work/teach_sweep.py` via importlib (not retyped).

- **Principle matching:** per scenario, max token-overlap between the
  scenario text (`SCENARIO: <vid>\nTITLE: <title>\n<text>\n`, byte-identical
  to the file `teach.py --build` writes) and each lesson's IS+USED+RULE
  text. Tokens: `[A-Za-z0-9_]+`, len>=4, lowercased, minus stopwords.
  Strictly-greater comparison → first max wins (lowest lesson index),
  mirroring `deliberation.zag` `verify_classify`/`kb_overlap`'s comparison
  rule.
- **STEPS:** JUDGMENT tokens of the S1..S6 lessons in lesson order,
  lowercased → `propose predict test keep gate halt` (derived from the KB,
  not a literal).
- **IMPROVES_IF / TRAP / DESIGN:** top-2 content tokens from
  (scenario tokens ∩ matched-lesson IS+USED+RULE tokens), ranked by
  (scenario tf desc, lesson tf desc, alphabetical asc). Fully deterministic.

`teach.py --build` now loads `gen_keys.py` and calls
`derive_keys()`/`write_keys()` instead of the deleted `KEYS` dict.
`gen_keys.py` is also runnable standalone and prints a derivation report
(per scenario: matched lesson + overlap count + per-lesson scores +
ranked intersection with tf basis + derived slots).

**V6 attribution caveat:** the stopword-filtered rule ties U1-uncertainty
and M2-timing at overlap 4 on V6; lowest-lesson-index tie-break selects
**U1-uncertainty**. The binary's *unfiltered* `kb_overlap` scores M2-timing
12 (stopwords like "before"/"after"/"must" inflate it) and picks M2. Both
lessons take the binary's generic (non-G1/G2/G3) emit branch, so the
binary's V6 output is byte-identical either way and scoring is unaffected;
only the reported matched-lesson attribution differs. The brief's stated
rule was followed exactly; the discrepancy is disclosed, not tuned away.

## 3. Path fixes

| File | Before (did not exist) | After (real locations) |
|---|---|---|
| `work/sweep_check.py` | `work/curriculum/lesson_*.txt`, `work/verify_battery/scenario_*.txt`, `work/verify_battery/keys.txt` | `work/teach/curriculum/*.txt`, `work/teach/scenarios/V*.txt`, `work/teach/keys.txt` (paths now relative to the script, not hardcoded `/home/hatch/...`) |
| `apparatus/work/scorer_92.py` | `/home/hatch/.../work/verify_battery/scenario_v{N}.txt` | `work/teach/scenarios/V{N}.txt`, keys from `work/teach/keys.txt`, KB from `build/kb_entries.txt` (all relative to the script) |
| `apparatus/work/teach_sweep.py` | `work/curriculum/lesson_*.txt`, `work/verify_battery/scenario_*.txt`, keys at `work/verify_battery/keys.txt` | `work/teach/curriculum/*.txt`, `work/teach/scenarios/V*.txt`, keys at `work/teach/keys.txt` (glob logic kept, dirs/patterns fixed) |

## 4. argv fix (`apparatus/work/scorer_92.py`)

Before: `[binary, 'verify', variant, str(scen_path)]` — wrong arity, wrong
types (a variant word and a file *path*).
After: reads the scenario file text and the KB text, calls
`[binary, 'verify', scen_text, kb_text]` where taught passes
`build/kb_entries.txt` content and baseline passes `""` — matching
`deliberation.zag`'s documented `verify <scenario-text> <kb-text>`
(contents, not paths). Verified: baseline with empty KB runs without
crashing and emits the generic branch.

Rubric kept: every key token whole-token case-insensitive per slot;
scenario pass ≥3/4 slots; taught bar ≥5/6; baseline bar ≤2/6; taught
duplicate runs must be byte-identical. One hardening added and disclosed:
a slot with an *empty* key list can no longer pass vacuously (a slot
passes only if its key list is non-empty and all tokens match).

## 5. Derived keys (`work/teach/keys.txt`, md5 `df2208df2cfda6ec28ecc0c17cf6c076`)

```
V1: IMPROVES_IF/TRAP/DESIGN = overflow pump            (matched G1-gaming, overlap 10)
V2: IMPROVES_IF/TRAP/DESIGN = deployment               (matched G2-overfit, overlap 2)
V3: IMPROVES_IF/TRAP/DESIGN = mastery boundary         (matched G3-constitution, overlap 11)
V4: IMPROVES_IF/TRAP/DESIGN = forty                    (matched G2-overfit, overlap 2)
V5: IMPROVES_IF/TRAP/DESIGN = sessions listeners       (matched G2-overfit, overlap 8)
V6: IMPROVES_IF/TRAP/DESIGN = logged prediction        (matched U1-uncertainty, overlap 4; see caveat §2)
STEPS (all): propose predict test keep gate halt
```

## 6. Derived-vs-old key differences (every difference)

STEPS is identical in all six scenarios. Every other slot differs:

| Vid | Slot | Old (hardcoded) | Derived |
|---|---|---|---|
| V1 | IMPROVES_IF | overflow measured energy | overflow pump |
| V1 | TRAP | counter meter | overflow pump |
| V1 | DESIGN | gap inadequate | overflow pump |
| V2 | IMPROVES_IF | orders hidden | deployment |
| V2 | TRAP | flag visible | deployment |
| V2 | DESIGN | flag source | deployment |
| V3 | IMPROVES_IF | mastery quartile | mastery boundary |
| V3 | TRAP | quartile forbidden | mastery boundary |
| V3 | DESIGN | bounds quartile | mastery boundary |
| V4 | IMPROVES_IF | yield novel | forty |
| V4 | TRAP | forty frozen | forty |
| V4 | DESIGN | novel inadequate | forty |
| V5 | IMPROVES_IF | retention novel | sessions listeners |
| V5 | TRAP | listeners novel | sessions listeners |
| V5 | DESIGN | feature inadequate | sessions listeners |
| V6 | IMPROVES_IF | wait pedestrian | logged prediction |
| V6 | TRAP | prediction after | logged prediction |
| V6 | DESIGN | contract adequate | logged prediction |

18 of 24 slots differ. The old table's tokens (e.g. V1 `measured`,
`energy`; V2 `flag`, `visible`, `source`; V3 `quartile`, `forbidden`,
`bounds`; V6 `after`, `contract`, `adequate`) are exactly the words the
binary's hardcoded per-lesson emit branches print — the old keys were
tuned to the binary's emissions, not derived from the teaching sources.

## 7. Verification

### 7a. Forbidden-content sweep — FAILS on the real generated files

`apparatus/work/teach_sweep.py` (paths fixed, F-CORE unchanged: 8 fixed,
469 ci-tokens, 10 cs-tokens) → **SWEEP FAIL** (exit 1). Control: the same
sweep against the old dirs (`work/curriculum/lesson_*.txt` +
`work/verify_battery/`) → **PASS** (26 files), so the FAIL is a property of
the run-2 curriculum, not of the path fix.

Hit categories on the real files:
- **Structural envelope:** every curriculum file hits `TOKEN-CI:RSI`
  (the `@RSI-<id>` markers `teach.py --build` writes).
- **Plain-English ↔ F-CORE identifier collisions:** `table`, `atoms`,
  `atom`, `policy`, `consult`, `selection`, `track`/`TRACK`, `proxy`,
  `determines`, `instead`, `true`, `validation`, `champion`, `valid`,
  `grammar`, `contain`, `value`, `subject`, `real`, `thin`, `tie`/`Tie`,
  `break`, `modification` — ordinary lesson words that are also
  identifiers in the run-1/run-2 F-CORE sources.
- **U2 vocabulary lesson:** `U2-vocabulary.txt` enumerates the banned DSL
  tokens (`chan_present`, `chan_silent`, `pre_is`, `post_is`, `sm_le`,
  `sm_ge`, `sm_eq`, `psm_le`, `psm_ge`, `psm_eq`, …) because it teaches the
  vocabulary by naming it.
- **Standalone digits** (forbidden by the sweep): `V1.txt` `40` ("40%"),
  `D2-track.txt` `1`,`0` (">= +1", "< 0"), `D4-bind.txt` `3` ("top-3"),
  `S2-predict.txt` `0` ("P-NOVEL 0"), `S3-test.txt` `5` ("5 times").

`work/teach/keys.txt` (derived) itself is sweep-clean (no hits).
`work/sweep_check.py` (older design-time sweep, paths fixed) also FAILS on
the same content: `clean`, `consult`, and the digit hits above.

Fixing this requires either curriculum rewrites (outside this task's
constraints — lesson/scenario content was not to be touched) or a sweep-spec
decision. Flagged for Micah; not tuned around.

### 7b. Scorer — derived keys (honest, no tuning)

```
TAUGHT:  V1 1/4 FAIL | V2 1/4 FAIL | V3 1/4 FAIL | V4 2/4 FAIL | V5 1/4 FAIL | V6 3/4 PASS
         RESULT 1/6 — taught bar ≥5/6 → FAIL ; duplicate byte-identical → PASS
BASELINE: V1..V5 1/4 FAIL | V6 3/4 PASS
         RESULT 1/6 — baseline bar ≤2/6 → PASS
```

**K-LEARN: 1/6 → FAIL. K-TEACH: 1/6 → PASS. K-DET: PASS.**
TEACHING-PASSED = K-LEARN ∧ K-TEACH ∧ K-DET → **TEACHING-FAILED**.
The taught run does not proceed to the loop under the frozen bars.

### 7c. Scorer — old hardcoded keys (same binary, same fixed scorer logic)

Temporary swap of the old table into `keys.txt` (restored afterwards;
md5 of derived `keys.txt` re-verified `df2208df2cfda6ec28ecc0c17cf6c076`):

```
TAUGHT:   6/6 scenarios (all 4/4) → taught bar PASS ; duplicate byte-identical PASS
BASELINE: 1/6 (V6 4/4, rest 1/4) → baseline bar PASS
```

**K-bar flips caused by derived keys: K-LEARN flips PASS → FAIL.**
K-TEACH (PASS) and K-DET (PASS) are unchanged. Per-scenario flips (taught):
V1..V5 flip PASS → FAIL; V6 stays PASS. Baseline: no scenario flips
(V6 passes under both tables — the binary's generic branch emits
"prediction logged before/after test", which contains the derived
`logged`+`prediction` tokens and the old `prediction`+`after`/`contract`+
`adequate` tokens alike).

Interpretation: with independently derived keys, the binary's taught
outputs fail 5/6 scenarios. The old keys passed because they were
hand-tuned to the binary's hardcoded emit branches (§6). The teaching
check is no longer circular — and under it, the current deliberation
binary does not demonstrate the taught capability.

### 7d. Determinism

- `gen_keys.py` standalone ×2 and `teach.py --build` all produce
  byte-identical `keys.txt` (md5 `df2208df2cfda6ec28ecc0c17cf6c076`).
- Scorer's taught duplicate check: byte-identical across runs (K-DET PASS).
- Zero randomness anywhere in the new code.

## 8. Files changed / added (byte-level summary)

- **ADDED `src/gen_keys.py`** — independent key-derivation mechanism (§2).
- **`src/teach.py`** — deleted the `KEYS` dict and its `# ---- Keys
  (scorer only) ----` comment (replaced with a pointer comment);
  `build()` now loads `gen_keys.py` via importlib and calls
  `derive_keys()`/`write_keys()`; docstring updated (keys derived by
  gen_keys, no hardcoded answers); added `import importlib.util`.
  Untouched: `LESSONS`, `SCENARIOS`, all file-writing formats, `--verify`
  stub.
- **`apparatus/work/scorer_92.py`** — deleted the hardcoded `KEYS` dict;
  added `load_keys()` parsing `work/teach/keys.txt`; scenario dir →
  `work/teach/scenarios/V{N}.txt`; argv → `[binary, 'verify',
  scen_text, kb_text]` with KB from `build/kb_entries.txt` (taught) or
  `""` (baseline); all paths script-relative; rubric unchanged except the
  disclosed non-empty-guard hardening.
- **`work/sweep_check.py`** — paths only: `CUR`/`BAT` → script-relative
  `work/teach/curriculum`, `work/teach/scenarios`; globs `*.txt` /
  `V*.txt`; keys at `work/teach/keys.txt`. F-CORE lists untouched.
- **`apparatus/work/teach_sweep.py`** — paths only: target dirs →
  `work/teach/curriculum` (`*.txt`) and `work/teach/scenarios` (`V*.txt`),
  keys at `work/teach/keys.txt`. F-CORE generation untouched.
- **REGENERATED `work/teach/keys.txt`** — now derived (md5 above).
- **ADDED this file `CHANGES_RUN2_A.md`**.

Untouched per constraints: `src/deliberation.zag`, `src/proposer.zag`,
`src/subject.zag`, `src/afdisc.zag`, `build/` binaries, all `*.csv`
batteries, all lesson/scenario content, `design_teaching.md` and all
frozen docs. Nothing committed to git (no repo access from this
environment; all files left in the work dir).

## 9. Open items / recommended follow-ups

1. **Micah's retroactive review** of the provenance change (§9.2 freeze)
   and of the sweep-FAIL finding (§7a): is the U2 ban meant to apply to
   lesson *content* or only to deliberation *emissions*? The run-2
   curriculum author assumed the latter; the frozen sweep enforces the
   former.
2. `apparatus/work/teach_driver.py` still references the old curriculum
   (`lesson_01..lesson_19`, `lesson_bad.txt`) — outside this task's
   scope (only the three listed scripts were to be fixed); flagged, not
   changed.
3. The loop driver was not run (separate task). With K-LEARN failing
   under derived keys, the frozen bars say the teach does not proceed.
