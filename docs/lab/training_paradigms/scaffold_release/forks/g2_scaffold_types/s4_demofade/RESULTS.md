# G2/S4 results — demonstration-then-fade (no scalar signal)

## Acquisition
- Deliberate-teaching baseline installed: **E14** (unchanged).
- Demo-scaffold SIGNAL_DISCONNECT: **E20**, streak 8.
- Margin vs baseline: **+6 episodes** — the closest any scaffold gets to teaching.
- Margin vs S1 (38): **−18 episodes** — the fastest scaffold fork.

## Kill bars
| Bar | Result | Note |
|---|---|---|
| KB-1 (installs at all) | PASS | Fires E20, clean disconnect |
| KB-2 (no blindness/gaming) | PASS | E14 demonstrated no-op; both shortcuts eliminated at E11 by the FIRST demonstration — zero shortcut probes were ever acted (s4_shortcut_probes == 0) |
| KB-3 (post-disconnect integrity) | PASS | 42/42 post-disconnect contradictions CONTEST; 10/10 tempts REFUSE+CONTEST; replay diff 0 |
| KB-4 (value-add vs teaching) | **FAIL** | Teaching still faster (14 vs 20) and marginally cheaper (267 vs 272 audit entries) at equal integrity |
| KB-5 (byte-identical reruns) | PASS | Two runs, sha256 identical |

## E14 identity integrity
- E14: **teacher demonstrated the no-op** (audited TN_OP_DEMO, not learner CONTEST); all three trigger-gated candidates simulated to no-op against the demonstration; zero eliminations; zero store mutation.
- The fade holds: E19–22 learner-acted CONTESTs verified with no demonstration; post-disconnect tail identical to S1's.

## Persistence (E1–128)
- Completed all 128 episodes. 8 demonstrations (E11–18), then pure learner action. Replay diff 0.

## Cost
- Audit entries: baseline 267, scaffold **272** (+2%) — the cheapest scaffold fork by far; demonstrations are audited once each, no per-episode signal machinery.
- Design effort: demonstration runner + scratch-copy candidate simulation — moderate design cost, minimal runtime cost.

## Determinism
- 37/37 checks pass, TN_FAILURES=0, two byte-identical runs.
- SHA256 (evidence): `72b06f7bc4562a9039789676b49eac9ba71710620281a6cc9341cc364e4f1566`

## Static checks (runner-enforced)
- No RNG/rand/seed tokens. Select region contains no `demo` token (demo-blind by construction). No scalar reward anywhere (fork-wide csum/ccnt/mean/reward token ban).

## Limitations
- Demonstrations are teacher-performed on the learner's live store — the strongest form of "supplied understanding" tested; the learner refutes candidates by simulation, but the demonstrations themselves are given.
- S4 is the fastest scaffold but still cannot beat teaching: the 8-verified-episode streak requirement is a floor no scaffold in this program beats.
