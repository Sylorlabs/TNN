# INTERACTIVE-TNN SURVEY: wave-20260927-0521pdt

Date: 2026-09-27 PDT. Working copy: ~/workspace/tnn-rsi at ecbe9b5b7.
Merge range scanned: 463b115b6..ecbe9b5b7 (10 commits: wave-20260927-0221pdt loop wave commits plus Micah's 5 new commits 73411bdef, 7aad68fad, 7aa40ac0d, ae965e697, 945b061b4 and the merge ecbe9b5b7). Read-only survey, pure shell tools (git, grep, sha256sum). No Python anywhere.

## 1. New chat/REPL/interactive-loop entry points: NONE FOUND

Layered scan results:

* Layer 1, added-file name scan: 1390 added files in the range; word-boundary scan over names for chat|repl|interactive: ZERO hits. All additions are docs/lab lab artifacts: epistemic_native phase1 traces (448+448+448 study traces), audio round3, dialogue/deliberation repair docs, upscale redteam, mg_chunking, determinism reports.
* Layer 2, range-diff content scan: 206,688-line diff; word-boundary hits for chat|repl|interactive: ZERO. Substring check for "repl" yielded only "replan"/"replace(s)" (audio planner M3 closed-loop replan prose, epistemics comments); "chat" and "interactive" substrings: zero. Prior-wave survey prose in the diff was distinguished from code by inspection: all keyword-adjacent hits are design prose, none are code.
* Layer 3, git diff --stat over src/ and units/: zero changed files in the range.
* Layer 4, tip grep of src/zag plus units/ for word-boundary chat|repl: ZERO hits. False-positive check for "repl" inside "replay"/"replication": no such tokens exist anywhere in the diff or the tree.
* Close cases reviewed manually and dismissed:
  - docs/lab/dialogue/deliberation/build/deliberate_frozen_r4repair2.zag (NEW this range, commit 945b061b4 fork-divergence repair): a batch battery runner that reads battery.txt with a DIALOGUE/U-turn loop; zero stdin reads; the same multi-turn harness predates the range (identical loop present in deliberate_frozen_r4.zag and deliberate_frozen_r4repair.zag at the range base 463b115b6). Not a new interactive entry point.
  - docs/lab/epistemic_native/phase1/epistemic.zag (NEW this range, commit 828bc6ee8 pure-Zag deliberation engine): argv-driven CLI with learn/loo modes; zero stdin reads; zero word-boundary keyword hits. A per-claim FACT/OPINION/LIE/UNDETERMINED verdict engine, not a chat/REPL entry point.

## 2. Frozen pin verification (sha256, all PASS)

* Baseline probe binary: 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c, verified on ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt. MATCHES the frozen pin.
* Decline-gate probe binary: 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7, verified on ~/workspace/tnn-fitchat-1421pdt/tnn_chat_decline_1421 (twin binary tnn_chat_decline identical). MATCHES the frozen pin.
* Pinned znc: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, verified on src/tools/toolchain/znc_linux_x86_64_abed8aa1. MATCHES the frozen pin.
* Frozen sources: docs/lab/rsi/fit_authority/tnn_chat.zag is present, sha256 c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c, matching the README pin. docs/lab/rsi/fit_authority/tnn_chat_decline.zag is present, sha256 a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b, matching the README pin. Zero changes to docs/lab/rsi/fit_authority/ anywhere in the merge range.
* No interactive probes were run (standing rule: a supervised probe run happens only when the survey reveals change).

## 3. FIT carry-over per P12/P16: zero change, determinism cited, not re-run

Zero change found, so the tnn_chat FIT CONFIRMATION carries over from the wave-20260925-1421pdt fresh re-run (evidence 9692f5d1d: 2/2 binary reproducibility, 9/9 rerun pairs byte-identical, KB1 30/30, KB2 17/17, KB5 10/10). Determinism is cited from that evidence; nothing was re-run this wave.

Traveling caveats (verbatim):

* Confabulation caveat: tnn_chat emits unflagged confabulations on out-of-KB questions.
* Record defect: docs/lab/rsi/fit_authority/SHA256SUMS does not exist; pins live in fit_authority/README.md.

## 4. Verdict proposal

CONFIRM interactive TNN [RE-CERT]: EXISTS for supervised red-team probe chats only, unchanged.

Nothing to escalate. This file was left in place uncommitted per task instructions.
