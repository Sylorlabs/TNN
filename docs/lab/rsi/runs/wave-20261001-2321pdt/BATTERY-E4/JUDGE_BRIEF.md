# JUDGE_BRIEF.md -- E4 precedence-reversal verdict

RENDER_SHA: b3fd77c2c1c4037ded940072fa147d6fd0a1fd912ac0054038d487bbbca40b74
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: BATTERY Part 2 1/6 PASS, BATTERY-CLUSTER analysis
(Cluster 1 DERIVATION SUBORDINATION, H1a), BATTERY-E1 E1-FIRSTCLASS
as the motivating result (H1c killed; refined cause: derived
structures exist but have no privileged standing in the read path).
NEW_KNOWLEDGE_CLAIM: The precedence-reversal world shows the
licensed derived structure surviving flat-fact teaching and
licensed contradiction fully intact, confirming H1a as pure
read-path precedence rather than a deeper suppression of the
derived layer.

## Verdict: E4-PRECEDENCE

Frozen rule (PREREG_E4 section 5): W0 DERIVED=1 FIRSTCLASS=1
VALID=1 on all 3 runs; W1 DERIVED=1 PREFLAT=1 POST=1 VALID=1 on
all 3 runs.

## Evidence (per world, identical across 3 runs)

E4-W0 (control, no flat fact): inspector finds one licensed
derived structure (id=13, subj=72101, rel=72119, answer=72195,
both-hop evidence); probes return 72195/72195; validity 72191,
72195. Baseline holds.

E4-W1 (precedence-reversal): chain taught and probed (derived
structure id=13 forms, probes 72295/72295); flat wrong fact 72299
taught on the probe key (probe returns 72299: PREFLAT,
subordination replicated); licensed contradiction teaches the
derived value 72295 (probe returns 72295: POST, supersession per
the frozen protocol); validity probes hit. Inspector: the same
licensed derived structure (id=13, answer 72295, both-hop
evidence) persists through the flat-fact teaching and the
contradiction with no degradation; the flat wrong fact leaves no
trace in its evidence.

World hashes: e4_w0.txt
184ed250b3773ee92c7c00671b788c4734f45aec153892ffd3f52465158f558b;
e4_w1.txt
cfefb30e39b05e4fd1f25af83ea8da767182b2be0c83dacb77cf52acfdc7f389.
State bins: w0
7bfbed3389e5f6892c370dc76f6c9c6c74cae29f3314b2ec55054602b5887d03;
w1
fc5279f9204b3551b2d0170e9bd348d9d57610e3a3955c052396b704087889e2.

## Process

Prereg frozen at b63f80289 (shared commit with the ARENA5 prereg
after an index race; E4-K1 holds: first E4 commit, no E4
implementation inside). E4-K2/K3/K4/K6 PASS; calibration
(competent, degenerate, inspector cross-check, K-C0A) PASS.
Prediction E4-PRECEDENCE confirmed. C0-A through C0-D NOT MET;
nothing here is L3.

## Caveats

- The promotion probes carry the PF-A2/H1d oracle-verification
  instrument property; the discriminating DERIVED leg is
  oracle-blind and unconfounded. PREFLAT/POST are pure flat hits.
- A mid-lane interactive rebase on tnn-native-lab (outside this
  lane, later aborted by the orchestrator) delayed the
  implementation commits; all files were staged outside the repo
  until it resolved, then committed in preregistered order.
  E4-K1 holds.

## Recommendation

Record E4-PRECEDENCE as decided evidence for the refined H1a in
the cluster analysis: Cluster 1's subordination is a read-path
ordering phenomenon (flat layer consulted first), not a deeper
suppression of derived structures. No repair proposed (TNN-3
business).
