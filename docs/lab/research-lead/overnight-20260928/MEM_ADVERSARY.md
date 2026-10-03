# H-MEM Adversary Verdict: MEM_ADVERSARY.md

**Date:** 2026-09-29
**Adversary prereg:** PREREG_MEM_ADV.md (commit ef71f58f2, frozen before
  any attack executed)
**Attack code:** mem_adv.zag (pure Zag) + MEM_ADV_RAW_OUTPUT.txt
**Overall verdict: H-MEM SURVIVES WITH DOWNGRADE**

All six frozen bars verify as written and governance is clean, so the
hypothesis is not killed. But the interpretation must be narrowed: the
evidence supports "argmin over an authored recent-window proxy selects
different policies on two authored streams" and not the stronger
readings ("developed an effective memory strategy", "data-driven
re-selection on every pressure event"). Details per attack below.

## M-A1: newcomer churn and hot-newcomer probe

**Verdict: NO-KILL on the kill criterion; DOWNGRADE on re-selection.**

The frozen kill criterion (evict a newcomer with strictly more window
hits than some surviving proc) did NOT fire, and the probe shows why
it cannot easily fire. Attack A1, phase 2: after pressure ev0, proc8
was queried x5 (uses=5, the LFU victim since incumbents had 6, window
cost 5). At pressure ev1 the table was:

```
LFU victim=slot0(proc8) cost=5
LRU victim=slot1(proc1) cost=0
FIFO victim=slot1(proc1) cost=0
LIFO victim=slot0(proc8) cost=5
RANDOM victim=slot2(proc2) cost=0
selected: LRU cost=0
```

The hot newcomer survived: argmin strictly preferred the 0-cost
policies over the policies victimizing proc8. Lemma (checked against
the source): a policy whose victim has h window hits costs exactly h,
so argmin can only evict a window-hot proc via an exact cost tie plus
the authored tie-break. The mechanism provably protects window-hot
procs from strict-argmin eviction. This is a point FOR the builder:
the suggested kill is unreachable by construction, and the probe
confirms the protection empirically.

The DOWNGRADE: phase 3 (pressure ev2) produced a 5-way cost tie at 0
with 4-policy victim agreement (LFU/LRU/LIFO/RANDOM all victimize the
unqueried newcomer proc9; FIFO dissents only on victim, not on cost),
and the unqueried newcomer was churned (uses=0, lastq=0). Combined
with the builder's own events 1-3 on both streams, post-first-pressure
"re-selection" never faces a substantive choice: the trace does not
discriminate, the authored tie-break decides, and the newcomer churns.
The MEM_RESULT.md language ("the selection is data-driven and
revisable (re-selection runs on every pressure event against the
current trace)") is technically true and substantively vacuous in the
tested regime. The builder's honest limitation #1 (newcomer churn) is
confirmed and is worse than stated: it is not just a missing
probationary period, it makes 6 of the 8 reported selections vacuous.

## M-A2: trace staleness (two regimes)

**Verdict: NO-KILL.**

800 ancient queries (regime 1: procs 0..7 x100) followed by a 20-query
recent regime (proc0 x20) selected LFU, exactly the same selection as
the baseline with only 8 ancient queries. The full candidate tables
were identical between the ancient-history and baseline runs. Ancient
history did NOT flip the selection. The windowed cost model makes
selection robust to arbitrarily large ancient history; staleness lives
only in the victim statistics, not in the choice.

Inspectability caveat (not a downgrade of the claim): the evicted
victim was printed as "proc1 uses=100 lastq=200", all 100 uses ancient.
The K-M2 trace display conflates lifetime statistics with recent
experience. A reader of the trace cannot tell that the "100 uses" are
all stale. The builder's limitation #3 is confirmed with a concrete
demonstration.

## M-A3: degenerate agreement

**Verdict: DOWNGRADE.**

Dedicated stream (procs 1..7 x5, proc0 never queried, single pressure):

```
LFU victim=slot0(proc0) cost=0
LRU victim=slot0(proc0) cost=0
FIFO victim=slot0(proc0) cost=0
LIFO victim=slot7(proc7) cost=5
RANDOM victim=slot3(proc3) cost=0
selected: LFU cost=0
```

3-policy victim agreement (LFU/LRU/FIFO on slot0) plus a 4-way cost tie
at 0 resolved by the authored tie-break. The "selection" among the tied
candidates is vacuous.

Tabulation of the builder's own 8 pressure events (MEM_RAW_OUTPUT.txt):
- A-e0: all victims distinct; LFU wins STRICTLY (1 < 2). Non-degenerate.
- A-e1/e2/e3: LFU/LRU/LIFO agree on the newcomer victim; winner-cost
  tie at 0; tie-break picks LFU.
- B-e0 (the headline event): LRU and RANDOM agree on victim slot3
  AND tie at cost 0; tie-break picks LRU.
- B-e1: LFU/LRU/LIFO agree on newcomer; RANDOM different victim, same
  cost 0; 4-way tie; tie-break picks LFU.
- B-e2/e3: LFU/LRU/LIFO agree on newcomer; winner-cost tie at 0.

7 of 8 events are degenerate (victim agreement and/or winner-cost tie
resolved by the authored tie-break). Exactly ONE event in the entire
experiment, stream A event 0, was a strict, non-degenerate,
experience-driven selection. The K-M5 "data-dependent selection"
narrative therefore rests on one strict argmin (A-e0) plus one
tie-break decision (B-e0, LRU over RANDOM). The "developed a strategy"
reading is downgraded accordingly.

## M-A4: independent recomputation

**Verdict: NO-KILL on the bars; DOWNGRADE of the frozen record.**

Re-derived every victim slot, cost, RANDOM index
(k = ((ev*7+3) % nstored)), tie-break application, and the vicA_ok /
vicB_ok check logic from the committed SOURCE. Findings:

- Stream A: all hand computations correct. Totals 17,13,9,7,6,3,9,4;
  last-query order p6 oldest through p7 newest; victims LFU->slot5
  cost 1, LRU->slot6 cost 5, FIFO->slot0 cost 3, LIFO->slot7 cost 2;
  RANDOM (ev0, k=3) -> slot3 cost 2, omitted from the prereg's
  hand computation but consistent with the program. Winner LFU
  strictly. K-M3a's "pre-pressure totals of 6 or more" holds
  (p4 = 6 exactly); first-evicted proc5 had the minimum total (3).
- Stream B: victims and costs correct (LFU->slot1 cost 6, LRU->slot3
  cost 0, FIFO->slot0 cost 10, LIFO->slot7 cost 4; window = seq 67..86
  = p7x4, p1x6, p0x10 as preregistered). BUT the prereg's frozen
  expectation "Winner: LRU, strictly" is WRONG: RANDOM (ev0, k=3)
  also victims slot3 at cost 0. The program output confirms the tie
  ("RANDOM victim=slot3(proc3) cost=0", "selected: LRU cost=0").
  LRU won by the authored tie-break, not strictly. The prereg also
  omits RANDOM's hand-computed victim/cost on both streams.
- vicA_ok / vicB_ok logic (`st_pid(W,5)==8` plus `has_proc(W,5)==0`,
  where has_proc searches by proc id, not slot) is confusingly named
  but correct: it verifies the evicted slot now holds the newcomer
  AND the evicted proc is gone.

No frozen bar fails as written (K-M1b requires selection=LRU,
victim=slot3, cost 0 strictly below FIFO's 10; all true). The
downgrade is to the record: the headline "Stream B selected LRU"
was a tie-break decision, and the prereg's "strictly" must be
struck. Any future citation of the B result must disclose the
LRU/RANDOM tie.

## M-A5: governance

**Verdict: NO-KILL (all checks pass).**

- Commit order: prereg 304918d7b is an ancestor of implementation
  75842e367 on branch tnn-native-lab; timestamps 2026-09-29 22:44:06
  UTC -> 22:45:15 UTC (69 seconds apart). Strictly precedes. PASS.
- No Python: no .py files anywhere in the work directory; the string
  "python" appears in builder files only inside "Pure Zag. No Python."
  declarations. The committed source contains no Python, and the
  verification below used only znc plus shell cmp. PASS.
- Independent reproducibility (stronger than the builder's own check):
  extracted mem_learn.zag from commit 75842e367, confirmed the
  worktree copy is byte-identical to the committed source, rebuilt
  with the pinned znc 2026.07.0-dev, ran the fresh binary twice:
  byte-identical via shell cmp; fresh output byte-identical via cmp
  against the committed MEM_RAW_OUTPUT.txt. PASS.

## M-A6a: window-size fragility

**Verdict: DOWNGRADE.**

Replicated both builder streams exactly and selected with several
window sizes on fresh stores (attack code, pure Zag):

Stream B: win=10 -> LFU (4-way tie at 0); win=20 -> LRU (tie with
RANDOM at 0, tie-break); win=40 -> LRU strictly (costs 6,0,10,6);
win=86 (full trace) -> LFU (tie LFU/LIFO at 6, tie-break).

Stream A: win=10 -> LRU (tie LRU/FIFO at 0, tie-break); win=20 -> LFU
strictly (costs 1,5,3,2); win=68 (full trace) -> LFU strictly
(costs 3,9,17,4).

Both streams' selected policies vary with the authored window
parameter. The K-M5 narrative ("stable popularity -> LFU, shifting
popularity -> LRU") holds only inside a window-size band that the
builder chose (20). With the full trace as the window, stream B
selects LFU, not LRU. The selection is (data x authored-window)-
dependent, not purely experience-driven. The window size is disclosed
as authored (builder limitation #4), and this attack shows it is
load-bearing for the headline result, not an incidental constant.

## M-A6b: held-out future

**Verdict: DOWNGRADE of the word "effective".**

Replicated stream A through pressure ev0 (window=20): selected LFU
strictly (cost 1), victims LFU->proc5, LRU->proc6, FIFO->proc0,
LIFO->proc7, RANDOM->proc3. Then scored each policy's victim against
two held-out 20-query futures (never seen by the selector):

- F1 (trend continuation: proc0 x20): LFU 0, LRU 0, FIFO 20, LIFO 0,
  RANDOM 0. The selected policy is tied-best.
- F2 (regime flip: proc5 x20, the evicted proc): LFU 20, LRU 0,
  FIFO 0, LIFO 0, RANDOM 0. The proxy's STRICT winner is the menu's
  strictly WORST performer on held-out future queries.

None of the six frozen bars measures future-query performance; they
measure the proxy. The cost model's rationale ("recent queries predict
near-future queries") is a stationarity assumption supplied by the
builder, and the learner contributes only argmin over the authored
proxy. "Effective" as a property of the developed strategy is therefore
unestablished by this experiment: under F1 the selection looks
effective, under F2 it is the worst choice, and nothing in the
experience distinguishes the two cases in advance. This does not kill
bounded L2 (the selection IS experience-driven); it kills the
"effective memory strategy" gloss. Correct characterization:
proxy-optimizing selection.

## What the evidence actually supports (narrowed claim)

After the attacks, the defensible bounded-L2 reading of H-MEM is:

1. On two builder-authored streams with the builder-authored
   window=20 cost model, argmin over replay costs selects LFU
   (strictly, once: stream A event 0) and LRU (by tie-break over
   RANDOM: stream B event 0). The selection is not hardcoded: it
   varies with the input trace.
2. The argmin mechanism provably protects window-hot procs: a policy
   victimizing a proc with h window hits costs exactly h, so a
   strictly-hot proc cannot be strictly-argmin-evicted (M-A1 probe
   confirms empirically).
3. Selection is robust to arbitrarily large ancient history because
   costs are windowed (M-A2: 800 ancient queries changed nothing).
4. Deterministic and independently reproducible from the committed
   source (M-A5).

What is NOT supported: that the learner "developed an effective
memory strategy" (effectiveness unmeasured, M-A6b; strategy choice
vacuous at 7/8 events, M-A3; post-first-pressure behavior is
newcomer churn, M-A1), that re-selection is substantive (tie-break
decides, M-A3), or that the LFU-vs-LRU separation is a pure property
of experience rather than of the authored window (M-A6a).

## Fairness notes (points for the builder)

- M-A1's suggested kill was unreachable by construction; I verified
  the protection rather than asserting the weakness. The mechanism is
  self-consistent: it never evicts the window-hottest proc by strict
  argmin.
- M-A2's suggested ancient-history flip did not occur. The windowed
  cost is a genuine robustness property, not just an authored
  convenience.
- M-A4 found the frozen arithmetic correct everywhere it matters for
  the bars; the single inaccuracy ("strictly") does not break any bar.
- M-A5 governance is fully clean, including a rebuild-from-source
  reproducibility check the builder had not performed.

## Commits (tnn-native-lab)

- ef71f58f2 PREREG H-MEM ADVERSARY FROZEN (attacks M-A1..M-A6,
  kill/downgrade criteria; committed before any attack executed)
- [attack evidence + this verdict: mem_adv.zag,
  MEM_ADV_RAW_OUTPUT.txt, MEM_ADVERSARY.md]

No Python was used anywhere in the adversary pipeline (Zag via pinned
znc 2026.07.0-dev; shell cmp/grep/sed for verification).
No em-dashes were used in adversary documentation, per loop style rule.
