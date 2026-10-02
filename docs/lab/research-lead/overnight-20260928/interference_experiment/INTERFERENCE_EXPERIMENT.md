# TNN-2 Memory Interference Experiment

Date: 2026-10-01. Experimenter: Memory Interference Experimenter (subagent).
Variant: unfrozen TNN-2, cognition byte-identical to frozen build `f4de7ff46`.
Status: COMPLETE. 3 runs byte-identical (cmp clean).

## Question

Micah's lifetime measure: "memory under long interference." Does TNN-2's
fixed eviction policy (3-step eviction, directional bid, PRO-clock protection)
preserve useful learned structures under sustained interference, or does it
catastrophically forget? And does the policy respect usefulness (access
patterns)?

This is a diagnostic run on an UNFROZEN variant to confirm and refine the
transfer analysis `475c57e23` P4 finding with a controlled retention curve.
No eviction policy fix is proposed or implemented here.

## Method

Task A (the important memory): teach 4-hop chain (1,11)->(2,11)->(3,11)->(4,11);
query (1,40) triggers trial loop, promotes MAP + shadow fact. Criterion:
requery(1,40) == 5.

Baseline (pre-interference, content-verified): MAP node 45 (bid 2, never
protected), root op cell node 30, 18 cells (8 winner + 10 rejected-trial
garbage), chain facts at nodes 2,3,4,5, shadow fact node 46 (bid 0,
PRO-protected with 12-event clock).

Interference: V unrelated teaches ev_teach(W,700+i,41,i), V in
{0,1000,1050,1100}. Volumes span the eviction-pressure onset (the 1024-node
budget binds near V=1000; pre-pressure volumes 500/900 show zero disturbance
in pilot runs and were dropped for runtime).

Two modes:
- IX-1: no refresh. Pure retention curve.
- IX-2: re-query (1,40) every 10 interference events (refreshes PRO clock
  and adds USE edges); stop refreshing on first miss, record fail_at.

White-box (content-verified, read-only): MAP survival (node id 45 + tag),
op-cell count (tags 101-104), chain fact survival (node id + (s,r) content),
shadow fact survival (node id + (s,r) content), bids, PRO status,
re-execution via t2_exec (only if root still an op cell), then a fast
read-only activate check for answer retrievability last.

Critical probe fix: evicted slots are reused by interference facts, so
survival checks verify node id AND tag AND (s,r) content, not just slot
liveness. An earlier probe version measured liveness only and falsely
reported survival; it was discarded and rebuilt.

## Results

All values from interf_run1.txt; interf_run2.txt and interf_run3.txt are
byte-identical (cmp clean, 3x).

### IX-1 retention curve (no refresh)

| V | map | cells | chain/4 | shadow | reexec | requery | live_nodes |
|---|-----|-------|---------|--------|--------|---------|------------|
| 0 | 1 | 18 | 4 | 1 | 5 | 5 | 46 |
| 1000 | 1 | 8 | 4 | 1 | -999999 | 5 | 1022 |
| 1050 | 1 | 0 | 4 | 0 | -999997 | -2 | 1022 |
| 1100 | 1 | 0 | 4 | 0 | -999997 | -2 | 1022 |

### IX-2 retention with refresh (every 10 events)

| V | fail_at | map | cells | chain/4 | shadow | reexec | requery |
|---|---------|-----|-------|---------|--------|--------|---------|
| 0 | -1 | 1 | 18 | 4 | 1 | 5 | 5 |
| 1000 | -1 | 1 | 8 | 4 | 1 | -999999 | 5 |
| 1050 | -1 | 1 | 0 | 4 | 1 | -999997 | 5 |
| 1100 | -1 | 1 | 0 | 4 | 1 | -999997 | 5 |

fail_at=-1 means the refresh query never missed at any volume.

## Analysis

### 1. Eviction order is fixed and structural, not usefulness-ranked (IX-1)

