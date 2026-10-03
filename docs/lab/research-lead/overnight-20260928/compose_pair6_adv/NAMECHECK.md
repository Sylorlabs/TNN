# NAMECHECK.md -- Compose Pair-6-ADV Worker (diamond/fan-out vs unified operation U)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
```

Setup script (repo-relative):
`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
reported: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.

Verification, run 2026-10-02 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
sha256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(identical hash for the safebin `znc`; same pinned compiler as the
compose_collapse and compose_pair5 batteries).

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (cat), and byte verification
(diff/head/cmp/sha256sum).

## Scope

- Read the COMPOSE-COLLAPSE verdict (C319 SUBSUMPTION: H1+H2 = one
  behavior-contract operation U) and its frozen sources (uc_base.zag,
  uc_uni.zag), and the COMPOSE-PAIR5 transfer result (C368 BUILD-PASS).
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before
  any implementation (prereg commit-order self-check).
- Design and freeze a diamond/fan-out composition test (Q1/Q2): one MAP's
  output feeding TWO downstream MAPs with a 2-input join, on the unmodified
  unified operation (Arm UNI-D) and on the candidate general extension GEN
  (Arm GEN), plus GEN regression on the collapse battery P1/P2a/P2b/P3.
- Base change allowlist (PREREG Sec 7): exactly one new generic 2-input
  arithmetic class (ADD2, class 4) with 1-input arity-mismatch -> -2,
  exec_map2/observe2/teach2, second-input contract table, and the two
  diamond world setups. U's composer functions byte-identical to the frozen
  reference (verified by diff, PREREG K6).
- Run 3x per binary, byte-identical determinism, record sha256.
- Write REPORT.md with the verdict per the frozen Section 8 mapping:
  INFORMATIVE-FAIL (U) is the primary deliverable; GENERAL-EXTENSION-EXISTS
  iff K3+K4+K5 pass.
- Commits LOCAL only, explicit pathspecs, never push, never git reset, never
  amend shared history. Isolated worktree ~/workspace/tnn-rsi-pair6, branch
  lane-composepair6-20261002 (from tnn-native-lab).

## Constraints observed

- No COMPOSE_MODE, no domain-pair handlers, no new finite-menu modes, no
  diamond-specific code in GEN (the fork emerges from the value-pool rule).
- One generic 2-input arithmetic class only (PREREG boundary B1); zero
  relation-conditional branches; zero new 1-input behavior classes.
- No em/en dashes in documentation (byte-verified before each commit).
- Other workers' files untouched; isolated worktree used throughout.
- Never weaken frozen kill bars; verdict follows the frozen mapping.
