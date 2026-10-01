# NAMECHECK: DYN-1 Discount Cost Measurement

## Step 0: Toolchain Guard

Executed at task start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with empty `which` output. `python3` and
`python` do not resolve in the safebin PATH. Zero forbidden executables
invoked during this task. All computation via the pinned znc
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`). Shell used only to
invoke znc, run the compiled binary, and do git/file operations.

## Scope

MEASUREMENT ONLY. Unfrozen variant. No implementation, no design changes,
no source modifications beyond the pre-existing discount pilot splice
(from `0daaa2ed4`, used verbatim).

## Input Provenance

- Discount cognition: `discount_impl/di_variant.zag` (verbatim copy,
  from commit `0daaa2ed4`; contains the D1+D2+W3+R1 pilot splice of
  `bootstrap_miss`, no test main).
- Measurement driver: `dyn1/dyn1_driver.zag` (verbatim copy, from
  commit `003767553`; the DYN-1 250-event sequence driver).
- Method follows `dyn1_node1/DYN1_NODE1.md` (commit `67b700d3f`):
  variant cognition plus verbatim driver appended, compiled with
  pinned znc, 3/3 byte-identical runs.
- Frozen baseline for comparison: `dyn1/DYN1.md` (commit `003767553`).

## Constraints Honored

- Unfrozen variant only. Frozen source read-only (never opened for
  editing; `di_variant.zag` is the pre-built pilot cognition).
- Pure Zag via pinned znc. Safebin active throughout.
- Zero em dashes and zero en dashes in deliverables (byte-verified).
- Research paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  not opened).
- No sealed worlds opened or created.
- Nothing pushed. Local commit only, explicit pathspecs on both
  `git add` and `git commit`.
