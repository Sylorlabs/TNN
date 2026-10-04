# PREREG: PREDICT-OPTIONALITY (C520-C529)

Worker: PREDICT-OPTIONALITY. Lane: `docs/lab/research-lead/overnight-20260928/predopt/`
Branch: `lane/predopt`. Worktree: `/Users/Shared/micah/Documents/TNN/.worktrees/predopt`.
Charter: 20 (prediction is ONE capability, not the universal primitive), 39 (compute
adapts to difficulty), 79 (stupid baseline), 108 (no task-type labels), 167 (cognitive
cost), 238 (would the architecture still choose if all labels disappeared).

Committed BEFORE any implementation `.zag` exists in this lane.

---

## 0. The claim under test

The frozen architecture should use PREDICTION only when it is actually useful, and
just as importantly should NOT predict when knowledge already determines the answer.
The learner must infer what is useful from its own state, not from a label.

**Central negative form (charter 238).** If all task names, domain names, benchmark
labels, expected answers and special-case handlers disappeared, would the frozen
architecture still choose correctly?

## 1. Prior work this must not duplicate, and defects it must absorb

Built on (not duplicated):
- `lane/p7belief` `p7_belief_inquiry/`: proved a single utility argmax over an
  ENUMERATED candidate set with no mode label can gate commitment on the frozen
  `bp2_select` numeric refusal. Reused the *pattern* (enumerate, score one way,
  strict argmax), not its machinery.
- `lane/adversary` `adversary/BREAKS.md`: six frozen defects that directly threaten
  any optionality claim. Each gets an explicit bar below.

| prior defect | threat to THIS lane | bar |
|---|---|---|
| C504 `bootstrap_miss` subject-blind: answers a question about a never-taught subject from other subjects' facts | a "KNOWN" signal that is not subject-bound is a FAKE known | **K-FAKEKNOWN** |
| C508 `bootstrap_miss` insertion-order dependent | a "known/derivable" split that is really an order artifact | **K-ISOMORPH** |
| C505 `res_op` node-id>=1000 collision; `-2` is both honest decline and broken decline | my own substrate could make every decline indistinguishable | **K-DECLINE-DISTINCT** (node cap asserted, and decline reason enumerated) |
| C501 `learn_bindings` memoizes procedure family on a bare need tag; `compose` skips binding on a plan hit | the learner's KNOWN/DERIVABLE distinction could BE that memo | **K-NOMEMO** (ablate the memo: choice must not move) |
| C502 `compose` returns "built" on `plan_new`=-1; plan stride overflow at 5 needs | success reported where nothing was built | **K-NOFAKE-SUCCESS** (every reported success has a non-zero record) |
| C509 single-valued answer type erasure | INADEQUATE (set-valued) may be structurally inexpressible, so "construction pressure" may be undetectable | **K-WIDE** (report honestly if the substrate cannot signal it) |
| p7belief FP-M9 failed: a channel calibrated in-session can be "a prior that happens to be right" | a per-relation prior that happens to be right on every fixture | **K-PRIOR-ADVERSARIAL** (mislead the prior after the main table; estimate must fall) |

## 2. THE HARD RULE: no labels reach the learner

The learner is forbidden any knowledge of which case it is in.

Forbidden and asserted by grep (K-NOLABEL-SRC):
- no string literal anywhere in the learner file (the frozen cores contain none either);
- no occurrence of any case name, expected op name, or fixture-specific entity id;
- no `if/while` whose condition mentions a case, a label, a mode, or an op name;
- the learner's only free constants are the frozen model constants of section 4.

The fixture writes two arena bands the learner NEVER reads:
`LABEL` (case name code) and `TRUTH` (expected op code). Their offsets are passed to
the grader only. At runtime, `po_bin nolabel` does not write either band at all
(region left zero by `z_alloc`). The learner is not modified for that run.

## 3. SUBSTRATE, and why not the frozen cores verbatim

