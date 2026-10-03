# NAMECHECK: COGOPS-TRANSITION-PREDICT-2 (c22)

## Step 0: Toolchain guard (safebin mandatory)
- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  (already active from prior work in this lane).
- `export PATH="$HOME/safebin"` set for all build/run commands.
- Verified: `which python3` returns nothing; `which python` returns
  nothing under safebin PATH (checked 2026-10-03, recorded in lane).
- All computation in Zag (probe: c22_probe.zag; battery: c22 build).
  Shell used ONLY for: invoking znc, running binaries, git ops,
  file moves, grep/sed/diff on outputs (text processing, not
  computation). No Python invoked at any point.
- Pinned znc: `~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Git via `/usr/bin/git` (safebin git symlink has EPERM on writes;
  per AGENTS.md, use resolved binary path).

## Step 1: Prereg commit-order self-check
- PREREG.md, NAMECHECK.md, c22_probe.zag, c22_probe_c21replay.txt,
  c22_probe_c22predict.txt, c22_stages_predicted.txt, c22_world_add.zag
  committed BEFORE any implementation file (c22_main.zag,
  c22_build.sh) is written.
- Verify: `git log --oneline -- <lane>` shows prereg commit
  strictly before implementation commit.

## Step 2: No-Python-in-probe
- The probe (c22_probe.zag) is pure Zag. Its outputs were compared
  with shell grep/diff only (byte comparison, not computation).
- No Python in probe, analysis, or scoring.

## Step 3: Fresh-context discipline
- Each arc uses a fresh (nn,rel) context: P1=(3,617), P2=(3,619),
  Q1=(3,621), Q2=(3,623). No (nn,rel) shared between arcs.
- New rels have world facts mirroring rel 613's pattern; pilot
  verified NEED-winnable (setup) / unwinnable (test) with identical
  costs before prereg freeze.

## Step 4: plan_drop discipline
- c21's battery calls `plan_drop(L,g_tag(G))` after every stage;
  the plan table has 4 slots. The c22 main MUST do the same, or
  stages beyond the 4th will `decline=1` (pilot caught this).
- Kill bars K1-K4/K9 require DET-STRAT at every battery stage;
  a decline at any stage is a K9 fail.
