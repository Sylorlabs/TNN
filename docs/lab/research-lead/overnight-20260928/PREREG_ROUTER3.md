# PREREG_ROUTER3: Threshold Compilation and Mark Provenance for Learned Routing (H-ROUTER3)

**Status:** FROZEN. No edits after this commit except an explicit amendment
record. Implementation must strictly follow this document.

**Date:** 2026-09-29
**Parent result:** H-ROUTER2 DOWNGRADED by independent red team
(`ROUTER2_ADV_RESULT.md`). Two kills met:
- X-R1 (curriculum gaming): learner accepted consistently-wrong marks with
  zero diagnostics. Policy content is researcher-supplied; the learner is a
  supervised compiler, not a policy discoverer.
- X-R3 (threshold divergence): induced per-value equality rules withhold on
  nseg>=5 where authored H-ROUTER routes to PROC_LEARN/CAUS_LEARN. The claim
  "matching the authored H-ROUTER decisions" is false outside the curriculum
  range.

**Question:** Can the two downgrades be repaired by (a) enriching the routing
vocabulary with induced thresholds (nseg>=B) via post-induction compilation,
and (b) making mark-dependence explicit with consistency diagnostics that
distinguish gamed curricula from honest ones?

## Hypothesis H-ROUTER3

1. **Threshold repair (X-R3):** After the standard equality-SPLIT induction
   (machinery untouched), a threshold-compilation pass detects the pattern
   "same s0-family, contiguous learn-values above a withhold boundary" and
   compiles threshold rules [s0=X & s1>=B] -> learn-mark and [s0=X & s1<B]
   -> WITHHOLD. The compiled policy then routes nseg>=B inputs per the
   threshold, matching H-ROUTER's authored decisions on nseg=5..9.
2. **Provenance repair (X-R1):** A mark-dependence manifest traces every
   compiled rule to its supporting researcher marks; a leave-none-out replay
   verifies the compiled policy reproduces all marks; a mark-merger
   diagnostic fires when one mark class spans multiple s0 feature families
   (the structural signature of the X-R1 gamed curriculum). The claim is
   re-scoped: the learner contributes rule structure and threshold
   compilation, not policy content.

## Design (frozen)

**Machinery:** `router3_learn.zag` is a copy of `router2_learn.zag` with an
untouched induction section (causal SPLIT machinery, feature extractors,
teach(), curriculum order all identical) plus new post-induction sections.
`router2_learn.zag` is not modified.

**Phase 1 (induction):** The exact 18-item marked curriculum from
PREREG_ROUTER2, in the same order. Expected induction is identical to
H-ROUTER2 (11 ACTIVE entries: H4/H5 queries, H6..H13 per-value learn/withhold,
H14 fallback). If induction differs, the run is INVALID (machinery drift),
not a repair failure.

**Phase 1b (threshold compilation, new):**
For s0v in {1,2}: collect ACTIVE entries with mask == (s0|s1) (bits 0b011)
and cv_s0 == s0v, with FX_SET on var0. Partition their s1 values by task
code. Compile a threshold iff:
- exactly two distinct task codes appear: W(10) and M in {11,12};
- letting B = min{s1 : task = M}: every s1 with task W is < B;
- the M-valued s1 set is contiguous from B upward (no gaps);
- at least one W-valued and at least two M-valued entries exist.
Then emit threshold rules [s0=s0v & s1>=B] -> M and [s0=s0v & s1<B] -> W,
mark the consumed equality entries COMPACTED (store status 4, excluded from
routing), and record an audit line naming the consumed entries and B.
If the pattern is absent (e.g. gamed curricula), no threshold is compiled
and routing falls back to the equality entries; this is honest degradation,
not failure.

**Phase 1c (compiled routing table, new):**
A first-match table. Order: threshold rules, then remaining ACTIVE equality
entries by descending mask specificity, then the [any] fallback last.
Each rule carries condition kinds (any/eq/ge/lt) per variable. Routing
`learned_route3` scans the table; first match wins. The hypothesis store is
retained unchanged as induction evidence; the table is the compiled policy
with its own audit dump.

