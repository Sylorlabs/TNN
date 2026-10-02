# JUDGE_BRIEF.md - BATTERY-E8 lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: (recorded in follow-up commit; commit containing
  E8_RUN.md and this brief)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 post-freeze sealed adversarial
  battery 1/6 PASS on frozen TNN-2 (tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
  as the analyzed artifact; BATTERY-CLUSTER analysis (two shared
  causes covering all eight failure signatures) with E8
  prioritized as the H2d discriminator, as the experiment
  specification; BATTERY-E2 E2-CONTENT-BLIND as the motivating
  result (H2a confirmed, H2b killed, leaving H2c to E6 and H2d to
  this lane); this lane executes E8 exactly as preregistered,
  prereg frozen alone at commit 034ecbd35 (SHA-256
  aa5f09a9d02902c482d1108bc2c53ac9abf82bb916c203c5a6e7b184448d071b)
- NEW_KNOWLEDGE_CLAIM: With guide presence held constant (one live
  guide, no concurrency, no resolution), an in-context guide and
  an aged-out-of-context guide produce different actions
  (CHOICE 30 vs CHOICE 0) on frozen TNN-2, proving guide-content
  differences manifest behaviorally when the output channel can
  express them and placing output bandwidth in the causal chain
  of Cluster 2.

## Verdict

E8-BANDWIDTH. SIGNATURE-BANDWIDTH-SUFFICIENT per the frozen
section 3 decision rule: CHOICE(E8-A) = "CHOICE 30" vs
CHOICE(E8-B) = "CHOICE 0", differing as byte strings and
replicated across all 3 fresh-state runs of each world. Guide
presence is identical across the two worlds (exactly one live
guide, no concurrency, no resolution), so the presence bit cannot
explain the difference; it is content-driven (the guide's
contextual actionability). Calibration passes: E8-C0 (empty ACT)
and E8-C1 (post-hit ACT) yield CHOICE 0 and E8-A yields
CHOICE 30 on all runs, so the {0, 30} repertoire demonstrably
expresses the correct-action difference and the output channel
is not stuck. All process bars PASS: E8-K1 prereg ordering,
E8-K2 3/3 byte-identical determinism with exactly one CHOICE
line per transcript, E8-K3 frozen binary hashes pre/post, E8-K4
seal integrity, E8-K5 block calibration, E8-K6 no-leak, K-C0A
zero new semantic cases in any harness.

## What this decides

- H2d confirmed as a contributing cause per the frozen task
  mapping: output bandwidth is in the causal chain of whether
  guide-content differences manifest behaviorally. When the
  correct actions objectively differ (30 for the actionable
  guide, 0 for the non-actionable guide) and the repertoire can
  express both, the actions differentiate.
- H2a's strong form ("guide content never reaches action
  selection in any form") does not survive E8: content as
  contextual actionability reaches the selection stage (the
  candidate rule reads the guide's content key against context).
  The precise surviving H2a claim is narrower: subject-identity
  content of an actionable guide does not differentiate the
  emitted action (E2's result stands for its instrument).
- H2d's literal "lacks bandwidth" form did not do the work here:
  the {0, 30} channel proved sufficient for the observed content
  difference; the differentiation was carried by selection, not
  by a richer emission vocabulary. No third action was observed
  in any E8 context.
- For the cluster: E6 (H2c lifecycle) remains the open
  within-cluster discriminator; E8 closes H2d with the
  bandwidth-sufficient signature.

## Governance notes

- No patch, mode, bridge, handler, or semantic case introduced;
  K-C0A PASS. Outcome feeds back into the BATTERY-CLUSTER
  analysis as decided evidence; no repair proposed, per the
  no-patch-treadmill rule.
- Criterion 0 not met; mechanism-targeted evidence only. No L3
  language used.
- The recorded design limitation from the prereg stands: the
  differentiate outcome implicates selection-stage content
  reaching as well as output sufficiency; the verdict labels
  follow the frozen rule exactly and mechanistic interpretation
  is kept separate in E8_RUN.md.
