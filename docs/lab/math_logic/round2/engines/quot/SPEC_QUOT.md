# ARCH D — QUOT: admissible-support quotient

(Grok-4.7 arm, MATH R2 ideas round, 2026-09-24. Raw model output:
[ideas/grok_raw.md](grok_raw.md). This doc is a build-ready rewrite in our own words.)

## One-line summary

QUOT never asks "is ¬H derivable?" like ONE does, and has no referee object
like DUAL/HYB. It runs ONE forward match-and-bind pass to fixpoint, but every
claim carries a **support bitset** (which contingent store items it depends
on). Contradiction is not explosion: derivations that sit inside a conflict
are *tainted* and cannot establish anything, while derivations outside the
conflict remain fully admissible. The commit decision is a pure function of
two subset-minimal tables — a pure function, no agent, no rubric, no scores.

## Structural contrast with the other engines

- vs ONE: ONE treats the store as one theory; once a false rule makes the
  union inconsistent, ONE's "derive ¬H" referee test succeeds for every H and
  ONE withholds on everything. QUOT keeps the tainted derivations in the
  audit (they stay inspectable) but quarantines their *authority*: a support
  bitset that covers a conflict cannot commit any claim. Uncontested atoms
  (clean proofs that never touch the conflict) are derived normally.
- vs DUAL/HYB: there is no R, no directive interface, no scoring rubric, no
  second pass. The answer comes from a fixed function evaluated once at
  fixpoint over two tables (minimal supports, minimal conflicts). If your
  build contains an agent that "decides," you built HYB, not D.
- vs REF-FIRST: the referee does not drive search; there is no search
  guidance at all. The fixpoint is query-independent — one run serves every
  target.
- vs LEARN-FORM: QUOT refuses NL input; it is purely a formal-battery engine.
- vs ARCH E (RESIDUAL): QUOT builds the global forward closure and then
  filters by support; RESIDUAL never builds it and proves only the target.
  QUOT can *commit* on contested atoms via a specificity rule; RESIDUAL
  deliberately cannot.

## 1. Core operation

1. **Load and index.** Load frozen schemas and the frozen store. Sort store
   items by canonical bytes (raw length-prefixed s-expressions; no unicode
   normalization; `eq` args sorted lexicographically). Assign contiguous ids
   `0..n-1` in that order. Each store item carries a frozen header marking it
   `FACT` or `RULE`; a rule has antecedent literals and one head literal.
2. **Classify schemas.** Logical schemas (modus ponens, instantiation,
   equality) contribute NO premise id to a support bitset. Contingent store
   items (facts and domain rules, including any injected false ones) DO.
   There is no ex-falso schema anywhere — contradiction is never an
   inference rule.
3. **Seed the pool.** Each fact `i` becomes a claim: atom bytes, polarity,
   support bitset `{i}`, depth 0, empty schema trace, hot bit clear.
4. **Forward match-and-bind to fixpoint** over a precomputed Herbrand
   universe `U`: every ground term in store ∪ problem, closed under subterms,
   then closed under actually-occurring function symbols, to depth
   `max_term_depth(store ∪ problem) + schema_count`. `U` is a function of
   the input, not a fixed depth-8 constant. Incompleteness beyond `U` is a
   withhold, never a guess. Every new claim's support = bitwise OR of the
   premise supports, OR the contingent rule id if the producing schema
   instance came from one.
5. **Conflict registration.** Whenever the pool holds `P` with support `S1`
   and `¬P` with support `S2`, insert conflict `K = S1 OR S2` into the
   conflict family, then subset-prune the family (drop any member that has
   another member as a subset). Bitsets are `ceil(n/8)` bytes, little-endian.
6. **Taint.** A support `S` is tainted iff some conflict `K ⊆ S`. Taint is
   monotone: once tainted, always tainted. Do NOT delete the claim — keep it
   so later conflicts stay visible. A tainted claim simply cannot establish
   anything (it never appears in a commit, and explosion records are born
   tainted and never count).
7. **Subset pruning of supports.** Per `(atom, polarity)`, keep only
   subset-minimal bitsets, sorted lexicographically as bitset bytes. A
   larger bitset is a worse proof of the same literal and is discarded.
