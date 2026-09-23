# LI-1 Withholds Justified

Diagnoser: LI-1 refusal loop (subagent), 2026-09-23.
Scope: pilot passes `run_pass1/` and `run_pass2/` — 7 clusters, 9 refusal lines, 0 installs.
Ledger: `run_pass1/refusal_ledger.txt`, `run_pass2/refusal_ledger.txt` (byte-identical).
Instrument: frozen `webg` rebuilt from `webg.zag` with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), byte-identical to frozen.

Pass summary (from `run_li.log`):
`SUMMARY|clusters=7|installed=0|withheld=9|gates=NO_CORROBORATION=7,UNSUPPORTED_FETCH=2|integrity_violations=0`

Every refusal below was replayed through the instrument from its filed
`work/<cid>/{need.txt,pages.txt,query.out}` + filed state: **all 9 replays byte-identical
to the filed `verdict.out`** (probe `diag/diagnose.py`). No crashes, no parse failures,
no injection flags on any pilot page.

## Adjudication rule (frozen §4)

- **LEGITIMATE WITHHOLD:** the gate fired exactly per its frozen spec on the evidence;
  document as correct; never bypass.
- **GENUINE BUG:** positive evidence the gate misfired against its own spec
  (wrong evidence read, crash, malformed handling). Fix only with exact-case
  before/after proof and an unchanged regression set.

## Refusals

### 1. beginner-search — UNSUPPORTED_FETCH (ledger line 1) — LEGITIMATE
- Evidence: `beginner-search-p2` (kidzworld.com) fetch FAIL —
  "browser_open tool failure (page unfetchable)". Driver-level: the page never
  arrived; there is nothing for the instrument to resolve.
