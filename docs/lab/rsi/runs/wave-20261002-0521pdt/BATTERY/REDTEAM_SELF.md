# REDTEAM_SELF.md: E10 battery self red team

Wave wave-20261002-0521pdt, lane BATTERY-E9. Date 2026-10-02.
Reviewer role: attack the battery itself, not the mechanisms. Written
by the same worker that built the battery; the discipline is to try to
void each world's evidential value and record where the attack
succeeds. Documentation rule observed: no em-dashes.

## 1. Reskin audit vs FW1-FW9

- M1-W1 (nesting: sum over chain-ends) vs all FW: no FW world nested
  two assemblers. New.
- M1-W2 (chained join, two value lookups) vs all FW: no FW world did
  joins. New (E9-E2 did one hop; this is two).
- M1-W3 (bootstrap fabrication) vs all FW: no FW world tested the
  fallback heuristic. New.
- M2-W1 (selection v2) vs FW6 (literal CHOICE contract): FW6 had a
  fixed correct literal; W1 has no correct literal (sealed mapping)
  and scores information gain. Different.
- M2-W2 (budget stopping) vs FW6/FW7: no goal, no contract; tests
  mechanism-controlled stopping. New.
- M2-W3 (population change) vs FW6: re-selection under mapping
  change. New.
- M3-W1 (orphan poisoning) vs FW5 (contradiction overwrite): FW5's
  bar REQUIRES last-write-wins; W1's bar punishes revising the wrong
  graph. Different demand on the revision machinery.
- M3-W2 (chained propagation) vs FW5: single contradiction vs
  stacked MAPs, depth 2. New.
- M3-W3 (specificity control) vs FW5: FW5 tested overwrite; W3 tests
  revert/no-op precision. Different.

## 2. Reskin audit vs the 1421pdt battery and E9

- M1-W1 vs E9-E1/E2/E3 (branch/join/depth): nesting is a fourth
  topology gap, not a variant of any. Not a reskin.
- M1-W2 vs E9-E2 (one-hop join): join depth 1->2, two sequential
  value lookups. Close family, materially different demand (the
  second lookup cannot even be framed as a followable path).
- M1-W3 vs E9-E3 (miss by depth cap): miss by fabrication vs miss by
  capacity. Different mechanism (fallback heuristic vs trial loop).
