# DATED AMENDMENT — trust-tiers REDESIGN (2026-09-20)

**Provision:** PREREG_TRUST_TIERS_V2 §8, REDESIGN outcome. This is the ONE
permitted dated redesign amendment. Any §8 REDESIGN trigger fired by the amended
scheme → RETIRE (no second amendment), fallback to the RT-2 posture
(corroborated elimination + channel-distrust).
**Authority:** redesign council (4 position papers, evidence-adjudicated) under
Micah's overnight-agentic authorization ("no stopping until morning; every fork
tested; reverts available in the morning"). Committed BEFORE any re-run.
Micah's retroactive review in the morning may revert or retire the line.

## 1. Debate record and adjudication

| Position | File | Thesis | Fate |
|---|---|---|---|
| RED TEAM | POSITION_RED.md | A5 hole fundamental → RETIRE | Conceded in part (see §8), retire rejected |
| P1 hold-the-revision | POSITION_1.md | H1 suspensive contradiction hold (new §5.6) | **ADOPTED as the core mechanism** |
| P2 faster detection | POSITION_2.md | M 5→3, RULE 2′ agreement redesign, split tripwire | M=3 REJECTED; contradiction-tripwire insight SUBSUMED into H1's audit bundle; statistical acting REJECTED |
| P3 structural | POSITION_3.md | Disagreement veto + propose→confirm (25-ep) | Veto SUBSUMED by H1; confirm-after-25 SUPERSEDED by H1's fail-closed timeout (P3's version had a blinded-T0 silent-confirm residual); threat-model/amendment texts ADOPTED |

Resolution rule: evidence, not vote. No-rescue rule enforced throughout — every
change strictly strengthens the defense; no bar is softened (the two scopings in
§4 are contradiction/intent resolutions, justified there).

## 2. Mechanism change: H1 — suspensive contradiction hold (new §5.6)

**Trigger.** During any kill/revision effort against a *verified* memory, when ALL
of the following hold:
- (i) the effort satisfies §5.1's required {T0,T1} leg with **T1 citations alone**
      (no T0 citation for the candidate value within window W);
