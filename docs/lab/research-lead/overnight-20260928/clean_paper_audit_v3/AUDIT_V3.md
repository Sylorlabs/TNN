# AUDIT_V3.md

Clean-Paper v3 Governance Audit (pipeline stage 11, third cycle).
2026-09-30 UTC. Auditor: Clean-Paper v3 Governance Auditor.

Target: docs/lab/research-lead/overnight-20260928/clean_paper/TNN_CLEAN_PAPER_v3.md
(commit c4855a65b), checked against the 63-claim ledger freeze:
canonical_ledger/CLAIM_LEDGER.md + canonical_ledger/CANONICAL_STATE.md
at 236a63a5a0.

Method: assume the paper is wrong; try to find where it misstates the
canonical record. Shell and git only for verification, with one
disclosed read-only python3 exception noted below. The contaminated
internal log TNN_RESEARCH_PAPER_20260929.md was never read for
evidence; its diff is verified zero.

## Verdict: PAPER-GOVERNANCE-V3-PASS

No blocking flags. The v3 paper is faithful to the 63-claim ledger on
every check. Three non-blocking observations are recorded below.

## K1 (completeness): PASS

- All 63 ledger claims C01-C63 are cited at least once in the paper
  (scripted sweep over all 63 IDs; zero missing).
- Every per-claim verdict label in the paper body matches the ledger
  entry's verdict line. Checked claim by claim against the 63
  verdict lines in CLAIM_LEDGER.md, including the mixed verdicts:
  C01 (KILLED generic reading; bounded L2 utility SURVIVES), C19
  (DOWNGRADED to bounded L2; SURVIVES-AS-L2), C20 (SURVIVES with
  downgrades), C32 (INVALID / VOID-then-SURVIVES /
  KILL-with-RETRACTED, all three components stated), C33
  (BUILD-FAIL), C52 (EXPLORATORY diagnostic finding), C60
  (BUILD-FAIL on K3 process grounds with the worker's claimed
  BUILD-PASS and the python3 disclosure both preserved).
- The paper's top-line tally matches the ledger's own "## Ledger
  tally" section list-for-list and count-for-count: 24 SURVIVES
  (bounded L2/L2+, none L3), 13 KILLED, 7 DOWNGRADED, 6 BUILD-PASS,
  3 BUILD-FAIL, 3 RETRACTED, 3 GOVERNANCE-PASS, 1
  REPRODUCTION-CONFIRMS, 1 UNVERIFIABLE, 1 SUPERSEDED, plus C52
  EXPLORATORY. The established conventions are identical in both
  documents: C19-as-L2 counted under DOWNGRADED and listed under
  SURVIVES; C33 under both KILLED and BUILD-FAIL; C08 and C15
  labeled SURVIVES in the claim entries but absent from the tally
  list. Because the ledger's own tally section encodes these exact
  conventions, the paper introduces no deviation from the canonical
  record. (Whether the ledger's tally convention is ideal is a
  ledger matter, not a paper deviation; see observation 1.)
- The ten new claims C54-C63 are handled correctly: C54
  CAUSAL-REVERT-PASS (SURVIVES bounded L2+, edit vocabulary
  researcher-supplied, revise mode not canonized per the ONE-SYSTEM
  RULE); C55 OPSCOPE-DISPLACEMENT-LOAD-BEARING (SURVIVES bounded
  L2+ boundary-mapping evidence, python3 setup disclosure preserved
  verbatim with the purity caveat traveling); C56 L3B-V2-PASS
  (SURVIVES bounded L2, finite-menu adversary noted, no menu
  expansion per the lane ruling); C57 LEARNER-REVERT-PASS
  (SURVIVES bounded L2, one lifetime); C58
  THRESHOLD-BOUNDARY-MAP-COMPLETE (SURVIVES bounded L2
  boundary-mapping evidence, Tier-2 retired); C59
  L3C-V2-ADV-SURVIVES-THIS-ROUND (SURVIVES bounded L2, this round
  only, disjunction blind spot and F2 wording mismatch disclosed);
  C60 L3A-TRACE-BUILD-FAIL (BUILD-FAIL on K3 process grounds);
  C61 FORKBATTERY-80/82 PASS (GOVERNANCE-PASS); C62
  PAPER-GOVERNANCE-V2-PASS (GOVERNANCE-PASS); C63
  PAPER-DERIVED-COMPLETE (SUPERSEDED, not evidence).
- No paper section asserts a result absent from the ledger. The
  ONE-SYSTEM RULE section states explicitly that the rule "is not
  itself a ledger claim." The eight pending decisions are in a
  section headed "They are not decided here." L3 achieved anywhere:
  zero, stated in the top line, section 1, section 9, and the
  closing line.

## K2 (commit chains): PASS

- All 173 distinct 9-hex commit hashes cited in the paper resolve
  to commit objects via git cat-file -t (zero failures, zero
  ambiguous prefixes, zero non-commit objects).