- M2-W1 vs E9-E1: different informant population (plausible liar
  truth+1, cross-key contrarian vs fixed table and constant
  flatterer), miss-first calibration (guide-gated exploration is
  informative here; E9-E1's calibration ACTs were wasted), 5+3 keys
  vs 6+4. Same family, materially different structure.
- M2-W2 vs E9-E3 (thrift): fixed suppression vs mechanism-controlled
  stopping under a budget. Different.
- M2-W3 vs E9-E1: population change mid-task with per-episode sealed
  PIs; the re-selection demand is new.
- M3-W1 vs everything: the orphan-poisoning family was queued by E9
  as untested; this is its first deliberate test. New.
- M3-W2 vs E9-E2 (amended, depth-1 propagation): depth-2 chained
  propagation. The link-3 orphan-dodge is reused deliberately so the
  bar isolates propagation.
- M3-W3 vs E9-E3 (success-then-revert): W3 scores the revert as
  CORRECT and adds the unlicensed-contradiction no-op. Control, not
  a kill; documented as such.

## 3. Bar calibration audit (per world)

- T-K5: degenerates do not pass (D0/D2 INVALID, D1 reaches scoring
  0/2). A constructor emitting nested sum-over-paths passes. Fair.
- T-K6: degenerates do not pass (D0 INVALID, D1/D2 reach scoring
  0/2). A value-join mechanism passes. Fair. The 60911/60912
  distractors are doing real work (D1 would otherwise pass probe 3
  by recency); verified by the D1 trace.
- T-K7: degenerates do not pass. A miss policy that distrusts
  coincidental invariance passes (returns -2). Fair; the demand is
  ignorance-admission, documented.
- T-K8: always-c fails (f) for every PI; rotate-1,2,3 gets 2/6 < 5
  for every PI (verified against the derived PI 1->A 2->C 3->B and
  by case analysis for all six). A genuinely discriminating
  mechanism passes (explore in the 5 miss-first calibration keys,
  exploit 5-6/6 in hidden). Fair.
- T-K9: always-NULL fails (a) -> WORLD-INVALID; always-INQ and
  rotate get 12 > 6 -> (b) FAIL for every PI. A stopping mechanism
  passes. Fair, with one noted softness (section 5).
- T-K10: always-c fails (d) for every PI combination (the 4/4-luck
  case is caught by distinctness); rotate gets exactly 2/4 < 3 for
  every combination (verified against derived bits 1,1 and by case
  analysis). A re-selecting mechanism passes. Fair.
- T-K11: degenerates do not pass (all INVALID). A reviser with a
  per-graph provenance lookup passes. Fair; this is the queued
  adversarial family.
- T-K12: degenerates do not pass (all INVALID). A downstream-
  propagating reviser passes (the new links are taught in-world).
  Fair.
- T-K13 (control): degenerates do not pass (D0/D2 INVALID, D1
  reaches scoring 0/2). The frozen mechanism passes, which is the
  point: the bar is passable and the battery is not a
  fail-everything machine.

## 4. Oracle audit

- M1-W1 bar probes: no data path computes 15/9 (all path values are
  3/5/7 or fan values; subset sums decline above 900). Confirmed.
- M1-W2 bar probes: the only length-2 path is [60201,60651];
  60671/60672 unreachable. Confirmed.
- M1-W3 bar probe: expected -2 never verifies; bootstrap ignores
  the oracle. Confirmed.
- M2 probes: CHOICE values are not oracle-derived. N/A.
- M3-W1/W2 bar probes: exact hits on stale taught facts; the trial
  loop is never reached, so the oracle cannot rescue a non-reviser;
  a reviser would have taught the expected value and the hit would
  return it. Confirmed.
- M3-W3 probes: exact hits on live taught facts (control).
  Confirmed.

No bar is oracle-passable.

## 5. Blemishes (do not void; recorded for future batteries)

**B1. T-K1 commit contamination.** The freeze commit d22862d07
contains 72 files from the concurrent ARENA lane (this worker's
`git commit` without a pathspec swept the shared index). Ruling:
T-K1's substance holds (prereg hash predates every E10 battery
artifact; only two BATTERY files are this lane's; zero E10
artifacts in the commit; hash unmodified after). The "contains
only" phrasing is not literally true; the deviation is recorded
here, not hidden. No history rewrite was performed (shared repo,
concurrent workers; the ARENA files are intact). Process lesson:
freeze commits must use pathspec-only `git commit -- <paths>`
when other lanes share the index.

**B2. T-K9 has no distinctness sub-bar.** A policy of
"emit 1 once per key, then emit NULL" (1-then-0) passes T-K9 when
PI(1)=A (as derived: bit 0 -> 1->A): 4 non-NULL ACTs <= 6, 4/4
probes correct, 4 keys early. It is defeated only when PI(1)=B.
No single trivial policy passes for EVERY PI, and the frozen
mechanism fails deterministically (12 ACTs), so the bar still
discriminates the test subject; but unlike T-K8/T-K10 it leaves a
PI-dependent 1-bit luck path. Future selection/budget bars should
carry a distinctness or cross-key-consistency sub-bar.

**B3. M3-W3 is a predicted-PASS control, not a kill.** Stated
openly in the prereg (section 6.9). Its evidential role is
precision mapping and battery honesty (bars are passable). It
does not dilute the M3 verdict (T-K11 and T-K12 both FAIL).

**B4. Second znc miscompile (AGENTS.md 2026-10-02).** All E10 Zag
tools were written with the safe-emit discipline and every
binary's stdout was byte-verified before use, including a
positive LEAKCHECK case. No output anomalies were observed in
this battery's tools.

## 6. Adversarial-to-strength honesty check

- M1-W1: engagement probes (forward 2-hop, the FW1/FW2 strength)
  pass in-world (2/2); the nesting demand is the single added
  step. Honest.
- M2-W1: engagement (a) proves ACTs fire after misses (6/6); the
  demand is that the firings carry information. Honest.
- M3-W1: MAP_B's promotion (which requires the trial to try and
  reject the decoy, creating the orphan) proves the machinery is
  live; the contradiction then exposes the lookup bug. Honest.

## 7. Overall battery verdict

Per-world: all nine worlds CALIBRATED (bars discriminate,
degenerates do not pass, competent mechanisms could pass,
oracle-proofed, leak-checked). The three MECHANISM-WEAK verdicts
stand on the calibrated portion. Blemishes B1-B4 do not void:
B1 is ruled on substance, B2 is a noted softness that does not
affect the test subject's deterministic FAIL, B3 is a documented
control, B4 was mitigated by construction.
