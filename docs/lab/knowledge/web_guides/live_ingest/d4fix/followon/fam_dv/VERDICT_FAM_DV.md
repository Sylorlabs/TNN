# FAMILY VERDICT — FAM-DV (distinct-verb attacks)

**Crew:** D4-RESID FAM-DV (depth-2 subagent)
**Prereg:** `PREREG_D4_RESID.md` @ `235152e8247c542480560b0c5317616e4083e2ca` (frozen)
**Base code:** D4-FIX @ `5aef8c16` (sources verified byte-identical, SHA prefix
`1697a0d3d04fe01b` / `77c6afc52da9fbaa` / `e6379ddb0b05d95b`)
**Date:** 2026-09-24/25 (UTC 2026-09-25)
**Implemented:** R0 key format v3 + R1 PRED-DISAGREE, exactly per prereg §2/R1.
R4a/R4c as verification locks. No R2/R3 code (out of scope for this family).

## Implementation (committed)

- `fam_dv.zag` — driver; `d4_keys_contradict` extended to 12 args
  (primary pair + main pair), PRED test FIRST, returns 4; driver maps 4 → `PRED`.
- `fam_dv_triple.zag` — key module: exact frozen negation list
  (not/no/never/neither/nor/none/nobody/nothing/nowhere,
  without/lacking/minus; n't-contractions) and quantifier list
  (every/all/each/both/some/several/many/much/few/a few/one/two/…/ten,
  first/second/…/tenth); negation excluded from content sets; main v3
  `neg`+sorted `quant` sections before subj/obj; primary v3 `pneg`+sorted
  `pquant` appended; subj/obj merge indices shifted 4/5 → 6/7.
- Build: clean, same 17 baseline analyzer warnings as unmodified.

## Battery & method

- DV battery (`dv-1`..`dv-4`, each +2 neutral fillers) committed BEFORE
  implementation (commit `790b2d3302631d72d021bdf2dff2c588bbded3e9`).
- Unmodified-binary hole demo: `w1` INSTALLS, `dv-2` INSTALLS (nominal hole);
  `bl-a5`, `dv-1`, `dv-3`, `dv-4` withhold. Recorded in `hole_evidence.txt`.
- Full regression: B1 (60) + B2 (p1..p4) + B3 (S1 h/a) + B4 (w1..w3) +
  B5 (blind h1..h6/a1..a6) + governing wolves/hawks pair + DV battery =
  **96 clusters, control + fam_dv arms × 2 passes, all five artifacts
  byte-identical pass1=pass2 (DETERMINISM PASS)**.
- Zero RNG: grep for `rand|seed|random|shuffle` over all Zag + Python sources:
  zero matches.

## Results

| Bar | Result | Evidence |
|-----|--------|----------|
| DV: dv-1..dv-4 → 0 installs | **PASS** | 0 installs |
| DV: dv-2 → PRED ledger | **PASS** | `U\|…\|dv-2\|PRED\|…` |
| DV: dv-1/dv-3/dv-4 withhold, no install | **PASS** | — |
| DV: bl-a5 → WITHHOLD | **PASS** | — |
| DV: w1 → WITHHOLD (+PRED ledger) | **PASS** | `U\|…\|w1\|PRED\|…` |
| G1 Type-B 2/24 (nf-b-12, nf-b-17); control 0/24 | **PASS** | — |
| G2 blind honest h1..h6 → 6/6 | **FAIL** | 5/6 — **bl-h4 → PRED**, withheld |
| G2 attacks a1/a2/a6 + w2/w3 ledgered | **PASS** | ROLE-SWAP / MODAL / REFERENCE / ROLE-SWAP / MODAL |
| G3 Type-A 20/20; Type-C = control 16/16 | **PASS** | — |
| G4 governing → ROLE-SWAP, neither installed | **PASS** | — |
| G5 w1 WITHHOLD; p3 WITHHOLD no install | **PASS** | w1 PRED; p3 PRED |
| G6 determinism + zero RNG | **PASS** | byte-identical; grep clean |

No unexpected installs: fam_dv's 7 installs over control are exactly the 5
honest blind + nf-b-12/nf-b-17 (all bar-required).

## G2 conflict — bl-h4 PRED false positive (KNOWN, shared with FAM-NOM)

**Observed:** `bl-h4` ("Elena Marsh wrote the harbor report last winter." /
"The harbor report was written by Elena Marsh last winter.") → `PRED`,
WITHHOLD. It is an honest active/passive paraphrase and must INSTALL per G2.

**Root cause (verified by key dump, hex):**
- Main keys: stem `last`=`last` (the rightmost verb-table form is "last" in
  "last winter"); subj `elena,harbor,marsh` = `elena,harbor,marsh`;
  obj `winter` = `winter`.
- Primary keys: pstem `write` vs `report` — "report" (noun use: "the harbor
  report") is in the frozen verb table and is p2's leftmost lexical verb-table
  hit, so it is selected as p2's primary over the true predicate "written".
- All five frozen PRED conditions hold: keys non-empty; main stems equal;
  anchored both (`last`≠`write`, `last`≠`report`); main roles identical;
  pstems differ. → code 4.

The prereg's worked prediction for the analogous bl-h1 case ("stem == pstem
('beat'), not anchored") is a mis-trace: the code selects `last` as the main
verb there too; bl-h1 is saved only by pstem equality (`beat`=`beat`), which
bl-h4 lacks because of the `report` noun-verb.

**Cross-check:** sibling FAM-NOM crew independently reproduced this exact
false positive on the identical R1 spec and killed their round honestly
rather than weakening the bar (their verdict:
`docs/lab/knowledge/web_guides/live_ingest/d4fix/followon/fam_nom/FAMILY_VERDICT.md`).
This crew likewise did **not** invent a guard outside the frozen spec.

**For the integration crew:** R1-as-frozen over-fires on honest
passive paraphrases whenever (a) a verb-table form sits in trailing
adjunct position ("last winter") becoming the main verb on both sides, and
(b) a noun-use verb-table hit ("report") becomes one side's primary. Any
frozen-prereg amendment must exclude this shape without losing the true
positives (w1, dv-2, nom-3, p3 — all verified PRED above).

*Scratch validation (not implemented, for amendment design only):* a
"displaced primary" guard — a primary verb-form is displaced if a later verb
follows it across a bridge of only glue/be-form tokens containing a be-form
("report **was** written": `report` displaced; "marks **the** mint": not, no
be-form) — blocks bl-h4 while keeping w1/dv-2/p3/nom-3 → PRED in a scratch
harness (6/6 correct). Uses only existing closed-class lists (glue,
be-forms). Proposed as candidate amendment language, not as code.

## Cross-family note (for integration)

`bl-a3` ("did not build"/"built") → PRED + WITHHOLD under R0+R1 (verified).
R2's NEGATION as frozen requires pstem equality, but the actual pstems are
`do` ("did") vs `build` — the prereg's R2 worked prediction ("pstem 'build'
both") is likewise a mis-trace. Under full R0+R1+R2 integration, PRED (code
4, fired first) would preempt NEGATION for bl-a3, conflicting with FAM-NEG's
bar ("bl-a3 → WITHHOLD + NEGATION ledger"). Flagged for the integration
crew; not a FAM-DV bar.

## Verdict

**FAM-DV: CONDITIONAL PASS** — all family bars and G1/G3/G4/G5/G6 hold;
dv-2 PRED true-positive confirmed; **G2 fails 5/6 on the known frozen-spec
bl-h4 false positive** (same root cause as FAM-NOM's). No bars weakened, no
spec deviations. Awaiting frozen-prereg amendment (or integration-crew
ruling) on the PRED false-positive shape.
