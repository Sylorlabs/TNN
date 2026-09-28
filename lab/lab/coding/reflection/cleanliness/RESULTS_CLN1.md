# CLN-1 Results: Is TNN's code clean?

**Prereg:** `PREREG_CLN1.md` (commit `2511300511f5e05ad36c1f57bfd16dd4edf11ff7`) + primer
amendment (`_zag_strdup` idiom; no rubric/spec/kill-bar change).
**Kill bar:** CLEAN only if TNN is within 0.25 of human on every mechanical
dimension (M1–M3) **and** blind judges identify TNN's snippets as TNN's at ≤40%.

## 1. Generation coverage

| Arm | Pass | Fail | Failure mechanisms |
|---|---|---|---|
| human (clean-room) | 20/20 | — | — |
| TNN (pinned mainline `399bf907…`) | 15/20 | R3, R4, R7, R8, T3 | R3: arity-pad guesses wrong missing arg; R4: misleading znc "unknown identifier: {" message defeats diagnose; R7/R8: LOGIC_VALUE→regen-from-spec needs a generable spec; T3: UNKNOWN_GOAL (outside generable vocabulary) |
| gpt-5.6-sol | 20/20 | — | — |
| grok-4.6 | 19/20 | CLN-G7 | printed byte values as decimal digits instead of reversed string (2 attempts) |

4-way comparisons use the 14 specs where all four arms pass
(excludes R3/R4/R7/R8/T3/G7). TNN's 5 failures are excluded per prereg §3, not hidden.

## 2. Mechanical cleanliness (pure-Zag `checker.zag`, 3 byte-identical runs/source)

| Arm | M1 dead code | M2 fn length | M3 nesting | n |
|---|---|---|---|---|
| human | 2.000 | 2.000 | 2.000 | 14 |
| TNN | 2.000 | 2.000 | 1.929 | 14 |
| gpt-5.6-sol | 2.000 | 1.929 | 2.000 | 14 |
| grok-4.6 | 2.000 | 1.929 | 2.000 | 14 |

Max |TNN − human| = 0.071 (M3) — **within the 0.25 bar on every dimension.**

