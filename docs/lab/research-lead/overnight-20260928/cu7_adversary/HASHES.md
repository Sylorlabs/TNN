# CU7-ADV hash and lineage evidence

Date: 2026-09-30. All hashes are md5 of file bytes. Toolchain:
Linux `znc` binary from the TNN repo
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`), pure Zag.

## Custom adversary harness (X-CU7-1, X-CU7-2, X-CU7-4)

Source: `cu7a_adv.zag` in this directory.
`md5: c739185e63dababbc010c159565fbec4`
Construction: lines 1..2501 of the committed builder result
`b56ed4694:docs/lab/research-lead/overnight-20260928/causal_unified7/unified_causal7.zag`
(the full mechanism region; `fn main` begins at line 2503),
byte-verified with `cmp` against `git show` (MECH-REGION-BYTE-IDENTICAL),
plus an attack-only `fn main` and attack-only helpers appended below.
Zero mechanism bytes altered.

Three valid runs, byte-identical:
`CU7A_ADV_RAW_1.txt` md5 `7f1da12caeff399e75d5cc7d72c3f3c6`
`CU7A_ADV_RAW_2.txt` md5 `7f1da12caeff399e75d5cc7d72c3f3c6`
`CU7A_ADV_RAW_3.txt` md5 `7f1da12caeff399e75d5cc7d72c3f3c6`
All three exit 0. Final line of each:
`CU7-ADV VERDICT: HOLD (all attacks held)`.

The invalid development run (wrong initializer `fu_init`
pre-creating 4 entries; disclosed harness bug, NOT evidence):
`CU7A_ADV_INVALID_DEV_RUN.txt` (run1, exit 1, verdict KILL).
Preserved only as a disclosed development failure.

## Builder blob reproduction (X-CU7-3)

Committed sources extracted from `b56ed4694`:
`unified_causal7.zag` md5 `a91ffa107627c53850154e9c2b3de4d8`
`cu7_adv.zag`        md5 `2f36a8a276111e824af8b12f19331702`
`cu7_test.zag`       md5 `d6c81a5df49272967d8cb33bc3842410`
Each rebuilt with the Linux znc and run 3 times. Stdout hashes:

Builder adversary (`X3_BUILDER_ADV_RAW.txt`):
`36f835f69f41f100675bc385394cf6c3` (3/3 runs identical)
Frozen builder hash: `36f835f69f41f100675bc385394cf6c3`. MATCH.

Builder battery (`X3_BUILDER_TEST_RAW.txt`):
`3bde55fe381a7c8ff1cef93d8c038da3` (3/3 runs identical)
Frozen builder hash: `3bde55fe381a7c8ff1cef93d8c038da3`. MATCH.

Builder main (`X3_BUILDER_MAIN_RAW.txt`):
`87f8edc29825802327029f46f045dbe3` (3/3 runs identical)
Frozen builder hash: `87f8edc29825802327029f46f045dbe3`. MATCH.

## CU6-to-CU7 diff (X-CU7-3)

`diff` of committed `unified_causal6.zag` (from H-CAUSAL-UNIFIED6
result `438c3344a`) against committed `unified_causal7.zag`
(`b56ed4694`): 23 changed lines total, all inside the frozen
R1..R5 hunks:
R1: `fn EP_COUNTED()i32 { return 2; }` (new episode state).
R2: `conflict_adjudicate` tally skips `EP_SUP` and `EP_COUNTED`.
R3: carve loop skips counted episodes and marks winners
    `ep_st_set(W,f,EP_COUNTED())`.
R4: `entry_eps` includes `EP_ACT` and `EP_COUNTED`.
R5: every other episode-state check unchanged (verified: no other
    hunks in the diff).
No fixture literals, no test strings, no harness code in the
mechanism region. Diff-purity holds.

## Commit lineage

Builder result under attack: `b56ed4694`
"RESULT H-CAUSAL-UNIFIED7 SURVIVES (6/6). One-episode-one-vote
repair: EP_COUNTED retires carve winners from future tallies;
battery/main byte-identical to CU6; entrenchment fixture confirms
double-vote defect closed. Pure Zag." (2026-09-30 00:22:50 UTC)
Adversary prereg frozen: `1a50a3f5ebbf9822a83ab27d85d0eb2e84b5c36f`
"Prereg: H-CAUSAL-UNIFIED7 red team (CU7-ADV) FROZEN."
This report and harness: committed locally on branch
`tnn-native-lab`; no push authorized.
