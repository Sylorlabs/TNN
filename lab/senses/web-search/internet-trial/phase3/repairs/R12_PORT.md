# R12 Port Report — HELL-HOLE V3, pure-Zag R1/R2 (`src/r12.zag`)

Date: 2026-09-22. Author: subagent (differential port of `tools/proto_r12.py`).

## What was delivered

`src/r12.zag` — a complete, pure-Zag port of `tools/proto_r12.py` (R1 AFFIRM
endorsement semantics + R2 UTF-8 negation semantics), including the exact
lexicon tables (STOP, VERB_STEMS, REPORTING, NEG_TOKENS, STRONG_DENY,
WEAK_DENY, SUPERLATIVE, CONJ_SKIP, WH_AUX, FILLER, synonym map, antonym map,
denial-prefix list), the tokenizer, the stemmer, the clause splitter, and the
full `classify()` decision procedure (gate → DENY-lex → antonym → neg-scope →
competing-subject → AFFIRM → neutral).

The file is a single self-contained Zag source with a TSV driver:
`r12 <input.tsv>` reads `id<TAB>claim<TAB>title<TAB>snippet` rows and prints
`id tag reason` per row (tag 0/1/2, reason
gate|deny-lex|antonym|neg-scope|competing-subject|endorse|neutral).
Deterministic, zero RNG. No phase-2 sources and no `tools/proto_r12.py` were
modified. Nothing was committed.

## Port method (exact)

1. Transcribed every lexicon from the prototype byte-for-byte (verified by
   dumping sorted lexicons from Python and diffing against the Zag blobs via
   generated `lex_*` matchers — all match).
2. Ported, in order: UTF-8 helpers → tokenizer (regex
   `[A-Za-z0-9\u2019']+(?:-[...]+)*` as a byte scanner) → stemmer
   (`proto_r12.stem`, incl. the VERB_STEMS verb-form fallback) → clause
   splitter (digit-dot protection + `[.!?;\u2014]+` split, unstripped parts,
   blank-part drop) → claim representation (content words, leading-gerund
   strip, anchors, predicate + copula/have fallback, synonym expansion) →
   clause scanner (DENY a/b/c/d, AFFIRM, interrogative, reporting-frame,
   competitor, claim-value guard) → whole-text overlap gate → driver.
3. Toolchain constraints honored (per workspace AGENTS.md): `_zag_arg(1)` read
   unconditionally (argc is untrustworthy, ZNC-2026-09-21-007); no
   `as []i32` casts (ZNC-2026-09-21-007 aliasing bug) — all tables are `[]u8`
   arenas with explicit little-endian accessors; raw UTF-8 bytes in literals
   (`\u2019` does not decode); flat early-return control flow (no 5-deep
   else nesting, ZNC-2026-09-21-013); `z_alloc`/`z_free` naming.

## Differential testing

Oracle: `tools/proto_r12.py` (`classify()`), frozen at
`b676e9ba32246944849c9c605ea3d77cd1df01d425ccda031ad68ec519d43727`.

Evidence actually present on disk (counted 2026-09-22):
- `course_input_solo.tsv`: **168 rows**
- `course_input_helper.tsv`: **196 rows**
- combined: **364 rows** (the task text's "348" does not match the physical
  files; all 364 physical rows were tested — nothing omitted)
- `frozen_stances.tsv`: 364 rows
- +18 curated tests extracted from the prototype's `__main__` block
  (each asserted to pass under the oracle before use)
- **382 classification cases total**, compared on tag AND reason.

Unit-level differential suites (generated from the oracle):
- stemmer: **2617/2617** unique corpus tokens byte-identical
- tokenizer: **401/401** unique corpus texts byte-identical
- clause splitter: **401/401** unique corpus texts byte-identical
- 16 extra synthetic edge cases (trailing-comma numbers, curly-apostrophe
  negation, "no longer"/"no evidence", anaphoric denial, antonym both
  directions, interrogative/reporting-frame blocks, competitor + claim-value
  guard, decimal protection, hyphenation, em-dash split, empty title/snippet):
  **16/16** agree.

### Bugs found and fixed during porting (all caught by the differential tests)

1. `z_toks` consumed only one character per token (inner hyphen loop broke
   after the first char) — every token was 1 char. Caught by tokenizer
   unit tests.
