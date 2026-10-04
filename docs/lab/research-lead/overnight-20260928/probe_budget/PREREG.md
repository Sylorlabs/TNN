# PREREG: Experience-Set Probe Budgets (PBUDGET)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/probe_budget/` only.
Worker: Probe Budget Worker (subagent, 2026-10-02).
Parent mandate: test EXPERIENCE-SET probe budgets (learner manages its
own probe budget).

## 1. What is being tested

LEARNER-PROBE-COMPLETE proved the learner can choose WHICH inputs to
probe from an open pool. Its disclosed boundary: "Not claimed:
experience-set probe budgets". Open question: when probes are
expensive and the budget is LIMITED, can the learner allocate probes
wisely across time: spend nothing on redundant stretches, concentrate
spend on informative moments (here: a regime drift window), detect the
drift within budget, and respect a hard cap even when it wants more?

## 2. Frozen world data

Stream of T=30 steps, t=0..29.

Free surface signal s(t), visible to the learner at zero cost:
- t<15: s(t) = 100 + 2*(t%3). Values: 100,102,104 repeating.
- t>=15: s(t) = 200 + 40*((t*5+1)%3). Values: 240,200,280 repeating.
  Regime drift at t=15 to a high volatility regime.

Full frozen s(t) table:
t:   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14
s: 100 102 104 100 102 104 100 102 104 100 102 104 100 102 104
t:  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29
s: 240 200 280 240 200 280 240 200 280 240 200 280 240 200 280

Hidden information value info(t), revealed ONLY when the learner
spends a probe on step t:
- info(t) = 10 for t in {15,16,17,18,19} (drift window).
- info(t) = 1 otherwise.

Evaluator-side naive baseline (no learner involvement): uniform probe
indices {0,6,12,18,24}. Captures info(0)+info(6)+info(12)+info(18)+
info(24) = 1+1+1+10+1 = 14.

## 3. Frozen learner mechanism (disclosed, generic)

Learner state (u8 buffer, 32 bytes): pred (i32, init 100), mean
(i32 surprise EMA, init 0), budget (i32, init 5), captured (i32),
probes (i32), drift_probes (i32), refused (i32).

Per step, the learner observes s(t) for free:
- surp = |s(t) - pred|.
- mean update (sign safe, no negative division):
  if surp >= mean: mean = mean + (surp-mean)/32
  else: mean = mean - (mean-surp)/32.
- gate = 5 + 2*mean.
- If surp > gate and budget > 0: spend probe. budget--, probes++,
  pred = s(t) (snap), captured += info(t) (resolved by the driver
  from the world AFTER the spend decision).
- If surp > gate and budget == 0: refused++ (the cap binds; the
  learner wanted a probe it could not afford), then the free EMA
  update below still applies.
- Otherwise, and after a refusal: free EMA update (sign safe):
  if s(t) >= pred: pred = pred + (s(t)-pred)/4
  else: pred = pred - ((pred-s(t))/4).

The learner knows nothing of the drift step, the info values, or the
baseline. Constants (5, 2, 1/32, 1/4, init pred 100) are generic
novelty gating constants, not fitted to t=15. No modes, no bridges,
no handlers. Observation is always free; only the probe reveal costs
budget.

Hand-derived expectation (disclosed, NOT a kill bar): probes spent at
t=15,16,17,18,19; captured=50; drift_probes=5; refused=6;
budget_left=0; baseline=14.

## 4. Frozen kill bars

KB1 budget respected and binding: probes_used <= 5 AND refused >= 1.
KB2 informative probes under constraint: captured >= 40.
KB3 drift detected within budget: drift_probes (probes with
15 <= t <= 19) >= 4.
KB4 beats naive allocation: captured >= 2 * baseline (baseline=14,
so captured >= 28).
KB5 determinism: 3 full binary runs produce byte identical stdout
(sha256 equal, shell verified).

Verdict rule: KB1..KB5 all pass gives PROBE-BUDGET-COMPLETE. Any bar
fails: the verdict names the failed bar, no completion claim. A
forbidden interpreter invocation at any point is PROCESS-FAIL and the
wave result stays exploratory.

## 5. Build and run plan (post prereg)

Single file src/probe_budget.zag (world + learner + driver +
single raw syscall flush). Build: `znc src/probe_budget.zag -o
bin/probe_budget`. Run 3x to runs/run1.txt, runs/run2.txt,
runs/run3.txt. sha256sum compare. Write REPORT.md. Commit with
explicit pathspecs.
