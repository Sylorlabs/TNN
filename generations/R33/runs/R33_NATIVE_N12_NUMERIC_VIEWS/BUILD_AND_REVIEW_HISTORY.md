# N12 authoring and review history

This is provenance, not execution evidence or a preregistration. No N12 fixture
or primary was executed during the authoring steps recorded below.

The original 104-line numeric-view source is retained in AUTHORING_INITIAL_V1.
Independent reviewer Mill inspected that revision and reported F01–F05 in
INDEPENDENT_REVIEW_DRAFT.md. The implementation was corrected for live-map
association, closed-map access, full tuple validation, LONG raw spans, and
empty-axis multiplication. Caller-supplied row destinations were removed.

AUTHORING_BUILD_01 failed the compiler's declared-type check for a pointer
subtraction expression used by the evaluator's integer-stride assertion.
Its source and error are retained. Separately typed pointer/address temporaries
fixed that authoring error. AUTHORING_BUILD_02 compiled; it was not executed.
The first matching pair BUILD_01/02 has binary SHA256
0684ecaef66626a78dd4b7f0f3759213bcef3361022ed3e2a4523f6fd150ec91.

INDEPENDENT_FINAL_REVIEW.md required two evaluator changes before preregistration:
B01, positive LONG/sign-boundary acceptance controls, and B02, independent
complete scalar/rank-eight/empty row-layout oracles. Its exact reviewed sources,
design, configuration and review are copied unchanged to PREREVIEW_V1. The report
is not retroactively changed into an approval.

The revised evaluator adds sixteen literal LONG scalar controls, ten LONG-backed
view controls and complete row assertions for the existing twenty shape cases.
Both LONG1 and LONG4 are covered. All native implementations/imports are unchanged
from the final review; only the evaluator and its design/configuration changed.
The focused re-review was assigned to the same independent reviewer, with only
INDEPENDENT_FINAL_REVIEW_V2.md allowed as its write target.

BUILD_03 and BUILD_04 each compiled successfully with empty compiler stderr,
and byte-for-byte binary comparison passed. Both binaries are 578048 bytes and
have SHA256 139a94483b84717e40c12cc85358e3522f7ebcb23733185b9eca340533f32b32.
Their source copies match the live revised source; all six transitive imported
files match the unchanged corresponding N11 build inputs.

Revised source identities:

- views.zag: 1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6
- driver.zag: badf9c5af229ee9f203f0f5599e5a31733e01d446804426c4cf9ece62baa9919
- DESIGN.md: 11e49bc31be4b087bee38d9db8897b7f72f58afe76119cb5e6f56cabcc4d2a2e
- CONFIG.json: ae2c262196d5630660dbacd43f4fad4fd4307098725c470fd701e8ad7d1fd474

Compiler is Research/toolchain/znc_macos_arm64_7cacbfc0, SHA256
3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956.
Flags: --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache.
Host rechecked as macOS26.6.2, build25G83, ARM64. The first result-poll attempt
was blocked before returning command status. Read-only inspection then found
both completed binaries and no matching compiler process; the subsequent poll
returned the original command's settled exit0. No compilation was repeated.

PREPARATION_V2 holds successful integrity output for all198 N10 artifacts,
217 N11 artifacts and50 N11 source pins. The earlier fifteen-file progress
closeout snapshot was also verified from its own root, preserving historical
hashes instead of repinning evolved live documents.

Authoring/build/review steps do not change the diagnostic execution count or
grant training, mutation, promotion, original-behavior equivalence, or a human
authority credential. Final review approval, prospective registration, exact
freeze and separate launch admission remain required before exposure.
