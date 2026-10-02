# NAMECHECK.md - wave-20261001-2021pdt / F2v3 research worker

## Step 0: Toolchain guard (mandatory, before any other work)

Date: 2026-10-01 20:26 PDT (Thu)
Worker: research worker (depth 2/2), lane F2v3 (F2 v3 with X-rule distinguishability)

Actions taken:
1. Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   - Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   - znc pinned toolchain present: /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
   - Safebin verify reported: python3 absent from safebin PATH (OK), python absent (OK)
2. Exported PATH="$HOME/safebin" (safebin only, no other entries)
3. `which python3` -> nothing found (OK)
4. `which python` -> nothing found (OK)

Toolchain status: PURE-ZAG PATH active. python3 and python do not resolve.
No forbidden executable has been invoked. This record satisfies Step 0.

Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
Write scope for this phase: docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/ only.
No implementation files will be written before coordinator authorization
(UNVERIFIABLE ORDERING voids the prereg). No commits by this worker.

## Step 0b: Build-phase authorization and commit-order check (2026-10-01 20:33 PDT)

1. Coordinator authorization to implement received via the lane task
   (implement DPDS per frozen prereg, pure Zag, inside the lane dir).
   This is the build phase the prereg section 13 anticipates.
2. Commit-order self-check: prereg commit 13206c15b is an ancestor of
   HEAD (verified with `git merge-base --is-ancestor`), and zero commits
   have touched docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/ since
   13206c15b (verified with `git log 13206c15b..HEAD -- <lane>`).
   Implementation files written from this point are new untracked files,
   so they first appear strictly after the prereg commit. Ordering is
   verifiable; the prereg is not voided.
3. Toolchain re-verified at build start: PATH="$HOME/safebin",
   `which python3` and `which python` return nothing. No forbidden
   executable has been invoked. Pure Zag only from here on.