2. `z_clauses` stripped each clause; the prototype keeps original spacing and
   only drops blank parts (matters for `startswith("legend:")`). Fixed to keep
   unstripped clauses.
3. `z_clauses` reused a scratch `prot[]` buffer across calls without clearing
   it — stale decimal-protection flags from earlier texts suppressed real
   clause splits. The prototype rebuilds the protected string per call.
   Fixed by zeroing the range on entry. (This one also corrupted full
   classification, not just the unit test.)
4. Claim-number extraction initially required length ≥ 2 and stripped
   trailing commas; the prototype's `\d[\d,]*` has no such filter
   (e.g. claim "1," yields number "1"). Fixed to mirror the regex exactly.

Initial full-suite diff: 18/18 curated rows mismatched (root causes 1+3, plus
a harness idx-collision bug that has since been fixed — see below).
After fixes: **382/382 zero-diff, tag and reason.**

### Determinism

Two consecutive runs over all 382 inputs: byte-identical output.
SHA-256 of both runs: `80c29475748d613dbb5bf94c98a38042d579f9ea5b073279f05b242734faab9d`.

## Hashes (SHA-256, 2026-09-22)

| artifact | sha256 |
|---|---|
| `src/r12.zag` (deliverable) | `a867c3be7cf44126db61d7ba69421a4ddad3819e19d4e5485b4c5dfaa0543080` |
| `tools/proto_r12.py` (oracle) | `b676e9ba32246944849c9c605ea3d77cd1df01d425ccda031ad68ec519d43727` |
| `evidence/course_input_solo.tsv` | `9f24a91e485033971c4a3d82bd964eac559909287f12cf80de2f79baccddfccf` |
| `evidence/course_input_helper.tsv` | `15aa045dcd952741a2af12b2899abd0ab339c7c010fc8e2dff0c799088c124c0` |
| `evidence/candidates.tsv` | `e37e3164d22db8eb69f915f5c3504dbd494138b35c85652c458fcdf1b7d5e550` |
| oracle expected output (382 rows) | `e49615d30d288434a3e033a42d5c08ad1912fa9c357cc04da1bcd6752017b575` |
| Zag output run 1 = run 2 | `80c29475748d613dbb5bf94c98a38042d579f9ea5b073279f05b242734faab9d` |

Scratch copy of the source hashes identically to the repo deliverable.
Build command (pinned toolchain, no cache):
`znc_linux_x86_64_abed8aa1 r12.zag --no-zagd --no-analyze --no-foreground-cache -o r12`

## Notes and honest qualifications

- **frozen_stances.tsv is not the oracle.** It is the phase-2 calibration
  target (labels from the old phase-2 classifier, per
  `tools/gen_input.py`). The current R1/R2 prototype itself disagrees with it
  on 191/364 rows — expected, since R1/R2 are repairs that deliberately
  re-score stances. Differential testing was therefore done oracle-vs-port,
  not stances-vs-port.
- **Row-count discrepancy:** the task text says 348 frozen evidence rows;
  the physical TSVs contain 168 + 196 = 364. All 364 were tested.
- **Harness bug (mine, fixed):** the first test-input build keyed rows by
  `(candidate, result_idx)`, which collides across queries (39 duplicate
  keys). Rebuilt with unique sequential ids plus a `keymap.tsv` recording
  `(arm, candidate, query, result)` per row.
- **Driver shape:** the prototype's executable surface is its `__main__`
  test block; the Zag deliverable exposes the same `classify` semantics
  behind a TSV-file driver (`id/claim/title/snippet` → `id tag reason`).
  This is a harness difference, not a semantic one — every semantic path is
  covered by the 382-case differential suite.
- **Scope kept:** the port covers exactly what `proto_r12.py` implements
  (R1 + R2). R3–R6 live in their own files and were not touched.
- **No semantic compromise.** The final port reproduces the prototype on
  all 382 cases including tag *and* reason strings, with byte-identical
  reruns. The four bugs above were found by the differential tests and
  fixed; the final state has zero known divergences.

## Repo hygiene

`src/` contains only the five `.zag` sources. No binaries, no `.zagd` /
`.zag-cache` files were left in the repo tree (stale toolchain caches from
earlier compiles were removed). All build and test artifacts live in
`~/workspace/r12work/` (scratch, outside the repo).
