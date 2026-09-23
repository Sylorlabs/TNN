# A1 (NEGATION HUNTER) — Mistag Report

Crew: A1 · Campaign: hell-hole V4 · Date: 2026-09-23
Target: frozen stance classifier `/home/hatch/workspace/scratch-hellhole/hellhole/r12_v3`
(no fixes attempted — analysis only)

## Method (oracle-first ordering)

1. Read `r12_v3.zag` end-to-end to understand the negation machinery before
   writing any fixture.
2. Hand-authored all 52 rows of `corpus_neg.tsv` and assigned the
   `oracle_tag` column (col 5) **solely from my own reading of
   (claim, title, snippet)**. The classifier binary was not executed until
   the corpus file was complete.
3. Projected cols 1–4 to `corpus_neg_input.tsv`, ran the binary 3×,
   confirmed byte-identical output, then scored mechanically against the
   frozen oracles.
4. **One fixture refinement after the first run (documented, not hidden):**
   NEG-01's first snippet was "Contrary to the myth, bats are NOT blind."
   It tagged DENY — but via the deny-lexicon path (`contrary` ∈
   `lex_strong`), not via negation handling, so it did not test the reported
   "bats are NOT blind" → AFFIRM failure. The snippet was replaced with
   "Field studies show bats are NOT blind." to isolate the negation
   structure. **The oracle tag (DENY) was not changed** — it was fixed from
   my original reading and is identical before/after. Corpus re-frozen
   (new SHA below), all 3 runs re-done, re-scored.

## Freeze

- `corpus_neg.tsv` SHA-256:
  `85a84ed3a361f5d807e4b3ccb7baaa3538efaa5091820899518f4a8dd85154c0`
- Classifier output (`run1.txt` = `run2.txt` = `run3.txt`, `cmp`-verified
  byte-identical across 3 runs) SHA-256:
  `2158ddc7c9ba1886c43285a94aa88d1d2cd3a2bc9bc4537fde5e45f5a320e579`
