# JUDGE_BRIEF.md - CLUSTER-FINAL lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: e969b2003 (this lane's commit containing
  CLUSTER_FINAL.md, JUDGE_BRIEF.md, and NAMECHECK.md; content
  identical to the final commit except this SHA line)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY-CLUSTER analysis (55ee13a1c;
  JUDGE_BRIEF 335b169ae) clustering the post-freeze sealed
  adversarial battery 1/6 PASS signatures into two shared
  causes with discriminating experiments E1-E8;
  CLUSTER-SYNTHESIS/CLUSTER_SYNTHESIS.md folding decided
  evidence from lanes E1-E7 (E8 PENDING); BATTERY-E8
  E8-BANDWIDTH verdict (RENDER_SHA c7c70b934; prereg
  034ecbd35; tools eb854c45d) completing the program;
  this lane synthesizes the final per-hypothesis statuses,
  refined shared causes, and architectural implications, adding
  no new evidence and proposing no repair.
- NEW_KNOWLEDGE_CLAIM: With E8 completing the discrimination
  program, both cluster analyses close on a subordination
  account: licensed derived structures exist but have no
  privileged standing in the read path (Cluster 1: pure
  read-path precedence, instance-only writes,
  oracle-dependent selection) and guide content exists but is
  decoupled from action except through a sticky lifecycle and
  selection-stage actionability (Cluster 2), fixing which
  requires one general substrate change giving
  learner-created structures standing in read paths,
  completeness in write paths, and legibility in selection
  paths.

## Final verdicts

Cluster 1 (DERIVATION SUBORDINATION): H1a CONFIRMED as pure
read-path precedence (E4-PRECEDENCE, 61df738fe); H1b CONFIRMED
at behavioral and state levels (E5-INSTANCE-ONLY, 8510feee6);
H1c KILLED (E1-FIRSTCLASS, f5b1bab41); H1d SUPPORTED in
refined form, assembly real and selection oracle-dependent
(E3-ORACLE-DEPENDENT, impl ce46b327a).

Cluster 2 (GUIDE CONTENT DECOUPLING): H2a REFINED (subject tag
reaches ACT as recency gate; distinguishing (s,r) content never
read; narrowed by E8: subject-identity content of an actionable
guide does not differentiate the emitted action, while
contextual actionability reaches the selection stage);
H2b KILLED (E2-CONTENT-BLIND, 6c9d96cef); H2c CONFIRMED as
H2C-STICKY (E6-CONTENT-READ, 486c13c5c; guide records never
retired/updated); H2d CONFIRMED as contributing cause
(E8-BANDWIDTH, c7c70b934: output bandwidth in the causal chain;
30-vs-0 carried by candidate-selection, not a richer emission
vocabulary).

## Governance notes

- No patch, mode, bridge, handler, or semantic case proposed
  or introduced; repair design is TNN-3 governance per the
  no-patch-treadmill rule. Section 3 of CLUSTER_FINAL.md states
  required properties of a general substrate change only.
- Criterion 0 not met by anything in this program; no L3
  language used. E7 never ran and no verdict depends on it.
- All commits local only on branch tnn-native-lab, never
  pushed. All work pure Zag under the safebin PATH; Step 0
  toolchain guard PASS (recorded in this lane's NAMECHECK.md).
