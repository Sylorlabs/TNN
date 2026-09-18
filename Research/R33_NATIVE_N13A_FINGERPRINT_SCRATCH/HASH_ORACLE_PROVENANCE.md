# N13A externally published hash oracles

These literals were transcribed by the main author from the retained official
NIST and RFC files. They are external known-answer data, not values derived
from fingerprint_sha.zag, a candidate execution, or an independent-agent report.
The existing reviewer failed before completing its requested oracle authorship;
no independent review approval is claimed by this document.

## Source identities

NIST page: https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/secure-hashing

Archive: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/shs/shabytetestvectors.zip

Retained archive SHA256:
929ef80b7b3418aca026643f6f248815913b60e01741a44bba9e118067f4c9b8.
Exact extracted SHA256ShortMsg.rsp SHA256:
75e1cb83994638481808e225b9eb0c1ebd0c232d952ac42b61abce6363be283c.
Exact extracted SHA256LongMsg.rsp SHA256:
6fac36f37360bcf74ffcf4465c18e30d6d5a04cc90885b901fc3130c16060974.
Both are byte-oriented CAVS11 vectors dated2011-03-15. Len fields are BITS.

RFC: https://www.rfc-editor.org/rfc/rfc6234.txt
Retained text SHA256:
8f39f02a57bfd1da15634706724a585766e6223f77ecdaf243cad16cd3a1aa1b.
Pattern definitions are at retained lines5138-5150; SHA256 expected values at
5425-5442. No C source, reference evaluator or downloaded program was executed.

## Exact selected schedule

| Case | Source selector | Native bytes | SHA256 |
|---|---|---:|---|
|1|ShortMsg Len0; ignore placeholder Msg00|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855|
|2|ShortMsg Len8|1|28969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c1|
|3|ShortMsg Len440|55|6595a2ef537a69ba8583dfbf7f5bec0ab1f93ce4c8ee1916eff44a93af5749c4|
|4|ShortMsg Len448|56|cfb88d6faf2de3a69d36195acec2e255e2af2b7d933997f348e09f6ce5758360|
|5|ShortMsg Len504|63|18041bd4665083001fba8c5411d2d748e8abbfdcdfd9218cb02b68a78e7d4c23|
|6|ShortMsg Len512|64|42e61e174fbb3897d6dd6cef3dd2802fe67b331953b06114a65c772859dfc1aa|
|7|LongMsg Len1304|163|3c593aa539fdcdae516cdf2f15000f6634185c88f505b39775fb9ab137a10aa2|
|8|RFC SHA256 TEST1, abc|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad|
|9|RFC SHA256 TEST2_1|56|248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1|
|10|RFC SHA256 TEST4,64-byte pattern repeated10times|640|594847328451bdfa85056225462cc1d867d877fb388df0ce35f25ab5562bfbb5|
|11|RFC SHA256 TEST3,one million ASCII a bytes|1000000|cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0|

All source messages are literal hex or the exact repeated ASCII pattern in
hash_vectors.zag. Runtime construction is native Zag. The old native SHA is
also compared against each published digest; it does not generate the oracle.
Additional groups test256dirty-workspace reuses, argument/alias refusal,
full-input/seven-table fingerprint coverage and unchanged budget semantics.
The complete new child has15grouped cases, not15assertions.

Finite limits: separate literal cases at65/119/120/127/128/129bytes and the
112-byte SHA256 example are NOT included. Padding branches are tested at55/56,
63/64 and multi-block inputs163/640/1000000. This is not exhaustive hashing,
formal proof, official CAVP validation, authentication or security certification.
