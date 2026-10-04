# Amendment 1 to PREREG_CU3_ADV (transparent, re-frozen)

**Date:** 2026-09-29
**Amends:** PREREG_CU3_ADV.md (commit f92aad7a4)
**Status:** FROZEN (this commit). Attack code is built and run strictly after.
**Reason:** The frozen X-CU3-1b empirical attempt (orphaned contest via
split-failure, then feed at the exact state) has a shadowing flaw found on
closer analysis: driving split-failure requires extra episodes at other
states, which create fresh mask-0 ACTIVE entries once the target entry goes
ST_CONFL; those fresh entries then match the probe state in `find_entry`
before `find_conflicted` is ever consulted, so the probe would not test the
absorb path at all and could produce a false KILL.

## The correction (frozen)

X-CU3-1b is operationalized as a runtime invariant scan instead of the
single fragile construction. The attack question is unchanged: can a
ST_CONFL entry ever lose its exact-state live episodes to EP_SUP (which
would make `find_conflicted` miss and resurrect the X-CU2-1 bypass)?

- Code proof (unchanged): the sole EP_SUP writer is `contest_feed`,
  reachable only through the ACTIVE path of `learn_episode`; `find_entry`
  never returns ST_CONFL entries; `merge_pass` only merges ST_ACTIVE.
- Empirical: after every workspace built in this red team (flood W,
  scope probes W2/W2b, split-failure W3), scan every ST_CONFL entry and
  flag any EP_SUP episode inside it.

Kill criterion (unchanged in substance): any EP_SUP episode found inside a
ST_CONFL entry, or equivalently a fresh ACTIVE entry created plus
`fu_predict` returning 1 at an exact contradicted state ->
**H-CAUSAL-UNIFIED3 KILLED**. If the scan is clean on all workspaces ->
X-CU3-1b holds, F2 confirmed empirically.

All other attacks (X-CU3-1a, X-CU3-1c, X-CU3-2a/b/c/d, X-CU3-3, X-CU3-4)
and their kill criteria are unchanged.
