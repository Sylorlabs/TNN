# TRIAL RESULTS — lifecycle-as-advisor

**Date:** 2026-09-19/20 · **Prereg:** `PREREG.md` (written before any run)
**Design:** `ADVISORY_DESIGN.md`
**Implementation:** `trial/adv_trial.zag` + `trial/adv_advisor.zag` (+ `trial/memory_core.zag` extended with `MA_OP_ADVISE` / `ma_kill_advised`)
**Runner:** `trial/run_adv.sh` · **Evidence:** `trial/EVIDENCE_ADV_20260920T002110Z/` (+ gate evidence in the same bundle)
**Gate white-box:** `trial/adv_gate_test.zag` — 8/8 checks pass.

## Verdict: MIXED

Per the prereg: POSITIVE required ADVICE strictly greater than NO-ADVICE in
all 6 cells with acceptance in (5%, 95%); NEGATIVE required zero advice wins
or acceptance outside that band (≤5% = never trusted; ≥95% = automaticity
smuggled back). Observed: **advice wins 2, loses 0, ties 4**, acceptance
**59%** (98 accept / 66 reject — genuinely weighed, neither rubber-stamped
nor ignored). All 19 structural CL_CHECKs pass. So: the advisory interface
works as designed (advice is real, weighed, and structurally gated), and it
helps decisively in 2 of 6 designed cells while never hurting — but it does
not clear the all-6 bar.

## Results (held-important / admitted-important, per cell)

| cell | design | NO-ADVICE | ADVICE | winner | acc/rej | w_end |
|---|---|---|---|---|---|---|
| v0 | standard base | 30/37 (81%) | 30/37 (81%) | tie | 14/14 | 16 |
| v1 | standard + bursty importance | 0/0 | 30/32 (93%) | **ADVICE** | 21/11 | 0 |
| v2 | standard + late drift | 30/37 (81%) | 30/37 (81%) | tie | 14/14 | 16 |
| v3 | adversarial base | 30/35 (85%) | 30/35 (85%) | tie | 18/8 | 8 |
| v4 | adversarial trap-deep | 9/9 (100%) | 30/33 (90%) | **ADVICE** | 18/6 | 41 |
| v5 | early-honest → trap flip | 30/35 (85%) | 30/35 (85%) | tie | 13/13 | 8 |

Tally: wins_adv=2, wins_noadv=0, ties=4. Acceptance 98/(98+66) = 59%.

