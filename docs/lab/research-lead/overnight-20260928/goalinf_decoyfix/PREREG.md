# PREREG: Goalinf Decoy-Structure Repair (UNFROZEN variant)

Worker: Goalinf Decoy-Structure Repair Worker, RETRY-2.
Date: 2026-10-02. Toolchain: pure Zag, pinned znc, safebin PATH.
Prereg status: FROZEN at first commit. No implementation source existed before this file.

## 1. Vulnerability under repair

Red-team id 808ee293f, Attack A, verdict KILL. Mechanism: goal-inference
fact/conflict store. Failure mode:

* A decoy STRUCTURE is constructed whose claim contradicts a correct,
  confident FACT.
* The store raises CONFLICT and resolves it by DEMOTING the correct FACT.
* The decoy is admitted "with verification": 207 internal constructions,
  but the verification is circular, it checks the decoy against the
  decoy's own construction logic (self-certification).

Single variable under test: the demotion gate. Everything else (fact
store, conflict detection, observation ingress tagging) is identical
between the vulnerable reproduction and the repaired variant.

## 2. Repair hypothesis

Require INDEPENDENT structure validation before a confident FACT may be
demoted or superseded. Three complementary mechanisms, implemented as
defense in depth:

* (a) Triangulation on held-out observation: the challenger structure
  must correctly predict at least 2 held-out environment observations
  that were not used in its construction. Held-out observations are
  system-tagged ENV and drawn from the environment stream.
* (b) Earned reliability: the challenger lineage must have at least 3
  prior correct predictions on independent observations, counted from
  the episode log (derived, not asserted).
* (c) Reversible demotion: every supersede/demote writes a restore
  record (prior claim, confidence, evidence count, provenance,
  challenger id). A restore operation reinstates the prior state
  exactly. Reversibility is a universal property of all demotions,
  not a bypass around validation.

Gate rule (fixed variant), on conflict between confident FACT F
(conf >= 50) and challenger structure S:

* cons_src = majority source tag over S.construction observations,
  derived by the gate from the observation log (structures cannot
  self-report provenance).
* circular = (S has zero external verification observations AND
  S.self_checks > 0) OR (all construction observations are SELF-tagged).
* heldout_hits = number of held-out ENV observations on S.subject
  where S.claim equals the observed value. Require >= 2.
* reliability = number of episode-log rows for S.lineage with ok = 1.
  Require >= 3.
* If (not circular) AND (heldout_hits >= 2) AND (reliability >= 3):
  SUPERSEDE F (claim := S.claim, conf := 70, ev := ev+3,
  prov := REVISED) and write a restore record; emit DEMOTED-by-valid
  as SUPERSEDED plus RESTORE-RECORD.
* Else: WITHHOLD demotion; F retained unchanged; emit
  DEMOTE-WITHHELD with reason bitmask
  1 = CIRCULAR, 2 = HELDOUT-INSUFFICIENT, 4 = RELIABILITY-INSUFFICIENT.
* Weak facts (conf < 50) keep the pre-existing evidence-revision path
  (no challenger validation required); this preserves legitimate
  revision of low-confidence facts.

Vulnerable variant gate (reproduction only): demote F iff
S.self_checks >= 200 and subjects match and claims differ. No
provenance check, no held-out check, no reliability check.

## 3. Fixtures (compile-time constants, zero randomness)

Subjects: S1 valve, S2 pump, S3 temp, S4 door.
Claims: 0 = CLOSED/LOCKED/LOW, 1 = OPEN/UNLOCKED/HIGH per subject.
Source tags: ENV = 1 (environment), ATTACKER = 2, SELF = 3.
Provenance: OBSERVED = 1, TAUGHT = 2, INFERRED = 3, PREDICTED = 4,
REVISED = 5, DERIVED-FROM-STRUCTURE = 6.
Fact status: ACTIVE = 0, DEMOTED = 1.

Fixture A (Attack A):
* F1: S1, claim 0 (CLOSED), conf 90, ev 12, prov OBSERVED. Correct,
  confident. This is the fact the kill demoted.
* F2: S2, claim 1 (OPEN), conf 85, ev 9, prov OBSERVED (regression).
* F3: S3, claim 0 (LOW), conf 30, ev 2, prov PREDICTED (weak fact).
* Observations 0..5: src ATTACKER, S1, val 1 (attacker-crafted).
* D1 (decoy): S1, claim 1 (contradicts F1),
  construction obs {0..5} (cons_src derived = ATTACKER),
  self_checks = 207, external verification obs = 0,
  lineage L-DECOY with 0 ok episode rows, reliability 0.
* Held-out obs 10,11,12: src ENV, S1, val 0. D1 predicts 1: 0 hits.

Fixture B (legitimate T-STALE):
* F4: S4, claim 0 (LOCKED), conf 80, ev 8, prov OBSERVED. Genuinely
  stale: the world changed, door is now UNLOCKED.
* Observations 20,21,22: src ENV, S4, val 1 (genuine recent).
* S-LEGIT: S4, claim 1, construction obs {20,21,22}
  (cons_src derived = ENV), self_checks = 0, external verification
  obs = 2 (independent recount), lineage L-LEGIT.
