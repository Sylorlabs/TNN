# JUDGE_BRIEF.md - BATTERY-E5 lane wave-20261001-2321pdt

## Provenance header

- RENDER_SHA: c8d9f14e1 (commit containing the E5 tools, K-C0A
  PASS, calibration PASS, sealed worlds, oracles, and manifest;
  this brief and the run report committed separately after)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: BATTERY Part 2 post-freeze sealed adversarial
  battery 1/6 PASS on frozen TNN-2 (tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
  as the analyzed artifact; BATTERY-CLUSTER analysis with E5
  prioritized as the within-cluster discriminator for H1b
  (Cluster 1, DERIVATION SUBORDINATION); BATTERY-E1 E1-FIRSTCLASS
  as the motivating result (E1-W3: per-instance structures,
  DERIVED=0, supporting H1b); BATTERY-E3 E3-ORACLE-DEPENDENT as
  the wave-shaping result (discriminating probes run blind;
  oracle-present probes would mask a law-write via
  t2_try_verify); e1_inspect_state / e1_audit_noleak /
  e3_blind_driver lineage as the probe machinery, reused
  byte-identical; PREREG_E5 frozen alone at 282c8301e (SHA-256
  bc15a264293469319e8de3b63aee755e50410547c48648e08ab2ae963bffeefd)
- NEW_KNOWLEDGE_CLAIM: Contradicting two instances of a two-hop
  derived law leaves the unseen third instance on the old law
  (72323) and the analogous relation untouched (72421) while the
  white-box inspector shows the contradiction writes landing
  only in the flat instance-fact layer with the per-instance
  derived structures unrevised and zero cross-instance
  aggregation, confirming H1b (instance-only write path) at both
  the behavioral and state levels.

## Verdict

E5-INSTANCE-ONLY, unanimous across 3 fresh-state runs in both
driver conditions. Full evidence in E5_RUN.md.

## Decision inputs (frozen bars, all PASS)

- E5-K1 prereg ordering PASS; E5-K2 determinism PASS
  (byte-identical transcripts, equal state.bin hashes);
  E5-K3 frozen binary PASS; E5-K4 seal integrity PASS
  (manifest 3/3 OK, zero 72xxx literals in frozen binaries);
  E5-K6 no-leak PASS.
- Calibration: competent LAW-REVISED, competent INSTANCE-ONLY,
  and degenerate controls all print exactly the frozen
  expectations; inspector cross-check reproduces E1 w2/w3
  STRUCTURE lines; blind driver K1 byte-identity re-verified;
  K-C0A PASS.

## What the judge should record

H1b confirmed for this instrument. The revision/contradiction
operator in frozen TNN-2 writes only to the instance layer; no
law-level write path was observed even with licensed derived
structures present per instance. This is decided evidence for
the cluster analysis, not a patch request.
