# NAMECHECK.md - Zombie Census Worker

## Step 0: Toolchain Guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 41 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp,
  sha256sum, git-receive-pack, git-upload-pack, and coreutils).
- `export PATH="$HOME/safebin"` applied before all work.
- `which python3 python` returns nothing. Zero forbidden executables invoked.
- All computation in pure Zag via pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Shell used only to invoke znc, run binaries, git ops, move/copy files.
- Guard check recorded: 2026-10-01.

## Step 1: Scope

- Measurement ONLY. No source fixes, no TNN-3, no architecture changes.
- Frozen TNN-2 untouched. All experiments on verbatim copy
  `zombie_census/zc_base.zag`.
- Verbatim verification: SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  matches frozen `tnn2_build/tnn2.zag` before and after all work.

## Step 2: Input Provenance

- Layout facts from frozen `tnn2.zag` (read-only): node offset 64+n*40,
  field 0 = tag, field 36 = live; MAP tag 20, s at field 8, r at field 4,
  graph root at field 20, answer at field 28; edges at 41024+e*16,
  field 0 = from, field 4 = type, field 8 = to; SEQ edge type 12;
  op tags 101-104; workspace size 110656 bytes.
- Zombie definition from eviction-corruption analysis `986c52fdc`:
  MAP root stored as plain integer field, not edge; evict_node cannot see
  field-based references; graph cells (bid 0) evicted first under pressure.
- Baseline rates from white-box inventory `b17fee225`: 9/52 W MAPs dangling
  (20 percent), FW MAPs 45/82 corrupted in FW9 churn.
- Inspector `inspect_state.zag` from `b17fee225` consulted for layout
  cross-check only; detector written independently in-driver.

## Step 3: Workloads

- Unsealed synthetic integer subjects only (4000s, 5000s, 6000s ranges).
  No sealed H2/FW/W world content opened, listed, or hashed.
- W1 LIGHT: 20 teaches + 4 masked queries (MAP promotion, no pressure).
- W2 MEDIUM: 60 teaches + 10 masked queries + 5 contradictions.
- W3 HEAVY: 80 chain-promote cycles (2 teaches + 1 masked query each),
  designed to exceed the 1024-node budget and force eviction churn.

## Step 4: Determinism

- 3 runs per workload. Byte-identical required before any rate is quoted.

## Constraints honored

- Frozen source/binary read-only. Pure Zag. Zero em dashes
  (byte-verified before commit). Paper untouched. Nothing pushed.
  Local commit only, explicit pathspecs.
