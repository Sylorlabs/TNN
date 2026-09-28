# R33-N16 independent pre-run review V2

Review completed 2026-09-07 after V1 declaration corrections, against the
exact 24-entry `PRE_REVIEW_V2_INPUTS.sha256` manifest, SHA256
`6cf66f5e774ce72220d221d48b7a27d4c68c9976657fe498cfbcd0f3bcb65ccc`.
All 24 entries verified and all N16 scientific roots remained absent.

## Terminal disposition

`REQUEST_CHANGES`

The two V1 blockers are closed:

- Arm6 comparator is now declared exactly for selected arms 9-12, matching
  native `n16_holdout_gate()`.
- Occupancy arms 14/15 are now correctly documented as using the second
  old-support set's unlabeled occupancy counts for routing.

One preregistration blocker remains:

- **Support target-truth attribution is still incorrect.** CONFIG/DESIGN state
  that the second old-support set "never contributes ... target truth." But
  `n16_anchor_set_loss()` computes `n16_old_target(x)` on `support_seed`, and
  `n16_anchor_loss()` uses that labeled support loss to accept/reject proposed
  updates for dual-support preservation arms 2, 6, 7, 11, 12, 19. This is not
  probe leakage, but it is target-truth use in update acceptance. The
  declaration must state that explicitly, or the mechanism must change, before
  preregistration.

All other reviewed controls remain consistent: probe outcomes/gate-hit
telemetry are evaluator-only; routing itself uses input geometry/occupancy
without probe labels; selector/fallback/sentinel and stage gates are coherent;
arms 1-20 are holdout-admissible; fixed controls de-duplicate correctly;
comparator arithmetic matches CONFIG; namespaces are fresh/disjoint; exposure
arithmetic is 210 + 128/144 + 128/144, maximum 498; no material
overflow/runtime hazard was found; all scientific roots remain absent.

## Reviewed identities

- V2 manifest: `6cf66f5e774ce72220d221d48b7a27d4c68c9976657fe498cfbcd0f3bcb65ccc`
- `driver.zag`: `ab6f9bc44ebb1ccdd06971a47ef70fd094f5bdc21101d5f26b4107bf7900bc46`
- `CONFIG.json`: `0042ed472e46edbcc653695b0c320d03afa7d07cc2a2bd6b95f9057437544165`
- `DESIGN.md`: `44e40b260bf729e52a31ef430e4c716d995e5bd622dd4c35746e2dac148d8705`
- `AUTHORING_HISTORY.md`: `df4a4f1421b641c918e57e7b1e8e64f644bfb84598c4601eb4ecdbbc3449ccae`
- V1 review: `5ea33993896071c38f687424882f44e64ce4bc71266aa5eece5c1b5abb6abe0c`
- BUILD_09/10: byte-identical, 148736 bytes,
  `6135e70986c3402e368836ef24b253e30a2be190f21f8aaa723ab3cd2c45a7ee`
- Smoke08/09: `073f47cbfd9fe9cffd5976b2c5d3284dea08bf94426433953dbdeea8dd8e9dca`

No N16 scientific execution was authorized by this review.
