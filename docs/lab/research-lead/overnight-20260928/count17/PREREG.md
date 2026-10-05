# PREREG -- PHASE 17: IS COUNTING DOMINANCE AN ARTIFACT OF CANDIDATE SIZE?

Branch `ownership`. Written **before** any code for this phase.

Supersedes the disputed `count16/`. PHASE 16's `SIG_B` win is **void as
evidence of learned selection**: its routing feature was a
researcher-authored bucket index, so the "learned" arm was reading a
context router I wrote. Requirement C below exists to prevent that
recurrence.

## QUESTION

`RED_TEAM.md` A1 and PHASE 16 disagree about why counting wins:

* **PHASE 16:** the small-N tests were underpowered; a query-conditional
  arm beat counting 12-to-1 at N=36.
* **RED_TEAM A1:** counting is the *ceiling of all query-blind
  selection*, and beating it needs a feature that partitions candidates.

Both can be true only if the mechanism of the win is **conditional
information**, not candidate-set size. This phase isolates that.

## ANALYTICAL UPPER BOUND -- DERIVED BEFORE EXECUTION

Setup: `C` contexts, `N` candidates, each candidate is correct on
exactly `R_test` of the `H = N*R_test` test queries.

* **Query-blind rules** (any rule that names one candidate without
  reading the query) score **at most `R_test`**. Proof: the rule emits a
  fixed candidate `k`, and `k` is correct on exactly `R_test` queries by
  construction. This bound is attained by any query-blind rule,
  including `argmax` frequency when counts are balanced.
* **`RANDOM`**: expected `R_test/N`.
* **Oracle**: `H`.

Therefore the quantity of interest is **`R_test` versus what a
conditional learner can reach**, and the phase is only informative if
`R_test/N << R_test << H`, i.e. if `N` is genuinely large.

With `N` swept over {5, 10, 20, 30, 50} and `R_test = 2`:

| N | H | query-blind ceiling | random | oracle |
|---|---|---|---|---|
| 5 | 10 | 2 | 0.40 | 10 |
| 10 | 20 | 2 | 0.20 | 20 |
| 20 | 40 | 2 | 0.10 | 40 |
| 30 | 60 | 2 | 0.067 | 60 |
| 50 | 100 | 2 | 0.04 | 100 |

The query-blind ceiling is **flat at 2** across a 10x change in `N`.
So if a learned arm beats 2 at large `N`, candidate-set size is *not*
the explanation, and conditional information is.

## FREQUENCY IS DELIBERATELY NON-DISCRIMINATIVE

Balanced design: each candidate is correct on exactly `R_train` training
queries, so **every count ties** and `argmax` frequency degenerates to
an arbitrary tie-break. This is stronger than "diluted": there is no
frequency signal at all. Two further regimes:

* **MISLEADING PRIOR**: a decoy candidate's count is inflated so
  frequency points *away* from correctness.
* **REGIME CHANGE**: the mapping from context to correct candidate
  changes mid-stream. Tests whether experience gets revised (question E)
  rather than merely accumulated.

## REQUIREMENT 2 -- USEFUL CANDIDATES ARE NOT THE MOST FREQUENT

Enforced and **printed**: the correct candidate for each test query is
reported alongside the raw counts, so a separate scorer can confirm that
frequently-wrong candidates are frequent.

## ARMS

| arm | kind |
|---|---|
| `ORACLE` | upper bound (upper bound, not a claim) |
| `COUNT` | global argmax frequency, index tie-break |
| `RECENCY` | most recently correct candidate |
| `RANDOM` | deterministic pseudo-random |
| `FIXED_CTX` | argmax count restricted to a single fixed context value |
| `FACTS_ONLY` | argmax count using only facts present in the query |
| `EXHAUSTIVE` | tries all candidates, keeps any correct one (upper bound on search) |
| `LEARNED` | conditional over a **learned** representation |
| `SHUFFLED` | `LEARNED` with candidate IDs permuted (control) |

`EXHAUSTIVE` and `ORACLE` are bounds, not competitors. The comparison
that matters is `LEARNED` against the flat ceiling of 2.

## REQUIREMENT 5 -- HOLD-OUT

Structures and instances are held out: candidates whose IDs are permuted
(`SHUFFLED`) and test queries whose contexts never occurred in training.
`LEARNED` cannot win by memorising the later winner, because it never
sees it.

## REQUIREMENT 7 -- PERMUTATION ROBUSTNESS

Candidate IDs, fact order, and insertion order are permuted with fixed
seeds and every arm is re-run. A result that survives only one
permutation is an artifact of identifier layout.

## REQUIREMENT 8/9 -- RAW OUTPUT AND EXTERNAL RECOMPUTATION

The program prints, for every (regime, N, arm, test query): raw counts,
consequences, eligibility, the chosen candidate, and ground truth. It
prints **no `*_ok` verdict flags** and no aggregate success bars. All
verdicts are computed by an **independently written scorer** that parses
this output. `tnn_bars_lint.sh` is run and its result reported.

## REQUIREMENT 10 -- REPLICAS

Three deterministic replicas, sha256-compared. Plus an independent
scorer (`score17.py`) written against the output format, not against the
generator.

## FALSIFIABILITY

* If `LEARNED` fails to beat the flat ceiling of 2 at N=50, **counting's
  dominance is not a size artifact**, and the correct next step is
  root-causing why conditional learning failed -- *not* generating
  another selection mechanism.
* If `LEARNED` beats 2, it is **not** method ownership. Per the
  instruction: the method must move into learner state. A conditional
  readout over contexts is a router. Classify conservatively as
  **conditional competence without method ownership**.

## CANDIDATE REPRESENTATION (how LEARNED is built)

To avoid authoring a context router, `LEARNED` receives only
**opaque candidate behaviour traces**: for each candidate, its output on
a fixed set of probe contexts, as integers. It must induce the
context-to-candidate association itself. No bucket index, no
`qfeat`-style feature, no researcher-chosen context partition.

This is the load-bearing design decision. If `LEARNED` only works when
handed a researcher-authored feature, that is C confirmed, and it is
reported as a negative about my own design.