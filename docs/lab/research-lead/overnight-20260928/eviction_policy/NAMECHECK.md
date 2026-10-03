# NAMECHECK: EVICTION-POLICY comparison (FIFO vs owner-partitioned vs pinning)

## Step 0: Toolchain Guard

- Safebin activated at startup: `$HOME/safebin` (verified present).
- `export PATH="$HOME/safebin"` applied for all subsequent work.
- `which python3` returned NOTHING. `which python` returned NOTHING.
- `which znc` returns `/home/hatch/safebin/znc`, a symlink to the pinned
  compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`).
- No Python, C/C++, JavaScript, or Rust invoked at any point. Work so far:
  shell only (mkdir, ls, git branch/status, file writes of prereg documents).
- Any forbidden-executable invocation in later steps = automatic
  PROCESS-FAIL for the current scientific wave.

## Scope

Lane directory (owned path only):
`docs/lab/research-lead/overnight-20260928/eviction_policy/`

Contents: PREREG.md (frozen first), NAMECHECK.md (this file),
eviction_policy.zag (implementation, after prereg commit), build
outputs, raw run logs (run1/2/3.txt), REPORT.md (after 3/3 runs).

## Environment notes

- Repo ~/workspace/tnn-rsi-gpi3; branch tnn-native-lab. Working directly
  in the checkout (no sparse worktree needed; the pinned znc is already
  present at src/tools/toolchain/).
- Commits local only, never pushed. Explicit pathspecs on every commit.
  No `git reset`. No amend of shared history. Per the 2026-10-03 shared
  workspace lesson, git writes go through /usr/bin/git directly (the
  safebin git symlink has failed with EPERM on object writes); on
  index.lock contention, retry with sleep backoff and never remove the
  lock while other workers are active.
- Builds on L2-INTERFERENCE2 (`../l2_interference2/`, VERDICT=PASS,
  2026-10-03): same A family (35 queries), same benign FULL writer
  (20 conflicts), same churn adversary (key 3999, B-owned, w writes),
  same owner-scoped reads. Frozen differences: pool fixed at 32, the
  POOL0 ablation branch removed, and the conflict-relocation path
  parameterized by eviction policy (0 FIFO, 1 PART, 2 PIN) with the new
  header fields documented in PREREG.md.
- Non-ledger task: claim minting paused; no ledger entries are made.
- Sealed worlds: none used. No sealed-world contents inspected.
- Documentation style: no em or en dashes in lane documents (verified
  before commit).

## Design lineage

Follow-up to L2-INTERFERENCE2 (VERDICT=PASS). That lane's money result
was that circular FIFO eviction is flushable: pool=32 absorbs the
benign writer (ret=100) yet the churn adversary drives retention to 0
(dose-response [100,54,0] at r=0,20,32). Its report recommended this
exact comparison as option (b): FIFO vs owner-partitioned vs pinning
with the adversary held fixed. This lane is a policy comparison on a
frozen mechanism, not a repair lineage: the mechanism does not change,
only the pool eviction policy varies, and the adversary (key, values,
doses) is identical across policies with its footprint kill-barred by
K7.
