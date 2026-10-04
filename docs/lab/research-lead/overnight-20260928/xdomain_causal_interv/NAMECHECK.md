# NAMECHECK: xdomain_causal_interv worker

## Step 0: Toolchain guard (mandatory)

Executed at worker startup:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. `guard-check-done` printed.
Safebin PATH active for all subsequent work.

Recorded: 2026-10-02, worker start.

## Toolchain verification

- `which python3` -> empty
- `which python` -> empty
- Pinned compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- All research computation in Zag via znc. Shell only for: invoking znc,
  running binaries, git operations, moving/copying files.

## Standing attestation

No forbidden executable (python3, python, or other interpreters) was
invoked during this wave. If one had been, this wave would be PROCESS-FAIL
per Micah's mandatory toolchain guard.
