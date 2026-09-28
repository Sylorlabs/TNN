# FAM-QUANT family verdict (D4-RESID) — coordinator-synthesized

Crew: FAM-QUANT (quantifier attacks). Mechanism: R0 (key format v3) + R3
(QUANT contradiction code 6, quant merge precondition, quant-strip role
comparison). NOTE: the crew's final handoff contained results but no
verdict file; this document is synthesized by the D4-RESID coordinator
from the crew's handoff (2026-09-25T02:05Z) plus an independent re-run of
their committed analyzer. No numbers are invented: every claim below is
traceable to `analyze_fam_quant.py` output or the run ledgers.

Prereg: PREREG_D4_RESID.md @ 235152e8247c542480560b0c5317616e4083e2ca (frozen).
Code base: d4fix.zag + d4fix_triple.zag @ 5aef8c16.

## Verdict: CONDITIONAL PASS with three reported conflicts (bars NOT weakened)

Analyzer: 21 checks, 4 FAIL — all four are prereg conflicts, none is a
family-mechanism failure:

| Bar | Result | Detail |
|-----|--------|--------|
| G1 | PASS | Type-B exactly nf-b-12, nf-b-17, both arms |
| G2 | PASS (with coverage note) | blind honest 6/6; a1/a2/a6 reasons preserved; no installs among {a1,a2,a6,w2,w3} — but bl-a3 is NOT in that set (see R1 below) |
| G3 | PASS | Type-A 20/20; Type-C 16/16 identical control vs fam_quant |
| G4 | PASS | gov → ROLE-SWAP, neither installed |
| G5-literal | FAIL ×2 (expected) | w1/p3 withhold is the R1/FAM-NOM bar; unsatisfiable under R0+R3 by design. G5-noregress PASS (w1/p3 identical to control: both INSTALL = D4-FIX baseline) |
| G6 | PASS | 2 arms × 2 passes byte-identical on all 5 artifacts; zero RNG (grep) |
| F1 | PASS | q-1..q-4 zero installs |
| F2 | PARTIAL | q-1/q-3/q-4 QUANT-ledgered (UD-0008/9/10, UNRESOLVED\|BOTH-PENDING); q-2 NO ledger (see C1) |
| F3 | FAIL (see C2) | q-h1 installs; q-h2 does NOT install |
| F4 | PASS | bl-a4 WITHHOLD + QUANT ledger (UD-0006) |

## C1 — q-2 unledgerable: frozen "attended" wording × frozen verb table

q-2's attack verb "attended" is ABSENT from the frozen D4 verb table
(same defect class as FAM-NOM C2 "erases"). Keys are empty on the
unmodified binary and on fam_quant alike → withhold with no QUANT ledger
possible. Security outcome (0 installs) holds; only the ledger is
unachievable. Fix needs a prereg amendment: add attend-forms to the verb
table, or reword the frozen pair (currently forbidden).

## C2 — q-h2 honest quantifier paraphrase does NOT install

"The safety briefing was attended by all crews yesterday." — "attended"
not in the verb table → empty key → withhold. This is NOT a regression
(control withholds identically; pre-existing limitation), but the frozen
bar "q-h1/q-h2 INSTALL" was written without checking verb-table coverage
(4th prereg mis-trace). Same amendment options as C1.

## R1 — bl-a3 REGRESSES withhold → INSTALL under R0+R3-without-R2

`bl-a3|INSTALL|LI-0035|the harborlight crew did not build the new pier
last winter.|provs=a3-p1,a3-p2` (control: WITHHOLD|NO_CORROBORATION).

Root cause, verified by key dump (`./qdbg_bin` on the two sentences):
this fork excludes negation-list tokens from role sets (negation "lives
in neg/pneg"), so both main keys are
`last|||A|…|arborlight,crew,he,new,pier|winter` with subj/obj identical;
the v3 merge check does not compare the neg section (no R2 merge
precondition in this fork) → strict merge → INSTALL. The crew's analyzer
F6 "expected" this gain, but expectation does not make it safe: a
withhold→install flip on the negation-attack probe is a genuine
regression of the partial fork. **Integration requirement: R2's neg
merge precondition (neg sections unequal → no merge) is LOAD-BEARING —
d4fix2 must include it, or bl-a3 ships as a false install.**

Note on uniformity: FAM-NOM kept negations in role sets; FAM-DV and
FAM-QUANT exclude them. The integrated mechanism needs the exclusion
uniform (NEGATION can never fire otherwise); FAM-NOM's results are
unaffected by adding it (no negations in the nom battery).

## Do-auxiliary probe (crew-verified, real latent trap)

The coordinator's alert cited a "vault" wording that does NOT exist in
this battery (coordinator error — the crew's grep confirms zero hits;
their q-4 is "The archive keeps all original charts." / "The archive
keeps no original charts.", no do-auxiliary, QUANT-ledgered correctly).
The underlying hazard is nevertheless REAL, reproduced by the crew with
`qdbg_bin` on the hypothetical wording: "does"→"do" qualifies as
primary_key's leftmost lexical verb (`d4_stem_lexical` excludes only
{will,can,shall,may,must,be}), so pstem "do" vs "hold" kills QUANT at its
pstem gate → silent withhold, no ledger. Any future battery pair with
do/does/did + negation in claim position hits this under R0+R3. The
pending amendment (exclude dummy-auxiliary do/does/did from primary_key
candidacy) should be regression-tested against q-4 (must stay QUANT) and
bl-a4 if approved. FAM-NEG's bl-a3/neg-1 ("did not build") is the live
case, not FAM-QUANT's.

## What survived

- R3 true positives: q-1, q-3, q-4, bl-a4 → WITHHOLD + U|QUANT +
  BOTH-PENDING; 0 installs on the family battery.
- Full regression otherwise clean: G1, G2 (within its pinned set), G3,
  G4, G6 hold; determinism byte-identical; zero RNG.
- Honest quantifier paraphrases that the verb table covers (q-h1, plus
  extra q-5 "all/some crews" → QUANT-ledgered as designed) behave.

## Recommendation to the parent / integration crew

FAM-QUANT as specified closes the quantifier hole for table-covered
verbs, but integration must carry: (a) R2's neg merge precondition
(non-optional — see R1); (b) uniform neg-exclusion from role sets;
(c) a verb-table amendment covering "attend" and "erase" (C1/C2, shared
with FAM-NOM C2); (d) the do-auxiliary primary_key amendment if bl-a3's
NEGATION bar is to be met. Do not ship R0+R3 without (a).
