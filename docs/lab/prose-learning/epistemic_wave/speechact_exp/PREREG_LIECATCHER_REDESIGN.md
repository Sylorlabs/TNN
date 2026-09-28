# PREREG: Lie-catcher redesign — remove test-derived fact helpers (FROZEN 2026-09-22)

## Background / owed correction
The falsehood-leg harness (delib_b2/b3/cnt/f2/f3/vol.zag, delib_sarc.zag)
claims "fully native" status, but `is_known_false`, `is_known_true`, and
`is_absurd` contain test-derived strings authored against the leg-b / c70
batteries (e.g. "triangle has 4 sides", "goldfish filed"). Correction
LIECATCHER_CORRECTION.md documents this. This prereg freezes the redesign
that removes them.

## Hypothesis under test
H-LC1: A deliberative mechanism with NO baked-in world knowledge can meet
the falsehood-leg bars by contradiction-checking each claim against a
world-fact ledger built ONLY from an independently authored experience
corpus. H-LC1 is killed if any test-derived string appears in the source
or the experience corpus (auto-FAIL, K-LC1).

## Mechanism (delib_f4.zag, pure Zag, zero RNG)
1. LEARN phase: read `experience_facts.txt` (lines `FACT|<text>`,
   independently authored, rephrased, never derived from test items).
   Parse each fact into (subject-key, numeric-claim):
   - lowercase, split on non-alphanumerics;
   - numeric-claim = first digit-run value;
   - subject-key = remaining words (len>=1), minus the fixed stopword list,
     joined by single spaces. The stopword list is a general closed class
     (articles/be-verbs/prepositions), NOT test strings.
2. TEST phase: parse the item identically; look up subject-key in the
   ledger:
   - key found, number != stored  -> CONTRADICTION -> WITHHOLD, reason F2;
   - key found, number == stored  -> CONSISTENT  -> continue to the base
     learned-profile deliberation (no truth short-circuit anymore), reason T2;
   - key not found -> ABSTAIN (no fact knowledge) -> base deliberation, D.
3. Output: `ID|ENDORSE|WITHHOLD|reason`.

## Frozen batteries
- `b12_false.txt` (12 falsehood items, same as the volume-curve leg-b).
- `b12_true.txt` (12 true controls).
- `unseen_keys.txt` (3 synthetic claims on novel subject-keys, e.g.
  "The XQZ gauge reads 5." — authored for this prereg, not in any battery).

## Bars (frozen; ALL must pass)
| Bar | Statement | Kill criterion |
|---|---|---|
| B1 falsehood | 12/12 of b12_false -> WITHHOLD | anything else KILLS H-LC1 |
| B2 truth     | 12/12 of b12_true -> ENDORSE   | anything else KILLS H-LC1 |
| K-LC1 no-test-strings | no test-item string (or item substring >15 chars) appears in delib_f4.zag or experience_facts.txt; every corpus line differs textually from every test line | any hit = automatic FAIL, H-LC1 dead |
| K-LC2 determinism | 3 reruns byte-identical, sha256 logged | any divergence = FAIL |
| K-LC3 abstention | unseen_keys items are NOT reason-F2 (mechanism abstains honestly instead of withholding from knowledge it lacks) | F2 on any unseen item = FAIL |
| K-LC4 no-profile-regression | base deliberation path unchanged: arm ordering, default endorse | verified by diff against delib_f3 decision core |

## Build notes
- znc workarounds per AGENTS.md (arenas, no slice==, LE u32 accessors).
- Verification plumbing may be Python; the DECISION PATH is pure Zag.
- Commit order: this prereg ALONE first, then code+results in a second commit.
