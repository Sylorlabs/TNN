# Arm-3 Variation C — Verdict

**Date:** 2026-09-21. **Teacher:** `teacher.zag` (engagement-meter, teacher_id=3).
**Bar:** arm-3 criterion (3) "shows adaptive judgment" (PREREG_FREEZE.md §4 B.1).

## Verdict: PASS

The rebuilt teacher satisfies the bar the fixture failed: a
history-conditioned proposal policy `(spec, stimulus, history) → proposal`
exists **in the teacher**, not in the driver script.

### What was demonstrated

1. **The mapping lives in the teacher.** The driver (`verify/session.py`)
   only appends bytes: it writes the teacher's emitted proposal into the
   history, appends a scripted student decision, and re-invokes the teacher.
   No proposal content, span, kind, confidence, or grounding is chosen outside
   `teacher.zag`. Proven by `selfcheck` mode: every recorded proposal across
   4 scripted sessions (12, 6, 14, and 64 proposals) is byte-identical to the
   teacher's re-derivation from the tape prefix. A forged proposal is caught
   (exit 21).
2. **Adaptive judgment, history-conditioned.** The engagement meter E folds
   the decision tape (ADOPT +120 / REVISE +60 / DEFER +10 / REJECT −150 /
   per-proposal decay −20 / double-reject −200, clamped [0,1000]) and the
   emission decision reads E's band:
   - cold (E<300): low-confidence probes (60–100), WORD_SPAN only, fresh regions;
   - warm: appeals of R1/R2/R5-rejected spans with **new grounding**
     (observed: span 51151–51157 re-proposed with a fresh grounding span
     after an R1 reject; budgets enforced — max 2 appeals, dead after
     2 final rejects);
   - hot (E≥700): SAME_AS / BOUNDARY / GROUP relational proposals over
     adopted units (observed kinds 2, 3, 4 in the 64-proposal session),
     confidence 180–220, never 255;
   - two consecutive REJECTs at any E: RETRACT of the most recent
     un-decided proposal + cursor jump + E −= 200 (observed: kind-5
     retract of seq 2 after REJECT,REJECT with deferred proposals pending).
3. **History sensitivity on identical stimulus** (slice S0, session seeds
   differ only in the decision script):
   - all-ADOPT ×14: E 0→1000, hot band from proposal ~8, relational
     proposals, next-proposal confidence 203;
   - all-REJECT ×12: E pinned at 0 throughout, WORD_SPAN cold probes only
     (confidence 60–100), next-proposal confidence 60.
   Same stimulus, opposite histories → opposite teaching behavior.
4. **E is a pure function of the tape.** Teacher `trace` mode vs an
   independent Python reference implementation of §2: equal at every event
   (24/12/28/24 events across sessions).
5. **Determinism.** N=5 byte-identical on a fixed history; 5/5
   byte-identical under adversarial heap perturbations (`MALLOC_PERTURB_`
   ∈ {0,1,165,90,213}).
6. **§P iron rules preserved exactly.** 19 hostile histories → exact exits
   (1,2,3,4,5,6,8,9,10 per SPEC.md §6), logged on fd 2, zero stdout bytes.
7. **§C kept conservative.** Cumulative monitor: smuggle tiling fires
   (code 1), single conf-255 >5% dump fires immediately (code 2), clean
   all-ADOPT teaching never fires, no-255 high-coverage stream never fires.
8. **No flaw manifest** (T-7): honest vocabulary spans only, E-scaled
   confidence, evidence grounding. Thesis holds: spans only, no commands,
   no token ids.

### Honest caveats

- The "student decisions" are scripted verdicts, not a live learner. That is
  the specified interface (B.5: the teacher reads decisions as history), and
  the script chooses only verdicts — never proposals — but end-to-end
  adaptivity against the real harness student is not demonstrated here.
- The within-band confidence mapping (`E mod 41` etc.) is deterministic but
  stipulated, not derived — the "judgment" demonstrated is the E-meter's
  band/appeal/retract/relational behavior, which is the mechanism under test.
- §C monitor is cumulative over the session, not the frozen rolling-200
  window — strictly more conservative; documented deviation, parked for Micah
  (same deviation as the arm-3 fixture verdict).
- Appeal "new grounding" uses neighboring word spans when pattern
  occurrences are exhausted — new evidence spans, but weaker than fresh
  occurrences; disclosed in SPEC.md §3.2.
- Session cap of 64 proposals is a teacher-side termination bound; the
  per-proposal termination bound itself lives with the student (B.5).

### Kill-criteria check

No kill criteria were set against this variation beyond the bar itself;
nothing was bent: the frozen §P wire format, iron rules, exit codes, and the
§C tripwire are preserved exactly, and the prereg's negative declarations
(no RNG, no wallclock, no learning machinery, fixed-size session state) are
met and auditor-verifiable from `teacher.zag` + `SPEC.md`.
