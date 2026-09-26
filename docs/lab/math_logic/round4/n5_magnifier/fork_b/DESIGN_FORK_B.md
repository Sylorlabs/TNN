# FORK B design: native sub-word perception without a magnifying glass

## Hypothesis under test

Micah (2026-09-26): TNN should "just see it natively within its bytes" — no
explicit sub-span addressing machinery, no zoom operation. Fork B implements the
strongest defensible version of that hypothesis inside N5's architecture.

## The enrichment

N5 perceives text through `n5_collect` / `n5_collect_neg`: each state is reduced
to an *unordered set* of stem-hashes (whole words; single letters dropped unless
numeric-leading; stop/negation words filtered). All matching — antecedent
coverage (`n3_match_conj`), goal coverage (`n3_goal_match`), contradiction
detection, definition-expansion keys — works over these sets.

Fork B adds a second pass to both collectors: every word is additionally
perceived through its **contiguous character fragments (lengths 2–4)**, hashed
through the identical stem pipeline into the *same* set. Consequences:

- "Perception records THAT a fragment occurs, never WHERE." Fragments are
  hashed; positions are discarded at emission. There is no way to ask "where in
  the span" or "the k-th occurrence" — the information does not exist.
- Two passes (all whole words first, fragments fill remaining capacity) keep
  whole-word behavior bit-identical to baseline when fragments don't fit.
- `n3_propose` and all 12 licenses are untouched. No new license, no new
  proposal kind, no binding representation, no span constructor.

## Why this is "perception" and not smuggled zoom

| zoom / rewrite machinery | fork B |
|---|---|
| occurrence positions / addressing | none — hashes only |
| bind step (term → value) | none — equality spans stay flat |
| rewrite license / span synthesis | none — `n3_propose` untouched |
| new conclusion shapes | none — all conclusions still verbatim copies |

The `diff n5.zag n5b.zag` (128 lines) is the complete audit surface, and
`verbatim_check.py` verifies at runtime that zero novel spans were emitted in
any trace.

## The parser fix (F2, shared with sibling fork)

`n5_goal_form` recognizes the R3N battery's real question forms (`prove that` /
`prove` / `find` / `determine` / `what is|are|was` / `is` / `was` / `does`),
records the goal line offset so the goal line is never also a premise, and marks
answer-seeking goals (`find`/`determine`/measure-of/length-of). Answer-seeking
goals that withhold print `REASON: answer-seeking goal; numeric or enumerative
answers are outside n5's operation set` — withhold-with-reason, never rc=-2.

## Build note

This znc build resolves `@import` relative to the **source file's directory**
(an older AGENTS.md note says CWD; empirically false for
`znc_linux_x86_64_abed8aa1`). The fork builds from
`src/math_logic/round4/engines/n5/n5b.zag` with `src/deliberation_depth`
symlinked to the lab tree, so `../../../../deliberation_depth/harness/...`
resolves. CWD for runs: `math_logic/round4/engines/n5` (recovery protocol).

## Cost of the enrichment

Fragment hashing roughly doubles word-collection work; R3N problems run in
~5–20 s each (well under the 180 s recovery timeout). No timeouts hit in
PB1/PB4.

## Result pointer

The enrichment demonstrably works (T_PERC: baseline WITHHELD → fork DERIVED via
a round-1 L5 firing on `lock`⊂`clock`) and demonstrably does not yield
substitution (SUBST_B3 + novel instances all WITHHELD; zero novel spans
emitted). See VERDICT_FORK_B.md for the locate/bind/synthesize decomposition.
