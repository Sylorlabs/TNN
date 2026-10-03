# NAMECHECK: NT-ORDER-MIRROR

## Step 0: Worker toolchain guard (mandatory)

- Safebin activation: `export PATH="$HOME/safebin"` run at worker
  startup before any build/run step. Recorded here.
- Toolchain verification: `which znc` -> `/home/hatch/safebin/znc`
  (pinned znc 2026.07.0-dev, same build as NT1/NT-D2/NT-PORT/
  NT-PRESSURE/NT-PORT-PRESSURE/NT-LOWVALUE-BOUNDARY);
  `which python3` -> nothing (no output);
  `which python` -> nothing. Python and all other forbidden
  interpreters are absent from the worker PATH.
- Pure-Zag rule: all research logic (learner, oracles, protocol,
  probes, kill-bar evaluation) implemented in `ntom_full.zag` only.
  Shell used solely to invoke znc, run the binary, and for git/file
  operations. No Python/C/JS/Rust anywhere in the lane.
- Compiler-defect workarounds honored per PREREG Section 6
  (same five as NTLV: get32/set32 only; single-buffer cursor output
  + one raw syscall; De Morgan in while conditions; if-nesting at
  most 3 deep via per-arm helper fns; no `[]u8 as *u8` casts).

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/nt_order_mirror/`
- Task: NT-ORDER-MIRROR worker; non-ledger task (claim minting
  paused). Parent: NT follow-up orchestrator.
- Subject: D1+D2 port verbatim from NT-LOWVALUE-BOUNDARY
  (ntlv_full.zag cl_* fns); the SOLE lane change is phase-2 teach
  order: the RARE link (148,1)->152 is taught FIRST (not last)
  among phase-2 teachings on re-teach passes.
- This lane is the order-dependence mirror recommended (not
  preregistered) in the NTLV REPORT: it tests whether installation
  recency, not reinforcement frequency, is the true determinant of
  D2 victimhood. Frozen directional prediction: tenure-protection,
  avail 4/4 for all K (K=1,2,3,6).
- Distinct from `nt_lowvalue_boundary` (RARE taught last;
  LIABILITY-CONFIRMED, avail 4/2/1/0): same workload, same K-sweep,
  same learner, mirrored teach order only.
