# REDTEAM_SELF: COMP lane, wave-20261002-0521pdt

Self red team on the comparative battery, the D construction, and the
collapse claim. Adversarial stance: every favorable reading below was
attacked; what survives is reported.

## 1. Is D just C renamed?

Attack: D's satisfy looks like C's DFS with knobs turned.
Evidence against rename:
- Three frozen behavioral differences are real in code AND behavior:
  (i) prefix application: d_satisfy tries k0 from 4 down to 1 per MAP;
  cc_candidates walks the FULL relseq only. PART decides it: D
  genuinely passes (SAT-SEGS n=2, composite relseq [1,1,2] from X's
  [1,1,1,1]); C's compose cannot fire there (marker absent; its PART
  pass is the trial path).
  (ii) multi-grounding with backtracking: D enumerates ALL t2_gather
  groundings with full backtracking across MAPs, prefix lengths, and
  groundings; C uses t2_lu_first (first grounding only). ADVA decides
  it behaviorally for D (SAT-SEGS n=2 despite the distractor taught
  first); C's ADVA pass is the trial path (no COMP-SEGS marker).
  (iii) unsupervised fixpoint: d_fixpoint with no expected consulted;
  C returns -2. NOSUP decides it: D promotes a verified 7-step
  composite (relseq [1,1,2,2,3,3,3], terminal 108); C fails.
- Structural differences: no compose flag/stage/mode anywhere in D
  (KB4 verified); no 3-segment researcher cap (COMP5: 5 segments,
  C fails); single-structure queries go through the same operation
  (SINGLE: SAT-SEGS n=1; D has no rebind stage).
- Honest residue: D IS "C's DFS architecture with pluggable
  applicability, prefixes, backtracking, and a fixpoint", i.e. the
  collapse direction the prereg predicted. Calling it "one general
  operation" (goal-part satisfaction: satisfy) is an engineering
  claim about the construction, not a discovery that the principles
  were already identical. The rename attack fails on behavior but
  the novelty is in the generalization, not in a new principle.

## 2. Does PART smuggle researcher glue?

