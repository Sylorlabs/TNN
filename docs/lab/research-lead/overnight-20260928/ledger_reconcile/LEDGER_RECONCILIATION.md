# LEDGER RECONCILIATION: NT-era watchdog claims C404-C454 vs canonical CLAIM_LEDGER.md

Status: PROPOSAL ONLY. No changes were made to `canonical_ledger/CLAIM_LEDGER.md`.
Approval needed from parent/main agent before any ledger write.

Date: 2026-10-03 (analysis of commits through 10:09 UTC)
Worker: LEDGER-RECONCILE (follow-up to NT-SYNTHESIS C452 governance flag)

## 1. Sources examined

- `docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
  (working tree; highest claim number present is C410; no C411+ in any format)
- Full git history of `WATCHDOG: ledger Cxxx` commits on 2026-10-03, 07:47 to 10:08 UTC
  (series runs C404 through C454, all "Local only, never pushed")
- Uncommitted working-tree diff of CLAIM_LEDGER.md
- Commit d0d59a968 (CITATION-HYGIENE, 10:06 UTC) which cites displaced numbers

## 2. What happened (timeline)

On 2026-10-03 between 07:47 and 10:08 UTC, the NT-SYNTHESIS watchdog worker minted
claim numbers C404 through C454 in commit messages, in chronological order, without
writing any of them into CLAIM_LEDGER.md. Meanwhile, other workers had written (or
were writing) entries C400-C410 into the working-tree CLAIM_LEDGER.md for different
experiments.

The watchdog discovered the overlap mid-series and, starting 07:57 UTC, began
re-minting C404-C410 with the canonical experiment names (commits 9992a325e,
1611dc81c, 44ecf987a, c99bd82f5, ff8a2d8df, 92a1831a7, 9fd459b2e), effectively
conceding those numbers to the canonical ledger. Its original NT-era assignments
for C404, C405, C406, C407, C409, C410 were left standing in the earlier commit
messages with no ledger home.

Net result: 6 genuine collisions, 43 clean watchdog-only claims, 1 probable
duplicate, 2 superseded renumbering artifacts.

## 3. Collisions (watchdog number vs canonical number)

The canonical ledger holds these assignments (all in working-tree CLAIM_LEDGER.md;
C401-C410 currently uncommitted, see section 7):

| #   | Canonical (ledger)                              | Watchdog's earlier claim (commit, UTC)                        |
|-----|-------------------------------------------------|---------------------------------------------------------------|
| C404| MP-2 REGIME-CHANGE (belief_mprov2/)             | NEGATIVE-TRANSFER NT1 PASS (c66edb1ba, 07:47)                  |
| C405| DEEP7-RC-CLEAN (hcontlife5-deep7-rc-clean/)     | LIFETIME-META LM1 (3385761b6, 07:54)                           |
| C406| COGNITIVE-OPS-LEARNER (cognitive_ops_learner/)  | GEN-STATEFIX UPGRADE-TO-SUBSUMES (ea8c50a52, 07:55)            |
| C407| COMPAUDIT-1 (compaudit1/)                        | NT-CAPACITY NT2 FAIL (054f42a33, 07:58)                       |
| C409| JOINT-BLINDNESS (composition_jointblind/)       | L3-INR-SEALED L3-KILLED (78cb7703c, 08:04)                    |
| C410| COGNITIVE-OPS-COMPOSE (cognitive_ops_compose/)  | GEN-STRESS BOUNDARY-FOUND ARENA-4MAP (5f612ec1a, 08:05)        |

Note: there is no watchdog collision at C408. The watchdog minted
COGNITIVE-OPS-LEARNER at C408 (0f7530e57, 08:00:38) 21 seconds after minting the
same experiment at C406 (44ecf987a), then conceded C408 to MP-3 (ff8a2d8df,
08:06:35). Canonical C406 = COGNITIVE-OPS-LEARNER and C408 = MP-3 LEARNED
MAGNITUDE both stand; 0f7530e57 is a superseded artifact, no experiment orphaned.

The 10 NT-chapter experiments from NT-SYNTHESIS, for reference:
NT1 NEGATIVE-TRANSFER, NT2 NT-CAPACITY, NT-EVICT-H1, NT-EVICT-H3, NT-D1, NT-D2,
NT-PORT, NT-PRESSURE, NT-LIFOBOUND, NT-FRESHCHURN.

## 4. Proposed resolution

Principle: the canonical ledger is the single source of truth for claim numbers.
The watchdog's own later commits already concede C404-C410 to the canonical
experiments, so canonical priority is consistent with the worker's own behavior.
Do not renumber canonical entries; renumber the displaced watchdog claims into
the next free block (watchdog series ends at C454, so C455-C460 are free),
preserving their original relative chronological order.

### 4a. Displaced claims: renumber C404-C410 era to C455-C460

| Old (watchdog msg) | New (proposed) | Experiment (verdict) |
|--------------------|----------------|----------------------|
| C404 | C455 | NEGATIVE-TRANSFER NT1 PASS: selective retention from entry-local evidence revision; 6/6 agreed kept, 6/6 contradicted revised, 12/12 untouched kept, FORGET=0, forward D=2, 3/3 byte-identical (c66edb1ba) |
| C405 | C456 | LIFETIME-META LM1: NO net meta-learning per B5a FAIL; B5b DECREASE PASS 84->9 on cluster episodes, control flat; outlier negative transfer + overshoot coupling diagnosed; 3/3 byte-identical (3385761b6) |
| C406 | C457 | GEN-STATEFIX UPGRADE-TO-SUBSUMES: 10-line fix restores P5 sequential growth ANS=3 TRIES=6 no WIDEN; zero regression on 9 subsumes + diamond batteries; 3/3 byte-identical; recommend retiring U (ea8c50a52) |
| C407 | C458 | NT-CAPACITY NT2 FAIL: eviction preempts revision, contradicted keys never complete revision, stable +7/pass churn, 41 vs 6 evictions; uncontested retention survives; diagnostic mapping exact envelope; 3/3 byte-identical (054f42a33) |
| C409 | C459 | L3-INR-SEALED L3-KILLED: incomplete-disambiguation trap kills L3 claim, T1 HELD 4/6 EDGES 12 FAIL; K5/K3/K7/K8/KC0D RED; reclassified L2+; honest arms pass; 3/3 byte-identical (78cb7703c) |
| C410 | C460 | GEN-STRESS BOUNDARY-FOUND ARENA-4MAP: frozen GEN cannot address 5+ structures, nm=5-7 silent corruption nm=8 panic; WIDEN breaks decline-soundness; 64-pool caps quantified; 3/3 byte-identical (5f612ec1a) |

### 4b. Watchdog-only claims: admit verbatim (no collision)

43 claims, C411-C416 and C418-C454, never in the ledger, no numbering conflict.
Admit with their watchdog numbers and one-line verdicts as minted:

- C411 LIFETIME-META-2 META-LEARNING DEMONSTRATED (eaf6d7ba1)
- C412 NT-EVICT-H1 FAIL (9bb51ff39)
- C413 U-RETIREMENT: U formally retired as separate mechanism (872d07428)
- C414 GEN-CYCLES PASS C1-C8 (2c9a62293)
- C415 META-GENERALIZE TRANSFER DEMONSTRATED (f20dddf0b)
- C416 NT-EVICT-H3 FAIL (aa777118c)
- C418 COMPRESSION-AUDIT (4e291843b)
- C419 META-FAMILY-B UNDECIDED (0ad24fbcb)
- C420 CYCLES-GENERALIZE PASS G1-G9 (902937145)
- C421 L3-INR-K10 independent red-team (df00ecbc5)
- C422 COGOPS-3WAY THREE-WAY COMPOSITION DEMONSTRATED (b93868439)
- C423 L3-NEXT L3-RX design (9af618be3)
- C424 CONTRACT-UNIFICATION SUBSUMES (5bfb7f445)
- C425 CYCLES-OSCILLATORY PASS O1-O9 (137b15129)
- C426 META-DISTRACTOR INTERFERENCE DEMONSTRATED (7703c4ddc)
- C427 NT-D1 FAIL informative (28a21a345)
- C428 CYCLES-CONVERGENT PASS (4d17a8b5b)
- C429 GEN-REDIM PASS exploratory, PROCESS-FAIL stray python3, EXPLORATORY pending clean repro (a0e7e45fe)
- C430 CYCLES-FEEDBACK INFORMATIVE-FAIL (6eb098c6b)
- C431 NT-D2 PASS K1-K5 (bcb60c008)
- C432 CYCLES-FEEDBACK-REFIX PASS (cf9ec673a)
- C433 COGOPS-DIAMOND DIAMOND COMPOSITION DEMONSTRATED (76bc20240)
- C434 GEN-REDIM-CLEAN CLEAN-REPRODUCTION-PASS; C429 PROMOTED EXPLORATORY to canonical (1c5095d45)
- C435 META-RECOVERY RECOVERY DEMONSTRATED CONVERGED (9b54b203b)
- C436 COMPOSITION-SYNTHESIS (9c709c1da)
- C437 NT-PORT PORT-PASS (e045b1e72)
- C438 GEN-NM10 INFORMATIVE (552328720)
- C439 NT-PRESSURE PORT-PASS-ALL (2db6c3df9)
- C440 MA1 META-ARCHITECTURE BUILD-PASS (4eaaffb38)
- C441 GEN-COGOPS-UNIFY FEASIBLE (88626d65b)
- C442 COGOPS-CYCLES CYCLES JOIN THE ENVELOPE (da79dcfd9)
- C443 SUBSUMPTION-P0 TWO mechanisms (847d4c849)
- C444 MA2 BUILD-PASS (11f148ccc)
- C445 NT-LIFOBOUND INCONCLUSIVE (71dc546f2)
- C446 GEN-POOLFLOOD PASS F1-F7 (c34adc8f0)
- C447 DEFECT-AUDIT (1075b82a2)
- C448 NT-FRESHCHURN FRESHCHURN-PASS-ALL (09cb461b0)
- C449 MA3 BUILD-PASS (30bd87586)
- C450 OPACITY-ERE (05d6cab9b)
- C451 COGOPS-OSCILLATORY INFORMATIVE-FAIL (0b2c593bc)
- C452 NT-SYNTHESIS: NT chapter closed (f116885f1)
- C453 L3-RX-BUILD CONDITIONAL-PASS 15/16; DISCLOSURE 2 python3 invocations, parent rules on PROCESS-FAIL (413df4dea)
- C454 CITATION-HYGIENE (6d9119b0a)

Caveats to carry into ledger entries: C429 stays EXPLORATORY (PROCESS-FAIL,
stray python3) until clean repro; C453 carries the 2-python3-invocation
disclosure and conditional status (RX-K10 red team pending).

### 4c. Probable duplicate: watchdog C417

Watchdog C417 (9d7afaec0, 08:15:27): "COGOPS-COMPOSE COMPOSITION DEMONSTRATED
K1-K6: two learner-owned procedures composed learner-driven, per-goal order
[R,V]/[V,R], version selection from coverage, plans persisted/reused, 10/10
agree, 3/3 byte-identical."

This appears to describe the same experiment as canonical C410
(COGNITIVE-OPS-COMPOSE, lane cognitive_ops_compose/, prereg db7d396a3), which
the watchdog itself had already conceded at C410 four minutes earlier
(9fd459b2e, 08:11:01). The kill-bar counts differ in the summaries (K1-K6 /
10/10 vs K1-K8 / 8/8), so duplication is probable but not established from
commit subjects alone.

Recommendation: verify C417 against the cognitive_ops_compose lane before
admission. If same experiment, mark C417 SUPERSEDED-BY-C410 and do not admit
as an independent claim. If distinct, admit as C417.

## 5. Citation remaps required if this proposal is adopted

These existing records use the displaced watchdog numbering and must be
updated to the C455-C460 numbers:

1. Watchdog C421 (df00ecbc5): "C409 KILL terminal untouched" refers to
   L3-INR-SEALED, i.e. proposed C459 (not canonical C409 JOINT-BLINDNESS).
2. Watchdog C447 (1075b82a2): "GEN-STRESS S1/S2/S4 confirmed-affected" refers
   to GEN-STRESS, i.e. proposed C460 (not canonical C410 COGNITIVE-OPS-COMPOSE).
3. Commit d0d59a968 (CITATION-HYGIENE, 10:06 UTC): "retarget GEN-STRESS S4
   (C410) citations to GEN-REDIM S4 (C434)". The "(C410)" here means GEN-STRESS,
   i.e. proposed C460. Affected files: citation_hygiene/CITATION_UPDATES.md,
   composition_synthesis/COMPOSITION_SYNTHESIS.md (1 line), gen_nm10/PREREG.md,
   gen_nm10/REPORT.md.
4. Watchdog C420 (902937145): "C403 regression clean" is ambiguous. No watchdog
   C403 was ever minted; canonical C403 is NODE-BLINDNESS, which is not a
   cycles regression target. Flag for the worker to clarify (likely an internal
   family numbering or a message error).
5. The NT-SYNTHESIS C452 message and any NT-chapter indexes that list the
   series as C404/C407/C412/... should gain a mapping note to C455/C458/...

References that need NO change (both ends watchdog-only, numbers preserved):
C432->C430, C434->C429, C436->C424, C442->C433, C443->C424/C436, C448->C445,
C450->C434.

## 6. Proposed ledger-write plan (needs approval)

1. Append 6 entries C455-C460 (section 4a) to CLAIM_LEDGER.md.
2. Append 43 entries C411-C416, C418-C454 (section 4b) with caveats noted.
3. Resolve C417 per section 4c before writing.
4. Add a short "renumbering record" note in the ledger mapping old watchdog
   message numbers to new canonical numbers (C404->C455, C405->C456,
   C406->C457, C407->C458, C409->C459, C410->C460) so future readers of the
   old commit messages are not misled.
5. Apply citation remaps in section 5 (items 1-3; item 4 pending clarification).

## 7. Hygiene flags (not part of the numbering proposal)

- The canonical C401-C410 entries (and a C398 touch-up) currently exist only as
  UNCOMMITTED working-tree changes to CLAIM_LEDGER.md (40 insertions). The last
  committed ledger state is C399 (ee7711b1e, 07:45 UTC). Uncommitted ledger
  content is at risk: on 2026-10-03 a faulty worker commit (b9999590) deleted
  136 ledger lines including C377-C410, requiring a restore commit (860f009b5).
  Recommend committing the working-tree ledger promptly, independent of this
  reconciliation.
- The watchdog's concession commits (9992a325e, 1611dc81c, 44ecf987a, c99bd82f5,
  ff8a2d8df, 92a1831a7, 9fd459b2e) agree with the canonical assignments and can
  serve as the audit trail for canonical priority; no history rewrite proposed.

## 8. Open questions for parent/main agent

1. Approve the C455-C460 renumbering of the 6 displaced claims?
2. Admit the 43 watchdog-only claims (C411-C416, C418-C454) to the ledger as
   listed, with the C429/C453 caveats?
3. How to dispose of watchdog C417 (verify-then-supersede vs admit)?
4. Who performs the ledger write (this worker on approval, or the parent)?
5. Should the uncommitted C401-C410 ledger entries be committed first, before
   appending C411+?

No ledger modifications were made in producing this document.
