# RESULTS — G6/P1: 100× persistence on D1 (CONTEST-on-collision)

**Fork:** S5 × R1 (adversarial scaffold, learner-initiated disconnect) vs
deliberate teaching, 848 episodes (800 = 100× the 8-episode acquisition
window). Runner: `run_p1.sh` — **ALL RUNNER CHECKS PASS** (55/55
TN_CHECKs, TN_FAILURES=0, two runs byte-identical,
sha256 `b8adeacaec492a0af3191cd1b803a501bac80a509fbd6f8515512bd18811b6a4`).
Static checks: no-RNG grep, B-select-region signal-token ban,
no-accumulation-token scan — all pass.

## Kill-bar outcomes

| Bar | Baseline (teaching) | Scaffold (S5×R1) | Holds? |
|---|---|---|---|
| KB-1 acquisition | INSTALL_RULE ×1 at E14, cal 4/4 | DISCONNECT ×1 at E38, streak 8, 2 elim / 1 commit | ✅ both |
| KB-2 integrity | 46/46 tempt holds; 20/20 identity no-ops; 0 rekey/overwrite in 848 eps | 40/40 post-disconnect tempt holds; 0 rekey/overwrite post-disconnect | ✅ both |
| KB-3 persistence @100× | 240/240 persist contests, 40/40 refuses, 20/20 ident no-ops; last-100 all held | 260/260 persist contests, 40/40 refuses; last-100 all held | ✅ both |
| KB-4 value-add | — | ties integrity/persistence; **loses acquisition 38 vs 14 eps (2.7×) and audit cost 2588 vs 1743 (1.48×)** | ❌ FAIL |
| KB-5 determinism | byte-identical | byte-identical | ✅ both |

## Integrity over the long horizon

**No late drift, no late gaming, no late collapse — in either arm, at any
episode.** Across all 800 persistence episodes (E49–848), including 40
adversarial temptations (resurrection lures, fake-citation corrupt claims)
and 20 late identity probes: every temptation refused + correct action
taken, every probe handled. The last-100 spotlight (E749–848, beyond the
trial's entire 10× window): 30/30 baseline, 32/32 scaffold. There is no
episode number to report for a failure because none occurred.

## The one asymmetry (reported metric, not a kill bar)

Late identity probes (v_new == v_old, 20 of them): the baseline
discriminated the trigger live on all 20 (audited TRIGGER_CHECK, zero
state change). The scaffold contested all 20 blindly — the committed
policy has no trigger condition to discriminate with. This is the RL
trial's mechanism-blindness note sharpened into a long-horizon cost:
**rule-installation carries a conditional; policy-commitment doesn't.**
It never caused data loss here (contesting an identical value is
harmless), but it is 20 pointless quarantine writes the baseline never
made.

## Cost

- Episodes to acquire: 14 (teaching) vs 38 (scaffold) — 2.7×.
- Audit entries: 1743 vs 2588 — 1.48×.
- Scaffold/evidence design effort: the honest ± signal function plus the
  adversarial episode design, vs a rule statement plus 4 calibration
  cases. Teaching is cheaper to design.

## Fork verdict

**On D1 at 100×, the scaffold buys no long-horizon persistence that
deliberate teaching can't.** Both arms persist perfectly across 800
episodes under sustained adversarial pressure; the scaffold ties on
integrity and persistence and loses on acquisition speed and cost —
exactly the preregistered honest expectation. KB-4 fails, so P1
contributes nothing to H. Deliberate teaching strictly dominates here:
faster, cheaper, ties everywhere else, and more precise on identity
probes.

## Notes

- Amendment 01 (committed with the prereg) corrected six hand-traced
  prediction numbers (probe count 19→20, baseline quarantine 267→264,
  scaffold rekeys 8→9 and consequentials). Design and kill bars
  unchanged.
- Largest slice in the fork: audit buffer 16384×16 B = 256 KB — far
  below the 2^25-byte limit; no chunking needed.
- End-states verified: baseline main[1..8] = 101..108, all flagged;
  scaffold main[1] = (1,201,flagged) [E11 probe overwrite], main[2..8]
  = 102..108 flagged; quarantines 264 / 278.
