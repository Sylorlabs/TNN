# PREREG AMENDMENT 2: R4b/R4c MAP Training via ev_query

Date: 2026-10-02. Worker: H-FALLBACKFIX-1.
Amends: PREREG_AMENDMENT1.md, training method.

## Change

R4b/R4c 1-link MAPs are trained via ev_query (the standard MAP
formation path: ev_teach fact, then ev_query triggers mp_run /
t2_trial which promotes the 1-link chain graph), not via direct
t2_trial calls.

## Rationale

Direct t2_trial cannot reliably train 1-link MAPs in the dense
layered graph context: t2_trial tries k=2,3,4 chain lengths before
falling back to 1-link, and in the dense 2-wide graph the longer
chain attempts interfere (measured: t2_trial declined idx=2,3 while
succeeding on idx=0,1; a hand-built t2_asm_chain plen=2 also failed
verification). The unified red-team's rt_train1 (the reference R4b/R4c
implementation this ports) uses ev_query for 1-link MAP training.

Feasibility verified 2026-10-02: 28 MAPs via ev_query train in 0.2s,
MAP-COUNT=28, zero failures, well within workspace capacity. The
AGENTS.md ev_query stall lesson (19 MAPs) does not apply here; the
2-wide 28-MAP world trains cleanly.

No kill bar changes. K2/K4/K5 thresholds and timeouts unchanged.
