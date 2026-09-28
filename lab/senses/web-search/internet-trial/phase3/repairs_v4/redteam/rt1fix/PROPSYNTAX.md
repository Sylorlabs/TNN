# LOGIC-CORE Proposition Syntax (PROPSYNTAX)

Native proposition language for the Track G logic engine (`logic.zag`).
Everything the engine judges is expressed in this syntax; the engine
performs **structural logical operations** on it — no keyword heuristics,
no lexicon, no web, no seeded verdicts.

## Lexical rules

- Identifiers: `[A-Za-z0-9_]+`. Case-insensitive (canonical form lowercases
  names and arguments; operator keywords stay UPPERCASE in canonical form).
- Whitespace between tokens is ignored.
- A proposition is one of the forms below. Nesting is allowed wherever a
  `<prop>` appears.

## Forms

| Form | Meaning | Example |
|---|---|---|
| `PRED(a1,a2,...)` | Atomic predication, `PRED()` allowed (0 args) | `FLOATS(ice,on_water)` |
| `NOT(<prop>)` | Negation | `NOT(BLIND(bats))` |
| `QTY(t,mode,...)` | Quantity claim about `t` (see below) | `QTY(senses,exactly,5)` |
| `CAUSE(<prop>,<prop>)` | Causal claim: antecedent brings about consequent | `CAUSE(RAIN(),FLOOD())` |
| `ALL(d,<prop>)` / `SOME(d,<prop>)` / `NONE(d,<prop>)` | Quantification over domain token `d`; `d` may occur inside `<prop>` | `ALL(birds,FLIES(birds))` |
| `IF(<prop>,<prop>)` | Conditional; consequent is **unasserted** | `IF(RAIN(),FLOOD())` |
| `MAYBE(<prop>)` | Hedged proposition; asserts nothing | `MAYBE(RAINS())` |
| `BEFORE(x,y)` / `AFTER(x,y)` | Temporal order of event tokens `x`,`y` | `BEFORE(dawn,noon)` |

## QTY modes

`QTY(thing, mode, values...)`, `thing` an identifier.

| Mode | Args | Interval meaning |
|---|---|---|
| `exactly` | one value `V` | `[V,V]` |
| `range` | `LO,HI` **or** one range literal | `[LO,HI]` closed |
| `at_least` | one value `V` | `[V,+inf)` |
| `at_most` | one value `V` | `(-inf,V]` |
| `more_than` | one value `V` | `(V,+inf)` open |
| `less_than` | one value `V` | `(-inf,V)` open |

Value tokens (parsed **natively** by the engine, never hand-normalized):

- Decimal integers: `5`, `22`, `33`.
- Word numbers: `five`, `twenty_two`, `thirty_three` (one–nineteen, twenty,
  thirty, …, ninety, and tens+ones composites).
- Unit suffixes (time): `sec(s)`, `min(s)`, `hr(s)`, `hour(s)`, `day(s)`,
  `wk(s)`, `week(s)`, `mo(s)`, `month(s)`, `yr(s)`, `year(s)`, plus `s`,
  `d`, `w`, `y`. No unit = bare count. Unit classes never mix: a `count`
  quantity is incomparable with a `sec` quantity.
- Range literals: `22_to_33`, `between_22_and_33` (either accepted as the
  single value of `range` mode).

Canonicalization: `AFTER(x,y)` ≡ `BEFORE(y,x)` (strict order, by definition);
`NOT(NOT(P))` ≡ `P`; word numbers and digit forms canonicalize to the same
decimal (`QTY(senses,exactly,five)` ≡ `QTY(senses,exactly,5)`).

## Native rule set (rule IDs emitted in proofs)

Evaluated per (claim, evidence-prop) pair, evidence in input order. At most
one DENY rule and one AFFIRM rule fire per pair. Final tag: DENY if any
DENY rule fired, else AFFIRM if any AFFIRM rule fired, else NEUTRAL.
Proof lists fired rule IDs in firing order (duplicates removed).

