# Mini-Lifetime Worlds: Seal Record

**Status:** SEALED. Hashes recorded. Contents not inspected beyond hashes
until evaluation (evaluation is this run; the sealer and runner are the
same agent, documented as a limitation).
**Date:** 2026-10-01.

## World spec

File: `ml_world.zag`. SHA-256:
`18efd9e8747bb26e3b4f409595a15999cbcd8b10db92bae29a104f4359db2f45`.

The spec defines three minis, hardcoded in the driver (no external
world files). The hash above is the seal.

## Design (from MINI_LIFETIME.md, no contents beyond structure)

- R_TEACH=1 (chain-building facts), R_PROBE=50 (queries).
- A-mini: subjects 1,2,3. Per s: (s,1,1000+s), (1000+s,1,2000+s),
  (s,1,3000+s), (3000+s,1,2000+s). Probes: (s,50) expects 2000+s.
  TRIAL-EXPECTED. No direct (s,50) fact taught.
- B-mini: subjects 11,12,13. t=11 uses s_t=1, etc. Teach (t,1,1000+s_t).
  Trial recruits A's (1000+s_t,1,2000+s_t). Probes: (t,50) expects
  2000+s_t. TRIAL-EXPECTED.
- C-mini: contradictions via ev_observe:
  - (1001,1,2001)->9001 (SHARED, in B MAP provenance for t=11)
  - (1002,1,2002)->9002 (SHARED, in B MAP provenance for t=12)
  - (3001,1,2001)->9003 (UNSHARED, redundant path)
  - (1003,1,2003)->9004 (V2-hole trap for subject 3)
  Probes: 3 revised-A (LOOKUP-EXPECTED), 3 B (LOOKUP-EXPECTED),
  1 V2 trap (white-box).

## Trial-must-run validation

Per design Section 5: no TRIAL-EXPECTED probe's (s,r) has a direct
fact. Verified by construction: all teaches use relation 1, all
probes use relation 50. The acceptance micro-world (ml_accept.zag)
confirms trial runs and promotes on this pattern.

## Binaries (world drivers)

- Build A driver: `ml_world_a_bin`, SHA-256
  `6f94b62418b7eb8294fc338488b2ca0b84f0c8852dfa6133b09b23496dc9de4c`.
- Build B driver: `ml_world_b_bin`, SHA-256
  `f7b72afce45ae4f268a79260110c1e03ca4bd19dc383b05f9bfc6876cd8ddae7`.
- Full hashes in `WORLD_HASHES.txt`.

## Budget

Design budget: 500-600 nodes, 250-350 events. Actual usage not
instrumented in this run (DYN-1 profiles deferred to follow-up).
No budget-guard flag triggered (run completed).
