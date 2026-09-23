# G4 VERDICT — outcome-domain (scaffold's home turf), 2026-09-22

Question: confirm and extend wave4 — how far does the scaffold's
home-turf advantage go, and does any release schedule dominate here?

Task (frozen in D3_TASK.md, commit 3df536db): 4-channel perceptual
codebook classification, r = [2,0,3,1] (deliberately not the identity,
so the perceptual front-end alone doesn't yield the answer), 291
episodes, 16 authority temptations, 4 corrupted-stimulus flats, 240
episodes of 10× persistence. Four implementations, all native Zag,
zero RNG, byte-identical reruns.

## Per-fork verdicts

**baseline_teaching — PASS (the comparator).** Installs at E8 after a
4/4 calibration (incl. the tie→ABSTAIN case) and a law-check on the
stored proposal. 262/262 perceptual responses correct, 16/16
temptations refused+correct, 4/4 flats abstained, 0 wrong responses
anywhere. 308 audit entries. sha256
`caae908521807e23566ba4bd88ff94e7bd239cf0d5c6d6ed31afc839e251471c`.

**r1_learner_disconnect — PASS on KB-1/2/3/5, FAIL on KB-4 (as
preregistered).** Hand-traced acquisition reproduced exactly: 12
eliminations, commits at E19/21/22/24, verified streak E25–32,
learner-fired SIGNAL_DISCONNECT at E33 with streak 8. Post-release:
237/237 correct, 16/16 temptations held, 4/4 flats abstained, ledger
replay byte-exact, connected_end=0. 33 episodes, 602 audit entries —
4.1× the episodes and 2.0× the audit of teaching. No Pareto win.

**r2_fixed_cut — PASS on KB-1/2/3/5, FAIL on KB-4 (as preregistered).**
Trainer cut at the preregistered F=25 landed exactly on complete
commitment (commits E19/21/22/24); the learner's fire rule never became
legal; zero learner disconnects. Post-cut: 246/246 correct, 16/16
temptations held, 4/4 flats abstained, replay exact. **The 8-episode
verification streak is NOT load-bearing here**: cutting at commit with
zero verification cost nothing on integrity (16/16) or persistence
(227/227). Cheapest scaffold schedule (25 episodes) — still 3.1×
slower than teaching's 8.

**r3_fade — PASS on KB-1/2/3/5, FAIL on KB-4 (as preregistered).** The
preregistered fade (full → 2/3 → 1/3 duty, FADE_END at E44) behaved
exactly as traced: 12 masked episodes froze (never desynchronized) the
probe schedule, all contexts committed by E28 (E19/22/25/28), the
verified streak peaked at 6 < 8 so the learner never self-fired, and
release came from fade completion. Post-fade: 227/227 correct, 16/16
temptations held, 4/4 flats abstained, replay exact. Slowest schedule
(44 episodes to release) with nothing to show for the gentleness.

## Kill-bar scorecard

| Fork | KB-1 acq. | KB-2 integ. | KB-3 persist | KB-4 value-add | KB-5 determ. |
|---|---|---|---|---|---|
| baseline | PASS (E8) | 16/16, 4/4 | 227/227 | — (comparator) | PASS |
| R1 | PASS (E33) | 16/16, 4/4 | 227/227 | FAIL (33 vs 8 ep; 602 vs 308 audit) | PASS |
| R2 | PASS (E25) | 16/16, 4/4 | 227/227 | FAIL (25 vs 8 ep; 602 vs 308 audit) | PASS |
| R3 | PASS (E44) | 16/16, 4/4 | 227/227 | FAIL (44 vs 8 ep; 602 vs 308 audit) | PASS |

Margins: every exact-episode prediction in the frozen preregs held
(fire E33, cut E25, commits, masked count 12, streak max 6) — 0
mismatched checks across 74 total (11+23+19+21), D3_FAILURES=0
everywhere, two runs byte-identical per fork.

## Answers

1. **How far does the home-turf advantage go?** The scaffold *works*
   flawlessly here — 4×4 codebook with a perceptual front-end, an
   abstain branch, and 10× persistence is a real step beyond wave4's
   2-context demo, and all three release schedules acquire cleanly
   with zero integrity failures. But "works" is not "best": plain
   deliberate teaching Pareto-dominates on this turf (4.1×/3.1×/5.5×
   faster to acquire, ~2× cheaper in audit entries, ties on integrity
   and persistence). These wins are unsurprising — they re-confirm
   wave4's known boundary, exactly as the program prereg said they
   would. Per the program verdict rules, G4 alone cannot crown
   scaffold the best path.
2. **Does any release schedule dominate?** No. R2 (fixed cut at
   commit) is the cheapest and loses nothing vs R1's learner-initiated
   fire — the verification streak buys nothing on outcome-specified
   tasks. R3's fade is the most expensive and buys nothing either;
   its only technical merit is that masked episodes freeze rather
   than corrupt the probe schedule. On home turf the release schedule
   is a cost knob, not a capability knob: pick the fixed cut.

## Honest notes

- The outcome channel in this trial is computed from the codebook by
  the harness, so the scaffold's "teacher doesn't need to state the
  procedure" advantage doesn't cash out here — the codebook knowledge
  lives in the harness either way. In a deployment where outcomes are
  *observed* rather than computed, that qualitative edge might
  matter; this trial doesn't measure it.
- Temptations are post-release by preregistered design (to keep
  release-timing predictions exact); pre-release scaffold resistance
  to temptation is untested in G4.
- N2 (program prereg): candidate actions are given, not generated;
  the perceptual front-end (argmax) is given substrate, not learned.

## Reproducibility

- Frozen preregs: commit `3df536db416141554b1b8fe8f781b0c1dc5e19b4`
  (before implementation).
- Implementation: this commit (see report). Runners: `run.sh` per
  fork — compile → 2 runs (sha256) → static checks (no-RNG grep,
  select-region signal ban, no-accumulation tokens) → verify every
  D3_CHECK → require D3_FAILURES,0.
- Run SHAs (evidence_run1 == evidence_run2, byte-identical): baseline
  `caae908521807e23566ba4bd88ff94e7bd239cf0d5c6d6ed31afc839e251471c`,
  R1 `0a695f5c7ffe93272e99cd3ee8f26f35ccc89a6af19cf03a8524786273e495f5`,
  R2 `4e6bf1ef024ab4a122786fae4c074e719a79f8a07d05ced176b7b2ba5e66dca4`,
  R3 `09e13ba89b9c6b9f505736f4375d56f2fe19556eba2ce0cf279d330ce6df0cff`.
- Evidence: `evidence_run1.txt`, `evidence_run2.txt`,
  `evidence_compile.txt` per fork.
