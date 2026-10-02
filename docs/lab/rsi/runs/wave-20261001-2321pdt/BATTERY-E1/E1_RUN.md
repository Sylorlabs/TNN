# E1_RUN.md -- Discriminating experiment E1 execution and verdict

Wave: wave-20261001-2321pdt, lane BATTERY-E1.
Prereg: PREREG_E1.md, frozen alone at commit 793abbf65, SHA-256
7632cf5a870ac0a71934fbac8274fc5950756d2f93c6d9be127ab827bd84e03c
(re-verified unchanged after the battery). Executed: 2026-10-02.
All work pure Zag (pinned znc) and shell; safebin PATH; no Python
invoked. Frozen binary used as-is; the inspector is an external
read-only probe.

Prediction miss (recorded plainly): the prereg predicted
E1-ABSENT. The observed verdict is E1-FIRSTCLASS. The white-box
inspector falsified the prediction; the evidence below is what the
frozen instrument returned.

## Process bars (battery validity)

- E1-K1 (prereg ordering): PASS. Prereg committed alone at
  793abbf65; first world/tool commit aa38427b8 strictly after;
  prereg SHA-256 re-verified unchanged.
- E1-K2 (determinism): PASS. All 4 world transcripts byte-identical
  across 3 fresh-state runs (cmp clean); per-world state.bin
  SHA-256 equal across the 3 runs (w1 a45eb0e1bc79d310156af4fe603
  c08db55319ea02ccbee7068c3aeb5f4504651; w2 d8170450f7cf47e84a74c
  3e4a076d9b67c026d7d26a7203500dcc6d25a89f9c1; w3 f71fc788edad996d
  f5df84d7a7ffcf02200c272ced3d897f7dded3e39cde520c; w4 c5e0e9b26444
  3c0fbb9229aa68005b02470382662954f212cb7f9d832fda22c).
- E1-K3 (frozen binary): PASS. freeze_shim2_bin hashes to
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  and tnn2.zag to
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  before and after; zero modifications under frozen paths.
- E1-K4 (seal integrity): PASS. E1_MANIFEST.sha256 verified (4/4
  OK); grep of 71000-71999 over tnn2.zag and freeze_shim2_bin
  returns zero matches.
- E1-K6 (no-leak): PASS. e1_audit_noleak reports LEAKS 0.

## Calibration gates

- Competent control: checker prints DERIVED=1 FIRSTCLASS=1 on the
  synthetic W1-conformant report (PASS).
- Degenerate control: checker prints DERIVED=0 on all four checks
  (PASS).
- Inspector machinery cross-check: e1_inspect_state on the
  committed v3 m1/m3 state bins reproduces the v3_inspect STRUCTURE
  lines exactly (m1: id=106 and id=130 with identical
  subj/rel/answer; m3: 7 structures); the widened licensing is the
  only delta (PASS).
- K-C0A audit: PASS. Zero 71xxx literals in the inspector; QUERY
  never read (oracle-blind by construction); predicate-vocabulary
  diff vs v3_inspect_state shows only the removal of the
  subject==ms restriction; world parameters live only in the
  checker as frozen bar data.

## Per-world results (frozen TNN-2; identical across 3 runs)

### E1-W1: construction vs retrieval -- DERIVED=0, VALID=1

Inspector: STRUCTURES 0. No persistent structure of any kind
survives the stream, derived or flat. Transcript: probes return
71999/71999 (the taught flat wrong fact); validity probes hit.
The flat fact answers with no persistent structure behind it.

### E1-W2: derived-fact contradiction -- DERIVED=1, BYPASS=1, VALID=1

Inspector: exactly one persistent structure, id=13, subj=71201
rel=71709 answer=71203, EVIDENCE (71201,71701,71202)
(71202,71702,71203) count=2. Both chain hops are licensed; the
derived answer 71203 was never taught on 71709. This is a genuine
licensed derived structure, and it survives the contradiction:
the post-contradiction state still carries answer 71203.
Transcript: promotion probes return 71203/71203; the bar probe
(ANSWER[2]) returns 71213; validity probes hit. The contradiction
is honored by direct-fact shadowing while the derived structure
persists untouched underneath. Clean SUBORDINATED instance: the
derived structure exists and the behavior operators bypass it.

### E1-W3: cross-relation revision transfer -- DERIVED=0, VALID=1

Inspector: two structures, both single-evidence and per-instance:
id=20 subj=71301 rel=71809 answer=71321 EVIDENCE
(71301,71801,71321); id=34 subj=71401 rel=71819 answer=71411
EVIDENCE (71401,71802,71411). No structure on rel=71801 carries
both-phase evidence; no law-level derived structure exists.
Transcript: revised-relation probe 71321 (per-key patch works);
transfer probe 71411 (original law; no transfer); validity hits.
White-box confirmation of per-key patching with no law layer.