**Phase 1d (mark provenance and consistency audit, new):**
- **Mark-dependence manifest:** for each compiled rule, list the 1-based
  curriculum indices whose features satisfy the rule conditions and whose
  mark equals the rule task. Emitted as RULE-DEPENDS lines.
- **Replay:** route all 18 marked items through the compiled table and
  compare to marks. Emitted as REPLAY n/18.
- **Mark-merger diagnostic:** for each task code in {11,12,13,14}, collect
  the s0-constraint status across compiled rules concluding it
  (constrained values, plus whether any rule leaves s0 unconstrained).
  Emit MARK-MERGER for a task iff its rules show >=2 distinct constrained
  s0 values, or an unconstrained rule coexists with a constrained one.
  WITHHOLD(10) is excluded (the fallback legitimately merges).
- **Provenance statement:** emitted verbatim: "POLICY PROVENANCE: every
  routing decision is traceable to researcher-supplied marks; the learner
  contributes rule structure (SPLIT) and threshold compilation, not policy
  content."

**Phase 2 (tests):** All routing goes through `learned_route3`.

**Inductive bias disclosure (frozen):** Threshold compilation encodes the
researcher-supplied bias "prefer the minimal consistent threshold over
per-value memorization for ordered variables." The boundary B is
data-determined; the preference for thresholds is not. This bias is
falsifiable: K-R3-2 tests the extrapolation against H-ROUTER's authored
decisions.

## Frozen kill bars

**K-R3-1 (gamed curriculum flagged):** PASS iff, on the X-R1 gamed
curriculum variant (s0=1 multi-seg items marked CAUS_LEARN, all else
identical), the run emits MARK-MERGER for CAUS_LEARN(12) AND the honest
curriculum run emits no MARK-MERGER for any of {11,12,13,14}. The gamed
marks must be compiled faithfully (replay 18/18 on the gamed run); the bar
is on the diagnostic distinguishing the runs, not on rejecting marks the
learner cannot judge.

**K-R3-2 (threshold generalization):** PASS iff all 10 probes route per
H-ROUTER's authored predicate (nseg>=2 str>str -> PROC_LEARN, nseg>=2
iii>ii -> CAUS_LEARN):
5,6,7,8,9-seg str>str -> PROC_LEARN; 5,6,7,8,9-seg iii>ii -> CAUS_LEARN.
10/10 required. This bar SUPERSEDES K-R2C (withhold on nseg=5); the behavior
change is intentional, preregistered here, and tested.

**K-R3-3 (regression + faithfulness):** PASS iff (a) all 16/16 original
H-ROUTER2 suite items (10 H-ROUTER items + 6 novel) route identically through
`learned_route3`, and (b) REPLAY is 18/18 on the honest curriculum.

**K-R3-4 (determinism):** PASS iff 3 consecutive runs are byte-identical
(md5 of stdout).

**Verdict rule:** H-ROUTER3 SURVIVES iff K-R3-1, K-R3-2, K-R3-3, K-R3-4 all
PASS. Any FAIL kills H-ROUTER3. If K-R3-2 fails while K-R3-1/K-R3-3/K-R3-4
pass, the verdict is DOWNGRADED (provenance repair stands, threshold repair
fails; claim re-scoped to the curriculum range with the threshold recorded
as a failed extrapolation).

## Scope notes (frozen)

- Pure Zag. No Python anywhere, including verification.
- No em dashes in loop documentation.
- New files only: `router3_learn.zag`, `ROUTER3_RESULT.md`,
  `ROUTER3_RAW_OUTPUT.txt`. `router2_learn.zag` and all adversary files are
  not modified.
- Commit order: this prereg strictly before any implementation commit.
- K-R2A (inspectability) is inherited: the hypothesis dump plus the new
  compilation audit must both be white-box readable.
- Classification if SURVIVES: bounded L2+ (threshold vocabulary enrichment
  over supervised rule induction). NOT L3: features are authored, marks are
  supplied, the threshold preference is a researcher bias.
