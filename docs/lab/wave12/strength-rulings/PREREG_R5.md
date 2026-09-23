# PREREG — Strength-trial Ruling 5: freeze-vs-retention treatments (wave12/strength-rulings)

**Status:** FROZEN 2026-09-20. This prereg is fixed before implementation.
Any change to the positions, tests, metrics, or favor-criteria below
requires a dated amendment. This experiment does NOT rule — it produces
the evidence each position needs. The final ruling is Micah's.
Micah's leaning (freeze = bug, P3's claim) is recorded and baked into
nothing.

**Context.** Three positions on the graded-strength store freeze
(protection with no cost, no expiry, no audit trail = de-facto
force-pin with no trainer behind it):
- **P1 — MEASURE:** Pressure-Tested Retention suite (PTR/EC/CT) computed
  from the audit ledger; reporting rule with teeth: EC < 0.5 → PTR
  reported as UNEVALUATED (a recorded failure-to-evaluate).
- **P2 — SCORE:** Effective Retention + hard tripwires: drops ≤
  2×capacity (S1: 64) else cell FAILED; churn-throughput floor
  (admitted/offered ≥ capacity/offered_total) else FAILED.
- **P3 — FIX:** uncertainty expiry (protection lapses to BASELINE after
  K episodes without fresh cited evidence; K=50 at S1) + protection
  budget (≥1 of 2 churn-demand victims from the strongest-held half).
Standing recommendation: **P3 expiry + P2 tripwire + P1 metric,
skipping forced churn**. This experiment tests whether the evidence
supports that combination or favors a different one.

**Favor criteria (evidence only, not a ruling).** The supported
combination is the minimal set that: (1) DETECTS the freeze —
P1's UNEVALUATED and P2's FAILED must be evaluated for agreement on
the frozen config (V2 §5.4 requires the agreement matrix; disagreement
is a finding, not averaged away); (2) RESOLVES it without destroying
retention — the mechanism must complete churn evaluation while keeping
important-memory retention high; (3) adds no redundant treatment —
if a subset performs identically to the full combo, the evidence
favors the subset. Forced churn (the skipped option) is tested as a
comparator so "skipping" it is an evidenced choice, not an
assumption. Report the agreement matrix and the mechanism comparison;
do not rule.

## Tests

### E1 — treatment agreement matrix (reproduction, real VUP cells)
VUP curriculum, S1 (32 slots, 500 episodes), arms **B** (control),
**C** (graded, freeze-prone), **C-P3** (graded + P3), variants 0/1/2,
each cell ×2 runs, byte-identical. Implementation: unmodified copies
of the wave-8 trial sources built fresh (`r5/trial/`); the P1/P2/P3
verdicts are computed by the analysis script from the cells'
`ST_METRIC`/`ST_DROPS` lines (deterministic arithmetic on committed
outputs — analysis is not a mechanism change).
Per config × variant:
- P1: PTR (tag 8), EC (tag 9), CT (tag 10); verdict UNEVALUATED iff
  EC < 0.5 (else report PTR/EC numerically).
- P2: ER (tag 11), drops vs ceiling 64 → FAILED/PASS per cell;
  churn-throughput floor: admitted/500 ≥ 32/500 → PASS/FAIL.
- P3 (C-P3 only): protection-expiry count (audited `PEXPIRED`
  entries), expiries that enabled a kill (BASELINE-path kills of
  expired slots), `ck_no_permanent_lock` invariant status.
Agreement matrix (the required output): for C and C-P3, does P1 say
UNEVALUATED/frozen exactly where P2 says FAILED? Does C-P3 resolve
either flag relative to C? Where P1/P2/P3 disagree, report the
disagreement verbatim.

### E2 — P3 mechanism efficacy with citations available (scripted)
Counterfactual mechanism test (stated explicitly: VUP provides no
contradiction citations, so this isolates the mechanism from the
scenario). `r5_treatments.zag`, deterministic, ×2 runs:
- 32-slot store, stage FULL, 2 CORE slots. Fill 30 graded memories:
  strengths cycle {10, 40, 75} (learner-declared scale) with every
  10th trainer-declared to 80; values = deterministic ids.
- 5 churn demands at episodes {100,200,300,400,500}, 2 slots each.
  Victim policy mirrors the learner: lowest strength first, ties →
  lowest slot; graded configs pay effort or `st_abandon`.
- Configs: **FROZEN** (p3 off) vs **P3** (`st_set_p3(1,50)` +
  maintenance rule: re-cite slots expiring within 25 episodes when a
  fresh episode exists + `st_protection_expired` issuance).
- `cites=1`: the harness issues up to 4 fresh contradiction citations
  per victim attempt (fresh deterministic cite episodes) + JUSTIFY.
- Metrics: demands completed (both slots freed), kills
  (full-effort vs BASELINE path), abandons, important retained
  (strength ≥75 or trainer-80 alive at end / offered), evidence cites
  issued per kill, audit_n, fingerprint.
Question: when its precondition (available citations) holds, does P3
reduce the evidence cost of churn / complete demands the frozen
config abandons, without killing anything itself?

### E3 — forced-churn comparator (scripted, the skipped option)
Same harness as E2 with `cites=0` (the VUP reality: no contradiction
evidence). Configs: **FROZEN** vs **P3** vs **FORCED**:
- **FORCED:** at each demand, kill the lowest-score eligible slot via
  the uniform `st_kill` (strength-blind; audited as `KILL`, visibly
  distinct from `KILL_EVIDENCED`). Non-CORE, non-force-pinned only.
- Metrics: same as E2, plus retention cost (important memories lost
  to forced kills) and ER-equivalent (important retained / important
  offered).
Question: does forced churn resolve the freeze, and at what retention
price vs P3's evaluation-not-killing approach? This makes "skipping
forced churn" an evidenced comparison.

## Standing checks (all experiments)
Zero RNG in decision paths (static grep); byte-identical reruns;
`st_replay_check` + `st_refusals_clean` + `ck_verify` clean on every
cell (E1) and every scripted run (E2/E3); bare `@import`.

## What this does NOT test
The implant/wrong/designation defects (R3 / other workstreams); the
overwrite question (R4); S10/S100 legs; tuning of K or the 25-divisor
(mechanisms, not constants, per V2 §11).

## Outputs
`r5/trial/` (unmodified wave-8 trial copies + `r5_treatments.zag`),
`r5/evidence/` (E1 cell logs ×2 + determinism diffs + agreement-matrix
table; E2/E3 per-config logs ×2), `SUMMARY_R5.md` (agreement matrix,
mechanism comparison, which combination the evidence supports, no
ruling).
