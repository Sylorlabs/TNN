# INTERACTIVE-TNN SURVEY: wave-20260926-2321pdt

Date: 2026-09-26 PDT. Working copy: ~/workspace/tnn-rsi at run-start HEAD 377c36fd9.
Merge range scanned: 5ba241235..377c36fd9 (8 commits). Read-only survey.

## 1. New chat/REPL entry points: NONE FOUND

Zero new chat/REPL/interactive entry points were added in the merge range.

Evidence:
- Added-file name scan (diff-filter=A on the range, word-boundary match on
  chat or repl, excluding replay/replica): zero matches.
- Content scan of the range diff for word-boundary chat or repl hits: zero
  genuine code hits.
- The merge range is owner-frontier work: Micah's commits (Experiment 1 and
  Experiment 2 frozen preregs, deliberation v1 repair #4, audio de-synth
  round 2, upscale repair round 2 KILLED, MP3 risks closure, Dialogue
  round-4 ADOPTED) plus the wave's merge commit and the prior wave's own
  evidence commit. All owner work is treated as CLOSED, not re-litigated.

## 2. Known entry point status (unchanged)

- docs/lab/rsi/fit_authority/tnn_chat.zag (frozen DIALOGUE v1 retrieval core
  plus interactive stdin loop) still present at the tip.
- Built binary ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt
  present, sha256 prefix 1ada2fae63dd matches the frozen pin recorded on
  2026-09-23 (1ada2fae). Unchanged since the 2021pdt wave's PASS.
- Traveling caveats unchanged: FIT FOR SUPERVISED red-team probe chats
  only; the machinery emits unflagged confabulations on out-of-KB questions
  (documented failure class); see
  docs/lab/rsi/runs/wave-20260923-0834pdt/tnn_chat_caveats.md.

## 3. Runnability verdict for this wave

Runnable interactive TNN EXISTS on this branch (tnn_chat.zag source plus
the pinned binary). No new entry points this wave. Nothing needs escalation.
