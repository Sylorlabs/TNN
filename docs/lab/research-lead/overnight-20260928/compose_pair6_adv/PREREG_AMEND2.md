# PREREG_AMEND2: Correction to the frozen K5 detailed derivation (GEN Q2)

Committed BEFORE the official GEN runs. Transparent amendment per the
AMEND1 precedent: the error is reported, not hidden. The measurable K5
bars (ANS=5, TRIES=47, WIDEN=1) are UNCHANGED and were matched exactly;
only the explanatory parenthetical and the round-by-round derivation are
corrected. No implementation change.

## The error

PREREG Section 5 derived G's Q2 contract as inmask1={1}, inmask2={2},
from the misleading teach2(m3,211,212,423). It forgot the fourth Q2
teaching fact: teach2(m3,202,202,404). observe2 unions observed kinds,
so after all four teachings G's contract is inmask1={1,2}, inmask2={1,2},
outmask={2} (not {1}|{2}).

## Consequences

- G(202,202) is ADMITTED in round 1 (both observed-kind checks pass),
  so the round-1 trace contains INTER2=404, not a rejection.
- The parenthetical "G's contract grows inmask1/inmask2 {1}|{2}" is
  incorrect: the contract is already saturated at {1,2}|{1,2} before
  the run, so no growth occurs or is needed. The operative mechanism is
  exactly as designed: fixpoint (no new tries, no new pool values)
  triggers WIDEN=1, the admission-off phase exhaustively tries the
  remaining pairs, and G(3,2)=5 (INTER2=5) succeeds end-to-end.
- The round-by-round INTER/INTER2 sequence in Section 5 is superseded
  by the observed trace; the frozen measurable bars stand.

## Corrected K5 bar (measurable part unchanged)

GEN Q2: WIDEN=1 fires exactly once (fixpoint: a full round with zero new
tries and zero new pool values), the admission-off phase runs, and the
run ends ARM=GEN PROB=Q2 ANS=5 TRIES=47. G's contract starts saturated
(inmask1={1,2}, inmask2={1,2}) and is not the binding constraint; the
binding constraint is the observed-kind admission, which the fixpoint
correctly identifies as exhausted before widening.
