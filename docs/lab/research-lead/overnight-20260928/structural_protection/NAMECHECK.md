# NAMECHECK: Structural Protection Builder

## Step 0: Toolchain guard (mandatory)

Executed at worker start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Guard check done.
Safebin active at $HOME/safebin. No python3, no python in PATH.

## Scope

UNFROZEN VARIANT ONLY. Frozen source is read-only reference.
Builds learner-owned structural protection for graph cells on top of the
interference-experiment variant (commit 3708fbd15), which is itself an
unfrozen variant with cognition byte-identical to frozen f4de7ff46.

## Mission

Build a protection mechanism: when a MAP is referenced (promoted,
queried, revised), mark its graph cells as structurally important using
existing architecture (PRO edges, type 9; existing decay/is_prot
machinery). No new node types, no new edge types, no new fields, no new
modes, no new bridges, no new handlers.

Test treatment vs control on the interference battery
(V in {0,1000,1050,1100}, IX-1 no refresh, IX-2 refresh every 10).

## Forbidden executable check

Zero invocations of python3/python in this wave. Shell used only for:
znc invocation, running compiled binaries, git operations, file copies.
Pure Zag for all research computation.

## Input provenance

- Base cognition: docs/lab/research-lead/overnight-20260928/interference_experiment/tnn2_interference_variant.zag (commit 3708fbd15)
- Battery driver: docs/lab/research-lead/overnight-20260928/interference_experiment/interference_probes.zag (commit 3708fbd15)
- Control numbers: INTERFERENCE_EXPERIMENT.md from the same commit (3 byte-identical runs)
- Compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1 (pinned)

## Constraints honored

Unfrozen variant only. Frozen source untouched. Pure Zag via pinned znc.
Zero em/en dashes in all docs. Research paper untouched. No sealed
worlds. Nothing pushed (local commits only).
