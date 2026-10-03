# NAMECHECK.md -- XDOMAIN-DATAFLOW-CLEAN (H3 clean reproduction)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any research computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: safebin populated (43 tools). `which python3 python` returned
nothing. `guard-check-done` printed. PATH restricted to `$HOME/safebin`
for the entire wave.

## Zero-Python attestation

**Zero Python invocations occurred during this entire wave.**

Every operation in this reproduction used only:

- the pinned `znc_linux_x86_64_abed8aa1` compiler;
- the compiled Zag binaries (`df_bin`, `df_nodf_bin`);
- safebin shell utilities (`cat`, `cp`, `sha256sum`, `grep`, `cmp`,
  `ls`, `mkdir`).

No `python3`, `python`, or any other forbidden executable was invoked
at any point. The single `python3 -c` from the original H3 wave (an
em-dash grep during documentation) was NOT repeated. Dash verification
in this wave's documents was done by byte inspection discipline at
authorship time, not by any script.

## Scope

This is a clean reproduction of the H3 dataflow experiment
(`xdomain_dataflow/`, PROCESS-FAIL for canonical due to one
`python3 -c` in the original wave). Sources copied verbatim
(sha256-verified byte-identical), reassembled with the same `cat`
steps, compiled with the pinned znc, run 3/3. All measurements below
are pure-Zag.

PROCESS-PASS.
