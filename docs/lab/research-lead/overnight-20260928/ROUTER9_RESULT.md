# H-ROUTER9 RESULT: KILLED per frozen K-R9-3 (zero-refusal clause)

## Verdict

H-ROUTER9 is KILLED. Frozen kill bar K-R9-3 required zero THRESH-REFUSED
lines in the pre-existing fixture sections. The frozen run produced
exactly one: in the single-segment pre-existing fixture, the gate
refused the s0=1 threshold pair. Per the frozen kill condition ("any
failed repair claim kills H-ROUTER9; no downgrade escape"), the verdict
is KILLED.

This kill is on the bar's letter, not on a broken mechanism. The
refusal is a documented TRUE POSITIVE: it names a genuine
direct-evidence contradiction that H-ROUTER8 silently swallowed (the
taught (1,1,0)->CAUS_LEARN mark #19, whose episode sits in surviving
ACTIVE H9, contradicted by the compiled claim [s0=1&s1<2]->WITHHOLD).
The bar's premise (all pre-existing fixtures contradiction-free) was
factually false. That premise error is the builder's bar-design mistake,
owned below. The parent adjudicates whether the kill stands or the
premise correction warrants a re-freeze.

## Numbers first

- In-program automated bars: 15/15 PASS (13 inherited R8 bars + K-R9-1
  + K-R9-2). Program exit code 0 on all runs.
- Determinism (K-R9-5): stdout byte-identical across 3 runs.
  md5 9628052981a018896cff8dad89f2f870 (3/3). Zero stderr.
- K-R9-1 (X-R8-3b closure): PASS. Probes (1,5,0)=10, (1,1,0)=10,
  (1,3,0)=11, (1,4,0)=11. Replay 7/7. Exactly one THRESH-REFUSED line
  for s0=1 in the shadow section; zero THRESH-COMPILE [s0=1 lines there.
- K-R9-2 (below-boundary side): PASS. Probes (1,2,0)=11, (1,1,0)=10,
  (1,4,0)=11, (1,5,0)=11. Replay 7/7. Exactly one THRESH-REFUSED line
  for s0=1 in the T2 section; zero THRESH-COMPILE [s0=1 lines there.
- K-R9-3: FAIL on the zero-refusal clause only. All 13 inherited bars
  pass; one THRESH-REFUSED line in the single-segment pre-existing
  fixture (line 795 of the raw output).
- K-R9-4 (clean honest threshold still compiles): PASS. Honest section
  emits THRESH-COMPILE for s0=1 ([s0=1&s1>=2]->PROC_LEARN +
  [s0=1&s1<2]->WITHHOLD from {H6,H7,H8,H9}) and s0=2
  ([s0=2&s1>=2]->CAUS_LEARN + [s0=2&s1<2]->WITHHOLD from
  {H10,H11,H12,H13}); K-R4-4 threshold probes 10/10.
- Pre-existing replay mismatches: all pre-existing under R8 with
  governing bars passing (pollution-swap 18/20, single-side 18/19,
  fallback-loss 18/19, single-segment 18/19). No new mismatch
  introduced by the gate.

## What was built

Repair R9-1 (as amended by A1): `thresh_survivor_ok(W, s0v, B, M)`
gates `compile_thresholds`. After the clean-boundary checks pass and
before any rule is added or any source compacted, the gate scans every
ACTIVE FX_SET survivor's episodes. When an episode's features have
f0 == s0v and its TAUGHT task (ep_ns) differs from the task the
threshold pair claims at that triple (M when f1 >= B, else WITHHOLD),
the whole pair is refused: a THRESH-REFUSED line names the survivor
entry, the episode triple, the taught task, and the contradicted
claim; no threshold rules are added; sources stay ACTIVE. Routing falls
back to the surviving entry rules.

## The K-R9-3 refusal: complete evidence

Raw output line 795 (single-segment fixture):

THRESH-REFUSED s0=1: survivor H9 episode triple (1,1,0) taught
CAUS_LEARN contradicts generalization claimed [s0=1&s1<2]->WITHHOLD;
threshold pair refused, sources stay ACTIVE

Induction history (same section): the fixture teaches 19 marks, the
19th being `TEACH [ab>cd] feat=(1 1 0) -> CAUS_LEARN` after mark #12
`TEACH [ab>ba] feat=(1 1 0) -> WITHHOLD`. The log shows:

CONTEST action 7 state (1 1 0) outcomes (10 0 0)@seq12 vs (12 0 0)@seq19
opened at seq 19 (LAW-CHANGE suspected, WITHHOLD)

The taught CL episode sits in surviving ACTIVE H9, whose rule remains
[s0=1&s1=1]->WITHHOLD. The threshold claim [s0=1&s1<2]->WITHHOLD
contradicts that taught episode. Under the frozen A1 gate contract ("a
threshold may never contradict a taught episode"), refusal is
mandatory. This is the same bug class as X-R8-3b: direct taught
evidence shadowed by threshold generalization.

R8 baseline comparison (frozen router8_learn.zag from builder result
41ec8f641, built and run with the same pure-Zag toolchain for this
verification only): the single-segment section compiled
`THRESH-COMPILE [s0=1&s1>=2]->PROC_LEARN + [s0=1&s1<2]->WITHHOLD`,
and replay showed `REPLAY-MISMATCH #19 mark CAUS_LEARN routed
WITHHOLD`, `REPLAY 18/19`, identical to the R9 run. The contradiction
predates the repair; the R8 suite had no bar covering it (K-R7-2
checks only swap detection, tfam=1 bit0, which passes under both).

Consequences of the refusal in that fixture: no frozen-bar outcome
changed (all 13 inherited bars pass). Table-derived behavioral delta
(not probed by any frozen bar): unobserved s0=1 triples such as
(1,5,0) route PL under R8 (threshold) and WITHHOLD under R9 (fall back
to the [any] default), because the whole pair is refused per the
frozen whole-pair design.

## Causal interpretation

The X-R8-3b kill had two candidate scopes: (a) any surviving entry
whose condition overlaps the generalized range (condition-overlap),
(b) surviving entries with direct taught evidence at the contradicted
triple (episode-level). Scope (a) was prototyped first and refutes
itself: the induction's [any]->WITHHOLD default (H14, 5 episodes, none
with s0 in {1,2}) overlaps every threshold range, so scope (a) refuses
the honest curriculum's thresholds, breaks frozen K-R4-4 (0/10), and
would refuse essentially every threshold whenever the default
survives, destroying the family-boundary generalization capability the
lineage exists to provide. Scope (b), frozen by amendment A1 before
implementation, closes exactly the soundness hole: a threshold may
generalize over triples no survivor has direct evidence about
(generalization-vs-generalization resolved by the designed
family/specificity policy), but may never contradict a taught
episode. K-R9-1 and K-R9-2 verify both threshold sides refuse on the
absorbed taught episodes ((1,5,0)->W in H1; (1,2,0)->PL in H1) while
all taught probes route correctly and replay is exact.

## Boundaries and non-claims

- The gate does not see contest status: a contested taught episode
  (mark #19, "LAW-CHANGE suspected") counts as taught evidence. The
  refusal takes no side in the unresolved contest; it only blocks the
  threshold from asserting the contested triple.
- Refusal is whole-pair (frozen design): a contradiction on either
  half refuses both, including the uncontradicted half.
- The repair does not fix induction-level inconsistencies: H9's own
  rule [s0=1&s1=1]->WITHHOLD still misroutes mark #19 under R9 (replay
  18/19, same as R8). The gate stops the threshold from compounding
  it; it does not resolve the underlying contest.
- Bounded L2+ at best; no L3 claim. The ROUTER6 through ROUTER8
  lineage remains quarantined (Python-contaminated H-ROUTER8
  adversary); H-ROUTER9 is exploratory regardless of the verdict.
- The in-program verdict line ("H-ROUTER9 AUTOMATED BARS PASS")
  covers only the in-program checks. The frozen K-R9-3 includes the
  external zero-refusal check, which is what kills.

## Governance disclosures

1. Pre-freeze pure-Zag fixture-reachability pilot (disclosed in
   prereg section 5): reproduced both conflict directions without
   repair code before freezing. No Python used.
2. Prereg amendment A1 (commit 14386db64, before implementation):
   gate criterion changed from condition-overlap to episode-level
   direct-evidence contradiction, with reason recorded, after the
   overlap prototype refused the honest thresholds (K-R4-4 0/10 in
   the prototype run). Kill bars unchanged.
3. The overlap-gate prototype was built and run 3/3 (byte-identical)
   as a criterion check only; it is superseded evidence, not a
   result, and is not represented as one.
4. R8 baseline build+run (frozen source, pure Zag) was used solely
   to verify the single-segment #19 mismatch predates the repair.
5. No Python anywhere in H-ROUTER9: implementation, build (znc),
   runs, and verification (shell/grep/awk/md5sum) are Python-free.
6. Bar-design error owned: K-R9-3's zero-refusal clause assumed
   pre-existing fixtures were contradiction-free without checking.
   The single-segment fixture was not. The kill follows the frozen
   letter; the true-positive analysis is attached for adjudication.
7. No em dashes in H-ROUTER9 loop documentation (byte-checked).

## Provenance and commit lineage

- Prereg frozen alone: 09e65c83ece3f2922104af6f0f4132e2f49e4afb
- Prereg amendment A1 (alone): 14386db64e353b3b0535da6178b35e0fa8da11c2
- Source base: router8_learn.zag from H-ROUTER8 builder result
  41ec8f641 (worktree md5 85f11f1bbb86b6c659c6cd5c87d0d1f8 at copy;
  file verified pristine and unmodified in the working tree).
- router9_learn.zag: byte-verbatim copy plus exactly the frozen R9-1
  edits (8 diff regions, 161 changed lines, 2487 lines total, zero
  em dashes): new thresh_survivor_ok, gate call + refusal flag in
  compile_thresholds, banner, S-R9A and S-R9B black-box sections,
  summary lines, K-R9-1/K-R9-2 verdict checks.
- Prereg commit 14386db64 is a strict ancestor of the implementation
  commit (this result commit).
- Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/
  local-tnn-native-lab/znc, znc 2026.07.0-dev (edition 2026).
- Raw output md5: 9628052981a018896cff8dad89f2f870 (3/3 runs,
  byte-identical, zero stderr, exit code 0).
- This result commit: [to be filled at commit time]
- Files committed (owned paths only):
  docs/lab/research-lead/overnight-20260928/router9_learn.zag
  docs/lab/research-lead/overnight-20260928/ROUTER9_RAW_OUTPUT.txt
  docs/lab/research-lead/overnight-20260928/ROUTER9_RESULT.md

## Recommendation

The repair is sound and verified on both frozen fixtures plus a
newfound true positive, but the frozen bar killed it on a miscounted
expectation. Recommend the parent adjudicate: (a) uphold the kill and
close the lane, or (b) authorize H-ROUTER10 as a corrected re-freeze
whose K-R10-3 permits only refusals that name genuine
direct-evidence contradictions (audited against the raw output),
keeping the 13 inherited bars and the no-spurious-refusal intent.
Do not silently amend K-R9-3 after the fact.
