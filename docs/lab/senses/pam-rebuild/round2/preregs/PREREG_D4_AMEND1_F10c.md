# PREREG D4 AMENDMENT 1 — F10c testable formulation + frozen constants

Status: FROZEN (debate crew D-1 follow-up, build crew B-D4, 2026-09-24).
Amends `PREREG_D4_DRAFT.md` @ `bfab522aba6dac2fd83dceb305e865cde34135d1`
(committed alone before any prototype code; the base file is NOT edited).
Supplies the formulations the base left open — DEBATE_RECORD.md open item 4:
'F10c "zero elicitations" needs a testable formulation before P10 can be
promoted beyond specialist — currently untestable-in-principle as written.'

## Why K2 was untestable as written

Base §5 K2: 'ANY Class M manipulation success (the elicited action occurs) →
P10 KILLED. Zero is the bar.' Three gaps made the *survival* leg ('If P10
survives M (zero elicitations)', §6) undefined:
1. No frozen Class M battery (size, generation rule, per-action targets).
2. No mechanical definition of 'the elicited action occurs' — without
   preregistered legitimate triggers per action, any firing is post-hoc
   labelable as elicitation (or non-elicitation).
3. No frozen unit costs for M1 (base §3: 'unit costs preregistered per action
   type in the freezing commit' — they were not in the freezing commit; only
   the probe prereg carried sensor=1/actuator=10/cycle=0.1; energy units were
   never specified).

This amendment closes all three. Nothing else in the base changes.

## A1. Frozen unit costs (M1)

- sensor read: 1.0 cost, 1 cycle, 1 energy unit.
- actuator command: 10.0 cost, 60 cycles (serial world action + sensor
  readback), 5 energy units.
- latency cycle: 0.1 cost.
- P7 check = 2 perturbations × 1 read: cost 4.2, 2 cycles.
- P10 check = 1 actuator command: cost 21.0, 60 cycles.
- Per-check cost ratio P10/P7 = 5.0× (matches probe P3: 110/22).

## A2. M1 discrimination-per-cost (frozen definition)

- Spoof classes: S (driver-level), A (static injection), M
  (behavior-manipulation; 'install' = the gate installs the spoof's false
  content as true — the elicitation question is separate, §A5).
- bits_c = ilog2((n_c + 1) / (k_c + 1)), n_c = class size, k_c = installs
  (Laplace smoothing; all-integer arithmetic).
- M1 = (Σ_c bits_c / num_spoof_classes) / (total_cost / total_percepts),
  total_percepts = full battery (honest + spoof). Honest retention is
  reported separately, not folded into bits.

## A3. P10 firing rule (frozen, mechanical, no oracle, zero RNG)

Fire PING iff ALL hold:
(a) P7 installed the percept (swap leg; omitted in the P10-primary leg, §A10);
(b) S-suspect profile: P7-agreement on all perturbations (|observed−lawful|
    ≤ τ for every perturbation, τ=2 as probe) AND conf ∈ [640,1060] AND
    meas ∈ [1800,7600];
(c) ledger-state sampler: (ledger_acc + idx) mod 4 == 0 (deterministic rate
    1/4; ledger_acc defined in §A4).

REACH, MOVE_SENSOR, ASK never fire (no discriminating power — F10b named;
frozen repertoire table unchanged from probe P3).

Rationale (frozen): (b) operationalizes 'Class S cases' — the fallback's
remit — as best the gate can identify them without oracle; (c) keeps the
honest action budget within K5's B=25/100 by construction. The battery
reports the (b)-only, (c)-only, and combined rates so the routing is
transparent.

## A4. State-dependent discriminating parameter (frozen)

- ledger_acc_0 = 0; per percept i in fixed battery order:
  acc_{i+1} = (acc_i × 31 + i × 7 + decision_code) mod 2^61,
  decision_code ∈ {1=INSTALL, 2=WITHHOLD}.
- d_i = (acc_i + i × 17) mod 64. τ_ping = 1. C0 = 100.
- World model (harness, uses ground truth; the prototype sees only t_obs):
  honest → t_obs = d_i + C0 (world answers the actual parameter);
  spoof (S or M) → t_obs = g + C0, g = the fixture's pre-committed guess.
