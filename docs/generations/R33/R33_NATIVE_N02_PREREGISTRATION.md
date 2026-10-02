# R33-N02 — native integrity implementation

Identity: `r33-native-n02-sha256-v1`, authored engineering fixtures, not scientific
worlds or fresh generalization. Native SHA256 implementation and assertion driver
replace Python hashing/verification on the forward path; no old fixture runs.

Primary schedule: one `check` execution,35 assertions. Ten known-answer cases
each assert success, expected digest and untouched output tail: empty, abc,
standard56-byte text, zero bytes of lengths55/56/63/64/65/128, and one million
ASCII a bytes. Five more assertions cover insufficient output capacity with
unchanged output and overlapping input/output with exact result and tail.
The six zero-pattern and two text digests were checked using the host's checksum
utility before registration; the native driver authors the actual byte buffers.
Expected constants are independent of the implementation being tested.

Source-derived operation bounds: input<=33,554,360 bytes, output>=32 bytes,
one padded buffer and1088 bytes of word storage. No unbounded/recursive input
parsing, filesystem effects or subprocess calls occur in `check`. Native guard
sets wall/CPU30s,1MiB output files, zero core and64 descriptors. Actual resource
metadata are retained; peak RSS is not a hard kernel resident-memory limit.

The read-only `file` mode subsequently hashes bounded regular files with no-follow
directory/child descriptors and compares to an explicit expected digest. Such
artifact verification is not new learning or another primary KAT execution.
Register each use as read-only evidence verification, not held-out capability.

Freeze sources/imports/compiler/binary/protocol before execution. Retain failures
and any changed-source correction under a new identity. Success requires all
35 checks match, `FAILURES,0`, `N02_NATIVE_SHA256_PASS,35`, exit0 and empty native
stderr. No cryptographic certification, authenticated policy, signed checkpoint,
hostile-code isolation, learner competence, promotion or R33 completion claim.
