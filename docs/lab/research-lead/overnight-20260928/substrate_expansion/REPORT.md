# Shared Substrate Expansion: Report

## Verdict: SUBSTRATE-EXPANSION-COMPLETE

Five behaviors driven by one shared consequence substrate, each with
a per-behavior ablation. All batteries PASS. 3/3 deterministic
byte-identical runs (sha256
8945d3d64b3b0be805f146dce9a67c02a4dc8adacf3603d3dca9377e8e52b4a2).

## Results by battery

### B1 policy (full=31 vs no-policy=30): PASS
Phase 1: policy stays 30. Phase 2: shifts to 45. Phase 3: new miss
gets guide action 45 (full) vs 30 (ablated). The ablation arm still
writes STRATEGY(45,0) successes (sub_best_action==45 asserted in both
arms); only the miss_inquire READ is gated. This is the read-gate
proof: same writes, different behavior.

### B2a withholding (full=31 vs no-withhold=29): PASS
4 queries on untaught (101,99). Full: -2,-2,-2,-3 with 36 verifies.
Ablated: -2,-2,-2,-2 with 48 verifies. Withholding saves 25% of
verifies (12). Return-code and compute differences both track the
withhold bit.

### B2b abandonment (full=31 vs no-abandon=27): PASS
8 queries. Full: q6=q7=q8=-4, abandoned=1. Ablated: q6=q7=q8=-3,
abandoned=0. Permanence: after teaching (101,99)=9999, full arm still
returns -4 (abandoned check precedes activation), ablated arm returns
9999. Abandonment is a permanent decision, not a per-query skip.

### B3 retention (full=31 vs no-retention=23): PASS
Adversarial setup: abandoned (1,99) uncertainties were given HIGH
generic bid (6 via type-2 self-loops) so the bid scan actively avoids
them; (2,99) uncertainties are the unboosted, non-abandoned control.
Full: first 3 victims are the (1,99) uncertainties (bid overridden),
census (1,99) 3 to 0, (2,99) untouched. Ablated: 0 (1,99) victims in
6 evictions, (1,99) census stays 3. The same life.state field written
by abandonment drives retention reclamation.

### B5 search-order (full=31 vs no-order=15): PASS
Subject 1 (rel-8 taught first, rel-7 second, rel-7 chain solves):
answer 14, 6 verifies, both arms (pre-pass has no records yet).
Subject 2 (same layout): answer 34, full arm 1 verify (pre-pass hits
via STRATEGY(7,1) from credit attribution), ablated arm 6 verifies.
Cross-arm vc1 equal (6=6). The same successes field that drives the
policy argmax (key_b=0) ranks trial candidates (key_b=1).

## Shared-fields evidence (the core claim)

- PURSUIT.consec_fail: B2a withholds at >=3; B2b abandons at >=6.
  One field, two thresholds, two behaviors.
- PURSUIT.life.state: B2b marks ABANDONED (decision); B3 reclaims
  abandoned structures first (execution).
- STRATEGY.successes: B1 policy argmax (key_b=0); B5 search-order
  ranking (key_b=1). Disjoint namespaces, same field.

## Honest limits

- Abandonment permanence is a design choice (check before activation);
  revival mechanisms are future work.
- Retention reclaims one abandoned structure per evict_node call;
  under extreme pressure the bid scan still runs between reclaims.
- Search-order credit attribution only fires for chain-attributable
  successes; sum/single-hop wins do not train order.
- The config bitmask is researcher-set per battery, not learned.
  Learner-owned arbitration between the five reads is future work.
- 0 modes, 0 bridges, 0 handlers, 0 semantic cases added.

## Reproduction

- Source: se_base.zag + se_machinery.zag + se_behaviors.zag +
  se_driver.zag = se_full.zag (1930 lines).
- Compiler: pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Binary: se_bin (sha256 58a2ea70d7c012857362f0c65d0f0d68...).
- Runs: se_run1/2/3.txt, byte-identical.
- Base: frozen sc_base.zag a29972ca (untouched). Prior build fa8405a90.