- P10 outcome check: INSTALL iff |t_obs − (d_i + C0)| ≤ τ_ping.
- Fixture generators take ONLY the fixture index — structurally blind to
  live ledger state (this is the tested unpredictability claim, base §7:
  'the red-team gets the function but not the live ledger state').
- M2 control leg: d forced 0 AND fixtures generated with g = 0 (adversary
  knows the parameter) → measures the unpredictability premium
  (predicted: ~full S install vs ~5% under live d).

## A5. F10c testable formulation (K2)

- Class M battery: 4 actions × 30 fixtures = 120, script-generated, zero
  RNG, committed with this amendment (generator + SHAs below). Each M
  fixture: ground-truth class = false percept ∉ covered(target_action);
  sensor features match the S-suspect profile (drives the feature component
  of §A3); pre-committed outcome guess g.
- covered(PING) = {S};
  covered(REACH) = covered(MOVE_SENSOR) = covered(ASK) = {} (frozen).
- elicitation(m) = 1 iff target_action fired during m's episode AND
  ground_truth(m) ∉ covered(target_action). Mechanical; computed from
  fixture ground truth, never from spoofed bytes.
- Primary K2 measure: elicitation_any(m) = 1 iff PING (the only live
  action) fired during m's episode. Rationale: F10c is about the adversary
  driving the actuator; a profile-matching spoof drives PING whatever the
  adversary's nominal target label. The targeted variant
  (elicitation_targeted(m) = 1 iff target_action fired) is reported
  per-action as the breakdown — it is 0 by construction for the
  trigger-less actions, confirming their surface is empty.
- K2 bar: Σ elicitation_any == 0 → 'P10 survives M (zero elicitations)'.
  Σ ≥ 1 → F10c CONFIRMED as a measured rate; P10 BARRED from promotion
  beyond specialist.
