# Integration Report — hell-hole r12_v4 (B1+B2+B3+B4)

Date: 2026-09-23. Frozen input: `hellhole/r12_v3.zag`. Output: `crews/integ/r12_v4.zag`
(121 functions, no duplicate definitions, balanced braces). Built with pinned
`znc_linux_x86_64_abed8aa1 --no-zagd`; pure Zag, zero RNG/time/network
(grep-clean; only file read/write syscalls). Analyzer: 3 warnings, all inherited
from source patterns. **No commit** (per instructions).

## Architecture (final)

- **B4 as spine**: `tag*16+reason` encoding; reason 7 temporal, 8 comparative,
  9 quantifier, 10 numeric-mismatch. Scratch `[100000,101000)`; claim/evidence
  tables, `SUBJA`, `neg_scope` ported. B4's `classify` + pipeline + main kept.
- **B1 negation**: `neg_scope` + `veto_idiom` + `matrix_deny` + lexicons merged in;
  B1's DENY(a–f) rule order preserved. `find_word` fixed to `tok_is`-based
  whole-word matching; `scan_text` hardened with reporting-verb exemption
  (`say/said/says/told/state/stated/claims/claimed/claim/according` no longer
  count as hedges — this was suppressing B1's DENY in reporting frames).
- **B3 causal**: `has_cexp`, `non-claim-subject` guard in `veto_idiom`,
  polarity-aware DENY rule (`ns!=cneg`), `competitor` guard, `causal` helpers,
  lexical-cause DENY, B3's `nummis` guard with B4 `reason=10`.
- **B2 contrastive**: B2's `SUBJA`; numeric guard runs **after** text DENYs,
  **before** AFFIRM — fixes the B2 bug where numerals vetoed genuine textual
  DENY (A2 C24–C26, C37, C39: now DENY).
- **V4-INTEG fixes** (cross-family, found during integration):
  1. `whedge`: B1's blanket "whether"-suppresses-AFFIRM broke B4's C12
     ("whether you smoke or not" concessive). Rewrote with concessive
     "whether X or not" exemption via `tok_is` (first attempt had a `tmpS`
     overwrite bug — caught by C12, fixed).
  2. Copula-complement "not X but Y": B1's `neg_scope` DENYed C40
     ("The meeting is not at eleven but at noon." vs "The meeting is at noon.");
     B2/oracle say AFFIRM. Added veto: if the claim complement (`cadj`)
     appears after "but", it's a correction that affirms → return 0.
- Scratch map: B1/B2/B3 extras occupy `[97928,99976)`, below B4's conditional
  scratch at 100000+. No overlap verified.

## Verified results (2026-09-23, binary `r12_v4`)

| Battery | Score | Notes |
|---|---|---|
| A1 negation | **52/52** | |
| A2 contrastive | **27/50** | handoff baseline 13/50; B2's own binary scores 22/50 on this corpus; V4 loses none of B2's wins except C40, which V4 now also gets right (fix #2 above). 5 new wins: C24–C26, C37, C39 (numeric-guard reorder). |
| A3 causal | **51/51** | |
| A4 conditional | **12/13** | miss = C8, B4's documented sole conditional miss |
| A4 hedge / quantifier / temporal | **12/12 each** | |
| A4 comparative | **10/10** | |
| Real seeds | V3-03 **6/8** AFFIRM; V3-05-q0-r2 DENY; V3-07-q0-r2 DENY; negation seeds **3/3** DENY | |
| REG382 | **17 full-line diffs / 13 tag flips** | exact union of crew diffs: B1 8 (7 flips + 1 reason), B3 7 (4 flips + 3 reason), B4 2 (2 flips), B2 0. Zero interaction diffs. |
| Curated rows 365–382 | **2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1 — exact** | |
| Determinism | 3 full-battery runs byte-identical | output SHA-256 `67324bde…96ac0` |

## REG382 tag-flip justification (each individually verified)

**B4 (2 flips, hedge rule):** P2S-5-2, P2H-5-2 ("COVID lab leak" / "New evidence
*suggests*…"): "suggests" ∈ lex_hedge → hedged endorsement → neutral. Was false
endorse of a hedged proposition.

**B3 (4 flips, polarity rule):** P2S-18-2, P2S-18-4, P2H-18-2, P2H-18-4
("Lightning *never* strikes…" vs evidence affirming strikes): claim-negative,
evidence-positive → polarity clash → DENY. Was false endorse.

**B1 (7 flips):**
- P2S-8-1, P2S-8-2, P2H-8-1 ("The Earth is flat." vs quora "Related: what
  evidence is there that Earth is flat?"): bare related-link snippet, no
  endorsement content → neutral. Was false endorse.
- P2S-8-4, P2H-8-4 (vs "…the Bible *nowhere* states categorical…"): B1's
  `neg_scope` catches "nowhere"-scoped denial → DENY. Was false endorse.
- P2H-8-0 (vs "Although scientific evidence says the Earth is a *sphere*…"):
  mixed evidence (believers claim flat / science says sphere) → neutral.
  Was false endorse.
- P2H-15-96 ("Chocolate cures insomnia" vs "No credible study shows…"):
  B1's "no + evid-word" generalization → DENY. Was false endorse; clearly correct.

Reason-only changes (tag stays DENY): P2S-18-0, P2H-18-0, P2H-18-5
(deny-lex → neg-scope); P2H-8-96 (competing-subject → neg-scope).

## Reproducibility

- `merge1.py` (extract + surgical patches) → `merge3.py` (B4 classifier edits) →
  `merge2.py` (final assembly) → `znc --no-zagd r12_v4.zag -o r12_v4`.
- Source SHA-256: `1e7700df8550391649e2e94d5afe187304eed9964325d1fed9ef49188ea81a37`
- Binary SHA-256: `84be4b81a63834007f1a12bbaa9ce1fa0378725347c785f28a065376d384bc9b`
- `score1.py` reproduces the hunter-corpus table above.

## Open / recommended follow-ups

- A2 remains 27/50: remaining misses (C04–C08, C09, C16–C21) are B2-family
  weaknesses, out of scope for this integration; no V4 regression vs B2.
- A4 C8 stays neutral (B4's known miss); C12 fixed by the whedge exemption.
- B1's REG382 note of "8 diffs" was confirmed against B1's own binary
  (earlier ID-keyed comparison was confounded by duplicate row IDs in
  reg382_input.tsv; line-order comparison is authoritative).
