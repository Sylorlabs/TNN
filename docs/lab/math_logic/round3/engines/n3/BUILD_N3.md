# BUILD_N3 — N3 ONEBRAIN-NATIVE build record

Date: 2026-09-25. Engine: `n3.zag` (pure Zag, zero RNG), built with the pinned
compiler `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`n3.zag --no-zagd --no-analyze --no-foreground-cache -o n3_bin`), CWD =
`math_logic/round3/engines/n3`.

Binary SHA-256: `c02f37eaba8bcc1e8d97117ad2e1bae374b65495a978412ee1dcc9d062201123`
(binary NOT committed; build artifact only).

## Knowledge-store pin

Pinned to the R3 NL knowledge store that landed during this build:
`math_logic/round3/batteries/knowledge/KNOWLEDGE_STORE_NL.md`
(frozen raw-NL rendering of KNOWLEDGE_STORE.md; all R3N items cite its IDs).

- Coordinator-cited commit: `db913da907d0` on tnn-native-lab.
- Local file SHA-256: `910ea9da0989e113587a3856583ba1ec1ea8b4f59258ab3374f1b17b9220084a`
- NOTE: the local working tree is not a git checkout, so the cited commit
  hash could not be independently verified here; the pin is recorded as cited
  plus the file hash above. No fallback store was used (the NL store exists).
- Default knowledge path (relative to engine CWD):
  `../../batteries/knowledge/KNOWLEDGE_STORE_NL.md`.

## Mechanism (as built)

One shared append-only ledger of raw text states
`(id, bytes, source, depth, status live|defeated)`; sources:
input / cite / assume / prop / subgoal / pbc. Four fixed threads in
deterministic order T-CONTRA(0), T-CONSTRUCT(1), T-LEMMA(2), T-GOAL(3);
each live thread proposes at most one step per round (max 25 rounds =
100 thread-steps). Every proposal is contradiction-checked against the
entire ledger BEFORE appending (byte-overlap ≥2 shared content words +
negation-polarity flip; see below). Outcomes: append (strikes reset) /
discharge (contradicts only assumptions → assumptions + tainted states
defeated, proposal appended) / refuse (strike++). Refused and appended
(license,premise) pairs are never re-proposed; defeated states are never
cited. 3 consecutive refusals → strategy KILLED (logged). T-CONTRA's
refused tainted CONSEQUENCE may fire PBC (assumption + taint defeated,
goal skeleton appended → DERIVE). DERIVE iff a thread appends a state
byte-equal to the goal skeleton (case-insensitive, trimmed). Otherwise
WITHHOLD (all killed / proposal-free round / budget exhausted).

Nine licenses: contra-assume (L0), contra-expand (L1), contra-apply (L2),
construct-expand (L3), construct-iff (L4), lemma-apply (L5),
goal-defsplice (L6), goal-lemmasub (L7), goal-close (L8).
Definition shape = `HEAD: body` byte split; conditional shape =
`if <C>, then <Q>` / `if <C> then <Q>` / `if <C>, <Q>` byte splits.
Contradiction = ≥2 shared distinct content words (len≥3, non-stop,
non-negation-marker) with a flipped negation-scope word. Skip spans:
goal span inside the input (the question is not a claim); definition
head spans (the definiendum is a label, not a claim); conditional
head/antecedent/consequent spans (a conditional asserts none of them).
Anti-bridge: matching is case-insensitive byte equality of word spans
and substrings only; no variables, no scope, no unification, no
NL→schema mapping. Fixed literal bytes appear only in the L0 template
`"It is not the case that "`.

## Corrections made during testing (mechanism-level reasons)

1. **Negation markers excluded from overlap vocabulary.** Markers
   (`not`, `no`, …) are operators: they set polarity via the neg-scope
   sets but must not count as shared content. Otherwise `not` + one
   stray shared word (e.g. `2`) fabricated contradictions (found:
   assumption vs K004 Euclid's postulates via `not`+`2`).
2. **Content words must be ≥3 bytes for overlap.** Numbers and
   single-letter variables (`2`, `m`, `x`) are too ambiguous for
   byte-overlap; they fabricated a contradiction between P01's
   assumption and K109 (`m^2`). Genuine overlaps (P02 vs K206) are
   unaffected.
3. **No self-licensing by conditionals.** `n3_match_conj` excluded the
   conditional's own state and all other conditional-shaped states
   (their conditional spans are unasserted), and L8's establisher may
   not be the conditional itself. Found: K001 and K202 each "applied"
   to themselves, appending their own consequents unconditionally.
4. **PBC restricted to tainted consequences** (`src==prop`), never the
   assumption's own refusal. Firing PBC on a refused assumption would
   prove the goal from a mere failure to assume it — unsound.
5. znc codegen probe: `let s:*T=c.*.s; s.*.field` (local pointer loaded
   from a struct) verified correct on the pinned toolchain, so the
   N3C-context pattern is safe here.

## Smoke results (public problems only; sealed battery never touched)

Sealed guard: any path containing `sealed` → exit 3 before any read
(verified on problem path and knowledge path).

| problem | verdict | trace |
|---|---|---|
| MECH1 (pigeonhole, dev-only) | DERIVED | T-LEMMA applies K204, antecedent matched in input, contradicts only the assumption → discharge → goal appended |
| P01 (√2 irrational) | WITHHELD (DISCHARGE, BUDGET-EXHAUSTED) | assumption appended; T-GOAL's K105 splice discharged it (`sqrt2 is not rational` appended); engine cannot complete the proof — honest withhold |
| P02 (infinitely many 4k+3 primes) | WITHHELD (BUDGET-EXHAUSTED) | assumption refused — contradicts K206 (genuine: it is K206's negation) among noisier overlaps; T-CONTRA route correctly closed |
| P03 (n^5−n divisible by 30) | WITHHELD (BUDGET-EXHAUSTED) | assumption appended; T-CONSTRUCT expands definitions; no thread bridges to the goal — honest withhold |

Determinism: in-process 3× rerun per invocation (exit 5 on divergence);
plus 3 separate process invocations per problem — all byte-identical.

## Commit set

`math_logic/round3/engines/n3/n3.zag`, `math_logic/round3/engines/n3/BUILD_N3.md`.
Excluded: `n3_bin`, `.zagd.semantic-ready`, `.zag-cache/`.
Committed via `~/workspace/commit_racefree.py` with TMPDIR=`~/workspace/tmp_commit`.
