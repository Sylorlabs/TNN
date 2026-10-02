# NAMECHECK F3B (worker toolchain guard, Step 0)

Wave: wave-20260930-1121pdt. Worker: F3B (interface-extension lane).

Step 0 toolchain check: `which python3` returns /usr/bin/python3.
Present in PATH; not removed (system interpreter; removal would be
destructive and out of scope for this worker). Documented instead:
python3 was never invoked during this wave. All computational research
operations are pure Zag (f3b_len.zag, compiled with the repo Linux znc
binary). Shell used only for orchestration: invoking znc, running the
compiled binary, git operations, moving/copying files, and byte-level
audits (grep, diff, cmp). No Python in decision paths, harnesses,
analysis, or verifiers. Dash-check script is shell-only.

Result: toolchain guard SATISFIED by documentation (no invocation).
