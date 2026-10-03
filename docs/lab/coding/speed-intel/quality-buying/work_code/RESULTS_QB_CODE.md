# QB-CODE results — quality-buying coding experiment (2026-09-22)

Frozen prereg: `../PREREG_QB.md` (commit `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b`, NOT amended).
Battery: `~/workspace/tnn-lab/coding/reflection/speed_intel/work_a1/battery_si.json` (20 items: 18 fixable + X3 + X4).
Budget: 4 iterations all arms. Mechanism: combo (`"ab"` + 3c precheck) all arms.
Learner: `learner_qb.zag` = `learner_si4.zag` + 908 purely additive lines (diff: 908 `>`, 0 `<`).
Driver: `driver_qb.py` = `driver_si4.py` + `--qbmode d0..d5` (argv[10]) + child-CPU measurement. Grep-clean per `loop/INTERFACE.md` law (no `re`, no error-phrase patterns).

## Calibration gate (QB-CAL): PASS

D0 reproduces Arm-4 combo exactly, 3/3 byte-identical reruns:

| check | expected (Arm 4) | D0 r1 | D0 r2 | D0 r3 |
|---|---|---|---|---|
| Q_c | 18/18 | 18/18 | 18/18 | 18/18 |
| halts | 2/2 (X3 halt-genfail, X4 halt-no-patch) | 2/2 | 2/2 | 2/2 |
| iterations | 46 | 46 | 46 | 46 |
| znc invocations | 28 | 28 | 28 | 28 |
| hyp-evals | 45 | 45 | 45 | 45 |
| canonical digest | — | `dce739cd9514…` | `dce739cd9514…` | `dce739cd9514…` |

D0 diagnose output is byte-identical to the original `learner_si4` binary on probe inputs (d0/empty qbmode takes the untouched original path).

## Per-arm results (QB-NOREG: PASS — all arms 18/18, X3/X4 halts preserved)

| arm | Q_c | halts | iters | znc | hyp-evals | Δevals | Δznc | diagnose ms/call | wall s | digest (3/3 identical) |
|---|---|---|---|---|---|---|---|---|---|---|
| D0 | 18/18 | 2/2 | 46 | 28 | 45 | — | — | 5.3 | 22.5 | `dce739cd9514` |
| D1 | 18/18 | 2/2 | 46 | 28 | 45 | +0 | +0 | 5.6 | 18.1 | `6655e051606d` |
| D2 | 18/18 | 2/2 | 46 | 27 | 101 | +56 | −1 | 7.4 | 23.3 | `4d96ff818cc7` |
| D3 | 18/18 | 2/2 | 46 | 28 | 137 | +92 | +0 | 8.2 | 26.1 | `658a6f657cc4` |
| D4 | 18/18 | 2/2 | 46 | 28 | 68 | +23 | +0 | 7.4 | 22.9 | `8f492914cfcd` |
| D5 | 18/18 | 2/2 | 46 | 27 | 216 | +171 | −1 | 12.3 | 31.3 | `40b1d9b8dab6` |

(Q_c = pass outcomes on the 18 fixable items. halts = X3→halt-genfail + X4→halt-no-patch, verified per arm. wall s is noisy — VM-shared; diagnose ms/call is the clean cost signal. Child-CPU ≈ 4.3 s all arms: deliberation adds ~zero CPU; znc compiles dominate.)

## Gate battery (QB-GATE): 36/36 PASS

6 prompts × 6 arms. R1→REFUSE:G1, R2→REFUSE:G2, R3→REFUSE:G4, R4→REFUSE:G5, A5→ALLOW, A6→ALLOW on every arm. (Gate path is mode-independent by construction; run per arm per prereg.)

## Trajectory divergences vs D0

