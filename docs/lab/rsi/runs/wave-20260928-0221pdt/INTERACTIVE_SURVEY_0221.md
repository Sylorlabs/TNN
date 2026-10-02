# Interactive Survey 0221 PDT (wave-20260928-0221pdt)

Task: INTERACTIVE SURVEY worker. Check the merge range for new
chat/REPL/interactive entry points since the last survey.
Read-only survey; Micah's frontier dirs untouched; no builds, no runs.

## Merge range

- Range: `baf48e474..43f339e60` (previous wave start HEAD to this wave's run-start HEAD)
- Commits in range: 9, all tnn-rsi-loop wave records, zero Micah commits
  - `43f339e60` LOOP_STATE verdicts (EXP1c VOID/K7, C3 gloss struck; survey NONE)
  - `d5d5dd58d` debate transcript plus design-lane judge amendment
  - `3636d2fe4` EXP1c independent red-team review
  - `0563e0cce` EXP1c Zag-generated evidence note
  - `26669a08d` EXP1c full experiment and deterministic rerun
  - `7fbd485b6` EXP1c retune iteration 3 variants and calibration
  - `9926b0860` fork battery results (56 entries, 54 PASS, 0 FAIL, 2 UNTESTABLE)
  - `3dc45ca35` design lane HUNT_2321
  - `9c6646c04` interactive re-survey fc1a43b8c..baf48e474, verdict NONE

## Files swept

- Added files in range: 1,224
- Text files swept: 736 (remainder are binaries: probe_bin, hello_bin, neg*_bin, ocean/bin artifacts, etc.)
- Added `.zag` files: 226, separately scanned for fd-0 stdin patterns
- Modified files in range: 1 (`LOOP_STATE.md`); deleted: 0; renamed: 0

## Keyword method

Case-insensitive grep over all 736 text files for:
`chat`, `repl`, `interactive`, `tui`, `fd-0`, `fd0`, `readline`,
`read_line`, `readln`, `stdin`, `console`.
All 226 added `.zag` files additionally scanned for
`read_line`, `readln`, `readline`, `_zag_raw_syscall(0`,
`syscall(0`, `fd-0`, `fd0`, `getchar`, `prompt`,
`repl_loop`, `console`, `argv` in an input context.

Initial run with a trailing `|` regex bug matched all files; corrected
run (no empty alternative) produced 14 keyword hits across 14 files,
plus zero stdin/fd-0 hits in all 226 `.zag` files.

## Per-hit classification

Every one of the 14 keyword hits is a false positive. No hit is an
entry point of any kind.

False positive, self-reference to this task's own instrument
(`INTERACTIVE_SURVEY_2321.md`, commit `9c6646c04`):
- `docs/lab/rsi/runs/wave-20260927-2321pdt/INTERACTIVE_SURVEY_2321.md`
  (the prior survey doc itself; hit source, lines 1-74; describes the
  prior range's method and verdict, including the standing frozen batch
  probe note and the Micah REPL note)

False positive, debate records referencing the prior survey and the
`n_replans` diagnostic field (substring of `replans`, not `repl`):
- `docs/lab/rsi/runs/wave-20260927-2321pdt/debate/ADVOCATE_2321.md`
  (lines 9, 220-238, 272, 295: M4 confirm-NONE discussion; `repl`
  matches are `n_replans`)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/debate/JUDGE_2321.md`
  (lines 9, 81, 91-92, 200, 244, 293-297: M4 CONFIRM ruling;
  `repl` is `n_replans`; `chat` is the `tnn_chat` FIT staleness note)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/debate/SKEPTIC_2321.md`
  (lines 9, 214, 272, 285, 349-355: attack on M4; `repl` is
  `n_replans`; `chat` is `tnn_chat` FIT staleness)

False positive, design lane referencing the survey commit:
- `docs/lab/rsi/runs/wave-20260927-2321pdt/design_lane/HUNT_2321.md`
  (lines 11-20: cites INTERACTIVE_SURVEY_2321, verdict NONE;
  `chat` is `tnn_chat` FIT)

False positive, EXP1c evidence (`n_replans` / `replans` diagnostic
field in the batch evidence generator output):
- `docs/lab/rsi/runs/wave-20260927-2321pdt/exp1c/REDTEAM_EXP1C_2321.md`
  (line 130: `replans=423`)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/exp1c/evidence/EVIDENCE_EXP1C.md`
  (lines 34-82: `n_replans` header plus 48 per-arm rows)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/exp1c/iterations/iter3/ITER3.md`
  (line 14: `n_distinct, replans` in the reporting contract)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/exp1c/src/x1c_agents.zag`
  (lines 293, 308, 479: `n_replans:i32` struct field, batch only)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/exp1c/src/x1c_evidence.zag`
  (lines 110, 138, 411, 422: `n_replans` arena slot and IDIAG label,
  batch evidence writer)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/exp1c/src/x1c_run.zag`
  (line 84: `dr = xst.n_replans`, batch runner)

False positive, fork battery records and harness:
- `docs/lab/rsi/runs/wave-20260927-2321pdt/forks/ENUMERATION_MANIFEST.md`
  (line 156: cites the interactive re-survey commit `9c6646c04`)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/forks/FORK_RESULTS_2321.md`
  (lines 352-353: cites the survey commit; line 436: `tnn_chat`
  FIT note header)
- `docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag`
  (lines 166-214: `argv` vector built for `sc(59,...)` execve of
  canned-argument binaries; a spawn helper, not an interactive
  input path)

False positive, self-reference in the sole modified file:
- `LOOP_STATE.md` (added line: "4. Interactive survey [NEW]: NONE
  loop-owned..." records this wave's prior-survey verdict verbatim;
  no new entry point)

## Verdict

**NONE.** No new chat/REPL/stdin/tui interactive entry points in
`baf48e474..43f339e60`, from any source, loop-owned or Micah's.
All 14 keyword hits are false positives (diagnostics, comments,
self-references to the prior survey). All 226 added `.zag` files
have zero stdin/fd-0/readline interactive indicators. The only
modified file (`LOOP_STATE.md`) adds only prose about the prior
survey's NONE verdict.

The frozen batch probes (`fit_authority/tnn_chat.zag`,
`tnn_chat_decline.zag`) are unchanged and remain the only
loop-owned chat entry points, batch-only.

## Standing note

Micah's closed-frontier REPLs (h1/h2/h3 at `9dbd01e26`,
`7979a55b1`, `7f5a8ccdb`; wb3 chat modes and d2bin tui from the
prior survey) were not touched by this survey: they are outside
this merge range, were surveyed read-only, remain untouched, and
were never re-judged. Nothing in this range alters their status.

No Python used in this survey. Survey scope was read-only except
this report file.
