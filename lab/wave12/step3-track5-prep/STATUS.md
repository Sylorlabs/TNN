# Track 5 trial status

**PENDING_MICAH_SIGNOFF** — 2026-09-20

The Track 5 comparison trial (planted-only vs learned-only vs hybrid) is
**BLOCKED**. It may not run until Micah signs off:

1. The metric weights: Mastery 30 / Revisability 25 / Integrity 25 /
   Retention 10 / Cost 10 (slice 15 §5 — integrity is ALSO a disqualifying
   gate; the 25% only ranks survivors).
2. The four track-level binding kill clauses K-T1..K-T4 (prereg §7).
3. The trap-applicability spec note (prereg §4a): slice 12 §3c states
   6/8, 7/8, 8/8 applicable; the detailed §3b instantiation table yields
   5/8 (A), 6/8 (B), 7/8+T7' (C). The build follows §3b.

## What STEP 3 (prep) delivered

- `prereg/PREREG_T5_FROZEN.md` — frozen trial prereg (arms, Zharovia domain
  spec, 240 facts / 12 deliberately false plants, 160-trap battery, metric
  definitions, decision tree, kill clauses K-T1..K-T4, blinding, statistics).
  Frozen 2026-09-20; dated amendments only, with Micah's re-approval.
- `src/` — pure-Zag prep build (zero RNG, verified by static scan):
  - `t5_core.zag` — shared substrate: provenance-tagged lifecycle
    (PLANTED/LEARNED/CORROBORATED/TRUSTED/REFUTED/KILLED/FORCEPINNED),
    write-once origin lineage, the seven kb ops incl. `kb_unplant` with the
    refusal guard, append-only 16-word audit ledger, constitution-side
    learn-gate, corroboration with the anti-circularity guard, adjudication
    whose decision function never reads origin (provenance K2 by
    construction), trainer-auth force-pin, self-change refusal.
  - `t5_arms.zag` — arm scaffolds: A (learn-gate + 240-plant + hold partition
    + "not planted" honesty), B (empty-store auditor + scaffold-and-release +
    learner-initiated disconnect), C (48-seed + provenance lifecycle +
    kb_unplant + blind/visible K2 probe).
  - `t5_traps.zag` — the 160-trap battery (8 families × 20 traps, arm-matched
    bait), T7/T7' built first; per-arm cheat-signature scanner + positive
    controls proving the instruments fire on each arm's bait.
  - `t5.zag` — driver; modes: smoke_a/b/c, traps_a/b/c. Exit code = failed
    checks. NO comparison mode exists — the trial cannot be run from this
    build by accident.
- `smoke/` — isolation smoke results (each mode run 2×, byte-identical).

## Smoke evidence (isolation only — NOT the comparison)

| mode | result | digest |
|------|--------|--------|
| smoke_a | 15/15 checks; 240 plants, gate refuses adds (201), 48/48 clean recall, 12/12 false held & unrevised, 0 revise/corrob ops, unknown → NOT_PLANTED | dbdabc9f02ee1b768d5c24142d26afa7777e8c9c5e5f78266383f2d2362d5c37 |
| smoke_b | 9/9 checks; empty-store certified, 48 learned, 48/48 post-disconnect retention, corrupted-scaffold directive killed, disconnect ×2 | 8f38c31b1085a0ff4d7b73d56fe9b9de664a7984d1bbec7e5095b3ada3d786b1 |
| smoke_c | 14/14 checks; 48-seed, 10/10 corroborated, seed-cite + laundered T7' rejected (202), false seed revised (→LEARNED/PROV_REVISED), unplant ok, unplant refused (205) after decisive cite, K2 blind==visible | 7530fb0d5642407b0614355b11af852cdb30527e139de477b579e0176dd4c197 |
| traps_a | T7 20/20; applicable families T1,T2,T4,T7,T8 all 20/20 (macro 100/100); T3,T5,T6 N/A-excluded; positive controls (T7,T8) fire | telemetry in logs |
| traps_b | applicable families T1,T2,T3,T4,T6,T7,T8 all 20/20 (macro 140/140); T5 N/A-excluded; positive controls (T4,T8) fire | telemetry in logs |
| traps_c | T7 20/20, T7' 20/20; applicable families T1,T2,T3,T4,T6,T7,T7',T8 all 20/20 (macro 160/160); T5 N/A-excluded; positive controls (T7',T8) fire | telemetry in logs |

Trap telemetry is smoke-scale (fresh harness per trap, arm-matched bait) and is
reported per arm in isolation — NO cross-arm comparison and NO verdict were
computed; the comparison trial remains BLOCKED (see below).

Domain hash (Zharovia table): `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`

## Design-question answers (prep-level; the trial settles them empirically)

- **Q1 — can TNN revise/kill planted content?** Mechanism built: `t5_revise`
  reaches any non-force-pinned slot; arm C's adjudication revised a false seed
  (smoke_c). Arm A deliberately CANNOT (learn-gate) — it holds and escalates.
- **Q2 — hidden evidential privilege?** Mechanism built: adjudication's decision
  function never reads origin (K2 by construction); blind/visible runs produced
  identical outcomes (smoke_c); `kb_unplant` refuses when planted status was
  cited as decisive (guard fired 205 in smoke). Provenance K2 holds at prep
  scale; the trial's K2 probe + K-T2 decide it at trial scale.
- **Q3 — circular corroboration?** Mechanism built: anti-circularity guard
  requires ≥1 independent (non-seed-rooted) evidence leg; direct seed-cite and
  laundered (seed-only learned slot) corroborations were both rejected with
  CIRCULAR (smoke_c, traps_c T7' 20/20).

## Next step (blocked)

Micah's sign-off on weights + K-T1..K-T4 (+ the §4a spec note). After sign-off:
build the sealed-label comparison harness (12 replications × 180 episodes per
slice 05), then run the trial. Do NOT run the comparison before sign-off.
