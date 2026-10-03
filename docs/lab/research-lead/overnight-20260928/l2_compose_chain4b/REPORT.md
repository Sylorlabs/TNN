# REPORT: L2-COMPOSE-CHAIN4B

Date: 2026-10-03. Worker: L2-COMPOSE-CHAIN4B-RETRY.
Lane: docs/lab/research-lead/overnight-20260928/l2_compose_chain4b/
Non-ledger task (claim minting paused).

## Verdict: L2-COMPOSE-CHAIN4B-PASS (infeasibility confirmed)

No 4-operator chain with 4th operator != INVERT is
feasible on the frozen learner. [6,5,4,2] and
[6,5,4,5] are empirically preempted; [6,5,4,1],
[6,5,4,3], [6,5,4,6] fall to the preregistered
analysis.

## Method

Prereg (frozen 2026-10-03, committed alone at
1d5061261) hypothesized H-4B: the [6,5,4] prefix is
forced (QD3 must be INVERT, the only operator with
the aend discriminator), and any non-INVERT 4th link
is preempted on Z4/Z5 by the de-discriminator
symmetry.

Amendment1 (pre-implementation): `f_teach` caps at
44 facts; world_F uses all 44. Revised to a minimal
probe: QD1 builds Z4 via op6, then two probes test
whether SUBSTITUTE or ABSTRACT can survive as a
later link. If preempted on Z4 (first Z in phase 2),
they can never be a 4th link.

## Results (build G, 3/3 byte-identical, FALSIFIERS 0)

- QD1(90,97,59): op=6, tries=6, via=3, val=59.
  Z4 built (id 3), exact state verified.
- QD4S(180,187,67) [SUBSTITUTE probe, entry rel 29]:
  phase 1 all 6 fail; phase 2 on Z4: op2 EXCLUDED
  (29==29), op5 FIRES. op=5, tries=11, via=4,
  val=67. A [6,5] 2-chain. SUBSTITUTE preempted.
- QD4A(190,197,68) [ABSTRACT probe, entry rel 23]:
  phase 1 all 6 fail; phase 2 on Z4: op2 FIRES
  (23!=29). op=2, tries=8, via=5, val=68. A [6,2]
  2-chain. ABSTRACT preempted.

Kill bars: G-K1 (QD1 op6/tries6) PASS. G-K2
(QD4S op5 not op2; QD4A op2 not op5) PASS.
G-K3 (3/3 sha256 c4762315...) PASS. G-K4
(FALSIFIERS 0, oth 0) PASS.

## Why [6,5,4,4] is unique

The 4th link must fire on Z6 but Z4/Z5 are tried
first. Only INVERT has a discriminator (aend +
reversed rels) that is false on Z4/Z5 but true on
Z6. SUBSTITUTE/ABSTRACT use the entry-rel
discriminator, which is symmetric: any entry rel
either matches Z4/Z5's de (firing ABSTRACT there)
or mismatches it (firing SUBSTITUTE there).
CONCRETIZE needs novel folds, but Z5 shares Z6's
folds. COMBINE cannot discriminate (identical
dnf/dvr). TRUNCATE is preempted by mA'.

## Provenance

- learner.zag: sha256 6e8ed1e0..., byte-identical
  to chain4's. Zero changes.
- world_G.zag: 39 facts (chain4 prefix subset +
  16 probe facts).
- Pure Zag, safebin PATH, no python3/python.
  Toolchain guard in NAMECHECK.md Step 0.
- Commits local, explicit pathspecs, never pushed.
- Chain4 lane untouched.

## Files

- NAMECHECK.md, PREREG.md, PREREG_AMENDMENT1.md
- learner.zag, world_G.zag, driver_G.zag
- comp_G_full.zag, comp_G_bin, run_G1/2/3.txt

## Note

`via` records the newly built Z's id (4, 5), not
the source (3). The prereg's via==3 predictions
were corrected to via==4/5 in the driver before
the final 3/3; the verdict-relevant bars (op!=2
for QD4S, op!=5 for QD4A) are unaffected.