- Corpus: 52 rows. Oracle distribution: 40 DENY / 9 AFFIRM / 3 NEUTRAL.
- All 3 required seed rows present: NEG-01 (bats NOT blind → DENY),
  NEG-29 (No clinical evidence… celery juice → DENY),
  NEG-23 (Coffee doesn't cause cancer → DENY).

## Per-subtype accuracy

| Subtype | Rows | Correct | Acc | Mistags |
|---|---|---|---|---|
| NOT (explicit "not") | 6 | 3 | 50.0% | NEG-01, NEG-02, NEG-04 |
| NEVER | 4 | 2 | 50.0% | NEG-08, NEG-09 |
| NO | 5 | 2 | 40.0% | NEG-12, NEG-13, NEG-14 |
| NONE | 3 | 0 | 0.0% | NEG-16, NEG-17, NEG-18 |
| NEITHER_NOR | 4 | 2 | 50.0% | NEG-20, NEG-21 |
| NT_ASCII (n't) | 3 | 2 | 66.7% | NEG-24 |
| NT_CURLY (n’t U+2019) | 3 | 1 | 33.3% | NEG-27, NEG-28 |
| NO_EVIDENCE / NO_LONGER | 5 | 2 | 40.0% | NEG-29, NEG-30, NEG-32 |
| DOUBLE_NEG | 5 | 1 | 20.0% | NEG-34, NEG-35, NEG-37, NEG-38 |
| OUTSIDE_SCOPE | 3 | 1 | 33.3% | NEG-39, NEG-40 |
| NOT_X_BUT_Y contrast | 4 | 0 | 0.0% | NEG-42, NEG-43, NEG-44, NEG-45 |
| NEG_REPORTING verbs | 7 | 2 | 28.6% | NEG-46, NEG-47, NEG-48, NEG-49, NEG-52 |
| **TOTAL** | **52** | **18** | **34.6%** | **34** |

Mistag reasons: 24× `endorse` (false AFFIRM), 6× `neg-scope` (false DENY),
1× `deny-lex` (false DENY), 3× `neutral` (missed DENY).

## Full mistag list (idx, oracle → got, reason)

| idx | subtype | oracle | got | reason |
|---|---|---|---|---|
| NEG-01 | NOT | 2 | 1 | endorse |
| NEG-02 | NOT | 2 | 1 | endorse |
| NEG-04 | NOT | 2 | 1 | endorse |
| NEG-08 | NEVER | 2 | 1 | endorse |
| NEG-09 | NEVER | 0 | 2 | neg-scope |
| NEG-12 | NO | 2 | 1 | endorse |
| NEG-13 | NO | 2 | 1 | endorse |
| NEG-14 | NO | 1 | 2 | neg-scope |
| NEG-16 | NONE | 2 | 0 | neutral |
| NEG-17 | NONE | 2 | 0 | neutral |
| NEG-18 | NONE | 2 | 0 | neutral |
| NEG-20 | NEITHER_NOR | 2 | 1 | endorse |
| NEG-21 | NEITHER_NOR | 2 | 1 | endorse |
| NEG-24 | NT_ASCII | 2 | 1 | endorse |
| NEG-27 | NT_CURLY | 2 | 1 | endorse |
| NEG-28 | NT_CURLY | 0 | 1 | endorse |
| NEG-29 | NO_EVID_LONGER | 2 | 1 | endorse |
| NEG-30 | NO_EVID_LONGER | 2 | 1 | endorse |
| NEG-32 | NO_EVID_LONGER | 1 | 2 | deny-lex |
| NEG-34 | DOUBLE_NEG | 2 | 1 | endorse |
| NEG-35 | DOUBLE_NEG | 2 | 1 | endorse |
| NEG-37 | DOUBLE_NEG | 2 | 1 | endorse |
| NEG-38 | DOUBLE_NEG | 1 | 2 | neg-scope |
| NEG-39 | OUTSIDE_SCOPE | 1 | 2 | neg-scope |
| NEG-40 | OUTSIDE_SCOPE | 2 | 1 | endorse |
| NEG-42 | NOT_X_BUT_Y | 1 | 2 | neg-scope |
| NEG-43 | NOT_X_BUT_Y | 2 | 1 | endorse |
| NEG-44 | NOT_X_BUT_Y | 2 | 1 | endorse |
| NEG-45 | NOT_X_BUT_Y | 1 | 2 | neg-scope |
| NEG-46 | NEG_REPORTING | 2 | 1 | endorse |
| NEG-47 | NEG_REPORTING | 2 | 1 | endorse |
| NEG-48 | NEG_REPORTING | 2 | 1 | endorse |
| NEG-49 | NEG_REPORTING | 2 | 1 | endorse |
| NEG-52 | NEG_REPORTING | 2 | 1 | endorse |

Correct rows (18): NEG-03, NEG-05, NEG-06, NEG-07, NEG-10, NEG-11, NEG-15,
NEG-19, NEG-22, NEG-23, NEG-25, NEG-26, NEG-31, NEG-33, NEG-36, NEG-41,
NEG-50, NEG-51.

## Diagnosis per subtype

Mechanism references are to `r12_v3.zag`.

### 1. neg_scope's 4-token BEFORE-only window (dominant failure)

`fn neg_scope` scans tokens `pi-4 .. pi-1` only — never after the predicate,
never farther than 4 back. Two systematic consequences:

- **Post-predicate negation is invisible.** "bats are NOT blind"
  (NEG-01), "bats are not blind" (NEG-02): pred resolves to "be" via the
  "are" fallback; "not" sits AFTER pi → `ns=0` → AFFIRM by overlap+anchor.
  Same for "causes neither cancer nor heart disease" (NEG-21) and the
  double negations "is not ineffective" / "is not unpopular" /
  "is not uncommon" (NEG-34/35/37), where "not" follows the copula.
- **Distant negation is invisible.** "Not a single study has shown that
  coffee causes cancer" (NEG-04), "never, in any of the published trials,
  cures" (NEG-08), "no plausible mechanism by which" (NEG-12), "No credible
  scientist believes" (NEG-13), "Neither researchers in Europe nor those in
  Asia found that" (NEG-20), "didn't, after reviewing all the data,
  conclude that" (NEG-24 ASCII, NEG-27 curly): the marker is 5+ tokens
  before pi → `ns=0` → AFFIRM.

In all these rows the AFFIRM branch then fires on topic overlap alone
(`nclm>=need`, anchor present, `ns==0`): the R1 "no fallthrough to AFFIRM"
still falls through to AFFIRM whenever the words overlap.

### 2. neg_scope is proximity, not proposition scope (false DENYs)

When a marker IS inside the window, it fires regardless of what it scopes:

- NEG-09 (NEUTRAL→DENY): "Coffee never causes jitters, but whether it
  causes cancer is unknown." `pi` is the FIRST "cause" token — the one
  scoping "jitters". No argument-structure check; `nclm` counts claim stems
  anywhere in the clause.
- NEG-14 (AFFIRM→DENY): "No treatment cures disease faster." The "no" is a
  comparative ("no X-er" = superlative), not a predicate negation — but it
  is a bare `lex_neg` token inside the window.
- NEG-38 (AFFIRM→DENY): "never fails to prevent" — double negation the
  window reads as single negation.
- NEG-39 (AFFIRM→DENY): "not only prevents" — "not" is part of the additive
  "not only … but also" construction; the window cannot see the idiom.
- NEG-42/NEG-45 (AFFIRM→DENY): "Not coffee but tea causes cancer" — the
  "not" scopes the contrasted SUBJECT, not the predicate.

### 3. "not X but Y" contrast: 0/4, window-edge lottery

The contrastive "not" is either inside the window (false DENY on AFFIRM
oracles: NEG-42, NEG-45) or exactly one token outside it (NEG-43: "It is
**not** coffee but tea that causes cancer" — "not" is 5 tokens before pi →
missed → false AFFIRM; NEG-44 same shape). There is no model of
contrastive focus; correctness is decided by token distance.

### 4. Negated reporting verbs: lexicon holes (5/7 mistag)

DENY(a) needs a `lex_strong` stem or a `deny_prefix` stem
(debunk/disprov/refut/incorrect/wrong/myth/hoax/fals). The stems actually
produced miss it:
"denies"→"deny", "rejected"→"reject", "disputes"→"disput",
"contradicts"→"contradict", "denied"→"denie" (the -ed branch appends "e"
after a vowel → "denie", missing the listed "denied"). None are in
`lex_strong`; none match the prefixes. Only "refutes"→"refut" (NEG-50) and
the literal "false" (NEG-51) fire. **Dead entry:** `lex_strong` lists
"denies", but the stemmer maps "denies"→"deny", so that entry can never
match a stemmed token.

### 5. "none": lexicon + predicate-detection double fault (0/3)

"none" ∈ `lex_neg` but ∉ `lex_strong`/`lex_weak`, and DENY(a) never consults
`lex_neg`. Worse, for NEG-16/17 the claim verb "showed" stems to "show",
which is in `lex_reporting` → skipped as predicate → fallback finds no
be/have auxiliary → `pred=""` → `pi=-1` → every predicate rule is dead →
NEUTRAL. NEG-18 ("The benefits were none to speak of") likewise has no
"show" token → NEUTRAL. A negation the lexicon knows about is unreachable
from both deny paths.

### 6. "no evidence" / "no longer": substring rules, no scope

- The weak-deny trigger is the literal substring "no evidence": inserting
  one adjective defeats it — "No **clinical** evidence supports the claim
  that celery juice cures" (NEG-29), "no **good** evidence" (NEG-30) →
  AFFIRM. (Exact "no evidence", NEG-31, works.)
- "no longer" is polarity-blind: NEG-32 "The policy is no longer suspended
  and remains active" (oracle AFFIRM — "no longer suspended" = active)
  fires weak-deny + `nclm>=2` → false DENY. The rule negates the clause;
  here the negated word is the claim's opposite.

### 7. Curly n’t works; distance doesn't (NT_CURLY 1/3)

The U+2019 branch in `neg_scope` is correct: "doesn’t" adjacent to the
predicate (NEG-26) → DENY. It fails only via the same distance fault as
ASCII (NEG-27). NEG-28 is a clause-splitting interaction: the em dash in
"The treatment cures disease — or doesn’t it?" splits off the hedge into
clause 2; clause 1 endorses (AFFIRM) and the per-clause interrogative check
never sees the "?" in clause 2 → NEUTRAL oracle mistagged AFFIRM.

### 8. Outside predicate scope (1/3)

- NEG-39 "not only … but also" → false DENY (see §2).
- NEG-40 "It is **hardly** the case that the treatment cures disease":
  "hardly" ∈ `lex_neg` but sits 6 tokens before pi (matrix-clause negation)
  → missed → false AFFIRM. The window cannot reach matrix-level negation.
- NEG-41 ("It is not the case that critics, but scientists, confirm the
  theory") passes only because the window happens to miss the matrix "not".

### 9. What passes, and why (coverage note)

Adjacent-before markers work: "does not cause" (NEG-03), "It is not true
that" (NEG-05), "never causes" (NEG-07/10), "No doctor says" (NEG-11),
"Neither/Nor does" (NEG-19/22), "doesn't" (NEG-23/25), "doesn’t" (NEG-26),
exact "no evidence" (NEG-31), "no longer" on DENY oracles (NEG-33),
"refutes"/"false" (NEG-50/51), separate-clause "not" (NEG-06), unrelated
"no" with no predicate match (NEG-15), "not uncommon" (NEG-36 — passes via
subject+copula endorsement with `need=1`, for the wrong reason: the "un-"
morphology is unmodeled).

## Files

- Corpus (frozen, oracle-first):
  `/home/hatch/workspace/scratch-hellhole/crews/a1/corpus_neg.tsv`
- Classifier input projection (cols 1–4):
  `/home/hatch/workspace/scratch-hellhole/crews/a1/corpus_neg_input.tsv`
- This report:
  `/home/hatch/workspace/scratch-hellhole/crews/a1/MISTAG_REPORT.md`
- Byte-identical run outputs:
  `/home/hatch/workspace/scratch-hellhole/crews/a1/run1.txt`
  (`run2.txt`, `run3.txt` identical, SHA above)

## Bottom line for the parent

The frozen classifier gets **18/52 (34.6%)** on a negation-focused corpus
(oracle mix 40 DENY / 9 AFFIRM / 3 NEUTRAL). The R2 negation machinery fails
in four structural ways, none fixable by lexicon tweaks alone: (1) the
4-token **before-only** scope window misses post-predicate negation
("bats are NOT blind" → AFFIRM, reproducing the v3 trial failure) and
distant negation; (2) the window is proximity-based, so it **false-fires**
on "not only", "never fails to", "not X but Y", comparatives ("no …
faster"), and negation scoping a different proposition; (3) the deny
lexicon misses the actual stems of "denies/denied/rejected/disputes/
contradicts" (and lists an unreachable "denies"); (4) predicate detection
dies when the claim verb is in `lex_reporting` ("showed") or absent
("were none"), stranding even known markers like "none". No commits made;
no code touched.
