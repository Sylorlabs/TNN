# Fork battery results, wave-20260928-0821pdt

Fork-battery coordinator lane. Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, task-pinned run-start commit
3e76c0fde6b6fa9a217554aac98aa2686cca9da5. Run start 2026-09-28
08:23 PDT. Read-only git operations throughout. Pinned-commit
discipline: the live entry was extracted at its run-start-pinned SHA
3e76c0fde, never at a live ref. Scratch: ~/workspace/fb0821 (fresh
this wave). The wave lock was not touched.

## Verdict

58 named battery entries. 56 PASS, 0 FAIL, 2 UNTESTABLE, 0 CONFIRM.
1 live entry (tested fresh this wave); 57 fixture entries (carried
forward from ef418824b at unchanged SHAs).

Tag: [RE-CERT] process confirmation. This is not a new adoption and
carries no new verdict beyond toolchain/extraction stability at the
task pin.

No new FAIL. The 1721pdt probe-loss FAIL stays closed: the
toolchain-dir repair (37d1d3cab) is an ancestor of the task-pinned
commit (confirmed via git merge-base --is-ancestor); znc_probe.zag
and the znc binary are present in the tree; the probe compiles and
runs with the pinned znc (R32_ZNC_PROBE_OK met); the live entry
local-tnn-native-lab PASSES the full frozen battery at the task pin.

The two UNTESTABLEs are the expected pull-head entries
rh-pull-1-head and rh-pull-2-head (identical cause many waves
running: non-TNN research-doc trees, pinned toolchain path absent).
No result was faked. Scope stamp: this battery certifies toolchain
and extraction stability only, not the contents of the tested
commits.

UNTESTABLE caveat: the two UNTESTABLEs are content-dependent (their
trees lack the toolchain path), not toolchain regressions; the counts
above are never headlined without this caveat.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
commit ef418824b at
docs/lab/rsi/runs/wave-20260928-0521pdt/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the frozen value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc extracted read only from the task-pinned
commit 3e76c0fde6b6fa9a217554aac98aa2686cca9da5
(src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use; build command: ./znc_pin_extract build
fork_battery.zag --no-zagd --no-analyze --no-foreground-cache -o
fork_battery). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to wave-20260928-0221pdt's and 0521pdt's rebuilds;
the harness build is deterministic; lineage sha a2e6284c confirmed).
This byte-identical rebuild at the task pin is the toolchain-stability
confirmation.

## Live entry result (fresh this wave)

run_one.sh (frozen driver, extracted from ef418824b) over
local-tnn-native-lab at 3e76c0fde6b6fa9a217554aac98aa2686cca9da5:

- verdict=PASS
- znc_sha256 = the pin (498abcb5...), probe_sha256 = 3b29aa06...
- b1=PASS, b2=PASS, b3=PASS (b3_check_exit=0), b1_cmp=PASS,
  b2_bin_cmp=PASS, b2_bin_a_sha256 = B2_BIN_PIN (75b85d3c...),
  b1_run_sha256 = B1_RUN_PIN (5dfe3c16...)
- neg1_ok=PASS (driver compile exit 1, check exit 1, the fork's own
  znc reports E0002: neg1_e0002_hit=1). Broken sources do not compile.
- neg2_ok=PASS (compiles clean, runs clean, stdout "WRONG OUTPUT"
  differs from expected "FORKBATTERY-OK 42" at char 1: "W" vs "F").
- probe_build_exit=0, probe_run_exit=0, probe_run_stdout=R32_ZNC_PROBE_OK

RESULT.txt for the entry is recorded at
~/workspace/fb0821/E/local-tnn-native-lab/RESULT.txt (scratch; the
wave record carries the summary above plus the pins).

## Carried-forward fixtures (57 entries)

All fixture tips byte-identical to the 0521 manifest; their results
are carried forward verbatim from ef418824b (56 PASS, 0 FAIL,
2 UNTESTABLE at pin f03aa6fc8). No re-test was required: unchanged
SHAs cannot change results, and the [RE-CERT] tag marks exactly this
carry.

## Race caveat (standing)

This battery certifies the task pin 3e76c0fde only, not the closing
tip: the wave record commits (lane records, debate transcript,
LOOP_STATE update) land after the battery run and move the tip. Mid-run
lane commits were inert to the battery by pinned-commit extraction.
