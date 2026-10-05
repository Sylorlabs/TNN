# REPORT -- PHASE 17: VOID. The world has no learnable signal.

Branch `ownership`. Prereg `count17/PREREG.md`, frozen before code.
3/3 sha256
`3457645c0c333f2efac0167bc0cbc57567ed52b7d62225c7ec64e85056fa41a1`
(42,481 lines of raw output, no verdict flags emitted)
`tnn_bars_lint`: CLEAN. `tnn_loop_lint`: CLEAN.

## VERDICT UP FRONT

**This phase is VOID.** It does not answer whether counting's
dominance is an artifact of candidate size. The world I built has **no
learnable signal at all**, so every arm's score is explained by
tie-breaking rather than by competence. Reporting the `LEARNED` arm's
+1 excesses over the query-blind ceiling as wins would have been
exactly the error this phase was designed to catch.

The architecture and instrumentation worked. The *world* was wrong.

## WHAT DID WORK

These are real, reusable, and worth keeping:

1. **Analytical bound, derived before execution and confirmed.** A
   query-blind arm emits one fixed candidate; each candidate is correct
   on `ceil(312/N)` of the 312 test queries, so it is capped there
   regardless of `N`. Predicted and confirmed exactly:

   | N | ceiling | COUNT | RECENCY | FIXED_CTX | FACTS_ONLY |
   |---|---|---|---|---|---|
   | 5 | 63 | 62 | 62 | 62 | 62 |
   | 10 | 32 | 31 | 31 | 31 | 31 |
   | 20 | 16 | 16 | 16 | 16 | 16 |
   | 30 | 11 | 10 | 10 | 10 | 10 |
   | 50 | 7 | 6 | 6 | 6 | 6 |

   **The query-blind ceiling is flat-ish and falls as 1/N, not flat at
   2** — see "correction" below. `ORACLE` = 312/312 in every cell, so
   the harness is not degenerate.

2. **The invariant check fired correctly.** The scorer verifies that no
   query-blind arm exceeds its own analytic bound. It reported
   `Invariant OK` throughout.

3. **`RANDOM` caught a real defect.** My first RANDOM arm used
   `(t*31+...)%N`. Since truth was `c%N` and `gcd(31,N)=1`, `t*31%N`
   coincides with `t%N` — so "RANDOM" scored **312/312, a perfect
   predictor**. A random arm that scores perfectly is a self-reporting
   bug, and it was visible immediately. Replaced with an xorshift-style
   hash; now scores 4-70 against an expectation of 312/N.

4. **`EXHAUSTIVE` caught a second defect.** Its fit score used
   `(a2-a1)%7`, and Zag's signed modulo can go negative, making the
   argmax meaningless. It tied `COUNT` exactly, which is the tell.
   Replaced with an absolute-difference score.

5. **Requirements 8/9/10 met.** Raw per-candidate counts, per-query
   chosen candidate and ground truth, all 42,145 decision records
   printed. Zero `*_ok` flags. All verdicts come from
   `score17.py`, which shares no code with the generator. 3/3 replicas
   sha-identical.

## WHY IT IS VOID

### Defect 3 (fatal): the LEARNED arm's metric is identically zero

The trace-matching distance was built as

```
d = sum_p | cand_out(k, ctx_x(probe_p)) - cand_out(k, ctx_x(t)) |
```

The two terms are **the same expression**. The distance is exactly 0
for every candidate, at every `N`, in every probe
(`rootcause17.py`: `spread min=0.0 max=0.0 distinct=1`).

So the `LEARNED` argmax is decided by **iteration order** — it always
returns the lowest-index candidate. Its score is a constant-candidate
score in disguise. It is therefore a query-blind arm wearing a
learned label.

### Defect 4 (fatal): truth is a function of the query INDEX

`truth(c) = c % N`. This depends only on the position of the query in
the stream. Nothing observable about a query reveals `c % N`. The
candidate trace `out(k, x) = a*x+b` is monotone in `x` for all `k`
(`a>=1`), so ranking by trace distance ranks by `(a,b)` — which is
**uncorrelated** with `k == c % N`.

**There was no signal to learn.** No mechanism could have done better
than tie-breaking. The instrument could not have detected this; only
reading the code found it.

### Why the +1 excesses are not wins

The scorer listed `LEARNED`/`SHUFFLED` as exceeding the ceiling (33 vs
32, 17 vs 16, 12 vs 11, 8 vs 7). These are **the slack of a near-tie**,
not conditional competence:

* `SHUFFLED` — a pure ID permutation `(k*7+3)%N` — beats `LEARNED` in
  **12 of 15** (regime, N) cells. A permutation of a signal-free choice
  cannot outperform the original systematically. If trace-matching
  carried signal, `LEARNED` should dominate `SHUFFLED`.
