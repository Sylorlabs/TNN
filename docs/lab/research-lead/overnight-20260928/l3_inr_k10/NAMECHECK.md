# NAMECHECK: L3-INR-K10 independent red-team probe worker

Worker: L3-INR-K10 (subagent, depth 2/2, 2026-10-03). Task: independent
adversarial probe follow-up on L3-INR-SEALED (verdict L3-KILLED, C409).
Goal is NOT to overturn the KILL (terminal per governance). Goal: complete
the verdict record by characterizing the L2+ envelope, focused on the
honest arms that passed: T4 (regime-change revision) and T5a (probe
resolution). Map the boundary between L2+ success and failure.

Work directory: `l3_inr_k10/` (this directory). The frozen implementation
`l3_inr_impl/` is NEVER modified by this worker (read-only; its frozen
binaries and verbatim driver script are invoked, never edited). The frozen
prereg `l3_interm_repr_reuse/` and the sealed battery `l3_inr_sealed/` are
never touched. World files are data, not code.

Probe family (designed by this worker, independent adversary, materially
different from S1-S5):
- P-C (pc.world): probe-loop iteration test. Two gaps; the id-first gap is
  REVERSED relative to id order, so the first probe's true answer (0)
  agrees with E*'s prediction and the probe loop must iterate to resolve
  the second gap. Tests the exact mechanistic boundary of the S1 kill
  (there, the first probe's answer 1 eliminated E* and stopped the loop).
- P-D (pd1.world -> pd2.world): revision under ID-PERMUTED world. Same
  mild block-rotation regime change as S2, but pd2's PAIR listing order is
  permuted so first-appearance ids differ from pd1's. Tests sealed-battery
  adversarial finding #3 (toxic purge compares positional ids with no
  remapping) as an ACTIVE probe rather than a documented caveat.
- P-E (pd1.world -> pe2.world): FULL-ORDER-REVERSAL revision with ALIGNED
  ids. Tests whether revision magnitude is bounded given id alignment.

## Step 0: Worker toolchain guard (MANDATORY, recorded)

Safebin activated at startup: `export PATH="$HOME/safebin"`.
Verification performed under the safebin PATH before any K10 work
(2026-10-03):

- `which python3` returns nothing.
- `which python` returns nothing.
- `which znc` returns /home/hatch/safebin/znc (pinned compiler).

All scientific computation is pure Zag executed via the FROZEN
implementation binaries (learner_bin/world_bin/spearman), which are
themselves pure-Zag builds of the frozen implementation. No new Zag code
is written by this worker (world files are data; no compiler invoked).
Shell is used only for: invoking binaries, file moves/copies, sha256sum
digesting, git operations, and the file-mediated driver (no computation).
No Python or other interpreter is invoked at any point. Per Micah's
2026-09-30 governance ruling, any forbidden executable invocation would
make this wave PROCESS-FAIL. None occurred.

## Step 1: Scope check

- Prereg (PREREG.md) is committed BEFORE any world is materialized or any
  arm is run. Commit order: prereg commit strictly precedes worlds/runs.
- Frozen predictions are recorded in PREREG.md; the verdict is read off
  them after 3/3 byte-identical runs.
- This worker is the INDEPENDENT ADVERSARY for K10: P-D is designed to make
  the honest T4 arm FAIL (predicted FAIL = successful probe); P-C and P-E
  are designed to map capability boundaries (predicted PASS).
- The L3-KILL verdict is terminal and is not revisited. No L3 claim is
  made or implied by any outcome here.
- Opaque identifiers throughout (fresh w*/v* names; attrs verified
  |Spearman| < 0.2 vs true order with the frozen spearman binary).
- Commits local, never push, explicit pathspecs.
