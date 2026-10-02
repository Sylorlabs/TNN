# NAMECHECK: wave-20261001-2021pdt, lane CONTLEARN (continuing learner integration)

## Step 0: toolchain guard (safebin activation)

- Date: 2026-10-01 20:26 PDT (Thu)
- Ran: `cd ~/workspace/tnn-rsi && bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python); znc OK
  (pinned /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- Exported PATH="$HOME/safebin" (safebin only).
- `which python3` prints NOTHING (verified empty, exit 1).
- `which python` prints NOTHING (verified empty, exit 1).
- No Python, C/C++, JavaScript, or Rust will be used for research logic in
  this lane. Shell only invokes pinned znc, runs binaries, git ops, and file
  moves/copies. Any forbidden executable invocation is automatic PROCESS-FAIL
  and will be reported honestly.
- Phase 1 scope: WRITING ONLY (PREREG_CONTLEARN.md). No implementation, no
  experiment execution, no binary runs in this turn.

## Step 1: working copy

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (verified
  via `git branch --show-current`).
- Lane directory: docs/lab/rsi/runs/wave-20261001-2021pdt/CONTLEARN/ (writes only
  inside this directory).
- No git push, no git reset --hard, no rebase, no git commit by this worker;
  the coordinator commits at wave end (prereg committed alone first, per K0).

## Step 2: context re-derived (not cited from memory)

- Read H10 (one learner-owned structural workspace) and the ranking notes in
  docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md (lines ~290-400).
- Read docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/ARCH_ACCOUNTING.md in full
  (M1/M2/M3 researcher-vs-learner line, 12/12 retention, dormant evidence
  machinery).
- Read docs/lab/rsi/runs/wave-20261001-1421pdt/gov/ARCH_ACCOUNTING_1421.md
  (contlearn2: 136 lines, 1024 bytes; CLA-2: 739 cognition lines; frozen core
  586 cognition lines, 32768 state bytes).
- Read docs/lab/research-lead/overnight-20260928/continuing_learner/PREREG_CLA2.md
  (event loop, evidence rules, kill-bar style) and PREREG_CONTLEARN2.md
  (commit-order bar, frozen workload style).
- Read the frozen core source
  docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag directly:
  event loop (ev_teach/ev_query/ev_observe), trial (t2_trial/mp_run),
  promotion (promote_graph), revision (revise_on_contradict/t2_revise_graph),
  allocator (alloc_node/evict_node), decay, z_alloc zero-fill. SHA-256
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd verified.
- Governance caveat honored: the mini_lifetime_integration 3/3 determinism
  claim is not artifact-backed beyond run1 transcripts (per the 1721pdt zombie
  investigation); it is not cited as established anywhere in this lane.
