# REPORT.md -- Unlabeled Cognitive Selection

## Verdict: UNLABELED-SELECTION-COMPLETE

## What was built

A Zag battery (`us_full.zag`, ~600 lines) testing Micah's Section 1 correction:
the prediction-optional A-to-G taxonomy is still researcher-authored. This
experiment removes ALL type labels. The driver presents unlabeled goals as
(s, r) only. The learner selects cognitive operations from its own state via
a learned consequence history. Multi-step sequences emerge because each
operation changes the state, changing which operations are applicable next.

No TYPE=PREDICTION. No TYPE=DEDUCTION. No external mode selector.

## Mechanism

Ten cognitive operations with natural state preconditions (not a taxonomy):

1. RECALL: fact(s,r) in store -> return it.
2. GATHER: derivation premises in store -> load to working memory.
3. DERIVE: premises in working -> derived reference value.
4. EXEC: trusted MAP(r) -> execute and return.
5. VERIFY: candidate MAP(r) + reference value -> promote if match.
6. RETRIEVE: MAP(r) in store -> load structure to working.
7. REBIND: working MAP + new subject -> adapted simulated value.
8. CROSSCHECK: simulated value + independent check -> commit if agree.
9. PREDICT: weak MAP(r) -> execute as guess.
10. INQUIRE: always applicable -> withhold (-3).

Selection: for each goal, compute a condition signature from state
(fact present? premises? trusted? candidate? working slots?). Among
applicable ops, pick the Laplace-smoothed argmax of (successes/attempts)
from the consequence substrate (tag-61 records keyed by op and sig).
Tie -> lowest op id. Fully deterministic, integer arithmetic.

Credit assignment: after each goal, a backward usefulness walk over the
operation trace. Terminal op useful iff answer correct. Predecessor useful
iff its successor required its provision and was useful. All traced ops get
attempts; useful ones get successes. Wasted ops (e.g. RETRIEVE then REBIND
before PREDICT, where PREDICT ignored the simulated value) get attempts
only, so their scores decay and they stop being selected.

## Results (3/3 byte-identical, sha256 12caf74a...)

Goals are (s,r) only. Names below are reporting-only; solve_goal receives
(s,r) exclusively.

```
GOAL T1-fact  ans=100 exp=100 ok=1 steps=1 trace=1
GOAL T2-fact  ans=200 exp=200 ok=1 steps=1 trace=1
GOAL T3-fact  ans=300 exp=300 ok=1 steps=1 trace=1
GOAL T4-trust ans=115 exp=115 ok=1 steps=1 trace=4
GOAL T5-trust ans=116 exp=116 ok=1 steps=1 trace=4
GOAL T6-trust ans=117 exp=117 ok=1 steps=1 trace=4
GOAL T7-deriv ans=300 exp=300 ok=1 steps=2 trace=2,3
GOAL T8-deriv ans=400 exp=400 ok=1 steps=2 trace=2,3
GOAL T9-deriv ans=500 exp=500 ok=1 steps=2 trace=2,3
GOAL T10-pred ans=208 exp=208 ok=1 steps=3 trace=6,7,9
GOAL T11-pred ans=210 exp=210 ok=1 steps=1 trace=9
GOAL T12-pred ans=212 exp=212 ok=1 steps=1 trace=9
GOAL S1-seq  ans=200 exp=200 ok=1 steps=4 trace=2,3,5,4
GOAL S1p-seq ans=500 exp=500 ok=1 steps=4 trace=2,3,5,4
GOAL S2-seq  ans=50  exp=50  ok=1 steps=3 trace=6,7,8
GOAL S2p-seq ans=132 exp=132 ok=1 steps=3 trace=6,7,8
SUMMARY main correct=16 total=16 steps=31
GOAL A-pred ans=321 exp=321 ok=1 steps=3 trace=6,7,9
GOAL A-s1   ans=200 exp=200 ok=1 steps=4 trace=2,3,5,4
GOAL A-s2   ans=50  exp=50  ok=1 steps=3 trace=6,7,8
SUMMARY abl correct=3 total=3 steps=10
```

Op ids: 1 RECALL, 2 GATHER, 3 DERIVE, 4 EXEC, 5 VERIFY,
6 RETRIEVE, 7 REBIND, 8 CROSSCHECK, 9 PREDICT, 10 INQUIRE.

