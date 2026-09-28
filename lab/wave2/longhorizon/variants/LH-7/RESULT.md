# LH-7 — Rapid-alternation interference (A/B every 4 episodes × 120 cycles) — RESULT

**Date:** 2026-09-19 · **Agent:** E2 (curriculum & interference) · **Apparatus:** R34 v3 continual learner, Linux port
**Evidence:** [EVIDENCE_20260919T221454Z](EVIDENCE_20260919T221454Z/) (`failures=0`, RECEIPT.txt)

## Config (as preregistered)

- 120 cycles × 4 episodes, regime = cycle mod 2 (starts A), updates ALWAYS on
  (learn=1, allow_switch=1, explore=1). Total: 480 train updates, one lineage, no restarts.
- Eval probes per regime every 10 cycles (cycles 9, 19, …, 119), 16 episodes each,
  updates DISABLED. B probe mirrors eval_B (learn=0, allow_switch=0); A probe mirrors
  the return_A gate (learn=0, allow_switch=1). Zero updates during probes asserted at
  every probe point.
- **Fresh documented seeds: learner 55223, world 353.**
- `r34_learner_core.zag` unmodified (md5 `cf823bedd7afe300ae3da382a9e78aab`, isolation=true).
- Interference rule (prereg): interference iff A endpoint >2 below its slow level (15/16 → ≤12)
  or B endpoint >2 below its slow level (16/16 → ≤13).

## Per-regime endpoint counts (E51 law: every probe reported separately)

| probe at cycle | updates | A pos/16 | B pos/16 |
|---------------:|--------:|---------:|---------:|
| 9 | 40 | 15 | 16 |
| 19 | 80 | 15 | 16 |
| 29 | 120 | 15 | 16 |
| 39 | 160 | 15 | 16 |
| 49 | 200 | 15 | 16 |
| 59 | 240 | 15 | 16 |
| 69 | 280 | 15 | 16 |
| 79 | 320 | 15 | 16 |
| 89 | 360 | 15 | 16 |
| 99 | 400 | 15 | 16 |
| 109 | 440 | 15 | 16 |
| 119 (endpoint) | 480 | **15** | **16** |

- A endpoint 15/16 = exactly the slow-protocol return_A gate level (no drop).
- B endpoint 16/16 = exactly the slow-protocol eval_B level (no drop).
- **Interference: none** (a_ok=1, b_ok=1). The preregistered hypothesis (rapid switching
  causes interference the slow protocol hides) is **rejected** — per-regime endpoints
  are indistinguishable from the slow protocol at every probe point.

## Cycle dynamics

- The learner re-settles onto the correct context within each 4-episode block:
  `switches` increments once per cycle, `active` matches the block regime at every
  probe landing (B-settled), and per-cycle train positives are 1–4/4 (the switch
  episode plus exploration noise — expected, not retention evidence).
- Endpoint state: `updates=480`, `contexts=3`, `switches=120`, fp=799333, pending=0.

## Method note: probe-order artifact found and fixed during the run

The first probe implementation probed A **before** B. Since probes land after B blocks,
probe A's `allow_switch=1` re-settled the learner onto A's context, and the B probe
(`allow_switch=0`) then measured B locked on the wrong context → 0/16 at all 12 probes
(a measurement artifact, not destroyed B knowledge — cycle data shows B re-settles
every block). Probe order was swapped to settled-regime-first (B, then A), which mirrors
both baselines fairly (eval_B from B-settled; return_A from B-settled). The swap is
evaluator-side only, within prereg ("eval probes per regime every 10 cycles" does not
fix order), and is documented here rather than hidden. The fixed order produced the
table above.

## Determinism & controls

- Two same-seed runs → byte-identical stdout (`determinism_same_seed=true`).
- Matched control: original R34 v3 campaign recompiled with the same compiler in this
  variant tree → `R34V3_FAILURES,0` (slow-protocol levels reproduced: return_A 15/16,
  eval_B 16/16).

## Hypothesis verdict

**Rejected (informatively).** Continued fitting under rapid alternation does not destroy
the other regime's knowledge. The 3-context switch mechanism is fast enough to re-settle
inside a 4-episode block, and per-regime endpoint retention is bit-identical to the
slow protocol at all 12 probe points across 480 updates. The 15/16 vs 16/16 asymmetry
on A is a property of the return transition itself (present in the slow baseline too),
not of alternation speed.

## Notes for Agent F

- Candidate robustness mechanism: context-local score tables + switch-on-unexplained-negative
  reward isolate regimes; rapid alternation never forces overwrites because a switch is
  cheaper than re-learning. Worth testing at what block size this breaks (block=1?).
- The probe-order artifact is a reusable lesson: in multi-regime probes with switch-enabled
  passes, always probe the settled regime first, or B-style measurements read lock-in,
  not knowledge loss.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results in this document come from a training run
with `explore_enabled=1`, which engaged the hidden seeded LCG (`r34v3_rng`,
`(rng*997+7919) mod 1000003`) inside `r34_learner_core.zag`, driving 1-in-5
pseudo-random explore flips in `r34v3_choose` — hidden randomness in the AI's
decision path, violating the no-randomness law. This leg: LH-7, rapid-alternation interference, updates always on with explore=1.
Verified by the r34 RNG probe (workstream 2/8), investigation commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The run is reproducible engineering evidence (byte-identical reruns hold) but
**not law-compliant evidence**. The stability verdict below stands recorded
but may not be cited as canonical — including the rapid-alternation interference results — until clean
reruns (deliberate or state-varying exploration, no LCG) reproduce it.
The original text above is left intact for the record.
