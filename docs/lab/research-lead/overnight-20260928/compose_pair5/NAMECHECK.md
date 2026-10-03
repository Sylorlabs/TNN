# NAMECHECK.md -- Compose Pair-5 Worker (5th domain pair transfer test)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
```

Verification, run 2026-10-02 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty)
- `which python` -> NOTHING (empty)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin.

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(also reachable as `znc` via safebin; same pinned binary family as the
compose_collapse battery).

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (cat/sed), and byte verification
(grep/cmp/sha256sum).

## Scope

- Read the COMPOSE-COLLAPSE verdict (SUBSUMPTION: H1+H2 = one behavior-contract
  operation U) and its frozen sources (uc_base.zag, uc_uni.zag).
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before any
  implementation (prereg commit-order self-check).
- Test U on a 5th cross-domain pair NOT in the original 4
  (navigation x aggregation, arithmetic x planning, causal x intervention,
  grammar x construction): spatial-layout x task-scheduling.
- Composition logic (uc_uni.zag functions) and base machinery (uc_base.zag)
  are copied BYTE-IDENTICAL; only a new world setup + main are added.
  K3 is verified by extraction + diff, not by inspection.
- Run 3x, byte-identical determinism, record sha256.
- Write REPORT.md with BUILD-PASS/FAIL and the transfer answer.
- Commits LOCAL only, explicit pathspecs, never push, never git reset, never
  amend shared history. Worktree: ~/workspace/tnn-rsi-pair5, branch
  lane-composepair5-20261002 (from tnn-native-lab).

## Constraints observed

- No COMPOSE_MODE, no domain-pair handlers, no new finite-menu modes, no new
  behavior classes, no new opcodes. The only new code is integer fact data
  (fact_add), MAP inventory (map_new), teaching calls (teach), and main.
- No em/en dashes in documentation (byte-verified before each commit).
- Other workers' files untouched; isolated worktree used throughout.