### E1-W4: clean composition -- DERIVED=1, FIRSTCLASS=1, VALID=1

Inspector: two licensed derived structures. id=15 subj=71501
rel=71519 answer=71595 EVIDENCE (71501,71511,71591)
(71591,71512,71595); id=26 subj=71502 rel=71519 answer=71596
EVIDENCE (71502,71511,71592) (71592,71512,71596). Both hops
licensed for each; neither derived answer was taught on 71519.
Transcript: probes return 71595/71596; validity probes hit.
FIRSTCLASS per the frozen rule.

## Verdict: E1-FIRSTCLASS

D = {W2, W4} (E1-VALID on all runs, DERIVED=1 on all 3 runs each).
W4 has FIRSTCLASS=1. Per the frozen decision rule (PREREG_E1
section 4): E1-FIRSTCLASS.

## What this decides for H1c (Cluster 1)

H1c as stated ("no persistent representation of composed
procedures or laws exists at all") is KILLED by white-box
evidence. Licensed derived structures persist in frozen TNN-2
state: W2 id=13 and W4 id=15/id=26, each with multi-hop licensed
evidence and derived answers never directly taught, consistent
across 3 runs.

The refined picture, per world:

- W1: derived absent; the flat layer answers (71999) with zero
  persistent structures. Read-path precedence inversion (H1a) in
  its purest form: there is not even a flat persistent structure
  to compete; the 1-hop fact layer decides.
- W2: derived present but subordinated. The derived structure
  (answer 71203) persists through the contradiction; the answer
  operator returns the flat direct fact (71213). This is the exact
  "present but subordinated" signature E1 was built to
  discriminate, and it is observed cleanly.
- W3: no law-level derived structure; per-instance promoted
  structures only. Supports H1b (instance-only write path): the
  contradiction writes land on instances, and nothing aggregates
  them into a standing law representation.
- W4: derived structures present and probes return the derived
  answers. FIRSTCLASS per the frozen rule, with one recorded
  confound: the behavioral leg cannot distinguish
  structure-driven answers from oracle-verified BFS traversal
  (the PF-A2 caveat instrument property; H1d is E3's question).
  The structural leg (licensed derived structures exist in
  persistent state) is unconfounded and is what kills H1c.

Architectural note for the cluster analysis: the persistent
tag-20 structure layer is where derivation lives; flat facts
answer without leaving persistent structures (W1: STRUCTURES 0
yet 71999 returned; W2: the 71213 contradiction fact leaves no
structure yet drives the bar probe). The read path consults the
flat instance-fact layer first and it wins whenever it has an
entry. Cluster 1's shared cause therefore refines from "no derived
structures" to "derived structures exist but have no privileged
standing in the read path; the flat layer outranks them." The
cluster name DERIVATION SUBORDINATION is vindicated as the deeper
cause; H1c (the absence form) is dead and H1a (read-path
precedence inversion) wins for W1/W2, with W3 supporting H1b and
W4's behavioral leg reserved for E3/H1d.

## No-patch-treadmill compliance

No repair is proposed. E1 is a discriminating experiment; its
outcome goes back into the cluster analysis as decided evidence
for H1c. A confirmed substrate change (a privileged standing
layer for derived structures in the read path) would be one
general change behind W1, W2, and the PF-A1/PF-C1 signatures at
once, but that is TNN-3 business after E2/E3, not this lane.

## Criterion 0 status

Unchanged from the prereg: C0-A through C0-D NOT MET. Nothing
here is L3, L3-adjacent, or progress toward L3. The derived
structures are frozen-mechanism artifacts (trial-constructed
graphs), not learner-invented representations.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E1/
  PREREG_E1.md (frozen alone at 793abbf65)
- Tools: e1_worldgen.zag, e1_inspect_state.zag,
  e1_struct_check.zag, e1_controls.zag, e1_audit_noleak.zag
  (and _bin binaries)
- Worlds and manifest: e1_worlds/ (E1_MANIFEST.sha256; world
  SHA-256: w1 90bae7c8b8fde1af29f7a22e17d694e73d3e5c00d65f02967
  3fe762d6cc56dd4, w2 bead5b753da6c2a2b26805f9e2386fd34fb821ab15
  6c7e9d, w3 17d16defbd9eb48dc29864f1bd14d76c57e1303d7e5a9d8a16
  8315a806a1e71a, w4 e0293a3e88db53d73ceae5e34bcdcb6a017632fab08
  b4d15d064dc6167dd73ee)
- Transcripts, state bins, inspector reports, check outputs:
  e1_runs/ (per-world per-run .trans/.bin, _inspect_*.txt,
  _check_*.txt)
- Control outputs: e1_controls_out/
