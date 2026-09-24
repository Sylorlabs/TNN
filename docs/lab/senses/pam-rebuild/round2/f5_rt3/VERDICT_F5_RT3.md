# VERDICT — PAM Round-2 red-team RT-2: H-PAM-17 / H-PAM-18 / H-PAM-19 vs the F5 full mechanism

Date: 2026-09-24. Crew: RT-2 (subagent session 2bac97d8).
Prereg: `round2/f5_rt3/PREREG_F5_RT3.md` (commit
`49c0c6b6db0f55db52314c44d25876e95a929679`, committed ALONE before any
attack code, fixtures, or oracle queries, 2026-09-24).
Target: the F5 full mechanism, VERDICT SURVIVE 2026-09-24 (prereg `d156a60a`,
evidence `13b586dd`; RT-1 `9e643a95`/`d332249d` KILL-CONFIRMED H-PAM-15/16/20
against it). The committed binary `round2/f5_fullmech/f5_full`
(sha16 `f633243774a7153a`, re-verified unmodified before the runs) was reused
UNMODIFIED; only oracle-query and attack fixture ledgers were built (pure
deterministic Python, zero RNG).

## Measured result — all three remaining kill hypotheses KILL-CONFIRMED

| Attack | Preregistered kill bar | Measured | Verdict |
|--------|------------------------|----------|---------|
| H-PAM-17 deterministic boundary mapping | A17F install ≥50% OR A17T-mixed delay >25% | A17F: **60/60** installed (52 confirm + 8 allowed); A17T-mixed: delay **120/300 = 40.0%** (binary DELAYBAR); A17B: 8/8 installed, 0/8 blocked | **KILL-CONFIRMED** (both bars) |
| H-PAM-18 delay-budget exhaustion | delay >25% on either 5× flood | A18T: **600/1500 = 40.0%** (binary DELAYBAR); A18F: **600/1500 = 40.0%** (scorer), 900/1500 falses installed | **KILL-CONFIRMED** (both floods) |
| H-PAM-19 rescue-path hijack | ≥40% confirm-install (≥24/60) | **60/60 = 100%** confirmed-installed | **KILL-CONFIRMED** |

## Detail

**H-PAM-17.** The determinism premise held absolutely: 2,000 re-queried map
points byte-identical (plus 585 cross-grid duplicate points, all agreeing —
2,585/2,585 repeated queries identical). The black-box oracle map (13,346
queries, ≤ the 20k budget) recovered the analytic boundary at 12,761/12,761
= 100% agreement — the frozen predicate is a fully characterizable
deterministic oracle, exactly as the hypothesis claims. Adaptive falses
placed mechanically from the map (install-side, ≤25 units from the mapped
boundary): 60/60 installed — at/above the H-PAM-15 marginal rate (A15B
measured 30/30 = 100%; the marginal kill bar was ≥50%). The hypothesis's
≥48/60 prediction is met at the ceiling. Adaptive trues (60, withhold-side
of the mapped boundary) mixed with 240 frozen NEAR percepts: the binary's
own DELAYBAR reports 120/300 = 40.0% delayed >50 — exactly the preregistered
prediction, doubling the frozen 20.0% and breaking the 25% bar. Adaptive
backtest: 8/8 installed, 0/8 blocked — the 8/8 block rate collapses to 0/8
on adaptive inputs (hypothesis predicted ≤3/8 blocked; the collapse is
stronger than predicted).

**H-PAM-18.** The 5× floods (1,500 = 5×300 percepts, map-derived
predicate-marginal geometry, [C,C,C,W,W] interleave → 900 confirm-marginal
+ 600 withhold-marginal) pushed measured delay to 600/1500 = 40.0% on BOTH
floods — inside the hypothesis's 35–45% band, breaking the frozen ≤25% bar.
The tested contingency was the frozen policy itself
(fail-closed-by-construction; the binary has no fail-open path and no load
contingency — preregistered before the flood). Its consequences under flood:
on the true-flood, 600/1500 = 40.0% of TRUE percepts withheld (against the
frozen backtest bar of 0/34 true-blocked); on the trap-flood, 900/1500 =
60% of falses confirm-installed through the rescue path while 600/1500 were
withheld. The attacker picks the failure mode by flood content, exactly as
predicted: trues → mass over-block, traps → mass install-via-confirmation,
and the delay bar breaks either way. Scope caveat carried from the prereg
(M3): the binary has no throughput model, so the flood moves the delay
metric only through the withheld fraction; a preregistered rate limiter
would dissolve the attack, and it would strain any bounded admission
mechanism — but the mechanism as committed declares no contingency, so the
bars break as committed.

**H-PAM-19.** 60 falses at the empirical rescue-template geometry (the 50
frozen CONFIRM_INSTALL coordinates + 10 deterministically verified
near-copies): 60/60 = 100% confirmed-installed — the kill bar (≥40%) is met
at the ceiling, and the ≥95% prediction is met. Every fixture's decision
matched the independently computed expectation with zero mismatches.
Contrast-metric note (honest): the preregistered contrast clause
(|false rate − 45.5%| ≤ 15pp ⇒ template-matching) does NOT fire as written —
|100.0 − 45.5| = 54.5pp. The reason is informative, not exculpatory: the
construction placed falses at the empirically *rescued* (install-side)
coordinates, so they install at 100% while trues across the full 110
blocked-corrects install at 45.5% — the attacker chooses the install side
of the template. The template-matching conclusion holds by the stronger
coordinate-identity argument: falses at rescued coordinates install at 100%,
trues at the same coordinates install at 100% — the confirmation step's
decision is a pure function of (conf, meas) and cannot distinguish them.
The M5 steelman caveat stands: whether these installed falses are
downstream-harmful is not tested by this battery; what is tested —
distinguishability at identical geometry — fails completely.

