# R32 V24 — Explicit Future-Resolution Horizons

Status: **REFERENCE_ONLY / HORIZON SIGNAL RETAINED / RUNTIME REPLACEMENT REJECTED**

The multi-horizon models validate as useful forecasts: policy-level horizon choice agrees with the oracle-best horizon 93.96% of the time and realizes mean delayed continuation utility 0.0947 versus oracle 0.1149.

But replacing the mature source-7 INSPECT Q with the horizon head is not acceptable. Hardening gives no-unique UNKNOWN **0.605** and resolvable success **0.345**; replacement falls to **0.12**, reversal to **0.17**.

Causal classification: **decision decomposition failure**, not evidence that temporal forecasts are useless. Horizon value and source-specific inspect value solve different subproblems. Retain the horizon signal as a diagnostic/feature; do not substitute it for INSPECT. Next learn the pairwise delayed-utility advantage of INSPECT over the best terminal action directly, which places the decision on one causal utility scale without global Q replacement.
