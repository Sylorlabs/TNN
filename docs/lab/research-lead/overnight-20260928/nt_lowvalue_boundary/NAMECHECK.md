# NAMECHECK: NT-LOWVALUE-BOUNDARY

## Step 0: Worker toolchain guard (mandatory)

- Safebin activation: `export PATH="$HOME/safebin"` run at worker
  startup before any build/run step. Recorded here.
- Toolchain verification: `which znc` -> `/home/hatch/safebin/znc`
  (pinned znc 2026.07.0-dev); `which python3` -> nothing (no output);
  `which python` -> nothing. Python and all other forbidden
  interpreters are absent from the worker PATH.
- Pure-Zag rule: all research logic (learner, oracles, protocol,
  probes, kill-bar evaluation) implemented in `ntlv_full.zag` only.
  Shell used solely to invoke znc, run the binary, and for git/file
  operations. No Python/C/JS/Rust anywhere in the lane.
- Compiler-defect workarounds honored per PREREG Section 6.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/nt_lowvalue_boundary/`
- Task: NT-LOWVALUE-BOUNDARY worker; non-ledger task (claim minting
  paused). Parent: E8 follow-up orchestrator.
- Subject: D1+D2 port verbatim from NT-PORT-PRESSURE; novelty is the
  workload (RARE genuinely-useful infrequently-reinforced link 148)
  and the K-sweep protocol (P1/P2/P3/P6 arms, M=6 passes).
- Distinct from `nt_lifobound` (key-value workload, once-taught
  novels, verdict INCONCLUSIVE at P2/P3/P5): this lane uses
  rule-structured 2-hop-chain families and a reinforcement-period
  sweep with a scored usefulness probe (q(100) requires the RARE
  link).
