# tnn_chat FIT re-certification: wave-20260925-0221pdt

Path taken: FRESH RE-RUN. This is not a candidate verdict and it is not merge review of the merged-in work. It certifies the 38-fact closed-book probe chain only.

## Literal scope

Working HEAD is b4507fb22fa176de9d2e4029400ed034802135bd (post-merge HEAD; the merge folded origin tip 4050b1097, Micah's Math R2 QUOT verdicts and AMBIG gallery, which are CLOSED and not re-litigated). This report certifies only the frozen 38-fact closed-book probe chain: the two frozen probe instruments (baseline tnn_chat.zag, decline tnn_chat_decline.zag), the two R33 support sources, the canonical kb.txt and gaz.txt, the pinned toolchain, the three probe fixtures, and the expected classes. Nothing in docs/lab/senses/pam-rebuild/ was touched. Nothing was pushed to GitHub. Nothing was committed by this worker.

## Carry-over precondition check (standing rule, judge M3)

All four must hold for carry-over; any failure forces a fresh re-run.

### (1) The frozen chain is fully enumerated: PASS

Facts: 38 facts (ids 0 through 37), the exact kb.txt content at canonical sha 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1, 38 lines:

0 Herman Melville wrote the novel Moby Dick.
1 Herman Melville was born in 1819.
2 Moby Dick was published in 1851.
3 Moby Dick was written by Herman Melville.
4 Jane Austen wrote the novel Pride and Prejudice.
5 Jane Austen was born in 1775.
6 Pride and Prejudice was published in 1813.
7 Pride and Prejudice was written by Jane Austen.
8 Charles Darwin wrote On the Origin of Species.
9 Charles Darwin was born in 1809.
10 On the Origin of Species was published in 1859.
11 On the Origin of Species was written by Charles Darwin.
12 Marie Curie discovered radium.
13 Marie Curie was born in 1867.
14 Marie Curie won the Nobel Prize in 1903.
15 Andy Weir wrote The Martian.
16 Andy Weir was born in 1972.
17 The Martian was published in 2011.
18 The Eiffel Tower is in Paris.
19 The Eiffel Tower was built in 1889.
20 The Eiffel Tower is 330 meters tall.
21 The Montparnasse Tower is in Paris.
22 The Montparnasse Tower was built in 1973.
23 The Montparnasse Tower is 210 meters tall.
24 The Louvre is in Paris.
25 The Louvre opened as a museum in 1793.
26 The Statue of Liberty is a landmark in New York.
27 The Statue of Liberty was dedicated in 1886.
28 The Statue of Liberty is 93 meters tall.
29 Big Ben is a landmark in London.
30 Big Ben is 96 meters tall.
31 The Colosseum is in Rome.
32 The Colosseum was completed in 80 AD.
33 Paris is the capital of France.
34 Berlin is the capital of Germany.
35 Water boils at 100 degrees Celsius at sea level.
36 Mount Everest is 8849 meters tall.
37 The Amazon River is 6400 kilometers long.

Gazetteer: gaz.txt at canonical sha b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a, 27 lines.

Probe inputs and expected classes:
- KB1 (kb1_out30.txt, 30 adversarial out-of-KB turns, sha 936c35e11706e98f08ea0dbe0b33f2c6d93c1a301c7a3e003f850e5f610b8188): 30/30 specific declines (26 phrasing "My knowledge base contains nothing about ...", 4 phrasing "No knowledge-base fact connects/covers ..."), 0 blanket refusals.
- KB2 (kb2_inkb.txt, 17 in-KB turns, sha 730e2d246926bbd91909da1799b7327c9cba586085dbfa79e2407bcc39883184): 17/17 answered, 0 declines, output byte-identical to baseline.
- KB5 (kb5_nogame.txt, 10 in-KB turns, sha b60198b059f332eb821be257eb130e59c3e22009600ba89abd04cf267ee86a38): 10/10 answered, 0 declines, output byte-identical to baseline.

Instrument sources and expected binaries:
- baseline tnn_chat.zag, frozen sha c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c; frozen binary sha 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c.
- decline tnn_chat_decline.zag, frozen sha a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b; frozen binary sha 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7.
- R33_NATIVE_IO_V1.zag, frozen sha e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8.
- R33_NATIVE_SHA256_V2.zag, frozen sha 9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf.
- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1, pinned sha 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.

Expected output hashes (prior wave records): KB1 a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308; KB2 e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264; KB5 4f1603aa2a798a97679e91f54c0614d0de8465856a982a61debc54bc4670e88d.

### (2) Inputs extracted read only from the archive branch tnn-native-lab-wave-archive-wave-20260924-2321pdt: FAIL

Command used (content-sha scan over the archive branch, git show with no checkout):

git ls-tree -r --name-only tnn-native-lab-wave-archive-wave-20260924-2321pdt docs/lab/rsi/runs | grep -vE '\.(md|txt|json|py|sh|err|log)$' then git show <ref>:<path> | sha256sum compared against the four frozen source shas.

Result: the baseline instrument source tnn_chat.zag (frozen sha c0776ad6...) is ABSENT from the designated archive branch. No file anywhere in docs/lab/rsi/runs, docs/lab/dialogue, or docs/lab/bytegen of that branch matches that content sha. The 09-23 run directories that held it were pruned from this archive snapshot. Present and verified in the designated archive branch: decline source as docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref.zag (sha a87011fe..., matches frozen decline source), the decline binary frozen ref at the same dir without extension (sha 20273a99..., matches frozen decline binary), R33_NATIVE_IO_V1.zag and R33_NATIVE_SHA256_V2.zag at docs/lab/bytegen/authority_law/dialogue/ (shas match frozen), kb.txt and gaz.txt at docs/lab/dialogue/ (shas match canonical), and the three fixtures under docs/lab/rsi/runs/wave-20260924-0521pdt/forks/scratch/fitchat0521/ (shas 936c35e1..., 730e2d24..., b60198b0..., byte-identical to the fixtures the 2321pdt wave used from the older archive branch). One missing chain input is a hard failure of precondition (2). Per the standing rule this is not a blanket license to skip: a FRESH RE-RUN was performed instead.

### (3) Diff of the enumerated chain across the merge verified empty: PASS

Command: git diff tnn-native-lab-wave-archive-wave-20260924-2321pdt b4507fb22 --stat -- docs/lab/dialogue/kb.txt docs/lab/dialogue/gaz.txt docs/lab/bytegen/authority_law/dialogue/ docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/ docs/lab/rsi/runs/wave-20260924-0521pdt/forks/scratch/fitchat0521/ src/tools/toolchain/znc_linux_x86_64_abed8aa1

Output: empty (exit 0). No difference on any chain-relevant path.

The merge itself (diff e33b5ddb..b4507fb22) touched 115 files, all under docs/lab/ambig_1080p, docs/lab/math_logic, and docs/lab/onebrain (Micah's Math R2 QUOT verdicts and AMBIG gallery plus related frontier work). All disjoint from the FIT chain paths. The merge introduced no FIT-relevant change.

### (4) Determinism already established: PASS

Cited from the 2321pdt record: binary reproducibility 2/2 PASS (decline rebuild byte-identical to 20273a99, baseline byte-identical to 1ada2fae); rerun determinism 9/9 run-pairs byte-identical; all three output hashes (a2ca4dd7, e05fb4ec, 4f1603aa) byte-identical to the prior wave's records. All 15 runs exited 0 with empty stderr.

## Fresh re-run procedure (pure Zag, zero Python)

Because precondition (2) failed, a fresh re-run was performed on HEAD b4507fb22. Sources extracted read only (git show, no checkout) and sha-verified before use:

- tnn_chat.zag and tnn_chat_decline.zag from archive branch tnn-native-lab-wave-archive-20260923-2321pdt (paths docs/lab/rsi/runs/wave-20260923-0834pdt/tnn_chat.zag and docs/lab/rsi/runs/wave-20260923-1121pdt/tnn_chat_decline.zag): shas c0776ad6... and a87011fe..., both match the frozen record.
- R33_NATIVE_IO_V1.zag and R33_NATIVE_SHA256_V2.zag from archive branch tnn-native-lab-wave-archive-wave-20260924-2321pdt (docs/lab/bytegen/authority_law/dialogue/): shas e6379ddb... and 9824f6db..., both match the frozen record.
- kb.txt and gaz.txt from HEAD b4507fb22: shas 3ef27296... and b75fd113..., both match canonical.
- Fixtures kb1_out30.txt, kb2_inkb.txt, kb5_nogame.txt from archive branch tnn-native-lab-wave-archive-wave-20260924-2321pdt (docs/lab/rsi/runs/wave-20260924-0521pdt/forks/scratch/fitchat0521/): shas 936c35e1..., 730e2d24..., b60198b0..., byte-identical to the fixtures used by the 2321pdt wave.
- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1 from HEAD: sha 498abcb5..., matches the pinned record.

Build: znc tnn_chat_decline.zag -o tnn_chat_decline (exit 0); znc tnn_chat.zag -o tnn_chat (exit 0). The sources @import R33_NATIVE_SHA256_V2.zag by relative name; the archive copy was staged into the build dir. Build host: ~/workspace/tnn-fitchat-0221pdt/ (outside the repo; build logs and all probe outputs retained there). Both binaries ran from the directory containing the verified kb.txt and gaz.txt copies. 38 facts loaded at startup on every run. No Python was used anywhere in this work (shell coreutils only for extraction, building, running, and greps; no Python contact, so no evidence is voided).

Binary reproducibility on HEAD b4507fb22: 2/2 PASS.
- Decline rebuild: sha256 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7 (byte-identical to the frozen 20273a99 record).
- Baseline rebuild: sha256 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c (byte-identical to the frozen 1ada2fae record).

## Probe results (3 runs each, all exit 0, all stderr empty)

- KB1 re-decline (30 adversarial out-of-KB turns, decline binary): 30/30 specific declines on each of 3 runs. Per run: 26 turns use "My knowledge base contains nothing about ..." and 4 turns use the "No knowledge-base fact connects/covers ..." phrasing. 0 blanket refusals on all 3 runs. Output sha256 a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308 on every run, byte-identical to the prior wave's recorded output.
- KB2 in-KB (17 turns, decline binary): 17/17 answered, 0 declines on all 3 runs. Output sha256 e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264 on every run, byte-identical to the rebuilt baseline binary on all 3 runs (zero regression).
- KB5 no-decline-gaming (10 required in-KB answers, decline binary): 10/10 answered on each of 3 runs, 0 declines. Output sha256 4f1603aa2a798a97679e91f54c0614d0de8465856a982a61debc54bc4670e88d on every run, byte-identical to the baseline binary on all 3 runs.
- Rerun determinism: 9/9 required run-pairs byte-identical (r1/r2, r2/r3, r1/r3 for each of the three fixtures, verified with cmp). The six baseline run-pairs were also byte-identical.

All stderr logs empty; no runtime errors. All 15 runs exited 0.

## Verdict: FIT on b4507fb22fa176de9d2e4029400ed034802135bd

Numbers: precondition (2) failed so a fresh re-run was performed on HEAD; binary reproducibility 2/2 PASS (byte-identical to 20273a99 and 1ada2fae); KB1 30/30 specific declines, 0 blanket refusals (3 runs); KB2 17/17 answered, 0 declines, byte-identical baseline parity (3 runs each of decline and baseline); KB5 10/10 answered, 0 declines, byte-identical baseline parity (3 runs each); rerun determinism 9/9 run-pairs byte-identical. All three output hashes byte-identical to the prior wave's records. The b4507fb22 merge introduced no observable FIT deviation. [RE-CERT] tnn_chat FIT

## Caveats (plain language)

This certifies the 38-fact closed-book probe chain only. The chat answers from a fixed 38-fact KB (HEAD's canonical docs/lab/dialogue/kb.txt and gaz.txt); it is a closed-book probe instrument, not an open-domain conversational model. The decline binary is a supervised red-team probe instrument for decline behavior, not a general interactive TNN.

No runnable interactive TNN exists on this branch beyond the frozen probe instruments: the archived tnn_chat.zag and tnn_chat_decline.zag, which hold a stdin line loop (/new resets the conversation) over the 38-fact KB. There is no live learning, no open-domain conversation, and no interactive session beyond those instruments.

Nothing is faked: every number above comes from binaries rebuilt with the pinned znc on HEAD b4507fb22 and run against the frozen fixtures. No Python was used anywhere in this work (shell commands only for extraction, building, running, and greps; no Python contact, so no evidence is voided). Nothing was pushed to GitHub.
