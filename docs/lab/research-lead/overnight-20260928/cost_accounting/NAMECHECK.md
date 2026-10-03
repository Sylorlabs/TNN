# NAMECHECK: Cost Accountant

## Step 0: Toolchain guard (mandatory, recorded)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked allowed tools
  (git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum
  git-receive-pack git-upload-pack).
- `export PATH="$HOME/safebin"`.
- `which python3 python` returned NOTHING. Zero forbidden executables invoked.
  All computation in Zag (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`); shell used only to invoke
  znc, run the binary, git ops, move/copy files.

## Scope

Establish systematic cost accounting for TNN-2 operations along four
dimensions: node allocation, edge allocation, ISA execution steps, and
workspace scan steps. Measurement only; no capability claim.

## UNFROZEN VARIANT declaration

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  verified before copying. Frozen source and frozen binary `tnn2_bin`
  untouched (no modifications; verified by path isolation, no writes to
  `tnn2_build/`).
- `cost_base.zag`: verbatim copy of frozen source (SHA-256 identical,
  verified).
- `cost_full.zag`: `cost_base.zag` plus behavior-preserving instrumentation
  (12 counter increments into spare header offsets 56 and 60, which no
  production code reads or writes), original test `main` removed,
  `cost_driver.zag` appended. Cognition logic untouched; `diff` against
  `cost_base.zag` shows only the 12 insertions, the main removal, and the
  driver.
- `cost_bin`: compiled from `cost_full.zag` with the pinned znc.

## Instrumentation (variant only)

Spare header offsets 56 (EXEC) and 60 (SCAN), free in the frozen layout
(used: 0,4,8,12,16,20,24,28,32,36,40,44,48; nodes start at 64).

- EXEC (hg 56): incremented once per iteration of the `execute` ISA loop.
  Counts opcodes executed (tags 101-104).
- SCAN (hg 60): incremented once per iteration of each instrumented
  workspace scan loop: `link_edge` alloc scan, `is_superseded`,
  `activate`, `decay`, `is_prot`, `evcount`, `bid` MEM scan,
  `evict_node` node scan, `evict_node` edge scan, `ref_prot`,
  `t2_lu_first`.
- Nodes/edges: no instrumentation; measured as delta of `hg(W,20)` /
  `hg(W,24)` snapshotted before/after each operation in the driver.

Not instrumented (documented limitation): `alloc_node`/`alloc_raw`
free-slot scans (small, bounded by first-free-slot), `fr_get`/`fr_set`
frame walks, trial assembler loops. SCAN is therefore a lower bound on
total loop iterations; the dominant O(NxE) scans are all covered.

## Behavior preservation

The driver asserts the expected return value of every measured operation
(chain4 trial returns 5, act returns 30, revise post-query is 999, etc.).
Zero ASSERT-FAIL lines across 3/3 byte-identical runs. The counters write
only to spare header fields that no production code reads.

## Input provenance

- Frozen source SHA-256 (above).
- Prior measurements: state dynamics `ee238d8d4` (teach +1/+2, masked
  miss +14/+6).
- Baseline arena `dbf0ce359` (requires marginal/amortized accounting).

## Constraints honored

UNFROZEN VARIANT ONLY. Pure Zag. Zero em dashes (byte-verified).
Paper untouched. Nothing pushed. No sealed worlds. Measurement, not TNN-3.
