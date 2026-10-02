# NAMECHECK: Verification Transfer Worker

Worker: Verification Transfer Worker (subagent, 2026-10-02).
Scope: `docs/lab/research-lead/overnight-20260928/verify_transfer/`
only. The frozen sibling directory `l3_delayed_stochastic/` is
read-only; its `learner_ds.zag` is copied byte-identical, never
modified.
Prereg: `PREREG.md` (frozen, committed alone before any implementation
existed; zero amendments).

## Step 0: Toolchain guard (mandatory, recorded before any work)

Ran at worker startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` printed nothing; `guard-check-done`
confirmed. No python3/python in PATH for the whole task. All
computational work (including the pre-prereg independent checker in
/tmp/vtcheck.zag and the awk attribution audit, which is a log check,
not research logic) done with safebin tools and pure Zag via the
pinned znc. No forbidden executable invoked: no PROCESS-FAIL.

## Build record

(TBD at implementation; this section is filled when the implementation
commit lands.)

## Commit record

(TBD; prereg commit first, alone, with explicit pathspecs.)
