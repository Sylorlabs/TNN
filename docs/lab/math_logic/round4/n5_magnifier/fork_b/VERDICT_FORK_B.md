# FORK B verdict: can native perception do substitution?

Micah order 2026-09-26 ~00:07 PDT. Fork B coordinator report.
Date: 2026-09-26. Sealed R4 evidence untouched; all work in `~/workspace/n5_fork_b/`.

## The question

Micah's alternative hypothesis: TNN should "just see it natively within its bytes" —
no explicit sub-span addressing machinery, no zoom operation. Fork B tests exactly
that: enrich the chainer's native perception *within* spans, with a hard constraint —
**no explicit sub-span addressing, no zoom operation, no new rewrite license with
bind/zoom steps. Perception enrichment only.**

## What was built

`n5b.zag` = frozen `n5.zag` (SHA-256
`c2c105d8d14799fa0655b80f4391a1e083ce47d07d9e98d3f3ed922e63817598`) plus two
changes, and nothing else (full diff: 128 lines, audited below):

1. **Sub-word fragment perception** (the experiment): `n5_collect` /
   `n5_collect_neg` now run a second pass that hashes every contiguous character
   fragment of each word (lengths 2–4) through the same stem-hash pipeline into
   the *same unordered word set* used by all matching. Perception records THAT a
   fragment occurs, never WHERE — no positions are kept, no span is addressed,
   no zoom step exists. Two passes (all whole words first, fragments only fill
   remaining capacity) keep whole-word behavior identical to baseline.
   `n3_propose` and all 12 licenses are byte-untouched.
2. **Goal-parser fix** (the F2 crash fix, same as sibling fork): `n5_goal_form`
   recognizes `prove that` / `prove` / `find` / `determine` / `what is|are|was` /
   `is` / `was` / `does` goal forms; the goal line is skipped as a premise via
   its recorded line offset; answer-seeking goals (`find`/`determine`/measure)
   that withhold print an explicit REASON line instead of crashing.

Constraint audit: `diff n5.zag n5b.zag` shows no new license, no occurrence
positions, no binding representation, no span constructor. The white-box trace
check (below) confirms it held at runtime.

## Discriminating tests (all 2× byte-identical)

| test | setup | fork B | baseline n5 |
|---|---|---|---|
| T_PERC (perception demo) | "The clock stopped." + "If the lock stopped, then the clock is broken." → "the clock is broken." | **DERIVED** (R1 L5 fires: `lock` perceived inside `clock`) | WITHHELD (budget-exhausted) |
| SUBST_B1 (pre-computed conditional) | n=2k + "If n=2k, then n^4=16k^4." | DERIVED (no regression) | DERIVED |
| SUBST_MIN1 | n=2k → n^4=16k^4 | WITHHELD | WITHHELD |
| SUBST_B3 (general Leibniz schema) | n=2k + general substitution schema | WITHHELD | WITHHELD |
| SUBST_NOVEL_X | x=3y + schema → x^2=9y^2 | WITHHELD | WITHHELD |
| SUBST_NOVEL_M | m=4n + schema → m^3=64n^3 | WITHHELD | WITHHELD |

