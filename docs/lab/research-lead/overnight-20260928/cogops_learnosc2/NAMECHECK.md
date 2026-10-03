# NAMECHECK.md -- COGOPS-LEARNOSC2 Worker (outcome-record ablation)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work.

The lane convention (`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`)
does not exist in this checkout (same as the parent worker's
finding). The pre-existing `$HOME/safebin` was verified directly
instead, which satisfies the substance of the guard (no forbidden
interpreter reachable, pinned znc used for all builds).

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `ls $HOME/safebin | wc -l` -> 49; python3/python absent

Result: PASS. No python3/python reachable in PATH. All subsequent
commands in this task run with PATH=$HOME/safebin (exported in every
shell invocation). Git write operations use /usr/bin/git by absolute
path (the safebin git symlink has the known EPERM-on-write defect;
see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned compiler as the parent cogops-learnosc battery;
`znc 2026.07.0-dev`).

This PREREG.md + NAMECHECK.md (with this Step 0 confirmation) are
committed alone before any implementation file exists; the prereg is
adopted as frozen without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden
executable during this task. All scientific computation is pure Zag
(znc-compiled binaries). Shell is used only for: safebin PATH
export, znc invocation, binary execution, git operations, file
assembly (cat/cp/cmp), and byte verification
(cmp/sha256sum/grep).

## Scope

Outcome-record ablation for COGOPS-LEARNOSC: a single-word lesion
of the learner's outcome record (OUTC entry count at L+14500),
then re-presentation of goal 818. Tests whether the reuse
advantage (S9: 2 passes, how=2) is causally downstream of the
outcome record (predicted: full invention path, how=1, passes=4,
src=0, S3-identical cycle). Claim scope is L2 plus lesion
evidence; L3 representational invention and learner-invented
detection are explicitly not claimed (see PREREG Section 2.5).

## Pre-implementation checklist

- [x] PREREG.md frozen with exact predicted stdout (Section 7:
      S1A..S9 prefix byte-copied from the parent's frozen
      c7_run1.txt, mechanically verified; S10+SUMMARY hand-traced)
- [x] Kill bars K1..K9 frozen; verdict rule stated; falsification
      conditions stated (Section 2.3)
- [x] Honest boundary stated (necessity not sufficiency; no L3;
      no detection-invention claim; lesion is harness-side)
- [x] Step 0 toolchain guard recorded above
- [x] PREREG.md + NAMECHECK.md committed alone (this commit)
