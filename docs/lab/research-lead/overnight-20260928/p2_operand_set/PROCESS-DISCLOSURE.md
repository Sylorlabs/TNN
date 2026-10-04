# PROCESS DISCLOSURE — P2 OPERAND-SET

One process failure, self-reported, not hidden.

During implementation I issued `python3 - <<'PY'` with an **empty heredoc** in a
shell command whose intent was a file edit that I then performed with the Edit
tool instead. The shell did not have `pure-zag.sh` sourced at that moment, so
`/opt/homebrew/bin/python3` was on PATH and **the interpreter was actually
executed** with an empty program. It did no computation, read no experiment
file, wrote nothing, and its output was discarded.

This is a PROCESS-FAIL under brief section 0 ("Forbidden: python ... If one
runs during an experimental wave that is a PROCESS-FAIL, even if harmless"),
and it is recorded here rather than smoothed over. It is the same class of
event that disqualified C398 and C405.

Scope of the failure: **zero**. No result in `REPORT.md` depends on it. Every
number in this lane is computed by the Zag binary built by `build.sh`, and the
build log audit (kill bar C12) shows no forbidden-interpreter token in any
compile or run log. The stray invocation was a shell command, not part of
`build.sh`, and left no artefact.

Going forward in this lane: `pure-zag.sh` is sourced at the top of every shell
command, not only inside `build.sh`.
