# FAM-NEG verdict

Family: LI-FAM-NEG — R0 (key format v3: stem|modals|vseq|voice|neg|quant|subj|obj,
primary v3) + R2 (NEGATION contradiction rule). R1/PRED and QUANT rules
explicitly NOT implemented.
Prereg: PREREG_D4_RESID.md @ 235152e8247c542480560b0c5317616e4083e2ca.
Base: D4-FIX @ 5aef8c16 (byte-identical verified). Pure Zag, zero RNG,
two byte-identical passes.

## Shared guards G1–G6 (fam_neg arm vs control, 102 clusters x 2 arms x 2 passes)

| Bar | Result | Detail |
|---|---|---|
| G1 Type-B | PASS | fam_neg 2/24 = nf-b-12, nf-b-17; control (unmodified D4-FIX) also 2/24, exact match |
| G2 blind | PASS | honest 6/6 install; bl-a1/a2/a6, w2/w3 ledgered ROLE-SWAP/MODAL/REFERENCE, none installed |
| G3 A/C | PASS | Type-A 20/20 both arms; Type-C 16/16 identical to control |
| G1c control | PASS | redundant with G1 (kept for analyzer parity) |
| G4 governing | PASS | gov-wolves -> ROLE-SWAP ledgered, neither side installed, WITHHOLD |
| G5 w1/p3 | REPORTED | both still INSTALL (R1 nominal-verb hole; no negation tokens, so R2 cannot touch them). Requires FAM-NOM mechanism; unchanged from D4-FIX baseline |
| G6 determinism | PASS | 5 artifacts x 2 arms x 2 passes byte-identical; zero-RNG grep clean |

No regression vs control on any shared guard (regression-guard grep: no
honest merging pair carries negation-list tokens except the intended
neg-h1/neg-h2 claim sentences).

## FAM-NEG family bars (frozen pairs)

| Bar | Verdict | Mechanism (probe-verified) |
|---|---|---|
| neg-1: 0 installs + NEGATION ledger | installs PASS / ledger FAIL | CONTRA=0: pstem "do"("did") vs "build" — prereg worked prediction mis-traced |
| neg-2: 0 installs + NEGATION ledger | installs PASS / ledger FAIL | CONTRA=0: both primary keys EMPTY ("approved" absent from frozen verb table) |
| neg-3: 0 installs + NEGATION ledger | installs PASS / ledger FAIL | CONTRA=0: both primary keys EMPTY ("emitted" absent from frozen verb table) |
| neg-4: 0 installs + NEGATION-or-QUANT ledger | installs PASS / ledger FAIL | CONTRA=0: pobj differ ("all" stays in p2 roles per frozen spec); QUANT out of scope |
| neg-h1: INSTALL | PASS | MERGE=1, installed |
| neg-h2: INSTALL | FAIL | MERGE=0: "filed" absent from frozen verb table -> p2 empty key |
| bl-a3: WITHHOLD + NEGATION ledger | withhold PASS / ledger FAIL | CONTRA=0: same pstem "do" vs "build" mis-trace as neg-1 |

## Crew-added extra pairs (documented, in-table verbs)

| Pair | Verdict | Detail |
|---|---|---|
| neg-5 (never/built) | PASS | CONTRA=5 NEGATION, 0 installs, WITHHOLD + NEGATION ledger |
| neg-6 (never/held) | PASS | CONTRA=5 NEGATION, 0 installs, WITHHOLD + NEGATION ledger |
| neg-h3 (never/did-not, built) | PASS | MERGE=1, installed |
| neg-h4 (never/did-not, showed) | PASS | MERGE=1, installed |

## Bottom line

R0+R2 are implemented exactly per the frozen spec and behave exactly as
specified everywhere the frozen battery lets them engage (neg-5/neg-6 ->
CONTRA=5; neg-h1/h3/h4 merge). The frozen family bars that FAIL do so
because of prereg-level conflicts between the frozen mechanism text and
the frozen battery/sentences, discovered empirically and reported without
weakening any bar or inventing any fix:

1. bl-a3/neg-1: worked prediction "pstem 'build' both" is a mis-trace;
   frozen code yields pstem "do" vs "build" (d4_stem_lexical excludes only
   {will,can,shall,may,must,be}), so the pstem-equality gate can never fire.
   (Also flagged independently by FAM-DV; PRED-preemption under integration
   is their measurement, reported for the integration crew.)
2. neg-2/neg-3: "approved"/"emitted" absent from the frozen verb table.
3. neg-4: "all" stays in roles per frozen R2 spec -> pobj unequal; QUANT
   rule is another family's.
4. neg-h2: "filed" absent from the frozen verb table -> honest INSTALL
   impossible.
5. G5 as literally written requires FAM-NOM's R1; out of scope for this
   family by prereg design.

Recommended amendments (for parent approval, NOT implemented): (a) exclude
dummy-auxiliary "do" from primary_key candidacy; (b) PRED/NEGATION
clause-ordering rule for integration; (c) extend frozen verb table or
reword frozen pairs (frozen pairs cannot be reworded without a prereg
amendment). Until amended, the honest verdict is: mechanism correct,
several family bars unpassable as frozen.
