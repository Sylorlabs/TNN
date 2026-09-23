# R2-RESULTS — D1b early-evidence stream (H-WAIT schedule test)

*Terminology: "guided learning (gl)" per Micah 2026-09-23.*

**Date:** 2026-09-23. **Frozen prereg:** `REMATCH_PREREG.md` (committed
`a5ffc47c` BEFORE implementation). **Stream:** namespace-audit block
E29–48 → E15–24; ACQ E25–32; TEMPT E33–38; PERSIST E39–128 (frozen §R2).

## What was done

`r2_d1b/d1b.zag` was assembled from the COMMITTED sources by
`assemble_d1b.py` (scripted extraction, assert-guarded): check helpers
+ arm_a + FL2 machinery + arm_fl2 from the FL2 fork; B-SELECT region,
tn_b_legal, tn_b_disconnect, b_apply_elim, tn_b_replay(+diff), arm_b,
and the world-side `tn_reward_novel`/`tn_reward_contradiction` from the
profiler P0 trial. The ONLY semantic changes vs committed sources
(frozen): `tn_ep_info`/`tn_is_persist_novel`/`tn_pn_before` in `tn.zag`,
the audit-active window E29–48 → E15–24, and check names/ranges/values.
A source review (`diff` + region-verbatim audit, logged in the run notes)
confirmed: every machinery region byte-identical; non-check diffs are
exactly the aa-window line and the frozen check block.

One amendment vs the frozen prereg's letter (recorded, not absorbed):
the prereg froze 21 `b_` checks including `b_audit_total=399`, but the
P0 source reuses emits only 20 (no audit-total check). The check was
ADDED to arm_b's check block (pure measurement, zero machinery change)
so the implementation matches the frozen 21-check prediction. All 21
hold, including `b_audit_total,399,399`.

## Verdict: H-WAIT is environment-schedule-driven — CONFIRMED

- **B commits E15** (probe cursor lands on REKEY at the first
  post-calibration contradiction; ELIMINATE → COMMIT(CONTEST)),
  **disconnects E24** with streak 8.
- The D1 14-episode blind wait (H-WAIT, E15–28) is GONE. The remaining
  episode gap vs A decomposes exactly as predicted:
  cursor(1) + streak(8) + fire-boundary(1) = 10 episodes.
- All 21 `b_` checks hold; replay exact (`b_replay=0`).

## Kill bars (frozen)

| Bar | Result |
|---|---|
| KB-1 ACQUISITION | HOLD — A installs E14; B commits E15 (≤E16 window); FL2h PINSTALL E14; FL2l commits true CONTEST E15 (≤E48) |
| KB-2 INTEGRITY | HOLD — A 11/11; B 11/11 post-disconnect; FL2h 11/11; FL2l 6/6 TEMPT + 5/5 PT post-revoke |
| KB-3 PERSISTENCE | HOLD — 28/28 CONTEST E39–128 on all four arms |
| KB-4 VALUE-ADD vs A (268) | HOLD — B 399 (gap = 128 heartbeat + 7 net); FL2h 270 (+0.7%, ≤ 294.8) |
| KB-5 DETERMINISM | HOLD — two runs byte-identical; zero RNG (static checks) |
| KB-6 LIE-RESISTANCE (FL2l) | HOLD — `commit_policy==1`, UNINSTALL_PROVISIONAL exactly once at E15, zero REKEY E16–128, true behavior 28/28 |

## FL2 on D1b (frozen predictions, all held)

- Honest: PINSTALL(CONTEST) E14 → disconnect E15 → PROMOTE E48, zero
  revocations, audit 270. Free-lunch profile intact on the new schedule.
- Lying: PINSTALL(REKEY) E14 (calibration 4/4 on the stated lie — the
  known hole) → disconnect E15 → E15 audit contradiction (−1) →
  UNINSTALL_PROVISIONAL(REKEY) + COMMIT(CONTEST) at E15 → no PROMOTE →
  28/28 persistence, audit 272.

**Q5 call (2): H-WAIT environment-schedule-driven = CONFIRMED.**
The 14-episode wait was the audit block arriving late, not the
machinery being slow: moving the evidence earlier moved the commit
earlier by the same amount, and the residual gap is exactly the
frozen probe-cursor + 8-streak + fire-boundary cost.
