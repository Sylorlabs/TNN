# MATH R2 extended batteries (battery crew, frozen before engines run)

Authored deterministically by `gen_batteries.py` (no RNG; rerun is
byte-identical). Verified by `verify_batteries.py` (mechanical property
checks, not an engine). Scored for B7F by `b7f_checker.py`.

## Layout

- `b4x/` — 15 transfer problems (B4X_01..15), causal / temporal / semantic /
  social, beyond math-adjacent. Each needs >= 3 derivation steps, solvable
  ONLY with the committed schemas (S_MP, S_PBC, S_UI) + `knowledge/KB_B4X.md`.
- `b5x/` — 60 false-rule-injection problems: 3 chain-depth levels (L2/L3/L4)
  x 20. False rules chain: false sd=>fd_1 plus false fd_1=>fd_2 makes false
  sd=>fd_2 derivable in 2 hops (single-hop detection insufficient: no single
  false rule's consequent is contradicted by trusted content; ablation proves
  every hop is needed). Injected into COPIES of the store:
  `knowledge/KB_B5X_L2.md`, `KB_B5X_L3.md`, `KB_B5X_L4.md` (copies of
  `knowledge/KB_B5X_BASE.md` plus the false chains). Kind D (12/level):
  correct verdict DERIVED (true chain survives; false endpoint defeated by a
  trusted premise). Kind W (8/level): correct verdict WITHHELD (target
  derivable only via the false chain).
- `b6x/` — 3 scaling problems needing >= 100 DISTINCT store items each
  (verified, no padding): B6X_01 linear 120-chain (120 items), B6X_02 DAG
  with curried merge (110 items), B6X_03 PBC chain (101 items). Bound 128.
- `knowledge/` — KB_B4X.md, KB_B5X_BASE.md, KB_B5X_L2/L3/L4.md, KB_B6X.md,
  KB_B7F.md (intentionally claim-free; B7F analogs are self-contained).
- `sealed/` — grader solutions. NEVER on an engine input path (exit-3 guard).
  SEALED_B4X.sol (15), SEALED_B5X.sol (60), SEALED_B6X.sol (3),
  SEALED_B7F.sol (20 verdicts), SEALED_B7F_NL.md (20 NL texts),
  SEALED_B7F_FORM.sol (20 formal analogs). B5X verdicts are computed from
  trusted premises + the BASE store (injection excluded).
- `B7F_MANIFEST.md` — B7F IDs + domains only (no NL wording leaks).
- `b7f_checker.py` — mechanical schema-equivalence scorer (schema-choice +
  slot-binding, 0-100). Reads sealed analogs only at scoring time; prints
  numeric subscores only. Usage:
  `python3 b7f_checker.py sealed/SEALED_B7F_FORM.sol produced.form`
  where produced.form uses the .form layout.
- `verify_batteries.py` — battery-property verification (forward S_MP/S_UI
  closure + CONTRA; no referee/PBC/learning). Run: `python3 verify_batteries.py`.
- `gen_batteries.py` — deterministic authoring source.

## Conventions

- `.form` format matches round 1 exactly: `ID:`, `STORE:`, `PREMISES:`,
  `TARGET:` (no whitespace inside claim bytes).
- `STORE:` paths resolve relative to `docs/lab/math_logic/` (round-1
  convention), e.g. `round2/batteries/knowledge/KB_B4X.md`.
- B1N: no new authoring; P01-P22 raw NL texts confirmed present in
  `docs/lab/math_logic/problems/P01.txt`..`P22.txt` (round-1 commit).

## Sealing protocol (followed)

Batteries + sealed solutions committed to branch `tnn-native-lab` BEFORE any
engine build/run. Engines never read `sealed/` (guard exits 3 on any input
path containing "sealed"). The LEARN-FORM learner additionally never sees
`SEALED_B7F_NL.md` (trains on frozen round-1 traces only); B7F NL wordings
verified absent from round-1 traces by 6-gram wash in `verify_batteries.py`.
