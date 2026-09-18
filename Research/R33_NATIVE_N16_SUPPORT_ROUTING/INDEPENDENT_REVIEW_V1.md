# R33-N16 independent pre-run review V1

Review completed 2026-09-07T04:52:47Z against the exact 22-entry pre-review
manifest `PRE_REVIEW_INPUTS.sha256`, SHA256
`819718f2ee74f262c70d263a48c03b5feaf09f80486ab08bc60802404830064a`.
All 22 entries were verified before the review. This report preserves the
terminal disposition recovered from the independent reviewer's persisted task
transcript after the parent coordination channel failed to deliver it.

## Terminal disposition

`REQUEST_CHANGES`

Two preregistration blockers remain in the exact manifest-bound N16 candidate:

1. **Holdout comparator mismatch.** `CONFIG.json` says the arm6 frontier
   comparator applies when the selected arm is "9 or higher." Native
   `n16_holdout_gate()` applies it only to arms 9-12. That changes
   qualification semantics for selector-returnable arms 13-20. CONFIG/DESIGN
   and native code must prospectively agree on the exact arm set.
2. **Old-support attribution mismatch.** DESIGN states the second old-support
   set is used only to accept/reject proposed updates, but
   `n16_build_protos()` injects that support set into occupancy counts for arms
   >=14; those counts directly affect routing for occupancy arms 14/15. This is
   still training-side input and not probe leakage, but the declared
   experimental variable/attribution is inaccurate and must be corrected
   before exposure.

Everything else reviewed was consistent: no probe/target leakage into routing
or update acceptance; selector/fallback/sentinel handling is bounded; every
real selector arm 1-20 is holdout-admissible; stage gating and no-rerun
structure are coherent; 21 x 10 development = 210 exposures; 16-population
holdouts = 128 or 144 exposures each; maximum campaign = 498; namespaces are
separate from N15; fixed-control de-duplication and the other comparator
arithmetic are consistent; no material overflow hazard was found.

## Reviewed identities

- `PRE_REVIEW_INPUTS.sha256`: `819718f2ee74f262c70d263a48c03b5feaf09f80486ab08bc60802404830064a`
- `driver.zag`: `ab6f9bc44ebb1ccdd06971a47ef70fd094f5bdc21101d5f26b4107bf7900bc46`
- `CONFIG.json`: `42a8aef5b55511c9b6e5fdb26e2741f165c034462b05e606bc0a066cb1d09e4c`
- `DESIGN.md`: `0d90c137cf2246f899ca4f4b63c8fd02eaa9d1f8442850f00df448d18a8b5d8e`
- `AUTHORING_HISTORY.md`: `be2a5245bd2513f4b10363a66b9e128d3645776b3202fef6a9902fda38546cc7`
- BUILD_07/08 binary: byte-identical,
  `6135e70986c3402e368836ef24b253e30a2be190f21f8aaa723ab3cd2c45a7ee`
- Smoke06/07 stdout: byte-identical,
  `073f47cbfd9fe9cffd5976b2c5d3284dea08bf94426433953dbdeea8dd8e9dca`

No N16 scientific execution was authorized by this review.
