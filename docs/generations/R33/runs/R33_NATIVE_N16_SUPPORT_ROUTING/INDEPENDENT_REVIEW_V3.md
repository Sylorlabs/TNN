# R33-N16 independent pre-run review V3

Review completed 2026-09-07 against the exact 26-entry
`PRE_REVIEW_V3_INPUTS.sha256` manifest, SHA256
`02c4016fee3cac4b74d8c5c82056bfc1a377d19aac2db58e3d55ef676dcd7cb1`.
All 26 entries verified and all N16 scientific roots remained absent.

## Terminal disposition

`APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`

All three historical blockers are closed:

- Arm6 comparator scope is exactly arms 9-12, matching native
  `n16_holdout_gate`.
- Support occupancy use is correctly attributed to arms 14/15 as unlabeled
  routing input.
- Dual-support preservation arms 2/6/7/11/12/19 explicitly declare synthetic
  old-target correctness on support inputs for update acceptance, matching
  `n16_anchor_loss`; this is not probe leakage.

Other reviewed controls remain consistent: probes/gate-hit telemetry are
evaluator-only; routing uses training-side geometry/occupancy only;
selector/fallback/-1 sentinel, stage binding and native gates are coherent;
selector arms 1-20 are holdout-admissible; fixed-control de-duplication and
comparator arithmetic match CONFIG; namespaces are fresh/disjoint with no
scientific roots present; exposure accounting is 210 + 128/144 + 128/144,
maximum 498; no material overflow/runtime hazard was found; scope remains
synthetic-only, non-canonical, non-promotable.

## Reviewed identities

- V3 manifest: `02c4016fee3cac4b74d8c5c82056bfc1a377d19aac2db58e3d55ef676dcd7cb1`
- `driver.zag`: `ab6f9bc44ebb1ccdd06971a47ef70fd094f5bdc21101d5f26b4107bf7900bc46`
- `CONFIG.json`: `4a72fbdd2ba7cbc2b09a8cacf493d0550533dd8ecd1b8e6530936b4341d957c7`
- `DESIGN.md`: `95f9c96bd2d52db3eac8c7d49c2f45e1c1672d4f96f60e7198d69c32f5bd95e0`
- `AUTHORING_HISTORY.md`: `53300cbeda22900714010d26cb219a75c917deefb548330410c932e534ca0d2d`
- V1: `5ea33993896071c38f687424882f44e64ce4bc71266aa5eece5c1b5abb6abe0c`
- V2: `4ac927572484a6480acd6a68500630022897429b9023076e0f74078272702701`
- BUILD_11/12: byte-identical, 148736 bytes,
  `6135e70986c3402e368836ef24b253e30a2be190f21f8aaa723ab3cd2c45a7ee`
- Smoke10/11: `073f47cbfd9fe9cffd5976b2c5d3284dea08bf94426433953dbdeea8dd8e9dca`

This review authorizes preregistration only. It does not authorize execution.
