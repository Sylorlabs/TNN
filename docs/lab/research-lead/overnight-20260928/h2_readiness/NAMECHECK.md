# NAMECHECK.md - H2 Readiness Checker

## Step 0: Toolchain Guard

Date: 2026-09-30 (PDT). Worker: H2 Readiness Checker (subagent, depth 1/2).

Commands run at startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed nothing; only `guard-check-done` appeared.
No `python3`/`python` resolves in PATH. Toolchain status: PASS.

## Scope

CHECK ONLY. Verify H2 masked-probe readiness: probe design, sealed trap
worlds, seal integrity, kill-bar freeze status. No probe was run. No source
was modified. No binary was built.

## Source material consulted (read-only)

- `docs/lab/research-lead/overnight-20260928/tnn2_h2probes/H2_PROBE_DESIGN.md`
  (commit `4631c5918`)
- `docs/lab/research-lead/overnight-20260928/h2_trapworlds/` including
  `SEAL_H2.md` (commit `86389b108`)
- Commit `36e5a70e1` (gap bars draft: K-H2 text)
- Frozen TNN-2 build `f4de7ff46`; binary
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin` (presence
  confirmed, not executed)

## Deliverables

- `H2_READINESS.md`: the readiness checklist (this directory).
- This file (NAMECHECK.md).

Commit: explicit pathspecs only, under
`docs/lab/research-lead/overnight-20260928/h2_readiness/`.

## Constraints honored

- Owned path only: all writes inside `h2_readiness/`.
- Sealed trap world file CONTENTS were not opened; only SHA-256 hashes were
  recomputed and compared against `SEAL_H2.md` (hash check is authorized).
- No sealed FW/GW contents inspected.
- Research paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- No em dashes in documentation.
