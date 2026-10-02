# JUDGE_BRIEF.md - BATTERY-E6 lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: to be recorded (commit containing E6_RUN.md and
  this brief; recorded in the follow-up commit per lane precedent)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 post-freeze sealed adversarial
  battery 1/6 PASS on frozen TNN-2 (tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
  as the analyzed artifact; BATTERY-CLUSTER analysis (two shared
  causes covering all eight failure signatures) with E6
  prioritized sixth, as the experiment specification; BATTERY-E2
  E2-CONTENT-BLIND (H2a confirmed, H2b killed), as the motivating
  result; this lane executes E6 exactly as preregistered, prereg
  frozen alone at commit 58811f3a5 (SHA-256
  80ea66f7f9cf292b0d15f5b586e968fea280a39d303c1698985a8d5f3c7f87a0)
- NEW_KNOWLEDGE_CLAIM: On frozen TNN-2, guide records are written
  once with content fields and then never retired, updated, or
  aged by resolution, while the ACT path observably reads the
  guide's subject and action-value fields but never the
  uncertainty content, so the constant-30 guide behavior is a
  sticky-lifecycle plus output-bandwidth phenomenon rather than a
  literally absent content channel.

## Verdict

E6-CONTENT-READ, with H2C-STICKY. SIGNATURE-CONTENT-READ per the
frozen section 4 decision rule: zeroing the guide subject field
(F4) flips the ACT probe from "CHOICE 30" to "CHOICE 0"
byte-identically across all 3 chains, while the natural-sequence
ACTs stay "CHOICE 30" across two distinguishable guide contents
and three resolution states. The degenerate control yields
CHOICE 0 on all 3 runs, so the presence bit reads correctly and
the comparisons are calibrated. All process bars PASS: E6-K1
prereg ordering, E6-K2 3/3 byte-identical determinism across all
stages and ablation classes, E6-K3 frozen binary hashes pre/post,
E6-K4 seal integrity (all five world files hash to prereg values),
E6-K5 block calibration, E6-K6 no-leak, K-C0A zero new semantic
cases in any harness.

## What this decides

- H2c (sticky guide lifecycle) CONFIRMED as a lifecycle property:
  both resolution events leave every guide and uncertainty record
  byte-identical (no retire, update, unlink, or aging operator
  fires). This is why PF-B1's post-resolution ACT stayed 30.
- The cluster's channel story is REFINED, not merely confirmed:
  H2a as literally stated ("content never reaches action
  selection in any form") is too strong. An ACT-path read touches
  the guide subject field (recency gate) and the guide action-value
  field (emitted choice), but the distinguishing uncertainty
  content (relation, count, resolution state) has no read path
  into ACT at all, and the action value is construction-constant
  (30). Per the frozen rule this redirects Cluster 2 toward H2d
  (output vocabulary bottleneck): content reaches ACT's gating
  read but cannot be expressed in the action.
- Recommended redirect for the cluster: E8 (orthogonal-signal ACT
  bandwidth probe, H2d) is now the live discriminator; E7
  (sequential two-guide world) already lost its H2b rationale to
  E2 and gains nothing from E6.

## Governance notes

- No patch, mode, bridge, handler, or semantic case introduced;
  K-C0A PASS. Outcome feeds back into the BATTERY-CLUSTER
  analysis as decided evidence for H2c vs H2d; no repair
  proposed, per the no-patch-treadmill rule.
- Criterion 0 not met; mechanism-targeted evidence only. No L3
  language used.
- Recorded design limitation stands: ablation detects ACT-path
  reads with an observable effect on the CHOICE line; a read with
  no observable effect is undetectable by any external probe, so
  the signatures are operational on observable reads.
- Prereg erratum recorded transparently in E6_RUN.md (POLICY_ROOT
  index gloss corrected from workspace offset 20 to node-0
  field-20 / offset 84 per the frozen pol_get/pol_set; predicate
  and decision rule unaffected, no bar moved).
