# NAMECHECK.md -- COGOPS-DETECTION Worker

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work.

The lane convention
(`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`)
does not exist in this checkout (same finding as the
COGOPS-LEARNOSC and COGOPS-LEARNOSC2 workers). The
pre-existing `$HOME/safebin` was verified directly instead,
which satisfies the substance of the guard (no forbidden
interpreter reachable, pinned znc used for all builds).

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc
- `~/safebin` holds 49 entries; python3/python absent

Result: PASS. No python3/python reachable in PATH. All
subsequent commands in this task run with
PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path
(the safebin git symlink has the known EPERM-on-write
defect; see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev`; same pinned compiler as the
cogops_learnosc / cogops_learnosc2 batteries).

This PREREG.md + NAMECHECK.md (with this Step 0
confirmation) are committed alone before any
implementation file exists; the prereg is adopted as
frozen without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other
forbidden executable during this task. All scientific
computation is pure Zag (znc-compiled binaries). Shell is
used only for: safebin PATH export, znc invocation,
binary execution, git operations, file assembly
(cat/cp/cmp), and byte verification
(cmp/sha256sum/grep).

## Scope

Learner-invented oscillation DETECTION: the learner
assembles a detection procedure from the generic
pairwise snapshot-comparison primitive
(`traj_state_eq`), driven by an experience-shaped lag
prior in learner state. The researcher-provided
recurrence scan (`osc_review`) is present in the binary
via the frozen prefix but provably uncalled (K8).
Claim scope is L2 structural learning; L3
representational invention is explicitly not claimed
(see PREREG Section 2.3).

## Pre-implementation checklist

- [x] PREREG.md frozen with exact predicted stdout
      (Section 7)
- [x] Kill bars K1..K11 frozen; verdict rule stated
- [x] Honest boundary stated (generic machinery vs
      learner-created; no L3 claim; the red-team
      "rewritten scan" attack pre-answered four ways)
- [x] Step 0 toolchain guard recorded above
- [x] PREREG.md + NAMECHECK.md committed alone (this commit)