A new flat arena is used. Reason, stated plainly: the six frozen defects above are
*in* the frozen paths I would otherwise build on, so a result built on them would
measure C501/C504/C509 rather than optionality. To avoid discarding the knowledge,
the two frozen behaviours that matter most are **replicated as explicit, separable
switches** so their effect can be measured rather than assumed: `PO_ABL_RECENCY`
(replicates the C504/C508 subject-blind recency rule) and `PO_ABL_MEMO` (replicates the
C501 route memo).

Bounds adopted from the frozen defects, enforced in code:
- live records per band capped at 256 (`K-NODECAP`), far below C505's 1000 threshold;
- never reuse a record id, never scan "the most recently allocated ids" as a
  substitute for a subject match (that is exactly C508);
- every reported success is accompanied by a record count that must be non-zero.

## 4. FROZEN COST MODEL (fixed here, before any run)

One utility, one scale, integers only. No floats exist in Zag.

```
certainty(op)  in [0,255]
cost(op)       in steps, measured by DRY-RUNNING the route in a scratch region
utility(op)    = certainty(op) - W_COST * cost(op)
W_COST         = 8
```
Chosen before any run for a stated reason, not tuned: one store read is 8 points,
about 3 percent of the 255 scale, i.e. below the resolution that matters; a 6-entry
prior scan plus one allocation is 7 steps = 56 points, decisive. **W_COST is
acknowledged as load-bearing and is swept at 4, 8, 16 as robustness bar K-WCOST-SWEEP.**

### Certainty (each is the learner's own honest posterior for the value it returns)
| op | certainty | why |
|---|---|---|
| RETRIEVE | `255 / n_distinct` | returning 1 of n stored values for (s,r) is right with probability 1/n. **This is the C509 correction, not a special case for the WIDE fixture.** |
| DERIVE | `255` if every leaf of the closure is an OBSERVED record; else `255 - 55*unwitnessed_hops` | a closure whose leaves are all observed is a proof, not an inference; only unwitnessed hops decay |
| CONSTRAIN | `255 / n_feasible` | returning 1 of n values surviving the constraint set |
| CONSTRUCT | `255` | the set of live distinct values for (s,r) is exactly what is stored |
| INQUIRE | `255 * hits / trials` on that channel, default `128` if `trials==0` (Beta(1,1)) | learned, never declared |
| PREDICT | `255 * hits / trials` on that relation, default `128` if `trials==0` (Beta(1,1)) | learned, never declared |

### Cost (measured by dry run, never a lookup table)
| op | cost |
|---|---|
| RETRIEVE | 1 read |
| DERIVE | closure record count + 1 result alloc |
| CONSTRAIN | constraint record count + 1 |
| CONSTRUCT | distinct value count + 1 set-node alloc |
| INQUIRE | channel cost + 1 |
| PREDICT | live prior-history entries for the relation + 1 alloc |

### Availability
A candidate with no supporting structure in the store is **UNAVAILABLE**: excluded
from the argmax, never scored, never executed for real. PREDICT is available only if
`prior_n >= 1` (there is some history to be prior over); with zero history the learner
has no prior and must not guess. An unavailable candidate still costs its scan; the
scan cost is reported separately as `enumeration_visits`.

### Argmax and tie-break (frozen)
Strict maximum of utility. Tie broken by (1) lower measured cost, then (2) lower
candidate index in the frozen scan order `RETRIEVE, DERIVE, CONSTRAIN, INQUIRE,
CONSTRUCT, PREDICT`. Bar **K-COSTORDER** re-runs with 3 permuted scan orders and
requires an identical choice vector, so the tie-break and scan order are shown not to
decide any case.

## 5. FROZEN FIXTURES (6 cases, no label reaches the learner)

