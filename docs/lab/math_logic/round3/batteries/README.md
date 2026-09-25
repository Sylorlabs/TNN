# MATH Round 3 batteries (native NL reasoning)

Round 3 tests whether native engines reason directly over raw utterance
bytes -- no NL->schema translation. Engines see the raw NL files below;
formal controls (DUAL-R1, REF-FIRST) work from the formal originals.

## Batteries

- `r3n/` -- 24 native items (R3N_01..R3N_24): 6 each in number theory,
  geometry, logic puzzles, causal/temporal. Types: proof / derivation /
  refutation-open. 8 of 24 are gullibility traps (twin-prime conjecture,
  false universal claims, affirming the consequent, denying the
  antecedent, post-hoc and lucky-socks causation); verdicts are sealed.
- `twins/` -- 37 NL twins (T2_01..T4_15) of the round-2 formal originals
  B2_01..B4_15: same problems, NL wording only. T2_07 is a trap
  (round-2 F-SEAL-01: B2_07 is genuinely underivable); the other 36
  follow from their premises.
- `b5x_nl/` -- 60 false-rule-injection problems (depths 2/3/4 x 20; 12
  Kind D + 8 Kind W per level). The false rule sits MID-CHAIN
  (position p=(L+1)//2), never at the endpoint, and every problem carries
  one distractor true-but-irrelevant chain. False rules are plausible
  corruptions of real NL knowledge items (Euclid's lemma, Pythagoras,
  pigeonhole, binomial coefficients, mid-segment theorem, ...).
  Verdict = derivation from TRUSTED premises + BASE store only.
- `b6x_nl/` -- 3 raw-NL deep derivations (linear chain, DAG with merge,
  contradiction chain), each requiring >=100 distinct derivation steps
  (bound 128), rendered from deterministic formal skeletons.
- `knowledge/` -- KNOWLEDGE_STORE_NL.md: frozen raw-NL rendering of the
  round-2 KNOWLEDGE_STORE.md (25 items). All R3N items cite only IDs /
  content from this file.

## Sealed (never on an engine input path)

- `sealed/SEALED_R3N.sol`, `sealed/SEALED_TWINS.map`,
  `sealed/SEALED_B5X_NL.sol`, `sealed/SEALED_B6X_NL.sol` -- verdict keys.
- `sealed/B6X_SKELETONS.json` -- formal skeletons for the B6X step audit.
- `sealed/SEALED_AUDIT.txt` -- 6 paraphrase + 6 nonce-word anti-bridge
  variants of R3N items (sealed).

## Determinism

`gen_batteries_r3.py` is the single deterministic source: no RNG, no
timestamps, no unordered iteration. Re-running it reproduces this tree
byte-for-byte (checked by `verify_batteries_r3.py`).

The generator exits 3 if any sealed content is ever directed outside
`sealed/` (sealed-path guard).
