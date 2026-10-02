# NAMECHECK.md -- Composition Cross-Domain Worker

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

Result: `which python3 python` returned NOTHING. Guard check printed
`guard-check-done` with no interpreter paths above it. Safebin active for
all compile and run steps below. No forbidden executable was invoked at
any point in this task.

Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Build record

Pure Zag. Zero em/en dashes in sources and docs (byte-verified with grep).
Bases and patches copied verbatim from prior workers (byte-compared, see
REPORT.md). Only the three drivers (`xd_driver_a/b/c.zag`) are new.

Assemblies:
- `xd_full_a.zag` = `../composition_A/cx_core.zag` + `../composition_A/cx_patch.zag` + `xd_driver_a.zag`
- `xd_full_b.zag` = `head -1567 ../knowledge_composition/kc_core.zag` + `../composition_B/cb_patch.zag` + `xd_driver_b.zag`
- `xd_full_c.zag` = `../composition_C/cc_base.zag` + `../composition_C/cc_patch.zag` + `xd_driver_c.zag`

Binaries: `xd_bin_a`, `xd_bin_b`, `xd_bin_c` (pinned znc).
Runs: `xd_run_a1/2/3.txt`, `xd_run_b1/2/3.txt`, `xd_run_c1/2/3.txt`
(3/3 byte-identical per binary; SHA-256 in REPORT.md).

## Experiment identity

- X domain: chain-following, r=81, plen-4 chains. Queries (s,91) -> endpoint.
- Y domain: count aggregation, r=82. Queries (s,92) -> link count. Y MAPs
  are count graphs (guard/set links + INC cells + MOV epilogue); output is
  computed arithmetically, not retrieved by navigation.
- Z: chain-then-count, query (31,93) -> 2. Facts (31,81,32),(32,81,33),
  (33,81,34) then (34,82,35),(35,82,36). Requires X-walk to 34, then
  Y-count of 34 = 2.
- Arms per mechanism: TREAT, ABL-X (r=91 MAPs deleted), ABL-Y (r=92 MAPs
  deleted), FRESH (no X/Y training). B TREAT adds one ev_cq co-use episode
  (chain query then count query on its output) to give B's history
  mechanism its best chance.

Frozen source read-only. Paper untouched. Committed locally, nothing pushed.
0 modes / bridges / handlers / new semantic cases.
