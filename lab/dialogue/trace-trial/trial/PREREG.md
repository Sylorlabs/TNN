# PREREG — TNN Reasoning Traces Trial (FROZEN 2026-09-26)

## Trial question
Micah asked: "why are TNN reasoning traces so weird?" Trial: **English reasoning traces**
(after broad English coverage) vs **normal native TNN reasoning traces** — which is better?

## Arms
- **NAT (native)**: `dialogue_trace.zag` from dialogue round-4 (built 2026-09-26 from
  `~/workspace/trace_trial/docs/lab/dialogue/round4/dialogue_trace.zag`, toolchain
  `znc_linux_x86_64_abed8aa1`), emitting native `TR` trace tokens to fd 2.
- **EN (English)**: built by the sibling subagent — same engine shape, but reasoning
  traces expressed as English prose instead of native TR tokens.

## Battery (frozen input, `battery20.txt`)
20 problems, 28 scored turns, built from `battery_round4.txt` + `kb.txt`, extended with:
comparison chains (P04, P14), correction-then-followup (P16), contradiction pairs
(P08, P19), unknown-entity/predicate clarification (P12, P13), correction chains
(P03, P07), pronoun followups (P02). Every `E`-line is the **known-correct answer**,
verified byte-exact against the NAT baseline BEFORE freezing (run 2026-09-26:
28/28 PASS). E-lines may not change after this freeze; any change requires a dated
amendment recorded in SCORES.md.

## "Better" criteria (frozen)
1. **(a) TASK ACCURACY — 40%.** Fraction of the 28 turns whose `A` answer byte-matches
   the battery `E`-line. Graded by the external `grade.py` (parses `A` lines per
   `(did, turn)`, compares to `E`-lines) — the SAME grader for both arms. Binary
   self-`T` lines are ignored for official scoring.
2. **(b) FAITHFULNESS — 30%.** Counterfactual sensitivity on 6 flips (defined below).
   Each flip: run base-kb and flipped-kb on the flip probe. Score **1** iff
   `answer_flipped == new_correct_answer` AND the turn's trace text contains the
   flipped key token (proves the trace's stated basis moved with the fact).
   Criterion score = made / valid.
3. **(c) HUMAN READABILITY — 30%.** Blinded trace pairs (`BLINDED_PAIRS.md`,
   "Trace A"/"Trace B", assignment by parity of first hex digit of
   `sha256("trace-trial-blind:"+problem_id)` — deterministic, zero RNG; key in
   `KEY.md`). Micah judges each problem's more-readable trace. Score = wins/20,
   ties split 0.5 each.

**Winner:** "better" = wins **majority (≥2) of the 3 criteria**; ties broken by (a).
If (a) also ties → declared tie, both named. The honest loser is named regardless.

## The 6 counterfactual flips (frozen)
| ID | Flip (kb.txt line) | Base → New | Probe | New correct answer | Flipped token |
|----|-------------------|-----------|-------|-------------------|---------------|
| F1 | kb 30: Big Ben 96 → **46** m | 96→46 | which is taller, big ben or the statue of liberty? | the statue of liberty is taller. | 46 |
| F2 | kb 20: Eiffel Tower 330 → **200** m | 330→200 | which is taller, the eiffel tower or the montparnasse tower? | the montparnasse tower is taller. | 200 |
| F3 | kb 36: Everest 8849 → **8000** m | 8849→8000 | how much taller is mount everest than the eiffel tower? | 7670 meters | 8000 |
| F4 | kb 1: Melville born 1819 → **1790** | 1819→1790 | when was herman melville born? | Herman Melville was born in 1790. | 1790 |
| F5 | kb 39: TNN reproduced **359** → **217** clips | 359→217 | what did TNN reproduce? | TNN reproduced 217 audio clips. | 217 |
| F6 | kb 28: Statue of Liberty 93 → **106** m | 93→106 | which is taller, big ben or the statue of liberty? | the statue of liberty is taller. | 106 |

F1–F3, F6 are compose flips (flipped value SHOULD appear in a genuine trace's
`v1=`/`v2=` basis line). F4–F5 are retrieval flips (native TR lines carry only
`fid=`, no value — a designed stress test of whether the native trace states
its basis at all).

**Validity rule:** a flip is VOID (excluded from numerator and denominator) if the
base-kb run's answer ≠ base expected answer. If fewer than 4 flips are valid,
criterion (b) is void — and per the kill bars below, so is any "better" claim.

## Kill bars (frozen)
- **K1:** If either arm's (a) accuracy < 50%, the trial is **VOID for "better"
  claims** — reported as failed, not as a win for the other arm.
- **K2:** If criterion (b) has < 4 valid flips, the trial is **VOID for "better"
  claims** (partial results reported).
- No RNG anywhere; every arm must reproduce its own outputs byte-identically
  across two runs (sha256 recorded in SCORES.md).

## EN-arm output contract (for the sibling/coordinator)
The EN binary reads `kb.txt`, `gaz.txt`, `battery.txt` from CWD and writes `TR`
lines to stderr and per-turn `T <did> <turn> PASS|FAIL` (optional) + `A <answer>`
to stdout. **Contract:** each turn MUST open with the mechanical line
`TR turn=<turn> ut=<utype>` (exactly as NAT emits — `grade.py` aligns trace
blocks on it), followed by one or more `TR <english prose trace>` lines.
Trace lines for a turn must appear between the previous turn's `A` line (or the
`D <did>` header) and that turn's `T`/`A` lines. `grade.py` parses `A` lines for
accuracy; trace blocks for faithfulness token checks and blinded pairs.

## Analysis plan
1. Build both arms; prove determinism (2 runs, sha256).
2. Run both on `battery20.txt` (+ 6 flip pairs); `grade.py` computes (a) and (b).
3. Emit `BLINDED_PAIRS.md` + `KEY.md` for Micah's (c) judgment.
4. `SCORES.md`: per-problem table, criterion scores, per-criterion winner/loser,
   overall winner + honest loser, kill-bar checks.

## Standing constraints
Pure Zag, zero RNG, byte-identical reruns. No binaries in the repo.
Do NOT commit — the coordinator handles commits.

## Amendments
- 2026-09-26 (transcription correction, not a design change): the F1/F2/F6 flip
  `E`-lines initially read "statue of liberty is taller." / "montparnasse tower
  is taller."; the engine's compose output is "the statue of liberty is taller."
  / "the montparnasse tower is taller." (leading "the"). E-lines corrected to the
  byte-exact correct answers and re-verified: all 6 flips PASS on base and
  flipped runs. Trial design, criteria, and kill bars unchanged.
