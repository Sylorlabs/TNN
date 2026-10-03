# Interactive Survey 1721 PDT (wave-20260927-1721pdt)

Light re-survey of the merge range `9beb0adea..d09d5bfde` (origin/tnn-native-lab
since the last loop survey, merged into local tip `f55e8c27a`) for new
chat/REPL/stdin interactive entry points in source.

## Method

1. `git log --diff-filter=A 9beb0adea..d09d5bfde` to list newly added files.
   Result: 185,035 added files (mostly evidence, corpora, and generated source),
   of which 12,704 are `*.zag`.
2. Built the full added-file `*.zag` diff (`git diff 9beb0adea d09d5bfde
   --diff-filter=A -- '*.zag'`) and scanned every added line for interactive
   indicators: `chat`, `repl`, `stdin`, `readln`, `readline`, `argv`,
   `interactive`, plus raw fd-0 reads (`_zag_raw_syscall(0,0,...)`).
3. Checked adding commit and author for every hit.

## Commit range surveyed

`9beb0adea..d09d5bfde`, 45 commits, all authored by `micahcooley` on 2026-09-27.
No loop-authored commits in this range.

## New interactive entry points found

Three files contain stdin reads or argv-driven interactive modes. All are
Micah-authored.

### 1. wb3_nosynth.zag chat REPL

- Commit: `13c557cd3354928b335139a627a7e766e0669c62` (micahcooley, 2026-09-27,
  "exp2d pre-run: amendments, predictions lock, source, cleaned items, extended
  probes")
- File: `lab/composition/redo_2026-09-27/wb3_nosynth.zag`
- Mode: `argv[1]=="chat"` starts a persistent stdin/stdout conversation loop;
  history, salience, and session-taught facts live in process memory and
  evaporate on exit; answers print as `A <text>` lines.
- Status: **Micah's closed frontier.** Read-only awareness only. Not built, not
  run, not certified, not re-judged by the loop.

### 2. wb3_stringrule.zag chat REPL

- Commit: `13c557cd3354928b335139a627a7e766e0669c62` (micahcooley, 2026-09-27)
- File: `lab/composition/redo_2026-09-27/wb3_stringrule.zag`
- Mode: same `argv[1]=="chat"` persistent stdin/stdout REPL as wb3_nosynth, with
  the native string-rule engine answering first when it owns the turn.
- Status: **Micah's closed frontier.** Read-only awareness only.

### 3. d2.zag tui mode (game sim, not a chat)

- Commit: `597aa311f8e39b7ec39f2ec2abe9dc958c814a89` (micahcooley, 2026-09-27,
  "D2 action-sequence instrument: build, validation, K2-VOID battery")
- File: `lab/composition/d2/src/d2.zag`
- Mode: `d2 tui <scenario>` runs an interactive terminal UI over the TIDELOCK
  survival sim, reading one action digit (0-6) per tick from stdin via
  `read_line()`; `d2 run <scenario> <policy>` is the batch mode.
- Status: **Micah's commit.** Action-sequence instrument for a game sim, not a
  knowledge/architecture probe chat. Not loop-built.

## Explicitly not interactive entry points

- `lab/phase4/build/p4.zag`, `lab/phase4-style/build/sa.zag`: read a probe
  script path from `argv[1]` and emit ledger/result lines. Deterministic batch
  instruments, no stdin, no REPL.
- `lab/onebrain4/impl/onebrain_v4.zag`, `lab/onebrain5/reint-mechanism/impl/*`,
  `lab/onebrain5/v4-repair/impl/onebrain_v5.zag`: `argv[1]` selects batch
  ablation modes (single | onebrain | ablate | poison | min). No interactivity.
- `lab/senses/pam-rebuild/selfpam/r2/forkD/forkd2/src/main2.zag`: `argv[1]`
  mode switch for the evidence partition. Batch only.
- `docs/lab/growwithme/phase2/runs/*/chat_S*.txt`: run transcripts (data), not
  entry points.
- `lab/epistemics/GOALA_INDINGUISHABLE/raw/grok-probes/chat_long.py`: raw probe
  data in Micah's epistemics area. Not an entry point; untouched.

Zero additional stdin-read hits exist anywhere else in the added `*.zag` diff.
No new REPL loops, no interactive flags, no chat modes beyond the two Micah
chat REPLs above.

## Verdict

**NONE.** No loop-runnable interactive TNN exists on this branch for red-teamed
probe chats (knowledge vs architecture diagnosis) that the loop itself built,
ran, and certified. The only interactive chat REPLs added in this range are
Micah's own (`wb3_nosynth.zag`, `wb3_stringrule.zag`, commit `13c557cd3`), which
are his closed frontier and are not to be touched, built, run, certified, or
re-judged. The one other interactive mode (`d2.zag` `tui`) is a game-sim action
instrument, also Micah-authored, and is not a probe chat. The frozen probe
instruments remain the only loop-owned probe path, and they are batch-only.

The six governance rulings stay OPEN and are Micah's; nothing in this survey
relitigates them.
