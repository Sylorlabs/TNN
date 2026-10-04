# NAMECHECK.md -- Invention Hypothesis 2 Worker (Fragment Recombination)

## Step 0: Toolchain guard (mandatory)

Executed at startup (2026-10-01, before any research command):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed nothing; `guard-check-done` printed.
`PATH=/home/hatch/safebin` for all subsequent commands.
Zero forbidden executables invoked. Pure Zag for all computation.
Pinned compiler for builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## Step 1: Identity

Worker: Invention Hypothesis 2 (fragment recombination).
Hypothesis: TNN holds MAP fragments (sub-chains, partial structures) from
prior learning. On a novel problem, TNN RECOMBINES fragments from different
MAPs in a way never seen before. The recombination is not from a template;
it is a novel assembly of pieces. If the recombined form succeeds and is
useful, it is a new structural form.

Distinction from Composition C: Composition C chains WHOLE MAPs (each
segment is one MAP's full relation sequence). This worker recombines
SUB-MAP fragments: contiguous sub-chains (map_id, start, length) that were
never promoted as standalone MAPs. The critical discriminator is a goal
for which NO whole MAP's full relation sequence is satisfiable, but
fragments from different MAPs chain to a solution.

## Step 2: Base

Unfrozen variant only. `ir_base.zag` is a byte-identical copy of
`composition_C/cc_base.zag` (SHA-256
dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6),
which is the frozen TNN-2 core plus rebind (everything before `ev_query`).
Frozen source read-only, never modified. All new mechanism lives in
`ir_patch.zag`.

## Step 3: Outputs

- `ir_patch.zag`: fragment recombination mechanism + new `ev_query`
  (`recombine_try` hooked between `rebind_try` and trial). One-line config
  `frag_on()`: 1 = fragment recombination; 0 = whole-MAP-only control.
- `ir_driver.zag`: experiment driver (TREAT / WHOLE-ONLY / ABL-X / ABL-Y /
  FRESH / REUSE arms).
- `ir_full.zag` / `ir_full_nc.zag`: assembled sources (one-line diff:
  `frag_on()` 1 vs 0).
- `ir_bin` / `ir_nc_bin`: compiled binaries (pinned znc).
- `ir_run1/2/3.txt`, `ir_nc_run1/2/3.txt`: 3/3 byte-identical transcripts.
- `REPORT.md`: full analysis with SUF verdict.

Pure Zag. No em dashes or en dashes in loop documentation. Paper untouched.
Nothing pushed. 0 modes / 0 bridges / 0 handlers / 0 new semantic cases.
