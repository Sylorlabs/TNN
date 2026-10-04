# CANDIDATES — frozen policy space C1..C5 (2026-09-22)

Authored apparatus (declared in RUN_PREREG §2). Each candidate is a
precise, implementable modification of the askfirst decision procedure.
The exact Zag rule code lives in `candidates.zag.inc` (generated single
source of truth, pasted into proposer and subject). The proposer
SELECTS by proxy simulation; the hands never choose.

## C1 — CONSULT-ON-CHANNEL (targets GAP-1)

Mechanism: consult iff (c != NEW) OR (channel packet present, cidx != -1).
Causal argument: on ADV-OLD items the pre-channel verdict is wrong-NEW
and nothing fires; but an independent-channel packet IS present. The
presence of unexamined independent information is itself a reason to
look — Micah's ask-for-more-info principle extended: ask when more info
EXISTS, not only when undecided. Expected: fixes the 2 ADV-OLD misses;
adds 2 consults (the ADV-OLD items); N-clean/O-clean/NEITHER have silent
channels, unchanged.

## C2 — THIN-MARGIN CONSULT (targets GAP-1)

Mechanism: consult iff (c != NEW) OR (c == NEW AND (sn - so) <= 2).
Causal argument: correlated-wrong agreement hides in thin margins; a
2-point margin on 3 relations is one flipped relation from a tie.
Expected: also fixes ADV-OLD (their margin is exactly 2), but consults
every thin N-clean item too (their margins are also 2, channels silent
→ consult confirms, wasted ops). Higher cost than C1 for the same fix.

## C3 — SILENT-ECHO WITHHOLD (targets GAP-1)

Mechanism: after consult, if the channel was SILENT, WITHHOLD (distrust
any verdict no independent channel confirmed).
Causal argument: a verdict no independent source checked is a guess.
Expected: HARMFUL — withholds the 6 correct O-clean installs (their
channels are silent). The proxy simulation should reject this; a
deliberation that keeps it has failed.

## C4 — LEAN-RECOMPUTE (targets GAP-3)

Mechanism: consult recompute evaluates ONLY the corrected relation
(2 ops) instead of all 3 (6 ops). Consult extra cost 16 → 12.
Causal argument: the channel corrects exactly one anchor; the other two
relations' contributions are unchanged — recomputing them is waste.
Verdicts bit-identical by construction (same arithmetic, fewer terms).
Expected: acc/wrong unchanged, cost 424 → 360. A pure free lunch.

## C5 — UNANIMITY-INSTALL (targets GAP-1)

Mechanism: install NEW/OLD only on a 3-0 relation sweep (|margin| == 3);
else WITHHOLD.
Causal argument: installs should require unanimous corroboration.
Expected: HARMFUL — observed margins never reach 3, so every install
becomes a withhold; accuracy collapses toward the degenerate baseline.
The proxy simulation should reject this.

## Composition

Candidates touch disjoint stages (consult trigger: C1/C2; post-consult
verdict: C3; consult cost: C4; install bar: C5) and compose in id order.
C1+C2 consult-trigger = OR. Kept candidates persist across rounds, so
the loop compounds: each round's champion is the previous round's
kept set, and the proposer re-simulates the remainder against it.