At V=1000 (memory at cap, 1022 live nodes) the measured destruction order is:

1. Graph cells first: 18 -> 8 (the 10 rejected-trial garbage cells plus 2
   winner cells evicted). Cells carry bid 0 and no PRO edge; they are the
   global minimum and die first.
2. Executable structure breaks while facts persist: reexec=-999999 (graph
   disconnected) but shadow=1, chain=4, requery=5.
3. Shadow fact (the memorized answer) dies at V=1050: its PRO clock expired
   (12 events, never refreshed in IX-1) and its bid is 0. requery=-2:
   catastrophic forgetting of the answer.
4. Chain facts (the evidence) survive at all volumes: each carries one DEP
   edge from the MAP (bid 1), which outranks the 0-bid interference facts.
5. MAP survives as a fossil at all volumes: bid 2 (self SUP+USE), never
   protected, but never the minimum while 0-bid nodes exist.

The executable structure is strictly the most fragile component. The "how"
dies before the "what."

### 2. The dissociation: refresh saves the answer, not the procedure (IX-2)

Refresh every 10 events keeps the shadow fact PRO-protected at every volume
(fail_at=-1 throughout; shadow=1 and requery=5 at V=1050/1100 where IX-1
lost both). The fixed policy does respect access recency for facts.

But the cell counts in IX-2 are identical to IX-1 at every volume (18/8/0/0).
Refresh does nothing for the executable graph: cells have no PRO edge, the
(1,40) query never touches them, and no USE edge reaches them. The procedure
rots at exactly the same rate whether or not the answer is rehearsed.

So under the fixed policy a continuing learner keeps its rehearsed answers
while losing the executable structures that produced them. The MAP becomes a
fossil pointer to a dead graph: map_same_id=1 at every volume, but with
nothing left to execute.

### 3. Answer to the question

Does the fixed policy preserve useful learned structures under sustained
interference? For declarative facts that are re-accessed, yes (IX-2). For
the executable graphs that constitute the learner's procedures, no: they
are the first thing evicted, they cannot be protected by use, and their
loss is invisible to the fact-level retention metrics.

Does the policy respect usefulness? It respects access recency, not
structural importance. A MAP with a dead graph keeps its standing bid of 2
forever; the cells that made it executable die at bid 0 without any
mechanism for the learner to mark them worth keeping. There is no
learner-owned retention priority; the policy is fixed and the learner
cannot change what it protects.

This is the architectural pressure point for the one-system-rule question
"what general learner-owned memory representation would let one frozen
learner preserve newly useful knowledge, dependencies, hypotheses and
structures": the current answer is that nothing in the fixed policy
distinguishes a load-bearing graph cell from garbage. Any future mechanism
must give the learner a way to mark structural importance, not just rely on
access recency.

## Standing architectural metric (variant delta vs frozen)

RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (no cognition changes; probe only)
LEARNER-OWNED STRUCTURAL DECISIONS: 0
SOURCE-ENUMERABLE FORMS: all (unchanged)
SUF DECISIONS: 0
LEARNER-INTERNAL CRITERIA: 0
REUSE EVENTS: observed via requery/reexec
REVISION EVENTS: 0
COGNITION LINES: 0 added, 0 modified (probe driver only)
MODES / BRIDGES / HANDLERS / SEMANTIC CASES: 0 / 0 / 0 / 0

## Verdict

INTERFERENCE-EXPERIMENT-COMPLETE.

Retention measured on unfrozen variant (cognition byte-identical to frozen
f4de7ff46), 3 byte-identical runs. Eviction order under interference:
graph cells (bid 0) -> shadow fact (bid 0, PRO expired) -> chain facts
survive (bid 1 via MAP DEP) -> MAP fossil (bid 2). Refresh preserves the
memorized answer at all volumes but does not slow procedure decay by any
measured amount. The fixed eviction policy respects access recency for
facts and is blind to structural importance.
