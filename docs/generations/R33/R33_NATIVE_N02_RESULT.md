# R33-N02 negative result

The sole registered native execution failed11 of35 assertions and exited1.
All10 expected digests and the overlap digest were wrong; status/capacity/tail
controls matched. Actual output is retained in
[the primary record](R33_NATIVE_N02_RUN_PRIMARY_V1/RESULT.json).

Source inspection found a malformed manually transcribed round-constant string:
extra hexadecimal digits shifted later words. For example the frozen sequence
contains `80deb19fe3bdc06a7` where the distinct32-bit words should be
`80deb1fe` and `9bdc06a7`. The64-word table in RFC6234 section5.1 and the
native test's independent known-answer constants identify an implementation
defect. No compiler defect or recovery campaign is inferred.

Freeze, source, driver, expected values, binary and failed output remain intact.
Do not use this version to hash scientific artifacts or checkpoints. Correction
uses a new identity, preserves the old failure, and explicitly reuses the KATs
as engineering regressions. No training, evidence freshness, native journal,
cryptographic certification or promotion is established.
