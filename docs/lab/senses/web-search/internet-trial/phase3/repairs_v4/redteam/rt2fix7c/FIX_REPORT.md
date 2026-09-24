# HELL-HOLE V4 r12_v4 Round 7c Fix Report

## Target
Fix RT2d A24 ("The coffee is cold." / "The coffee is not hot." — false affirm).
Attempt guarded A20 (equivocation) and A45 (pronoun ambiguity).

## Before / After (RT2d A)

| Item | t7 (before) | t8 (after) |
|------|-------------|------------|
| A20 (equivocation) | 1 endorse | 1 endorse (unchanged) |
| A24 (negated scalar) | 1 polarity/paraphrase | 0 neutral **FIXED** |
| A45 (pronoun ambiguity) | 1 polarity/paraphrase | 1 polarity/paraphrase (unchanged) |

RT2d A false affirms: 2 (A20, A45) — meets ≤2 target.

## A24 Fix (SHIPPED)
Root cause: three deny paths treated "not hot" as contradicting "cold":
1. `scan_text` neg-scope DENY (`ns!=cneg`) — vetoed when evidence contains
   negated gradable antonym of claim adjective (new `r7c_neg_grad_veto`).
2. `scan_text` antonym DENY — vetoed for negated gradable pairs.
3. `antonym_deny` (via `numeric_guard`) — skips gradable antonyms when the
   evidence adjective is preceded by a negation word.

New `gradable_antonym()` table: 30 scalar pairs (hot/cold, warm/cool,
tall/short, big/small, high/low, long/short, fast/slow, strong/weak,
expensive/cheap, etc.). Complementary antonyms (open/shut, alive/dead)
are NOT in the table — "not open" still correctly denies "open".

Also fixed: `r6_negclaim_rel` no longer affirms the opposite extreme from
negated scalar evidence.

## A20/A45 Guards (ATTEMPTED, REVERTED)
Built guarded suppress-affirm mechanisms:
- `r7c_equiv_one`: pivot word with distinct content premodifiers + claim
  overlapping both territories → suppress affirm (A20).
- `r7c_pronoun_one`: 2+ proper-name candidates + pronoun + claim matching
  exactly one → suppress affirm (A45).

Both fixed their targets (A20→neutral, A45→neutral) but overfired on
prior corpora:
- B35 ("box holds"/"bag holds") — fixed via premodifier-disambiguation check.
- CAU-B01/B02, V3-03 ("Ice floats... it...") — pronoun guard misfired on
  "Why"/"Ice" + "it".
- C33 ("restaurant is excellent/terrible") — equiv guard misfired.

Per brief: **both guards REVERTED**. Functions remain as dead code
(documentation of the attempt). 

**Comprehension ceiling**: A20 (equivocation across word senses) and A45
(pronoun anaphora resolution) require word-sense disambiguation and
anaphora machinery beyond the current classifier's lexical-overlap
architecture. The guards' territory/candidate heuristics cannot distinguish
true equivocation from normal word repetition without semantic understanding.

## Regression Verification (t7 vs t8 byte-diff)

| Corpus | Result |
|--------|--------|
| RT2 A/B, RT2b A/B, RT2c A/B | IDENTICAL (zero regressions) |
| RT2d A | Only A24 differs (fixed) |
| RT2d B | IDENTICAL |
| Frozen (b1, b2, cau, cmp, con, cond, hedge, neg, qnt, tmp) | IDENTICAL |
| Curated-18 | IDENTICAL |
| v3seed | IDENTICAL |
| reg382 (382 rows) | IDENTICAL (both stop at row 59, see below) |

## reg382 Long-Token Limitation
Both t7 and t8 panic ("slice index out of bounds") at row 59 (P2S-5-4)
due to a 70-byte URL token in the title field. Rows 1-58 output is
byte-identical between t7 and t8. Nine rows in the corpus contain
long URL tokens; this is a pre-existing limitation, not a regression.
A bounds check was added to `lower_copy` (truncation instead of panic
for that function), but other fixed-size buffers still panic on
extreme tokens. Full 382-row processing requires a systematic
buffer-audit (out of scope for 7c).

## Determinism
Three complete t8 runs on RT2d A: byte-identical.
SHA-256: `2d0e9f505d0a847460abd66c8a0bc7f875fe37af399b9a3e7118cd6eb6f86294`
(all three runs).

## Binary
`r12_v4_t8` SHA-256:
`87d903318e107c38087cc48e53eba1aaf2febea413bf3c38e875fed97caef4a7`

Built with pinned znc (`znc_linux_x86_64_abed8aa1`), pure Zag, zero RNG.
Source: `r12_v4_t8.zag`. Not committed per brief.

## Verdict
**SHIP**: A24 fixed, zero prior-corpus regressions, ≤2 false affirms on
RT2d A, byte-identical determinism confirmed. A20/A45 documented as
comprehension ceiling (reverted, not shipped).
