# JUDGE_BRIEF.md - BATTERY-E1 lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: 4afcd9f3b (commit containing the E1 tools, K-C0A
  PASS, calibration PASS, and v3 cross-check PASS; this brief and
  the run report committed separately after)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 post-freeze sealed adversarial
  battery 1/6 PASS on frozen TNN-2 (tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
  as the analyzed artifact; BATTERY-CLUSTER analysis with E1
  prioritized first by information gain (tests H1c for Cluster 1,
  DERIVATION SUBORDINATION) as the experiment specification;
  v3_struct_check / v3_inspect_state lineage as the inspector
  machinery; PREREG_E1 frozen alone at 793abbf65 (SHA-256
  7632cf5a870ac0a71934fbac8274fc5950756d2f93c6d9be127ab827bd84e03c)
- NEW_KNOWLEDGE_CLAIM: The E1 white-box inspector falsified H1c as
  stated by finding licensed derived structures persisting in
  frozen TNN-2 state (W2 id=13 with both-chain evidence, W4
  id=15/id=26 with both-hop evidence), while showing the flat
  instance-fact layer outranks them in the read path (W2's derived
  structure keeps answer 71203 while the bar probe returns the
  flat 71213; W1 answers 71999 with zero persistent structures),
  refining Cluster 1's shared cause from "no derived structures"
  to "derived structures exist but have no privileged standing in
  the read path."

## Verdicts

- Experiment verdict: E1-FIRSTCLASS (per the frozen decision
  rule: D = {W2, W4}, W4 FIRSTCLASS=1; all process bars E1-K1,
  E1-K2, E1-K3, E1-K4, E1-K6 PASS; calibration and K-C0A PASS).
  This was a prereg prediction miss (predicted E1-ABSENT).
- H1c ("no standing derived structure exists at all"): KILLED by
  white-box evidence, consistent across 3 runs per world.
- H1a (read-path precedence inversion): WINS for the W1/W2
  signatures; W2 is the clean "present but subordinated"
  observation E1 was built to discriminate.
- H1b (instance-only write path): SUPPORTED by W3 (no law-level
  derived structure; per-instance promoted structures only).
- W4 behavioral leg caveat: structure-driven answers vs
  oracle-verified BFS traversal is not discriminated here (the
  PF-A2 caveat instrument property); reserved for E3 (H1d).

## Recommended follow-ups

- Feed E1's refined Cluster 1 cause ("derived structures exist
  but have no privileged standing in the read path") back into
  CLUSTER_ANALYSIS.md as decided evidence for H1c; H1a becomes
  the live hypothesis for the W1/W2 signatures.
- E3 (blind composition probe, tests H1d) is now higher value:
  W4's FIRSTCLASS behavioral leg is the open question it answers.
- No repair proposed per the no-patch-treadmill rule; a future
  privileged-standing layer for derived structures would be one
  general substrate change, TNN-3 business after E2/E3.
