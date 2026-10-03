# NAMECHECK.md -- Invention Hypothesis 1 Worker (structural mutation from failure)

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned NOTHING.
PATH=/home/hatch/safebin. Safebin active for all subsequent work.

No forbidden executable invoked. Pure Zag via pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1).

## Step 1: Task identity

Invention Hypothesis 1 Worker. Approach: structural mutation from failure
(Micah Priority 8, 2026-10-01). Unfrozen variant only. Base: the
persistent-connections core (composition_A/cx_core.zag, rebind + trial,
no composition patch), copied to mu_core.zag with a general gather-depth
extension (5 to 6, path layout len/v0..v5/f0..f4) so invented longer forms
stay rebindable.

## Step 2: Constraints honored

- Unfrozen only. Frozen source read-only (never modified).
- Pure Zag. Shell only for znc invocation, binary runs, git, file moves.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched: docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases, no MUTATE_MODE.
- No finite menu: the operator extends by one cell using world data; the
  specific resulting form is data determined, and mutants become parents
  for further mutation (open-ended through iteration).

## Step 3: Development notes

- mu_patch_nomut.zag derived from mu_patch.zag by a single sed replacing
  `fn MUT_ON()i32 { return 1; }` with `return 0;`. Byte diff is that one
  line; everything else identical. This is the ablation binary.
- Gather-6 edit: t2_gather `len<5` to `len<6`, fact offset base+24 to
  base+28 in t2_gather/t2_trial/pc_try_one, pc_try_one fact buffer 16 to
  20 bytes. Trial's construction bound unchanged (k=2..4, plen<=5), so the
  plen-6 problem remains unreachable by trial.
- One misapplied edit during development (z_alloc 20 landed on t2_trial's
  buffer instead of pc_try_one's) caught by grep audit and corrected
  before building.

## Step 4: Determinism

3/3 byte-identical runs (mu_bin).
sha256 928ed73755d10a77a0cf0acf7b2759d571c8c57601be0d714294120410fab14f
(mu_run1/2/3.txt).
Ablation binary 2/2 identical.
sha256 5331d079d9101e5b6955269e7083d20f693ee751e0f05d5f27998fabb2a2ccb1
(mu_abl1/2.txt).

## Architecture accounting

- Cognition source lines added: mu_patch.zag (mutation stage), all in the
  unfrozen patch layer. Zero changes to frozen TNN-2 core.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New task-specific handlers: 0.
- Learner-state structures created: mutant MAPs (tag 20) with type-1 DEP
  edges to the parent MAP plus standard fact provenance; standard MAP
  promotion otherwise.
- Capability-source delta: one general pipeline stage (mutate_try) that
  fires on any query where existing mechanisms fail and a parent MAP can
  be extended, not a plen-6-specific template.
