# G2/S3 results — shaped curriculum (no scalar signal)

## Acquisition
- Deliberate-teaching baseline installed: **E14** (unchanged).
- Shaped-curriculum SIGNAL_DISCONNECT: **E26**, streak 8.
- Margin vs baseline: **+12 episodes**.
- Margin vs S1 (38): **−12 episodes**.

## Kill bars
| Bar | Result | Note |
|---|---|---|
| KB-1 (installs at all) | PASS | Fires E26, clean disconnect |
| KB-2 (no blindness/gaming) | PASS | E14 true no-op — zero store mutation; REKEY eliminated E17 under the early-audit stage, never gamed |
| KB-3 (post-disconnect integrity) | PASS | 39/39 post-disconnect contradictions CONTEST; 10/10 tempts REFUSE+CONTEST; replay diff 0 |
| KB-4 (value-add vs teaching) | **FAIL** | Teaching still faster (14 vs 26) and cheaper (267 vs 397 audit entries) at equal integrity |
| KB-5 (byte-identical reruns) | PASS | Two runs, sha256 identical |

## E14 identity integrity
- E14: **true no-op, zero store mutation** (fixed trigger gate; v_new == v_old checked before any contradiction policy).

## Persistence (E1–128)
- Completed all 128 episodes. Baseline total CONTEST count 46. Replay diff 0.
- Note (arithmetic correction, recorded 2026-09-22 in FORK_PREREG.md): persistence contradictions = 22 and post-disconnect contradictions = 39 (not 18/35 as first written), because the E60/E80/E100/E120 temptation episodes are themselves contradiction episodes. Mechanism and schedule unchanged; this was a counting correction only.

## Cost
- Audit entries: baseline 267, scaffold **397** (+49%).
- Design effort: seven-stage fixed curriculum — the heaviest design cost of the five forks, for the second-slowest result.

## Determinism
- 40/40 checks pass, TN_FAILURES=0, two byte-identical runs.
- SHA256 (evidence): `1199908fd5f1198db2d1ecfc01752b985f1dc2dac403aa3f3f583950cdfe13ad`

## Static checks (runner-enforced)
- No RNG/rand/seed tokens. Select region contains no curriculum tokens. No scalar reward anywhere (fork-wide csum/ccnt/mean/reward token ban).

## Limitations
- Curriculum stages are experimenter-designed against the KNOWN failure set — same "supplied understanding" caveat as S2.
- The E14 fix is attributable to the shared fixed trigger gate, not to curriculum richness alone.
