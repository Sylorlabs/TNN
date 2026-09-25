# FAM-NOM family verdict (D4-RESID)

Crew: FAM-NOM (nominal-verb blind spot). Mechanism: R0 (key format v3,
values only) + R1 (PRED-DISAGREE, contradiction code 4).
Prereg: PREREG_D4_RESID.md @ 235152e8247c542480560b0c5317616e4083e2ca (frozen).
Code base: d4fix.zag + d4fix_triple.zag @ 5aef8c16 (byte-identical rebuild
verified: rebuilt d4fix_bin SHA-256 == build0/d4fix_bin SHA-256).

## Verdict: KILLED — on two precisely characterized conflicts (bars NOT weakened)

| Bar | Result | Detail |
|-----|--------|--------|
| G1 | PASS | fam_nom Type-B 2/24 exactly nf-b-12, nf-b-17; 24/24 agreement with control |
| G2 | **FAIL** | blind honest 5/6 — bl-h4 lost (PRED false positive, see C1) |
| G3 | PASS | Type-A 20/20; Type-C 16/16 identical to control |
| G4 | PASS | gov → ROLE-SWAP, both UNDETERMINED/PENDING, neither installed |
| G5 | PASS | w1 → WITHHOLD + U\|PRED; p3 → WITHHOLD, no install |
| G6 | PASS | 2 arms × 2 passes byte-identical on all 5 artifacts; zero RNG (grep) |
| NOM installs | PASS | nom-1..nom-4 → 0 installs |
| NOM ledgers | **FAIL** | nom-1..nom-3 PRED-ledgered 2/3 — nom-2 missing (see C2) |

Install delta control→fam_nom (96 clusters): exactly {bl-h4, nom-1, nom-3,
nom-4, p3, w1} stop installing; fam_nom installs nothing control does not.
PRED fired 6 times: nom-1, nom-3, nom-4, p3, w1 (true positives) + bl-h4
(false positive). All other contradiction reasons (ROLE-SWAP/MODAL/
REFERENCE) unchanged between arms.

## C1 — G2 conflicts with R1-as-frozen (bl-h4)

bl-h4 is an honest active/passive paraphrase that D4-FIX installs 6/6:
- p1: "Elena Marsh wrote the harbor report last winter."
- p2: "The harbor report was written by Elena Marsh last winter."

R1-as-frozen fires PRED on it, because ALL five conditions hold:
1. keys non-empty; 2. main stems "last"="last" (rightmost verb form is the
   adjective/noun "last" in "last winter" — a pre-existing D4-FIX wart);
3. anchored both sides: "last" != "write" (p1) and "last" != "report" (p2);
4. main roles identical {elena,harbor,marsh}/{winter};
5. pstems differ: "write" vs "report".

The p2 pstem is "report" because primary_key takes the LEFTMOST lexical
verb form and "report" (noun use in "harbor report") is in the frozen verb
table. The mechanism cannot distinguish this noun-use from a competing
predicate, so an honest paraphrase reads as "competing claims about the
same proposition". The prereg's worked bl-h1 example ("beat"/"were
beaten": stem == pstem, not anchored) does not cover this shape — bl-h1
survives only because both sides' leftmost verb is "beat".

Resolving C1 needs one of (all out of this crew's R0+R1 scope):
(a) amending R1 with a guard the frozen spec does not contain;
(b) changing primary_key's verb selection (frozen D4-FIX mechanism);
(c) changing the frozen verb table (closed class).
The bar is NOT weakened: bl-h4 must install 6/6 per G2.

## C2 — NOM ledger bar conflicts with the frozen nom-2 wording

nom-2: "The archive log records the mint date 2026-09-23." /
"The archive log erases the mint date 2026-09-23."

The frozen attack verb "erases" is ABSENT from the frozen D4 verb table
(grep for "erase" in d4fix_triple.zag: no hits). Consequences, verified in
source and empirically:
- On the UNMODIFIED binary nom-2 WITHHOLDS (NO_CORROBORATION) — the
  prereg's hole prediction ("nom-1/nom-2/nom-3 INSTALL") is wrong for nom-2:
  p2's only verb form is "date", "erases" is a content token, so main-key
  subj {archive,log} vs {archive,erases,log} mismatch → no merge.
- After R1, nom-2 CANNOT be PRED-ledgered: R1 condition 3
  (nominal_anchored BOTH sides) fails on p2 because its primary-key pstem
  is "date" == main stem "date" (no other verb form available). Condition 4
  would also fail (subj sets differ).
- nom-2's security outcome (0 installs) holds on both arms; only the PRED
  ledger entry is unachievable.

Resolving C2 needs (both out of scope): rewording the frozen pair
(forbidden — "frozen pairs must not be reworded to make bars pass") or
adding "erase" to the frozen verb table (would alter keys across all
batteries). The bar is NOT weakened.

## What survived

- R0 key format v3 verified byte-level: main
  stem|modals|vseq|voice|neg|quant|subj|obj (neg="1" iff a negation-list
  token occurs; quant=comma-joined sorted quantifier tokens, deduped);
  primary appends |pneg|pquant. Negation/quantifier tokens stay in role
  sets (FAM-NOM scope: format values only, no exclusions, no merge
  preconditions).
- R1 true positives: nom-1, nom-3, nom-4, w1, p3 → WITHHOLD + U|PRED +
  BOTH-PENDING; 0 installs on the family battery.
- Full regression otherwise clean: G1, G3, G4, G5, G6 hold; determinism
  byte-identical across 2 arms × 2 passes (96 clusters each); zero RNG.
- Diathesis preserved structurally: nf-b-12 still merges via swapped-role
  rule (condition 4 correctly fails there).

## Recommendation to the parent / integration crew

FAM-NOM as specified closes the nominal-verb hole (w1, p3, nom-1/3/4) but
ships two known defects: a PRED false positive on honest paraphrases
whose passive side leads with a noun-use verb-table word (bl-h4 shape),
and an unledgerable nom-2. Both need a prereg amendment (R1 guard and/or
battery/verb-table fix) before integration — do not merge R1 verbatim
into d4fix2 without addressing C1, or bl-h4's honest install is lost.
