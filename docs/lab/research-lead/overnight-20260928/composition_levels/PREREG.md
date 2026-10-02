# PREREG: Composition Three Levels (L1/L2/L3)

Frozen 2026-10-02. Committed alone before implementation.
Worker: Composition Three-Level Worker. Branch: tnn-native-lab.

## Objective

Measure the unified composition mechanism
(docs/lab/research-lead/overnight-20260928/composition_unified/,
384 lines per task brief, 420 lines per REPORT.md; single DFS operation)
at three levels separately, per Micah Priority 3:

- **L1 exact reuse:** X and Y execute unchanged in Z.
- **L2 adaptive reuse:** X or Y must be adapted (extended here) for Z.
- **L3 novel composition:** X and Y provide pieces, but Z requires a NEW
  intermediate structure that did not previously exist.

Do not collapse into one PASS. Each level gets its own verdict.

## Test Design

All tests use fresh workspaces, the unified `compose_try` (verbatim
un_patch.zag), and the standard pipeline
(activate -> rebind_try -> compose_try -> trial).

Relation numbers: r1=1 (X chains), r2=2 (Y chains), r9=9 (novel).
Query relations: 71 (X), 72 (Y), 70 (Z). All relations < 64 to avoid
the value-constraint machinery.

### L1: Exact reuse

Train:
- X: ev_teach(11,1,12), ev_teach(12,1,13); query (11,71,13) -> MAP_X [1,1]
- Y: ev_teach(21,2,22), ev_teach(22,2,23); query (21,72,23) -> MAP_Y [2,2]

Gap: 30 distractor teaches (subjects 5000+, relations 60+).

Z facts: (101,1,102),(102,1,103),(103,2,104),(104,2,105).
Query (101,70,105).

Arms:
- L1-TREAT: expect ans=105, COMP-SEGS n=2.
- L1-ABL-X: delete MAP_X before Z query. Expect ans=-2.
- L1-ABL-Y: delete MAP_Y before Z query. Expect ans=-2.
- L1-FRESH: no X/Y training, only Z facts. Expect ans=-2.
- L1-REUSE: query (101,70,105) again after TREAT. Expect ans=105
  (via promoted MAP_Z or recomposition).
- L1-PROV: after TREAT, MAP_Z must have LINK14 edges to both MAP_X
  and MAP_Y (proves causal reuse, not fact re-derivation).

### L2: Adaptive reuse (extension)

Train X and Y exactly as in L1.

Z facts: (101,1,102),(102,1,103),(103,1,104) [THREE r1 links],
(104,2,105),(105,2,106) [Y shape].
Query (101,70,106).

For Z to succeed, X ([1,1]) must be EXTENDED to cover three r1 links,
or the DFS must otherwise adapt. The unified mechanism has no
extension operator.

Arms:
- L2-TREAT: expect ans=-2 (FAIL). The mechanism cannot extend MAPs.
- L2-FRESH: expect ans=-2.

L2 passes its kill bar iff the result is FAIL (-2), documenting the
adaptation gap. A PASS would be surprising and trigger investigation.

### L3: Novel intermediate

Train X and Y exactly as in L1.

Z facts: (101,1,102),(102,1,103) [X shape],
(103,9,104) [novel r9 link, NO MAP covers it],
(104,2,105),(105,2,106) [Y shape].
Query (101,70,106).

For Z to succeed, a NEW structure must bridge (103,9,104). The
unified mechanism composes only existing MAPs.

Arms:
- L3-TREAT: expect ans=-2 (FAIL). The mechanism cannot create
  novel intermediates.
- L3-FRESH: expect ans=-2.

L3 passes its kill bar iff the result is FAIL (-2), documenting the
novelty gap.

## Kill Bars (frozen)

- K1: L1-TREAT ans=105 with COMP-SEGS n=2.
- K2: L1-ABL-X, L1-ABL-Y, L1-FRESH all ans=-2 (causal proof).
- K3: L1-REUSE ans=105.
- K4: L1-PROV: MAP_Z has LINK14 to MAP_X and to MAP_Y.
- K5: L2-TREAT ans=-2 (adaptation gap documented, not a mechanism bug).
- K6: L3-TREAT ans=-2 (novelty gap documented, not a mechanism bug).
- K7: 3/3 byte-identical runs per level (sha256 recorded).
- K8: Zero em/en dashes in all deliverables (byte-verified).

Verdict is COMPOSITION-LEVELS-COMPLETE iff K1-K8 all pass.
Expected headline: L1 PASS, L2 FAIL (gap), L3 FAIL (gap).

## Implementation Plan (after prereg commit)

1. Write lv_driver.zag implementing L1/L2/L3 tests above.
2. Copy un_patch.zag verbatim (sha256-verified against the unified dir).
3. Build: cat cc_base.zag un_patch.zag lv_driver.zag > lv_full.zag.
4. Compile with pinned znc_linux_x86_64_abed8aa1.
5. Run 3x, verify byte-identical, check kill bars.
6. Write REPORT.md with per-level results. Commit with explicit pathspecs.

## Constraints

Unfrozen only. Frozen source read-only. Pure Zag. Zero em/en dashes.
Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
