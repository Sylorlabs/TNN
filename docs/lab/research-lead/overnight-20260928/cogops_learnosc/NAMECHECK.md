# NAMECHECK.md -- COGOPS-LEARNOSC Worker (follow-up to COGOPS-PERIOD C459)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work.

The lane convention (`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`)
does not exist in this checkout (verified: find over
`~/workspace/tnn-rsi/docs` returns nothing). The pre-existing
`$HOME/safebin` was verified directly instead, which satisfies the
substance of the guard (no forbidden interpreter reachable,
pinned znc used for all builds).

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc
- `~/safebin` holds 49 entries; python3/python absent

Result: PASS. No python3/python reachable in PATH. All subsequent
commands in this task run with PATH=$HOME/safebin (exported in every
shell invocation). Git write operations use /usr/bin/git by absolute
path (the safebin git symlink has the known EPERM-on-write defect;
see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned compiler as the cogops_cycles and
cogops_oscillatory batteries; `znc 2026.07.0-dev`).

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

Learner-invented oscillation handling from the L outcome record:
the learner constructs a per-goal cycle response from its own
trajectory (invention), the response works on new oscillatory
goals (transfer: new relation/phases, period-3), no false
positive on the convergent control, and the outcome record
causally drives faster handling on re-presentation (reuse).
Claim scope is L2 structural learning; L3 representational
invention is explicitly not claimed (see PREREG Section 2.3).

## Pre-implementation checklist

- [x] PREREG.md frozen with exact predicted stdout (Section 7)
- [x] Kill bars K1..K9 frozen; verdict rule stated
- [x] Honest boundary stated (generic machinery vs
      learner-created; no L3 claim; C459 detector distinguished)
- [x] Step 0 toolchain guard recorded above
- [x] PREREG.md + NAMECHECK.md committed alone (this commit)
