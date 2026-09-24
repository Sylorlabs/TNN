# VERDICT — PAM Round-2 red-team RT-1: H-PAM-15 / H-PAM-16 / H-PAM-20 vs the F5 full mechanism

Date: 2026-09-24. Crew: RT-1 (subagent session 858e3500).
Prereg: `round2/f5_rt2/PREREG_F5_RT2.md` (commit
`9e643a9541b5d9a17d3d1c9fe63369bb3b3ea7f5`, committed ALONE before any attack
code or fixtures, 2026-09-24).
Target: the F5 full mechanism, VERDICT SURVIVE 2026-09-24 (prereg `d156a60a`,
evidence `13b586dd`). The committed binary `round2/f5_fullmech/f5_full` was
reused UNMODIFIED; only new attack fixture ledgers were built (pure
deterministic Python generator, zero RNG).

## Measured result — all three attacks KILL-CONFIRMED

| Attack | Preregistered kill bar | Measured | Verdict |
|--------|------------------------|----------|---------|
| H-PAM-15 cross-crop coherent spoof | either sub-battery installs ≥15/30 | A15A interior: **0/30** installed (30/30 withheld); A15B marginal: **30/30** installed (30/30 CONFIRM+INSTALL, delay 3) | **KILL-CONFIRMED** (via A15B) |
| H-PAM-16 transient single-crop injection | net false-install ≥24/60 (40%) | **60/60** falses CONFIRM+INSTALL (delay 3); true-transient controls 30/30 installed | **KILL-CONFIRMED** |
| H-PAM-20 rectangle farming (K=40) | no rectangle policy beats false-install <50% AND true-withhold <50% | mechanism policy: 0/40 false-install, **7/7** true-withhold; P1 counterfactual: 40/40 false-install | **KILL-CONFIRMED** (logical dilemma) |

## Detail

**H-PAM-15.** The interior sub-battery (A15A), built EXACTLY as the hypothesis
specified (30 TMB-5 falses inside the 29/17 exemplar-cluster interior),
installed 0/30 — the hypothesis's ≥24/30 prediction is falsified, because its
geometric premise was wrong: the extraction script proved BEFORE the runs that
the frozen predicate's ±150/±2000 window fires everywhere in the interior.
The interior is the mechanism's stronghold, not its blind spot; the
hypothesis's parenthetical ("so the frozen predicate's trap window does not
fire") was a geometric error, documented in the prereg §2/M2. The marginal
sub-battery (A15B) — 30 falses that trip the predicate but sit in the
predicate-window-minus-jitter-expanded-core annulus, crop-coherent by
framework construction — was installed 30/30 by unanimous 3-0 quorum votes.
The quorum corroborated the lie exactly as predicted (≥21/30). Stage
attribution: the predicate did its job (30/30 blocked); the QUORUM killed it.

**H-PAM-16.** 60 falses at rep=1 edge geometry (predicate trips; exactly one
jittered crop lands inside the confirmation core → 1 WITHHOLD vote vs 2
INSTALL → installed): 60/60 CONFIRM+INSTALL, every fixture's decision
matching the script-computed (blocked, rep=1) expectation with zero
mismatches. The 30 true-transient controls at identical geometry were also
installed 30/30 — the hypothesis's steelman confirmed empirically: the
confirmation step cannot distinguish a false transient from a true one, and
the "rescue" behavior IS the attack surface. The 2/3-to-withhold quorum has
no safe operating point against a crop-aware adversary: H-PAM-15 wins at
rep=0 (3-0), H-PAM-16 wins at rep=1 (2-1); only rep≥2 (the red-team's trap
distribution) is defended.

