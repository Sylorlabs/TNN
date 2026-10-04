# CORE FREEZE CHALLENGE: Post-Run Governance Audit

Date: 2026-09-30. Auditor: Core Freeze Post-Run Governance Auditor (independent of the run-phase worker).
Status: FREEZE-GOVERNANCE-AUDIT-PASS.
Scope: whether the Stage 2 run phase (97b28e6a6) honored the frozen protocol (66e3c3f38).

## Frozen bars governing the run

- Protocol: FREEZE_PROTOCOL.md, frozen at 66e3c3f38 (FREEZE-PROTOCOL-COMPLETE).
  Governing clauses: 2.3 (mechanical hash verification, void-on-mismatch),
  4 (9-world battery with per-world anti-smuggling provisions), 5 (adversary
  handoff rules, including 5.4 pre-freeze team blindness), 6 (six measurements),
  7 (verdicts: COMPLETE/VOID/INCOMPLETE), 8 (honest-scope predictions),
  10 (stage gates).
- Freeze: FREEZE_RECORD.md at 87ac95d08. Source b761efd90cb1, binary
  8733af3d2814, null state c35020473aed1b4642cd726cad727b63fff2824ad68cedd7ffb73c7cbd890479,
  toolchain 498abcb5. Void-on-mismatch rule stated affirmatively.
- Worlds: pre-freeze seven at e806d634e (W1,W2,W3,W4,W5,W7,W8); post-freeze
  two at 6d185ebce (W6,W9). 15 world files total.
- Run: RUN_RESULTS.md at 97b28e6a6 (FREEZE-RUN-COMPLETE).

## Hash chain (independently verified via git)

- 66e3c3f38, 87ac95d08, 97b28e6a6, e806d634e, 6d185ebce all resolve to commit
  objects (git cat-file -t).
- Ancestry: 66e3c3f38 is an ancestor of 87ac95d08; 87ac95d08 is an ancestor
  of 97b28e6a6 (git merge-base --is-ancestor, both clean).
- The frozen binary blob at 87ac95d08 hashes to 8733af3d28148263, matching
  FREEZE_RECORD.md. The working-tree binary at
  core_freeze/stage0/world_learn_bin currently hashes to the same value.
  The binary was not modified by the run.

## Audit findings

### (a) Binary hash verified before every world: PASS

The run harness run_world.sh embeds the K1 check: it recomputes sha256 of
the binary before each world invocation and exits 10 (VOID) on mismatch
against the frozen hash 8733af3d28148263. RUN_RESULTS.md reports all nine
worlds ran with no VOID triggered, and the binary hash was re-verified
after the full battery: MATCH. The auditor independently confirmed the
current binary matches the freeze record. Protocol 2.3 satisfied.

### (b) All 15 world-file seals verified: PASS

RUN_RESULTS.md lists all 15 world files with MATCH against the seal hashes
recorded in the design commits: 7 pre-freeze files against e806d634e seals
(W1 9c8cdf42, W2 33958a4d, W3 01b4ee0d, W4 5d9bf895, W5 f926ec7b,
W7 27986463, W8 277320be) and 8 adversary files against 6d185ebce seals
(w6_phaseA 9c952dd0, w6_phaseB 24f011f7, w6_controlA 4829f3e0,
w6_controlB 011dc7e2, w6b_phaseA d09d81ba, w6b_phaseB 1221425f,
w9_treeA 43351a79, w9_treeB 036ba3b0). No SEAL-BROKEN. Protocol 10
(Stage 2 gate) satisfied.

### (c) Source and binary unmodified: PASS

RUN_RESULTS.md reports the source hash re-verified after the battery:
MATCH (b761efd90cb1). The auditor independently verified the binary blob
at the freeze commit and the current working-tree binary both hash to
8733af3d28148263. Zero source delta at every check; the challenge is not
void under protocol 7. CAPABILITY SOURCE DELTA = 2 (zero) for all worlds.

### (d) W6 responder contract R1 matched the design: PASS

