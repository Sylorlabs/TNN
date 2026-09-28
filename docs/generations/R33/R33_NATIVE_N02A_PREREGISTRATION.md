# R33-N02A — native SHA256 corrective regression

New identity `r33-native-n02a-sha256-v2`, not a repeat of the original primary
or fresh scientific evidence. N02 remains a valid retained engineering negative.
The frozen V1 constant text was528 hexadecimal characters instead of512;
unvalidated concatenation misaligned the round constants.

Changed variables: correct all64 constants against RFC6234 section5.1; encode
8-digit words with explicit spaces and validate exact count, separators and
hex digits before array writes. Add bounds validation to the word parser and
explicit allocation-failure exits in the driver. Compression, byte padding,
state update and every original KAT expected digest are unchanged.

Source reference: https://www.rfc-editor.org/rfc/rfc6234.html#section-5.1
This is a Zag implementation, not the RFC's C implementation or a Python wrapper.

Primary schedule: one native `check` process,45 assertions. The35 original
KAT/capacity/alias assertions are knowingly reused correction regressions.
Ten additional parser/table controls cover short input, negative offset, bad
digit, valid two-word loading, both values, extra digit, invalid separator,
invalid second word, and exact unchanged output after rejection.

Freeze new source/imports, driver, protocol and selected compiler/binary before
execution. CPU/wall30s,1MiB file output,64fds, zero core; measured RSS limit256MiB.
Success requires native45 checks, zero failed checks, exit0 and the exact final
marker. File identity mode remains read-only verification and cannot be used
until this corrected implementation's KATs pass. Preserve failed attempts;
do not change expected values after observing output. No learning, canonical
change, authority, full journal or cryptographic certification is involved.
