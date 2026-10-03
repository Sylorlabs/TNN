# NAMECHECK: F-INT4 Level 1 Strengthening Worker

Date: 2026-09-30. Worker: F-INT4 Level 1 Strengthening.
Task: Strengthen the TNN-1 XCAP test to use the real MAP node from
`ev_query` instead of a synthetic guide node (per F-INT4 disposition
`86518edc4`, Level 1).

## Step 0: Toolchain guard verification

Command run: `which python3 python 2>/dev/null; echo "guard-check-done"`
Result: `/usr/bin/python3` present (unremovable system binary).
Disposition: documented non-use. Zero invocations during this wave.
All computation in Zag via the pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Shell used only for: invoking znc, running binaries, git operations,
file copies. No Python, C/C++, JavaScript, Rust, or other interpreters.

## Owned path

`docs/lab/research-lead/overnight-20260928/fint4_l1/` only.

## Constraints honored

- TNN-1 source inspected read-only; not modified. The Level 1 test is
  built from a copy in the owned directory.
- No em dashes in wave files (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff
  verified before and after commit.
- No sealed FW1-FW9 files accessed.
- Explicit pathspecs on commit.
