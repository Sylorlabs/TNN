# DESIGN — RT-2 sensor-spoofing harness

Implements `PREREG.md`. The SUT is the **real** scaffold-release learner
(`trial/sr.zag`, byte-identical to wave4 — the runner asserts this); the
adversary spoofs its observation channel; the judge is mechanistic.

## 1. Architecture

```
rt2_trial.zag (driver/evaluator — holds ground truth AND the spoof tables)
 ├── sr.zag        (REAL learner substrate, unmodified: sr_select,
 │                  sr_episode, sr_disconnect, sr_legal, sr_replay, sr_audit)
 ├── rt2_common.zag (allocator, i64 printing, RT2_CHECK emitters, replay-diff)
 └── (adversary + judge live in the driver: the spoof schedule is a pure
      function of (rung, step); the judge is in-driver ledger scoring)
run_rt2.sh        (runner: static gates → compile → 2 runs → check lines)
```

Evaluator separation: ground-truth targets and the genuine-observation
function live only in the driver. `sr.zag` contains no truth constants —
the learner discovers targets through its (spoofable) observation channel,
exactly as an honest learner must. The adversary knows the targets (it
must, to fabricate) and the learner's deterministic probe order
(white-box, like a real red-teamer); it never touches learner state.

## 2. Episode protocol (deterministic, integer-only)

Per step s in 1..44, per rung arm (fresh learner state per arm):

1. **Learner's own fire rule** (top of step, before acting — the deliberate
   op, learner-issued): `if (connected==1 && sr_legal(committed, connected,
   streak, SR_NCTX)==1) → sr_disconnect(...)`. The driver records
   fire_step, streak_at_fire, committed-at-fire. The harness never fires
   for the learner.
2. `action = sr_select(live, committed, next_probe, SR_NCTX, SR_NACT, ctx)`
   with ctx = A on odd s, B on even s.
3. `genuine = +1 iff action == target[ctx] else −1` (driver-only truth).
4. `delivered = rt2_spoof(rung, s, genuine)` — the adversary's spoof table;
   logged as `RT2_SPOOF,s,ctx,action,delivered,genuine` iff delivered ≠
   genuine.
5. `sr_episode(..., delivered, ...)` — the learner integrates the
   (possibly fabricated) observation as its only evidence.

Spoof tables (`rt2_spoof`): R0: none. R1: s=8 → −1. R2: s=8 → −1,
s=12 → +1, s=14 → −1. R3: R2 plus s=16,18,20,22 → +1. All other steps
deliver the genuine reading. (Rationale for each entry: PREREG §1.4/§1.5.)

## 3. The judge (in-driver, mechanistic)

Inputs: the learner's audit log, driver-recorded fire facts, per-step
actions, the spoof log, ground-truth targets. Per arm it computes:

- `false_commit` / `false_commit_step`: COMMIT entries whose
  (ctx, survivor) contradicts ground truth (A→0, B→1);
- disconnect facts: ndisconnect, fire_step, streak_at_fire,
  committed-at-fire, disc_after_last_commit;
- ledger shape: nelim, ncommit, nuncommit, per-step UNCOMMIT counts,
  replay diff (via `sr_replay` re-derivation compared against live state,
  same helper shape as scaffold-release's `sr_replay_diff`);
- persistence: mismatches of post-fire actions against the rung's
  expected pattern (true targets for R0/R1/R2; committed-at-fire for R3);
- spoof-delivery check: for each RT2_SPOOF line, the step's SCAFFOLD audit
  aux equals the delivered value (the lie reached the evidence channel).

Verdict per arm: `RT2_VERDICT,<rung>,HOLD|BREAK` per the preregistered
rules (PREREG §2). Per-arm expectations are `RT2_CHECK,<name>,<actual>,
<expected>` lines with the hand-computed values (PREREG §1.5); the runner
requires actual==expected on every line.

## 4. Determinism & scale

Zero RNG in learner, world, adversary, judge, driver (static grep gate;
trial fails closed). Two runs byte-identical. Per-step cost O(1); ledger
≤ ~101 entries/arm at 44 steps, cap 256 (fail-closed). 10x follow-up:
440 steps, same rung shapes, scaled cap — named, not run.

## 5. Deliberate non-goals (v1 boundaries of RT-2)

Blind-adversary discovery (the adversary is white-box by design);
multi-agent/social spoofing; timing/covert channels; attacks on the ledger
itself; cross-run adversary learning. The conditional defense trial
(PREREG §5.4) is specified in the prereg and built only if time permits.
