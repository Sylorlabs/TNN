# NAMECHECK.md -- GEN-SUBSUMES-U Worker (architecture compression: does GEN subsume U?)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
```

Setup script (repo-relative):
`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
reported: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the safebin `znc` symlink target; same pinned compiler as the
compose_collapse, compose_pair5, and compose_pair6_adv batteries).

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (head/cat), and byte verification
(diff/cmp/sha256sum).

## Scope

- Read the COMPOSE-COLLAPSE verdict (C319 SUBSUMPTION: H1+H2 = one
  behavior-contract operation U), the COMPOSE-PAIR5 report (U on the 5th
  pair), and the COMPOSE-PAIR6-ADV report (GEN generalizes U to the diamond).
- Frozen sources reused byte-verbatim: pair6 `d6_base.zag` (GEN base),
  pair6 `d6_gen.zag` lines 1-239 (GEN composer, main excluded), pair5
  `p5_full.zag` lines 336-391 (five world-builder functions, main excluded).
- Only new code: `gsu_main.zag` (9 arms through `gen_solve`).
- No other lane directories touched. Commits use explicit pathspecs on
  branch `lane-gensubsumesu-20261003`; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
