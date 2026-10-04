# PREDICT-OPTIONALITY: prediction is optional (C520-C525)

Worker: PREDICT-OPTIONALITY. Lane `predopt`, branch `lane/predopt`,
worktree `/Users/Shared/micah/Documents/TNN/.worktrees/predopt`.
Charter 20 (prediction is ONE capability), 39 (compute adapts to difficulty),
79 (stupid baseline), 108 (no task-type labels), 167 (cognitive cost),
238 (label removal).

Prereg `PREREG.md` committed alone as `a1d1875c5` before any `.zag` existed in
this lane; pre-execution amendment `AMENDMENT_A1.md` alone as `3b4e58c31`.
**No bar was moved, softened or dropped after any run.** One bar FAILs and is
reported as a FAIL (K-ISOMORPH). Two preregistered ablation *predictions* are
reported as FALSIFIED.

Determinism `zbuild --rep 3`: 3/3 byte-identical,
`sha256 7e5cba0c9581b30f418e88e9634d5bd13ce23888cb5b83480a4b1e2eb7ee3fd8`,
5840 bytes, rc 0, non-empty (`K-DET`, `K-NONEMPTY`). Pure-Zag: `znc` only,
`tnn_pure_zag_report` -> `PURE-ZAG-CLEAN` at build and run. Every run went
through `tnnwatch.sh`; no binary left unattended.

---

## 1. What was measured

Six fixtures, one per required case. The learner is given a query `(s,r)` and
its own store. It enumerates six candidate routes, prices each by dry run, and
takes a strict argmax of `utility = certainty - 8*cost`. Certainty and cost are
defined in PREREG section 4 and are the learner's own measurements. There is no
label, no case name, no mode switch, no `if derivable then derive`.

**The learner file contains zero string literals and zero occurrences of any
case name, route name, or fixture entity id** (attested after stripping
comments; the only multi-digit constants are arena geometry, scratch cell
indices, and the 255/128/55 certainty scale).

## 2. Per-case result, with cognitive cost (charter 167)

| case | route taken | value | steps | allocs | verifs | visits | searches | support | certainty | utility | realized prediction steps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 KNOWN | RETRIEVE | 42 | 1 | 1 | 1 | 8 | 2 | 1 | 255 | 247 | **0** |
| 2 DERIVABLE | DERIVE | 5 | 3 | 1 | 3 | 9 | 3 | 3 | 255 | 231 | **0** |
| 3 FORMAL | CONSTRAIN | {5} arity 1 | 5 | 1 | 4 | 18 | 3 | 4 | 255 | 215 | **0** |
| 4 UNCERTAIN | PREDICT | 0 | 13 | 1 | 12 | 24 | 1 | 12 | 63 | -41 | 13 |
| 5 MISSING | INQUIRE | 666 | 3 | 1 | 1 | 4 | 2 | 1 | 255 | 231 | 0 |
| 6 INADEQUATE | CONSTRUCT | {11,13,17,19} arity 4 | 5 | 1 | 4 | 23 | 3 | 4 | 255 | 215 | **0** |

`VEC 0 1 2 5 3 4` = `EXPECT 0 1 2 5 3 4`, `CASE_MATCH 6/6`.
Totals: steps 30, allocs 6, verifs 25, visits 86, wasted steps 0.

**Unnecessary prediction cost (K-UPC).** `upc_realized` = prediction steps
spent on cases where PREDICT was not chosen = **0, exactly, on all of cases 1,
2, 3, 6** (`K-NOPREDICT-1236` PASS; `predsteps` is 0 on each of them
individually, not merely on the total). `upc_avoided` = cost the
always-predict baseline would have spent = **33** steps across the four cases
(`K-UPC-AVOIDED 33`).

**This is the strong form of the test and it held.** On cases 1, 2, 3 and 6 the
learner's own measurement says the relation's prior is 6-for-6, i.e. a perfect
100% accurate predictor of that relation. It refuses to predict anyway,
because a proof costs 1-5 steps and a lucky guess costs 7. On case 4, where the
prior is honestly 3-in-12 and no measurement channel exists, it predicts
despite a **negative** utility of -41, because prediction is the only route
with any support at all.

## 3. Label removal (charter 238, the central question)

`./po_full nolabel` is the identical binary with the two grader bands (case code,
expected row) never written. Diff of every choice-bearing line -- the six CASE
lines, VEC, all ABL_/ORDER/WCOST/REPEAT/ISO/X_TIEHIGH vectors -- is
**byte-identical**. The only removed line is the grader's own `CASE_MATCH 6/6`
report, which cannot exist without the expected rows it is reporting against.
`K-NOLABEL-RUN` **PASS**. Removing all task names, expected answers and
special-case handlers moves no choice.

## 4. Stupid baselines (charter 79)

| policy | correct | steps | wasted steps |
|---|---|---|---|
| always-RETRIEVE | **1/6** | 42 | 35 |
| always-DERIVE | **1/6** | 8 | 5 |
| always-PREDICT | **1/6** | 46 | 33 |
| learner | **6/6** | 30 (86 visits) | 0 |

