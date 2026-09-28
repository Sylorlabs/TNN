# N07 main-agent pre-exposure engineering review

The implementation and native evaluator are a new identity, not a modification
of N01/N02/N03/N04/N05/N06. SHA/IO/process imports remain frozen. Native byte
arrays avoid the previously observed numeric-slice allocation/stride error;
numeric wire values use explicit signed-positive31-bit bounds. No imported
numeric constants are used for new sizes, offsets, expected values or limits.

Authentication construction follows RFC2104. Seven public RFC4231 SHA256 cases
provide externally specified known answers, including long-key handling. The
published truncated case is only a conformance-prefix comparison; runtime token
verification still requires32 bytes. Raw SHA256 is never called a signature.
HMAC is symmetric authentication, not asymmetric/nonrepudiable human identity.

Every request body byte is MAC-covered. Actor, instance, scope, milestone,
epoch, nonce, parent version/hash, exact candidate/hash, dependency/policy,
charge and logical interval are checked. Reserved bytes and versions reject.
The API stages caller bytes, revalidates before reservation and again immediately
before commit under the same lock; there is no separate learner-callable grant
flag or public unprotected commit step. Restriction cannot increase limits.

The persisted sequence authenticates prior accounting and previous record tag.
Full uncommitted intents keep their charges/nonces; operational snapshot state
changes only with its exact published record. Restriction intents become effective
even without an acknowledgement marker, preventing resurrection after a crash.
Partial intents deliberately block recovery rather than guessing a grant or
refunding a charge. This is fail-closed behavior, not automatic full recovery.

Recovery reads all bounded record/commit paths and validates before exposing a
usable store. Corruption/holes/overcapacity refuse and close/wipe visible state.
Observer capacity/alias checks precede output writes. Key material never enters
the record, but the process is trusted: native structs and memory are not an
isolation boundary and cryptographic intermediate arena memory is not guaranteed
erased. Hard RSS/descendant containment and hardware power-cut tests are absent.

The old-prefix witness is intentionally a required negative: valid MACs do not
identify a newer missing suffix without independently protected high-water state.
Advisory file locks prevent cooperating concurrent writers, not hostile same-user
root replacement. A full protected runtime must add an external monotonic anchor,
isolation, real human authentication/key custody and complete authority integration.
No real grant is produced and no R33 authority milestone is qualified here.

This review is by the implementing main agent. It is not an independent review,
scientific approval, cryptographic audit, security certification or authorization
to bypass parent/sensory/causal/freshness prerequisites. Compilation and results
remain prospective until their actual retained outputs settle.

Both independent native compilations have now settled with exit0 and no fixture
execution. BUILD_01 elapsed1.34s and BUILD_02 elapsed1.40s, each observed
maximumRSS54,378,496bytes. Binary comparison is exact; both SHA256 values are
85e633876a48fb2f5b0dfc7584f5a4d4f596daee88376e2a133dfbe3e1c18bb9.
Selected BUILD_01. All source copies match their corresponding new sources or
frozen imports. Rechecked all seven test-case SHA256 strings against RFC4231
section4 before source freeze. No runtime result is inferred from compilation.
