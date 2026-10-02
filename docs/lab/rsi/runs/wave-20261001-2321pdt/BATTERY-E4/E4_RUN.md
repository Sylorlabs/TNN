# E4_RUN.md -- Discriminating experiment E4 execution and verdict

Wave: wave-20261001-2321pdt, lane BATTERY-E4.
Prereg: PREREG_E4.md, frozen at commit b63f80289, SHA-256
b3fd77c2c1c4037ded940072fa147d6fd0a1fd912ac0054038d487bbbca40b74
(re-verified unchanged after the battery; backup copy retained in
the lane scratch). Executed: 2026-10-02. All work pure Zag (pinned
znc) and shell; safebin PATH; no Python invoked. Frozen binary used
as-is; the inspector is an external read-only probe.

Prediction (recorded in the prereg before execution): E4-PRECEDENCE,
from the frozen ev_observe/revise_on_contradict mechanics and the
E1-W2 survival precedent. The observed verdict is E4-PRECEDENCE.
The prediction is confirmed.

## Process bars (battery validity)

- E4-K1 (prereg ordering): PASS with a documented race. The prereg
  was staged for a solo commit, but the ARENA5 worker's commit
  b63f80289 (2026-10-02 07:11:30 UTC) swept the staged files; the
  prereg is therefore frozen inside a shared commit that also
  carries the ARENA5 prereg. Substantively the bar holds: b63f80289
  is the first commit containing any E4 file, it contains no E4
  world file, spec file, or tool source (only PREREG_E4.md and
  NAMECHECK.md), and the prereg SHA-256 is unchanged after the
  battery. No E4 implementation file was created before b63f80289.
- E4-K2 (determinism): PASS. Both world transcripts byte-identical
  across 3 fresh-state runs (cmp clean); per-world state.bin
  SHA-256 equal across the 3 runs (w0
  7bfbed3389e5f6892c370dc76f6c9c6c74cae29f3314b2ec55054602b5887d03;
  w1
  fc5279f9204b3551b2d0170e9bd348d9d57610e3a3955c052396b704087889e2).
  Inspector reports identical across the 3 runs per world.
- E4-K3 (frozen binary): PASS. freeze_shim2_bin hashes to
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  and tnn2.zag to
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  before and after; zero modifications under frozen paths.
- E4-K4 (seal integrity): PASS. E4_MANIFEST.sha256 verified (2/2
  OK); grep of 72000-72999 over tnn2.zag and freeze_shim2_bin
  returns zero matches (binaries unchanged per E4-K3, so the
  pre-freeze seal still holds).
- E4-K6 (no-leak): PASS. e4_audit_noleak reports LEAKS 0
  (byte-identical to the E1 audit; its BAR line carries the E1-K6
  lineage label).

## Calibration gates

- Competent controls: checker prints DERIVED=1 PREFLAT=1 POST=1
  VALID=1 on the synthetic W1-conformant report (PASS) and
  DERIVED=1 FIRSTCLASS=1 VALID=1 on the synthetic W0-conformant
  report (PASS).
- Degenerate control: checker prints DERIVED=0 for both checks
  (PASS).
- Inspector machinery cross-check: e4_inspect_state_bin on the
  committed E1 W2 state bin plus the committed E1 W2 world file
  reproduces the committed e1_w2_inspect_r1.txt STRUCTURE lines
  exactly (PASS).
- K-C0A audit: PASS. e4_inspect_state.zag is byte-identical to the
  committed e1_inspect_state.zag (cmp clean); zero 71xxx/72xxx
  literals by grep; QUERY never read (oracle-blind inherited);
  world parameters only in e4_struct_check.zag as frozen bar data.

## Per-world results (frozen TNN-2; identical across 3 runs)

### E4-W0: control (no flat wrong fact) -- DERIVED=1, FIRSTCLASS=1, VALID=1

Inspector: exactly one persistent structure, id=13, subj=72101
rel=72119 answer=72195, EVIDENCE (72101,72111,72191)
(72191,72112,72195) count=2. Both chain hops licensed; the derived
answer 72195 was never taught on 72119. Transcript: promotion
probes return 72195/72195; validity probes return 72191/72195.
Baseline holds: the derived structure forms cleanly and drives the
probes with no flat competition.

### E4-W1: precedence-reversal -- DERIVED=1, PREFLAT=1, POST=1, VALID=1

Inspector: exactly one persistent structure, id=13, subj=72201
rel=72219 answer=72295, EVIDENCE (72201,72211,72291)
(72291,72212,72295) (72201,72219,72295) count=3. Both chain hops
licensed; the contradiction triple (72201,72219,72295) appears in
evidence as preregistered (its object is the structure's answer
literal); the flat wrong-fact triple (72201,72219,72299) leaves no
trace in the derived structure's evidence.

Transcript (6 answers):
- ANSWER[0]=72295, ANSWER[1]=72295: promotion probes; the derived
  structure formed and drove the answers.
- OBSERVE 72201 72219 72299: flat wrong fact taught on the probe
  key.
- ANSWER[2]=72299: PREFLAT. The flat wrong fact wins the
  pre-contradiction probe while the licensed derived structure
  exists underneath. Subordination replicated (the E1-W2 pattern).
- OBSERVE 72201 72219 72295: licensed contradiction; per the frozen
  protocol the old flat fact node is superseded (type-3 CON
  self-edge) and the derived value is taught as the new flat fact.
