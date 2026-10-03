# VERDICT: H5R2-SYNTH

Lane: HPI, wave-20261002-0221pdt. Prereg PREREG_H5R2_SYNTH.md frozen
alone at 5b2f8e0f0. Kill bars per prereg section 6; decision rule
per section 7 (BUILD-PASS iff every bar holds).

VERDICT: BUILD-FAIL

Bar scoreboard (evidence in SEALED_EVAL.md):
- SYN-NR-SEP: HOLD (S 8/8 SEP-NEW)
- SYN-NR-DECOY: FAIL (S 0/8 "D ok"; 8/8 D-DECOY-FAIL)
- SYN-NR-CHAIN: FAIL (S 0/8 "CD ok"; 8/8 CD-DECOY-FAIL)
- SYN-NR-BATT: FAIL (S 45/46; t_f2 fails)
- SYN-DT: FAIL (S 0/8 DT-FIRST vs H 8/8 and N 8/8; 0 > 8 false)
- SYN-DET: HOLD (12/12 worlds 3/3 byte-identical; battery 3/3)
- SYN-PURE: HOLD
- SYN-ORDER: HOLD
- SYN-SCOPE: HOLD (Q5 boundary respected; no general
  provenance-policy claim)
- SYN-ARCH: HOLD (+99/-0 lines in t2_trial only; no
  protected-core change)

The newest-live-among-all-live gate is newest-biased in exactly the
way the decoy family was built to punish: it relabels ties rather
than resolving them and regresses the frozen battery. The named
synthesis hypothesis is killed. Queued next: H5R2-SYNTH2 direction
decision (a structurally different discriminator, not another
tie-breaking rule).
