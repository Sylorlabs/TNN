# PREREG: Active Verification Build (A1 re-observe + A2 cross-check)

Date: 2026-09-30 UTC
Builder: Active Verification Builder (subagent)
Spec: docs/lab/research-lead/overnight-20260928/verify_attack/VERIFY_RESULT.md
  (frozen, 483b0e61f), sections 4 (A1/A2) and 5 (revision policy)
Base: docs/lab/research-lead/overnight-20260928/verify_build/v6_verify.zag
  (BUILD-PASS, a07f9b9a6)
Attack worlds: docs/lab/research-lead/overnight-20260928/verify_attack/gen_verify.zag
  (V1..V5, committed)

This prereg is committed alone BEFORE any implementation. No source
has been written or modified at the time of this commit.

## Problem

The verification build (a07f9b9a6) implements detection, provenance,
doubt, hedging (A3), and source-priority revision (A4). It does NOT
implement A1 (re-observe) or A2 (compositional cross-check). The
honest scope states: the contestant "detects, records, hedges, and
prioritizes sources, but does not yet spend asks to resolve doubt."

The frozen spec defines:
- A1 (re-observe): emit an observe request for a SUSPECT fact even
  though it is known. Requires lifting the known==0 gate on
  want_observe. Costly; budgeted like C8 ask costs.
- A2 (cross-check): for a SUSPECT fact (e,a), check compositional
  consequences. If (e,a) participates in a relation chain, verify
  the chain still resolves. (C4 path.)

The spec warns: "the known==0 gate must be lifted and ask costs
budgeted, or re-observation degenerates into the always-observe
policy the generic attack already refuted as unscored."

## Design: bounded A1

A1 fires only on SUSPECT facts, with a hard per-episode budget.

- Trigger: a test query of form fact|e|a (or fact2|e|a) where the
  fact slot for (e,a) has SUSPECT flag set (vflag==1), AND the
  re-observe budget for this suspect episode is > 0.
- Action: in addition to the hedged A3 reply (stored|superseded),
  emit an observe request for (e,a) even though the fact is known.
  This lifts the known==0 gate ONLY for SUSPECT facts with budget.
- Budget: 1 re-observe per suspect episode. Tracked in verify slot
  bytes 22..23 (currently reserved): byte 22 = re-observes issued
  for this episode, byte 23 = episode id (incremented each time
  SUSPECT transitions 0->1). Budget check: byte22 < 1.
- Stopping rule (on observe_result for a SUSPECT fact):
  - If incoming value == stored value: clear SUSPECT flag,
    clear superseded, reset byte22. Doubt resolved by confirmation.
  - Else if incoming value == superseded value: keep SUSPECT set
    (P-source-priority still applies: EXPO stored beats OBSERVE),
    but record corroboration in byte23 high bit. No further
    re-observe (budget exhausted). The hedged answer stands with
    stronger evidence for the alternative.
  - Else (third distinct value): replace superseded with the new
    value, keep SUSPECT, budget exhausted. The newest contradiction
    is the live alternative.
- New suspect episode (SUSPECT 0->1 transition) resets byte22 to 0
  and increments the episode id in byte23 low 7 bits.

## Design: bounded A2

A2 fires only on SUSPECT relation slots during hop2 composition.
It is internal computation, not an ask, so it cannot degenerate
into always-observe. It is bounded by triggering only when a
SUSPECT relation is traversed.

- Trigger: a hop2|start|rel1|rel2 query where the relation slot
  for (start,rel1) or (mid,rel2) has SUSPECT flag set in VERR.
- Action (compositional cross-check): compute the chain via the
  CURRENT mapping. Then compute the chain via the SUPERSEDED
  mapping (substituting the superseded value for the suspect
  slot). Compare:
  - If current chain resolves and superseded chain resolves to
    the SAME value: the remap does not affect this composition.
    Record a consistency note; SUSPECT stays (the remap is still
    a fact) but the query answer is not hedged for this chain.
  - If current chain resolves and superseded chain resolves to
    a DIFFERENT value: the remap is compositionally live. Hedge
    the hop2 answer as current|superseded-chain-value.
  - If current chain FAILS but superseded chain resolves: strong
    evidence the remap broke a working composition. Keep SUSPECT,
    answer with the superseded-chain value annotated, and route
    a note to the conflict store.
  - If both fail: answer UNKNOWN (as before); no new signal.
