# Step 0 name-check: L3A-TRACE clean rebuild (2026-09-30)

I read the four standing-rules sections at the top of LOOP_STATE.md:
the Standing owner rules (2026-09-23), the fork-testing rule, the
pure-Zag red line scope ruling (2026-09-23), and the shell-only byte
check rule (2026-09-30).

Rules that apply to this task and how I will honor them:

1. PURE ZAG ONLY (owner red line, literal scope). This rebuild exists
because the original L3A-TRACE builder incurred BUILD-FAIL for
authoring a python3 heredoc on a /tmp scratch copy during diagnostics.
I will not invoke python3 for any purpose in this wave: not for the
implementation, not for diagnostics, not for byte checks, not for
/tmp scratch, not for log comparison. Compilation uses the pinned znc
binary; log comparison uses cmp and sha256sum; dash checks use the
shell-only check_no_dash.sh snippet. I will affirmatively state the
zero-python3 result in the final report.

2. Shell-only byte checks (2026-09-30). Em/en dash checks run only via
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
No python3 byte checks: governance found 5 of the 6 newest K4 violations
were python3 byte checks, and disclosure does not cure use.

3. Fork testing and image-judge rules are background context and do not
directly operate on this clean rebuild; no image or fork work is in
scope.

4. Never weaken a frozen kill bar after results. The five bars (a)-(e),
the SEGMENT-MATCH guard [1,1,5], the beam/task configuration from
Amendments A1/A2, and the C0-A audit A1-A7 are frozen. If any bar fails
to reproduce I will report the exact measured numbers and a BUILD-FAIL
verdict, not a reinterpretation.

Name-check written before any implementation work. Proceeding to Step 1.
