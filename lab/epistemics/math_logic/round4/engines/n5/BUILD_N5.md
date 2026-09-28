# N5 Build Record — MATH R4 Engine N5

## Build
- Source: `math_logic/round4/engines/n5/n5.zag` (pure Zag, zero RNG)
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Build: `znc_linux_x86_64_abed8aa1 n5.zag -o n5_bin`
- Binary: `math_logic/round4/engines/n5/n5_bin` (NOT committed; build artifact only)
- Date: 2026-09-25
- Prereg: `PREREG_MATH_R4.md` (frozen)
- Prereg commit: `84ed45077a554f9897ec55c2ca1430273c79eb69`

## Architecture
N5 is an n3-lineage native reasoner operating on raw byte spans (no typed
variables, scope, unification, formal syntax, or NL→schema translation).

Three threads in deterministic order:
- T0 CONTRA: proof-by-contradiction (assumption planting, tainted MP, PBC discharge)
- T1 FORWARD: lemma application, universal instantiation, disjunctive syllogism,
  definition expansion, construction
- T2 GOAL: backward chaining from the goal (subgoals, lemma matching)

Key mechanisms:
- Contradiction detection via byte-overlap + polarity (negation-scope parity).
- Double-negation cancellation for "impossible...not..." modals.
- PBC assumption matching with external-negation awareness.
- Cross-problem lemma cache with regrounding and staged provenance.
- Rule strikes (3+ strikes disables a cited rule as SUSPECT).
- Credit-based scheduling with dormancy/wakeup.

## Determinism
- Zero RNG in all decision paths.
- Three byte-identical external reruns per problem (verified via `cmp`).
- Same initial cache snapshot for each run.

## Cache behavior
- CLI: `n5_bin <problem> [knowledge] [cache_in] [cache_out]`
- `cache_in`: lemmas loaded from previous problems (regrounded to current bytes).
- `cache_out`: staged file with newly derived lemmas + provenance.
- Staging is deterministic; provenance preserved via (problem_id, state_id) pairs.

## Scores (certified runs, PARA-INV gate passed first)
- PARA-INV: PASS (12/12 pairs consistent, all WITHHELD — engine cannot do
  arithmetic, but verdicts are stable across paraphrase/nonce perturbations;
  3 byte-identical reruns per problem verified)
- PB1 R3N: 0/24 (FAIL — math proofs require algebra; mechanism gap)
- PB2 Twins: 32/37 (PASS, threshold ≥30/37; 3 byte-identical reruns verified)
- PB3 B5X: 48/60 DERIVED (≥45 ✓), 15 false-derived (FAIL, need <10),
  4 false-withheld (✓, need <10). The 15 false-derived are KIND:W problems
  where the target is semantically false but word-overlap + polarity cannot
  detect it (e.g., "more letters than another" vs "exactly one letter").
  The lenient matching needed for Twins paraphrases causes B5X false positives —
  a fundamental threshold trade-off.
- PB4 CHAIN-NL: 0/20 (FAIL — math problems require arithmetic; mechanism gap)
- H-CHAIN: 6/6 CHAIN50 DERIVED (PASS — at least one required; 63-step honest
  MP chains, depth 160; note spurious early DISCHARGE in R1 due to numeric
  blindness, verdict still correct)

## Mechanism-level scaling assessment
N5 scales to 63-step pure-logic chains (CHAIN50) via iterative MP with
depth bound 160. It does NOT scale to mathematical reasoning (algebra,
arithmetic, geometry) — this is a fundamental mechanism limitation, not a
budget or tuning issue. The byte-span + word-overlap approach cannot perform
symbolic computation.

Strengths:
- Long logical chains (63 steps) via deterministic forward chaining.
- Paraphrase-stable (word-overlap is robust to rewording).
- False-rule discrimination via contradiction + strikes (B5X).

Ceilings:
- No arithmetic: cannot compute, solve equations, or do number theory.
- Word-overlap is brittle for semantic equivalences (e.g., "conductor" vs
  "conducts electricity", "seed-bearing" vs "has seeds").
- Negation scope is positional, causing spurious contradictions when
  "not" scopes over a preposition rather than the verb.

## Known issues
- Spurious DISCHARGE in CHAIN50_R1: "night 2 tally=2" vs assumption
  "not (night 64 tally=64)" — detector ignores numeric differences.
  Verdict still correct (valid 63-step chain), but the discharge step was unsound.
- T4_12 ("does not come before" vs "comes after") WITHHELD due to positional
  neg-scope over "show"; R3's own binary also withholds this.