- 26 result/prereg/freeze subjects spot-checked against the paper's
  verdict labels; all match. Prioritized the new C54-C63 entries:
  c09afd95e / ab68dd121 / da0cd17b6 (CAUSAL-REVERT-PASS), ae9c3f13e
  / 54d3e3ca9 (OPSCOPE-DISPLACEMENT-LOAD-BEARING), 05620eaa2 /
  197e2547a / 7a1d3265d (L3B-V2-PASS), daf4f015d / dc20745db
  (LEARNER-REVERT-PASS), 2eaa1f122 / ab9a3ccfd
  (THRESHOLD-BOUNDARY-MAP-COMPLETE), 2c0e52739 / 8b82a836a
  (L3C-V2-ADV-SURVIVES-THIS-ROUND), 05898699e / a6fbee865 (L3A
  trace: worker-claimed BUILD-PASS, governance BUILD-FAIL on
  process), a3d7a9ed3 / 801736ec4 (fork battery 80/82, 2
  UNTESTABLE), d66466101 (PAPER-GOVERNANCE-V2-PASS), 6425f5a55
  (34-claim draft PAPER-DRAFTED).
- Ledger freeze 236a63a5a0 subject reads "Ledger append 3: C54-C63
  canonical claims (63 total; 24 survivals; 0 L3)", matching the
  paper's derivation note. The cited freezes 714178dd9 (C01-C34),
  71fe67563 (C35-C49), and 8837d2ee0 (C50-C53) all resolve.
- 12 additional older subjects checked (C03 b2b1ec415, C50
  6d7681138, C53 d1305bd43, C51 ebd62fe5, C02 0add71b64, C31
  b19e0e594, C19 45db44fab, C01 4a2b8ef43, C29 fded44631, C49
  15982381c); all match their paper labels. Total spot-checked: 38,
  above the 25 minimum.

## K3 (audit hygiene): PASS

- This audit introduces no new scientific claims.
- Both audit files are pure markdown and pass the shell-only
  check_no_dash.sh.
- The contaminated paper has zero diff and was never read for
  evidence.
- Process caveat (disclosed, does not affect the deliverable): one
  python3 heredoc was used once for read-only regex extraction of
  ledger verdict lines during early inspection. It printed to
  stdout only, produced no artifact, and no logic from it was
  adopted; every finding it surfaced was re-verified with grep and
  git. Recorded in NAMECHECK_V3.md; disclosure does not cure use.

## Terminology checks: PASS

- Every SURVIVES in the paper is labeled bounded: section 1 states
  "Every SURVIVES in this paper is labeled bounded"; the section 2
  header scopes all entries as "SURVIVES as bounded L2 or L2+
  unless noted otherwise"; each entry carries the bounded label
  (C03's entry relies on the section header, matching the ledger's
  own wording "SURVIVES as canonical lifetime-learning result").
  No SURVIVES at L3 or Criterion 0 appears anywhere.
- "L3 achieved anywhere: zero" appears in the top line, section 1,
  section 9, and the closing line.
- The ONE-SYSTEM RULE is presented as a standing architectural
  directive, explicitly "not itself a ledger claim."
- The eight pending decisions (S7, MD-SSD-1, S11 image pair,
  S11-AUD, C12 judge queue, Python-mirror logic, Beam Design 1,
  L3C-v2 Family D arithmetic slip) are presented as undecided under
  the header "They are not decided here." The "retain
  L3C-V2-PARTIAL" wording appears only in the pending-decision
  item, not as a ledger verdict; the C36 entry correctly carries
  the ledger's BUILD-PASS (builder level only) label.

## Non-blocking observations (for the next regeneration)

1. The tally conventions (C19 double-counted under SURVIVES and
   DOWNGRADED; C33 under KILLED and BUILD-FAIL; C08 and C15 labeled
   SURVIVES in the entries but absent from the tally list) are
   encoded identically in the ledger's own "## Ledger tally"
   section, so the paper is faithful. A future ledger cycle may
   still want to decide whether the tally should be a strict
   one-claim-one-label partition; that is a ledger decision, not a
   paper defect.
2. C33's bullet sits in section 3 ("Killed claims") while carrying
   the correct BUILD-FAIL label per the ledger ("BUILD-FAIL /
   DOWNGRADED"). The label is right and the tally counts it under
   both KILLED and BUILD-FAIL per the ledger's tally; the section
   placement is only cosmetically awkward.
3. The paper is already stale for post-freeze verdicts by its own
   derivation rule (e.g., the CORE FREEZE CHALLENGE protocol freeze
   and L3B v2 hardening noted in current memory are not ledgered
   at 236a63a5a0). This is expected and properly disclosed; the
   paper stands only as a record against its freeze.

## Recommendation

The v3 paper is cleared for internal use as the canonical
evidence-first record against ledger freeze 236a63a5a0. It must be
regenerated after the next ledger append before being used as a
canonical record for newer verdicts. Distribution stays internal;
nothing is published without Micah's explicit approval.