The adversary design (6d185ebce, section 3.2) specifies R1: release
w6_phaseB.txt iff Phase A stdout contains exactly "ANSWER 22001 22101 -2"
AND a "CHOICE 0" line occurs after it in output order; otherwise release
the control phase B. The auditor inspected battery/W6phaseA.out: it
contains "ANSWER 22001 22101 -2" followed in order by "CHOICE 0" (after
intervening EVICT/OBSERVE lines). Battery/W6phaseB.out begins with
"OBSERVED 22001 22101 7" (the reveal), confirming the treatment arm was
released per the contract. The control arm (W6ctrlA/B) ran without ACT
lines as designed. R1 was implemented exactly as specified; the reveal
gating is world-side logic, not learner machinery, per the design.

### (e) Pre-freeze blindness caveat (protocol 5.4): DISCLOSED, does not invalidate any world

Protocol 5.4 bars the pre-freeze world-design team from candidate-internals
knowledge. The design document (e806d634e) carries an explicit "honesty
note": predictions were derived from two frozen public documents
(stage0/INTERFACE.md and FREEZE_PROTOCOL.md section 8), with the designer
verifying the Stage 0 driver's lookup semantics to make predictions
mechanism-level rather than speculative. The note states the worlds "were
not adjusted to flatter the candidate" and that no world file was executed
against the binary before the run phase.

Assessment: the designer disclosed interface-conformance reasoning in
writing. Whether reading driver lookup semantics exceeds "the interface
spec alone" is a genuine gray area under 5.4, and the auditor records it
as a disclosed deviation from strict blindness, not a hidden one. It does
not invalidate any world because: (1) the reasoning basis was disclosed,
not concealed; (2) every world satisfies the anti-smuggling provisions
(no task labels; id blocks disjoint across worlds, verified A6; A5 source
audit clean with the one numeric collision on 900 cleared as dead
uncalled legacy code with different argument position and semantics);
(3) the purpose of 5.4, preventing the candidate from being tuned to world
content, was not violated: the candidate was frozen at 87ac95d08 before
the worlds were revealed at run time, and the worlds were sealed at
e806d634e before the freeze. No world is ruled INVALID on this ground.

### (f) W6 B4 dual reading presented without decision: PASS

RUN_RESULTS.md records both the adversary FAIL reading (B4 attribution:
the constant CHOICE 0 cannot encode learner-determined inquiry; scoring
otherwise credits compliant plumbing as inquiry, the exact false positive
W6 was built to expose) and the literalist PASS reading (B1-B3 numeric
bars; the fixed default does not branch on world identity). It states
verbatim: "This is a protocol-interpretation call. The runner does not
decide it. Flagged for the research director." The auditor likewise does
not decide it. The call remains banked for Micah.

## Additional honest-reporting checks

- The eviction tie-breaker pathology (unpredicted, dominates W4/W5/W6/W8/W9)
  is documented mechanistically with the observed signature, its impact per
  world, and the revised W4/W5 predictions. The W4/W5 prediction revisions
  revise the mechanism claim, not the frozen bar, per protocol 8.
- The C1 conditional-validity confound for W6-treatment and W9 is stated
  explicitly with white-box evidence (reveal triple evicted; 27/28 W9 edges
  evicted), not buried.
- The W8 recall sub-prediction revision (0/4 observed vs 4/4 predicted) is
  disclosed with the eviction cause.
- Scoring per protocol 9 is delivered for all nine worlds; no averaging
  into a single number.
- The boundary analysis (protocol 8, six predicted points plus the
  unpredicted finding) is delivered honestly, including which predictions
  were confirmed and which were revised.

## Verdict

FREEZE-GOVERNANCE-AUDIT-PASS. The run phase honored the frozen protocol:
mechanical hash verification at every gate, all world seals verified, zero
source delta, the W6 responder contract implemented as designed, the 5.4
blindness question disclosed in writing and assessed above, and the W6 B4
interpretation left undecided as required. No protocol violation found.
The run phase is governance-clean. Challenge-level verdict
FREEZE-CHALLENGE-COMPLETE stands as an instrument verdict; the learner
profile is 1/9 WORLD-PASS (W1 only).

## Process

Pure markdown and shell. No Python invoked. Dash check via
worker_snippets/check_no_dash.sh (clean). Contaminated paper
TNN_RESEARCH_PAPER_20260929.md untouched (zero diff). Frozen source and
binary unmodified (hashes re-verified). Commits local, owned paths only,
explicit pathspecs.
