# NAMECHECK.md -- XDomain L2 Adaptive Reuse Worker (arithmetic to planning, renamed interface)

## Step 0: Toolchain guard (mandatory)

Worker ran the safebin setup before any build or experiment step:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3; which python; echo "guard-check-done"
```

Result: `which python3` and `which python` returned NOTHING
(setup script itself verified "python3 absent from safebin PATH (OK)",
"python absent from safebin PATH (OK)"). Guard check printed
`guard-check-done` with no interpreter paths above it. Safebin active
for all compile and run steps below. No forbidden executable was
invoked at any point in this task.

Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## Commit-order self-check

PREREG.md frozen and committed ALONE (this NAMECHECK.md committed in
the same prereg-only commit, no implementation) before any .zag
implementation was written. Implementation commit(s) follow strictly
after the prereg commit hash.

## Build record

Pure Zag. Zero em/en dashes in sources and docs (byte-verified).
Bases copied verbatim from prior workers (byte-compared, see
REPORT.md). New files only: trunc_patch.zag,
trunc_patch_noadapt.zag (exact one-line diff: adapt_on 1 -> 0),
xd_driver.zag, xd_driver_noadapt.zag.

Assemblies:
- `xd_full.zag` = `../composition_C/cc_base.zag` +
  `../composition_unified/un_patch.zag` + `trunc_patch.zag` +
  `xd_driver.zag`
- `xd_full_noadapt.zag` = `../composition_C/cc_base.zag` +
  `../composition_unified/un_patch.zag` +
  `trunc_patch_noadapt.zag` + `xd_driver_noadapt.zag`

Binaries: `xd_bin`, `xd_bin_noadapt` (pinned znc).
Runs: `xd_run1/2/3.txt` (3/3 byte-identical; SHA-256 in REPORT.md),
`xd_noadapt_run1/2/3.txt` (3/3 byte-identical; SHA-256 in REPORT.md).

## Experiment identity

- X domain (arithmetic): SUM over price facts, trained independently:
  ev_teach (201,81,231),(231,81,261),(261,81,291); ev_query
  (201,91,291) promotes MAP_X with relseq [81,81,81]. X outputs a
  scalar total.
- Y domain (planning): ALLOC budget procedure, trained independently:
  ev_teach (301,82,311),(311,82,321),(321,82,331); ev_query
  (301,92,331) promotes MAP_Y with relseq [82,82,82].
- Z world (cross-domain, length-mismatched planning problem): facts
  (101,81,102),(102,81,103),(103,81,104) [price accumulation],
  (104,82,105),(105,82,106) [allocation, only two steps while Y was
  trained with three]. Query (101,70,106): accumulate the scalar
  total, then allocate it in fewer steps than Y's trained interface.
- Mismatch: Y's trained interface [82,82,82] does not fit Z's two
  allocation facts. Exact composition provably fails (A5 control:
  -2); the failure defeats the full unified pipeline (C relseq, A
  contract, B ordering, trial), not a weakened configuration.
- Adaptation: TRUNCATE-TAIL, a learner-triggered operator. After the
  standard pipeline fails, it anchors at each candidate first-segment
  endpoint, reads the longest frontier-licensed proper prefix of each
  native MAP's relation sequence from the fact store, and truncates
  to it. Licensed by real Z facts, execution-verified, promoted with
  a type-16 adapted-from edge, then the unchanged compose_try
  re-runs. (An earlier rename-mismatch design was withdrawn by
  PREREG_AMENDMENT1 after a pilot showed the unified composition's
  contract fallback solves renames without adaptation.)

Frozen source read-only. Paper untouched. Committed locally, nothing
pushed. 0 new edge types, 0 new opcodes, 0 modes, 0 bridges, 0
handlers, 0 semantic cases.