- ANSWER[3]=72295: POST. The read path, freed of the wrong fact,
  settles on the derived value.
- ANSWER[4]=72291, ANSWER[5]=72295: validity; the taught hops are
  retrievable.

The licensed derived structure present after the promotion probes
is the same structure present after the full stream (id=13,
both-hop evidence intact): it survived the flat-fact teaching, the
subordination probe, the contradiction, and the decision probe
without degradation.

## Verdict: E4-PRECEDENCE

W0 has DERIVED=1, FIRSTCLASS=1, VALID=1 on all 3 runs; W1 has
DERIVED=1, PREFLAT=1, POST=1, VALID=1 on all 3 runs. Per the frozen
decision rule (PREREG_E4 section 5): E4-PRECEDENCE.

## What this decides for H1a (Cluster 1)

H1a as PURE READ-PATH PRECEDENCE is confirmed for the
within-cluster discriminator. The evidence:

1. The derived layer is fully intact through the entire
   flat-fact/contradiction sequence: the licensed derived
   structure (id=13, answer 72295, both-hop licensed evidence)
   persists with no degradation, and the flat wrong fact leaves no
   trace in its evidence.
2. The subordination observed at the pre-contradiction probe
   (72299 returned while the derived structure existed) therefore
   cannot be attributed to any damage, demotion, or blocking of
   the derived layer by the flat/contradiction machinery.
3. The only remaining account is ordering: ev_query consults
   activate (flat fact lookup) before mp_run/t2_trial
   (construction/consultation), so a flat hit preempts the derived
   structure. A pure precedence phenomenon.

The refined Cluster 1 shared cause ("derived structures exist but
have no privileged standing in the read path; the flat
instance-fact layer is consulted first and wins") is now decided
evidence for H1a, not merely the E1 verdict's inference. The
deeper-suppression alternative (the flat/contradiction machinery
degrading the derived layer beyond ordering) is disfavored: the
inspector shows the layer untouched.

Recorded confound, same as E1: the promotion probes (W0
ANSWER[0]/[1], W1 ANSWER[0]/[1]) run the trial, which verifies
against the QUERY-carried expected value (the PF-A2/H1d instrument
property; E3's question). The PREFLAT and POST probes are pure
activate-path flat hits and carry no oracle caveat. The
discriminating leg (DERIVED via the oracle-blind inspector) is
unconfounded in all worlds.

## No-patch-treadmill compliance

No repair is proposed. E4 is a discriminating experiment; its
outcome goes back into the cluster analysis as decided evidence
for the refined H1a. A confirmed substrate change (a privileged
standing layer for derived structures in the read path) remains
TNN-3 business after the remaining E-lanes, not this lane.

## Criterion 0 status

Unchanged from the prereg: C0-A through C0-D NOT MET. Nothing
here is L3, L3-adjacent, or progress toward L3. The derived
structures are frozen-mechanism artifacts (trial-constructed
graphs), not learner-invented representations.

## Repository incident (resolved; did not affect results)

During this lane, the repository entered an interactive rebase
("rebasing branch 'tnn-native-lab' on 'bedf8b4aa'", 37/2216
commits done, paused awaiting `git rebase --continue`) initiated
outside this lane. This worker did not start, drive, or resolve
the rebase. While it was in progress, all E4 implementation and
evidence files were kept in a lane scratch area outside the repo
so the pending rebase picks could not collide with untracked
files. The rebase was subsequently aborted by the orchestrator;
the branch is back on tnn-native-lab with the prereg commit
intact (b63f80289, prereg SHA-256 unchanged). The staged files
were then moved into the lane directory and committed in the
preregistered order (worlds, tools, runs), so E4-K1 holds: the
prereg commit strictly precedes all E4 implementation commits.
This worker never ran `git rebase --continue/--abort/--skip`.

## Evidence paths

Lane: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E4/.

Committed:
- Prereg: b63f80289: PREREG_E4.md
  (SHA-256 b3fd77c2c1c4037ded940072fa147d6fd0a1fd912ac0054038d487bbbca40b74)
- Prereg backup (outside repo): ~/workspace/e4_scratch/
  PREREG_E4.frozen.md (same SHA-256), NAMECHECK.frozen.md

Lane files (committed in preregistered order: worlds, tools,
runs):
- Tools: e4_worldgen.zag, e4_inspect_state.zag (byte-identical to
  committed e1_inspect_state.zag), e4_struct_check.zag,
  e4_controls.zag, e4_audit_noleak.zag (byte-identical to
  committed e1_audit_noleak.zag), plus compiled _bin binaries
- Worlds and manifest: e4_worlds/ (E4_MANIFEST.sha256; e4_w0.txt
  184ed250b3773ee92c7c00671b788c4734f45aec153892ffd3f52465158f558b;
  e4_w1.txt
  cfefb30e39b05e4fd1f25af83ea8da767182b2be0c83dacb77cf52acfdc7f389)
- Transcripts, state bins, inspector reports, check outputs:
  e4_runs/ (per-world per-run .trans/.bin, _inspect_*.txt,
  _check_*.txt, e4_checks_all.txt)
- Control outputs: e4_controls_out/
- Cross-check: committed E1 W2 state bin and world file were read
  via git show (not copied into the lane); outputs were ephemeral.
- This report: E4_RUN.md; verdict brief: JUDGE_BRIEF.md
