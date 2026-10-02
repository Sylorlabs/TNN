# WS2-C preliminary findings — TNN deliberative retrieval (2026-09-24)

## Verdict: FAIL (11/12 on the sealed holdout bar)

The preregistered bar was 100% recall on 12 sealed astronomy holdout probes
(H01–H12), unseen during deliberation. The scheme TNN chose passes 11/12.
Per the prereg, that is a FAIL, with per-miss diagnosis below. The failure is
a genuine generalization miss, not a harness bug, and the diagnosis points at
a concrete mechanism gap.

## What TNN did (its deliberation, in its audit's words)

TNN's engine (`delib.zag`, pure Zag, zero RNG) read the failure evidence
(43 prior-arm miss lines, 8 white-box fail records), then ran 5 rounds of
observe → hypothesize → predict → test → adopt/reject over a 4-parameter
mechanism palette (hint handling × scoring × abstention × expansion):

- **Round 1** (STRICT,COUNT,NEVER,NONE): 30 misses. Tried M_AB1 (abstain on
  all-zero scores) to fix 17 F_ABSTAIN misses. Trial: 30→26 but **2
  regressions** — abstention empties probes whose gold has no text evidence
  but was passing via top-k. **Rejected.** (It discovered the abstention /
  zero-evidence-recall trade-off by itself.)
- **Round 2**: Tried M_HM1 (VERIFY hints against text evidence) for 7
  F_HINT_EXCLUDE misses. Trial: 30→17, zero regressions. **Adopted**, even
  though its prediction ("all 7 go to 0") was violated (3 remained) — the
  adoption rule is miss-reduction with no regressions, and the violation is
  recorded honestly in the audit.
- **Round 3**: Tried M_HM2 (SOFT hints to +10 bonuses) for the 3 remaining
  hint-exclusion misses. Trial: 17→19 with 2 regressions — bonuses outrank
  weak text evidence (the Q41 QUOTE-bonus case). **Rejected.**
- **Round 4**: Tried M_EX1 (CLUSTER completion) for 4 F_CLUSTER misses.
  Trial: 17→17, no improvement — completion is undone by score-ordered
  re-truncation to K. **Rejected.**
- **Round 5**: No improving move remains. Stopped.

**Final scheme: (VERIFY, COUNT, NEVER, NONE)** — verify each hint against
text evidence (drop only if contradicted), raw occurrence-count scoring, no
abstention, no expansion. Full audit: `ws2c_r1/out/audit.md`.

P-AGE symmetry held every round (aged 0/5 vs recent 0/5 misses) — no
install-order bias in the mechanism.

## Visible-evidence scores (99 probes: 51 WS2-A + 48 MORG design)

| class | misses | note |
|---|---|---|
| P-AGE (10) | 0 | |
| P-COLL (11) | 0 | |
| P-CTX (18) | 0 | all X1/X2/X3 pass under VERIFY |
| P-PARA (6) | 4 (QP03–QP06) | zero exact-token overlap; unfixable by any token scheme |
| P-NEG (6) | 6 | abstention rejected (see round 1); scheme cannot say "not found" |
| MORG PURE/SUBJ/AMBIG (48) | 7 | Q39, Q40, Q45, Q46 (cluster), Q42, Q44, Q48 (hint) |

## Per-miss diagnosis: H07 (the holdout failure)

`H07|test|SUBJ|sh=telescope|text="everything about telescopes"|gold=AS21–AS30`
(10 telescope-procedure items; texts use "telescope" singular).

1. Query tokens: {everything, about, telescopes}.
2. Gold items' vocabulary: "telescope" (singular, in subject + texts). The
   plural "telescopes" has **zero exact-token overlap** — a morphological
   variant, the mildest form of the P-PARA gap.
3. VERIFY checks the subject hint: max text-score over subject-"telescope"
   items (AS21–AS30) is 0 → the **correct hint is dropped**. VERIFY cannot
   distinguish "hint contradicted by text" (Q41: QUOTE items score 0 on
   "loops", hint wrong) from "hint unverifiable due to vocabulary mismatch"
   (H07: hint right, but pluralization defeats exact matching). The
   verification step is fooled the same way stopwords fool it in reverse
   (Q42/Q48: a wrong hint survives because "the"/"code" give nonzero score).
