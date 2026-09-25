# IDEAS_N6 — N6 GOALCHAIN-NATIVE: explicit multi-step chaining over byte spans

**Round:** MATH R4 (frozen prereg `84ed45077a554f9897ec55c2ca1430273c79eb69`,
`docs/lab/math_logic/round4/PREREG_MATH_R4.md`).
**Spec status:** FROZEN by this commit (prereg §8: IDEAS addendum before any build).
**Author:** engine crew N6. **Date:** 2026-09-25.

---

## 1. The failure being attacked (R3 verdict §3)

R3's mechanism-level finding: natives RECOGNIZE inference idioms but DO NOT
COMPOSE them. n1's licenses fired yet chains never reached goals (3/37 twins)
— forward search drifted off-goal with no goal pressure. n2's backward
byte-overlap links found nothing (1/37) — overlap is too weak a relevance
signal. n3's machinery worked (derived a dev pigeonhole) but every thread
exhausted budget on real problems — search without goal-anchored pruning.

N6's thesis: **the composition failure is a search-control failure, not a
recognition failure.** The idioms were fine; what was missing was a mechanism
that (a) starts from the goal, (b) expands ONLY goal-relevant steps, (c)
remembers what it proved (lemmas), (d) backtracks on dead ends, and (e) says
WHY a chain died instead of silently drifting. N6 is that mechanism, over raw
byte spans, with zero formal machinery.

## 2. Core mechanism: goal-anchored backward chaining

```
need(G):                          # G = goal byte-span
  if memo[G] = proved   → return its chain        # lemma reuse
  if memo[G] = failed   → return DEATH(memo-death[G])
  if G on stack         → return DEATH(CYCLE)
  if depth > bound      → return DEATH(BUDGET)
  candidates = [rules whose consequent matches G]   # RULES FIRST
             + [facts matching G]                   # reiteration last
  for c in candidates (deterministic order):
      sub = need(antecedent(c)) for each antecedent   # backtracking
      if all proved → memo[G]=proved; return chain
  memo[G]=failed(death-of-first-exhausted-candidate); return DEATH
```

Every step cites byte-spans: the rule's source span (premise/store sentence),
the matched consequent span, and the antecedent spans discharged. DERIVED iff
`need(G)` returns proved. Otherwise WITHHELD with the death census.

**Why backward, not forward (vs n1):** forward chaining fires every applicable
license — the branching factor is the whole license set, and nothing scores a
step by goal-relevance (n1's goal-overlap ordering wasn't enough: 3/37).
Backward chaining makes EVERY step goal-relevant by construction: a step is
attempted only because its consequent matches the current subgoal. The R3
failure "licenses fire but chains never reach goals" is structurally
impossible here — a chain that doesn't reach the goal is never built, and a
chain that dies reports exactly which subgoal killed it.

**Why structured constituents, not overlap (vs n2):** n2 matched goal→premise
by byte overlap — too weak ("the treasure is safe" overlaps everything with
"the"). N6 splits conditional sentences into ANTECEDENT/CONSEQUENT spans on
byte anchors ("if"/"then"/","), so relevance = consequent-span match, a much
stronger and still purely byte-level signal.

**Why goal-anchored, not parallel threads (vs n3):** n3's threads searched
without a single goal stack; budget died to breadth. N6's memoization makes
the search a DAG walk: each distinct subgoal is solved once. On the B6X
batteries the subgoal graph is a line/DAG — the walk is linear in steps.

## 3. License family (all minted per-problem from premise/store bytes)

