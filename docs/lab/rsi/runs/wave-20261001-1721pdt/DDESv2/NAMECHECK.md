# NAMECHECK: ddes V2 steps 7-11 (t*=0 repair re-run)

Wave: wave-20261001-1721pdt. Lane: DDESv2.
Lane dir: docs/lab/rsi/runs/wave-20261001-1721pdt/DDESv2/
Worker: research worker (depth 2/2), no child subagents spawned.

## Step 0: toolchain guard (recorded before any other work)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh:
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- Exported PATH="$HOME/safebin" for all subsequent work.
- `which python3` returns nothing; `which python` returns nothing.
- `which znc` resolves to /home/hatch/safebin/znc (pinned znc,
  Linux x86_64 build abed8aa1).
- Guard check result: PYTHON3_NOT_FOUND (pass), PYTHON_NOT_FOUND
  (pass). Pure-Zag constraint acknowledged: any forbidden-executable
  invocation makes this wave PROCESS-FAIL.

## Step 0 (re-activation by the replacement worker, Thu 2026-10-01)

- Re-ran docs/lab/research-lead/overnight-20260928/safebin_setup/
  setup_safebin.sh: SAFEBIN-READY: /home/hatch/safebin (36 tools,
  no python).
- Re-exported PATH="$HOME/safebin" for all subsequent work.
- `which python3` returns nothing (exit 1); `which python` returns
  nothing. `which znc` resolves to /home/hatch/safebin/znc.
- No forbidden executable invoked. The lane's prior worker did setup
  and planning only; this worker reuses the frozen plan above and
  performs steps 7-11 (implementation, sealed re-run, RESULT doc).

## Assignment

Steps 7-11 of the DDES V2 pipeline (OOD test, ablation,
transfer/reuse, red team round 2, governance audit) plus repair of
the t*=0 soundness hole (sealed World F silent wrong convergence)
and a sealed re-run, all in pure Zag, zero randomness in decision
paths, byte-identical reruns (3/3) on the decisive tests.

## Frozen records located (step 1 of the task)

- Frozen prereg (V2): docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/
  PREREG_DDES_FOLLOWUP_V2.md plus PREREG_DDES_FOLLOWUP_V2_AMENDMENT1.md
  (wave-20261001-1121pdt).
- BUILD-PASS result: docs/lab/rsi/runs/wave-20261001-1121pdt/ddes/
  RESULT_DDES_FOLLOWUP_V2.md (implementation ddesp2.zag).
- Step 4 independent reproduction:
  docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/
  REPRO_DDES_V2_STEP4.md.
- Step 6 alternative-explanation attack:
  docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_attack/
  ATTACK_DDES_V2_STEP6.md (verdict: CLAIM-WEAKENED scoped; attacks
  1 and 4 succeed at the output level, attacks 2 and 3 confirm the
  white-box facts).
- R2 lineage (t*=0 repair origin): docs/lab/rsi/runs/
  wave-20260930-1121pdt/ddes/ (REPAIR-PASS, independently verified).
- Wave record with the three BINDING citation caveats:
  docs/lab/rsi/runs/wave-20261001-1421pdt/WAVE_RECORD.md.
- Step 7-11 plan definition: the queued item in WAVE_RECORD.md
  ("ddes V2: steps 7-11 of the pipeline (OOD test, ablation,
  transfer/reuse, red team round 2, governance audit) with the
  binding caveats and the post-freeze adversary-chosen record
  value") plus the step-6 attack report's recommended follow-up
  (post-freeze adversary-chosen record value carried through the
  disconnect, so hardcoding the frozen expected values cannot pass).

## Plan for this lane

1. Write PLAN_DDES_V2_STEPS7_11.md (frozen kill bars) BEFORE any
   implementation file. No commits in this lane, so ordering is by
   authorship sequence, documented here.
2. Implement ddesv2_s7.zag (pure Zag): repaired derivation on F
   (regression), A (anchor), fresh adversarial world H
   (same t*=0 hole, different signature V*=1), OOD derivation world
   K (no discriminating plan), red-team worlds RT1 (propagation
   chain) and RT2 (floor destroys discrimination); schema records
   R_F and R_H (R_H is the post-freeze adversary-chosen record
   value, frozen in the plan before implementation); scaffold
   disconnect; phase B on sealed G (R_F), sealed I (R_H), OOD world
   J (class mismatch, loud failure).
3. Pre-repair control binary ddesv2_pre.zag (unrepaired derivation
   on F) to exhibit the silent-wrong pattern being repaired.
4. Ablation variants of the main binary (mechanical sed edits,
   recorded): no-clamp, no-guard (with injected phase-2 probe),
   zeroed-record.
5. 3/3 byte-identical runs of every binary; sha256 comparison.
6. RESULT doc with per-step numbers, determinism evidence, the
   three binding caveats restated verbatim at the top, honest
   boundaries, and BUILD-PASS/BUILD-FAIL on the repair re-run only.
   No promotion claims.