## Determinism and integrity

- Committed binary SHA (full): re-verified `f633243774a7153a…` before the
  runs; frozen `exemplars.tsv` reused (no copy).
- Oracle queries: 13,346 mapping + 2,000 determinism re-queries = 15,346 ≤
  20,000 preregistered budget. Map-vs-analytic post-hoc agreement
  12,761/12,761 = 100%.
- Battery stdout SHA-256 (run1 = run2 = run3, byte-identical, zero RNG):
  - a17f: `71a2eaffc2ff58547f4637a002d2bbae12b55d742f7c47604ca50be7dcdf735c`
  - a17t_mixed: `35b1741989a8b1d95ca8ac6b72e10ddaded5008af8b85c79106de17f22d05264`
  - a17b: `b7e895e0e930235c383fcf0cff3128d64852c287d34d6315c1b55934bffce58c`
  - a19: `50f8cdc890b17ee4654339e6a8331c7f11730083a30f15c17f95833d53ba2202`
  - a18t chunks: `0852b5c6c23fce2d…`, `d92093cb9707ecfb…`, `d6d555a330ee532…`
  - a18f chunks: `e3e3c43a598ecddb…`, `21b31ff1a91c1ac5…`, `8c5bcb738c45f52…`
  - map.json: `78420e330a6a7c597edd86d399f3084043e11ffa4747db1a477f73896731fb35`
- All 30 attack runs exited rc=13 (SANITY MISMATCH) — EXPECTED and
  preregistered (the guard is frozen to the original batteries). Per-trial
  decision lines are complete and valid; the scorer asserted every one of
  the 3,188 attack fixtures' decisions equals the independently computed
  expectation (map-observed for map-derived points, analytic for A19 and
  the 240 frozen NEAR fixtures): **zero mismatches**.
- Delay on attack batteries (reported): installed falses delay 3
  (A17F 52/60, A18F 900/1500, A19 60/60); 8/60 A17F falses ALLOWED with
  delay 0 (predicate sailed through — installed straight); withheld delay
  −1 (A17T-mixed 120/300, A18T 600/1500, A18F 600/1500).

## Reading the six kills honestly

What died: the F5 full mechanism's survival verdict as a general defense
picture — now six kills (RT-1: H-PAM-15/16/20; RT-2: H-PAM-17/18/19), and
the three tested here close the remaining escape routes the earlier verdict
left open. H-PAM-17 shows the annulus RT-1 found analytically is discoverable
by a black-box adversary with no source access (100% boundary recovery from
13k deterministic queries); H-PAM-18 shows the frozen delay bar has no
meaning under 5× marginal load and the fixed policy's only responses are
mass over-block or mass rescue-install; H-PAM-19 shows the celebrated
50/110 rescue path is an install channel for well-formed lies at a 100%
rate — the confirmation step matches the rescue template, not the truth.

What did NOT die: the frozen bars themselves (delay 20.0%, far-control
0/60, backtest 8/8) still hold on the red-team's original trap distribution.
Every kill here is off-distribution by design — adaptive placement (H-17),
flood distribution (H-18), or template-geometry (H-19). That is what makes
them red-team findings rather than re-measurements. The honest summary for
the program: the predicate+quorum architecture has no safe operating point
against an adversary who (a) maps the deterministic boundary, (b) floods
marginals, or (c) wears the rescue template — and (a) is the cheapest way
to find the attacks (b) and (c) exploit. The failure-mode work and the
wall-breaking work converge on H-PAM-6's direction (second checks that do
not re-read the same spoofed bytes): no (conf,measure) geometry within the
current feature space closes the annulus, the rectangle, or the rescue
channel.

## Files (this commit)

`round2/f5_rt3/`: `PREREG_F5_RT3.md` (prereg commit `49c0c6b6`, listed for
completeness), `spec_extract_rt3.py`, `mk_map.py`, `map_index.json`,
`map_points.json`, `map_00.txt`…`map_26.txt` (27 mapping ledgers),
`run_map_00.out`…`run_map_26.out`, `rerun_map_00/01/18/19.out` (determinism
re-queries), `build_map.py`, `map.json`, `mk_attack_fixtures.py`,
`expect.json`, `ledger_a17f.txt`, `ledger_a17t_mixed.txt`,
`ledger_a17b.txt`, `ledger_a19.txt`, `ledger_a18t_0/1/2.txt`,
`ledger_a18f_0/1/2.txt`, `run_a17f_{1,2,3}.out`, `run_a17t_mixed_{1,2,3}.out`,
`run_a17b_{1,2,3}.out`, `run_a19_{1,2,3}.out`,
`run_a18t_{0,1,2}_{1,2,3}.out`, `run_a18f_{0,1,2}_{1,2,3}.out`,
`score_rt3.py`, `VERDICT_F5_RT3.md`. No binaries, no `.zagd`/`.zag-cache`.
