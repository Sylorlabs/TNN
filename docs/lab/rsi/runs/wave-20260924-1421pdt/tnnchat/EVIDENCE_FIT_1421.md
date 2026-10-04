# tnn_chat FIT check: wave-20260924-1421pdt

Re-verification of the supervised red-team probe chats on merged HEAD
28088d207 (branch tnn-native-lab), 2026-09-24. Method follows the
wave-20260924-1121pdt EVIDENCE_FIT.md frozen FIT procedure.

## Merge under test

HEAD 28088d207 is a merge of origin/tnn-native-lab e1f78ba35
("V-NOLIMIT: no-stupid-limits full-corpus teach -- prereg, sources,
evidence"). The merge brought in roughly 2992 files / 470300 insertions
of V-NOLIMIT teach sources and evidence. It did not touch the FIT
instrument chain: pinned toolchain sha unchanged, probe source shas
unchanged, fixture shas unchanged, and both rebuilt binaries are
byte-identical to the 1121pdt records (below). The merge introduced no
observable FIT deviation.

## Toolchain

Pinned znc used for the rebuild:
src/tools/toolchain/znc_linux_x86_64_abed8aa1
sha256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
Verified with sha256sum before use; matches the frozen record exactly.
Build host directory: ~/workspace/tnn-fitchat-1421pdt/ (not /tmp).
Both sources were compiled with `-o` and the resulting binaries were run
directly.

## Sources (pulled read-only from the archive branch)

Branch: tnn-native-lab-wave-archive-20260923-2321pdt.
Source shas were verified against the prior wave's recorded values
BEFORE building; all four matched:

- baseline tnn_chat.zag
  (docs/lab/rsi/runs/wave-20260923-0834pdt/tnn_chat.zag):
  c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c
  (matches recorded c0776ad6...)
- decline tnn_chat_decline.zag
  (docs/lab/rsi/runs/wave-20260923-1121pdt/tnn_chat_decline.zag):
  a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b
  (matches recorded a87011fe...)
- R33_NATIVE_IO_V1.zag
  (docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/interactive/
  R33_NATIVE_IO_V1.zag):
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (matches recorded e6379ddb...)
- R33_NATIVE_SHA256_V2.zag
  (docs/generations/R33/runs/R33_CLOSEOUT_20260915T174458Z/sources/
  Research/R33_NATIVE_SHA256_V2.zag):
  9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf
  (matches recorded 9824f6db...)

The tnn_chat sources @import R33_NATIVE_SHA256_V2.zag, which in turn
@imports R33_NATIVE_IO_V1.zag, both resolved relative to the source
file's directory. All four files were staged under
~/workspace/tnn-fitchat-1421pdt/src/ before building.

## Canonical fixtures (this HEAD)

- docs/lab/dialogue/kb.txt:
  3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
  (matches expected 3ef27296...)
- docs/lab/dialogue/gaz.txt:
  b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a
  (matches expected b75fd113...)

38 facts loaded at startup on every run. Both binaries were run from a
directory containing kb.txt and gaz.txt (copies verified at the same
shas above).

## Binary reproducibility (this HEAD's znc): 2/2 PASS

- Decline tnn_chat_decline.zag rebuild: sha256
  20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
  (matches the 1121pdt record; byte-identical). PASS.
- Baseline tnn_chat.zag rebuild: sha256
  1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
  (matches the 1121pdt record; byte-identical). PASS.

Both builds produced analyzer warnings only (A0102 ignored return value
of proc_sentence at line 1538 in both sources, plus A0107 dead-loop
hints in R33_NATIVE_IO_V1.zag at lines 637 and 892); exit 0 in both
cases. Full build logs retained at
~/workspace/tnn-fitchat-1421pdt/runs/build_decline.log and
build_baseline.log.

## Probe results

Frozen fixtures pulled from the archive
(docs/lab/rsi/runs/wave-20260923-1121pdt/kb1_out30.txt,
kb2_inkb.txt, kb5_nogame.txt). The decline binary was run 3 times per
fixture; the baseline binary 3 times per in-KB fixture. Scratch:
~/workspace/tnn-fitchat-1421pdt/runs/ (build logs and all probe
outputs retained there).

- KB1 re-decline (30 adversarial out-of-KB turns, decline binary):
  30/30 specific declines on each of 3 runs. Per run: 26 turns use
  "My knowledge base contains nothing about ..." and 4 turns use the
  "No knowledge-base fact connects/covers ..." phrasing. 0 blanket
  refusals on all 3 runs. Run 1 output sha256
  a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308,
  byte-identical to the prior wave's recorded kb1_out30_r1.txt
  (archive docs/lab/rsi/runs/wave-20260923-1722pdt/interactive/
  kb1_out30_r1.txt).
- KB2 in-KB (17 turns, decline binary): 0 declines on all 3 runs.
  Decline-binary output sha256
  e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264
  on every run, byte-identical to the rebuilt baseline binary on all 3
  runs (zero regression). Answers correct, e.g. "Herman
  Melville wrote the novel Moby Dick." and "Andy Weir was born in 1972."
- KB5 no-decline-gaming (10 required in-KB answers, decline binary):
  10/10 answered on each of 3 runs, 0 declines, output sha256
  4f1603aa2a798a97679e91f54c0614d0de8465856a982a61debc54bc4670e88d
  on every run, byte-identical to the baseline binary on all 3 runs.
- Rerun determinism: 9/9 run-pairs byte-identical (r1/r2, r2/r3, r1/r3
  for each of the three fixtures, verified with cmp). The frozen 9-pair
  count from 1121pdt holds exactly.

## Verdict: FIT

Numbers: binary reproducibility 2/2 PASS (decline
20273a99... and baseline 1ada2fae..., both byte-identical to the
1121pdt records, so the e1f78ba35 merge introduced no FIT-relevant
change); KB1 30/30 specific declines, 0 blanket refusals (3 runs);
KB2 17/17 answered, 0 declines, byte-identical baseline parity (3 runs
each of decline and baseline); KB5 10/10 answered, 0 declines,
byte-identical baseline parity (3 runs each); rerun determinism 9/9
run-pairs byte-identical; KB1 run 1 byte-identical to the prior wave's
recorded output.

## Caveats (carried)

- The chat answers from a fixed 38-fact KB (HEAD's canonical
  docs/lab/dialogue/kb.txt and gaz.txt). It is a closed-book probe
  instrument, not an open-domain conversational model.
- The decline binary is a supervised red-team probe instrument for
  decline behavior, not a general interactive TNN.

## Interactive TNN check

What exists on this branch: the archived tnn_chat.zag
(wave-20260923-0834pdt source) and tnn_chat_decline.zag
(wave-20260923-1121pdt source) probe instruments. Both rebuild and run
on this HEAD's toolchain, as verified above; they hold a stdin line
loop (/new resets the conversation) over the 38-fact KB.

What does NOT exist on this branch: a live interactive TNN. There is
no live learning, no open-domain conversation, and no interactive
session beyond the frozen probe instruments. Nothing here was faked:
every number above comes from binaries rebuilt on this HEAD and run
against the frozen fixtures.

## Blockers

None. No Python was used anywhere in this work (shell commands only for
extraction, building, running, and greps; no Python contact, so no
evidence is voided). Nothing was pushed to GitHub.
