# LH-5 — Reward-corruption ramp (credit robustness): RESULT

**Agent:** E3 · **Date:** 2026-09-19 · **Branch:** `tnn-native-lab` (no push)
**Prereg:** `../PREREG.md` variant LH-5 · **Apparatus:** R34 v3 continual learner, Linux port
**Evidence:** `EVIDENCE_20260919T221439Z/` (`failures=0`, `deterministic_runs_equal=true`)

## Protocol (as preregistered)

480-update runs under the LH-1 protocol: 10 × [train A(24) / eval A(16) /
train B(24) / eval B(16)], one lineage per corruption rate, corruption
0% / 10% / 25% / 50%. Seeded sign-flips of the delayed reward are applied
**before** `r34v3_accept`, on training accepts only (`learn==1`); eval
probes are uncorrupted, `learn=0`, `allow_switch=0`, `explore=0`.
Corruption RNG is a dedicated LCG in the harness (learner core untouched).

**Fresh documented seeds:** learner 5555 (all rates — matched lineages, so
differences are attributable to corruption only), world 51 (all rates),
corruption seeds 5600 / 5610 / 5625 / 5650 for 0/10/25/50%.
Flip check: flips/train_accepts = 0/0, 46/480, 124/480, 241/480 —
the corruption channel delivered the nominal rates (0%, 9.6%, 25.8%, 50.2%).

**New harness:** `toolchain/r34v3/lh5_corruption_harness.zag` (evaluator-side;
mirrors `r34_continuing_harness_v3.zag`). Isolation verified:
learner core byte-identical to toolchain original and import-clean
(`learner_core_unmodified=true`, `learner_core_isolation=true`).

## Per-block eval positives (E51: endpoint per regime, never aggregate-only)

`A/B` = eval positives /16 for regime A / regime B at each block end.
`X` marks a collapsed probe (0/16).

| block | 0% | 10% | 25% | 50% |
|---|---|---|---|---|
| 1 | 16/16 | 16/16 | 16/16 | 8/16 |
| 2 | 16/16 | 16/16 | 16/16 | **0**/16 |
| 3 | 16/16 | 16/16 | **0**/16 | **0**/16 |
| 4 | 16/16 | 16/16 | 16/**0** | **0**/16 |
| 5 | 16/16 | 16/**0** | 16/16 | **0**/**0** |
| 6 | 16/16 | 16/16 | 16/16 | **0**/**0** |
| 7 | 16/16 | 16/16 | 16/16 | **0**/16 |
| 8 | 16/16 | 16/16 | 16/16 | **0**/**0** |
| 9 | 16/16 | **0**/16 | **0**/16 | **0**/16 |
| 10 (endpoint) | **16/16** | **16/16** | **16/16** | **0**/16 |

Collapsed probes (of 20 per lineage): 0% → 0/20 · 10% → 2/20 ·
25% → 3/20 · 50% → 13/20.

## Endpoint eval positives vs corruption rate (the curve)

```
rate:    0%        10%       25%       50%
A:       16 ██████ 16 ██████ 16 ██████  0 ░░░░░░
B:       16 ██████ 16 ██████ 16 ██████ 16 ██████
collapsed probes: 0/20     2/20      3/20     13/20
```

**The knee is between 0% and 10%.** The preregistered hypothesis was
graceful degradation with a measurable knee. The data reject it: at 10%
corruption the learner already suffers total per-block policy collapses
(0/16 on a full eval probe), i.e. **the delayed-credit rule is fragile at
10%**, not merely degraded.

## Supplementary sensitivity (extra corruption seeds, same learner/world seeds)

- 10%, corr seed 7777: collapsed blocks 7-B and **10-B** → endpoint **B=0/16**.
- 10%, corr seed 4242: collapsed blocks 1-B, 2-B, 3-A, 4-A, 6-B, 8-A+B
  (7/20) → endpoint 16/16.
- 25%, corr seed 7777: collapsed blocks 3-A, 7-B, 8-A, **10-B** →
  endpoint **B=0/16**.

