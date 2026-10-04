# RESULT H-FDCR2: Held-Out Inference Probes SURVIVE (6/6)

**Prereg:** PREREG_FDCR2.md (commit d41e316f5, frozen before implementation)
**Date:** 2026-09-29
**Verdict:** H-FDCR2 SURVIVES. All four kill bars PASS.

## Summary

Six genuine held-out inference probes replace the confounded K5/K2/K4 bars.
Every probe queries a (subject, relation) pair never taught in any T line
(mechanically verified: 0 taught facts). Four probes are answered correctly
via sibling inference (sib marker in output); two correctly WITHHOLD
(conflicting evidence, isolated entity). Ablation (sibling step disabled)
destroys all four answers without introducing hallucinations. Deterministic
across three runs.

## Kill bar results

### K-H1 (genuine held-out): PASS 6/6

```
Q HELD1 h1a | hx_delta => dx1 (expected dx1) [OK] sib
Q HELD1 h1b | hx_gamma => gx1 (expected gx1) [OK] sib
Q HELD2 h2a | hy_high => hx1 (expected hx1) [OK] sib
Q HELD3 h3a | hz_green => WITHHOLD (expected WITHHOLD) [OK]
Q HELD4 h4e | hw_knd => rollx (expected rollx) [OK] sib
Q HELD5 h5a | hu_z => WITHHOLD (expected WITHHOLD) [OK]
```

All four answer-probes carry the "sib" marker (ans_kind=3), proving Step-0
direct lookup and Step-1 concept-direct did not answer them. Only sibling
inference produced the answers.

Family coverage:
- H1 (bidirectional): h1a/h1b share {hx_alpha, hx_beta}; each infers the
  other's unique relation.
- H2 (consensus): h2a infers hy_high=hx1 from agreeing siblings h2b, h2c.
- H3 (conflict): h3a WITHHOLDs; siblings h3b (gx1) and h3c (gx2) disagree.
  Most-specific preference correctly refuses to cherry-pick.
- H4 (conjunctive): h4e (redx+rndx, kind held out) infers rollx. Only the
  conjunction identifies roller; each dimension alone is ambiguous.
  Fresh-vocabulary replication of the disambig pattern.
- H5 (isolation): h5a has no sibling evidence for hu_z; correctly WITHHOLDs
  rather than hallucinating.

### K-H2 (Step-0 miss verified): PASS

Mechanical grep on heldout_infer.txt confirms zero T lines teach any
queried (subject, relation) pair:

- T h1a | hx_delta : 0
- T h1b | hx_gamma : 0
- T h2a | hy_high : 0
- T h3a | hz_green : 0
- T h4e | hw_knd : 0
- T h5a | hu_z : 0

Step-0 direct lookup provably cannot answer these probes.

### K-H3 (ablation): PASS

Ablation learner (/tmp build, SIBLING_ON=0, sibling block gated off;
Step-1 direct lookup intact; not committed):

```
Q HELD1 h1a | hx_delta => WITHHOLD (expected dx1) [FAIL]
Q HELD1 h1b | hx_gamma => WITHHOLD (expected gx1) [FAIL]
Q HELD2 h2a | hy_high => WITHHOLD (expected hx1) [FAIL]
Q HELD3 h3a | hz_green => WITHHOLD (expected WITHHOLD) [OK]
Q HELD4 h4e | hw_knd => WITHHOLD (expected rollx) [FAIL]
Q HELD5 h5a | hu_z => WITHHOLD (expected WITHHOLD) [OK]
```

All four answer-probes fail without sibling inference (0/4). Both
WITHHOLD probes still WITHHOLD (no hallucination introduced). Sibling
inference is causally necessary for the held-out answers.

### K-H4 (determinism): PASS

Three consecutive runs of heldout_infer.txt produce byte-identical stdout
(cmp-verified).

## White-box notes

Concept memberships from the run confirm the intended structure:
- h1a, h1b co-located via shared {hx_alpha, hx_beta} parent.
- h2b, h2c share an entity concept (identical features); h2a in parent.
- h4e and h4a share concept CM 11 (identical {hw_col=redx, hw_shp=rndx}
  features; kind is not a feature of h4e since it was never taught).
- h3a/h3b/h3c split as expected under contradictory hz_green; the
  most-specific candidate for h3a retains conflicting sibling evidence,
  hence WITHHOLD.

## Scope and boundaries

- Upgrades FDCR inference evidence from 3 probes (mini_world) to 9
  (3 mini_world + 6 held-out). The confounded K5/K2/K4 bars remain
  documented as confounded; this work does not re-validate them.
- Does not address MERGE incompleteness (red-team downgrade 2) or
  spurious SPLITs (downgrade 3). Those remain open.
- Does not claim L3. Classification remains bounded L2 representational
  adequacy with repaired inference.
- Pure Zag. No Python used at any stage.

## Commits

- Prereg: d41e316f5 (frozen before implementation)
- Fixture + result: this commit

## Raw outputs

- FDCR2_RAW_OUTPUT.txt: full stdout of the passing run
- FDCR2_ABLATION_RAW.txt: full stdout of the ablation run