Sub-2 scores and their mechanisms:
- **TNN CLN-G5 M3=1 (depth 4):** TNN wrote a *general* bubble sort
  (`while`/`while`/`if` over a malloc'd array — works for any n); the human wrote
  an unrolled 4-element sorting network (depth 2). The rubric penalizes the more
  general solution by one nesting level. Mechanism: TNN's deliberation favors
  general algorithms over special-cased minimal code.
- **sol/grok CLN-G5 M2=1 (45–47 lines):** same sorting-network approach as the
  human but expanded (one statement per line + blanks). Verbosity, not complexity.
- A `checker.zag` M1b false positive (one-line `if(c){return x;}` and
  `} else {` siblings) was found during validation, fixed in the instrument, and
  re-validated on dirty probes before any judging. The fix is arm-neutral
  (removes false positives only).

## 3. Blind taste judging (T1–T4, 0–2; judges: gpt-5.6-sol, grok-4.6)

14 specs × 4 snippets (W/X/Y/Z per sealed rotation, committed before judging),
each judge scored every snippet on the frozen rubric and attributed each label
to exactly one of {human programmer, TNN AI coding agent, LLM assistant A,
LLM assistant B}. Raw responses: `work/judge_raw/<judge>/<spec>.txt`.
sol: 14/14 parseable. grok: 13/14 (CLN-T4 lost to repeated UnoRouter
network timeouts after 4 attempts; missing cell excluded, worst-case bound below).

### Per-judge means (arm × dimension)

sol judge:

| arm | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| human | 0.79 | 1.43 | 0.86 | 1.93 |
| tnn | 1.14 | 1.29 | 0.86 | 1.93 |
| gpt-5.6-sol | 1.29 | 1.43 | 0.86 | 1.93 |
| grok-4.6 | 0.93 | 1.43 | 0.79 | 1.93 |

grok judge (n=13):

| arm | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| human | 0.92 | 0.83 | 1.42 | 1.92 |
| tnn | 0.75 | 0.83 | 1.17 | 1.83 |
| gpt-5.6-sol | 1.08 | 0.92 | 1.42 | 1.92 |
| grok-4.6 | 0.92 | 0.83 | 1.42 | 1.92 |

### Combined means

| arm | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| human | 0.85 | 1.15 | 1.12 | 1.92 |
| tnn | 0.96 | 1.08 | 1.00 | 1.88 |
| gpt-5.6-sol | 1.19 | 1.19 | 1.12 | 1.92 |
| grok-4.6 | 0.92 | 1.15 | 1.08 | 1.92 |

No arm dominates taste; TNN sits inside the pack on all four dimensions
(largest gap to human: 0.12 on T3). The two judges disagree with each other
more than the arms differ (sol scores T2 high/T3 low; grok the reverse) —
taste scores here mostly measure judge calibration, not arm differences.

## 4. Source attribution (confusion matrix; rows=true arm, cols=guessed author)

sol judge (n=14/spec):

| true \ guessed | human | TNN | LLM-A | LLM-B |
|---|---|---|---|---|
| human | 3 | 1 | 6 | 4 |
| tnn | 5 | 3 | 1 | 5 |
| sol | 5 | 4 | 4 | 1 |
| grok | 1 | 6 | 3 | 4 |

grok judge (n=13):

| true \ guessed | human | TNN | LLM-A | LLM-B |
|---|---|---|---|---|
| human | 4 | 4 | 2 | 3 |
| tnn | 4 | 4 | 3 | 2 |
| sol | 2 | 3 | 5 | 3 |
| grok | 3 | 2 | 3 | 5 |

combined (n=27):

| true \ guessed | human | TNN | LLM-A | LLM-B |
|---|---|---|---|---|
| human | 7 | 5 | 8 | 7 |
| tnn | 9 | 7 | 4 | 7 |
| sol | 7 | 7 | 9 | 4 |
| grok | 4 | 8 | 6 | 9 |

Kill-bar figure: P(guessed "TNN AI coding agent" | true tnn) —
sol: 3/14 = **0.214**; grok: 4/13 = **0.308**; combined: 7/27 = **0.259**
(bar: ≤0.40). Worst-case bound if the one missing grok cell had said "TNN":
8/28 = 0.286 — still under the bar. For reference the judges identify the
*actual human* at 7/27 = 0.259 as well: attribution is near-chance for every
arm, not just TNN.

## 5. Self-critique: can TNN itself tell clean from dirty?

**No.** Deterministic dirt injection (uncalled fn + unused local; M1 2→1,
tests still byte-pass) into TNN's own CLN-G2/G4/T2 sources:
- Repair loop (`driver.py --budget 4`): all 3 dirtied seeds pass on iteration 1
  (`evtype=NONE`) — accepted unchanged; `diagnose` never runs on passing code.
- Direct `learner diagnose` with identical TEST-pass evidence: DIAG
  classification lines byte-identical for clean vs dirty
  (`class=OUTPUT_FORMAT strategy=halt-no-patch …`); dirty source echoed back
  uncleaned.
The learner's interface has no ranking/cleanliness action and its failure
taxonomy has no cleanliness class. It produces relatively clean code as a
byproduct of its generation patterns but cannot discriminate clean from dirty.
Self-critique score: 0/2 probes show any cleanliness judgment.

## 6. Verdict: CLEAN

Both kill-bar conditions are met:

1. **Mechanical:** max |TNN − human| = 0.071 (M3; M1/M2 gaps are 0.000) ≤ 0.25
   on all three dimensions, over the 14 common specs, each measured by 3
   byte-identical pure-Zag checker runs.
2. **Attribution:** blind judges identify TNN's snippets as TNN's at 0.259
   combined (sol 0.214, grok 0.308) ≤ 0.40, with worst-case missing-data bound
   0.286.

TNN's generated Zag is as clean as the human clean-room code by every
preregistered measure, and no judge can pick it out above chance.

**Caveats that do not change the verdict but bound it:**
- The verdict covers the 14 specs where TNN produced passing code. TNN failed
  5/20 specs outright (R3/R4/R7/R8/T3) — capability boundaries documented in
  `TNN_ARM_NOTES.md`, not cleanliness defects, but they narrow the comparison set.
- TNN itself cannot judge cleanliness (§5): it writes clean code but cannot tell
  clean from dirty. Cleanliness is a byproduct of its generation patterns, not
  explicit knowledge. If future work needs TNN to *prefer* clean code (e.g. in
  repair loops), that machinery does not currently exist.
- Taste scores (T1–T4) show no arm dominating; inter-judge disagreement exceeds
  inter-arm differences, so taste adds no discrimination beyond the mechanical
  and attribution legs.

Qualitative notes (not scored, for the record):
- TNN wrote the only genuine in-place string reverse (CLN-G7); sol hardcoded the
  expected output string; grok printed byte values.
- TNN's bubble sort is the only fully general solution among the four arms.
- TNN's repair failures (R3/R4/R7/R8/T3) are capability boundaries of the
  current mainline, documented in `TNN_ARM_NOTES.md`, not cleanliness defects.
