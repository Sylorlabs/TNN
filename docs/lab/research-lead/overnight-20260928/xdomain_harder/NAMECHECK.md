# NAMECHECK.md -- X-Domain Harder-Pair Worker

## Step 0: Toolchain guard (mandatory)

Worker ran the safebin setup before any build or experiment step:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (no output lines before
`guard-check-done`). Safebin active for every compile and run below. No
forbidden executable was invoked at any point in this task. All
computation is Zag compiled with the pinned znc; shell is used only to
invoke znc, run binaries, and move files.

Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Preregistration

PREREG.md frozen and committed ALONE in commit 23266dc1c BEFORE any
driver source, assembly, binary, or run output was written. Kill bars
XH-H1/H2/H3, competence bar XH-COMP, determinism bar XH-DET, the H3
plen-sweep protocol, and the exact world facts are all fixed there.

## Experiment identity

- Harder pair: transform-then-navigate. X = COUNT (node -> number),
  r=81 facts, query r=91. Y = CHAIN on numeric subjects (number ->
  node), r=82 facts, query r=92. Z = Y(X(s)), query (21,93) -> 52.
- X1: (11,81,12),(12,81,13),(13,81,14); Q(11,91)->3.
- X2: (15,81,16),(16,81,17); Q(15,91)->2.
- Y1: (3,82,30),(30,82,31),(31,82,32); Q(3,92)->32.
- Y2: (2,82,40),(40,82,41),(41,82,42); Q(2,92)->42.
- Gap: 30 facts (5000+i, 60+(i%10), 6000+i).
- Z facts: (21,81,22),(22,81,23),(23,81,24),(24,81,25);
  (4,82,50),(50,82,51),(51,82,52). Q(21,93)->52.
- Arms per mechanism: TREAT, ABL-X (r=91 MAPs deleted), ABL-Y (r=92
  MAPs deleted), FRESH.

## Assemblies (patches verbatim, byte-compared)

- `xh_full_h1.zag` = `../invention_mutation/mu_core.zag`
  + `../invention_mutation/mu_patch.zag` + `xh_driver.zag`
- `xh_full_h2.zag` = `../invention_recombine/ir_base.zag`
  + `../invention_recombine/ir_patch.zag` + `xh_driver.zag`
- `xh_full_h3.zag` = `../invention_constraint/invent_base.zag`
  + `../invention_constraint/invent_patch.zag` + `xh_driver_h3.zag`

Patch SHAs (verbatim copies, verified with cmp against the source
dirs at build time; see build log):

- mu_patch.zag: H1 mutation stage (MUT_ON=1), ev_query redefined.
- ir_patch.zag: H2 fragment recombination (frag_on=1), ev_query
  redefined.
- invent_patch.zag: H3 constraint invention (invent_on=1),
  ev_query_c added.

Drivers are new (this worker): `xh_driver.zag` (H1/H2, plain
ev_query), `xh_driver_h3.zag` (H3, ev_query_c plen sweep 1..4 on Z,
plain ev_query on X/Y training).

## Build record

Pure Zag. Zero em/en dashes in sources and docs (byte-verified).
Frozen source read-only. Paper untouched. Committed locally, nothing
pushed. 0 modes / bridges / handlers / new semantic cases / domain
templates.

Binaries: `xh_bin_h1`, `xh_bin_h2`, `xh_bin_h3` (pinned znc).
Runs: `xh_run_h1_1/2/3.txt`, `xh_run_h2_1/2/3.txt`,
`xh_run_h3_1/2/3.txt` (3/3 byte-identical per binary; SHA-256 in
REPORT.md).
