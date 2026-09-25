# IDEAS_N7 — DISCRIM-NATIVE: native discriminator under false-rule injection

Crew: MATH R4 engine N7. Date: 2026-09-25 (PDT).
Status: SPEC FROZEN — committed before any build, per PREREG_MATH_R4 §8.

## 1. Mission (prereg §1)

Build a native that DISCRIMINATES under false-rule injection on B5X-NL:
DERIVES the true chains, WITHHOLDS the false ones. Not withhold-everything
(R3 natives: 24/60, fd=0, fw=36), not derive-everything (DUAL: 24
false_derived). Bar: PB3 = ≥45/60 correct, <10 false_derived, <10
false_withheld.

## 2. Chosen design: exact-span grounding + negation-skeleton contradiction sweep

### 2.1 The mechanism (four passes, all byte-native)

**Pass 1 — Parse.** Problem file → premise spans, target span. Store files
(base R-rules + injected I-rules; the INJ files carry I-rules only, so the
engine loads the problem's BASE-STORE: file from the same directory as the
given injected store) → rule spans (id, antecedent, consequent). Byte
operations only: cut parenthetical justifications at `. (`, split antecedent
/ consequent at `, then `, strip trailing `.`. No parsing into
subject/predicate, no variables, no grammar.

**Pass 2 — Ground (forward chain).** A rule fires iff its antecedent span is
byte-identical (case-insensitive) to a live claim span — premises first,
then derived consequents, iterated to fixpoint in deterministic file order.
A chain whose antecedent never grounds is REFUSED: it simply never fires.
No fuzzy matching, no arithmetic normalization, no substring tricks. This is
the deliberate "check every step's byte-span grounds" step: the Euclid's-lemma
false rule (`then 7 divides 8`) fires only if `7 divides 8`'s antecedent
grounds; the `5 squared = 2 squared + 3 squared` → `25 = 13` bridge never
fires because the spans differ.

**Pass 3 — Hunt (contradiction sweep with cascade).** Every derived claim is
checked against every premise for byte-skeleton contradiction. Three
closed-class, content-word-agnostic patterns (case-insensitive):

- (a) `not`-insertion: premise = X + `not ` + Y contradicts claim = X + Y
  (e.g. `8 is not a multiple of 7` vs `8 is a multiple of 7`).
- (b) `is not` vs `=`: premise = A + `is not` + B contradicts claim =
  A + `=` + B (e.g. `49 - 25 - 36 is not 0` vs `49 - 25 - 36 = 0`).
- (c) existential negation: `there is no <NP>` contradicts
  `there is a/an/some <NP>` with identical remainder
  (e.g. `There is no integer c with 19 = 0 x c` vs
  `there is an integer c with 19 = 0 x c`).

A contradicted claim dies; death cascades through derivation supports (a
claim survives iff at least one support path is live). This is the hunt for
the injected false rule — it fires mid-chain wherever its consequent (or a
downstream consequent) collides with a premise, and the whole poisoned chain
is retracted. Patterns key on function words (`not`, `is`, `no`, `a/an/some`,
`there`), never on content words, so they track relations, not surface
vocabulary.

**Pass 4 — Verdict.** DERIVED iff the target span matches a live (non-dead)
claim; otherwise WITHHELD. The distractor true-but-irrelevant chain
(library/bakery/…) fires harmlessly and never reaches the target: relevant
truth, not mere truth, decides.

### 2.2 Why these ideas (and not the alternatives)

1. **Exact-span grounding instead of fuzzy/idiom matching.** R3's n1 fired
   byte-pattern licenses but couldn't compose; n2's fuzzy backward links
   found nothing. The B5X battery is byte-designed: near-miss antecedents
   (`, `-comma in `transversal t cuts lines l and m, forming…`,
   `integers, and 19 != 0` vs `integers with 19 != 0`, `Transversal` vs
   `transversal`) are deliberate traps. Fuzzy grounding would fire the false
   chains; exact grounding refuses them. Strictness here is not stupidity —
   it is the discrimination.
2. **Case-insensitive exactness.** The one leniency: `A triangle…` (premise)
   vs `a triangle…` (R045/R085 antecedent) must ground, else the entire
   03-family true chain stalls. Case carries no logical content in this
   battery; punctuation and wording do. Verified: no W-kind false chain
   becomes fireable under case-insensitive matching (all are protected by
   commas or wording, checked problem by problem).
3. **Contradiction as byte-skeleton, not as logic engine.** The alternative
   — a formal contradiction prover — would be a disguised formalizer. The
   three patterns are syntactic: they never name a relation, never bind a
   variable, never evaluate arithmetic. They are also deliberately
   incomplete (no `does not` morphology, no `!=`, no quantifier reasoning
   beyond `there is no`): the sweep is a hunter, not an oracle. Verdicts do
   not depend on catching every false claim — only on never deriving the
   target through a poisoned chain.
