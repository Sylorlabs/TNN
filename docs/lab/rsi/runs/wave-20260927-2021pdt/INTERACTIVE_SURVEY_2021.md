# Interactive Survey 2021 PDT (wave-20260927-2021pdt)

Re-survey of the merge range `d09d5bfde..fc1a43b8c` for new
chat/REPL/stdin interactive entry points in source.

## Method

1. Resolved the range topology: 30 origin commits
   (`fc1a43b8c^1..fc1a43b8c^2`, all authored by `micahcooley`) plus
   10 local first-parent commits (the 1721pdt wave's own records).
2. Listed all 11,765 files added in the range (2,098 of them
   `*.zag`); built the full added-file `*.zag` diff
   (`git diff d09d5bfde fc1a43b8c --diff-filter=A -- '*.zag'`,
   217,516 lines) and scanned every added line for interactive
   indicators: `chat`, `repl`, `stdin`, `readln`, `readline`,
   `argv`, `interactive`, `tui`, plus raw fd-0 reads
   (`_zag_raw_syscall(0,0,...)`).
3. Separately enumerated all 184 `*.zag` files added by the 30
   origin commits and grepped each working-tree copy for fd-0
   reads.
4. Checked the adding commit and author for every hit, and checked
   the 10 local first-parent commits' added `.zag` sources
   (EXP1c iteration 1, 5168f0448) for indicators.

## New interactive entry points found

Three new stdin/chat entry points, all Micah-authored, all in his
closed D2 new-learner line under `docs/lab/composition/d2_newlearner/`.

### 1. h1.zag chat REPL (H1 practice-trace induction learner)

- Commit: `9dbd01e26` (micahcooley, 2026-09-27, "H1 practice-trace
  induction learner build (h1.zag + docs)")
- File: `docs/lab/composition/d2_newlearner/build/h1/h1.zag`
- Mode: `<binary> chat` prints a banner line, then one stdin line
  yields one `A ...` reply; input read via `read_line()` on fd 0
  (`_zag_raw_syscall(0,0,...)`).
- Status: **Micah's closed frontier.** Read-only awareness only.
  Not built, not run, not certified, not re-judged by the loop.

### 2. h2.zag chat REPL plus fuzz stdin driver (H2 taught-physics learner)

- Commit: `7979a55b1` (micahcooley, 2026-09-27, "H2 taught-physics
  world model + 64-tick lookahead planner (D2 new learner)")
- Files: `docs/lab/composition/d2_newlearner/build/h2/h2.zag`
  (main chat loop, `argv[1]=="chat"`: banner line, one `A ...`
  reply per input), `docs/lab/composition/d2_newlearner/build/h2/model.zag`
  (the fd-0 `read_line()` the loop calls),
  `docs/lab/composition/d2_newlearner/build/h2/fuzz.zag`
  (fuzz driver reading actions on stdin, one digit per line; a test
  instrument, not a chat).
- Status: **Micah's closed frontier.** Read-only awareness only.

### 3. h3.zag chat / chat-fixed / chattrace modes (H3 deliberative scheduler)

- Commit: `7f5a8ccdb` (micahcooley, 2026-09-27, "H3
  deliberative-scheduler action-policy learner (D2 new-learner
  build)")
- File: `docs/lab/composition/d2_newlearner/build/h3/h3.zag`
- Modes: `chat` (deliberative scheduler, Section L chat loop: every
  stdin line yields exactly one stdout line starting with `A `),
  `chat-fixed` (fixed-order control), `chattrace` (chat plus
  internal deliberation trace-ring dump). Input via fd-0
  `_zag_raw_syscall(0,0,...)`.
- Status: **Micah's closed frontier.** Read-only awareness only.

## Explicitly not new interactive entry points

- The 16 other fd-0-reading `.zag` files in the added diff are all
  pre-existing: the frozen batch probe instruments
  (`docs/lab/rsi/fit_authority/tnn_chat.zag`,
  `tnn_chat_decline.zag`, frozen at b650ea46f) and old-wave CV-1 /
  CV-P / COMP-2 batch instruments (1783234e0, 5c53da6ba, 91b7ee160,
  575c96d28, 358a8013c, 63cef111d, 621e10957). Inherited, not new.
- EXP1c iteration 1 sources (5168f0448,
  `docs/lab/rsi/runs/wave-20260927-1721pdt/exp1c/src/*.zag`):
  batch survival sim, zero interactive indicators. Clean.
- The one `tui` hit in new sources is a code comment in H2
  referencing the existing `d2bin tui` OBS lines (Micah's
  597aa311f instrument, surveyed at 1721pdt). No new tui mode.
- Prior known entries remain as surveyed at 1721pdt and are not
  re-listed as new: `wb3_nosynth.zag` and `wb3_stringrule.zag`
  chat REPLs (13c557cd3, Micah's closed composition-redo line) and
  the `d2.zag` `tui` game-sim instrument (597aa311f, Micah's).

## Verdict

**NONE loop-owned.** No loop-built, loop-run, loop-certified
interactive TNN exists on this branch beyond the frozen batch probe
instruments (`docs/lab/rsi/fit_authority/tnn_chat.zag`,
`tnn_chat_decline.zag`, batch-only). The three new chat entry
points this wave (h1, h2, h3) are Micah-authored in his closed D2
new-learner frontier: surveyed read-only, never built, run,
certified, or re-judged by the loop.

The six governance rulings stay OPEN and are Micah's; nothing in
this survey relitigates them.