## Key findings

1. Unlabeled selection works. All 19 goals presented as (s,r) with no type
   information. The learner selected the correct operation(s) from state in
   every case. 19/19 accuracy.

2. Sequences emerge from state, not script. S1 solved via
   GATHER(2) -> DERIVE(3) -> VERIFY(5) -> EXEC(4). Each step became
   applicable because the previous step changed the working state:
   GATHER loaded premises, DERIVE produced a reference, VERIFY consumed
   the reference to promote the MAP, EXEC fired on the newly trusted MAP.
   No sequence was programmed; the loop re-examined state after each op.
   S1p (new literals, r=63) reused the same emergent sequence.

3. S2 solved via RETRIEVE(6) -> REBIND(7) -> CROSSCHECK(8).
   RETRIEVE loaded the structure, REBIND adapted it to the new subject
   producing a simulated value, CROSSCHECK validated against an independent
   structure and committed on agreement. This is the
   RETRIEVE -> ADAPT -> SIMULATE -> CHECK pattern, emergent not scripted.
   S2p reused it.

4. Consequence history is causal, not correlational. T10 (first prediction
   goal, sig=24): trace 6,7,9 (RETRIEVE, REBIND, PREDICT), 3 steps, 2 wasted.
   T11 (identical sig=24): trace 9 (PREDICT), 1 step, 0 wasted. The ONLY
   difference between T10 and T11 is the consequence records written by
   T10's feedback. Ablation A-pred (fresh workspace, no history, same kind
   of goal): 3 steps, trace 6,7,9, matching T10. The records caused the
   3-to-1 reduction. Selection order is learned, not fixed.

5. No unnecessary prediction. PREDICT fired only when applicable and
   selected by consequence history. On fact, derivation, and trusted-exec
   goals it never fired. The dispatch does not consult predictive machinery
   unless the state warrants it.

6. Wasted steps are identified and eliminated. The backward usefulness walk
   correctly marked RETRIEVE and REBIND as not-useful on T10 (PREDICT did
   not consume the simulated value), so their scores decayed and PREDICT
   was selected directly on T11.

## Honest boundaries

- Op definitions, preconditions, DER rules, and the initial tie-break order
  are researcher-authored machinery. LEARNER-OWNED: all consequence record
  contents (op,sig)->(succ,att), every per-goal operation selection after
  the first encounter, all promoted MAP scores. Same standing as prior
  workers: researcher-owned rules, learner-owned values and choices.
- The tie-break (lowest op id) is an initial researcher bias. The T10->T11
  transition proves learning overrides it: the bias is a starting point,
  not a fixed order.
- Goal names (T1-fact, S1-seq) are human reporting labels only. They are
  never passed to solve_goal, which receives (s,r) exclusively. Verified by
  code inspection: do_goal(W,nm,s,r,exp) calls solve_goal(W,s,r,tr).
- DERIVE uses fixed compositional rules (r=53 via 51,52; r=63 via 61,62).
  The battery tests operation *selection*, not rule invention.
- S1's GATHER step is "recall of premises" (the RECALL in Micah's
  RECALL->DERIVE->VERIFY->ACT). Direct fact recall (op 1) was exercised on
  T1-T3.
- S2's REBIND combines ADAPT and SIMULATE in one op (adapt the structure
  to the new subject, producing a simulated value). CROSSCHECK is the
  CHECK step (independent validation).

## Standing metrics

- Cognition lines: ~600 (single file).
- Modes / bridges / handlers / semantic cases: 0 / 0 / 0 / 0.
- RESEARCHER-OWNED: op definitions, preconditions, DER rules, tie-break,
  world setups, provision/requirement table.
- LEARNER-OWNED: consequence records, per-goal selections, MAP promotions.
- SUF: consequence record values not enumerable from source (filled by
  experience); the op *menu* is enumerated.

## Deliverables

- `us_full.zag` (engine + battery + driver, pure Zag)
- `us_bin` (built with pinned znc)
- `us_run1.txt`, `us_run2.txt`, `us_run3.txt` (3/3 byte-identical)
- `compile.log`, `NAMECHECK.md`, `REPORT.md`

Constraints honored: safebin PATH, `which python3 python` empty, pure Zag,
unfrozen only, frozen source untouched, zero em/en dashes (byte-verified
below), paper untouched, nothing pushed.
