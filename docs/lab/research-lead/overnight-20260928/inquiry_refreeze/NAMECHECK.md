# NAMECHECK.md - Inquiry Re-freeze Worker (clean)

## Step 0: Toolchain Guard

- `which python3 python 2>/dev/null` in default PATH: `/usr/bin/python3` present (unremovable system binary).
- Restricted PATH: `$HOME/safebin` (35 tools symlinked: git, znc, shell coreutils only).
- In restricted PATH, `which python3 python` returns nothing. python3 is ABSENT.
- This is a CLEAN RE-FREEZE: zero tolerance. Any python3/python invocation at any point = PROCESS-FAIL.
- All implementation written via file tools; all computation via pure Zag compiled with pinned `znc_linux_x86_64_abed8aa1`.
- No em dashes in this file or any wave artifact (byte-greppable).

## Purpose

Re-freeze the learner-driven inquiry experiment (Pieces A + B) per frozen prereg
`docs/lab/research-lead/overnight-20260928/inquiry_prereg/PREREG_INQUIRY.md` (commit `04ac028fb`).

The prior wave (commit `396ecafa4`) passed all frozen bars but self-disclosed one
`python3` invocation on a /tmp scratch copy. Per the Worker Toolchain Guard that wave
is PROCESS-FAIL. This wave re-implements from scratch with zero Python.

## K1 ordering

- Prereg commit `04ac028fb` verified as ancestor of working HEAD before implementation
  (`git merge-base --is-ancestor 04ac028fb HEAD` = pass).