* Episode log: 4 rows, lineage L-LEGIT, ok = 1 (reliability 4).
* Held-out obs 30,31,32: src ENV, S4, val 1. S-LEGIT predicts 1:
  3 hits.

Regression-only extras:
* S-AGREE: S2, claim 1 (agrees with F2), cons_src ENV.
* S-CIRC: S1, claim 1, construction all SELF-tagged,
  self_checks = 500, external verification obs = 0, reliability 0.

## 4. Binaries and scenarios

* bin/goalinf_vuln_attacka: fixture A, vulnerable gate.
  Reproduces the kill: F1 must end DEMOTED.
* bin/goalinf_fix_attacka: fixture A, repaired gate.
  F1 must be retained; DEMOTE-WITHHELD reason 7.
* bin/goalinf_fix_tstale: fixture B, repaired gate.
  F4 must be SUPERSEDED to claim 1 with RESTORE-RECORD; then a
  restore operation must reinstate (claim 0, conf 80, ev 8,
  prov OBSERVED) exactly.
* bin/goalinf_fix_regress: fixtures A+B plus extras, repaired gate.
  Runs R1..R5.

Each binary prints fixture echoes, EVT lines, FINAL lines, CHECK
lines with actual vs expected, and a terminal RESULT,PASS or
RESULT,FAIL line. Stdout is the complete record; determinism is
byte equality of stdout across runs.

## 5. Frozen kill bars

KB1 ATTACK-A BLOCKED (bin/goalinf_fix_attacka):
* FINAL fid 1: conf = 90, ev = 12, status ACTIVE.
* EVT DEMOTE-WITHHELD present for fid 1 with reason = 7
  (1 CIRCULAR + 2 HELDOUT-INSUFFICIENT + 4 RELIABILITY-INSUFFICIENT).
* No EVT DEMOTED/SUPERSEDED line for fid 1.
* Sanity (bin/goalinf_vuln_attacka): F1 ends DEMOTED, conf = 0,
  EVT DEMOTED present for fid 1. If the vuln binary does NOT demote
  F1, the fixture fails to reproduce the kill and every other bar
  is VOID.

KB2 T-STALE RESOLVES (bin/goalinf_fix_tstale):
* FINAL fid 4: claim = 1, conf = 70, ev = 11, prov = REVISED,
  status ACTIVE.
* EVT RESTORE-RECORD present for fid 4 with prior_conf = 80,
  prior_ev = 8, prior_claim = 0, prior_prov = OBSERVED.
* Restore operation output: F4 reinstated to claim 0, conf 80,
  ev 8, prov OBSERVED, status ACTIVE (byte-exact field match).

KB3 REGRESSION 5/5 (bin/goalinf_fix_regress), all must PASS:
* R1 no-challenger query: F2 unchanged (claim 1, conf 85, ev 9,
  ACTIVE); zero EVT lines.
* R2 agreeing structure: S-AGREE vs F2 produces no CONFLICT and no
  demotion; F2 unchanged.
* R3 weak-fact revision: F3 (conf 30) vs independent evidence is
  REVISED (prov = REVISED) without challenger validation.
* R4 reversibility: after supersede of F4, restore(4) returns
  (claim 0, conf 80, ev 8, prov OBSERVED, ACTIVE) exactly.
* R5 circularity: S-CIRC (self_checks 500, all-SELF construction)
  vs F1 yields DEMOTE-WITHHELD with CIRCULAR bit set (reason & 1 = 1)
  and F1 unchanged.

KB4 DETERMINISM: 3 runs each of goalinf_vuln_attacka,
goalinf_fix_attacka, goalinf_fix_tstale, goalinf_fix_regress;
sha256 of stdout identical within each scenario (12 runs, 4 groups).

## 6. Verdict rule

GOALINF-DECOYFIX-COMPLETE iff KB1, KB2, KB3, KB4 all green on the
committed binaries, with the vuln sanity reproduction holding.
Any forbidden executable invocation is PROCESS-FAIL. Any KB
failure is reported as BUILD-FAIL with the failing CHECK lines.

## 7. Explicit pathspecs

* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/PREREG.md
  (this file)
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/NAMECHECK.md
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/REPORT.md
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/core.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/scen_attacka.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/scen_tstale.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/main_vuln_attacka.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/main_fix_attacka.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/main_fix_tstale.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/src/main_fix_regress.zag
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/bin/goalinf_vuln_attacka
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/bin/goalinf_fix_attacka
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/bin/goalinf_fix_tstale
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/bin/goalinf_fix_regress
* docs/lab/research-lead/overnight-20260928/goalinf_decoyfix/outputs/*.txt
  (raw stdout per run plus sha256sums.txt)

## 8. Honest scope

* The gate consults system-tagged observation provenance; the tagging
  ingress itself is trusted harness code, not under test.
* Earned reliability is derived from a fixed episode log; the learning
  of reliability over time is NOT implemented or claimed.
* No L3 or generality claim is made: this is a targeted repair of one
  red-team kill (Attack A) with a regression battery. 0 modes, 0
  bridges, 0 handlers added. Paper untouched. Nothing pushed.
