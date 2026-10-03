# SEALED_RESULTS.md: Battery E10 sealed execution record

Wave wave-20261002-0521pdt, lane BATTERY-E9. Date 2026-10-02.
Battery: E10, nine sealed worlds on TNN-2's three new mechanisms
(M1 runtime executable-graph construction; M2 learner-originated
uncertainty guiding action; M3 counterexample-driven revision).
Second battery built under the six triviality-review corrections
(CORRECTIONS.md); applies all six plus E9's queued lessons
(orphan-poisoning family, retrieval-based T-K15, pre-freeze index
audit).

## 1. Freeze and identity record

- Prereg: `PREREG_E10.md`, SHA-256
  `6d7cb92dbfe59a7622196f28bc55ac5c58c7e2c467c268b214df44fa98046952`,
  frozen alone in commit `d22862d07` before any battery artifact
  existed. Commit-order note (T-K1 ruling): the commit also contains
  72 files from the concurrent ARENA lane (shared-index sweep; see
  WORLDGEN.md and REDTEAM_SELF.md B1). Zero E10 battery artifacts
  were in the commit or existed before the prereg hash (verified by
  file listing and mtime order); the prereg is unmodified since
  (hash re-verified). T-K1 ruled PASS on substance, transparently.
- Frozen pins re-verified: tnn2.zag
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`;
  freeze_shim2_bin
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  (checked before every block run and after the battery); znc
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
  `git status` clean on both cognition paths.
- Sealed PIs (derived post-freeze from prereg hash bytes
  6d 7c b9 2d): W1: 1->A, 2->C, 3->B; W2: 1->A, 2->B;
  W3 ep A: 1->B, 2->A; ep B: 1->C, 2->A. Recorded in
  PI_RECORD.txt / PI_ENV.sh; identical for all 3 runs.
- Anti-smuggling grep for 60000-69999 over frozen cognition
  sources: zero matches (two coincidental hash fragments in the
  gitignored .zag-cache only; documented benign).

## 2. Process bars

- T-K1 (prereg ordering): PASS (substance ruling above).
- T-K2 (determinism): PASS. All 24 per-run artifacts byte-identical
  across 3 runs (sha256 equality of transcripts, grown worlds,
  driver logs, vocab/truths files, inspector outputs).
- T-K3 (frozen binary): PASS (pins above; shim checked before each
  of the 3 block runs and after).
- T-K4 (seal integrity): PASS. `sha256sum -c WORLD_MANIFEST.sha256`
  clean for all 28 files; cognition grep clean.
- T-K14 (retention): PASS, 12/12 collateral probes correct
  (m1w2 idx4, idx5; m1w3 idx3, idx4; m2w2 62091/62500, 62092/62500;
  m2w3 62091/62500, 62092/62500; m3w1 idx4, idx5; m3w2 idx6, idx7).
- T-K15 (no-leak audit): PASS. T-K4 grep clean; scorer LEAKCHECK
  clean on all 6 static worlds (no bar probe OBSERVE-taught); M2
  final probes exempt per prereg (scored as informant selection);
  per-world oracle-proof walks in prereg section 6 hold.

## 3. Mechanism bars (run 1; runs 2 and 3 byte-identical)

### M1 block

T-K5 (M1-E10-W1 nesting): FAIL. Engagement 2/2 PASS (3, 2: forward
2-hop composition fires in-world). Nesting probes 0/2 (both
ANSWER -2). The trial composes and sums but cannot nest them.

T-K6 (M1-E10-W2 chained join): FAIL. Engagement 2/2 PASS (direct
hits). Chained-join probes 0/2 (both -2). No data path exists for
either value lookup, let alone two in sequence.

T-K7 (M1-E10-W3 bootstrap): FAIL. Engagement 2/2 PASS. Bar probe:
60399, expected -2 (the invariant bootstrap fabricated an answer
from three coincidentally invariant distractor facts instead of
admitting ignorance).

### M2 block (VOCAB measured in situ: NULL_ACT=0, INQ_ACT=30)

T-K8 (M2-E10-W1 selection v2): FAIL. (a) PASS (6 hidden ACTs after
misses: inquiry fires); (b) 0/6 target A FAIL; (c) 0 target C PASS;
(d) 0/3 final probes FAIL (all -2: CHOICE 30 consults no
informant); (e) 6/6 budget PASS; (f) 1 distinct calibration CHOICE
FAIL.

T-K9 (M2-E10-W2 budget): FAIL. Vocab-verify PASS. (a) 12 non-NULL
ACTs PASS; (b) 12 > 6 FAIL (never stops: the gate re-fires while
any live guide's subject is ring-resident); (c) 0/4 FAIL;
(d) 0 keys stopped early FAIL.

T-K10 (M2-E10-W3 population change): FAIL. Vocab-verify PASS.
(a) PASS; (b) 0/4 FAIL; (c) 4/4 budget PASS; (d) 1 distinct FAIL.
No re-selection is possible with constant action content.

### M3 block

T-K11 (M3-E10-W1 orphan poisoning): FAIL. Validity 3/3 PASS
(MAP_A promotes at 65103; MAP_B promotes at 65104, its trial
genuinely trying and rejecting the decoy). Bar probe: 65103,
expected 65113 (t2_revise_graph patched MAP_B's rejected
candidate's orphan instead of MAP_A's live SETREG; re-execution
"succeeded" on the untouched graph; the live MAP never revised).
White-box diagnostic: MAP(65101,65509) ans=65103.

T-K12 (M3-E10-W2 chained propagation): FAIL. Validity 5/5 PASS
(A promotes at 66105; B at 66104; C at 66106; post-revision A
probe 66113: the link-3 trick kept the stale lookup clean, so the
upstream revision fired correctly). Bar probe: 66106, expected
66116 (no propagation through either downstream level).
Diagnostic: MAP(66101,66529) ans=66106 while MAP(66101,66509)
ans=66113.

T-K13 (M3-E10-W3 specificity control): PASS. Validity 4/4 PASS;
post-revert probe 67103 (revert retained the old answer, scored
correct); MAP_B unaffected 67113; unlicensed contradiction a
complete no-op; collateral hits.

## 4. Verdicts

- M1: MECHANISM-WEAK. Killing evidence: T-K5 0/2 (no nesting of
  assemblers; strength fires in-world and is insufficient), T-K6
  0/2 (no chained value join), T-K7 (fallback fabricates 60399
  instead of -2). The trial loop remains a fixed-topology
  per-probe search: chains, sums, counts, 1-hop, plus an
  uncalibrated invariance heuristic.
- M2: MECHANISM-WEAK. Killing evidence: T-K8 (b) 0/6, (d) 0/3,
  (f) 1 distinct (inquiry fires but carries no information);
  T-K9 (b) 12 > 6, (d) 0 early (no stopping decision possible);
  T-K10 (b) 0/4 (no adaptive re-selection). The presence gate
  works (all validity/vocab controls pass); everything beyond
  presence fails.
- M3: MECHANISM-WEAK. Killing evidence: T-K11 (revision patches a
  dead orphan; live graph untouched), T-K12 (no propagation through
  two downstream levels; upstream revision works). T-K13 passes as
  a control (revert and no-op precision are intact), which does
  not rescue the verdict: two of three bars FAIL.

No generality claim and no L3 claim is made (Criterion 0 status in
the prereg, section 10, is binding).

## 5. Notes and interpretations

- The T-K1 commit contamination (REDTEAM_SELF.md B1) is the
  battery's one process blemish; the substance ruling is recorded
  in section 1 and WORLDGEN.md. Future freeze commits must use
  pathspec-only `git commit -- <paths>`.
- T-K9's missing distinctness sub-bar (B2) is noted for future
  batteries; it does not affect the frozen mechanism's
  deterministic FAIL.
- Failure clustering by shared architectural cause (no-patch-
  treadmill rule): M1's three kills share one cause (the miss
  policy is a fixed-topology search with oracle verification and
  no compositional algebra: it cannot nest, join, or distrust its
  own fallback). M2's three kills share one cause (the action
  channel is a constant: selection is by bid among guides but the
  emitted value never varies, so no information flows from
  uncertainty to action). M3's two kills share one cause (revision
  is a single-schema local patch with a global stale-cell lookup
  and no dependency tracking: it patches the wrong graph and never
  revisits downstream licensees).
- General substrate hypotheses (not patch requests): (i) a
  constructor whose search space is itself learner-extensible
  (new topologies from the ISA, not three fixed assemblers);
  (ii) an action channel whose content is a function of the
  selected guide (addressing); (iii) revision with per-graph
  provenance and a dependency graph so contradictions propagate
  to licensees.

## 6. Degenerate calibration summary

18 degenerate runs (D0/D1/D2 over 6 static worlds, scored against
the frozen barspecs): 0 passes. 13 WORLD-INVALID (degenerate fails
engagement/validity), 5 FAIL reaching scoring (m1w1-D1, m1w2-D1,
m1w2-D2, m1w3-D1, m3w3-D1). M2: always-c fails the distinctness
sub-bars for every PI; rotate fails the correctness/budget
thresholds for every PI combination; always-NULL fails engagement
or scores 0. No trivial contestant passes any bar.

## 7. Queued next (for the parent orchestrator)

- The three shared-cause clusters above are the honest
  architectural read; each suggests a substrate hypothesis, not a
  patch. If a TNN-3 is ever built, its prereg should carry
  re-tests of T-K5/T-K9/T-K11 as regression bars (they are
  calibrated and non-trivial).
- T-K15's retrieval-based phrasing worked without the E9
  interpretation dispute; keep it.
- The freeze-commit index-sweep hazard (B1) should become a standing
  process rule: pathspec-only commits on freeze commits.
- The second znc miscompile (safe-emit discipline) is now load-
  bearing for all battery tooling; E9-era tools that use
  `_zag_print` for dynamic content should be treated as suspect
  until their stdout is byte-verified.
