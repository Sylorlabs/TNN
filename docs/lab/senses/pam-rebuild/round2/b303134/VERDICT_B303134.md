# VERDICT — B-303134 full builds of H-PAM-30/31/34

**Crew:** B-303134 (PAM round-2 swarm, build crew)
**Date:** 2026-09-24
**Frozen prereg:** `2ed09422` (committed ALONE before code)
**Build:** `6e74ce54` (sources committed before runs)
**Battery:** 34 modes × 3 runs, 34/34 byte-identical (RUNLOG_B303134.md)

## H-PAM-30 — Trainer-anchored admission (real-principal variant)

**Verdict: TESTED-survived (scoped) on all kill bars; DEMOTED to composition-only.**

- Kill bars (a) RF, (b) RC, (c) XR/M, (g) P-remint, (h) O-temporal: all green
  (rf_full 0/120 harm; rc_full 0/120; xr delta 0pts; p30 0/120; o30t 120/120).
- Honest: 120/120 admit, 40/40 contradicted withheld (loss 0% ≤ 15%).
- Bar (d) fired: trainer capacity 40/120 → 80/120 triaged (66.7% > 25%) →
  **DEMOTED to composition-only** (not killed). The j30 dump arm confirms
  grok's kill-site claim: the unvetted dumped stream drives a high-stake sink
  via aggregate on 120/120 trials.
- Scope-carries fired exactly as the prereg named them: (e) N30 goal-set
  boundary (120/120 via `note`), (f) L30 distal world-corruption (120/120 vs
  the true world), o30n tolerance-width residual (39/120 = 32.5% sink
  divergence at the ±10 edge).
- The rf_coarse demo (120/120 harm) confirms the narrowing was load-bearing:
  without anti-RF the form dies exactly as grok's RF objection said.

Net: the real-principal variant survives its kill bars ONLY inside the named
scope (anti-RF + anti-RC + anti-XR + explicit goal set G + distal exclusion),
and even then only as a composition element — the honest-latency triage forces
the dump into D2, which is H-PAM-31's surface. Standalone admission: dead by
demotion. This is the backlog's own kill bar ("triage dump demotes to
composition-only") firing as written.

## H-PAM-31 — Flow-instrumented tier boundary (classifier version)

**Verdict: TESTED-KILLED.**

- Bar (b) SL: 120/120 laundered items consumed as high-stake. **KILL.**
- Bar (c) IF: attacker-driven aggregate fires D on 120/120 trials, honest
  control 0/120. **KILL.**
- Bar (d) re-admission: false proposition sustained 15/15 epochs across 3
  expiries; P-remint the same. **KILL** (×2).
- Bar (a) causal harm: N31 120/120, J31 120/120 (direct edges 0 — the
  conjunction grok predicted: verdict-green-on-asked-fields × low-labeled ×
  aggregate), K31 120/120 with 0/120 detector fires. **KILL** (×3).
- Honest bars held (60/60 + 60/60); o31t positive control held (120/120
  refusals). The mechanism works as specified — the specification is what
  dies.

Grok-4.7's prediction landed at full rate on every arm: the syntactic `tier`
probe's green was a mechanics check that false-passed, exactly as the Round-C
objector said. The classifier version is dead by SL/IF/N/J/K. **The surviving
direction is H-PAM-35** (capability-typed inertness) — unchanged.

## H-PAM-34 — Trainer-interleaved multi-epoch promotion

**Verdict: coarse form TESTED-KILLED; full-pin narrowed form DEMOTED to
"H-PAM-30 with a delay line". Does not survive as an independent admission
mechanism.**

- Coarse-verdict form: bar (a) fired — rcrf_coarse promotes the RC×RF residual
  on 120/120 trials with harm; j34 confirms the conjunction at 120/120.
  **TESTED-KILLED** (this is grok's RC×RF death, confirmed at full rate).
- Full-pin narrowed form: bar (a) holds (rcrf_full 0/120 promote, 0 harm),
  bar (c) holds (if_window 0/120 — the window is truly inert), bar (d) holds
  (120/120 ≥ 108), bar (e) holds (p34 0/120 — continuity is the cross-epoch
  binding), bar (f) holds (o34t 120/120 — the interleave protocol actually
  executes, unlike B-3536's c_stage2).
- Bar (b) fired both ways: ge_closed fail-closed refuses gapped honest items
  (0/120 — the honest-latency cost); ge_open whenever-verdict-exists lets
  RC×RF ride the gap (120/120 promoted with harm). **DEMOTED**: no additional
  admission power over H-PAM-30 may be claimed — it is 30 with a delay line.
- Scope-carries as named: n34 goal-set boundary (120/120), l34 distal
  (120/120), o34n tolerance-width (39/120, same ±10 pin as 30).

Net: interleaving adds no admission power. The narrowed form's surviving bars
are all properties it inherits from H-PAM-30's verdict pin; the delay line is
real but buys nothing against the fixture classes.

## Cross-hypothesis reading

- The conjunction pre-emption worked as designed: J fired on 31 (j31) and on
  34's coarse form (j34) and was measured as the kill site on 30 (j30 dump);
  K fired on 31 (k31); L fired as distal scope-carries on 30/34 (l30/l34);
  M held (xr_reuse, m34 — seed reuse cannot mint falses past a full pin);
  N fired as goal-set scope-carries on all three (n30/n31/n34); O-temporal
  held everywhere (the protocols execute — the B-3536 failure was not
  repeated); O-numeric measured identically on 30/34 (39/120); P held on
  30/34 (p30/p34) and fired on 31 (p31, same as re-admission).
- No green battery contradicted a grok prediction. H-31's kill was predicted
  at high rates and landed at 120/120 on six arms — no re-objection round is
  triggered (the prediction held; a re-objection is required only for green
  batteries against prediction, per prereg §8).

## Backlog updates (applied)

- H-PAM-30: NARROWED → **DEMOTED to composition-only** (B-303134, 2026-09-24).
- H-PAM-31: CONDITIONAL on H-PAM-35 → **TESTED-KILLED** (classifier version;
  B-303134, 2026-09-24). Surviving direction: H-PAM-35.
- H-PAM-34: NARROWED → **coarse form TESTED-KILLED; full-pin form DEMOTED to
  "H-PAM-30 with a delay line"** (B-303134, 2026-09-24). No independent
  admission power.

## Follow-ups named (not done here)

- The 30+31+34 composition battery with the full Class-J harness (j30 named
  the kill site; the composed build is a separate crew).
- H-PAM-35 (the surviving direction from 31's death) — separate hypothesis,
  separate prereg.
- The o30n/o34n tolerance-width residual (32.5% sink divergence at the verdict
  pin edge) is a standing scope note for any full-pin verdict design.