`s` subject, `r` relation, `v` value. OBS = observed record (kind 1). DER = derived
record (kind 3) with a live support chain. CON = constraint record (kind 7):
relation 10 = GE, 11 = LE, 12 = NEQ, 13 = EQ. PROBE = channel record with a cost.

Every fixture also seeds the **per-relation prediction history**. On cases 1, 2, 3 and
6 the seeded history is **100 percent accurate on purpose**. This is the strong form of
the test: the learner is told, by its own measurement, that predicting this relation
never fails, and it must still refuse to predict, because a proof costs less than a
lucky guess.

| # | query | store | seeded prior | PROBE | expected op |
|---|---|---|---|---|---|
| 1 | `(7,10)` | OBS `(7,10,42)` | r10: 8 trials 8 hits, 6 entries | none for r10 | RETRIEVE |
| 2 | `(1,30)` | OBS `(1,10,3)`, OBS `(3,10,5)`, DER `(1,30,5)` depth 2, both leaves OBS | r30: 6/6, 6 entries | r30 cost 3 | DERIVE |
| 3 | `(9,40)` | CON on 9: GE 2, LE 6, NEQ 3, EQ 5 -> feasible `{5}` | r40: 6/6, 6 entries | r40 cost 8 | CONSTRAIN |
| 4 | `(5,50)` | nothing for (5,50) | r50: 12 trials **3** hits, 12 entries | **none for r50** | PREDICT |
| 5 | `(2,60)` | nothing for (2,60) | r60: 4 trials **0** hits, 4 entries | r60 cost 2, measured 5/5 informative | INQUIRE |
| 6 | `(4,70)` | OBS `(4,70,11)`, `(4,70,13)`, `(4,70,17)`, `(4,70,19)` -> 4 distinct | r70: 6/6, 6 entries | none for r70 | CONSTRUCT |

Case 4 has no probe channel because its generator is genuinely stochastic and no
measurement resolves it. Case 5 has one because its law is deterministic and a single
cheap observation resolves it. These are properties of the world, discovered by the
learner scanning probe records, never told to it.

Predicted utilities (frozen arithmetic, checked by the driver):
case 1: K `255-8=247` vs P `255-56=199`. case 2: D `255-32=223` vs I `255-32=223`
(**predicted TIE**, broken to DERIVE by lower cost 3 vs 4) vs P `199`. case 3: C
`255-40=215` vs I `255-72=183` vs P `199`. case 4: P `63-104=-41`, sole finite
candidate. case 5: I `255-24=231` vs P `0-40=-40`. case 6: V `255-40=215` vs P `199`
vs K `63-8=55`.

Case 2 is predicted to be a near-tie between a proof and a cheap probe. That is
reported as a boundary, not hidden.

## 6. KILL BARS (all must pass; any FAIL is reported as a FAIL)

