# REPORT: Composition Three Levels (L1/L2/L3)

## Verdict: COMPOSITION-LEVELS-COMPLETE

**The unified composition mechanism is measured separately at three
levels. L1 PASS: exact part reuse with causal proof and LINK14
provenance. L2 FAIL: no adaptation operator; clean decline on
extension demand. L3 FAIL: no novel representational element created.
The mechanism caps below L3. This is the honest measurement.**

Date: 2026-10-02. Worker: Composition Three-Level Measurement Worker.
Prereg: PREREG.md frozen alone before implementation (commit 4c15fe32d).
Amendment 1: PREREG_AMENDMENT1.md (strengthened L1 battery plen-4 to
plen-6). Branch: tnn-native-lab, local only, nothing pushed.

## Provenance of this wave

The prior wave froze the prereg, implemented the battery, and produced
runs, but never committed results. This worker adopts the frozen
PREREG.md + Amendment 1 as governing, independently verified the
driver against them line by line (see NAMECHECK.md), rebuilt the
binary from scratch, and reran all arms itself. The fresh build
reproduced the prior wave's run digest byte for byte
(d7cded3a3a26ccd9ea15dafe001d3aa64b824de8c397f2946b19c4d362272e51),
which is an independent reproduction, not a copied result.

## Design (frozen, from PREREG.md)

All arms use fresh workspaces, the verbatim unified `compose_try`
(un_patch.zag, sha256-verified identical to the unified directory
copy), and the standard pipeline
(activate -> rebind_try -> compose_try -> trial).

- X: MAP_X [1,1,1] plen-3 (11->12->13->14), queried via relation 71.
- Y: MAP_Y [2,2,2] plen-3 (21->22->23->24), queried via relation 72.
- 30 distractor teaches (subjects 5000+, relations 60-69) separate
  training from Z in every treatment arm.

### L1: exact reuse

Z facts plen-6: three r1 links (101..104) then three r2 links
(104..107). Query (101,70,107). X and Y execute unchanged in Z;
the learner fills the new values. Arms: TREAT, ABL-X (kill MAP_X),
ABL-Y (kill MAP_Y), FRESH (no X/Y), REUSE (second query after
composition), PROV (LINK14 provenance of MAP_Z to MAP_X/MAP_Y).

### L2: adaptive reuse (extension)

X ([1,1,1]) covers three r1 links, but Z needs FOUR (101..105),
then three r2 links to 108. Query (101,70,108). Composition would
require EXTENDING MAP_X. The unified mechanism has no extension
operator, so the frozen expectation is clean failure (-2),
documenting the adaptation gap.

### L3: novel intermediate

Z facts: three r1 links (101..104), a novel r9 link (104,9,105)
with NO MAP covering it, then three r2 links (105..108). Query
(101,70,108). Composition would require INVENTING a new structure
to bridge r9. The unified mechanism composes only existing MAPs,
so the frozen expectation is clean failure (-2), documenting the
novelty gap.

## Results

Binary rebuilt from scratch by this worker (frozen cc_base.zag +
verbatim un_patch.zag + verified lv_driver.zag), pinned
znc_linux_x86_64_abed8aa1. SHA-256 of the three runs:
d7cded3a3a26ccd9ea15dafe001d3aa64b824de8c397f2946b19c4d362272e51,
3/3 byte-identical.

### L1: exact reuse

| Arm | Expect | Result |
|-----|--------|--------|
| L1-TREAT | ans=107, COMP-SEGS n=2 | PASS: ans=107, COMP-SEGS n=2 (MAPs 27, 45) |
| L1-ABL-X | ans=-2 | PASS: ans=-2 (COMP-FAIL after killing MAP_X) |
| L1-ABL-Y | ans=-2 | PASS: ans=-2 (COMP-FAIL after killing MAP_Y) |
| L1-FRESH | ans=-2 | PASS: ans=-2 (trial alone cannot build plen-6) |
| L1-REUSE | ans=107 | PASS: ans=107 on the repeat query |
| L1-PROV | LINK14 to X and Y | PASS: mapz=134, link14-z-x=1, link14-z-y=1 |

