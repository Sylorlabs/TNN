# tnn_chat FIT fresh re-run: wave-20260929-0821pdt

Path taken: FRESH RE-RUN. Standing rule mandates a fresh re-run at
least every 8 waves; the last fresh re-run was wave-20260928-2021pdt
and the staleness reached 8 of 8, so the re-run was DUE this wave.
Staleness resets to 0 of 8 after this run; the next fresh re-run is
due 8 verdict-bearing waves hence. This is not a candidate verdict
and it is not merge review of merged-in work; it certifies the
38-fact closed-book probe chain only.

## Literal scope

Working HEAD is d24eda8bdc34dee54aace6451b193754e96784ab (this
wave's run-start tip, including the morning research-lead session
commits). This report certifies only the frozen 38-fact closed-book
probe chain: the two frozen probe instruments (baseline
tnn_chat.zag, decline tnn_chat_decline.zag), the two R33 support
sources, the canonical kb.txt and gaz.txt, the pinned toolchain, the
three probe fixtures, and the expected classes. Nothing in Micah's
merged-in frontier files was touched. Nothing was pushed to GitHub.

## Frozen chain enumeration (all 10 pins verified before use)

- tnn_chat.zag c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c
- tnn_chat_decline.zag a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b
- kb.txt 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1 (38 facts)
- gaz.txt b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a (27 lines)
- fixtures: kb1_out30.txt 936c35e11706e98f08ea0dbe0b33f2c6d93c1a301c7a3e003f850e5f610b8188;
  kb2_inkb.txt 730e2d246926bbd91909da1799b7327c9cba586085dbfa79e2407bcc39883184;
  kb5_nogame.txt b60198b059f332eb821be257eb130e59c3e22009600ba89abd04cf267ee86a38
- R33_NATIVE_IO_V1.zag e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
- R33_NATIVE_SHA256_V2.zag 9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf
- znc src/tools/toolchain/znc_linux_x86_64_abed8aa1
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

## Fresh re-run procedure (pure Zag, zero Python)

Inputs staged read only (shell cp from the verified durable paths, no
edits) into build host ~/workspace/tnn-fitchat-0821pdt/ (outside the
repo). Build: ./znc tnn_chat_decline.zag -o tnn_chat_decline (exit 0);
./znc tnn_chat.zag -o tnn_chat (exit 0). Both binaries ran from the
directory containing the verified kb.txt and gaz.txt copies. 38 facts
loaded at startup on every run.

Binary reproducibility on HEAD d24eda8bd: 2/2 PASS.
- Decline rebuild: sha256
  20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
  (byte-identical to the frozen 20273a99 record).
- Baseline rebuild: sha256
  1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
  (byte-identical to the frozen 1ada2fae record).

## Probe results (all runs exit 0, all stderr empty)

- KB1 re-decline (30 adversarial out-of-KB turns, decline binary, 3
  runs): 30/30 specific declines on each run (26 turns phrasing "My
  knowledge base contains nothing about ...", 4 turns phrasing "No
  knowledge-base fact ..."). 0 blanket refusals on all 3 runs. Output
  sha256 a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308
  on every run, byte-identical to the prior wave's recorded output.
- KB2 in-KB (17 turns, decline binary, 3 runs): 17/17 answered, 0
  declines on all 3 runs. Output sha256
  e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264
  on every run, byte-identical to the rebuilt baseline binary on all
  3 runs (zero regression).
- KB5 no-decline-gaming (10 required in-KB answers, decline binary,
  3 runs): 10/10 answered on each run, 0 declines. Output sha256
  4f1603aa2a798a97679e91f54c0614d0de8465856a982a61debc54bc4670e88d
  on every run, byte-identical to the baseline binary on all 3 runs.
- Rerun determinism: 9/9 required run-pairs byte-identical (r1/r2,
  r2/r3, r1/r3 for each of the three fixtures, verified with cmp).
  The six baseline run-pairs were also byte-identical.
  Decline/baseline parity: 2/2 pairs byte-identical (KB2, KB5).

All stderr logs empty; no runtime errors. All 15 runs exited 0.

## Merge-range entry-point scan (this wave's interactive procedure)

Merge range d2fdf1225..d24eda8bd (morning research-lead session
commits plus the 0521pdt wave record).

- Layer 1, added-file name scan: 17 new .zag files, all under
  docs/lab/research-lead/overnight-20260928/ (bridge_learn,
  causal/*, genbias_test, integ_learn, pi_adversary/*,
  rep_v2/fdcr_learn, route_learn, sem_l3/*, stress_learn,
  unified_learn). All are batch research instruments, not chat
  entry points.
- Layer 2, range-diff content scan: word-boundary grep for
  stdin, _zag_arg, repl over all 17 files at the tip: the only hits
  are _zag_arg(1)/_zag_arg(2) file-path arguments (obs/probe file
  inputs to batch instruments). Zero stdin-read chat loops.
- Layer 3, git diff --stat over src/ and units/: zero changed files.
- Tip state: no runnable interactive TNN exists on this branch
  beyond the frozen probe instruments (the archived tnn_chat.zag
  and tnn_chat_decline.zag, which hold a stdin line loop over the
  38-fact KB).

Result: no new chat/REPL/interactive entry points. Frozen pins all
match: binary pins 1ada2fae... and 20273a99... (verified on
rebuild), znc pin 498abcb5... (verified on
src/tools/toolchain/znc_linux_x86_64_abed8aa1), source pins
c0776ad6... and a87011fe... (verified on
docs/lab/rsi/fit_authority/).

## Verdict: FRESH FIT PASS on d24eda8bdc34dee54aace6451b193754e96784ab

Numbers: KB1 30/30 specific declines, 0 blanket refusals (3 runs);
KB2 17/17 answered, 0 declines, byte-identical baseline parity (3
runs each); KB5 10/10 answered, 0 declines, byte-identical baseline
parity (3 runs each); binary reproducibility 2/2 PASS; rerun
determinism 9/9 required run-pairs byte-identical; decline/baseline
parity 2/2. FIT staleness resets to 0 of 8.

No em-dashes used in this document.
