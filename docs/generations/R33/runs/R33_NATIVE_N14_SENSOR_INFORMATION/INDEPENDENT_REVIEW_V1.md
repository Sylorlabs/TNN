# Independent PRE-EXECUTION Source Review — R33-N14

Evidence limitation: this review is based only on the supplied exact evidence bundle.
The reviewer did not have filesystem access and did not independently hash, compile,
execute, or inspect repository files. No candidate execution, N06 execution, prior
primary, Python evaluator, or training path was performed.

## Terminal verdict

**REQUEST_CHANGES**

The candidate is not ready for preregistration. Two pre-execution correctness blockers
were found in the supplied exact driver source.

## Blocker 1 — supervisor executes superseded BUILD_01 binary

`n14_run()` hardcodes `Research/R33_NATIVE_N14_SENSOR_INFORMATION/BUILD_01/n14`
even though BUILD_01/02 are retained superseded compile-only history and BUILD_03/04
are the current byte-identical candidate. A future primary would therefore not execute
the reviewed binary identity.

Required fix: bind the supervisor to the exact selected reviewed build, or to an
equivalently frozen admission-selected path. The executed artifact must be part of the
freeze/admission identity.

## Blocker 2 — child-count validation is too weak

`n14_run()` parses `N14_CHILD_COUNTS` but accepts any `checks > 0`. A child could emit
only a tiny subset of the declared battery and still satisfy that parent check.

Required fix: preregister and enforce exact expected check counts for each successful
child. Reject missing/malformed/duplicate count records, missing terminal marker and
unexpected output shape.

## Positive findings

- The observer -> values + 12 metadata -> re-encode -> reseal -> byte comparison flow
  is directionally correct for the bounded encoded-file S1 claim.
- Signed little-endian PCM16 reconstruction and the full 65,536-codeword fixture are
  appropriate. Empty PCM is represented.
- RGB reconstruction and the cyclic order twin are appropriate for byte-order
  distinction, with the claim correctly limited to encoded packet information.
- The paired-twin distinctness plus equal-sum controls are appropriately bounded.
- Refusal tests snapshot state, causal bytes, head, attempts, blobs and count before
  `sn_append`; supplied sensor semantics validate malformed packets before mutation.
- Checksum regeneration is consistent with the supplied packet layout.
- Declared deadline/capture/RSS bounds are finite.
- Result publication precedes root-close checking, but the terminal PASS marker remains
  gated on the final failure count, so this is not itself a blocker.

## Required changes before approval

1. Replace the BUILD_01 runtime target with the exact reviewed selected build.
2. Enforce exact per-child evidence counts and exact log shape, including duplicate and
   malformed record rejection.
3. Rebuild under new identities and obtain a new independent review before registration.

**REQUEST_CHANGES; NO EXECUTION AUTHORIZATION.**
