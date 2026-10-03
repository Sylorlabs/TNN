# NAMECHECK: COGOPS-TRANSITION-PREDICT (c21)

## Step 0: Toolchain guard
- Safebin active: `export PATH="$HOME/safebin"`.
- `which python3` returns nothing. `which python` returns nothing.
- All computation in Zag (probe, battery). Shell only for znc,
  binary execution, git ops, file moves.
- Pinned znc: ~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1

## Step 1: Lane
docs/lab/research-lead/overnight-20260928/cogops_transition_predict/
Builds on COGOPS-LEADERSHIP-TRANSITION (c20h). No name collisions.

## Step 2: Base
c20_base.zag (frozen) + c18_world.zag (frozen) + c20h_learn.zag
(frozen, via build script) + c21_world_add.zag (NEW, empty: no new
kinds needed; proven kinds 2,4,8,9 reused) + c21_main.zag (NEW).

## Step 3: Determinism
3/3 byte-identical runs required (K6). sha256 recorded in REPORT.

## Step 4: Prereg commit order
PREREG.md + NAMECHECK.md + c21_stages_predicted.txt committed
BEFORE any implementation file (c21_world_add.zag, c21_main.zag,
c21_build.sh, c21h_learn.zag, binaries, REPORT.md).
Self-check: `git log --oneline -- <lane>` must show prereg commit
strictly before implementation commit.

## Step 5: Kill bars
K1-K8 in PREREG.md (frozen). No weakening.

## Step 6: Provenance
- Score formula, argmin, hedge: c20h_strat_additive.zag.
- Turn costs: validated against c20h_run1.txt DET evidence.
- Kinds 2,4,8,9: c18_world.zag / c19 (proven unwinnable/winnable).
- Probe: /tmp/tpv/probe.zag (throwaway, not committed).
- nn<=4: learner buffers (mat_inputs W=320B, topo_g ind/placed=16B)
  assume nn<=4. An nn=6 extension panicked (slice out of bounds);
  abandoned to keep the learn prefix frozen.