The preregistered expectation, reported verbatim as it came out: the learner
**ties** always-RETRIEVE on case 1 (identical policy there) and strictly beats
it on cases 2-6; the learner **ties** always-PREDICT on case 4 (identical
policy there) and strictly beats it on cases 1, 2, 3, 6. Both ties
materialized. No honest failure to report here. Note the cost comparison is
not like-for-like: a baseline must scan its whole band to discover that nothing
matches, while the learner is quoted its own priced route cost; the learner is
also charged 86 store visits, which is why its 30 steps and the baselines' 42
and 46 are not directly comparable. The comparison that *is* like-for-like is
correctness, and it is 6/6 against 1/6.

## 5. Ablations

| switch | removes | prereg predicted | observed | verdict |
|---|---|---|---|---|
| `PO_ABL_NOPRICE` | every available candidate priced 0 | PREDICT on 1,2,3,5,6; cost rises | `vec` **unchanged** `0 1 2 5 3 4`, steps 30 | **FALSIFIED** |
| `PO_ABL_PRIORWILD` | learned per-relation certainty forced to 255 | PREDICT wins 5 of 6 | `vec` unchanged, steps 30 | **FALSIFIED** |
| `PO_ABL_MEMO` | persistence of the (s,r)->route memo | choice unchanged, cost rises | memo-on repeat: steps 6 allocs 0; memo-off repeat: steps 30 allocs 6; `vec` identical | **CONFIRMED** |
| `PO_ABL_RECENCY` | subject-bound lookup, replaced by the C504/C508 rule | never-taught subject flips to a fabricated hit | main: `open0=0 route=DECLINE reason=1`; replicated: `open0=1 val=7 support=3 fabricated=1` | **CONFIRMED** |
| `X_TIEHIGH` (**post-hoc, not preregistered**) | price **and** the lower-index tie-break | -- | `vec 5 5 5 5 3 5`, PREDICT on 5 of 6, 4 wrong, steps 44 (+14) | see below |

**Why the two preregistered ablations failed, and what that means.** The prereg
believed that removing the price would send ties to PREDICT "because it is
scanned first". It is scanned **last**, and the frozen tie-break (PREREG s4) is
(1) lower measured cost, then (2) lower candidate index. With the price removed
the *utility* ties, but the **measured cost still differs** (7 for PREDICT vs 1
for RETRIEVE), so tie-break clause (1) resolves it before clause (2) is ever
reached. Suppression of unnecessary prediction is therefore carried by **two**
mechanisms, not one, and removing either alone leaves it intact. This also means
AMENDMENT_A1's judgement was wrong: it declined to amend the NOPRICE prediction
on the grounds that it was "a prediction about the world", when it was in fact
an internal inconsistency with PREREG section 4's tie-break. Reported, not fixed.

`X_TIEHIGH` is filed as **post-hoc exploratory** and is not a kill bar. It is
the ablation the mission requires: remove the mechanism(s) that suppress
unnecessary prediction. Doing so flips cases 1, 2, 3 and 6 from
RETRIEVE/DERIVE/CONSTRAIN/CONSTRUCT to PREDICT, makes 4 of 6 cases wrong, and
raises total realized steps from 30 to 44 (+14, +47%). That +14 is the price
the suppression mechanism is saving, measured.

## 6. Charter 39: compute adapts to problem difficulty

`K-DIFFICULTY`. DERIVE family, chain depth 1..5: steps **2,3,4,5,6** strictly
increasing, DERIVE chosen at every depth. KNOWN family with 0/4/8/12 padding
facts: steps **1 at every padding level**, RETRIEVE at every level, visits
constant at 8. Cost tracks depth and is invariant to distractor volume.

## 7. The C501 question: is "known" just the memo?

The COGOPS `learn_bindings` route memo is a mechanism by which "known" could be
faked. Here the memo is a real mechanism (it is written when enabled and read
on repeat queries) and the choice vector is **identical** with it on and off,
while cost rises 6 -> 30 without it. `K-NOMEMO-IDENTITY` and
`K-NOMEMO-COSTRISE` both **PASS**. The KNOWN/DERIVABLE split is therefore
**not** an artifact of `learn_bindings`.

It is, however, partly a *representation* distinction and this must be stated:
the learner separates RETRIEVE from DERIVE because one has an addressed record
and the other has a record carrying a support closure. That is honest reading of
structure, but it is reading structure, not introspecting on knowing. It also
means the honest CERTIFY certainty of `255/n_distinct` (the C509 correction) is
what stops a 4-valued question from being answered as a fact: on case 6
RETRIEVE is available but scores 63 and loses to CONSTRUCT's 255.

## 8. C504/C508 absorption

The replicated recency rule answers a question about never-taught subject 999
from six facts about six *other* subjects, and now also **persists** the
fabrication, reproducing the frozen C504 second-query behaviour. The real
learner refuses: `open0=0`, decline reason 1 (an enumerated code, never C505's
ambiguous bare `-2`). Live records peak at **40** per band, far below C505's
1000 threshold. `K-FAKEKNOWN`, `K-DECLINE-DISTINCT`, `K-NOFAKE-SUCCESS` PASS.

