# HELL-HOLE V4 RED-TEAM PREREG (frozen 2026-09-23)

**Parent:** hell-hole V4 (commit `e22be523b5dc`) — "full swarm — every
hell-hole issue found and repaired". PIPELINE crew: all bars met. JOKE-FIX:
30/30, zero deadpan installs. Integration: r12_v4 A1 52/52, A2 27/50,
A3 51/51, all v3 seeds flip, 382 regression 13 justified flips,
curated-18 exact, 3x byte-identical. Track G native logic core
(`logic.zag`) independently audited, K-V3PROOF/K-MLOGIC/K-DET/K-PURE met.

**Directive (Micah, 2026-09-23):** "since all bars met red team it test
red team and if all good document and commit but otherwise finish as
needed."

## Targets (committed artifacts ONLY — blind red team)
Base repo path: `docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/`
- T1 native logic core: `crews/c2/logic.zag` (batteries in `crews/c2/batteries/`)
- T2 integrated stance classifier: `crews/integ/r12_v4.zag`
- T3 joke classifier: `crews/jokefix/g_intent6_v4.zag`
- T4 full pipeline: `crews/pipeline/` (runner + scoring scripts)

## Blindness rules
- Red-team crews may read ONLY committed repo files above. They may NOT
  read `~/workspace/scratch-hellhole/` builder workdirs or any builder
  corpora/reports. They may not share state with builder crews.
- Every attack corpus is a frozen TSV `id \t claim \t evidence \t oracle`
  written BEFORE the target is run. Oracle labels are the attacker's
  pre-commitment; a "hit" is target output disagreeing with the oracle in
  the attacked direction.
- Targets run 2x; runs must be byte-identical or the measurement is void.

## Attack families (each crew: ≥40 novel items per family, none from the
frozen v4 batteries/corpora)
- **RT-A accept-invalid:** invalid logic shaped to be AFFIRMed —
  affirming-the-consequent, correlation-as-causation, scope-shifted
  negation ("not guilty" → "innocent"), range-mismatch affirmation,
  hedged claim over-affirmed as certain, conditional consequent asserted
  as fact. Target: T1, T2.
- **RT-B reject-valid (the v3 failure mode):** valid logic shaped to be
  REJECTed/WITHHELD — correct negation DENY, correct contrastive DENY,
  true causal AFFIRM, valid modus ponens. Target: T1, T2, T4. ANY hit
  here replays Micah's original directive (v3 verifier rejected good
  logic) and is a FAIL.
- **RT-C joke attacks:** deadpan factual statements as jokes, hostile/
  non-funny content, jokes with negation or contrastive structure,
  near-duplicate of training jokes with the punchline removed.
  Target: T3. Any deadpan install = FAIL.
- **RT-D calibration/edge probes (informational):** double negation,
  negation outside predicate scope ("not X but Y"), numeric edge
  ("at least 5" vs "5"), multi-step causal chains, prevented-cause,
  quantifier scope ambiguity. Documented as boundary map, not kills.

## Kill bars
- **K-RTA:** any RT-A family with ≥3 hits → FAIL, fix required.
- **K-RTB:** any RT-B hit on T1/T2/T4 → FAIL, fix required (v3 mode).
- **K-RTC:** any deadpan install or ≥3 joke misclassifications → FAIL.
- **K-RTDET:** any non-byte-identical rerun → measurement void, rerun.
- **K-RTBLIND:** corpus written after running the target → whole
  battery void (check file mtimes vs run logs).

## Deliverables (per crew, in `redteam/rtN/`)
`ATTACK_REPORT.md` (families, counts, hit list with idx/claim/evidence/
oracle/target-output, SHAs of corpus + both runs, honest limits),
frozen attack corpora TSVs, run logs. No commit by crews; the coordinator
commits the verdict.

## Amendments
Any change to families, bars, or kill criteria needs Micah's re-approval.
