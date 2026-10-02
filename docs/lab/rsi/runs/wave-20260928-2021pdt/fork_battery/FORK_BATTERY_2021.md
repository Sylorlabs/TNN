# Fork Battery Report: wave-20260928-2021pdt

Date: 2026-09-28. Driver: fork_battery/batch_2021.sh (frozen 1421pdt
driver; live entries updated, fixture SHAs unchanged). Harness: the
frozen pure-Zag instrument at ~/workspace/fb1421/fork_battery, rebuilt
byte-identical (binary sha256 a2e6284c) and re-verified this wave.

## Pins

- ZNC_PIN 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (uniform across all 58 tested entries).
- PROBE_PIN 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.
- B2_BIN_PIN 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2.
- Run-start pin: 4340126e6c1cd3f03dbc653ee1f585a741fff806 (task-pinned
  run-start commit; equals the current tip, so the battery certifies
  the current tip directly with no pin gap).

## Results: 60 named entries

- PASS: 58.
- FAIL: 0.
- UNTESTABLE: 2, the expected rh-pull-1-head at 5802fec8 and
  rh-pull-2-head at 4b76bb59 (non-TNN research-doc trees; pinned
  toolchain path absent, git show exit 128; identical cause to the
  1421pdt run).

## Per-verdict invariants on all 58 tested entries

- B1/PASS, B2/PASS, B3/PASS, b1_cmp PASS, b2_bin_cmp PASS.
- harness_verdict_pass_count = 1 on every entry.
- Negative controls discriminate on every tested fork: neg1_ok PASS on
  58/58, neg2_ok PASS on 58/58.
- probe_run_stdout = R32_ZNC_PROBE_OK on all 58.

## LIVE entries this wave (both certify the current tip)

- arch-wave-20260928-1721pdt at
  4340126e6c1cd3f03dbc653ee1f585a741fff806: PASS.
- local-tnn-native-lab at
  4340126e6c1cd3f03dbc653ee1f585a741fff806: PASS.

## Evidence quality note

batch_2021.log is empty (0 lines): the driver prints nothing per entry,
so no driver execution trace survives. Verdicts come from the 60
verified evidence/RESULT.txt files under ~/workspace/fb2021pdt/E/.
The gap is recorded, not papered over. (Same gap as the 1421pdt lane.)

## Scope stamp

This run certifies toolchain and extraction stability only (znc pin
uniform, frozen harness byte-identical, strict-check flag order holds,
probes compile and run on every tested fork), not the contents of the
tested commits. Zero origin commits in this window; the remote pins are
unchanged since 1421pdt.