**Insertion-order (C508): `ISO_REVERSE vec 0 1 2 5 3 4`, identical to main.**
Support leaves are resolved by content (relation and value), never by
allocation position. The C508 order artifact does not reproduce.

## 9. The one FAIL, and a real name leak

`K-ISOMORPH` **FAIL**. `ISO_RENAME` (every entity and relation id shifted by
140) gives `0 1 5 5 3 4`: case 3 flips CONSTRAIN -> PREDICT. Cause, localized
exactly: the learner hard-codes four relation codes as constraint operators
(10=GE, 11=LE, 12=NEQ, 13=EQ). Renaming them stops the restrictions from
constraining anything (certainty 255 -> 63) and PREDICT then wins.
`ISO_RENAME_KEEP_OPCODES` (same rename, operator codes restored) is
**identical to main**, which proves the break is those four codes and nothing
else.

This is a genuine charter-238 exposure: the architecture is **not** fully
name-blind. It carries four operator semantics inside the relation namespace.
The frozen cores have the same shape (op codes >= 1000 colliding with node ids,
C505), so this is a property of the family, not of this implementation.

## 10. Everything else

`K-WCOST-SWEEP` PASS (W_COST 4/8/16, identical vector -- the price weight is
load-bearing in size but not in sign on these fixtures).
`K-COSTORDER` PASS (3 permuted scan orders, identical vector). Note the
tie-break's index clause makes the scan order unable to decide anything when
costs tie, so this bar is weaker than it looks; it is reported, not inflated.
`K-PRIOR-ADVERSARIAL` PASS: after r70's realized outcomes are fed back as
misses, PREDICT certainty falls **255 -> 127 -> 85 -> 63**, strictly. The
prereg's additional clause "PREDICT must stop winning case 6" is **vacuous**,
because PREDICT never wins case 6 in the main table (CONSTRUCT does). A1
predicted this and it is reported as written.
`K-WIDE` PASS: case 6 returns a set node of arity 4 with values 11,13,17,19 --
the C509 single-valued type erasure is corrected, not worked around.

**15 of 16 preregistered in-binary bars PASS.**

## 11. Two compiler defects found (both silent, both would have produced a fake result)

1. **Byte offset vs cell index.** `get32`/`set32` take a **byte** offset.
   Code written to treat the argument as a cell index silently produces
   overlapping 4-byte writes: four consecutive fields overwrite one cell, and
   every downstream number becomes a heap address. Isolated by bisection
   (`po_dbg*`, deleted). This is the same class as the brief's warning about an
   `i32` where `[]u8` is expected: it compiles, and it lies.
2. **Five-term `&&` in an `if` condition silently evaluates false.** Four terms
   work; five do not. Restructured into a 3-term predicate.

Also a trap worth recording: an allocator that rounds every request up to
262144 bytes makes out-of-range cell indices *not crash*, which converts a
bounds bug into silent garbage. Both defects cost more time here than the
experiment did.

## 12. Verdict

**Prediction is optional in this architecture, and the optionality is real.**
The learner infers from its own state that a proof beats a lucky guess, and it
does so while holding a perfect in-memory record that predicting would have
been right; it predicts only where the future is genuinely uncertain, accepting
a negative utility to do it. Label removal moves nothing. It beats all three
stupid baselines 6/6 to 1/6.

Three qualifications, all load-bearing:
- the result is about a **faithful re-implementation of the frozen selection
  principle in a clean arena**, not about `tnn2_frozen_ref.zag` itself. The
  frozen cores were not used because C501/C504/C505/C508/C509 live in the exact
  paths the claim would rest on; the two behaviours that mattered most were
  replicated as explicit switches so their effect could be measured instead.
- the suppression is a **pair** of mechanisms (price + lower-index tie-break),
  not one. A single-mechanism account of "why it does not predict" is wrong.
- the architecture is **not name-blind**: four operator codes carry semantics
  inside the relation namespace, and renaming them changes a choice.

## 13. Boundaries

Six fixtures, one world each, no repetition, no error bars. Priors are seeded
by the grader, not learned in-run (except the adversarial bar). One `W_COST`,
one certainty scale, one arena geometry. The fixtures are deliberately built so
that prediction is *tempting* on 4 of 6 cases; a world where prediction is
correct on 1 of 6 and retrieval is unavailable was not tested. Case 2's margin
is **8 points, one cost step**, on a 255 scale -- the A1 amendment moved it
from a tie to a one-step win and it should be treated as a boundary, not a
result.

## 14. Next experiment

1. Move the four operator codes out of the relation namespace into a separate
   operator band and re-run; K-ISOMORPH should go from FAIL to PASS or be shown
   to be unfixable, which is itself the answer to whether the family can be
   made name-blind.
2. Port the same six-route argmax onto the frozen `try_family` / `bp2_select`
   paths in a world where the six routes are all expressible, to convert
   "faithful re-implementation" into "the frozen cores do this".
3. Repeat case 2's fixture 100x with perturbed W_COST to put an error bar on
   the 8-point margin, and add a 7th case where retrieval is unavailable and
   the prior is 100% accurate -- the case where suppression should be
   *impossible* and the architecture must be shown to pay for it.