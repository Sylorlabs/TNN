# Clean-Paper Governance Audit (pipeline stage 11)

**Verdict: PAPER-GOVERNANCE-PASS** (no blocking flags; three non-blocking
observations recorded below).

**Paper audited:** `docs/lab/research-lead/overnight-20260928/clean_paper/TNN_CLEAN_PAPER.md`
(commit 94c30752f), derived from `canonical_ledger/CLAIM_LEDGER.md`
(49 claims; freezes 714178dd9 + 71fe67563) and
`canonical_ledger/CANONICAL_STATE.md` (section 6 appended).

**Method:** assume the paper is wrong; check every cited ledger claim ID
against the ledger, spot-verify every cited commit chain resolves, check
no paper claim exceeds its ledger entry's scope, verify the three
retractions, the provenance incidents, the missing-pieces list, and the
tallies. Shell and git only; no Python.

---

## K1. Completeness: every cited ledger claim ID checked

All 49 ledger claims are cited in the paper. Per-section mapping:

| Paper section | Ledger claims cited | Ledger status match |
|---|---|---|
| 0 Top line | C03, C37, C35, C39, C47, C41, C49, C32 | PASS: C03/C37/C35/C39/C47 SURVIVES bounded L2; C41/C49/C32 RETRACTED; tallies match |
| 2.1 C1-CLEAN | C03 | PASS: SURVIVES; older C1 wave EXPLORATORY/GOVERNANCE-VOID per ledger |
| 2.2 scale-up/stress/episodic | C15, C37, C45 | PASS: all SURVIVES bounded L2; provenance note matches ledger C45 |
| 2.3 DDES chain | C35, C39, C47 | PASS: all SURVIVES bounded L2; caveats (researcher-owned format, arena C9 parked) match ledger |
| 2.4 OpScope | C38 | PASS: SURVIVES bounded L2; K=2 justification note matches ledger |
| 2.5 bounded family | C19, C20, C21, C23, C25, C26, C28, C30, C06, C29 | PASS: C19 counted under SURVIVES-as-L2 and DOWNGRADED per ledger tally; others match |
| 2.6 salt corrections | C32 | PASS: INVALID / VOID-then-SURVIVES / KILL-with-RETRACTED; H-B re-freeze 7aeb0cbda cited |
| 2.7 arena figures | C34 | PASS: BUILD-PASS figures only; LLM PENDING; HUMAN BASELINE NOT MEASURED |
| 3.1 REVISE | C01 | PASS: KILLED generic reading; step-4 prereg gap flagged per ledger |
| 3.2 OpScope v1 | C02 | PASS: KILLED |
| 3.3 beam lineage | C05, C07, C08 | PASS: KILLED, KILLED, SURVIVES-as-review |
| 3.4 conditional v1/tax | C09, C10 | PASS: both KILLED; /tmp debug disclosure marked non-canonical per ledger |
| 3.5 procedure v1 | C16 | PASS: DOWNGRADED to L2+ |
| 3.6 H-PROCLANG1/REPEXPAND | C17, C18 | PASS: KILLED as L3; DOWNGRADED to L2+ |
| 3.7 DDES as L3 | C31 | PASS: KILLED as L3; bounded utility stands |
| 3.8 SEM/H-CAUSALEXP as L3 | C29, C19 | PASS: both DOWNGRADED/KILLED-as-L3 |
| 3.9 C0INTEG Phase B | C14 | PASS: KILLED |
| 3.10 valley | C12, C42 | PASS: KILLED; BUILD-FAIL at validation gate |
| 3.11 churn | C44 | PASS: KILLED for single-wave regime (falsifier) |
| 3.12 L3B C0-C | C46 | PASS: KILLED as C0-C; A2/B2 frozen falsifiers; C43 not impugned |
| 3.13 downgrades | C13, C33, C24 | PASS: DOWNGRADED; BUILD-FAIL/DOWNGRADED; DOWNGRADED |
| 4.1 retractions | C41, C49, C32 | PASS: all three stated as retractions with boundary maps |
| 4.2 builder-level | C11, C40, C36, C43, C22, C27, C34 | PASS: all stay BUILD-PASS; C40 is REPRODUCTION-CONFIRMS not promotion |
| 4.3 fork battery | C48 | PASS: GOVERNANCE-PASS; infrastructure, not capability |
| 4.4 provenance | (incidents) | PASS: 9c6ee8ba8/fd31db230 stated factually; no history rewrite proposed |
| 4.5 unverifiable | (ledger list) | PASS: paper-log-only commits, C04, /tmp build, unrun stages all listed |
| 5.1-5.5 frontier/state | C03..C49 | PASS: six missing pieces each grounded in ledger/state; L3 zero; six Micah items match |

