# Interactive TNN investigation: wave-20260926-0821pdt

Branch: tnn-native-lab
Working copy: ~/workspace/tnn-rsi
HEAD: 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5
Read-only investigation. No commits, no pushes, no merges, no fetches,
no resets. No probe chats were run.

## Standing question: does a runnable interactive TNN exist on this branch?

YES, with the same caveat as every prior wave. There is still no
source-level chat/REPL entry point in the Zag source tree, but the
frozen FIT probe instruments still exist in runnable form with the
pinned znc, and frozen built binaries still exist and are executable.

## 1. Source-level chat/REPL entry point

NONE. Verified on this tip:

- `grep -rliE "repl|interactive|chat" src/zag/ units/` returned exactly
  one file: units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md. That
  is a false positive: the match is the substring "repl" inside words
  like "replication" and "replay". It is not a REPL or chat entry point.
- A follow-up grep for entry-point signatures
  (`fn main|stdin|readline|read_line|interactive_loop|repl_loop`) over
  src/zag/ and units/ returned zero files.
- `git diff` between the 0521pdt wave HEAD (d0076134) and this tip
  shows no new file matching *chat* or *repl* in src/ or units/.
  The only name match in the delta is the prior wave's own
  INTERACTIVE_0521.md doc.

Conclusion: no merged upstream work since the 0521pdt wave has added a
chat/REPL/interactive-loop entry point to src/zag/ or units/. The
finding of the prior waves is unchanged.

## 2. Runnable chat binaries in run dirs (and durable paths)

All existence checks are `file` + `sha256sum` only. No binary was
executed; probe chats are supervised red-team work, not this worker's
job.

### Frozen FIT authority instruments (never-prune path)

docs/lab/rsi/fit_authority/ (authority manifest: AUTHORITY_MANIFEST.md)

| Artifact | Path | sha256 | Status |
|---|---|---|---|
| baseline instrument source | docs/lab/rsi/fit_authority/tnn_chat.zag | c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c | matches frozen sha |
| decline-gate instrument source | docs/lab/rsi/fit_authority/tnn_chat_decline.zag | a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b | matches frozen sha |
| knowledge base (38 facts) | docs/lab/rsi/fit_authority/kb.txt | 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1 | matches frozen sha |
| gazetteer | docs/lab/rsi/fit_authority/gaz.txt | b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a | matches frozen sha |

Provenance (per README.md): extracted read-only with git show from
branch tnn-native-lab-wave-archive-20260923-2321pdt during
wave-20260925-1421pdt; byte-identical to frozen shas; never edited
post-hoc.

### Built binaries

1. Baseline probe binary (reference build):
   ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt
   ELF 64-bit LSB executable, x86-64, statically linked.
   sha256: 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
   Matches the frozen built binary sha in the authority manifest.
   RUNNABLE.

2. Decline-gate probe binary (frozen reference):
   docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref
   ELF 64-bit LSB executable, x86-64, statically linked.
   sha256: 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
   Matches the frozen built binary sha for tnn_chat_decline.zag.
   RUNNABLE. Its sibling source
   tnn_chat_decline_frozen_ref.zag is also present in the same dir.

3. CVP retest binaries (wave-20260925-0821pdt):
   docs/lab/rsi/runs/wave-20260925-0821pdt/cvp_retest/bin/cvp
   docs/lab/rsi/runs/wave-20260925-0821pdt/cvp_retest/bin/cv1c
   docs/lab/rsi/runs/wave-20260925-0821pdt/cvp_retest/bin/gate_op
   All three are ELF 64-bit LSB executables, x86-64, statically linked.
   These are the candidate/probe binaries from the CVP retest, with
   fixtures (kb.txt, gaz.txt) and sealed probes/keys under the same
   cvp_retest dir.

### Toolchain (pinned znc)

src/tools/toolchain/znc_linux_x86_64_abed8aa1
ELF 64-bit LSB executable, x86-64, mode -rwxr-xr-x.
sha256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
Matches the recorded pinned toolchain sha used for every FIT rebuild
since wave-20260924-1121pdt. The authority sources build deterministically
with it (recorded rebuild shas 1ada2fae... and 20273a99... above).

Note: znc is not on PATH in this shell, but the pinned binary is present
and executable in the repo tree.

## 3. Caveats for supervised red-team probe chats

- tnn_chat emits unflagged confabulations on out-of-KB questions (e.g.
  "Paris is the capital of France" for capital of Italy).
- FIT FOR SUPERVISED red-team probe chats only (knowledge vs
  architecture diagnosis). Not a general assistant, not a candidate for
  adoption.
- No probe chat was run in this investigation. Availability only was
  verified.

## What exists vs what does not

EXISTS:
- Frozen probe instrument sources: docs/lab/rsi/fit_authority/tnn_chat.zag
  and tnn_chat_decline.zag, plus frozen kb.txt and gaz.txt (all shas
  verified against the authority manifest).
- Runnable baseline probe binary:
  ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt (sha
  verified).
- Runnable decline-gate probe binary:
  docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref
  (sha verified).
- Runnable CVP retest binaries: docs/lab/rsi/runs/wave-20260925-0821pdt/cvp_retest/bin/{cvp,cv1c,gate_op}.
- Pinned build toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (sha verified).

DOES NOT EXIST:
- No source-level chat/REPL/interactive-loop entry point in src/zag/
  or units/ on this tip. The only grep hit was a "repl" substring false
  positive inside "replication"/"replay" in a brief doc.
- No new interactive entry point added by any merged upstream work since
  the 0521pdt wave.
- No freshly rebuilt tnn_chat binary this wave (not needed: frozen
  binaries and sources both verified byte-identical).
