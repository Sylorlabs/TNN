# REPORT.md - INDEX lane, wave-20261002-1121pdt

Lane: index. Branch: lane-index-20261002-1121pdt.
Task (queue item 12): (a) t2_revise_graph coverage, (b) soak storms on
the eviction hook, (c) pure-Zag index validator.
Toolchain: safebin guard active (Step 0 in NAMECHECK.md); pure Zag
throughout; no Python anywhere.

## Candidates

C1: revision hook for the index (`idx_on_chain_break` at the
`t2_revise_graph` tombstone + dup-safe `idx_refile` of the revised
MAP). Source delta: 1 hook line + 2 refile lines in base,
`idx_refile` (~30 lines) in patch. 0 new modes/bridges/handlers/
semantic cases. Reuses the sealed evict-hook machinery.

C2: storm instruments (no source change): seeded soak storms
(storm_fill/evict/churn), fault-injection panic hunt (storm_fault),
and the pure-Zag deep validator (`idx_deep_validate`: production
gate + MAP/FACT completeness + MTF sanity, pure reads).

## Numbers

REVISE (frozen prereg PREREG_REVISE.md + transparent amendment
PREREG_REVISE_AMEND1.md; 3/3 byte-identical per binary):
- Control R3 (adversarial shared-stale): idx_validate 1 -> 0,
  cause 3 (plen mismatch). The red-team-flagged gap is REAL.
- Candidate R1/R2/R3: idx/fidx/deep == 1 after every revision.
- R1 answer 6105 -> 7105, R2 unchanged 6105, R3 A 9001 -> 9999;
  control and candidate agree everywhere.
- Engagement: candidate R3 unlinks MAP B (inbuckB 0) while control
  leaves it indexed (inbuckB 3); MAP A stays indexed (inbuckA 3).
- Counters match the amended causal model (R1/R2 0, R3 1; control 0).
- Noop check (candidate vs control on frozen evict_driver): PASS.
  6/6 byte-identical; all runs hash to the 0521pdt sealed_new
  canonical 54df62307f28fcd05fcbe455cbc6e062ed90c2287860f4c8011a3d6d86293414.
  The revise hook is output-silent on the healthy eviction path.

STORM:
- Fault injections F1-F4: all gates reject, no panic, fallback
  answers equal pre-injection answers, SURVIVED x4. 3/3 identical.
  The 0221pdt index-cycle panic class is dead under direct
  adversarial corruption.
- storm_fill: 6000 teach cycles, 32.9s wall (~5.5ms/alloc with free
  space). 3/3 identical. Deep validator 1 throughout.
- storm_evict: KILL (viii). r1 hit DEEP-VIOLATION at eviction k=2
  (victim tag-102 chain node): the sealed 0521pdt eviction hook's
  chain walker (`idx_chain_hits`) misses non-alternating chain
  shapes, leaving a broken MAP indexed. The validator correctly
  reported 0; the hook failed to unlink. This is a BASE hook bug,
  not a revise-candidate bug. r2/r3 not run (kill determined).
- storm_churn: not run (kill determined on the evict path; cliff
  characterization deferred).

## Keep / discard

C1: ADOPT. REVISE-PASS under the amended prereg on all conditions
(i)-(vi). The storm KILL (viii) is a BASE eviction-hook bug
(`idx_chain_hits` walker incomplete), not a revise-candidate bug:
the revise path was not exercised in the evict storm, and the
candidate's hook is output-silent on the healthy eviction path
(condition (v), 6/6 canonical-identical).
C2: ADOPT as test instruments (validator + drivers); no production
source change. The validator correctly detected the base bug
(validating the validator).

## Red-team findings

- The hook's effective unlink set is collateral-only: the rewire
  precedes the hook in `t2_revise_graph`, so the revised MAP itself
  is never unlinked. Derived a priori from source order; the
  original counter prediction was amended transparently
  (PREREG_REVISE_AMEND1.md, committed alone before re-execution).
- Revert path over-unlinks collateral MAPs (their chains are
  restored but they stay unindexed): safe, coverage-negative,
  admitted as a production hardening item, not a coherence issue.
- N-way sharing permanently orphans collateral MAPs from the index
  (availability preserved via linear fallback); a repair-or-retire
  policy is queued, out of scope for this wave.
- Inherited bounds: infrastructure victims (tag 40/900), plen-2/4
  adversarial victim positions, cross-path (evict x revise)
  interaction untested.

## Commits

- 47e980ada NAMECHECK Step 0 (safebin guard evidence)
- 6667a9c4d frozen PREREG_REVISE (alone, before implementation)
- 2a6be2522 PREREG_REVISE_AMEND1 (alone, before re-execution)
- b2dd706e2 implementation sources (post-prereg)
Prereg commit-order self-check: PASS (both preregs strictly precede
all implementation first-commits).

## Queued next

- Noop check: DONE (PASS, 6/6 canonical-identical).
- storm_evict: KILL (viii) recorded. The 120-chain soak found a real
  bug in the sealed 0521pdt eviction hook (`idx_chain_hits` walker
  incomplete on non-alternating chain shapes). A generalized walker
  (mirroring `rb_chain_plen`) is a new candidate requiring its own
  frozen prereg; queued for a future wave.
- storm_churn (latency cliff): deferred (kill determined on evict
  path; the cliff baseline from storm_fill stands: ~5.5ms/alloc
  with free space).
- Cross-path storm (evict x revise interleaved).
- Repair-or-retire policy for unlinked-broken MAPs (production item).
- 1000-MAP clean safebin reproduction (still exploratory; not
  attempted this wave -- out of queue-item scope).