Collapse at 10% is not a one-seed fluke: 3/3 corruption seeds show 0/16
blocks, and 1/3 shows an endpoint regime collapse. Endpoint survival on the
primary 10%/25% lineages is seed luck, not robustness.

## Mechanism

Context switches (negative reward on a positively-scored cell, no
exploration → regime-change switch) per lineage:
0% → 19 · 10% → 91 · 25% → 149 · 50% → 181.
The score accumulator itself would degrade gracefully (expected net drift
per correct update = (1−2p)·100). The fragile part is the **switch rule**:
it treats every negative credit as a regime-change signal, so corrupted
sign flips inject spurious regime changes that destabilize the
latent-context structure. Collapses recover when subsequent training
rebuilds scores in the landed context (10%/25% transient blocks); at 50%
one regime is destroyed at endpoint (A=0/16 while B=16/16 — asymmetric).
Candidate mechanism note for Agent F: the switch trigger has no
corroboration requirement (single negative sample suffices).

## Gates / checks

- `train_updates == 480` in all 4 lineages (cl_check pass, exit 0).
- Determinism: two full-ramp runs byte-identical (`deterministic_runs_equal=true`).
- 0% lineage reproduces baseline-quality learning (20/20 probes 16/16),
  so the collapses are caused by corruption, not the 10× horizon.
- `LH5_FAILURES,0`; runner exit 0.

## Verdict

**LH-5 = fragility finding, reported exactly:** 10% reward corruption
already produces total (0/16) per-block policy collapses via spurious
context switches; 25% adds endpoint risk on some seeds; 50% destroys one
regime at endpoint. The delayed-credit update rule does not degrade
gracefully — the knee is at or below 10%.

---

# LH-6 — Scaled learner core (4×4): BLOCKED_ON_STABILITY

**Status: NOT BUILT. Blocked by the preregistered stability gate.**

Gate (PREREG.md, LH-6): "runs only if LH-1/LH-2 show stable learning."

What was checked (2026-09-19):
- `~/workspace/tnn-lab/wave2/longhorizon/variants/LH-1/RESULT.md` — **does not exist**.
- `~/workspace/tnn-lab/wave2/longhorizon/variants/LH-2/RESULT.md` — **does not exist**.
- The directory `~/workspace/tnn-lab/wave2/longhorizon/variants/` did not
  exist at all before this run (only LH-5 was created by this agent); a
  filesystem-wide search found **zero** `RESULT.md` files anywhere under
  `~/workspace/tnn-lab`.

Per the task instruction ("if the RESULT files don't exist yet, DO NOT
build LH-6"), no `r34v4_learner_core.zag` was created and no scaled run was
attempted. LH-6 remains blocked until sibling agents publish LH-1/LH-2
stability evidence; additionally, the LH-5 fragility finding above
(spurious-switch instability already at 10% corruption in the 2×2 learner)
is the kind of instability the gate exists to catch, and should be weighed
before any scale-up is approved.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results in this document come from a training run
with `explore_enabled=1`, which engaged the hidden seeded LCG (`r34v3_rng`,
`(rng*997+7919) mod 1000003`) inside `r34_learner_core.zag`, driving 1-in-5
pseudo-random explore flips in `r34v3_choose` — hidden randomness in the AI's
decision path, violating the no-randomness law. This leg: LH-5, 480-update runs under the LH-1 protocol, so training ran explore=1; the reward-sign flips were seeded harness-side.
Verified by the r34 RNG probe (workstream 2/8), investigation commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The run is reproducible engineering evidence (byte-identical reruns hold) but
**not law-compliant evidence**. The stability verdict below stands recorded
but may not be cited as canonical — including the noisy-reward fragility verdict (stable at 0% corruption, knee between 0% and 10%, regime switches exploding 19→181) — until clean
reruns (deliberate or state-varying exploration, no LCG) reproduce it.
The original text above is left intact for the record.
