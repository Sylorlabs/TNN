# REPORT: COMP lane, wave-20261002-1121pdt (ADV-A adversarial battery)

Worker: lane-comp-20261002-1121pdt. Task: queue item 1, adversarial
testing of the unified `satisfy` composition operation.

## Verdict line: BUILD-PASS; mechanism verdict: SURVIVES-ADV-A

The battery was built and run per the frozen prereg (d516c1da6):
frozen mechanism (zero edits), 18 tests, 3x byte-identical builds,
3x byte-identical runs. Kill bars KB1, KB2, KB3, KB4a, KB4b, KB5a,
KB6 all hold; PF-1a/PF-1b pass, so no downgrade to
SURVIVES-SEALED-ONLY. No breaker produced a wrong-answer promotion,
a hang, or dishonest attribution. No L3 claimed (C0-C/C0-D unmet).

## Numbers

- Sealed supervised: 15/15 PASS (TPF-1, TPF-2, B1, B2, B3S, B4, B5,
  B6, B7, B8, PM-1a, PM-1b, PF-1a, PF-1b) plus TPF-3 unsupervised PASS.
  16/16 scored tests pass; B3U FAILS as predicted (characterization).
- Trial-path-free battery: 3/3 (TPF-1/2/3), all with SAT-SEGS/SAT-FIX
  markers and exact 11-entry relseq [1,1,2,2,3,3,3,1,1,2,2],
  terminal 112. Trial reach (k<=4) structurally excluded.
- Attribution honesty: B4 ans=105 via trial, zero SAT markers, zero
  type-14 edges on the rel-70 MAP; B5 ans=-2, no markers.
- Timing: B1+B2+B7 = 16.4 s wall (bars 120/60/300 s). D exhausts 40
  eight-edge distractor subtrees where A stalled 50+ min on 40
  single-fact distractors: measured robustness difference.
- Predictions: 17/17 correct, including B3U FAIL (terminal 914),
  B4U INFO (terminal 103), PF-1c INFO (terminal 106).
- Determinism: builds 441bc63a... x3; runs af24011a... x3.
- Probe-menu/source-audit: source audit clean (zero test-value
  literals; zero compose code hits); PM-1a/b both PASS, expected
  selects among valid completions (BOUND: no intrinsic preference).

## Bounds found (not kills; all predicted in the frozen prereg)

1. Unsupervised satisfy is greedy and order-committed: B3U promotes
   the distractor composite (terminal 914); PF-1c commits to the dead
   DAG branch (terminal 106). Two independent demonstrations.
2. No intrinsic tie-break among multiple valid compositions (PM-1):
   the expected value does all the selecting.
3. Unsupervised promotes partial composites when stuck rather than
   abstaining (B4U: terminal 103, relseq [1,1]).
4. Latent: t2_gather 96-path cap could truncate correct groundings
   past ~50 same-node branches (untested; future breaker).

## Keep / discard / queued

- Keep: `satisfy` (patch_d.zag, frozen SHA df1d0faa...) as the working
  single composition operation; it now has adversarial survival
  evidence (trial-path-free battery, 8 breaker families, post-freeze
  diamond-DAG family, probe-menu/source-audit pass).
- Discard: nothing this wave.
- Queued: (1) t2_gather 96-cap breaker (60+ same-node branches,
  correct taught last); (2) composition battery where component MAPs
  are NOT trial-promoted (end the training-side trial dependence);
  (3) independent-adversary sealed family (C0-C) before any
  L3-adjacent claim; (4) revision/reuse of composites under memory
  pressure in one continuing learner (0521 queue item 4, still open).

## Commits (lane-comp-20261002-1121pdt, local only, never pushed)

- d8c5d740a NAMECHECK Step 0 toolchain guard (safebin; python3
  absent; znc=/home/hatch/safebin/znc).
- d516c1da6 PREREG_ADV frozen ALONE (kill bars KB1..KB7).
- 21b881c9e Implementation: driver_adv/shim_adv/asm_adv, frozen
  mechanism region (SHA 627ff98a...), 3x byte-identical builds+runs.
- 9976fae28 POSTFREEZE_PF1 design record (post-mechanism-freeze).
- (this commit) SEALED_EVAL_ADV.md, REDTEAM_ADV.md, REPORT.md.

## Provenance

- Mechanism inherited byte-identical from 0521pdt COMP
  (docs/lab/rsi/runs/wave-20261002-0521pdt/COMP/): patch_d.zag,
  substrate lines 1..1677 of cmp_full_c via full_d.zag lines 1..2027.
  Nothing modified; lineage verified by SHA at assembly time.
- 0821pdt lane branch (lane-comp-20261002-0821pdt) consulted for
  provenance only; no code or state inherited from it.
- No Python invoked anywhere in this lane (safebin PATH throughout;
  Step 0 evidence in NAMECHECK.md). No em-dashes in docs
  (check_no_dash.sh clean).

## Fork-testing scope note

Standing rule 3 (fork testing) was scoped: the artifact under test is
a frozen mechanism (SHA-pinned), not a branch tip, so per-branch
battery runs would not discriminate anything about `satisfy`; the
battery ran against the byte-identical frozen construction rebuilt
3x deterministically. Branch enumeration for the record: this lane
used only lane-comp-20261002-1121pdt; prior branches
lane-comp-20261002-0821pdt and the 0521 record were read-only sources.