8. **Decide (§4).** At fixpoint, evaluate the commit function once per
   target literal. Emit one audit line: `DERIVED` or `WITHHOLD`, the
   surviving minimal clean supports, and the conflict family. No numeric
   confidence — confidence is non-zero iff `DERIVED`.

Worked trace (penguin/bird/flies — the case ONE collapses on):

- `f0: penguin(tweety)`, `r_tax: penguin(x)→bird(x)`,
  `r_gen: bird(x)→flies(x)`, `r_exc: penguin(x)→¬flies(x)`.
- `flies(tweety)` gets minimal support `{f0, r_tax, r_gen}`;
  `¬flies(tweety)` gets `{f0, r_exc}`. Conflict `K` = their union.
- Each side alone is internally consistent — neither support is a superset
  of `K` by itself. Both are admissible. ONE withholds every atom here;
  QUOT derives `penguin(tweety)` (support `{f0}`, no conflict inside it, no
  admissible derivation of its negation) and uses specificity (§4) to defeat
  `r_gen`: `{penguin}` closes under `r_tax` to `{penguin, bird}` but
  `{bird}` does not close back to `penguin`, so the more specific
  `r_exc` wins. Committed result: `¬flies`. Defeat is per atom — `r_gen`
  stays available for non-penguin birds.

## 2. Data structures

- `StoreItem { id:u32, kind:FACT|RULE, canon:bytes, ante:[atom], head:atom }`
  in one array; index = id.
- `Claim { atom:bytes, pol:0|1, support:bitset, depth:u32,
  trace:vec<(schema_hash:u64, prem:[u32], bind:bytes)> }`.
- Pool index: B-tree `atom_bytes → ClaimSlot`; each slot holds two vectors
  of bitsets (positive / negative), subset-minimal, sorted lex.
- Conflict family: one vector of bitsets, subset-minimal, sorted lex.
- Schema index: B-tree from canonical bytes of the first premise pattern →
  list of schema ids; schemas in a frozen array sorted by canonical bytes
  (schema id = that index).
- Binding: `vec<(var_bytes, term_bytes)>` sorted by `var_bytes`.
- Worklist item:
  `(support_popcount, depth, schema_id, premise_ids_in_schema_order,
  binding_bytes, conclusion_bytes)`, array sorted ascending by that tuple.
  This tuple is the ENTIRE priority: smallest premise set first, then
  shallower, then lower schema id, then lower premise ids, then binding
  bytes.
- Specificity cache: B-tree `(contested_atom_bytes, rule_id) →
  taxonomy_closure_bitset`, filled lazily, frozen once written.

No scores, no confidence field, no referee mailbox, no priority queue beyond
the sorted worklist array.

## 3. Search / control

- Only schema instances whose substituted terms lie in precomputed `U`.
- Per schema, premises are matched left to right; at each premise, candidate
  claims are tried in ascending claim id. Every complete match is pushed —
  no first-match cut.
- Pop worklist index 0. Insert the conclusion only if its atom is new or
  its support is subset-minimal and not already present. On insert:
  subset-prune, update conflicts, enqueue every schema instance the new
  claim can feed.
- Tie-break is the worklist tuple; the key is total, so equal tuples are
  one tuple — do not insert duplicates.
- Termination: finite atoms over finite `U`, finite bitsets, subset pruning.
  A step adding no subset-minimal support and no subset-minimal conflict is
  a no-op. Fixpoint = the first pop that produces only no-ops for a full
  pass over newly inserted claims. No depth cap, no derivation-count cap.
- On fixpoint, run §4 once. QUOT is query-independent: one fixpoint serves
  every target. (Intentional — this is the cost contrast with E.)

## 4. Contradiction handling

Evaluated only at fixpoint, only per *contested* atom (an atom with at least
one clean minimal support on each side). "Clean" = not tainted.

- **Taxonomy rules** (relative to contested atom `A`): every rule whose
  head is neither `A` nor `¬A`.