- A2 does not clear SUSPECT by itself; it produces evidence that
  the revision policy or a future A1 can use. A2 never issues
  observe requests.

## Test worlds

- V1..V5 regenerated from committed gen_verify.zag (same as the
  verification build). A1/A2 must preserve DETECT=yes everywhere.
- V6 (new, committed in this work): the oracle lies twice about
  the same fact. Turn sequence: expo teach (e0,a0)=v0; observe
  (e0,a0)=w1 (lie 1, T2 fires, SUSPECT set); test fact|e0|a0
  (expect hedged v0|w1 AND one observe request = A1 firing);
  observe_result (e0,a0)=v0 (truthful re-observe, matches stored);
  test fact|e0|a0 (expect bare v0, SUSPECT cleared, no observe
  request). This tests the full A1 resolve cycle.
- V7 (new, committed in this work): relation remap with live
  composition. Expo relations (s,r1)=m, (m,r2)=fin; expo fact
  (s,r1) is the remap target. Observe remaps (s,r1) to m2 (T4
  fires, SUSPECT on relation slot). hop2|s|r1|r2 query: A2
  computes via current (m2, r2) and via superseded (m, r2).
  Expect hedged or annotated answer showing the compositional
  difference. Then expo re-teaches (s,r1)=m (correction);
  SUSPECT cleared; hop2 returns bare fin.
- CTL (control): the no-contradiction world from the verification
  build. Must show zero observe requests beyond the baseline
  (knowledge-gap asks only), conf_n=0, suspect_n=0.

## Frozen kill bars

- K1: Bounded A1/A2 specified AND implemented. A1: per-episode
  budget of 1, tracked in verify slot bytes 22..23, stopping rule
  as above. A2: fires only on SUSPECT relation traversal during
  hop2, compares current vs superseded chain, hedges when they
  differ. Source audit confirms the known==0 gate is lifted ONLY
  on the SUSPECT-with-budget path.
- K2: Doubt resolution measured. V6: after truthful re-observe,
  SUSPECT is cleared and the reply returns to the bare stored
  value; the full A1 cycle (doubt -> re-observe -> resolve) is
  demonstrated in the trace. V7: A2 produces a hedged/annotated
  hop2 answer where the baseline v6_verify gave a bare (possibly
  wrong) value or UNKNOWN. V1..V5 still DETECT=yes.
- K3: No degeneration. On V6+V7+CTL combined, the number of A1
  re-observe requests is <= the number of suspect episodes (each
  SUSPECT 0->1 transition yields at most 1 re-observe). An
  always-observe degenerate would issue an observe request on
  every test query for every known fact; the measured count must
  be bounded by suspect episodes, and CTL must show zero A1
  requests. Explicit metric: reobserve_n <= suspect_episodes.
- K4: Pure Zag at every stage (source, build via znc, execution,
  analysis). Zero Python invocations. Zero em-dash or en-dash
  bytes in committed files (byte-checked via grep). Each world
  (V1..V7, CTL) run 3 times; cognitive outputs byte-identical
  across runs. All stderr empty, exit 0.

## Falsification

This build FAILS if: V6 does not show the full A1 resolve cycle
(SUSPECT cleared after confirming re-observe); or V7 shows no A2
hedging where the compositional difference exists; or
reobserve_n > suspect_episodes on any world (degeneration); or
CTL shows any A1 request or any reply differing from the
v6_verify baseline; or any K4 purity check fails.

## Bar discipline

No kill bar is altered after results. If the implementation
misses a bar, the verdict is BUILD-FAIL with the miss named.
A1/A2 are additive; the A3/A4 behavior from a07f9b9a6 must be
preserved (V1..V5 DETECT=yes is a regression gate).
