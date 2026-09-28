# COMMIT_SCHEMAS.md — the commitment ceremony (frozen)

Per PREREG_ONEENGINE_VS_DUAL.md §2 (frozen, commit b5136fdb): inference
rules enter the engines ONLY as structured byte schemas committed here,
once, auditable. Both engines (ONE and DUAL) embed these exact bytes;
each engine asserts the schema hashes at startup and refuses to run on
mismatch. If a schema mis-encodes its rule, that is a build defect found
by the audit bar (KB4), not a silent fix.

Committed: 2026-09-24 by the coordinator, BEFORE any engine code, per the
commit protocol (§9). Source of truth: this file. The prereg gifts ONLY
what the frozen knowledge store gifts (K005: modus ponens, proof by
contradiction; universal instantiation via the K001 phrasing judgment
call, documented below and frozen).

## 1. Claim language (byte syntax, canonical)

All claims, premises, targets, patterns, and bindings are byte strings in
this syntax. No whitespace. Canonical form = exactly these bytes.

```
term    := const | var | fn '(' term { ',' term } ')'
const   := [a-z][a-z0-9_]*        e.g. socrates  a  k  sqrt2  add
var     := '?' [0-9]+             e.g. ?0 ?1 ?2   (schema binding variables;
                                                  never appear in ground claims)
fn      := [a-z][a-z0-9_]*        e.g. mul  div  mod4sq  sk
formula := atom
         | 'not(' formula ')'
         | 'imp(' formula ',' formula ')'
         | 'and(' formula ',' formula ')'
         | 'or(' formula ',' formula ')'
         | 'forall(' bvar ',' formula ')'
         | 'false'
atom    := pred '(' term { ',' term } ')' | pred     (0-ary atom, bare const)
pred    := [a-z][a-z0-9_]*        e.g. prime  divides  eq  ge
bvar    := [a-z][a-z0-9_]*        forall-bound variable, e.g. x  n
```

Notes:
- `and`/`or` exist in the language but NO committed schema eliminates or
  introduces them. Batteries are authored to not require and-elim/or-elim
  (conjunctions are split into separate premises; disjunctions avoided;
  implications are curried: imp(A, imp(B, C)) instead of imp(and(A,B), C)).
- `false` is the absurd claim. Negation semantics (§5) is language-level.
- Ground claim = formula with no `?N` variables. Patterns = formulas that
  may contain `?N`. A binding maps each `?N` to one ground subformula/term.

## 2. The three committed schemas (exact bytes)

Canonical schema bytes = `ID|A1|...|An|C` (fields joined by `|`, no spaces).
Hash = FNV-1a-64 over the canonical bytes (hex, 16 digits). Engines
recompute and assert equality at startup.

### S_MP — modus ponens (K005: "from P and P=>Q, infer Q")

```
ID: S_MP
A1: ?0
A2: imp(?0,?1)
C:  ?1
canonical: S_MP|?0|imp(?0,?1)|?1
hash: 62cc41ffd582e687
```

Rationale: `?0` binds any ground formula P in memory; `imp(?0,?1)` then
matches a ground implication whose antecedent is byte-identical to P,
binding `?1` to its consequent Q; the engine produces Q. This is exactly
modus ponens: the two antecedent patterns ARE the rule's two premises,
and the consequent pattern IS the rule's conclusion, with `?0`,`?1` as
the rule's schematic letters. No other reading is possible: any ground
instance (P, imp(P,Q) |- Q) is produced and only such instances.

### S_PBC — proof by contradiction (K005: "if assuming NOT-P leads to a contradiction, infer P")

```
ID: S_PBC
A1: imp(not(?0),false)
C:  ?0
canonical: S_PBC|imp(not(?0),false)|?0
hash: 0369efe53016bbe1a
```

Rationale: `?0` binds the formula P to be proved; the single antecedent
pattern `imp(not(?0),false)` is the claim "assuming not-P leads to
contradiction"; the consequent `?0` is P. This is exactly K005's proof by
contradiction.

ATTACHMENT (PBC-SUB, part of this schema's encoding, frozen): a ground
claim matching `imp(not(P),false)` is established by subproof — assume
`not(P)`, run bounded match-and-bind with the SAME three schemas over
memory ∪ {not(P)}; if `false` is derived, the subproof succeeds and P is
produced, citing (S_PBC, assumption not(P), subproof steps). The subproof
uses no new rules: it is match-and-bind all the way down, recorded in the
audit chain. The assumption is discharged (never leaks into memory).

### S_UI — universal instantiation (judgment call, frozen with the prereg)

K001's phrasing ("P(n) implies P(n+1) for every positive integer n") gifts
universal claims with instantiable bound variables. The prereg §2 records
this as a documented judgment call; this encoding freezes it.

```
ID: S_UI
A1: forall(?0,?1)
C:  SUBST(?1,?0,?2)
canonical: S_UI|forall(?0,?1)|SUBST(?1,?0,?2)
hash: b2f909c7d7b67f55
```

Rationale: `?0` binds the bound-variable symbol (e.g. `x`), `?1` binds the
body formula. The consequent is the body with every free occurrence of the
bound variable replaced by the ground term bound to `?2`. This is exactly
universal instantiation: from ∀x.φ(x) infer φ(t).

`?2` RANGES OVER A DETERMINISTIC TERM UNIVERSE (frozen): all distinct
ground terms occurring in current memory, enumerated depth-first,
left-to-right, in memory order (claim 0's terms, then claim 1's, ...),
first-appearance order, excluding the bound variable itself. No other
terms. This makes UI deterministic given state (no guessing, no RNG).

IMPLEMENTATION BOUND (documented, monitored): UI is applied per BFS level
against the term universe fixed at level start; any single claim larger
than 256 symbols is refused with a FLAG (never silently truncated). The
batteries are sized far below this; a run hitting it is reported, not
hidden. This is a load-bearing resource bound (finite memory), not a
reasoning limit.

## 3. Negation semantics (language-level, not a fourth schema)

If memory contains both `F` and `not(F)` with byte-identical `F`, the
engine derives `false`, citing (CONTRA, the two claim refs). This is the
meaning of `not`/`false`, presupposed by K005's proof-by-contradiction
wording ("leads to a contradiction"). It is structural, domain-free, and
identical in both engines. It is NOT an inference schema and carries no
domain content.

## 4. What is NOT committed

- No and-elimination, or-elimination, exists-elimination/introduction,
  forall-introduction, induction schema, or arithmetic computation. If a
  battery needs them, the battery's formalization does the standard
  faithful preprocessing openly (split conjunctions into premises,
  skolemize existentials with fresh constants, curry nested antecedents)
  and documents it per problem. The engines never invent these steps.
- No problem-specific content anywhere in this file: the schemas mention
  no predicates, no constants, no domains.

## 5. Audit citation format (both engines)

Every derived claim cites: `SCHEMA_ID  premise-ref...  binding`. Example:
`S_MP  P3 P7  ?0:=even(k) ?1:=eq(mod4sq(k),0)`. Schema IDs are the frozen
IDs above; premise refs are the engine's claim indices; bindings list
`?N:=<ground bytes>`. PBC-derived claims cite `S_PBC  ASSUME:not(P)
SUBPROOF:<steps>`. Contradiction steps cite `CONTRA  <refA> <refB>`.

## 6. Conformance

Both engine builds embed the three canonical byte strings verbatim and
assert all three hashes at startup (exit 6 on mismatch). The build docs
record the assertion. Any divergence = build rejected.
