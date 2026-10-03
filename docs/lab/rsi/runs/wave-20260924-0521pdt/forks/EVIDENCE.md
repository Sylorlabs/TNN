# Fork battery evidence, wave-20260924-0521pdt

Wave id: wave-20260924-0521pdt. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, HEAD 8a9052b85 ("FS-E4b verdict: fill in final commit SHAs").
Wave lock held by the coordinator (untouched).

## Enumerated forks

Five refs tested; no others exist. `git rev-parse forktest/main` fails
before and after `git fetch origin`: the six forktest/* detached worktrees
tested last wave are absent from this reset clone. Recorded as absent,
not tested.

| Branch | Commit | PASS/FAIL | znc sha256 |
|---|---|---|---|
| local tnn-native-lab | 8a9052b85 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| remotes/origin/tnn-native-lab | 8a9052b85 | PASS (read-only via git show; no reset, merge, or push) | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| local tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| local tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| local wave-debate-session-1-backup | 3947dca1a | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/main, r2-7, reorg_phase-0-1, tnn-native-lab, wg-freeze, tnn-native-lab-remote | absent | NOT TESTED (refs do not exist) | n/a |

Pinned znc value for every fork's own tree copy:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(extracted via git show for origin, working-tree copy for locals; scratch
copies chmod +x; working trees untouched).

## Shell harness results (per fork, its own znc copy)

Every fork: B1 PASS (compile exit 0, run exit 0, stdout byte-identical to
FORKBATTERY-OK 42, sha256 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066).
B2 PASS (rerun stdout identical; two compiles byte-identical, binary sha256
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2 on both).
B3 PASS (znc check file.zag --strict --no-zagd exit 0, "znc: OK - all
capability claims proven"). NEG1 fails as required (compile exit 1,
E0002 unterminated string literal; check exit 1). NEG2 fails at the
byte-compare step as required (compile exit 0, check exit 0, stdout
differs: char 1, line 1). Per-fork full logs: scratch/<label>/harness.log.

One harness bug was caught and fixed before any verdict: the first run
compared "sha256sum < file" output ("<hash>  -") against the bare
expected hash, so all five forks reported a spurious B2 failure while the
binary hashes were in fact correct (75b85d3...). The comparison was fixed
to cut the hash field; the rerun passed. Verdicts above are from the
fixed rerun.

## Pure-Zag harness results

fork_battery.zag extracted read-only from archive branch
tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag;
507 lines, sha256 f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
as required (not rebuilt from scratch). Built fresh with the pinned znc
(build exit 0; built binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).
Ran in per-fork scratch dirs with ./znc.path pointing at each fork's own
extracted znc copy. Result: VERDICT=PASS, exit 0, on all five forks
(B1=PASS, B2=PASS, B3=PASS, NEG1 fails as required, NEG2 fails as required).
Full reports: scratch/<label>/zagharness.out.

Harness parity: the pure-Zag instrument and the shell harness agree on all
five forks (5/5 PASS each).

## tnn_chat FIT check (item 6 of the wave job)

Chat entry point in the working copy at HEAD: docs/lab/dialogue/
(dialogue.zag variants; canonical kb.txt/gaz.txt at
docs/lab/dialogue/kb.txt and docs/lab/dialogue/gaz.txt). A runnable
interactive TNN exists: the archived baseline tnn_chat.zag (wave
20260923-0834pdt source) and the decline tnn_chat_decline.zag (wave
20260923-1121pdt source) both rebuild and run on this HEAD's toolchain.

Method (same as the prior wave, per the 0221pdt EVIDENCE.md tnn_chat FIT
section): sources pulled read-only from the archive
(tnn-native-lab-wave-archive-20260923-2321pdt) and rebuilt with this
HEAD's pinned znc in /tmp/fitchat0521 (scratch only). Source shas matched
the prior wave's recorded values before building: baseline tnn_chat.zag
c0776ad6..., decline tnn_chat_decline.zag a87011fe..., R33_NATIVE_IO_V1.zag
e6379ddb..., R33_NATIVE_SHA256_V2.zag 9824f6db.... The chat driver reads
kb.txt/gaz.txt from CWD: HEAD's canonical docs/lab/dialogue/ copies match
the recorded fixtures (kb.txt 3ef27296..., gaz.txt b75fd113...); 38 facts
loaded.

Binary reproducibility (this HEAD's znc):
- Baseline tnn_chat.zag rebuild: sha256
  1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
  byte-identical to the reference
  ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt. PASS.
- Decline tnn_chat_decline.zag rebuild: sha256
  20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
  byte-identical to the prior wave's recorded candidate build (and to the
  archived prebuilt binary in interactive/). PASS.

Probe results (frozen fixtures kb1_out30.txt, kb2_inkb.txt, kb5_nogame.txt
from the archive):
- KB1 re-decline (30 adversarial out-of-KB turns): 30/30 specific declines
  on each of 3 runs. Every decline cites a specific miss with quoted
  unknown words (26 use "My knowledge base contains nothing about ...",
  4 use the "No knowledge-base fact connects/covers ..." phrasing);
  0 blanket refusals. Run 1 output byte-identical to the prior wave's
  recorded kb1_out30_r1.txt. Full outputs: scratch/fitchat0521/.
- KB2 in-KB (17 turns): 0 declines; decline-binary output byte-identical
  to the rebuilt baseline binary on all 3 runs (zero regression); answers
  correct (e.g. "Herman Melville wrote the novel Moby Dick.").
- KB5 no-decline-gaming (10 required in-KB answers): 10/10 answered,
  0 declines, byte-identical to baseline on all 3 runs.
- Rerun determinism: 9/9 run-pairs byte-identical (r1/r2, r2/r3, r1/r3 for
  each of the three fixtures).

Verdict: FIT. Numbers: binary reproducibility 2/2; KB1 30/30 specific
declines, 0 blanket refusals (3 runs); KB2 0 declines with byte-identical
baseline parity (3 runs); KB5 10/10 answered with 0 declines and baseline
parity (3 runs); rerun determinism 9/9 run-pairs byte-identical.

## Blockers

None. No Python was used anywhere in this work (shell commands only for
extraction, building, running, and greps).

## Files

- EVIDENCE.md (this file)
- scratch/<label>/RESULT.txt: per-fork verdicts
- scratch/<label>/harness.log: shell harness full logs
- scratch/<label>/zagharness.out: pure-Zag instrument full reports
- scratch/fitchat0521/: tnn_chat FIT build logs and probe outputs
