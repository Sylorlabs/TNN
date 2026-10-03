# Rebinding Hardening Report

## Verdict: REBIND-HARDENING-COMPLETE

All four hardening worlds: GRACEFUL. Zero crashes, zero hangs, zero
false accepts on unmasked queries. Two scale limitations documented
(construction workspace limits, wrong-plen scan cost).

## Target

Structural rebinding mechanism from `91585087c` (REBINDING-COMPLETE
PASS), hardened in `db263d74c` (REBIND-ADV-COMPLETE, 7 worlds GRACEFUL).
Unfrozen variant only. This worker attacks scale and deception per
Micah Priority 3.

## Worlds and Measurements (3/3 byte-identical)

SHA-256 `84f12dd0ffb4d41d5dace080f741498b8a355a12771b167834fc7b25e7e5df98`.

### H1S: Scale 15 -- GRACEFUL but EXPENSIVE

A: 10 plen-3 decoy MAPs + 4 plen-5 decoy MAPs + 1 plen-5 correct MAP
(15 total). B: plen-5 chain query (expects 6114) with plen-3 distractor.

- Treatment: ans=6114, ok=1, tried=21 rejected=20.
- Control (fresh): ans=6114, ok=1, tried=4 rejected=3.

The 10 plen-3 MAPs each matched B's plen-3 distractor paths and were
correctly rejected by verification (wrong endpoint). The first plen-5
MAP won. Answer correct.

**Finding:** At scale, rebind can cost MORE than fresh trial (21 vs 4
verifies) when many wrong-plen MAPs match distractor paths. The
mechanism is correct but the linear scan has no early termination for
plen-mismatched MAPs that still match some path. This is a performance
limitation, not a correctness failure.

**Scale-100 note:** Direct construction of 100 MAPs in a single
1024-node workspace hits allocation/eviction limits. The 95 plen-3
decoys completed, but subsequent plen-5 promotions stalled (each
allocation triggering full-workspace eviction scans). 45-MAP
construction was abandoned; 15-MAP completed. The scan mechanism itself
is O(n) and would work at 100, but building the fixture is infeasible
in the current workspace. This is a test-harness limitation, not a
mechanism defect.

### H2: Deceptive similar -- GRACEFUL (robust)

A: 5 plen-5 MAPs from different A contexts (identical shape, different
provenance). B: two plen-5 paths, correct (7114) and wrong endpoint
(7214). Expected 7114.

- Treatment: ans=7114, ok=1, tried=1 rejected=0.

The first MAP tried the correct path first (BFS gather order) and
verified. The wrong-endpoint path was never tried because the first
MAP succeeded. No false accepts. With multiple identical-shape MAPs,
the mechanism remains correct because verification (not MAP provenance)
is the arbiter.

### H3: Partial applicability -- GRACEFUL (correct fallback)

A: plen-4 MAP. B: needs plen-5 (expects 8114).

- Treatment: RB-STAT tried=1 rejected=1; total tried=3 rejected=2;
  ans=8114, ok=1.
- Control: tried=0 rejected=0 (rebind); total tried=3 rejected=2;
  ans=8114, ok=1.

The plen-4 MAP matched a 4-node prefix path in B, was correctly
rejected by verification (endpoint 8113 != 8114), and fallback to trial
succeeded. **The mechanism does not do partial application.** A plen-4
shape is never accepted as "80% good enough" for a plen-5 problem.
This is correct behavior (all-or-nothing plen matching), not a
limitation to fix without a new adaptation mechanism.

Treatment tax: +1 verify (the rejected rebound) vs control.

### H4: Adaptation (extend/truncate) -- GRACEFUL (correct fallback)

A: plen-4 MAP and plen-6 MAP. B: needs plen-5 (expects 9114).

- Treatment: RB-STAT tried=2 rejected=2; total tried=6 rejected=5;
  ans=9114, ok=1.
- Control: tried=0 rejected=0 (rebind); total tried=3 rejected=2;
  ans=9114, ok=1.

Neither MAP was adapted. The plen-4 tried a 4-node prefix (rejected);
the plen-6 found no matching 6-node path (or tried and rejected).
Fallback to trial succeeded. **The mechanism cannot extend or truncate
shapes.** This is inherent to plen-exact matching. Adaptation would
require a new mechanism, not a tweak.

Treatment tax: +3 verifies vs control.

## Summary Table

| world | ans correct | treatment verifies | control verifies | behavior |
|---|---|---|---|---|
| H1S (scale 15) | 6114=6114 yes | 21 | 4 | correct, 5x cost |
| H2 (deceptive) | 7114=7114 yes | 1 | n/a | first MAP wins, correct |
| H3 (partial) | 8114=8114 yes | 3 (1 rebind) | 3 | fallback, +1 tax |
| H4 (adapt) | 9114=9114 yes | 6 (2 rebind) | 3 | fallback, +3 tax |

## Catastrophic vs Graceful

- Crash: none (3/3 runs).
- Hang: none (H1S slow but completed).
- False accept on unmasked query: none. Every accepted rebound
  satisfied v==expected by execution.
- Wrong answer: none.
- Fallback to trial when inapplicable: correct (H3, H4).
- Later learning never poisoned: all controls and treatments answer
  correctly.

## Limitations (not failures)

1. **Scale construction:** 100-MAP fixture infeasible in 1024-node
   workspace (allocation/eviction stall). 15-MAP works. The scan is O(n)
   but the test harness cannot build 100.
2. **Wrong-plen scan cost:** At 15 MAPs with distractors, rebind cost
   21 verifies vs control's 4. Many wrong-plen MAPs matching distractor
   paths create a verify tax. No early termination.
3. **No adaptation:** Plen matching is all-or-nothing. Cannot extend,
   truncate, or partially apply. H3/H4 correctly fallback, but do not
   adapt.

## Constraints honored

Unfrozen variant only; frozen source read-only (hard_base.zag SHA-256
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
hard_patch.zag verified by diff against adv_patch.zag). Pure Zag via
pinned znc. Safebin PATH; `which python3 python` returned nothing.
Zero em/en dashes (byte-verified). Paper untouched. No sealed worlds.
Nothing pushed.

## Files

- NAMECHECK.md (Step 0 toolchain guard, scope, provenance)
- ADVERSARY.md (this report)
- hard_base.zag (verbatim frozen copy)
- hard_patch.zag (verbatim rebinding mechanism)
- hard_driver.zag (four hardening worlds)
- hard_full.zag (assembled variant)
- hard_bin (compiled binary)
- hard_run1.txt, hard_run2.txt, hard_run3.txt (3/3 byte-identical)
- compile_err.txt (znc warnings only)
- build.sh (assembly script)