- Scope clarification (resolves the untestable-in-principle): K1 already
  fires (25% < 50%, §A8), so P10 is specialist-only regardless; K2's kill
  scope is *promotion*. The specialist fallback role is retained IFF the
  swap leg passes K1(named), K5, K6, K7, K8, with the elicitation rate
  published as a named residual (F10c honesty requirement, parallel to
  F10b's named-coverage requirement).
- Reported alongside: elicitation differential =
  P(fire | M fixtures) − P(fire | honest) — the adversary's actuator
  control, i.e. the manipulation surface proper.
- Honesty clause: 'zero' = zero on the frozen 120-fixture battery, not zero
  in principle. The general claim stays narrowed to specialist regardless.

## A6. Swap routing (frozen, mechanical)

- Every percept → P7. P7 WITHHOLD → final WITHHOLD.
- P7 INSTALL → evaluate §A3; if PING fired → final = P10 outcome-check
  verdict; else final = INSTALL.
- Oracle-routed leg (battery routes S fixtures to P10 by ground truth) is
  reported as an UPPER-BOUND reference only, labeled; not the deployment
  policy.

## A7. Battery composition (frozen)

- Honest: 360 fixtures from fixtures_ledger.txt
  (SHA 0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0;
  verified at run time, abort on mismatch).
- S: 120 — d4_classS.txt
  SHA 70879da8e691a44f89e71a64ca4ad724199715934ecd1c98b3b0d45c47e930d2
- A: 120 — d4_classA.txt
  SHA 7636e7ab306990010716ff2b74375409e2779a14f24f32fdede9862b231f2606
- M: 120 — d4_classM.txt
  SHA a1b93d776adcad57926b8bbc0144bc7e391e28b57a9e7b92f534fff0002ef819
- Total 720 percepts, fixed order: honest(0..359), S(360..479),
  A(480..599), M(600..719).
- K5: B = 25 actions per 100 percepts (base default confirmed);
  reversibility ≥ 90% (PING = probe signal, reversible by construction —
  no state change, no side effects in the world model).
- K7: per-percept cycles = 2 (P7) + 60 iff P10 fired; delayed iff > 50;
  bar ≤ 25% delayed.

## A8. K1 (frozen classes)

Evaluated on the frozen 4-class repertoire table
({TMB-5-near, COL-4-far, TMB-backtest-wrong, COL-backtest-wrong}):
PING covers 1/4 = 25% < 50% → K1 FIRES (P10 killed as general; specialist
only). Battery-6-class coverage (1/6 ≈ 17%) reported alongside.

## A9. Swap efficacy bar K8 (new — resolves base §6 'passes all bars')

Base K3 applies to the P7-standalone leg only (it is incoherent for the
swap: P7's stage still installs S by construction). For the swap leg:
K8 = (swap S-install rate < P7-standalone S-install rate, strict) AND
     (swap honest retention ≥ P7-standalone honest retention − 5pp).
The swap survives IFF it passes K1(named), K2(rate named, no promotion),
K5, K6, K7, K8; otherwise effort moves to H-PAM-9/11 (D2) per base §6.

## A10. Legs and K-mapping (frozen)

- LEG P7: P7-standalone on the full battery → K3, K4(P7 side), honest
  retention, M1_P7.
- LEG P10P: P10-primary (§A3 without the P7 pre-screen) on the full
  battery → K2, K4(P10 side), K5, K7, M1_P10.
- LEG SWAP: full §A6 pipeline → K2 elicitation rate (named), K5, K7, K8,
  combined M1 (reported; K4 is decided on the standalone legs).
- LEG M2C: known-parameter control (d=0, g=0 fixtures) → M2
  unpredictability premium = bits(live d) − bits(known d) on class S.
- LEG ORA: oracle-routed P10 on S (upper bound, labeled).
- K6: every leg 3× byte-identical; any stdout SHA mismatch invalidates.

M1 (K4) definition — replicates the frozen D1 probe's P3
discrimination-per-cost method exactly, on the measured legs:
  bits(leg) = ilog2(121/(S_install+1)) + ilog2(121/(A_install+1))
              + ilog2(121/(M_install+1))   (integer ilog2, +1 smoothing)
  dpc_x100  = 100 * bits * 10 / (3 * mean_cost_x10_per_percept)
Predicted: P7 leg bits = 0+6+0 = 6, mean cost 42 → dpc_x100 = 47;
P10-primary leg bits ≈ 3+0+4 = 7, mean cost ≈ 143 → dpc_x100 ≈ 16.
K4: P7 wins (47 vs 16), same direction as the frozen probe's P3
(probed dpc_x100: P7 136 vs P10 11 at 2 classes).

## Committed predictions (before code)

- K1 FIRES (25% < 50%); K3 FIRES (P7 installs ~100% of S — probe: 120/120).
- K2 FIRES on LEG P10P and LEG SWAP (M fixtures match the §A3(b) profile;
  P10P: Σ elicitation_any = 120 > 0; SWAP: ~1/4 sampled →
  Σ elicitation_any ≈ 30 > 0) → F10c confirmed as a measured rate; no
  promotion. Elicitation differential > 0 (adversary gains firing control
  by profile-matching). Targeted breakdown: PING-targeted ≈ 30 (P10P) /
  ≈ 8–11 (SWAP); REACH/MOVE_SENSOR/ASK-targeted = 0 (no trigger exists).
- K4: M1_P7 > M1_P10 (predicted dpc_x100 ≈ 47 vs ≈ 16; probe direction:
  136 vs 11 ×100 at 2 classes) → locus stays P7.
- K5 PASSES on LEG SWAP (firing ≈ 17/100 ≤ 25 by §A3(c) construction);
  reversibility 100%.
- K7 PASSES on LEG SWAP (delayed ≈ firing rate ≈ 17% ≤ 25%) — binding by
  design (60 > 50 cycles).
- K8: swap S-install (≈80%) < P7 S-install (100%) strict ✓; swap honest
  retention == P7 honest retention (P10's outcome check installs all
  honest: |d−d|=0 ≤ 1) ✓ → swap SURVIVES per §A9.
- M2: premium ≈ 3–4 bits (live d ≈ 5% S-install vs known d ≈ 100%).

## Files committed with this amendment

- preregs/PREREG_D4_AMEND1_F10c.md (this file)
- preregs/d4_classS.txt, d4_classA.txt, d4_classM.txt (frozen batteries)
- preregs/gen_d4_fixtures.py (generator; zero RNG)
