# DEVINT-CLA2 Red Team: NAMECHECK.md

## Step 0: Toolchain Guard

- Ran: `which python3 python 2>/dev/null`
- Result: `/usr/bin/python3` present (system binary, not removable; non-use documented).
- This wave: analysis and adversarial audit. Any computational work will use Zag
  via the pinned compiler; shell only for znc, running binaries, git, file ops.
- Zero forbidden executables invoked.
