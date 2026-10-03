# AUDIT_V2.md

Clean-Paper v2 Governance Audit (pipeline stage 11, second cycle).
2026-09-30 UTC. Auditor: Clean-Paper v2 Governance Auditor.

Target: docs/lab/research-lead/overnight-20260928/clean_paper/TNN_CLEAN_PAPER_v2.md
(commit 89cf970ee), checked against the 53-claim ledger freeze:
CLAIM_LEDGER.md + CANONICAL_STATE.md at 8837d2ee0.

Method: assume the paper is wrong; try to find where it misstates the
canonical record. Shell and git only, zero Python. The contaminated
internal log TNN_RESEARCH_PAPER_20260929.md was never read for evidence;
its diff is verified empty.

## Verdict: PAPER-GOVERNANCE-V2-PASS

No blocking flags. The v2 paper is faithful to the 53-claim ledger on
every check. Two non-blocking observations are recorded below.

## K1 (completeness): PASS

- All 53 ledger claims C01-C53 are cited at least once in the paper
  (scripted sweep over all 53 IDs; zero missing).
- Every citation's verdict label matches the ledger entry:
  - 18 SURVIVES (all bounded L2/L2+, none L3): C03, C06, C20, C21,
    C23, C25, C26, C28, C30, C35, C37, C38, C39, C45, C47, C50, C53,
    plus C19-as-L2 counted under DOWNGRADED.
  - 13 KILLED: C01 (generic reading), C02, C05, C07, C09, C10, C12,
    C14, C31, C33 (DEVANG2 part), C44, C46, C51.
  - 7 DOWNGRADED: C13, C16, C17, C18, C19, C24, C29.
  - 6 BUILD-PASS: C11, C22, C27, C34, C36, C43.
  - 2 BUILD-FAIL: C33, C42.
  - 3 RETRACTED: C32 (H-A diagnosis), C41 (v1 emergence claim),
    C49 (tiered claim), all stated as retractions in section 4.1 and
    the tally.
  - 1 REPRODUCTION-CONFIRMS: C40 (threshold, confirms C11).
  - 1 GOVERNANCE-PASS: C48 (fork battery).
  - 2 EXPLORATORY: old C1 wave (superseded by C03), C52 (HypD v2
    review).
  - 1 UNVERIFIABLE: C04 (Beam Design 1).
- The four new verdicts are handled correctly: C50 (recency-guard
  SURVIVES; retention lane stated CLOSED with the adopted
  discipline); C51 (OpScope gate KILLED, new section 3.14); C52
  (HypD v2 review EXPLORATORY); C53 (learner-integration SURVIVES,
  called the strongest continuing-learner result, with the "one
  continuing learner" goal stated as approached, not claimed).
- The C38 scope-narrowing caveat is present in section 2.4: the
  gate attack C51 narrows the result; the battery's position-1 "not"
  may be a hidden researcher choice.
- The paper's tally (section 5.5) matches the ledger's tally
  (CLAIM_LEDGER.md) list-for-list and count-for-count, including
  the inherited conventions (C19 counted under both SURVIVES and
  DOWNGRADED; C33 under both KILLED and BUILD-FAIL).
- No paper section asserts a result absent from the ledger. Every
  substantive section is claim-anchored; section 5.1 is synthesis
  with every sentence citing ledger claims.

## K2 (commit chains): PASS

- All 166 distinct 9-hex commit hashes cited in the paper resolve to
  commit objects via git cat-file -t (zero failures, zero ambiguous
  prefixes).
- 20 result-commit subjects spot-checked against the paper's
  verdict labels: b2b1ec415 (C1-CLEAN PASS), 51c54e262 (OpScope
  prereg), c60bfbe7a (OPSCOPE-R1R4-PASS), d1305bd43
  (LEARNER-INTEGRATION-PASS), 6d7681138
  (RECENCY-GUARD-CONTAINED), ebd62fe5 (gate-stress sealed), c6069aca4
  (HypD review EXPLAINED), 53b9a9a27 (REVISE-TRANSFER-PASS), 00e9a766e
  (REVERT-ADAPT-PASS), d9f3871c5 (DDES integration), c96875d36
  (L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN), 14a92a69d (L3B C0-C
  prereg), 15982381c (threshold red team prereg), 4a2b8ef43
  (REVISE-REDTEAM-KILLS), 955106ae5 (threshold repro prereg),
  07785ac78 (THRESHOLD-REPRO-PASS), 20705ab5a (fork battery 79/81),
  7b670b633 (PAPER-GOVERNANCE-PASS), 8837d2ee0 (ledger append
  C50-C53), 94c30752f (CLEAN-PAPER-COMPLETE). All 20 match.

## K3 (audit hygiene): PASS

- This audit introduces no new scientific claims.
- Shell and git only; zero Python invoked at any step.
- Both audit files pass the shell-only check_no_dash.sh.
- The contaminated paper has zero diff and was never read for
  evidence.

## Non-blocking observations (for the next regeneration)

1. In-flight statuses (section 5.3) now carry commit pointers where
   they exist and say "no verdict ledgered at this freeze" where
   they don't; this resolves the v1 audit's observation 1. One
   residual: the tak-displacement family (in flight at 5.3 item 8
   and noted in 3.14) completed around this freeze and is not yet
   ledgered (OPSCOPE-DISPLACEMENT-LOAD-BEARING); it is properly
   absent from the paper per the derivation rule but will need a
   ledger entry and paper section at the next cycle.
2. The SURVIVES terminology wrinkle from the v1 audit is resolved:
   section 1 defines SURVIVES as the bounded reading established by
   each claim's own frozen bars, explicitly distinct from the
   11-stage pipeline sense, which no mechanism has completed.

## Recommendation

The v2 paper is cleared for internal use as the canonical
evidence-first record against ledger freeze 8837d2ee0. Before any
external use: the paper stays internal until Micah rules, and it
must be regenerated after the next ledger append (several verdicts
have already landed after this freeze: threshold boundary map,
L3B v2, learner law-revert integration, OpScope displacement). The
derivation note in the paper requires this; the audit concurs.
