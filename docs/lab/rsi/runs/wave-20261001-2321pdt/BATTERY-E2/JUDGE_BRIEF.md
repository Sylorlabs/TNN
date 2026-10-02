# JUDGE_BRIEF.md - BATTERY-E2 lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: 6c9d96cef (commit containing E2_RUN.md and this
  brief; brief committed after the run report)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 post-freeze sealed adversarial
  battery 1/6 PASS on frozen TNN-2 (tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
  as the analyzed artifact; BATTERY-CLUSTER analysis (two shared
  causes covering all eight failure signatures) with E2
  prioritized second, as the experiment specification; this lane
  executes E2 exactly as preregistered, prereg frozen alone at
  commit 229cf5263 (SHA-256
  bdb6eddce83d72a3273cf6e829cd56fab457a7cc98fffafa882b6c45746abd83)
- NEW_KNOWLEDGE_CLAIM: Two materially different single guides,
  each run in isolation with no concurrency, produce byte-identical
  CHOICE 30 actions on frozen TNN-2, confirming that ACT reads
  uncertainty guides only as a presence bit and killing the
  concurrency-collapse alternative (H2b) for Cluster 2.

## Verdict

E2-CONTENT-BLIND. SIGNATURE-CONTENT-BLIND per the frozen section 3
decision rule: CHOICE(E2-A) = CHOICE(E2-B) = "CHOICE 30",
byte-identical across all 3 fresh-state runs of each world. The
degenerate control E2-D yields CHOICE 0 on all 3 runs, so the
presence bit reads correctly in this id block and the comparison
is calibrated. All process bars PASS: E2-K1 prereg ordering, E2-K2
3/3 byte-identical determinism, E2-K3 frozen binary hashes
pre/post, E2-K4 seal integrity, E2-K5 block calibration, E2-K6
no-leak, K-C0A zero new semantic cases in any harness.

## What this decides

- H2a (absent content channel at the guide-to-ACT interface)
  confirmed as the root cause of Cluster 2 (GUIDE CONTENT
  DECOUPLING). Guide content, and distinctness of guide content,
  has no write path into action selection in frozen TNN-2.
- H2b (concurrency collapse in the guide store) killed for this
  instrument: the constant-30 behavior survives complete removal
  of concurrency, so it cannot be a concurrency artifact.
- Recommended redirect for the cluster: the remaining
  within-cluster discriminators are E6 (guide-store lifecycle
  inspector, H2c) and E8 (ACT output bandwidth probe, H2d); E7
  (sequential two-guide world) loses its H2b rationale given this
  result.

## Governance notes

- No patch, mode, bridge, handler, or semantic case introduced;
  K-C0A PASS. Outcome feeds back into the BATTERY-CLUSTER
  analysis as decided evidence; no repair proposed, per the
  no-patch-treadmill rule.
- Criterion 0 not met; mechanism-targeted evidence only. No L3
  language used.
- The recorded design limitation stands: the QUERY oracle value
  is present per PF protocol, but the ACT observation channel
  carries no answer path, so oracle echo is structurally
  excluded as an explanation of the observed actions.
