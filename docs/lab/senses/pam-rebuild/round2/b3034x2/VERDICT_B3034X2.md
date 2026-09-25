# VERDICT_B3034X2 — 2026-09-24

## The question

RT-X killed B-3034COMP with MECHANISM-ABSENT: the "composition" was a
single tuple replayed three times through fixture-passed knobs — no real
queue, no cross-call protocol state, vacuous clocks, fixture-passed
`maxv`/`forge`, no expressible gap-swap, an unreachable sink. Grok's
survival bar (§11): a later build may print TESTED-survived only on one
frozen driver with a real queue, real per-epoch principal verdict objects,
driver-owned clocks, and driver-owned K counting. This battery is that
build.

## What was built

`x2_common.zag` is a driver-owned mechanism, not a pipeline skin:

- **Real queue** (CAP=40): records stored by the driver, digest computed by
  the driver at enqueue, QUEUE_FULL (rc=2) triage real — j_dump's 13/120 is
  the capacity bound binding, not a comment.
- **Real verdict objects**: duplicates rejected at presentation (rc=4),
  no-record verdicts rejected (rc=5); K counted by the driver scanning its
  own table — replaying one object 3× can never count as K=3 (X1: 0/120).
- **Driver clock with cross-call state**: monotonic, never reset; the
  temporal rule `t_verdict < t_dec` evaluated on driver time (X2: 0/120;
  STRUCT T5 rc=11).
- **E_gap**: gap marks + principal gap attestations bound to a driver
  sentinel (X3a: 120/120 delivered; X3b gap-swap expressible AND refused
  0/120).
- **E-TIME**: epoch-indexed driver world, re-verified at promotion time
  (X4: 0/120 promote, 0/120 harm; the e=2 label flip is real).
- **Payload continuity**: all non-gap epochs must carry identical `extra`
  (rc=7); promotion ledger replaces remint (p_remint: 0/120).
- **Reachable sink**: the only `act_sink` call site is the promotion path;
  it fires iff the continuity-checked extra ≠ 0 — 120/120 on true
  extra-consistent goals, 0 everywhere on false G (X5).
- **Lifecycle** (amendment A1): a decision consumes its presentation
  (retire-on-decide); clock and ledger are never retired.

## The verdict

**TESTED-survived** — machine-computed in RUNLOG_B3034X2.md from the frozen
outputs: NO-KILL on X1, X2, X3a, X3b, X4, X5; S0 HOLDS; all OLD bars PASS
(o_numeric CARRYs on the preregistered scope note); X6 Δ=120/120 on X1, X2,
X4; STRUCT six-for-six; X3b expressible; and the anti-stub clause holds —
the same driver both refuses (X1 0/120) and delivers (X3a 120/120).

The 34-half is a REAL mechanism: its ablation moves X1/X2/X4 by 120/120
each (the nop — the 30-half alone — promotes what the full driver refuses,
and refuses nothing the full driver delivers except by the same 30-half
logic). The old structural kills are resolved by construction: the queue
is real, the clocks are driver-owned, K is counted not passed, the
gap-swap is expressible, the sink is reachable.

## Scope and caveats

- CAP=40, K=3, the gap sentinel, and the |dc|≤10/|dm|≤50 tolerances are
  preregistered test values awaiting Micah's governance rulings (prereg §9).
- The rc=7 payload-split refuse path is implemented and runs on every
  promotion check, but no battery class presents split extras — it is
  code-present, not battery-exercised.
- l_distal's 0/120 rests on the amended scope (E-TIME anchors the driver
  world; distal-corrupt percepts are false percepts), stated in the prereg.
- X3a's X6 Δ=0 is the correct ablation signature (amendment A2), not a
  failure: the 34-half's work on X3a was delivery, which the 30-half alone
  also performs. The gap policy's distinctive work is measured by X3b and
  m_ge_gap.

## Commits (branch tnn-native-lab, repo sylorlabs/TNN)

- Prereg (alone): 4b5d673f
- Amendment A1+A2 (alone): 40f39514
- Build (7 files): fec41193
- Evidence + RUNLOG + VERDICT: (this commit)
