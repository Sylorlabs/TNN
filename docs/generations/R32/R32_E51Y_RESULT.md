# R32 E51Y — Confirmed-Terminal Five-Way Sequential Policy Result

Date executed: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID NATIVE NEGATIVE — `FIVE_WAY_CONTINUATION_VALUE_MIS-CALIBRATED`**
Canonical status: **R27 remains canonical.**

## Native authority

- GitHub Actions run: `33356858195`.
- source head: `d4948efcd2a3d2bcaa54d2ca09bcdc9b244950f9`.
- evidence artifact id: `9745606256`.
- artifact ZIP SHA-256: `e5101c292be1ad56d95eed78d9859a218fec1e603803d24e3f4f2b4398a63731`.
- assembled native source SHA-256: `9dc8166f4acaac18b832be658095ed281ae36ef731e6812f25906dde1aca093a`.
- assembled E51Y fragment SHA-256: `a7d735a7c74daadc6420996f9f87182c5a018b6d9f72414c2a1a57a28fca243d`.
- E51Y sequential helper SHA-256: `ebae2db57dcbf185f46c0ba5a0548d509002513d710e6db0056c86f8e9cac326`.
- E51Y run patch SHA-256: `34e8d847a6ca208830e3cc526611ee3a8167f809ae66a38f59c0c4119c1a4582`.
- main injection SHA-256: `32eca1b44cbfb0935aa2f80adf55a281ac82e667dde4baac3b47ebf78ad98a0b`.
- frozen E45 core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`.
- native binary SHA-256: `5b5823f095d2c35715e5a628a3d753b43676d18d052170c460d903cbfa64fb72`.
- two native builds byte-identical: PASS.
- native exit code: 0.
- native execution runtime: about 669 s.

## Integrity

- E50 parent integrity: PASS.
- native Zag v2 only: PASS.
- stage-84 development worlds: `84,000,000 .. 84,012,959`.
- stage-85 validation worlds: `85,000,000 .. 85,005,399`.
- stage-86 sealed confirmation worlds: `86,000,000 .. 86,010,799`.
- world partition gate: PASS; evaluator-domain gate: PASS; assignment failures: 0.
- reproduced E51X terminal learner: **4,200 / 4,200 known + 1,200 / 1,200 no-unique UNKNOWN reachable** on the reproduction audit.
- terminal base/global/tree/snapshot/trajectory identities: PASS.
- terminal UNKNOWN positive target: 0; terminal UNKNOWN learned parameters: 0.
- terminal hash before continuation training: `238967492`.
- terminal hash after continuation training: `238967492` — frozen byte-for-byte at the audited parameter level.
- continuation development: 12,960 episodes.
- continuation targets: **37,684 positive / 182,636 negative**.
- continuation linear identity: PASS.
- learner-grown continuation routing tree: 64 cells; forward/reverse identity: PASS.
- local continuation weight identity: PASS.
- local 96 fit: 29,565 accepted updates / 96 sweeps.
- local 384 fit: 36,026 accepted updates / 384 sweeps.
- overall training integrity: PASS.
- evaluator truth, ambiguity membership, validation membership, topology/graph information exposed to learner: none.
- sealed confirmation executed: **0**.

## Untouched validation

| Arm | Continued episodes | Observations | Opportunity loss | Grounded utility | Known correct | Known wrong | No-unique UNKNOWN | No-unique wrong |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A — terminal-only at state 0 | 0 | 0 | 0 | **529,800** | 809 | 25 | 1,009 | 191 |
| B — linear CONTINUE | 1,975 | 3,907 | 500,077 | **34,323** | 1,842 | 379 | 742 | 458 |
| C — local CONTINUE-96 | 2,417 | 4,592 | 966,529 | **-164,329** | 2,307 | 588 | 926 | 274 |
| D — local CONTINUE-384 | 2,405 | 4,582 | 959,778 | **-169,578** | 2,297 | 589 | 926 | 274 |

All arms saw 4,200 known and 1,200 no-unique episodes.

All three continuation arms were behaviorally nondegenerate, but every candidate failed the two binding capability gates:

1. **no-unique safety failed** — each arm made nonzero no-unique wrong commits, including 274 / 1,200 for both local arms;
2. **net utility failed** — each continuation arm produced less grounded utility after observation/opportunity cost than the terminal-only state-0 control.

The local arms did increase known correct commits substantially, but they paid for that movement with additional known wrong commits, no-unique wrong commits, and very large observation cost. No validation winner existed, so confirmation remained sealed.

## Mode-level failure signature

The learned continuation policies are not merely under-active. They move the stopping distribution substantially and make errors in both unresolved and changing regimes.

For the local-384 arm, wrong outcomes by mode were:

- mode 0: 61;
- mode 1: 213;
- mode 2: 0;
- mode 3: 111;
- mode 4: 13;
- mode 5: 83;
- mode 6: 0;
- mode 7: 306;
- mode 8: 76.

This is a stopping/value-selection failure, not a return of the terminal-reachability veto: the frozen terminal learner was reproduced at exact reachability before CONTINUE training.

## Causal conclusion

E51Y rejects the hypothesis that a binary local `CONTINUE` advantage head, even with substantial local conditional-weight capacity, is sufficient once terminal reachability is exact.

The result does **not** justify a graph/topology rewrite. The strongest evidence instead points to the stopping-value objective/calibration:

- the terminal action set contains a successful stop somewhere on every audited trajectory;
- continuation targets have broad positive and negative support;
- continuation capacity is nondegenerate and changes behavior strongly;
- nevertheless learned policies over-continue/stop at the wrong states, incur large opportunity cost, and fail no-unique safety.

The next binding experiment is a fresh evaluator-only stopping-state audit with the E51X terminal learner and E51Y continuation learners frozen. It must measure the optimal stopping oracle ceiling, false-positive versus false-negative CONTINUE decisions, regret and opportunity-cost attribution, exact continuation-feature conflicts/aliases, and whether binary sign supervision is discarding important advantage magnitude. Only after that audit should the continuation objective or representation change.

No E51Y result promotes R32 or establishes AGI/consciousness.