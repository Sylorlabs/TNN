# Ledger Duplicate Resolution: C361-C368

**Date:** 2026-10-02
**Issue:** Concurrent watchdog collision produced duplicate ledger numbers C361-C368.
**Resolution:** Both entries are canonical; history is not rewritten. Future ledgers continue from C374.

## Duplicates (both entries stand)

### C361 (2 entries)
- `da3e4361f`: XP-HIER-1 PASS (hierarchical composition, Z2 reuses Z1)
- `c721bcc61`: IVWC BUILD-PASS (learner commitment -> world consequence -> learner-owned evaluation, K1-K6, sealed calibration 113 vs 116)

### C362 (2 entries)
- `fa327b97b`: MULTIPOISON (tax additive per bit, U6 retires independently)
- `b01b36a5e`: XDOMAIN-CAUSAL-ADAPT BUILD-PASS K1-K7 (causal->intervention with required adaptation, direct copy fails, 3/3 byte-identical)

### C363 (2 entries)
- `d880241b9`: CAL-PASS (consensus-gated tolerance, 26/26 agreement)
- `2ec76f977`: L3-INR design freeze (prereg K1-K12/KC0A-D frozen, implementation queued)

### C364 (2 entries)
- `828c0a7a4`: POOLREPAIR (A1 NOT-FIXED honest negative, pool manageable)
- `5c7c871d8`: L2-SUBSTITUTE-XDOMAIN BUILD-PASS K1-K8 (arithmetic SUM substituted into planning with runtime interface adaptation, decoy rejected, 3/3 byte-identical)

### C365 (2 entries)
- `0f5ecbba8`: LEN5-PASS (length-5 does not blow up, 14x law)
- `f3638645c`: L2-TRUNCATE-XDOMAIN BUILD-PASS K1-K8 (learner-chosen k=3 truncation, full fails NOTRUNC fails, 3/3 byte-identical)

### C366 (2 entries)
- `04036254e`: XP-HIER-2 PASS (three-level hierarchy, recursion generalizes)
- `d71578446`: L2-EXTEND-XDOMAIN BUILD-PASS K1-K8 (learner-chosen k=4 minimal extension, unextended fails, 3/3 byte-identical)

### C367 (2 entries)
- `1a0ae353a`: GENREC-INTEGRATION (reclamation now default in CALR)
- `eec892b69`: L2-SPECIALIZE-XDOMAIN BUILD-PASS K1-K8 (learner-chosen nf=3, 2.95x speedup, genuine narrowing, 3/3 byte-identical)

### C368 (2 entries)
- `5cfc50755`: C368-C371 batch (WAVE5, DEEP, COMBINED-SCALING, DEEP2)
- `d40f5fe44`: COMPOSE-PAIR5 BUILD-PASS K1-K6 (unmodified U handles 5th pair spatial-layout x task-scheduling, 3/3 byte-identical)

## Governance
Per Micah's standing rule: never rewrite shared history. Both entries for each number are preserved. When citing, use commit hash to disambiguate.