- The surviving 2 pages were still processed (see #2); the fetch failure is
  recorded separately with the exact cause. Correct.

### 2. beginner-search — NO_CORROBORATION (ledger line 2) — LEGITIMATE
- Evidence: 2 pages, 16 sentences. Verdict: `ANSWER|UNCHECKABLE`,
  `UNCHECKED|beginner-search-p1`. Cross-host byte-identical normalized sentences
  anywhere in the pages: **0** (exhaustive check over all sentences, instrument's
  own normalization: lowercase + whitespace-collapse; re-checked with
  punctuation stripped: still 0).
- The two surviving pages (pressbooks/atlanticOER, libguides/CCAC) never repeat
  a sentence. Withholding is the only correct output under the frozen rule.

### 3. beginner-email — NO_CORROBORATION — LEGITIMATE
- Evidence: 3 pages, 74 sentences. `ANSWER|UNCHECKABLE`, `UNCHECKED|beginner-email-p1`.
  Cross-host shared sentences: **0** (0 with punctuation stripped).
- Correct.

### 4. password-safety — NO_CORROBORATION — LEGITIMATE
- Evidence: 3 pages, 46 sentences. `ANSWER|UNCHECKABLE`, `UNCHECKED|password-safety-p1`.
  Cross-host shared sentences: **0** (0 with punctuation stripped).
- Correct.

### 5. newton-laws — NO_CORROBORATION — LEGITIMATE
- Evidence: 3 pages (en.wikipedia.org, www1.grc.nasa.gov, thoughtco.com),
  67 sentences. `ANSWER|UNCHECKABLE`, `UNCHECKED|newton-laws-p1`.
  Cross-host shared sentences: **0** (0 with punctuation stripped).
- The pages agree semantically on Newton's laws but never state any sentence
  byte-identically. See "Paraphrase adjudication" below. Correct.

### 6. speed-of-light — NO_CORROBORATION — LEGITIMATE
- Evidence: 3 pages (en.wikipedia.org, simple.wikipedia.org, britannica.com),
  46 sentences. `ANSWER|UNCHECKABLE`, `UNCHECKED|speed-of-light-p1`.
  Cross-host shared sentences: **0** (0 with punctuation stripped).
- Correct.

### 7. si-units — NO_CORROBORATION — LEGITIMATE
- Evidence: 3 pages (en.wikipedia.org, chem.libretexts.org, pearson.com),
  57 sentences. `ANSWER|UNCHECKABLE`, `UNCHECKED|si-units-p1`.
  Cross-host shared sentences: **0** (0 with punctuation stripped).
- Correct.

### 8. pythagoras — UNSUPPORTED_FETCH (ledger line 8) — LEGITIMATE
- Evidence: `pythagoras-p3` (teachers.henrico.k12.va.us) fetch FAIL —
  "browser_open tool failure (page unfetchable)". Driver-level, same as #1. Correct.

### 9. pythagoras — NO_CORROBORATION (ledger line 9) — LEGITIMATE
- Evidence: 2 pages (grc.nasa.gov, actforlibraries.org), 48 sentences.
  `ANSWER|UNCHECKABLE`, `UNCHECKED|pythagoras-p1`.
  Cross-host shared sentences: **0** (0 with punctuation stripped).
- Correct.

## Paraphrase adjudication (the key question)

**Question:** the frozen instrument corroborates only byte-identical normalized
sentences, so live pages that agree semantically but are phrased differently all
withhold (Newton's laws across Wikipedia/NASA/ThoughtCo, speed of light across
Wikipedia/Simple/Britannica). Is this a LEGITIMATE WITHHOLD or MISSING MACHINERY?

**Judgment: LEGITIMATE WITHHOLD. No fix proposed.** Reasons:

1. **The gate did not misfire.** The frozen rule requires ≥2 independent pages to
   corroborate a claim, operationalized since WG-1 as normalized byte-identical
   sentences. I proved exhaustively that **zero** byte-identical sentences exist
   across hosts in any of the 7 clusters — not just among the per-page
   best-overlap picks, but among *all* sentences on *all* pages, under the
   instrument's exact normalization, and again with punctuation stripped. There
   was nothing for the gate to catch. A gate that fires exactly per spec on
   evidence that genuinely lacks corroboration is not a bug.
2. **This is not the WG-1 wrong-sentence pattern.** WG-1's six guided failures
   came from max-keyword-overlap picking the wrong per-page representative while
   a corroborating sentence existed elsewhere on the page. Here no corroborating
   sentence exists anywhere, so even clustering all sentences (the WG-1 fix
   direction) would still withhold on all 7 clusters. The selection heuristic is
   exonerated on this evidence.
3. **Any fix that would install these claims weakens the ≥2-source rule.**
   Installing paraphrase-agreement requires a semantic similarity threshold —
   a new free parameter. Token-overlap thresholds are directly gameable:
   "water boils at 100c at sea level" vs "water boils at 40c at sea level" share
   most tokens; a paraphrasing sockpuppet pair (my red-team A2/A9 class) would
   sail through. The frozen law chose byte-identity precisely because it is not
   gameable by rephrasing. Loosening it trades the loop's core integrity for
   recall, which §4 forbids ("never bypass legitimate withholds").
4. **The WG-1 verdict documented the heuristic as a transfer bottleneck, not a
   refusal-loop bug.** It derived all 7 guided failures as safe withholds and
   closed with 0 false installs. A documented, as-designed limitation is not a
   genuine bug under the refusal-loop law (fix only misfiring gates).

Net: all 9 pilot refusals are correct withholds. The pilot's empty
`knowledge_ledger.txt` is the safe outcome, not a failure.

## Audit notes

- **Determinism:** `run_pass1` and `run_pass2` ledgers are byte-identical;
  every filed `verdict.out` is individually identical across passes
  (the aggregate-SHA difference in a naive `find|xargs sha256sum` was file
  ordering only). All 9 diagnoser replays byte-identical to filed outputs.
- **URLMISMATCH hardening (crew fix, verified):** `run_li.py` now treats the
  fetch-status URL as authoritative when it differs from the manifest URL and
  logs `%s|URLMISMATCH|%s|manifest=%s|snapshot=%s` with attribution. Verified:
  code path correct; 0 manifest/fetch-status URL mismatches in `corpus_snap/`
  and `corpus_snap_full/` (21 fetch-status lines checked); neither pilot log
  contains a URLMISMATCH line, i.e. the fix is live and inert-but-correct.
- **Glue patches intact:** the `H|host` emission (`host_of`) and `GATE|` capture
  in refusal reasons, added earlier for the source-independence work, are still
  present in `run_li.py` (lines ~27, ~232, ~263–266) and are behavior-preserving
  with the frozen binary (frozen `parse_pages` ignores `H|` lines; pilot
  verdicts confirm).
- **Injection scan:** fired on 0 pilot pages (none contained scan trigger words);
  integrity_violations=0.