**K-DET** 3/3 byte-identical stdout. **K-NONEMPTY** stdout >= 200 bytes and rc 0.
**K-PUREZAG** `tnn_pure_zag_report` -> `PURE-ZAG-CLEAN` at build and run.
**K-NOLABEL-SRC** grep attestations of section 2 all return 0.
**K-NOLABEL-RUN** choice vector byte-identical between `./po_bin` and `./po_bin nolabel`.
**K-ISOMORPH** choice vector identical under (a) a bijective rename of every entity
and relation id and (b) a reversal of fixture insertion order.
**K-CHOICES** choice vector exactly `[RETRIEVE, DERIVE, CONSTRAIN, PREDICT, INQUIRE,
CONSTRUCT]` for cases 1..6.
**K-NOPREDICT-1236** realized prediction steps on cases 1, 2, 3, 6 are **exactly 0**.
**K-UPC** unnecessary-prediction cost reported per case as
`upc_realized` (spent on PREDICT when PREDICT is not chosen, must be 0) and
`upc_avoided` (cost the always-predict baseline would have spent).
**K-COST** per-case `visits, steps, allocs, verifs, searches` all non-negative and
printed; `searches` = count of AVAILABLE candidates.
**K-NOMEMO** with `PO_ABL_MEMO=1` (route memo disabled) the choice vector is
**identical**; `steps+allocs` is **>=** the main run. This is the direct C501 test: if
the KNOWN/DERIVABLE split moves when the memo moves, the split was the memo.
**K-FAKEKNOWN** with the main build, querying the never-taught subject 999 on r10
returns RETRIEVE **unavailable** (not a fabricated hit). With `PO_ABL_RECENCY=1` the
replicated C504/C508 recency rule DOES fabricate a hit. Both directions asserted.
**K-DECLINE-DISTINCT** live records stay `<= 256` per band; the decline reason is an
enumerated code, never the bare `-2` that C505 makes ambiguous.
**K-NOFAKE-SUCCESS** every case reporting a solved op has a non-zero support record
count; no op reports success with zero records.
**K-WIDE** on case 6 the learner returns a SET node of arity 4 and `n_distinct==4`;
single-valued return is forbidden (C509 correction).
**K-COSTORDER** identical choice vector under 3 permuted candidate scan orders.
**K-DIFFICULTY** (charter 39) (a) DERIVE family with chain depth 1,2,3,4,5: `steps`
strictly increasing, choice DERIVE at every depth. (b) KNOWN family with 0,4,8,12
padding facts: `steps` **constant** at 1 and choice RETRIEVE at every padding level.
**K-PRIOR-ADVERSARIAL** after the main table, r70's realized outcomes are fed back as
misses; the learner's PREDICT certainty for r70 must strictly decrease and PREDICT must
stop winning case 6. Directly answers p7belief FP-M9.
**K-WCOST-SWEEP** choice vector identical at `W_COST` in {4, 8, 16}.
**K-BASELINE** the three stupid baselines are implemented and scored; the comparison is
reported whatever it shows, including a tie.

## 7. ABLATIONS (one predicate each)

| switch | removes | predicted effect |
|---|---|---|
| `PO_ABL_NOPRICE` | dry-run pricing: every available candidate is given `cost=0` | ties everywhere go to PREDICT (scanned first); PREDICT selected on cases 1, 2, 3, 5, 6; **total realized cost rises**, and cases 1, 2, 3, 6 become wrong. This is the required ablation: remove the mechanism that suppresses unnecessary prediction, cost rises. |
| `PO_ABL_MEMO` | persistence of the learned (s,r)->route memo | choice vector **unchanged**; cost **rises** (repeat queries must re-derive) |
| `PO_ABL_RECENCY` | subject-bound lookup, replaced by the frozen C504/C508 recency rule | case 1 unchanged; the never-taught-subject probe flips to a fabricated hit |
| `PO_ABL_PRIORWILD` | learned per-relation certainty, forced to 255 | PREDICT wins 5 of 6, showing the main result is carried by pricing, not by a lucky prior |

## 8. STUPID BASELINES (charter 79), scored on all 6 cases

- **always-RETRIEVE**: if an exact fact for (s,r) exists return it, else fail.
- **always-DERIVE**: if a live closure exists use it, else fail.
- **always-PREDICT**: always return the relation prior's modal value.

Scored on: cases correct out of 6, total steps, wasted steps. The preregistered
expectation, to be reported verbatim whatever happens: the learner TIES
always-RETRIEVE on case 1 (identical policy there) and strictly beats it on cases 2-6;
the learner TIES always-PREDICT on case 4 (identical policy there) and strictly beats
it on cases 1, 2, 3, 6. If either tie does not materialize, report it.

## 9. Honest-failure clause

Any bar that fails is reported as failed with its number. No bar is moved, softened or
dropped after a run. One pre-execution amendment is permitted only for an internal
inconsistency in this document, committed alone, and no numeric bar may be relaxed by
it. Candidate claim IDs, minted only if the bars support them: **C520-C529**.