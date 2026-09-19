# R32 E51AA — Resource-Feasible Terminal Decomposition Result

Date executed: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID DIAGNOSTIC — `MIXED_RESOURCE_FEASIBLE_TERMINAL_LIMIT`**
Canonical status: **R27 remains canonical.**

## Native authority

- GitHub Actions run: `33361300600`.
- source head: `33f972704b0530c841d46d27a6afe8020bbf1c8f`.
- evidence artifact id: `9746883318`.
- artifact ZIP SHA-256: `503162e1c3abed4cd1e8aafc6de06402d8051be4aec048a70d153c927c6db2ff`.
- assembled source SHA-256: `b8f995c6b4654b8b43010198a436d162ca8921d2ebd4f1a96fd31c85949525e7`.
- E51AA audit fragment SHA-256: `247b5effca69060f5361f326e70d836cf4459ba064ef79f352445f044bb0a326`.
- E51AA injection SHA-256: `d6f272657c80ff5af7a80434331f3c9f6d58eb9b66204b3aee3c0c4822c30dd2`.
- assembly script SHA-256: `e346d8dbd59a3dc57809e32f21e171738cd1c631d6150f3ee68717e30f2e44f1`.
- frozen E45 core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`.
- native binary SHA-256: `8b0c2150b18471879b7e98ad4f1d595a407689a7782e4fc3e07ddf3795f45b88`.
- double native build byte identity: PASS.
- native exit code: 0.
- native execution runtime: about 338 s.

## Integrity

- E50 parent integrity: PASS.
- E51Y/E51X terminal reproduction: 4,200 / 4,200 known + 1,200 / 1,200 no-unique full-tape reachability: PASS.
- stage-88 worlds: `88,000,000 .. 88,005,399`.
- world partition/domain gates: PASS; assignment failures: 0.
- audit episodes: 5,400; states: 91,800.
- learner updates during stage 88: 0.
- terminal hash before/after: `238967492` / `238967492`.
- UNKNOWN target nonzero: 0.
- topology/graph changes: none.
- overall integrity: PASS.

## Resource-feasible decomposition

Frozen E51X terminal policy on stage 88:

- cost-feasible successful episodes: **5,059 / 5,400**;
- missing: **341**;
  - known missing: **332**;
  - no-unique missing: **9**.

For the 4,200 known episodes:

- at least one resource-feasible state where the frozen top commit among KEEP/CURRENT/RESTORE is grounded-correct: **4,151 / 4,200**;
- at least one resource-feasible grounded-correct action somewhere in KEEP/CURRENT/RESTORE, ignoring the frozen ranking: **4,152 / 4,200**.

Therefore the existing scalar commit-vs-UNKNOWN mechanism has a theoretical ceiling of only:

**1,200 no-unique + 4,151 known = 5,351 / 5,400 episodes.**

It cannot reach exact resource-feasible terminal success even with a perfect scalar calibrator.

### The 341 frozen misses

- **292** are scalar-only misses: the required terminal action is available/top-ranked somewhere feasible, but commit-vs-UNKNOWN calibration suppresses it (including all nine no-unique misses).
- **1** known episode is commit-ranking-limited: a correct KEEP/CURRENT/RESTORE action exists in the feasible prefix but is never the frozen top commit.
- **48** known episodes are action-support-limited: no KEEP/CURRENT/RESTORE action is grounded-correct anywhere before resource cutoff.

The 48 action-support misses are concentrated primarily in changing-state regimes, especially modes 4 and 5, with two additional mode-3/resource-2 cases. This is consistent with a structural problem in forcing terminal reporting through `initial/current/prior` belief-state slots: under tight resource horizons, the correct latent hypothesis may be supported by evidence before the temporal state machine has placed it in a reportable slot.

## Exact critical-state alias audit

The scalar-critical set contained 5,351 rows:

- exact duplicate critical feature rows: 0;
- contradictory commit-side versus UNKNOWN-side exact feature keys: 0;
- contradictory rows: 0.

So the scalar-solvable portion is not blocked by exact learner-visible aliasing on this population.

## Causal conclusion

E51AA rules out another scalar-only terminal repair as a complete solution. The current terminal action geometry itself is resource-limited: 48 known episodes cannot express the grounded-correct answer at any feasible stop because `KEEP / CURRENT / RESTORE` only report already-materialized belief-state slots.

The smallest justified architectural change is **not a graph rewrite and not a forced faster belief-state switch**. It is to decouple persistent belief-state maintenance from terminal reporting by giving the action-value system generic direct access to the currently represented hypothesis candidates. In the present two-candidate diagnostic world this can be instantiated as two candidate-commit actions, but the mechanism must be specified generically as `COMMIT(candidate)` rather than encoding task identities or answers.

The next experiment should compare the frozen E51X state-action terminal control against direct candidate-commit value heads on the same learner-visible state and grounded consequence targets. UNKNOWN remains neutral zero. No ambiguity labels, confidence thresholds, evaluator modes, graph topology, or hand-selected routing are permitted.

No R32 promotion or AGI/consciousness claim is supported.