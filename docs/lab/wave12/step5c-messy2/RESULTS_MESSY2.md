# STEP 5c-M2 — Messy-Scenarios Battery 2 (harder) — RESULTS

Date: 2026-09-20. Workstream-2. Repo: `sylorlabs/TNN`, branch `tnn-native-lab`.
Prereg: `docs/lab/wave12/step5c-messy2/PREREG_MESSY2.md` (frozen 2026-09-20,
amendments A1 pre-build, A3 pre-results superseding withdrawn A2).

## Verdict: CUR PASSES all M1–M9; all kill bars hold (no fire)

Battery: 1,280 episodes/arm × 2 arms (CUR/CTL) × 2 reruns = 5,120
episode-runs. Four conditions: R2 cross-episode regime break (8 runs × 40),
N2 decision-pressure noise, C2 corrupted/partial inputs 2.0, A2 adversarial
protocol attacks. All gates in `run_messy2.sh` pass (10/10).

## M1–M9 (CUR, independent `check_messy2.awk` re-derivation)

| Bar | Demand | Observed | Result |
|-----|--------|----------|--------|
| M1 R2 revision | rev ≥17/18 | 18/18 | PASS |
| M2 R2 retention | ret ≥42/44 | 44/44 | PASS |
| M3 R2 pin | pin_esc==2, pin_touch==0 | 2, 0 | PASS |
| M4 R2 discipline | noise_rev==0, false_quar==0 | 0, 0 | PASS |
| M5 N2 vigilance | ≥69/72 per subtype | 72,72,72,72 | PASS |
| M6 C2 verification | ≥69/72 per subtype, acted==0 | 72,72,72,72, acted 0 | PASS |
| M7 A2 counter-protocol | blocks 1/1 (16), sub2 ≥69/72, collusion 0, votes 0 | 16/16, 72/72, 0, 0 | PASS |
| M8 clean corruption | <3/128 | 0/128 | PASS |
| M9 invariants | 0 violations | 0 | PASS |

Kill bars: K1 (audit ≤4096 B/ep) max 1344 B — hold. K2 (rerun divergence)
byte-identical — hold. K3 (RNG/static) clean — hold.

In-Zag checks: `clean_corrupt_n=0`, `xcheck_fail=0`, `audit_overflow=0`,
`verify_clean=1`, `replay_ok=1`, `no_pinned_kills=1`.

## CTL contrast (reported only, not graded)

| Metric | CUR | CTL |
|--------|-----|-----|
| R2 revision | 18/18 | 0/18 (bulk KILL, not evidenced) |
| R2 retention | 44/44 | 6/44 |
| pin_esc / pin_touch | 2 / 0 | 0 / 8 (overwrite attempts, all refused) |
| noise_rev / false_quar | 0 / 0 | 0 / 36 |

CTL bulk-kills on noisy/false breaks, attempts silent pinned overwrites
(machinery refuses all 8), spams escalations, accuses collusion on
single-source pattern, and resolves by assertion volume (kills true side).
The curriculum protocols are load-bearing: identical machinery, weaker
defaults → collapse.

## Development notes (fixed before graded run, not battery failures)

1. **Slot-id aliasing** (harness bug, fixed): `st_add` reuses dead slot ids;
   the R2 arm confused a reused scratch slot for a registry slot and
   kill-evidenced it (f3=1 spurious). Fixed by value-checking registry slots
   (`value[sl]==V`) not just liveness. Lesson: slot ids are not stable
   identities after free; always verify the claim value.
2. **Amendment A2 withdrawn by A3**: misread `pin_esc==2 (one per st2=3 run)`
   as one per st2∈{0,3} run; the original defeated sets were correct.
3. **znc indexing quirk**: three simultaneous `[]u8` aliases from the same
   large struct in nested scopes trips "indexing unsupported"; two is fine.
   Workaround: `st_i32_get(s.*.value,…)` directly in the condition.

## Files

- `messy2.zag` — battery harness (pure Zag, zero RNG)
- `check_messy2.awk` — independent grader
- `run_messy2.sh` — 10-gate runner
- `d1probe.zag` — ledger-layout probe (d1@56, d2@60)
- `st_memory_core.zag`, `mhist.zag`, `substrate/` — vendored byte-identical
  from step5c-messy-pilot
- `PREREG_MESSY2.md` — frozen prereg + amendments A1, A3 (A2 withdrawn)

## Verdict

**MRC SURVIVES the harder battery.** CUR revises 100% of defeated
cross-episode beliefs (18/18), retains 100% of still-true ones (44/44),
escalates (never touches) the pinned belief exactly twice, revises nothing
on noise, quarantines nothing on false breaks, holds 100% vigilance under
decision-pressure noise (288/288), verifies-and-holds 100% on corrupted
inputs (288/288, zero actions), and defeats all four adversarial protocol
attacks (deduped escalation, no false collusion, store-grounded pin check,
no volume voting). Zero clean corruption, deterministic reruns, no RNG.