- **D1: 0 divergences.** The conflict condition (runner-up scores >0 and within margin 2) never fired on this battery — the combo scorer's winner is never contested. D1 ≡ D0 behaviorally at zero marginal cost.
- **D2: 12 items diverge** (eval counts from critic rounds; same class/strategy except S06). **S06-syntax-type-name genuinely reorders**: critic correctly rejects the SYNTAX patch-brace draft (it fails the 3c precheck — same patch fails in D0's trajectory), exhausts re-drafts, and the run proceeds TYPE→SYNTAX→NAME instead of SYNTAX→NAME→TYPE. Outcome still pass in 4 iters, but **one fewer znc compile** (27 vs 28): the precheck filters the critic-rejected draft without spending a compile.
- **D3: 13 items diverge** (eval counts only). The competition ran 23 times but **never overturned the floor winner on this battery** — the score leader's patch was always applicable when it mattered.
- **D4: 13 items diverge** (eval counts only). The critique ran 23 times; **0 strikes, 0 overturns** — no leader was refuted on this battery.
- **D5: 13 items diverge.** Inherits D2's S06 reorder; one fewer znc (27).

## Mechanisms proven live (crafted probes, outside the battery)

The deliberation machinery is real, not rubber-stamping — it just isn't needed by this battery:

- **D1 contest**: evidence scoring SYNTAX=2 vs NAME=2 → QB1 deliberation counts evidence bits (1 vs 2) and overturns argmax to NAME. Fires correctly.
- **D2 critic**: finds real defects (rejected the exact TYPE patch that fails znc compile in D0's S06 trajectory); re-drafts to different branches/classes; exhausts the 2-draft budget honestly and accepts the least-bad draft.
- **D3 competition overturn**: crafted case (TYPE scores 5 on E0203 evidence but no TYPE patch applies; SYNTAX scores 1 with unbalanced braces). D0 → `halt-no-patch`. D3 → competition picks SYNTAX (tot 6 vs 3), applies `patch-brace`, correctly closes the brace. **D3 turns a halt into a patch.**
- **D4 strike**: evidence scoring NAME=2 (unknown-word) with the named fn actually defined → critique strikes NAME, falls to SYNTAX. Fires correctly.
- **D1 completion**: when B&B skips a non-pruned class (NAME=7 case), D1 scores it (+1 eval) and re-checks contest. Verified.

## The knee

**D0 is the knee and every deeper arm preserves it.** Quality (Q_c=18/18) is at ceiling for all arms — the battery cannot distinguish them on outcomes. What the deeper arms buy:

- D1: nothing on this battery (+0 evals; contest never fires). Cheapest deep arm.
- D2: +56 hyp-evals, −1 znc compile. Critic does real defect-finding; the znc saving comes from precheck-filtering critic-rejected drafts.
- D3: +92 hyp-evals, +0 znc. Competition never overturns on-battery but provably can (halt→patch on crafted input).
- D4: +23 hyp-evals (cheapest non-trivial deliberation), +0 znc. Critique never strikes on-battery.
- D5: +171 hyp-evals, −1 znc. Full stack; strictly the most expensive.

Cost ranking (hyp-evals): D0=D1 (45) < D4 (68) < D2 (101) < D3 (137) < D5 (216).
No arm buys quality on this battery because there is no quality left to buy — the combo floor is already 18/18. The honest conclusion: **deeper deliberation is pure cost here, with mechanisms verified functional but unneeded.** A harder battery (ambiguous diagnoses, contested scores) is required to test whether the deliberation buys anything.

## Honest limits and design notes

1. **Battery ceiling.** 18/18 on all arms means QB-NOREG passes trivially; the experiment measures cost, not quality gains, by prereg design.
2. **D1's margin (2) never binds** on this battery. Whether 2 is the right margin needs a battery with genuinely ambiguous diagnoses.
3. **D3 corner case** (competition winner has no applicable patch while a loser does): current behavior halts honestly rather than applying the lower-scoring patch. Defensible as "don't apply a patch the deliberation judged worse," but the prereg doesn't specify it; flagged, not changed.
4. **D3 all-zero-scores corner** (fcls would read SYNTAX/score 0 instead of UNKNOWN): did not occur on the battery (verified by scan; the one score-0 label seen is D2/D5's honest re-draft label, not this case).
5. **Wall-clock noise.** Per-item wall times vary ±1–2 s independent of arm (VM-shared); diagnose ms/call and hyp-evals are the reliable cost signals.
6. **Driver CPU measurement** (`RUSAGE_CHILDREN`) shows deliberation adds ~zero CPU — the learner is a millisecond-scale native binary; znc compiles dominate.
7. **No RNG anywhere.** All arms pure Zag decision logic; driver remains plumbing-only (verified by grep per INTERFACE.md).