Attack: the driver hands D a 5-plen X and a goal needing 2 steps;
maybe the test leaks which prefix to use.
Defense: the driver never names MAPs or prefixes (prereg protocol);
dv_gap noise and fresh workspaces per test; the pass criterion reads
the PROMOTED composite from learner state with a mechanism-neutral
relseq extractor (dv_relseq, independent copy in the driver), not
D's own d_relseq. D's search tries every k0/MAP/grounding
combination; the [1,1] prefix wins by the frozen longest-prefix
ordering, not by instruction. No dedicated glue path exists in
patch_d.zag (299 code lines inspected; no PART-specific logic).
The attack fails. (Note: B's and C's PART passes ARE artifacts of
the shared trial path, which strengthens rather than weakens the
test's isolation of prefix-capable mechanisms.)

## 3. Is the collapse claim circular?

Attack: Amendment A1's rationale says outright that D's ordering was
changed so D could subsume C ("without it D cannot subsume C's
composite-reuse behavior, which would make the subsumption test
unfair to the collapse thesis"). D was engineered to win.
Assessment: this is researcher-tuning-toward-subsumption, disclosed
in the frozen prereg itself. It does not make the measured numbers
false (D genuinely does what C does on every C-passed test, plus
COMP5 and NOSUP which C cannot do by construction), but it caps the
interpretation: COLLAPSE-SUPPORTED means "one constructed operation
covers the others' genuine wins and strictly extends them", NOT
"the three mechanisms were discovered to be one principle".
The subsumption was built, then verified; it was not found.
Additionally, the ADV-A axis (does A's exhaustive grounding beat
D's backtracking anywhere?) is untested because A never completed;
a collapse refutation on that axis remains possible in principle.

## 4. Probe-menu equivalence

The battery reuses relation ids (1-5, 70-75) and value bands
(11-53, 101-111, 301-307, distractors 9100+) across tests. Could D
be keying on surface features? Counter-evidence: four structurally
different domains (linear chains, branching distractors, atomic
hops, 40-distractor noise); fresh workspace per test (no
cross-test memory); D2 teaches distractors FIRST yet D picks the
correct branch via backtracking; NOSUP has no expected answer at
all, so no target can leak. The mechanism matches structural
relation sequences, never literal values, from learner-promoted
MAPs. Residual risk: narrow value bands; a future battery should
use randomized ids per test.

## 5. Knowledge-vs-architecture confound (the trial path)

The sharpest self-catch. The shared substrate trial path (t2_trial:
assembles any taught path of k<=4 edges, verifies vs expected) can
answer every supervised test with a goal of 4 or fewer edges,
independent of the mechanism under test. Consequences:
- B's PART, D3H passes and C's PART, ADVA, SINGLE passes are trial
  artifacts (proven by marker absence + static analysis of the
  mechanisms' applicability conditions), not mechanism wins.
- B-ABL (the prereg's causality control for B) is confounded: the
  ablation genuinely removed the co-use signal, but trial answered
  anyway. The comparison is BUILD-FAIL; B's COMP2/D2/REV wins keep
  their constructive staging analysis but the battery cannot
  certify they were compose-caused in general.
- The genuinely isolating tests are COMP3, COMP5, D4, NOSUP. Any
  future composition battery must either remove the trial path,
  extend goals beyond its reach, or require stage-attribution
  markers (as D's SAT-SEGS/SAT-FIX provide).
- This confound does not touch the collapse verdict's direction:
  on isolating tests D is 4/4 and no other mechanism exceeds it.

## 6. Metric gaming

PASS/FAIL thresholds are mechanical equalities on answers and
extracted relation sequences; kill bars were frozen before
implementation (cc9acf48e) and none were moved. The miscalibrated
predictions (B/C PART, ADVA, D3H) were recorded as calibration,
never used to adjust bars. The B-ABL surprise was scored as an
invalid control per KB6's own clause, not re-scored as a pass.

## 7. Presentation fabrication check

Every number in SEALED_EVAL.md comes from the committed run logs
(sha256s listed); 3x byte-identical reruns for B/C/C0/D; 3x
byte-identical builds for all five binaries. Stdout sanity per the
2026-10-02 AGENTS.md toolchain lesson (name/layout-dependent
_zag_print miscompile): all run outputs show intact markers,
plausible integers, no dropped literals; KB1's byte-identity plus
content inspection both hold. No Python was invoked anywhere in
this lane (safebin PATH throughout; Step 0 recorded).

## 8. Criterion 0 assessment (conjunctive; no L3 claimed anywhere)

- C0-A (runtime-defined semantics, source holds only generic
  machinery): holds for A/B/C/D as built; KB5 verified zero new
  semantic cases, no domain detectors in mechanism code.
- C0-B (open structural form, never chosen from a finite
  researcher-enumerated family): composite chains of emergent
  length/segmentation; technically holds, but all four mechanisms
  are chain-family only (owner's standing note). Generality limit,
  not a C0-B violation.
- C0-C (sealed post-freeze worlds, at least one family by an
  independent adversary): FAILS for all. This battery was designed
  by the lane workers, not an independent adversary. No L3 claim
  is available to any mechanism on this clause alone.
- C0-D (cognitive reuse improving transfer/prediction/etc.):
  reuse is demonstrated (REV R2 direct reuse; REUSE as component
  with provenance), but improvement on a downstream cognitive
  metric was not measured. Not demonstrated.
Verdict: A is L2 structural-reuse (owner's note); B, C, D are L2
structural composition. D is the strongest L2 candidate and the
only one with genuine unsupervised composition (NOSUP) and prefix
composition (PART), but C0-C and C0-D are unmet, so no L3 claim.

## 9. Open threads (not verdicts)

- A's D4 computational blowup (O(MAPs^2 x paths^2) exhaustive
  search vs 40 distractors; 50+ min without completing) is a
  robustness finding favoring D's guided DFS, but A's column is
  incomplete and its KB1 unverifiable this wave.
- The ADV-A exhaustive-grounding axis (A's purported unique
  capability) is untested; a future run should complete A's
  battery or construct a targeted breaker.
- D's base SHA string in the prereg (0e2cafe2...) is unverifiable;
  lineage rests on the full-file SHA + exact cut point instead.