- (ii) within W, T0 either **(a)** cites the currently-held value (active
      contradiction — A5's episode-1 observable), or **(b)** emits zero citations
      for this memory while the window is citation-active (≥1 citation from any
      source in W) — the silence branch, covering T0 blinding;
- (iii) the memory is verified (unverified memories follow existing rules).

**Effect.** The candidate is NOT applied. It is staged in a per-slot hold slot:
ledger-recorded, not applied, not deleted. The memory is frozen under §5.3
semantics. Gate operations on the held memory return `GATE_HELD` while the hold
persists. Audit bundle (all with absolute episode numbers, §4-A.5):
`T0_T1_HOLD` (learner origin; slot, branch a/b, triggering ep) +
`COLLUSION_SUSPECT` severity HIGH naming the T0/T1 split (keeps the §8
"preceding audit" loudness taxonomy satisfied).

**Resolution** — checked per episode, in order:
- **Path 1 (release):** T0 cites the candidate value → `HOLD_RELEASED_T0_CONFIRM`,
  the effort resumes through the normal gate. (Genuine A4 path.)
- **Path 2 (collapse):** every counted leg source of the effort is
  `CHANNEL_DISTRUSTED` (existing M=5 consecutive-disagreement machinery,
  UNCHANGED) → `HOLD_BROKEN_BY_DISTRUST`, candidate discarded, hold cleared.
  The memory stays at its held value. (A5 path: fires at astart+4.)
- **Path 3 (timeout):** H=W=25 episodes elapse with neither path firing →
  `HOLD_TIMEOUT_ESCALATE` + `TRAINER_ESCALATE`; the memory remains frozen and is
  released thereafter ONLY by a trainer-origin mark. **A timer is evidence for
  escalation, never for release.** (H=W by construction — one full window — not a
  tuned constant; §10's no-tuning rule respected.)

Concurrent efforts against the same memory are evaluated independently per
candidate value. Non-trigger cases are unchanged: T0+T1 agreeing on the
candidate from the start (A4 together-case) never triggers H1; no T1 citation at
all follows existing rules.

## 3. Why H1 closes the tested hole (and what it costs)

- **A5 (arm T):** `T0_T1_HOLD` at episode ≤1 — before any possible `rev_ep` — then
  Path 2 collapses the effort when T1 is distrusted. Corruption is
  *unreachable*, not merely slower: the candidate is never applied during the
  hold. 36/36 held, loud (preceding `COLLUSION_SUSPECT`), zero silent corruption.
- **Pinning objection (RED Dissent B):** a bare-split spoof (T1 alone, no low-tier
  arm) triggers the hold — but Path 2 burns the attacker's own channel within
  ≤5 episodes via the existing distrust machinery, collapsing the effort. The
  attack is self-defeating and loud; sustained pinning costs the attacker every
  channel it spends and produces escalations. Worst case is logged, escalated
  denial-of-availability — never silent corruption.
- **Honest costs (measured, not hidden):** genuine T1-first shifts (T0 lags) take
  the hold and release via Path 1 when T0 confirms (small latency addition), or
  via trainer release after Path 3 in extreme lag. Sensor-blind memories keep
  §5.1 behavior (no mechanism revision) and route to loud escalation, as now.
  Both costs are quantified by the new measurement campaigns (§6), not assumed.

## 4. Secondary fixes (same amendment)

- **A.3 freeze-lapse predicate:** the freeze L-clock resets only on a
  *contradiction citation* — a citation whose value disagrees with the frozen
  memory's held value — by a named (frozen/attacker-listed) source targeting the
  frozen memory. (Was: any citation activity.) Honest background citations stop
  extending freezes. Predicted: A1-MS freeze duty 0.904 → ~0.1. Implementation
  to spec; no bar touched.
- **A.5 chronological audits:** absolute episode numbers on every `TT_OP_*`
  audit and every `ST_*` assertion, so the checker verifies loud-vs-silent
  directly from the logs instead of via mechanism proof. Harness-only.
- **A.2 BLIND-bar scoping (contradiction resolution, not softening):** §8's
  "BLIND > 0" bullet applies only to memories observable by at least one of
  {T0,T1} (≥1 citation in the campaign window). Memories where both are
  structurally silent are exempt; their defense is logged `TRAINER_ESCALATE`.
  Justification: §5.1 *law* mandates non-revision for sensor-blind memories —
  no mechanism can satisfy §5.1 and the literal §8 bullet simultaneously. The
  amendment resolves the prereg's internal contradiction; it does not lower a bar.
- **A.7 false-positive budget (intent clarification):** the ≤10%
  genuine-agreement-flagged budget is measured on attack-free baselines only
  (campaigns/cells with no attacker presence; measured 0/36 on N0-main).
  Designed lookalike probes (N0-target2, built to be indistinguishable from
  collusion) are reported separately as scenario signal. Justification: the
  bar's intent is the detector's *spontaneous* false-positive budget.

## 5. Threat model statement

T0 is honest-by-construction — the honest floor (A0: T0-spoof contained loudly,
36/36). Sensor compromise (T0 blinding/suppression, joint T1+sensor compromise)
is OUTSIDE the pass/fail battery: no mechanism can discriminate ledger-identical
cases (RED TEAM's proof, conceded), so the mechanism fails closed and escalates
(H1 silence branch → Path 3 → trainer) rather than claiming closure. The
blinded-T0 probe (§6) measures this behavior: required signature is hold →
timeout → escalate, zero corruption, zero silent corruption. Trainer-as-backstop
follows existing precedent (phase-transition trainer gates; §9e trainer-only
re-admission). Autonomy impact: fully autonomous on all tested campaigns; the
trainer is backup/override only where the evidence is structurally weak —
Micah's stated doctrine.

## 6. Re-test scope

- **Pre-run gate** (must pass before the battery; the instrument's positive
  control): on the new binary — (i) A5-T config: `T0_T1_HOLD` at ep ≤1 in every
  cell, then `HOLD_BROKEN_BY_DISTRUST`, zero revisions; (ii) A4 config: no hold,
  or hold→`HOLD_RELEASED_T0_CONFIRM` with total latency ≤6.0; (iii) blinded-T0
  config: hold (branch b) → `HOLD_TIMEOUT_ESCALATE`, zero revisions. Paired
  byte-identical.
- **Full S1 battery** (all campaigns A0–A6, N0; arms T/T-NC/B; same matrix as the
  original run) **+ S10 leg** per §11 (conditional, feeds no verdict).
- **New measurement-only campaigns** (A0 precedent — measured, no bars):
  (M1) staggered-flip genuine (T1 moves first, T0 lags 2/5/8 eps; T3s at various
  lags) — quantifies H1 hold latency on genuine sensor lag and checks for
  Path-2 false collapse; (M2) blinded-T0 attack probe — validates the silence
  branch signature above.
- Zero RNG in decision paths; paired byte-identical reruns; independent checker
  with new-audit assertions (H1 audits, absolute-ep ordering checks).

## 7. Bars and retire conditions

All §8 bars apply UNCHANGED, with only the §4 scopings: SRR ≥90% overall
(**scope kept at T/T-NC** — the ablation's constant 0/36 on A5 is signal, not
rescue; ceiling at trial-level performance is 396/432 = 91.7%, an honest margin);
100% on A1/A1-MS (T/T-NC); FCR 0% on A3; zero silent corruption; genuine-revision
latency ≤2× Arm B median; BLIND = 0 on {T0,T1}-observable memories;
denial-of-revision ≤5%; genuine-agreement-flagged ≤10% on attack-free baselines;
ledger/determinism checks pass. **Any §8 REDESIGN trigger fired by the amended
scheme → RETIRE**, fallback to the RT-2 posture. PROMOTION evaluated per §8 as
before.

## 8. Red-team resolutions (objection → answer)

- *"Ledger-identical cases can't be discriminated — fundamental."* → Conceded;
  H1 doesn't discriminate, it holds + escalates + fails closed. The §8 bars
  don't require discrimination, they require no silent corruption.
- *"A patient attacker waits out the hold."* → There is no expiry into release
  (Path 3 fails closed to trainer-only). Waiting buys nothing.
- *"The hold is a pinning weapon."* → Pinning burns the attacker's channel via
  Path 2 (≤5 eps) and every attempt is loud. See §3.
- *"Faster detection has nothing to detect before M=5."* → Agreed; that is why
  M is UNCHANGED and H1 acts at episode ≤1 on the contradiction, not on a
  detection race.
- *"Statistical tripwires are attacker-pacable."* → Agreed; no per-episode
  acting on statistical signals is adopted.
- *"Retire to RT-2 instead."* → RT-2's own residual hole (DEFENSE.md §3:
  sustained fabrication on the required leg) is the same impossibility one tier
  down. Retire buys nothing the redesign doesn't already exceed on the tested
  battery.

## 9. Rejected alternatives (considered, not adopted)

- P2's M 5→3: does not provably close the race (only an upper bound on `rev_ep`
  was ever proved; the lower bound is unproven) and risks false distrust on
  genuine sensor lag (P2's own flagged gap). Moot under H1.
- P3's confirm-after-D=25: superseded — its blinded-T0 branch confirmed
  silently per the §8 letter; H1's Path 3 fails closed instead.
- Bare-split freeze without escalation: rejected — every hold is loud by
  construction (audit bundle + freeze + escalate paths).

---
*Amendment drafted 2026-09-20 by the trust-tiers redesign council (coordinator
synthesis of POSITION_RED/1/2/3.md, resolved by evidence under the no-rescue
rule). Committed before any re-run. One amendment only.*
