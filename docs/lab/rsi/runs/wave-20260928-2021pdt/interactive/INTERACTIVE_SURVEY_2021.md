# Interactive Survey 2021 PDT (wave-20260928-2021pdt)

Task: INTERACTIVE SURVEY. Check the merge range for new
chat/REPL/interactive entry points since the last survey.
Read-only survey; Micah's frontier dirs untouched; no builds, no runs.

## Merge range

- Range: `4340126e6..4340126e6` (1721pdt wave LOOP_STATE commit to this
  wave's run-start HEAD). The run-start pin equals the 1721pdt tip
  exactly, so the range is empty.
- Commits in range: 0. `git rev-list --count 4340126e6..HEAD` is 0.
- The 1721pdt wave surveyed `81f0cfe12..547b2132c` and found NONE;
  this wave's range adds zero commits on top of that surveyed state.

## Files swept

- Added files in range: 0.
- Added files outside prior records: 0 (this wave's own lane files are
  untracked working-tree files, written by this wave, not evidence of
  anything new in the branch history).
- Added `.zag` files in range: 0.
- docs/lab/invention/ files changed in range: 0.

## Verdict

**NONE loop-owned.** No new runnable chat/REPL/stdin-loop TNN entry
point appears anywhere; the range is empty. The frozen batch probes
(docs/lab/rsi/fit_authority/tnn_chat.zag, tnn_chat_decline.zag) remain
the only loop-owned chat instruments, batch-only. Micah's closed-frontier
REPLs were surveyed read-only at earlier waves and remain untouched.

tnn_chat FIT staleness: 4 of 8, kept visible, not due this wave. Zero
commits in range are docs-only by construction (the range is empty), so
no regression path exists for the FIT to miss.