- **Taxonomy closure** of a ground literal set `G`: forward closure under
  logical schemas, facts, and taxonomy rules only. Contested-head rules are
  off. Cached.
- **Defeat**: support `S_¬` defeats support `S_+` on `A` when the last
  contested-head rule of `S_¬` has ground antecedents `G_¬`, the last of
  `S_+` has `G_+`, the taxonomy closure of `G_¬` contains `G_+`, and the
  converse fails. (The more specific rule's side wins.)
- **Decision for H**:
  - Clean minimal support for `H` exists, every clean minimal support for
    `¬H` is defeated by at least one clean support for `H`, and not vice
    versa → `DERIVED H`.
  - Symmetric case: `DERIVED ¬H` (audit records the negative literal; the
    caller maps to the problem's answer bit).
  - Both sides have an undefeated clean support, or each defeats the other
    → `WITHHOLD` that atom only.
  - Only tainted supports exist, or no support exists → `WITHHOLD` that
    atom only.
- Nothing global is dropped. Tainted claims stay in the audit so the
  conflict is inspectable. Uncontested atoms with a clean support are
  `DERIVED` even while some other atom is withheld.

This avoids ONE's failure mode (a conflict taints the union, so every
`¬H`-test "succeeds," so every answer withholds) and gullibility (a tainted
or defeated support never commits; incomparable clean supports withhold
rather than picking a side).

**Known hole (documented so the prediction stays honest):** specificity
commits a wrong answer when the false rule is the *more specific* one;
symmetric conflicts withhold. QUOT does not "weigh quality" beyond
specificity. A consistent false rule that contradicts nothing is accepted —
nothing deterministic can do otherwise without a score or external oracle.

## 5. Pure-Zag determinism seals

- Id order is lexicographic order of canonical bytes — never hash order,
  never allocation order from a hashmap.
- `FNV-1a-64` is used only as an atom identity and audit checksum: it never
  sorts, never samples, never breaks a tie.
- Bitset subset tests walk bytes from index 0. Worklist sort key is total
  (no residual original-order dependence). Conflicts are exact unions, then
  subset-pruned in lex order of bitset bytes.
- Taxonomy closure uses the same worklist rule with contested-head rules
  removed, so it cannot diverge from the main order.
- No clock, no address-order iteration, no randomized conflict
  minimization. Audit serialization is the shared field order; the trailer
  is `FNV-1a-64` over the audit body. Maps are B-trees keyed by canonical
  bytes; arenas bump ids upward.

Zag toolchain notes (from ~/AGENTS.md): use `[]u8` arenas with explicit
little-endian accessors for all tables (never `as []i32` casts); keep every
slice under 2^25 bytes; explicit `return;` in void fns; `.*` only on
pointer-typed operands.

## 6. Falsifiable prediction

On a KB5-shaped battery (injected rule makes the classical union explosive),
built with two measurable slices:

- **Slice I**: atoms whose clean proofs never meet a conflict (uncontested
  theorems, including trivial restatements of facts).
- **Slice II**: atoms whose two sides are clean and specificity-comparable
  (exception vs. general, as in the penguin trace).

Claim: ONE withholds on 100% of both slices. QUOT commits **0 incorrect**
on Slice I and commits the specificity winner on Slice II, withholding only
where the two antecedent closures are incomparable.

- If QUOT's Slice II accuracy matches DUAL's measured "0 incorrect" on
  specificity-shaped injection, the strong reading of **H1 is false** —
  contradiction tolerance that still answers is not owned by a referee.
- If KB5's contested items are symmetric, QUOT withholds them and H1 stands
  for those items; that split is the measurement, not a rescue.

Secondary (H2, timing): QUOT has no D↔R hop. On the scaling problems where
both round-1 engines emitted 52 derivations, predict wall time ≤ 1.5× ONE
at a committed-claim count equal to ONE's (extra bitset rows allowed, no
extra committed atoms). If time exceeds 2× ONE at equal committed atoms,
the round-1 gap was not the interface and H2's causal story fails for this
design.

**H5**: fails on this battery if QUOT, with no tolerant-referee component,
matches HYB's accuracy — the hybrid's referee was not the necessary part.