4. **No anaphora resolution (documented gap).** Six D-kind problems
   (L2/L3/L4 × 08/18) need `those subsets` → `the 2-element subsets of an
   5-element set` and `their count` → `the count of 2-element subsets`.
   Resolving this needs demonstrative/possessive span surgery — a real
   mechanism, but heuristic, and one misfire could poison true chains. With
   the bar at 45 and 54 projected without it, N7 withholds these six
   honestly (the true chain dead-ends; the target is unreached) rather than
   risk the audit. This is the known, named limitation: the coreference gap.

### 2.3 Projected score (hand-derived from the frozen battery bytes)

- 30/36 D-kind: true chain grounds exactly (case-insensitive); target
  derived. 6 D-kind (anaphora family) honestly withheld → 6 false_withheld.
- 24/24 W-kind: false chains stall on ungrounded antecedents (commas,
  wording, case-protected traps), except L2_05/L2_15 where the false chain
  reaches the target and is killed by pattern (c) → 0 false_derived.
- **Projected: 54/60, fd=0, fw=6** — clears PB3 (≥45/60, <10 fd, <10 fw).

### 2.4 What the mechanism catches vs what fools it (mechanism-level story)

- **Caught:** the Euclid's-lemma misapplication (L2/L3/L4_01/11 families) —
  hunted at the chain end by pattern (a); the `0 divides 19` →
  `there is an integer c with 19 = 0 x c` false derivation (L2_05/15) —
  killed at the target by pattern (c); the Pythagorean overgeneralization
  (L2/L3_03/13 families) — hunted by pattern (b); all comma/case-trapped
  false chains (midpoint `MN = 8`, alternate-interior `alpha = beta`,
  pigeonhole `some mailbox received at least 2 letters`) — refused at the
  ungrounded antecedent, never fire.
- **Fools it (by design limits):** the anaphora family — N7 cannot even
  *reach* the target, so it withholds; this is a reachability gap, not a
  discrimination failure. Arithmetic-bridged false steps
  (`5 squared = 2 squared + 3 squared` ≡ `25 = 13`) stall rather than get
  refuted — N7 never asserts them as lemmas it believes, it just can't
  prove them false; the verdict is unaffected.
- **DUAL's mirror failure avoided:** DUAL derives false chains because it
  never checks a consequent against the premises. N7 checks every derived
  claim against every premise, every run.

## 3. Nativeness audit argument (prereg §7)

- Every derivation step's grounds are byte-spans of the problem/store text
  or prior steps (stored as buffer offsets; the trace prints the spans).
- No step cites a schema term absent from the bytes. No typed variables, no
  scope, no unification, no formal syntax, no NL→schema translation step.
  Case-folding, `. (`-cutting, and trailing-`.`-stripping are byte
  operations, not parsing.
- The contradiction patterns are closed-class function-word skeletons;
  they contain no content-word lexicon and no per-problem content. Under
  nonce-word substitution of content words the patterns behave identically
  (relations preserved → same verdicts), satisfying the §7.4 vocabulary
  probe in principle.
- **Known paraphrase limitation (honest):** grounding is byte-exact, so a
  meaning-preserving rewording of an antecedent breaks grounding and flips
  DERIVED→WITHHELD. Paraphrase robustness is out of scope for this build;
  N7 does not claim to pass the sealed PARA-INV gate. Discrimination tracks
  relations (the sweep); reachability tracks bytes (the grounding). The
  round's paraphrase hunt belongs to N5/N6-line work.

## 4. Engineering contract

- Pure Zag, zero RNG, deterministic (rules in file order, claims in
  derivation order; 3× external reruns must be byte-identical).
- Pinned toolchain `znc_linux_x86_64_abed8aa1`.
- CLI: `n7_bin <problem> <inj_store> <out.trace>` (R3 convention); the
  engine additionally loads the problem's BASE-STORE: basename from the
  injected store's directory. Exit 3 if any arg contains `sealed`.
- Trace format: `N7-TRACE v1` header, premises/target spans, per-rule
  firing records with grounding claim ids, contradiction-sweep kills with
  the refuting premise, cascade notes, and a final `VERDICT: DERIVED` /
  `VERDICT: WITHHELD` line (regex-compatible with the R3 scorer family).
- Carryover batteries only (r3n, b5x_nl, b6x_nl, twins, b1n). Sealed R4
  batteries (CHAIN-NL/CHAIN50-NL/PARA-INV) are never read before the seal
  commit.

## 5. Kill criteria for this build

- If reruns diverge (non-byte-identical) → build VOID, fix before scoring.
- If B5X-NL < 45/60 or fd ≥ 10 or fw ≥ 10 → H-DISC-NATIVE fails for N7 as
  built; the mechanism-level miss table (§2.4) says exactly where.
- If the disguised-formalizer audit finds a schema term, variable, or
  unification in the trace → build VOID.
