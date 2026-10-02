# REPORT: Composition Three Levels (L1/L2/L3)

## Verdict: COMPOSITION-LEVELS-COMPLETE

**L1 exact reuse: PASS. L2 adaptive reuse: FAIL (gap documented).
L3 novel composition: FAIL (gap documented).**
3/3 byte-identical. Zero modes/bridges/handlers.

Date: 2026-10-02. Worker: Composition Three-Level Worker.
Prereg: PREREG.md (commit 4c15fe32d) + Amendment 1 (plen-2->plen-3,
105->107, strengthening the FRESH control; decided before any runs).
Branch: tnn-native-lab, local only, nothing pushed.

## Method

Unified composition mechanism (un_patch.zag, verbatim copy,
sha256 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2)
on cc_base.zag (frozen). New driver lv_driver.zag implements the
three levels. Build: cat cc_base.zag un_patch.zag lv_driver.zag >
lv_full.zag (2298 lines). Pinned znc, exit 0.

## Level Definitions (per Micah Priority 3)

- **L1:** X and Y execute unchanged in Z. The composed MAP_Z segments
  are exactly the learned MAP_X and MAP_Y.
- **L2:** X or Y must be adapted (here: extended) for Z. X=[1,1,1] but
  Z needs four r1 links.
- **L3:** X and Y provide pieces, but Z needs a NEW intermediate
  structure (here: an r9 bridge with no covering MAP).

## Results (3/3 byte-identical, sha256 d7cded3a...)

### L1: PASS

| Arm | Result | Kill bar |
|-----|--------|----------|
| L1-TREAT | ans=107, COMP-SEGS n=2 (MAPs 27 45) | K1 PASS |
| L1-ABL-X | ans=-2 | K2 PASS |
| L1-ABL-Y | ans=-2 | K2 PASS |
| L1-FRESH | ans=-2 | K2 PASS |
| L1-REUSE | ans=107 | K3 PASS |
| L1-PROV | link14 z->x=1, z->y=1 | K4 PASS |

Causal proof: removing X or Y breaks Z; fresh learner fails;
MAP_Z carries LINK14 provenance to both X and Y (not fact
re-derivation). Reuse works on second query.

### L2: FAIL (adaptation gap)

| Arm | Result | Kill bar |
|-----|--------|----------|
| L2-TREAT | ans=-2 | K5 PASS |
| L2-FRESH | ans=-2 | - |

X ([1,1,1]) cannot be extended to cover four r1 links. The unified
DFS has no extension operator. This documents the L2 gap; it is not
a mechanism bug but a missing capability. The invention H1 (mutation)
worker addresses extension separately; it is not part of the unified
composition operation.

### L3: FAIL (novelty gap)

| Arm | Result | Kill bar |
|-----|--------|----------|
| L3-TREAT | ans=-2 | K6 PASS |
| L3-FRESH | ans=-2 | - |

The r9 bridge (103->104) has facts but no MAP. The DFS composes only
existing MAPs; it cannot create a novel intermediate structure.
This documents the L3 gap, the important invention frontier per Micah.

## Kill Bars

- K1 PASS (L1-TREAT 107, n=2; per Amendment 1)
- K2 PASS (all three ablations -2)
- K3 PASS (L1-REUSE 107; per Amendment 1)
- K4 PASS (LINK14 provenance confirmed)
- K5 PASS (L2-TREAT -2, gap documented)
- K6 PASS (L3-TREAT -2, gap documented)
- K7 PASS (3/3 identical, sha256 d7cded3a3a26ccd9ea15dafe001d3aa64b824de8c397f2946b19c4d362272e51)
- K8 PASS (zero em/en dashes, byte-verified)

All 8 pass. Verdict: COMPOSITION-LEVELS-COMPLETE.

## Interpretation

The three levels are now measured separately, not collapsed:

- **L1 works:** exact reuse via DFS composition is solid, with causal
  proof and provenance.
- **L2 is open:** the unified operation cannot adapt (extend/truncate)
  existing MAPs. This is the T4 partial-applicability gap, confirmed
  at the extension variant.
- **L3 is open:** the operation cannot create novel intermediates.
  This is the invention frontier.

Do not claim "composition solved." L1 is solved; L2 and L3 define
the next work.

## Files

- PREREG.md, PREREG_AMENDMENT1.md, NAMECHECK.md, REPORT.md (this file)
- lv_driver.zag (new), un_patch.zag (verbatim), lv_full.zag (2298 lines)
- lv_bin (pinned znc), lv_compile.txt, lv_run1/2/3.txt

## Constraints Observed

Pure Zag (safebin, `which python3 python` empty). Frozen base
read-only. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
Prereg (and amendment) strictly precede results.
