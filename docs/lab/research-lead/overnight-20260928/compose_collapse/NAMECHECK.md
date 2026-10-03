# NAMECHECK.md -- Compose-Collapse Worker (H1+H2 consolidation)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

Verification, run 2026-10-02 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty)
- `which python` -> NOTHING (empty)
- `which git` -> /home/hatch/safebin/git
- safebin contains 49 symlinks (coreutils, git, znc via pinned binary path)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin.

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin setup, znc invocation, binary execution, git
operations, file assembly (cat), and byte verification (grep/cmp/sha256sum).

## Scope

- Read canonical consolidation (`composition_canonical/CONSOLIDATION.md`) and
  the H1 (`xdomain_typed`) / H2 (`xdomain_value`) preregs and reports.
- Freeze PREREG.md + this NAMECHECK.md Step 0 and commit them ALONE before any
  implementation (prereg commit-order self-check).
- Implement the discriminating battery (P1, P2a, P2b, P3, P5) in pure Zag:
  arms H1, H2, UNI (unified), UNI-NOKIND (one-line ablation).
- Run 3x per arm, byte-identical determinism, record sha256.
- Write REPORT.md with the consolidation verdict (subsumption / genuine
  distinction with boundary / undecided with decisive experiment).
- Commits LOCAL only, explicit pathspecs, never push, never git reset, never
  amend shared history. Branch: tnn-native-lab.

## Constraints observed

- No COMPOSE_MODE, no domain-pair handlers, no new finite-menu modes. The
  unified mechanism has one admission rule and one execution rule, always on;
  the widening is failure-triggered from learner-observed state.
- No em/en dashes in documentation (byte-verified before each commit).
- Never inspect sealed-world contents except via the authorized evaluator
  (no sealed worlds are used in this battery; all worlds are frozen in the
  prereg above).
- Other workers' files untouched. If the shared checkout is lock-contested,
  fall back to a sparse worktree under ~/workspace (not needed so far).
