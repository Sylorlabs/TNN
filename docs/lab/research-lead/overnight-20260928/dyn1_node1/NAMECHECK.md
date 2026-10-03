# NAMECHECK: DYN-1 on H3-lite Node 1 variant

## Step 0: Toolchain guard

Executed before any research work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: safebin active. `which python3 python` returned nothing
(only "guard-check-done" printed). Zero forbidden executables invoked in
this wave. Pure Zag compiled with the pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## Scope

MEASUREMENT ONLY. No implementation, no cognition changes, no prereg work.

## Input provenance

- Cognition: `h3lite_node1/h3n1_variant.zag` (H3-lite Node 1, commit
  `45c55ed83`), SHA-256
  `e45ecd418578de45db21ea7de085cc068363c38b9d9d61599be8f20b1ab89f67`
  (verbatim copy as `dyn1n1_cog.zag`, hash re-verified after copy).
- Driver: `dyn1/dyn1_driver.zag` (DYN-1 baseline driver, commit
  `003767553`), copied verbatim as `dyn1_driver.zag`.
- Build: `dyn1n1_full.zag` = cognition with its test `main` removed plus
  the driver appended (mirrors the `dyn1_full.zag` build pattern from
  `003767553`; only the `fn main()i32 { return run_all(); }` line removed,
  `run_all` retained as dead code).
- Probe: `probe_bin` = same cognition with a driver variant that emits
  the tag-40 policy node state after the sequence (diagnostic only).

## Constraints honored

- Unfrozen variant only. Frozen TNN-2 source read-only, never touched.
- Pure Zag via the pinned znc. Shell used only to invoke znc, run
  binaries, and do git/file operations.
- Zero em dashes (byte-verified below).
- Research paper
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  untouched.
- No sealed worlds opened. Nothing pushed.

## Deliverables

- `DYN1_NODE1.md` (method, measurements, verdict)
- `dyn1n1_cog.zag` (verbatim Node 1 cognition copy)
- `dyn1_driver.zag` (verbatim DYN-1 driver copy)
- `dyn1n1_full.zag` (measurement variant)
- `dyn1n1_bin` (compiled binary)
- `run1.txt`, `run2.txt`, `run3.txt` (3/3 byte-identical)
- `probe_driver.zag`, `probe_nomain.zag`, `probe_bin`, `probe_run.txt`
  (policy-state probe evidence)