**DENY rules**
- `R-NEG-DENY` — claim `P` vs evidence `NOT(P)` (or claim `NOT(P)` vs
  evidence `P`), structurally.
- `R-CAU-DENY` — claim `q` vs evidence `CAUSE(r, NOT(q))`: the evidence
  asserts a cause of the claim's negation.
- `R-CAU-PROP-DENY` — claim `CAUSE(r,q)` vs evidence `NOT(r)`,
  `NOT(q)`, or `CAUSE(r, NOT(q))`: the named mechanism (or its effect)
  is refuted, so the claim *as stated* is false.
- `R-QNT-DENY` — quantifier contradiction over the same domain and body:
  `ALL` vs `SOME NOT`, `NONE` vs `SOME`, `ALL` vs `NONE`,
  `SOME` vs `ALL NOT` (either direction).
- `R-QTY-DENY` — claim and evidence are `QTY` on the same thing and unit
  class with **disjoint** intervals (e.g. `exactly 5` vs `range 22–33`;
  `exactly 3sec` vs `at_least six_months` after native unit conversion).
- `R-TMP-DENY` — claim `BEFORE(x,y)` vs evidence `BEFORE(y,x)` with
  `x≠y` (covers `AFTER` via canonicalization).

**AFFIRM rules**
- `R-IDENT-AFFIRM` — claim and evidence are structurally identical
  propositions (never fires for `MAYBE`: hedging is inert).
- `R-CAU-AFFIRM` — claim `q` vs evidence `CAUSE(r, q)`: the evidence's
  consequent is exactly the claim, **and** the reason `r` is a non-vacuous
  asserted proposition (atom, `QTY`, temporal, causal, or quantified).
  Vacuous reasons — `NOT(...)`, `MAYBE(...)`, `IF(...)` — never affirm:
  an adversarial evidence author could otherwise install any claim `q`
  via `CAUSE(NOT(anything), q)`.
- `R-QTY-AFFIRM` — `QTY` on the same thing/unit class with evidence interval
  ⊆ claim interval (e.g. claim `range 22–33` vs evidence `exactly 25`
  → AFFIRM; claim `exactly 25` vs evidence `range 22–33` → NEUTRAL:
  compatible but not entailed).
- `R-COND-MP` — claim `b`, evidence contains `IF(a,b)` **and** a separate
  evidence prop structurally equal to `a` (modus ponens over the evidence
  set; `IF(a,b)` alone never fires).

**Deliberate non-rules (documented scope boundaries)**
- `IF(a,b)` alone never affirms/denies `b` → NEUTRAL.
- `MAYBE(p)` never affirms/denies anything, even `MAYBE(p)` vs `MAYBE(p)`
  → NEUTRAL. Hedging is inert in both directions: `R-NEG-DENY` does not
  fire when either side is top-level `MAYBE` (so `MAYBE(A())` vs
  `NOT(MAYBE(A()))` → NEUTRAL — a hedge asserts nothing, so there is
  nothing to contradict).
- No antonym knowledge: `FLOATS(ice,on_water)` vs `SINKS(ice,in_water)`
  → NEUTRAL (different predicates; the engine does not guess opposition).
- No chained modus ponens, no order-theoretic completion
  (`NOT(AFTER(a,b))` does not yield `BEFORE(a,b)`).
- `QTY` intervals that merely overlap (neither disjoint nor subset)
  → NEUTRAL.

## Engine interface

```
logic_bin <input.tsv>
```
Input TSV: `id \t claim_prop \t evidence_props \t oracle`
(`evidence_props` = `;`-separated propositions; `oracle`: 0/1/2, ignored by
the engine, used only by the scorer.)
Output per line: `id SP tag SP proof` where `tag` ∈ {0=NEUTRAL,
1=AFFIRM, 2=DENY} and `proof` = `;`-separated rule IDs in firing order
(empty when NEUTRAL with no rules fired).
Pure Zag, zero RNG, no I/O except the input file and stdout.
