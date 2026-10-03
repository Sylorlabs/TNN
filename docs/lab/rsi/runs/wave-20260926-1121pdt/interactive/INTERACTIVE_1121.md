# Interactive TNN investigation: wave-20260926-1121pdt

Branch: tnn-native-lab
Working copy: ~/workspace/tnn-rsi
HEAD: 02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2 (merge of origin tip 94625817c; 15 new upstream commits, CLOSED and not re-litigated)
Read-only investigation of the merged tip. No probe chats were run.

## Standing question: does a runnable interactive TNN exist on this branch?

Negative on source entry points, with the same caveat as every prior
wave. There is no source-level chat/REPL entry point in the Zag source
tree, but the frozen FIT probe instruments still exist in runnable form
with the pinned znc, and the frozen built binaries still exist and are
executable.

## 1. Source-level chat/REPL entry point

NONE. Verified on this tip:

- `grep -rliE "repl|interactive|chat" src/zag/ units/` returned exactly
  one file: units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md. That
  is a false positive: the matches are the substring "repl" inside the
  words "replay" and "replication". It is not a REPL or chat entry
  point.
- A follow-up grep for entry-point signatures
  (`fn main|stdin|readline|read_line|interactive_loop|repl_loop`) over
  src/zag/ and units/ (source files and docs) returned zero files.
- `git log` on the merge range 4bbbca69c..02ee5ae59 (21 commits) shows
  zero commits touching src/ or units/ at all; the newly added file
  scan (`git diff --name-only --diff-filter=A` filtered on chat|repl|
  interactive) returned nothing. No merged upstream work added a
  chat/repl-named file to src/ or units/.
- src/zag/ contains only INDEX.md: no chat/repl/interactive matches.

Conclusion: no source-level chat/REPL/interactive-loop entry point
exists in src/zag/ or units/ on this tip, and the merge delta added no
interactive surface. The negative finding of the prior waves stands.

## 2. Runnable probe chat surface (availability only)

All existence checks are `file` + `sha256sum` only. No binary was
executed; probe chats are supervised red-team work, not this worker's
job. A supervised probe run is scheduled only when the survey reveals
change. This survey revealed no change, so no probe chat was run.

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
post-hoc. `git diff` 4bbbca69c..02ee5ae59 over the chain paths
(docs/lab/rsi/fit_authority/, src/tools/toolchain/,
docs/lab/dialogue/, docs/lab/bytegen/authority_law/dialogue/) is
empty: the merge did not alter any FIT chain input.

### Built binaries

1. Baseline probe binary (reference build):
   ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt
   ELF 64-bit LSB executable, x86-64, statically linked.
   sha256: 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
   Matches the frozen built binary sha in the authority record.
   RUNNABLE.

2. Decline-gate probe binary (frozen reference):
   docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref
   ELF 64-bit LSB executable, x86-64, statically linked.
   sha256: 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
   Matches the frozen built binary sha for tnn_chat_decline.zag.
   RUNNABLE. Its sibling source
   tnn_chat_decline_frozen_ref.zag is also present in the same dir.

### Toolchain (pinned znc)

src/tools/toolchain/znc_linux_x86_64_abed8aa1
ELF 64-bit LSB executable, x86-64, statically linked.
sha256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
Matches the recorded pinned toolchain sha used for every FIT rebuild
since wave-20260924-1121pdt. The authority sources build
deterministically with it (recorded rebuild shas 1ada2fae... and
20273a99... above).

## 3. Why no probe chat was run

The standing rule schedules a supervised probe run only when the survey
reveals change. This survey revealed no change: zero source-level entry
points, the merge delta added no chat/repl surface, and every frozen
instrument, binary, and the pinned znc verify byte-identical to their
recorded shas. Availability was verified; execution was not needed.

## Caveats for supervised red-team probe chats

- tnn_chat emits unflagged confabulations on out-of-KB questions (e.g. "Paris is the capital of France" for capital of Italy)
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
- Pinned build toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (sha verified).

DOES NOT EXIST:
- No source-level chat/REPL/interactive-loop entry point in src/zag/
  or units/ on this tip. The only grep hit was a "repl" substring false
  positive inside "replay"/"replication" in a brief doc.
- No new interactive entry point added by the 4bbbca69c..02ee5ae59
  merge (21 commits, zero touching src/ or units/).
- No freshly rebuilt probe binary this wave (not needed: frozen
  binaries and sources both verified byte-identical).

## Python attestation

No Python was used anywhere in this work. All verification was done
with shell commands only: grep, file, sha256sum, git log, git diff,
git show. Zero Python touched wave artifacts.
