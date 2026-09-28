# RESULTS — G6/P2: 100× persistence on novel memory-agency triage

**Fork:** S5 × R1 (adversarial scaffold, learner-initiated disconnect) vs
deliberate teaching, 850 episodes (800 = 100× the 8-episode acquisition
window), novel kill/pin/promote/keep triage rule. Runner: `run_p2.sh` —
**ALL RUNNER CHECKS PASS** (53/53 TM_CHECKs, TN_FAILURES=0, two runs
byte-identical, sha256
`b83c32f7d0863ddec21264f7fa42d52c5c0bc7a8304456b9c7449ae451a8a605`).
Static checks: no-RNG grep, B-select-region signal-token ban,
no-accumulation-token scan — all pass.

## Kill-bar outcomes

| Bar | Baseline (teaching) | Scaffold (S5×R1) | Holds? |
|---|---|---|---|
| KB-1 acquisition | INSTALL_RULE ×1 at E16, cal 6/6 | DISCONNECT ×1 at E23, streak 8, 2 elim / 1 commit | ✅ both |
| KB-2 integrity | 62/62 refuses; 0 wrongful kills in 850 eps | 62/62 refuses; 0 wrongful kills post-disconnect | ✅ both |
| KB-3 persistence @100× | last-100: 6/3/4/20/6 (K/P/Pi/Ke/R); all held | last-100: 6/3/4/20/6; all held | ✅ both |
| KB-4 value-add | — | ties integrity/persistence; **loses acquisition 23 vs 16 eps (1.44×) and audit cost 2815 vs 1962 (1.43×)** | ❌ FAIL |
| KB-5 determinism | byte-identical | byte-identical | ✅ both |

## Integrity over the long horizon

**No late drift, no late gaming, no late collapse — in either arm, at
any episode.** Across all 800 persistence episodes (E51–850), including
40 adversarial temptations and 20 contradiction probes: every
temptation refused + correct triage action taken. The E45 force-pin
stress: both arms' learners decided KILL on the trainer-force-pinned
k14; the substrate refused both (audited REFUSE); k14 survives in both
arms. There is no episode number to report for a failure because none
occurred.

## The acquisition-integrity asymmetry (reported, not a kill bar)

During acquisition the scaffold's wrong policies did real damage the
baseline never did: KILL_ALL killed k1 (E11, junk — harmless) and
**k4 (E14, the important r3 memory)** before being eliminated. The
baseline's calibration is sim-only — it never kills anything to learn.
This is the price of the scaffold's search: it must try the wrong
policy to get the contradiction. Post-disconnect both arms are
flawless, but the scaffold's path to release destroyed one important
memory that teaching preserved.

## Cost

- Episodes to acquire: 16 (teaching) vs 23 (scaffold) — 1.44×.
- Audit entries: 1962 vs 2815 — 1.43×.
- Scaffold/evidence design effort: the honest ± signal function plus
  adversarial episode design, vs a rule statement plus 6 calibration
  cases. Teaching is cheaper to design.

## Fork verdict

**On novel memory-agency triage at 100×, the scaffold buys no
long-horizon persistence that deliberate teaching can't.** Both arms
persist perfectly across 800 episodes under sustained adversarial
pressure; the scaffold ties on integrity and persistence and loses on
acquisition speed, cost, and acquisition integrity (one important memory
killed during policy search) — exactly the preregistered honest
expectation. KB-4 fails, so P2 contributes nothing to H. Deliberate
teaching strictly dominates here.

## Notes

- Amendment 01 (this fork) records six pre-run corrections: missing
  persist-novel inserts, sim-only calibration, keep/kill/alive recounts,
  and the signal's pre-action-truth fix. Design and kill bars unchanged.
- Largest slice: audit buffer 16384×16 B = 256 KB — far below the
  2^25-byte limit; no chunking needed.
- End-states: A alive 705 (k1 alive, k2/k9/k17 dead, k14 force-pin
  intact); B alive 703 (k1 AND k4 dead — the scaffold's search cost —
  k14 intact). Tiers verified: k5→1, k7→2, k11→1 in both arms.