4. With the hint dropped, pure text scoring retrieves non-gold items sharing
   stopwords/content tokens; all 10 gold items score 0 and lose the id
   tie-break for the remaining top-20 slots → F_UNCLASSIFIED.

No palette scheme fixes this: STRICT passes H07 (hint kept → gold are the
only candidates) but fails 7 visible misleading-hint probes and the holdout
H10; SOFT passes H07 but visibly regresses Q41. The miss is a **mechanism
ceiling**, not a search failure — exact-token matching needs morphological
normalization (or a verify rule that doesn't drop hints when the query
vocabulary is entirely absent from the hint set).

## Red teams

- **R1 (wrong-hint swaps, 12 probes)**: 8/12 miss, all F_HINT_EXCLUDE except
  H07 (same morphological miss). Graceful degradation, no crash; the
  classifier correctly attributes swapped-hint failures.
- **R2 (holdout-id renaming AS→ASZ)**: identical 11/12 pattern (H07 misses).
  The scheme keys on content, not id strings.
- **R3 (6 novel zero-overlap probes)**: 5/6 return junk (F_ABSTAIN) — the
  documented cost of rejecting abstention. (The 6th passed vacuously: its
  hint matched zero items.)
- **R4 (seal audit)**: no holdout content in the deliberation workdir or
  audit. All `H01`–`H12` grep hits are `PH01` substrings or the engine's own
  seal assertion ("H01-H12 unseen by me"). The engine's seal self-check
  passed before deliberating.

## Determinism

Three full reruns (deliberation + sealed bar): byte-identical.
`audit.md` sha256 `edca12a2…`, `retrieval.txt` `1f179896…`,
`summary.txt` `6e326277…`, `scheme.json` `afbc8b21…` — identical R1/R2/R3.
Zero RNG in every decision path (greedy loop, fixed palette order,
score-desc/id-asc tie-breaks).

## Bill (instrumentation)

- Index: 280 items / 35 KB corpus; vocab 1,485 (MORG) + 219 (probe);
  19+23 subjects. One-time df build ~1 s.
- Per query: full scan of N items × query tokens (exact-token counts);
  VERIFY adds ≤4 scoring passes per hinted query. Sealed bar (12 queries):
  ~1.4 s wall. Deliberation (5 rounds × 99 probes, ~14 full evals): ~20 s.
- Install: copy 35 KB corpus + build df table. Lookup: O(N·tokens).

## Recommendation (plain language)

TNN's deliberation worked as designed: it found a real scheme, rejected
three tempting-but-harmful moves with recorded reasons, and its one holdout
miss is a genuine discovery — **exact-token verification cannot tell a
wrong hint from a right hint with mismatched vocabulary**. Two fixes, in
order: (1) morphological normalization (stemming) in the tokenizer, which
would fix H07 and the 4 P-PARA misses that are stemmable; (2) a verify rule
that treats "hint-set scores 0 AND the query's distinctive tokens are absent
from the hint set" as *unverifiable* (keep the hint) rather than
*contradicted* (drop it). Re-run the bar after either; the harness,
batteries, and audit trail are frozen and reusable. Do not tune against the
holdout — the next bar needs fresh sealed probes.

## Artifacts

- `delib.zag` — the deliberative engine (pure Zag, pinned znc).
- `evidence.md` — frozen failure evidence TNN read.
- `PREREG_WS2C.md` — frozen preregistration (fixture-count corrected).
- `ws2c_r1/` — R1 outputs: `out/audit.md` (full trace), `out/scheme.json`,
  `out/results.txt`, `out/census.txt`, `bar/out/retrieval.txt`,
  `bar/out/summary.txt`, `SHASUMS.txt`.
- `runs/R2`, `runs/R3` — byte-identical reruns (hashes in SHASUMS.txt).
- `redteam/` — R1–R4 inputs and outputs.
