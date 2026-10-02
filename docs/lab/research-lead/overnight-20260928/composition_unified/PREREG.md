# PREREG: Composition Collapse (Unified Mechanism)

## Identity
- Worker: Composition Collapse Builder (subagent, 2026-10-02)
- Mission: Priority D. Build ONE composition mechanism replacing A/B/C.
- Prereg frozen: commit of this file ALONE precedes any implementation commit.
- Unfrozen variant. Frozen source read only. Pure Zag. Paper untouched.
- Nothing pushed to GitHub. Zero em/en dashes in this document.

## Provenance note
Untracked design scratch files (un_patch.zag, _*.txt) existed in the target
directory before this session, dated 2026-10-02 07:09 PDT, from a prior
incomplete attempt. They were never committed and are not adopted by this
prereg. This PREREG.md is written fresh and its commit strictly precedes
any implementation commit, per the commit-order self-check.

## Design (frozen)

ONE composition operation, in ev_query between rebind_try and trial:

1. **Search core**: C's iterative depth-first search over MAP compositions
   (cc_dfs architecture). The researcher 3-segment cap is removed. DFS now
   attempts up to 8 segments (a practical search bound, documented; the
   battery needs 5). A/B pair-search machinery is deleted, not ported.
2. **Applicability predicate interface**: a MAP is a candidate at the
   current value if ANY predicate admits it:
   - P1 (from C): relation-sequence walkable from current value
     (structural constraint satisfaction, cc_satisfy).
   - P2 (from A): plen contract matches a real gathered path from the
     current value (fallback when relseq extraction fails, cx_contract
     plus t2_gather). Consulted, not a hardcoded gate.
   - P3 (from B): type-15 co-use history orders candidates (history-first)
     and accumulates from composition successes (co-use edges written
     between consecutive segments on promote). B's ev_cq episode facility
     is retained verbatim as the history-writing event.
3. **Assembly and verification**: unchanged from C (assemble rebound
   chains, SEQ-link, t2_try_verify, promote MAP_Z with LINK14 provenance
   to each segment MAP). No COMPOSE_MODE. No new modes, bridges, handlers,
   or semantic cases. Single compose_try entry point in ev_query.

## Battery (frozen)

Driver un_driver.zag: the 6 compare-battery tests (same world protocol as
the comparative battery, including B's co-use episodes so the type-15
predicate has input):
- T1: 3-structure (X+Y+W plen-2 each, rels 1/2/3) to Z plen-6, rel 70.
  Expect PASS (match C).
- T2A: 4-structure (add V, rel 4) to Z plen-8. Expect PASS.
- T2B: 5-structure (add U, rel 5) to Z plen-10. Expect PASS.
- T3: cross-domain (X plen-3 r1 chain + Y single-hop r5) to Z plen-4.
  Expect PASS (match C).
- T4: partial applicability (X plen-4, Z needs 3 of X + Y).
  Expect FAIL (documented open question, atomic MAP assumption; must not
  hang and must not produce a false positive).
- T5: no expected-answer (expected=-1). Expect compose to decline (-2);
  no hang.

## Kill bars (frozen)

- K1: T1 PASS, matching C's T1 result.
- K2: T3 PASS, matching C's T3 result.
- K3: T2A PASS (4-structure; proves the 3-cap was the only blocker).
- K4: T2B PASS (5-structure).
- K5: un_patch.zag cognition lines STRICTLY FEWER than the sum of the
  three separate engine patches (A cx_patch.zag 183 + B cb_patch.zag 298
  + C cc_patch.zag 308 = 789).
- K6: 3/3 runs byte-identical (determinism), SHA-256 recorded.
- K7: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Bridge audit:
  exactly one compose_try definition; exactly one call site in ev_query;
  no COMPOSE_MODE anywhere.
- K8: T4 and T5 must not regress relative to C (T4 FAIL without false
  positive, T5 compose declines with -2, both terminate).

Any bar missed: BUILD-FAIL, not COMPLETE.

## Verdict names
- All bars pass: COMPOSITION-UNIFIED-COMPLETE (report line-count delta
  and generality comparison vs A/B/C).
- Any bar missed: BUILD-FAIL (report which bar).

## Method
- Base: composition_C/cc_base.zag (frozen, read only).
- Patch: composition_unified/un_patch.zag (this worker, written after
  this prereg commit).
- Driver: composition_unified/un_driver.zag (battery above).
- Build: cat cc_base.zag un_patch.zag un_driver.zag > un_full.zag;
  compile with pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Toolchain guard: safebin PATH, no python3/python, verified in NAMECHECK.
- Commits: this PREREG.md ALONE first; then implementation + results with
  explicit pathspecs. Local only, never pushed.
