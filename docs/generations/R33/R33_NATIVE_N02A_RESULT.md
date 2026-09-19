# R33-N02A native correction result

All45 native assertions passed, exit0, including all10 known-answer digests,
overlap/capacity/tail controls and strict word-table rejection. The correction
changed the round-constant table and validation, not the expected KAT answers.
The original N02 negative remains frozen and consumed.

Actual [result](R33_NATIVE_N02A_RUN_PRIMARY_V1/RESULT.json),
[stdout](R33_NATIVE_N02A_RUN_PRIMARY_V1/native.stdout) and
[freeze](R33_NATIVE_N02A_FREEZE.json) identify the evidence. The host measured
0.45s wall (rounded),0.14s user CPU and3,309,568-byte peak RSS. The process guard
and every assertion were native Zag. No Python or historical primary ran.

This qualifies the exercised integrity implementation, not signature security,
whole-state serialization, journal recovery, learning or promotion. Read-only
artifact hashing may now use the exact frozen corrected binary's `file` mode;
those verifications are not new scientific experiments.