* `SHUFFLED` beat the ceiling even at N=50 (9 > 7). A permutation of a
  fixed candidate is still fixed-candidate, so it should be capped. It
  exceeded the cap because the *ceiling is computed per-arm* and the
  permutation changed which candidate, changing its hit count. This
  means my scorer mislabels an arm as "learned" when it is not.

**Both `LEARNED` and `SHUFFLED` are disqualified.**

## CORRECTION TO THE PREREG'S BOUND

The prereg derived the query-blind ceiling as `R_test` = 2, reasoning
that each candidate is correct on exactly `R_test` test queries. That
was wrong in two ways:

1. With 625 contexts and `N` not dividing 625 (N=10,20,30,50), the
   per-candidate counts are **not** equal — they are `ceil(625/N)` or
   `floor`, e.g. 62 or 63 at N=10. The realised ceiling is
   `ceil(312/N)`, which is what the scorer uses.
2. The ceiling **falls as 1/N**, not flat. So a larger candidate set
   actively *hurts* every query-blind arm: at N=5 the ceiling is 63, at
   N=50 it is 7.

The corrected ceiling is the one used above. This matters for the
framing: increasing N does not raise the bar for a query-blind rule, it
lowers the bar **and** lowers its score, in lockstep. Beating
`COUNT` therefore requires beating a target that shrinks with N — the
opposite of what the "N is the explanation" hypothesis predicts.

## ANSWERS TO THE FIVE PRIMARY QUESTIONS

**A. Does counting dominance persist at genuinely large N with
non-discriminative frequency?** — **UNTESTABLE HERE.** Frequency was
made non-discriminative (all counts tied by construction, plus a
misleading-prior regime that inflated a decoy and drove `RANDOM` to
0-11), and `COUNT` did sit at its ceiling. But with no learnable signal
anywhere, no arm could be expected to beat it. The question is
unanswered.

**B. Can a learner exploit conditional experience?** — **NO EVIDENCE.**
`LEARNED` and `SHUFFLED` are both disqualified by Defect 3 and by
`SHUFFLED` beating `LEARNED`. There is no conditional learning in this
run.

**C. Is any gain caused by learner state rather than a researcher-
authored router?** — **MOOT, because there is no gain.** Recorded for
completeness: `LEARNED` was built to receive only opaque integer
behaviour traces, with no bucket index and no `qfeat`-style feature, so
the researcher-authored-router objection that invalidated `count16`'s
`SIG_B` does not apply to its *design*. Its *implementation* is void
for a different reason.

**D. Does gain transfer / survive permutation?** — **NO GAIN TO
TRANSFER.** The permutation control (requirement 7) is what exposed the
defect: `SHUFFLED` beating `LEARNED` is exactly the permutation-robustness
failure the control was built to find.

**E. Does misleading experience get revised?** — **NO.** In regime 2
the truth mapping changes at context 160; `COUNT` and `RECENCY` score
identically before and after, and `LEARNED` shows no early/late
difference attributable to revision. With a signal-free world there is
nothing to revise.

## CLASSIFICATION

Per the instruction to classify conservatively: **no positive result
to classify.** Had `LEARNED` genuinely won, it would have been
**conditional competence without method ownership** — a conditional
readout is a router, and a method only counts as owned if the method
itself moves into learner state. That classification is recorded here
as the standing bar for the next attempt.

## WHAT THE NEXT ATTEMPT MUST DO DIFFERENTLY

Root cause is world construction, not counting. Four requirements:

1. **The truth must be a function of something observable.** Derive it
   from candidate behaviour, not from the query's index. Concretely:
   the correct candidate is the one whose *output on the query* matches
   the query's observed target. That is what makes the problem solvable
   at all.
2. **The learner's metric must be non-degenerate by construction.**
   Assert at build time that the metric's spread across candidates is
   > 0. This one assertion would have caught Defect 3 immediately, and
   it is cheap. Add it as a hard gate.
3. **Permutation control must gate the claim.** If `SHUFFLED` is not
   strictly worse than `LEARNED`, the result is void. Make that a
   precondition, not a footnote.
4. **Correct the ceiling to `ceil(H/N)`** and treat it as *falling* in
   N.

## STATUS

* C1634: **still open.** `count16` remains void as evidence of learned
  selection; `count17` is void entirely. The question is now better
  posed than either attempt: beating counting requires beating a target
  that *shrinks* as N grows.
* C1632: unchanged.
* L3 = 0. No architecture changed. No bridges added or removed.
* **Independence:** this run was authored by the same agent that wrote
  the generator. `score17.py` is an independent scorer in the narrow
  sense that it shares no code and recomputes every verdict, but it was
  written by the same author. Cleaner bars do not make this
  independent. The raw output is preserved precisely so it can be
  scored by someone else.