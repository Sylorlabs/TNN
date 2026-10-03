# NAMECHECK: Budget Pressure Experimenter

## Step 0: Toolchain guard (mandatory, recorded)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked allowed tools
  (git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum
  git-receive-pack git-upload-pack).
- `export PATH="$HOME/safebin"` for all work.
- `which python3` and `which python` returned NOTHING. Zero forbidden
  executables invoked in this wave. All computation in Zag via the pinned
  compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`; shell used
  only to invoke znc, run the binary, git ops, move/copy files.

## Scope

Budget-pressure experiment on TNN-2. Tests the forgetting-analysis
prediction (`2726baf74`): "P4 profile at scale (structures die first,
MAPs fossilize, answers catastrophically forgotten after 12 idle events,
garbage consumes budget)." Novel contribution beyond the existing P4
characterization (`tnn2_transfer/TRANSFER_ANALYSIS.md`): post-pressure
capability (can the learner still learn, answer, construct, and retain
under sustained cap pressure?).

## Frozen-artifact handling

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  verified before copying.
- `bp_base.zag`: verbatim copy, SHA-256 verified identical after copy.
- `bp_nodriver.zag`: verbatim copy with only the test-main line
  (`fn main()i32 { return run_all(); }`) removed. Cognition code untouched.
- `bp_full.zag`: `bp_nodriver.zag` + `bp_driver.zag` (measurement driver,
  new `main` only).
- Frozen `tnn2_build/tnn2.zag` and `tnn2_build/tnn2_bin` never modified;
  verified unmodified at end of wave (clean `git status` on `tnn2_build/`).
- All experiments on the clearly marked copies in this directory.

## Input provenance

- Eviction mechanics from `forgetting/FORGETTING_ANALYSIS.md` (read-only).
- P4 baseline from `tnn2_transfer/TRANSFER_ANALYSIS.md` section 4 (read-only).
- Driver patterns adapted from `state_dynamics/sd_driver.zag` (read-only).
- Unsealed synthetic subjects only (6000s, 7000s, 8000s, 9000s, 9100s,
  9500s, 9800s, 9900s). No sealed H2/FW/world files opened at any point.

## Constraints honored

- Frozen TNN-2 untouched. Pure Zag. 3/3 byte-identical runs required.
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commit only, explicit pathspecs.
- Experiment, not TNN-3: no source changes to cognition, no new mechanisms.