Per-quartile cohorts (E51AJ law — the v4 row is why: NO-ADVICE's "100%"
is 9 admitted vs ADVICE's 30 held of 33):

- v1: NO-ADVICE admitted **zero** important memories in any quartile
  (0/0, 0/0, 0/0, 0/0); ADVICE 12/12, 16/18, 2/2, 0/0.
- v4: NO-ADVICE 9/9 all in quartile 0; ADVICE 28/31, 2/2, 0/0, 0/0.
- v0/v2/v3/v5: both arms concentrate in quartiles 0–1, identical.

## Mechanism: where the advice helped and why

**v1 (burst) — advice defeats the frozen-value seal.** Declared values are
immutable after ADD (MEMORY_OPS law: judgment revised only by deliberate
acts). The policy's signed trust decayed during the first 50 all-unimportant
episodes, but the *stored* early memories kept their high ADD-time declared
values — so incoming burst-important memories could never *strictly beat*
the worst candidate and were dropped, all run, by the control arm (0
admitted). The advisor's estimator is *not* frozen: delayed credit keeps
updating its weights, so its signed suggestions for the stale stored
memories went negative (kill-lean), pulling their adjusted scores
`c = v + w·a` below the incoming memories'. The advisor is a second,
non-frozen signed signal — exactly the gap MA3's recommendation #2/#3
pointed at. Inferred from design + cohort pattern (q0–q2 admissions while
w>0, silence in q3 after w→0), flagged as inferred.

**v4 (trap-deep) — advice carries the signed evidence the policy was slow
to learn.** The trap (f0 3-vs-0 anti-correlated) fooled the policy's trust
into dropping 24 of 33 important memories; the estimator's signed weights
separated the trap feature and the policy, still trusting the advisor
(w_end=41, the highest), followed it 18/24 times to 30 held vs 9.

**Ties (v0/v2/v3/v5) — advice weighed but outcome-neutral.** Acceptance
~50% on these cells: the policy visibly accepted *and* rejected advice
(the interface is genuinely advisory), yet important-retention was
identical. The signed-trust policy already solves these; advice changed
*which* unimportant victims died without moving the primary metric. Note
v3: the adversarial base that beat MA3's agency 30-vs-11 is now a tie —
the signed declared values (MA3's own recommendation) closed that gap
before advice entered.

## Structural evidence (the anti-automaticity case)

- **Isolation:** `adv_advisor.zag` — zero imports, no `MaStore`/`ma_`
  references (runner grep passes). The advisor cannot name a slot.
- **Gated kill:** white-box gate test 8/8 — `ma_kill_advised` returns
  `REFUSED_NOADVISE` (109) with no token, with a wrong-slot token, and
  leaves state untouched on refusal; succeeds with a valid token; CORE
  stays `REFUSED_CORE` through the gated op.
- **Trial-level:** `adv_kills_gated` — 0 ungated kills across all advice
  arms (every kill immediately preceded by its ADVISE record);
  `noadv_no_advise` — control arm holds zero ADVISE records;
  `cell_valid` — CORE intact, pinned-while-pinned intact, ledger replay
  clean in all 6 cells; 19/19 CL_CHECKs pass.
- **Determinism:** variant-3 advice arm rerun fingerprint matches exactly
  (33500457 = 33500457) — the system is deterministic; the v5 regime flip
  is designed adversity, not noise. No RNG in system or harness (static
  check passes; curricula are closed-form).

## Honest negatives and flaws found

1. **The w-calibration metric diverges from decision value.** In v1 the
   advisory weight decayed to 0 (sign-agreement between advice and truth
   was poor) *even though* advice was decision-useful early — the policy
   stopped listening to a useful advisor. Sign-agreement is the wrong
   calibration target; ranking quality is what matters. Next iteration
   should calibrate w on ranking (e.g., did the advised victim rank below
   the admitted memory at revelation?), not sign.
2. **The estimator never visibly learns by absolute error.**
   Mean |err| first-60 vs last-60 revelations: 46→46, 47→47, 46→46,
   45→45, 40→40, 47→47 — flat everywhere, yet advice helped in v1/v4.
   The value is in *relative ranking*, not absolute prediction. The
   lifecycle-v1 absolute predictor may be the wrong substrate shape for an
   advisor; a rank-native advisor is worth designing.
3. **Advice never hurt here, but the win is narrow (2/6).** Per the prereg
   this is MIXED, not a confirmation. The honest read: advisory future-use
   is a real, structurally-safe second signal that rescues specific
   failure modes (frozen-value seal, slow trap learning) — not a general
   retention upgrade.

## Scale dimension (program law)

Trial scale 32 slots / 500 episodes (MA3-comparable). Per-episode cost is
O(CAP) victim scan + O(CAP·feats) advice scan — no pairwise/N×N
structures; the interface adds a constant factor to work the policy
already does. **Next scale test (explicit, not run):** one 320-slot /
5000-episode cell on v3 to verify wall-clock linearity and ledger sizing
(audit cap must grow with horizon: 4096 entries here, ~400k at 100x). If
per-episode cost deviates from linear, the scale claim is falsified.

## Next step

Redesign the advisor around **ranking, not absolute prediction**, and fix
w-calibration to reward ranking quality at revelation — then rerun the
same 6 cells. The structural interface (isolation + ADVISE records +
gated kill) held; what needs work is the *content* of the advice, not the
joint. If the rank-native advisor still can't beat 2/6, kill the
future-use-as-advisor direction and spend the budget on the deliberate
re-evaluation policy instead.