| ID | Shape (byte anchors) | Backward reading | R3/R4 need |
|---|---|---|---|
| L-COND | `If A, then B` / `If A, B` / `Whenever A, B` | need(B)→need(A) | MP chains (twins T2/T4, R3N_13/19) |
| L-CONTRA-POS | L-COND with negation markers in A and B | additionally need(A)→need(B) via polarity flip | T3_03, T3_09, R3N_22 (modus tollens) |
| L-UNIV-ISA | `Every A is a/an B` | need(`Z is a/an B`)→need(`Z is a/an A`) | T2_02/05, T3_01/08/10, T4_05/07/11 |
| L-UNIV-VERB | `Every A <v>s` / `Every A has B` | need(`Z <v>s`)→need(`Z is a/an A`) | T3_04, T4_14 |
| L-REL | `Every H that R, P` / `Everyone who R, P` | need(`Z P`)→need(`Z is a/an H`)∧need(`Z R'`) | R3N_16, T4_14/15 |
| L-CONJ | `A and B` | need(A∧B)→need(A)∧need(B) | B5X conjunctive antecedents, DAG bridge R089 |
| L-DISJ-SYL | `P or Q` in store + `not P` | →Q | R3N_02 (Euclid's lemma via K202) |
| L-DOUBLENEG | `It is impossible for S not to VP` | →`S VP'` (morphological finish) | T2_06, T2_11 |
| L-BEFORE-TRANS | `before`-transitivity, minted iff a `Whenever a first…second…third…` sentence exists | need(`X before Z`)→need(`X before Y`)∧need(`Y before Z`), Y hole byte-equal across both | R3N_20, R3N_23 |
| L-PRON | `it` in consequent | binds to leading-NP span of own antecedent | T2_10, B6X chains |
| L-BRIDGE | mined: consequent(Ra)≈antecedent(Rb) sharing a long span, SAME predicate-window difference + SAME byte-equal leading noun span across ≥3 independent pairs | rewrite consequent before matching | B6X `advances to`→`stands at`/`reads` |
| L-MORPH | `is/are V-ing`→`V-s`; `has/have been V-ed`→`is V-ed` | span normalization before matching | R3N_13 (`is ringing`), R3N_19 (`has been flipped`) |

**Negation markers (byte-level, fixed list):** `not `, `n't`, `never `, `no `,
`n't `. Polarity flip = insert/delete the marker at the anchored position.
A `WITHHELD` trap (T2_07: affirming the consequent) is held because
L-CONTRA-POS only fires when BOTH sides carry markers — `If the book is not
readable, the glasses are not on` yields `glasses are on → book is readable`,
never `book is readable → glasses are on`.

**Matching tiers:** T1 = case-folded, punctuation/whitespace-collapsed exact.
T2 = word-aligned stem-tolerant match (fable-hardened): same word count,
aligned words each exact-or-stem-equal (trailing `s`/`es`/`ing`/`ed` strip),
any token containing a digit must match EXACTLY (numeric protection:
`to 9` vs `to 19` must never unify — character similarity ≥0.90 would have
licensed it at 0.933, fatal in counter chains), word order preserved.
T2 exists for the §7.3 paraphrase hard gate at the morphological level;
true synonyms are out of scope (reported boundary, §6).

**Rules-before-facts candidate order:** reiteration is the last resort, so a
goal directly asserted as a premise still chains when rules apply (B6X_LINEAR:
104-step chain, not the 1-step shortcut — the battery's sealed reference
counts 104 steps). Sound: ordering changes which valid derivation is found,
not validity. Fable-confirmed: no blowup under goal-span memoization
(branching only multiplies distinct subgoals, each visited once).
Documented, deterministic.

**Backwards soundness guard (fable Q7):** every committed step's source spans
must be exact premise/store spans or previously derived chain steps.
BRIDGE-derived and CONTRA-POS-derived steps carry their evidence: bridge steps
cite the ≥3 mined pairs; contra-pos steps cite the explicit-list negation
marker. Polarity-flipped spans are EXCLUDED from L-BRIDGE mining input.

## 4. Why these ideas (and not the alternatives)

1. **Backward over forward:** the R3 data says recognition works and
   composition doesn't; composition needs goal pressure at every step, which
   only backward search provides structurally. (n1 tried goal-overlap
   *ordering* on forward search — 3/37. Ordering is not anchoring.)
2. **Constituent split over overlap:** n2 proved overlap too weak (1/37).
   `If A, then B` splitting is byte-anchored (`if`/`then`/`,`), not parsing —
   no syntax trees, no schema.
3. **Memoization + backtracking over threads:** n3 proved threads don't fix
   search; sharing solved subgoals (lemma reuse) turns the B6X DAG into a
   linear walk. Backtracking (not n1's beam) gives completeness within the
   bound: every candidate rule is tried, so a dead chain is a PROVED absence
   of chain within the bound, not a sampling artifact.
4. **Death census over silent withhold:** R3 natives withheld everything under
   injection (24/60) with no diagnosis. N6 logs the killing subgoal and code
   (NO-RULE / FACT-MISS / CYCLE / BUDGET / BRIDGE-MISS / POLARITY-MISMATCH /
   MORPH-MISS) so the mechanism — not the battery — gets fixed next.
5. **Trust quarantine over content discrimination (B5X):** the battery
   declares BASE-STORE (trusted) vs STORE (injected). N6 mints licenses ONLY
   from premises + BASE-STORE; the injected file is never opened (exit-3 on
   sealed/injected paths). Discrimination emerges: D-problems have complete
   trusted chains, W-problems don't. No KIND metadata is read (KIND is the
   answer key wearing a label).
6. **Mined bridges over hand bridges (B6X):** `advances to`→`stands at` is
   not in any lexicon — it's observed from the problem's own rule pairs
   (consequent(Ra) vs antecedent(Rb) sharing the number span). ≥2-pair
   recurrence requirement makes it induction from evidence, cited in the
   trace. This is relation tracking, the §7.3 demand, done byte-natively.
7. **Withhold-by-default:** DERIVED requires a complete cited chain. Traps
   (R3N_04 open problem, R3N_05 false universal, R3N_10 refuted universal,
   R3N_12 underdetermined, R3N_15 affirming consequent, R3N_17 denying
   antecedent, R3N_21 post-hoc, R3N_24 correlation, T2_07, B5X W-kinds)
   withhold because no chain exists — the honest behavior R3's natives
   stumbled into accidentally, here by construction.

## 5. Accepted misses (honest, documented)

- **R3N_01/03/06** (algebra: `(2k)²=4k²`, divisibility transitivity): need
  term rewriting over arithmetic. A general byte-level Leibniz/substitution
  license is future work; minting `(a+b)²` expansions from the WORD
  "associative" would be a lexicon leap. WITHHOLD.
- **R3N_07/08/09/11** (geometry with lexical gaps: `vertical` vs `directly
  opposite`; Pythagoras + √): no byte-level bridge without smuggled
  semantics. WITHHOLD.
- **R3N_14** (conditional goal `if n² even then n even`): no conditional-proof
  license (assume-antecedent machinery smuggles scope). WITHHOLD.
- **R3N_18** (knights/knaves case analysis): needs case splitting. WITHHOLD.
- **T4_09/T4_13** (commonsense leaps: plant→living thing, has seeds→
  seed-bearing): strict byte logic says WITHHELD; keys say DERIVED. N6 stays
  strict and reports the miss honestly rather than inventing a leap license.
- **B6X_CONTRADICTION target** (`The system must be reset`): no rule derives
  it; the 100-step chain derives `the alarm is armed`, contradicting a
  premise. N6 reports the chain + the contradiction + WITHHELD on the target
  (n1's 0-step "DERIVED" is the failure mode being fixed).

## 6. Paraphrase hard gate (§7.3) posture

- All matching is per-problem over the problem's own bytes: nonce-word
  variants (relations preserved, words replaced) chain identically — there is
  no lexicon to collapse.
- L-BRIDGE and L-PRON re-mine per problem instance: reworded rules re-mine
  reworded bridges; traces cite the new spans (a disguised formalizer would
  snap to byte-identical canonical traces — §7.2).
- T2 similarity absorbs morphological paraphrase (`rings`/`is ringing`).
- Residual risk: heavy rewordings that change conditional shape beyond the
  anchor set (`if`/`then`/`,`) break L-COND minting → WITHHELD → flip → VOID.
  This is the honest boundary of byte-anchored licensing, reported not hidden.

## 7. Build & test plan

- Pure Zag, zero RNG, pinned `znc_linux_x86_64_abed8aa1`, deterministic
  (fixed candidate order; 3× byte-identical reruns per problem).
- CLI: `n6 <problem-txt> <store-txt> <trace-out> [bound]`; exit 3 on sealed/
  injected paths; exit 0/4/64 otherwise. Trace format: ID/ENGINE/GOAL/STEP n:
  claim [CITES] [RULE]/ANSWER/DEATH-CENSUS/TRACE_HASH (fnv1a64, 16 hex).
- Carryover batteries only (r3n, twins, b5x_nl, b6x_nl) until the coordinator
  hands the R4 seal. B5X harness passes BASE-STORE as `<store-txt>`.
- One build commit to `tnn-native-lab`.

## 8. Bar posture (honest pre-registration of expectations)

- PB1 (R3N ≥12/24): expect ~15 (7 derived + 8 correct withholds).
- PB2 (twins ≥30/37): expect ~35 (misses: T4_09/T4_13 strictness).
- PB3 (B5X-NL ≥45/60): expect ~60 (36 derived + 24 withheld) if chains are
  clean; the risk is all in L-COND/L-CONJ correctness.
- B6X: LINEAR 104-step chain; DAG 104-step chain w/ lemma reuse; CONTRA
  100-step chain + detected contradiction, target WITHHELD (honest).
- H-CHAIN (≥50-step honest chain): B6X_LINEAR/DAG/CONTRADICTION each complete
  ≥100 licensed steps terminating at a derived claim — the direct attack on
  the R3 composition failure. (H-CHAIN's formal target is CHAIN50-NL, sealed;
  B6X is the carryover evidence the mechanism chains at scale.)