No ledger claim is cited with a wrong verdict label. No paper section
asserts a result not present in the ledger.

---

## K2. Commit-chain spot verification

61 distinct commit hashes cited in the paper were checked with
`git cat-file -t`: all 61 resolve to commit objects. Zero failures.

Spot-checked subjects against the paper's verdict labels (16 commits):
b2b1ec415 (C1-CLEAN PASS), daa9bf2fc (LEARNER-STRESS-PASS),
f843188ad (DDES-INTEGRATION-PASS), 7871ca6d3 (DDES-MULTISTEP-PASS),
00e9a766e (REVERT-ADAPT-PASS), c60bfbe7a (OPSCOPE-R1R4-PASS),
136588de5 (EPISODIC-PRESSURE-BLEED), c96875d36
(L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN), a40aac558
(L3B-C0C-BOUNDARY-EXPOSED), 2fb110ce7 (L3B-GROWTH-PASS),
e663864f5 (L3C-FORM-PASS), 07785ac78 (THRESHOLD-REPRO-PASS),
5db2712af (CHURN-REVISION-PASS), b4c81d190 (FORKBATTERY-78/80 PASS),
ea920137b (VALLEY-REDESIGN-FAIL). All match the paper's labels.

Tally cross-check: paper section 5.5 reproduces the ledger's tally
verbatim (16 SURVIVES bounded L2/L2+, 12 KILLED, 7 DOWNGRADED,
6 BUILD-PASS, 2 BUILD-FAIL, 3 RETRACTED, 1 REPRODUCTION-CONFIRMS,
1 GOVERNANCE-PASS, 1 EXPLORATORY, 1 UNVERIFIABLE, VOID/INVALID C32).
Independent extraction of all 49 Status lines from CLAIM_LEDGER.md
confirms the same per-claim mapping, including the double-counted
C19 (SURVIVES-as-L2 and DOWNGRADED) and the mixed C32/C33 entries.

---

## K3. Audit hygiene

- The audit introduces no new scientific claims; it only cross-checks
  paper text against ledger text and git objects.
- No Python used anywhere in this audit (shell, git, grep, sed only).
- No em dashes in this file (verified with the shell-only
  check_no_dash.sh snippet).
- The contaminated paper
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  was not read for evidence and has zero diff (`git diff --stat` empty).
- This audit's files live only under
  `docs/lab/research-lead/overnight-20260928/clean_paper_audit/`.

---

## Observations (non-blocking)

1. **In-flight statuses lack commit pointers.** Section 5.3 states
   several lanes are "in flight" (C1 law-revert attack, threshold
   boundary mapping, valley satisfiability search, L3C v2, learner
   integration, K=2 gate stress) without commit pointers or ledger IDs.
   The paper's derivation rule says every factual claim carries a commit
   pointer and a ledger claim ID. These are working-state observations,
   not result claims, so this is a minor deviation, not a scope
   exceedance. Recommendation: cite the in-flight prereg/freeze commits
   (e.g., 482980e9f and fd31db230 for the C1 attack, 7912fe11b for the
   valley search, 9e595301a for L3C v2) in the next regeneration.

2. **Inherited terminology wrinkle.** Section 4.5 item 4 says the
   verdict labels of C1-CLEAN, C11, and C15 "are not SURVIVES" (the
   11-stage-pipeline sense) while sections 2.1/2.2 label C03 and C15
   SURVIVES (the bounded-result sense). This tension is inherited
   verbatim from the ledger's own UNVERIFIABLE item 4, not introduced
   by the paper; the paper consistently qualifies every SURVIVES as
   bounded L2/L2+ everywhere else. Recommendation: one disambiguating
   line ("SURVIVES here means bounded-result survival, not pipeline
   promotion") in the next regeneration.

3. **Staleness is handled correctly.** Three verdicts landed after the
   ledger append 71fe67563 (RECENCY-GUARD-CONTAINED 68c5796d4/6d7681138,
   GATE-STRESS-FAIL 82262d90c/37d4212d/ebd62fe5, HYPD-REVIEW-COMPLETE
   2c4c58e80/c6069aca4). Per the derivation rule they are correctly
   excluded (not in the ledger), and the paper's derivation note states
   regeneration is required before use as a canonical record. This is
   proper governance, not a violation.

---

## Recommendation

The paper is cleared for internal use as the canonical evidence-first
record against ledger freezes 714178dd9 + 71fe67563. Before any external
use: regenerate after the next ledger append (the three post-freeze
verdicts above are already pending), fold in the two minor
recommendations above, and obtain Micah's ruling, since the paper stays
internal until he rules. No fixes are required for internal use.

No em dashes were used in this document (verified with the shell-only
check_no_dash.sh snippet).
