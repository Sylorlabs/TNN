# Amendment summary — PREREG_TRUST_TIERS v1 → v2

**Dated 2026-09-20. Authorized by Micah (testing authorization, per the
trust-tiers council recommendations).** The 7 v1 §11 open questions are
resolved; all amendments below are law. Status changed DRAFT → ACTIVE.
Constants K=25, W=25, M=5, N=25, L=25 frozen. Zero RNG, byte-identical
paired reruns, independent checker, and the §8 kill criteria carry
forward unchanged (one dated amendment permitted, then retire).

1. **Tier order is law (§2).** T0 > T1 > T2 > T3 approved; the kill/revise
   gate (§5.1) requires the {T0, T1} leg. Fixed the dangerous fallback:
   the required leg never collapses to {T1} under any future ruling —
   that would legalize A5-style corruption (spoofed-T1 + one colluding
   T3 satisfying the gate).
2. **T0 boundary holds; measurement-only A0 cell added (§6).**
   T0-honest-by-construction stays law for the pass/fail battery (INVALID
   on T0 fabrication stands). New campaign A0, arm T only, 30-episode T0
   spoof: carved out from the INVALID rule, no REDESIGN/PROMOTION
   triggers — reports degradation taxonomy + loud-vs-silent
   classification only.
3. **Bounded freeze with decay + reset (§5.3, §7).** Freeze lapses after
   L = 25 episodes only if colluding sources haven't re-offended;
   re-fabrication resets the clock. On lapse the §5.1 gate still applies —
   the attack can resume only into refused citations, never a kill. §7's
   recovery metric repaired (episodes from attack end to first genuine
   citation processed normally; censored at run length if none occurs);
   new metric: freeze duty cycle per campaign.
4. **Re-trust: trainer law + probationary path (§5.4).**
   Trainer-mark-only FULL re-admission stands. Added learner-initiated
   probation: after N = 25 consecutive agreeing episodes (matching T0's
   reading), a distrusted channel returns as CITATION-LEG-ONLY — counts
   toward the ≥2-source leg, never the {T0,T1} leg — audited
   `REHABILITATED_PROBATION`. M = 5 consecutive disagreements re-distrusts
   PERMANENTLY (trainer-only after). New metric: quorum composition over
   time (REQUIRED vs SUPPORTING counted citations per phase) to catch
   channel-flapping games.
5. **S1 primary + conditional S10 stretch leg (§11).** S1 remains the
   primary campaign. Added reduced-matrix S10 leg: 5000 episodes, arms T
   and T-NC only, one variant per campaign, 1 campaign-per-type
   (2×6×1×1×2 = 24 executions), campaigns A1–A6 (A1-MS, A0 excluded).
   Runs only if S1 completes without INVALID. Own bar: no
   signature-level change vs S1 on any §8 bar, else BLOCKED (horizon
   effect, not a mechanism verdict); feeds no REDESIGN/PROMOTION/RETIRE.
6. **T-NC ablation kept (§3).** Decisive counterfactual at ~7 minutes of
   compute; gate-only scheme promoted if it passes everything T passes.
7. **A1 100% bar hardened (§4, §6, §8).** Scoped to arms T and T-NC —
   Arm B's expected A1/A1-MS/A3 failures are control signal, never a
   bar violation (checker must not fire REDESIGN on them). Added
   verified-status checker precondition: target memory checker-confirmed
   verified, age ≥ K = 25, before the attack window, else the cell is
   VOID. Added A1-MS: 5 distinct T3 sources fabricate simultaneously for
   30 episodes — the literal "no matter how many agree" test, same 100%
   bar on T/T-NC.

**Not carried by this task (flagged, not decided):** the council's Q1
suggestion of a broken-sensor measurement cell (T0 honestly-wrong vs
trainer correct) was not among the 7 authorized amendments; left as
open future work.
