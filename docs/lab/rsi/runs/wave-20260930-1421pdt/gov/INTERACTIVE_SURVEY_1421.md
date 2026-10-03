# INTERACTIVE_SURVEY_1421.md

Wave: wave-20260930-1421pdt. Run-start tip: d5984f313.

## What was checked

1. New or modified .zag files in range d5984f313..HEAD: the range is
   EMPTY. HEAD is the run-start tip; no commits landed on the branch
   during the wave before this check (verified with git log).
2. Chat-pattern scan of the branch: `git grep -iE "repl|interactive|chat|stdin|readline"` over src/ returns only
   substring hits inside experiment names (e.g. TERMINAL, qualification
   discriminators) and reference-only Python files. No new REPL, chat
   loop, stdin-driven, or prompt-loop entry point exists anywhere new.
3. Frozen FIT authority path docs/lab/rsi/fit_authority/: tnn_chat.zag
   and tnn_chat_decline.zag are present, byte-identical to the frozen
   manifest at the current tip. Verified this wave with sha256sum:
   tnn_chat.zag = c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c (matches),
   tnn_chat_decline.zag = a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b (matches).

## Verdict

NONE new [NEW]. No interactive TNN instrument was introduced this wave.

A runnable interactive instrument EXISTS on the branch: the frozen
probe instruments tnn_chat.zag and tnn_chat_decline.zag (frozen at
wave 20260925-0221pdt). However, the FIT chain is stale for the
current architecture: the last fresh FIT re-run was be5bb24c8
(wave-20260927-0821pdt; KB1 30/30, KB2 17/17, KB5 10/10), and the
following landed after it: CLA-2 (e639904f2), CAM-1 (371d20743), ACT
(f7d87938f), the protected-core ISA ruling, and the C1 pure-Zag
driver (d5984f313). The frozen probe instruments therefore probe a
pre-ISA-ruling architecture. Red-teamed probe chats for
knowledge-vs-architecture diagnosis of the CURRENT substrate cannot
be claimed current until a fresh FIT re-run covers CLA-2/CAM-1/ACT.

No instrument was executed for this survey (survey only; no build or
smoke test). The FIT re-run is queued to the coordinator, not claimed
by this lane.

No em-dashes in this documentation.
