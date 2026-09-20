# EXP-1 C7 Deep-Dive Verification Report — Three Claims

Date: 2026-09-20. Status: COMPLETE.
Task: independently verify the deep-dive's three claims against committed
evidence (S10 redesign ledger). Do NOT adopt; do NOT run S100.

## Sources (all committed, read-only)

- `wave9/integration/C7_DEEPDIVE_WITHDRAWAL_2026-09-20.md` — the deep-dive
- `wave9/integration/RESCORE_C7_CHECKER_2026-09-20.md` — independent checker
- `wave9/integration/RESCORE_C7_DRAFT_METRIC_2026-09-20.md` — exploratory re-score
- `wave9/integration/DRAFT_AMENDMENT_2026-09-20-C7-METRIC-REDESIGN.md` — WITHDRAWN draft
- `wave9/integration/evidence_s10_c5redesign/c7.telemetry` — committed S10 redesign
- `wave9/integration/evidence_s10_repair/controls.log` — committed baseline

## Claim (a): Displacement — CONFIRMED

**Claim:** 17 forced hypotheses displaced 17 proactive 1:1 in DC-4
(proactive 639→622).

**Committed numbers:**
- Redesigned DC-4: `C7_TELEMETRY … cap4,914` (evidence_s10_c5redesign/c7.telemetry)
- Components (rescore table): DC-4 = (cok 256, ccon 2, mhyp 639, lopen 17)
  → 256+2+639+17 = 914. ✓ matches committed cap4.
- Baseline DC-4: `C7_TELEMETRY … cap4,897` (evidence_s10_repair/controls.log)
  → 256+2+639+0 = 897. forced=0, elected=0 → proactive=639.

**Derivation:**
- Redesigned DC-4: forced=17 (checker: 17/17/17/0, 51/51 complete chains).
  elected=0 in DC-4 (checker: 12 elected are in DC-2, n=0 force_abstain path).
  proactive = mhyp − forced − elected = 639 − 17 − 0 = **622**.
  (Checker independently measured proactive opens: 610/622/622/639 for
  DC-2/3/4/5 — DC-4=622 matches.)
- Baseline DC-4: proactive = 639 − 0 − 0 = **639**.

**Displacement:** 639 → 622 = **−17**, exactly the 17 forced. 1:1 confirmed.

**Structural (source-verified in prior work):** o2_cap=640, guard
`next_cid < o2_cap`; proactive (loop.zag:82), forced (loop.zag:161), and
elected (loop.zag:177) opens all draw from the same cid budget and all
increment `met.hypotheses`. The budget binds (mhyp=639=o2_cap−1 in all stages).

**Gap flagged honestly:** The proactive count (622) is not in a committed
log file as a direct field. It is (1) independently measured by the checker
via print-only instrumentation on a byte-identical binary, and (2) derived
arithmetically from committed components (639−17−0). The committed
c7.telemetry carries only aggregate caps. The component breakdown is in the
committed rescore document (which cites the committed ledger).

**Verdict: CONFIRMED.**

## Claim (b): Double-counting — CONFIRMED

**Claim:** Old metric sums met.hypotheses (639 incl. forced) + tr.l1_opened (17);
L1 hypotheses counted twice.

**Structural (source-verified):**
- `met.hypotheses` incremented at THREE sites (loop.zag:82 proactive,
  :161 forced, :177 elected) → includes all L1 opens.
- `tr.l1_opened` incremented at ONE site (seam.zag:409, in seam4_abstain on
  success) → forced_ok + elected_ok.
- Therefore cap_old = cok + ccon + proactive + 2×(forced+elected).
  L1 hypotheses are double-counted by construction.

**Numeric (DC-4):** 256 + 2 + 639 + 17 = 914 (committed).
The 639 includes the 17 forced; the 17 are added again via tr.l1_opened.

**Predates redesign:** Baseline DC-2 had 12 elected abstains (checker
confirmed), so 12 L1 hypotheses were double-counted in the repaired baseline
too. The bug was symmetric until the gate fired asymmetrically.

**Verdict: CONFIRMED.**

## Claim (c): Incoherence — CONFIRMED

**Claim:** The draft's literal prose reading gives DC-4=880, not the assumed 897.

**Draft prose (DRAFT §3, exact quote):**
> `cap = composites_ok + commits_constr + hypotheses_autonomy`, where
> `hypotheses_autonomy = proactive O2 hypotheses + elected L1 abstain-hypotheses`.

**Literal application (DC-4):**
- proactive = 622 (verified above), elected = 0
- hypotheses_autonomy = 622 + 0 = 622
- cap = 256 + 2 + 622 = **880**

**Draft's expected re-score (DRAFT §3):** DC-4 = 914 − 17 = **897**.

**880 ≠ 897.** The prose formula and the expected re-score disagree.

**Root cause:** The draft (like the rescore §1, like the stale code comment
at loop_capability) assumed `met.hypotheses` is proactive-only. It is not
(Claim b). The subtraction reading (914−17) keeps the 17 forced inside the
639 and only removes the double-count; the literal reading (622) removes
them from the autonomy count entirely. These are different operations with
different results.

**Consequence noted in deep-dive:** Under the literal reading, DC-4=880 vs
DC-5=897 → 897→880, bar `==` FAILS in the cap5>cap4 direction (opposite of
teacher-dependence). Under the subtraction reading, 897→897 ALIVE.

**Verdict: CONFIRMED.**

## Overall

All three deep-dive claims independently verified. The draft was correctly
withdrawn. §5 FAIL stands. S100 stays gated. No metric patching.

**No-teacher-dependence evidence (committed, stands):**
- DC-5 autonomy (639 proactive) = baseline DC-5 (639).
- Positive control convicts (897→641, composites-only collapse).
- Real gate cost: ~17 proactive hypotheses crowded out per firing stage
  (telemetry, not a bar failure).