**H-PAM-20.** 40 planted falses interleaved with the 7 conceded trues
(conf 770–830, meas 2185–2215 vs the trues' 770–830 × 2200; max L1 distance
from any false to the nearest true = 20; no mechanism-legal feature separates
them — the mechanism gave all 47 identical BLOCKED→WITHHOLD decisions).
Measured: 0/40 falses installed, 7/7 in-rectangle trues withheld. The
mechanism's only (conf,measure)-legal policy withholds 100% of in-rectangle
trues (≥50% bar failed); the P1 counterfactual (install in-rectangle)
installs 100% of falses (≥50% bar failed). No policy beats both bars: the
conceded 7-percept residual is a scalable defender's dilemma, exactly the
logical kill H-PAM-20 predicted. This kills the verdict's *residual
tolerance*, not the frozen bars (delay/far-control/backtest were not
re-measured on this battery and are unaffected).

## Determinism and integrity

- Committed binary SHA (first 16): `f633243774a7153a`; frozen
  `exemplars.tsv` reused.
- Battery stdout SHA-256 (run1 = run2 = run3, byte-identical, zero RNG):
  - a15: `61b882e4a5c9ad655886734192eabcd200037ca461c77d66af35769aead59fcb`
  - a16: `9cb89dc5562f69517a99fc58e105c9d601ded096c5d7882396d15046d1e652df`
  - a20: `21964d45dd6841d1b76eff3334b5d9d0b4206473d3509ba476052b4247222f56`
- All 9 runs exited rc=13 (SANITY MISMATCH) — EXPECTED and preregistered:
  the binary's sanity guard is frozen to the original batteries and no
  attack battery can satisfy it. Per-trial decision lines are complete and
  valid; the scorer asserted every one of the 197 fixtures' decisions equals
  the independently script-computed (blocked, rep, decision) expectation:
  **zero mismatches**.
- Delay on attack batteries (reported): installed falses delay 3
  (A15B 30/30, A16F 60/60, A16T 30/30); withheld delay ∞ (A15A 30/30, A20
  47/47). No installed false had delay 0 — every installed false passed
  through the full 3-crop confirmation.

## Reading the triple kill honestly

What died: the F5 full mechanism's *survival verdict* as a general defense
picture. The quorum — everything the repair added over the killed
tightened-window version — is a coherence detector, not an admission
security mechanism: any false placed in the annulus between the predicate
window (150/2000) and the jitter-expanded confirmation core (130/950)
installs, and the vote split (3-0 vs 2-1) merely records how deep in the
annulus it sits. The interior stronghold (A15A 0/30) and the rectangle
withhold (A20 40/40 blocked) show the mechanism working exactly as designed —
which is precisely H-PAM-20's point: the design's correct operation IS the
dilemma.

What did NOT die: the frozen bars themselves (delay 20.0%, far-control 0/60,
backtest 8/8) were measured on the red-team's trap distribution and still
hold there. The kills are off-distribution by design — that is what makes
them red-team findings rather than re-measurements.

Consequence for the program: the failure-mode work and the wall-breaking
work converge — the natural next defense is H-PAM-6's direction (second
checks that do not re-read the same spoofed bytes), since no (conf,measure)
geometry within the current feature space closes the annulus or the
rectangle. H-PAM-17 (deterministic boundary mapping) would now be the
cheapest way to *find* the annulus adaptively; H-PAM-21 (R2-3 audit) is
corroborated by the vote-split pattern (rep=0/1/3 determined by one
geometric placement, effective independent samples ≈ 1).

## Files (this commit)

`round2/f5_rt2/`: `PREREG_F5_RT2.md` (prereg commit `9e643a95`, listed for
completeness), `spec_extract_rt2.py`, `mk_attack_fixtures.py`,
`ledger_a15.txt` (`1addc13a…`), `ledger_a16.txt` (`68833066a…`),
`ledger_a20.txt` (`ff7e73483…`), `expect.json`, `score_rt2.py`,
`run_a15_{1,2,3}.out`, `run_a16_{1,2,3}.out`, `run_a20_{1,2,3}.out`,
`VERDICT_F5_RT2.md`. No binaries, no `.zagd`/`.zag-cache`.
