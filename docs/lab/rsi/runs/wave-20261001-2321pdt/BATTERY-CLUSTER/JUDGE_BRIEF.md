# JUDGE_BRIEF.md - BATTERY-CLUSTER lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: 55ee13a1c (commit containing CLUSTER_ANALYSIS.md and
  NAMECHECK.md; this brief committed separately after)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 post-freeze sealed adversarial
  battery 1/6 PASS on frozen TNN-2 (tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
  as the analyzed artifact; BATTERY Part 1 v3 VALIDATED (9/9
  mechanism bars FAIL with predicted degenerate signatures) as
  corroborating evidence; prereg SHAs dcf5e26ac3b095565f7c89926bd63ccb14efda3061cc6985e34c436a2de8037c
  (post-freeze) and
  587de900c681bc171d2f18fab9a77eeb84cfbc95692e6780b7bddbf656d25214 (v3)
- NEW_KNOWLEDGE_CLAIM: The eight failure signatures from the
  post-freeze battery and v3 validation reduce to two shared
  architectural causes in frozen TNN-2 (derivation subordination:
  the flat instance layer outranks all derived structure; guide
  content decoupling: ACT reads guides only as a presence bit),
  with eight structurally distinct falsifiable hypotheses and a
  prioritized discriminating-experiment ordering (E1-E8) that must
  precede any TNN-3 repair lineage per the no-patch-treadmill rule.

## Verdicts

- Clustering verdict: 2 clusters cover all 8 failure signatures
  (PF-A1, PF-B1, PF-B2, PF-C1, PF-C2, v3 M1, v3 M2, v3 M3). No
  observed signature requires an independent architectural cause.
- Cluster 1 (DERIVATION SUBORDINATION): flat instance-fact layer
  has no privileged standing layer for derived structures; a
  taught fact preempts traversal (PF-A1 60999 over 60902), a
  direct-fact write shadows the derived graph (PF-C1 60513),
  revisions patch instances only and cannot transfer across
  relations (PF-C2 60711 not 60721); corroborated by v3 M1 0/8
  composition with unlicensed inspector structures and v3 M3
  per-instance patching with generalization 0/2.
- Cluster 2 (GUIDE CONTENT DECOUPLING): ACT reads uncertainty
  guides only as a presence bit (PF-B1 baseline 0 becomes 30 with
  a live guide); content, count, and resolution state have no
  write path into action selection (PF-B1 pre=post=30; PF-B2
  30,30,30; v3 M2 constant CHOICE 30, 0/8 informant routing).
- Methods note: PF-A2 is a weak instrument (BFS reachability plus
  oracle verification is not discriminated from selective
  composition); it carries no verdict weight and is not assigned
  to a cause cluster.
- Hypothesis count: 4 per cluster (8 total), each with H/E/D; at
  least one general-substrate hypothesis per cluster (H1b, H1c,
  H1d; H2a, H2c).
- Experiment priority by information gain: E1 licensed-structure
  inspector (H1c), E2 single-guide content discrimination
  (H2a/H2b), E3 blind composition probe with oracle withheld
  (H1d); then E4-E8 within-cluster discriminators.

## What this does and does not establish

Establishes: a falsifiable causal map of the battery failures as
two substrate properties, with discriminating experiments that
can kill each hypothesized cause, satisfying the owner
2026-10-01 NO-PATCH-TREADMILL RULE (cluster by shared
architectural cause; 3+ structurally different hypotheses per
major bottleneck; no benchmark-specific repairs).

Does not establish: which hypothesis is true (that requires
running E1-E8 on the frozen binary under fresh preregs); any
repair direction for TNN-3; broad generality, L3, or progress
toward L3 (Criterion 0 not met; mechanism-targeted analysis
only).

## Commits (local only, never pushed; branch tnn-native-lab)

- 55ee13a1c: BATTERY-CLUSTER NAMECHECK.md (Step 0 toolchain guard)
  and CLUSTER_ANALYSIS.md (2 clusters, 8 hypotheses, E1-E8).
- (this brief): JUDGE_BRIEF.md committed after the analysis
  commit; RENDER_SHA above names the analysis commit.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/CLUSTER_ANALYSIS.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/NAMECHECK.md
- Analyzed artifacts: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/
  (PREREG_POSTFREEZE.md, POSTFREEZE_RUN.md, VALIDATION_RUN_V3.md,
  JUDGE_BRIEF.md, pf_runs/, pf_worlds/, v3_runs/, v3_worlds/)