**L1 verdict: PASS.** The mechanism reuses trained MAPs exactly,
filling new values, with causal proof (removing either MAP or both
destroys the composition) and white-box provenance (MAP_Z carries
LINK14 edges to both segment MAPs).

### L2: adaptive reuse

| Arm | Expect | Result |
|-----|--------|--------|
| L2-TREAT | ans=-2 (gap) | PASS(bar): ans=-2, COMP-FAIL, rebind tried 2 rejected 2 |
| L2-FRESH | ans=-2 | PASS: ans=-2 |

**L2 verdict: FAIL (adaptation gap, documented not fixed).** The DFS
considers both MAPs and rejects them; there is no operator that
extends MAP_X by one link, and the atomic-MAP assumption blocks
partial reuse. The failure is clean (no hang, no false positive).
This is the T4 partial-applicability gap in its extension variant.

### L3: novel intermediate

| Arm | Expect | Result |
|-----|--------|--------|
| L3-TREAT | ans=-2 | PASS(bar): ans=-2, COMP-FAIL |
| L3-FRESH | ans=-2 | PASS: ans=-2 |

**L3 verdict: FAIL (invention gap, documented not fixed).** No new
representational element is created for the r9 bridge. The promoted
MAP_Z is assembled from enumerated parts; that is reuse, not invention.

## Kill bars

- K1: L1-TREAT ans=107 with COMP-SEGS n=2. PASS.
- K2: L1-ABL-X, L1-ABL-Y, L1-FRESH all ans=-2. PASS (causal proof).
- K3: L1-REUSE ans=107. PASS.
- K4: L1-PROV LINK14 to MAP_X and MAP_Y. PASS (both 1).
- K5: L2-TREAT ans=-2. PASS (adaptation gap documented).
- K6: L3-TREAT ans=-2. PASS (novelty gap documented).
- K7: 3/3 byte-identical runs, sha256 recorded. PASS.
- K8: Zero em/en dashes in all deliverables (byte-verified). PASS.

All 8 bars pass. Verdict: COMPOSITION-LEVELS-COMPLETE.

## Honest interpretation

1. **The mechanism reaches L1 and caps below L3.** Exact structural
   reuse with parameter filling works and is causally proven. The
   novel combination X+Y->Z is constructed by the learner from generic
   machinery, which has an L2 flavor; the parts themselves are reused
   unchanged, which is the L1 content of the battery. The frozen level
   framing stands; these are the measured facts.
2. **L2 adaptation is a real gap.** Extension, partial MAP reuse, and
   operator invention are absent. The unified mechanism admits only
   whole existing MAPs as DFS segments.
3. **L3 invention is absent.** Nothing in the mechanism creates a new
   representational element. MAP_Z promotion is assembly of enumerated
   parts, not representational invention. Do not conflate with L2.
4. **Amendment note.** Amendment 1 strengthened the L1 battery
   (plen-4 to plen-6 Z) so the FRESH control genuinely excludes trial.
   It did not weaken any bar. File mtimes show the amendment write-up
   was finalized after the first run file; this worker rebuilt and
   reran the amended battery from scratch, and all bars are evaluated
   against the amended design only.
5. **No modes, bridges, handlers, or new semantic cases** were added.
   The driver uses only base and unified-patch entry points.

## Files

- PREREG.md: frozen preregistration (commit 4c15fe32d, before impl)
- PREREG_AMENDMENT1.md: transparent amendment (strengthening)
- NAMECHECK.md: toolchain guard, build records, audits
- REPORT.md: this file
- lv_driver.zag (201 lines): L1/L2/L3 battery driver (verified
  against prereg+amendment by this worker)
- un_patch.zag: verbatim copy of the unified mechanism
  (sha256 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2)
- lv_full.zag (2298 lines): base + patch + driver
- lv_bin: pinned znc build
- lv_run1/2/3.txt: 3/3 byte-identical runs
- lv_compile.txt: compile log (exit 0)

## Recommendation

The composition line should stop claiming progress at L3. The open
frontiers are T4 (decomposable MAPs, partial reuse) and T5
(unsupervised verification) from the unified report, plus a genuine
L2 adaptation operator (extension/partial application) before any new
L3 invention claim is entertained. The promoted MAP_Z reuse in
L1-REUSE is the closest the mechanism comes to learner-created
persistence, and it is not invention.
