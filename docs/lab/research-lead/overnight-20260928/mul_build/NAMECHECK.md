# MUL Builder NAMECHECK

## Step 0: Toolchain guard (executed before any work)

- `which python3 python` under default PATH: `/usr/bin/python3` present
  (unremovable system binary; documented non-use, never invoked).
- Restricted safebin built at `~/workspace/mul_safebin` with symlinks to
  coreutils/git/grep/sha256sum only (python/python3 excluded).
- Under safebin PATH: `python3` = ABSENT, `python` = ABSENT.
- All computational research work in this wave: pure Zag (pinned znc).
- Shell usage restricted to: invoking znc, running binaries, git ops,
  file moves/copies, byte-level grep checks.
- Zero forbidden interpreter invocations in this wave.

## Wave metadata

- Role: MUL Builder (MUL-1 learner construction experiment).
- Frozen prereg: `docs/lab/research-lead/overnight-20260928/mul_prereg/PREREG_MUL1.md`
  at commit `222899314`.
- ISA boundary: `docs/lab/research-lead/overnight-20260928/architecture_rulings/ISA_BOUNDARY_RULING.md`
  at commit `0525377f3`.
- K1 check: prereg commit `222899314` verified as ancestor of HEAD
  before implementation (see below).

## Owned path

- `docs/lab/research-lead/overnight-20260928/mul_build/`

## K1 verification (before implementation)

- `git merge-base --is-ancestor 222899314 HEAD` → K1-PREREG-OK
- `git merge-base --is-ancestor 0525377f3 HEAD` → K1-ISA-OK
- HEAD at build start: `170e39424`
