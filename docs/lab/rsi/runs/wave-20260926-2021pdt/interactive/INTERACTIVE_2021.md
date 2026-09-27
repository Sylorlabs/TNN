# INTERACTIVE-TNN SURVEY: wave-20260926-2021pdt

Date: 2026-09-26 PDT. Working copy: ~/workspace/tnn-rsi at HEAD fe1b5e2c0.
Merge range scanned: 45d449a56..fe1b5e2c0 (19 commits). Read-only survey.

## 1. New chat/REPL entry points: NONE FOUND

Zero new chat/REPL/interactive entry points were added in the merge range.

Evidence:
- Added-file name scan (diff-filter=A on the range, word-boundary match on
  chat or repl, excluding replay and replication): zero matches.
- Content scan of the range diff for word-boundary chat or repl hits: the
  only matches are prior-wave interactive-survey report prose inside
  LOOP_STATE.md and debate transcripts (reports describing the surveys
  themselves), not code. No genuine code hit.
- git diff --stat 45d449a56..fe1b5e2c0 -- src units: empty. No file under
  src/ or units/ was touched at all in this range.
- Source-tree grep on the tip (src/zag and units/, word-boundary chat or
  repl): zero matches after excluding the known false positive substrings
  (replay, replication, replace, replica, replicate).

Note on a new file that is NOT an entry point: docs/lab/dialogue/round4/
dialogue.zag (introduced in commit 75267f9df, this range) is a batch
prose-learning trial. It takes argv file paths, reads train/test inputs
from files, and emits batch results. It has no stdin prompt, no read loop,
and no interactive REPL path, so it does not qualify as a chat/REPL
entry point.

Conclusion: no source-level chat/REPL entry point exists on this tip, and
no new one was added by this merge range. Nothing to trace to an
introducing commit.

## 2. Frozen pin verification (sha256)

The expected pin values in the wave brief are the frozen BUILT BINARY
shas recorded in docs/lab/rsi/fit_authority/README.md. The frozen source
.zag files have their own distinct recorded source shas, which were also
checked against the README.

### Pin 1: baseline probe (frozen built binary)

Expected: 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
Artifact: ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt
          (reference copy named in wave-20260924-1121pdt/tnnchat/
           EVIDENCE_FIT.md; the original run dir is no longer on this tip)
Computed: 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
Verdict: PASS. Byte-identical.

Source cross-check: docs/lab/rsi/fit_authority/tnn_chat.zag computes to
c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c,
which matches the README recorded source sha exactly.

### Pin 2: decline-gate probe (frozen built binary)

Expected: 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
Artifact: docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/
          tnn_chat_decline_frozen_ref
Computed: 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
Verdict: PASS. Byte-identical.

Source cross-check: docs/lab/rsi/fit_authority/tnn_chat_decline.zag
computes to a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b,
which matches the README recorded source sha exactly.

### Pin 3: pinned znc toolchain binary

Expected: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
Artifact: src/tools/toolchain/znc_linux_x86_64_abed8aa1
Computed: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
Verdict: PASS. Byte-identical.

### Record caveat (carried forward)

docs/lab/rsi/fit_authority/SHA256SUMS does not exist on this tip. This is
a known record defect, not an evidence failure. The frozen shas are
recorded instead in docs/lab/rsi/fit_authority/README.md, and all three
pins verified above against that record.

## 3. tnn_chat status

docs/lab/rsi/fit_authority/tnn_chat.zag is supervised red-team probe-chat
material only: the 38-fact closed-book probe instrument (baseline) and its
decline-gate counterpart. Per the fit_authority README Scope section,
quote: "These instruments certify the 38-fact closed-book probe chain
only. No runnable interactive TNN exists on this branch beyond these
frozen probe instruments." tnn_chat is not an interactive TNN available
for adoption.

## 4. Bottom line

No interactive TNN exists on branch tnn-native-lab at fe1b5e2c0. There is
no source-level chat/REPL entry point in src/zag/ or units/, this merge
range added none (src/ and units/ were untouched), and the only chat
artifacts are the two frozen supervised probe binaries plus their frozen
Zag sources in the fit_authority path. All three frozen pins verify
PASS. tnn_chat remains supervised red-team probe-chat material only and
must not be presented as an interactive TNN available for adoption.
