# Incident note: CHAIN_NL_18/19/20.txt destroyed and restored (2026-09-26)

During the PB4 resume, a bug in the resume script (5 arguments passed to a
4-parameter shell function: the real input path landed in the `$out` redirect
target) truncated three battery fixture files to 29 bytes:

- `math_logic/round4/batteries/chain_nl/CHAIN_NL_18.txt`
- `math_logic/round4/batteries/chain_nl/CHAIN_NL_19.txt`
- `math_logic/round4/batteries/chain_nl/CHAIN_NL_20.txt`

Recovery: re-downloaded the authoritative copies from the `tnn-native-lab`
branch via the GitHub contents API (blob SHAs `9bd5955adb135fee3943999e8c25af84e23708a5`,
`0b15494eeeed78dc953ee8bdb8e91a531bbfe1cd`, `3afe870754251dabf404b3b7bec701236cd64242`)
and copied them back byte-for-byte. Verification:

1. The restored files' problem text matches the pre-incident run outputs
   (e.g. CHAIN_NL_18's goal "Medicine M caused the fever to break." == the
   CLAIM line in the surviving `CHAIN_NL_18_r1.out` from the main run).
2. Re-running the problems on the restored inputs produced outputs
   byte-identical to the pre-incident r1 (cmp-verified DETERMINISTIC).
3. A filesystem sweep found no other truncated battery fixtures (R3 + R4).

No other lab files were affected. The bug was fixed before the final resume.
This note is committed for provenance, per the standing rule that bent
procedures get documented and flagged.