T_PERC is the control that proves the enrichment is real and active: the same
engine, the same 12 licenses — the only difference is what the engine *sees*.
Baseline cannot fire the conditional (`lock` is not a whole word in "The clock
stopped."); the fork fires it in round 1 because `lock` is perceived as a
character-fragment inside `clock`. Native sub-span perception works.

## The clean negative: which step fails, at the mechanism level

Substitution needs three steps. Fork B isolates them:

1. **LOCATE** — *works natively.* At the word level N5's tokenizer already splits
   `n^4` into `n`,`4`; with fragment perception even glued occurrences
   (`lock`⊂`clock`) are seen. T_PERC proves occurrence perception fires rules.
2. **BIND** — *no mechanism.* The equality `n=2k` is a flat byte span. No license
   interprets an equality as a substitution binding; fragment perception adds
   occurrence fragments, not role structure — there is no LHS/RHS, no
   term/value distinction, nothing for `n→2k` to be *as*. In the SUBST_B3 trace
   the schema is expanded verbatim (L3) and then sits inert for the remaining
   rounds; the equality premise is never consumed by any license in any round.
3. **SYNTHESIZE** — *no mechanism.* All 12 licenses emit only byte spans that
   already exist contiguously in the ledger (or L9's fixed concatenation of two
   such spans). Mechanical proof: `verbatim_check.py` parses every trace's
   LEDGER and verifies each derived state's bytes occur verbatim in an earlier
   state (L9 concatenations checked as two earlier sub-spans). Result across
   all discriminating traces: **0 violations** — zero novel spans were ever
   emitted, in any run, by either engine.

So: perception can be enriched until the engine sees every byte-fragment, and
it still cannot do substitution, because *seeing* is not *rewriting*. The
general Leibniz schema is perceived perfectly well — and then nothing can act
on it, because acting on it requires constructing a span that exists nowhere
in the ledger (`(2k)^4`), and no code path constructs spans. **The magnifying
glass is necessary.** This is the successful clean negative the experiment was
designed to produce.

On (b): there is nothing to generalize — the fork derives substitution
instances *only* when the consequent is pre-computed in the input (SUBST_B1);
novel variable names and exponents (X, M) withhold identically. No pattern was
learned; no pattern could be.

## Collateral finding: fragment perception makes the engine more gullible

The enrichment is not merely inert for substitution — it is actively harmful
to judgment. R3N_04 (twin-prime conjecture — the battery's gullibility trap,
sealed WITHHELD):

- Baseline: WITHHELD, zero PBC firings (correct).
- Fork B: **DERIVED** — a false proof of an open problem, via
  `R2 T0 CONTRA L1 contra-expand ... PBC-FIRED contra=[S7]`, discharging the
  contra-assumption against S7 (Euclid's postulates, K004 — topically unrelated).

Mechanism: the contradiction detector's entry gate is `sh>=2` shared
word-hashes between the two spans (`n5_contra_state`). Whole-word perception
saw fewer than 2 shared hashes and correctly returned 0. Fragment perception
manufactured shared hashes out of sub-word collisions — `in` ⊂ `infinitely` /
`indefinitely` / `line`, `er` ⊂ `there` / `center`, and the like — crossing the
gate and letting a downstream path (polarity-flip or quantity-mismatch with
subject alignment) fire a proof-by-contradiction discharge. Looser perception =
more perceived contradictions = a more gullible prover. This is further
evidence against the "just see more within the bytes" hypothesis: even the
locate step, when enriched, degrades the engine's epistemics rather than
enabling new valid inferences.

## Battery numbers (honest)

Parser crashes: **0** (was 9 — the F2 fix, shared with the sibling fork). All
24 R3N + 20 CHAIN-NL runs completed rc=0, 2× byte-identical per problem
(cmp-verified; zero NONDET lines in RUNLOG).

Scores vs sealed keys (`score_fork_b.py`, sealed read-only):

- **PB1 (R3N): 9/24** correct — bar ≥12/24: MISS. False-derived: 1 (R3N_04, the
  twin-prime gullibility trap — see collateral finding). False-withheld: 14.
- **PB4 (CHAIN-NL): 0/20** — bar ≥12/20: MISS. False-derived: 0.
  False-withheld: 20.

Baseline for comparison: PB1 10/24 (with 9 crashes), PB4 0/20. The fork is one
point *below* baseline on PB1, entirely because of the R3N_04 false derivation
the fragment perception introduced; the parser fix converted 9 crashes into 9
scored runs, none of which derived correctly. On PB4 the fork matches baseline
exactly (0/20 — N5 cannot do multi-step chained derivation with or without
fragments).

Neither bar is met, and that is the point of this fork: it is a mechanism
experiment, not a capability bid. The perception enrichment demonstrably
activates (T_PERC), demonstrably cannot synthesize substitution
(zero novel spans in 88 traces), and demonstrably degrades judgment at the
margin (R3N_04). A clean negative with a named failure: **bind and synthesize
have no mechanism; locate works and still isn't enough.**

## Reproducibility

- Source `n5b.zag` SHA-256: (in RUNLOG.txt)
- Binary `n5b_bin` SHA-256: (in RUNLOG.txt)
- Knowledge store: `e8846333ff4a97a4224d6d262aef1cb021ea09e24b39cb1ecbfb4692f49c3c1d` (R4, matches sealed manifest)
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Runs: `evidence/runs/pb1|pb4/` — 88 outputs, r1/r2 cmp-identical
- `verbatim_check.py` — the no-synthesis mechanical proof
- `score_fork_b.py` — scorer vs sealed keys (read-only)
- Build note: this znc build resolves `@import` relative to the *source file's*
  directory (not CWD as an older AGENTS.md note claims); the fork builds from
  `src/math_logic/round4/engines/n5/n5b.zag` with `src/deliberation_depth`
  symlinked to the lab tree.
