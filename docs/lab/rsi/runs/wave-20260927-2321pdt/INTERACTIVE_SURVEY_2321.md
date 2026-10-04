# Interactive Survey 2321 PDT (wave-20260927-2321pdt)

Re-survey of the merge range `fc1a43b8c..baf48e474` for new
chat/REPL/stdin interactive entry points in source.

## Method

1. Resolved the range topology: 11 commits in the range
   (`git rev-list --count fc1a43b8c..baf48e474` = 11), all
   first-parent wave records, all authored by `tnn-rsi-loop`
   (the loop's own 2021pdt records: HUNT_2021 + INTERACTIVE_SURVEY_2021,
   tnn_chat FIT re-run, fork battery, EXP1c milestones 2-4, debate
   transcript, judge rulings, LOOP_STATE verdicts). Zero origin /
   Micah-authored commits in this range.
2. Listed all 1,208 files added in the range (222 of them `*.zag`,
   mostly fork-battery evidence archives plus EXP1c batch sources
   and the fork battery harness); built the added-file `*.zag`
   diff (`git diff fc1a43b8c..baf48e474 --diff-filter=A -U0 --
   '*.zag'`, 4,149 lines) and scanned every added line for
   interactive indicators: `chat`, `repl`, `stdin`, `readln`,
   `readline`, `argv`, `interactive`, `tui`, plus raw fd-0 reads
   (`_zag_raw_syscall(0,0,...)`, `read_line`).
3. Separately grepped every working-tree copy of the 222 added
   `.zag` files for fd-0 read patterns; separately scanned the
   full added diff (all 986 non-`.zag` files) for the keyword set.

## Hit list

Zero genuine interactive hits. Every keyword match is a false
positive, enumerated:

- `repl`: only matches are the `n_replans` field and its diag
  header (`enum_tick` line) inside fork-battery evidence `.zag`
  files (batch instruments, tnn-rsi-loop authored). No `repl`
  mode anywhere.
- `argv`: only matches are the execve spawn helper in
  `docs/lab/rsi/runs/wave-20260927-2021pdt/forks/fork_battery.zag`
  (`927b3f3f7`..`dbe397973`, tnn-rsi-loop), which builds the
  argument vector for batch subprocess spawns (`sc(59,...)`,
  execve). Not an interactive input path.
- `tui`: zero matches in new sources.
- `chat`, `stdin`, `readln`, `readline`, `interactive`: zero
  matches in new sources (the only occurrences in the full diff
  are the 2021pdt INTERACTIVE_SURVEY_2021.md doc itself,
  describing the previously found Micah REPLs).
- fd-0 reads (`_zag_raw_syscall(0,0`, `read_line`): zero in all
  222 added `.zag` files.

## Classification of the new sources

- 9 EXP1c sources (`.../2021pdt/exp1c/src/*.zag`): batch
  survival-sim sources, zero interactive indicators.
- `fork_battery.zag` + `run_one.sh` + fork evidence archives:
  loop-owned batch battery instruments. The `run_one.sh` runner
  spawns binaries with canned args; no stdin chat mode.
- Frozen batch probe instruments (`fit_authority/tnn_chat.zag`,
  `tnn_chat_decline.zag`) unchanged since b650ea46f; not in this
  range, still batch-only, still the only loop-owned chat entry
  points on the branch.

## Verdict

**NONE.** No new loop-runnable interactive TNN entry points in
`fc1a43b8c..baf48e474`. No new Micah chat REPLs either (zero
Micah commits in the range). The previously surveyed entries
(h1/h2/h3 chat REPLs at 9dbd01e26, 7979a55b1, 7f5a8ccdb;
wb3_nosynth/wb3_stringrule chat REPLs at 13c557cd3; d2bin tui at
597aa311f) remain Micah's closed frontier: read-only awareness
only, never built, run, certified, or re-judged by the loop.
No loop-owned interactive exists on this branch beyond the frozen
batch probe instruments (batch-only).

No build, run, certify, or judge action was taken on any
interactive entry point during this survey. No Python used.
