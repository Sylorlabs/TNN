# Supersession bindings update: wave-20261002-0221pdt RECORDS lane

Worker: RECORDS lane. Date: 2026-10-02. Wave: wave-20261002-0221pdt.
Scope: record bookkeeping item queued from wave-20261001-2321pdt
(WAVE_RECORD.md line 95: "Record bookkeeping: supersession bindings,
SHA-256 typo fix in LEARNER_MECH_ANALYSIS.md"; also queued as item 26
in this wave's BACKLOG.md).

## The current bindings record

A "supersession binding" is the annotation that ties a superseded claim
to the verdict that superseded it. The current bindings record consists
of two parts:

1. The canonical ledger's status entries:
   `docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
   (SUPERSEDED status lines plus the status tally near line 4567).
2. The supersession parenthetical notes on verdict lines in the wave
   records (the H7R/H6R fix pattern: a note on the superseded claim's
   line naming the superseding verdict).

This lane does not edit canonical records (worker must not edit the
wave record or the ledger). Missing or stale binding entries are
completed below as exact old/new byte citations for the coordinator
to apply.

## Survey: every known superseded claim

### Complete (verified, no action)

1. **C63 (Evidence-first paper draft, 34 claims) SUPERSEDED by the v1
   and v2 clean papers.** Bound in the ledger entry ("Status:
   SUPERSEDED, not evidence. Superseded by the v1 clean paper
   (94c30752f) and the v2 clean paper (89cf970ee)") and in the status
   tally ("SUPERSEDED: C63 (paper-derived 34-claim draft; superseded by
   the v1 and v2 clean papers)"). Complete.

2. **C84 (LORG standalone engine) SUPERSEDED by C89 (CLA-2
   consolidation).** Bound in the ledger entry ("Status: SUPERSEDED by
   C89. Per Micah's consolidation ruling, LORG must not become a
   separate permanent memory subsystem; its useful ideas were folded
   into the CLA-2 workspace") and in the tally ("SUPERSEDED: C84 (LORG
   standalone engine; superseded by the C89 CLA-2 consolidation)").
   Complete.

3. **Old C1 wave SUPERSEDED by C03.** Bound in the tally
   ("EXPLORATORY: old C1 wave (superseded by C03)"). Complete.

4. **C60 technical findings SUPERSEDED by the C70 clean rebuild.**
   Bound in the tally ("C60 technical findings (superseded by the C70
   clean rebuild)"). Complete.

5. **CONTLEARN "LEARNOWN-DEMONSTRATED" SUPERSEDED by CONTLEARN-OWNED
   "MACHINERY-DEPENDENT" (wave-20261001-2321pdt).** Bound in
   WAVE_RECORD.md line 40, which now carries "[Supersession note:
   CONTLEARN-OWNED (this record) refines the
   "LEARNOWN-DEMONSTRATED" label: integration is MACHINERY-DEPENDENT
   (0/6 with machinery disabled vs 6/6 control); the demonstrated
   integration sits on the researcher side of the control-plane
   line.]". The RECORD-CHECK A1 recommendation was applied. Complete.

6. **H7R worker "3/3 passing" claim SUPERSEDED by the H6R BUILD-FAIL
   verdict (wave-20261001-2321pdt).** Bound in WAVE_RECORD.md line 61
   parenthetical ("Note: the "3/3 passing" claim in the worker's
   report is superseded by the H6R BUILD-FAIL verdict recorded below;
   the substrate halves are H2R PASS, H7R PASS, H6R FAIL."). Complete.

7. **BATTERY-E4 commit chain (A3).** Not a claim supersession; the
   record error was corrected in WAVE_RECORD.md line 69 ("[Correction:
   the original line cited b63f80289 as E4's prereg; b63f80289 is
   ARENA5's commit ... E4's prereg content was restored byte-identical
   at 5a2c7c91c before any E4 implementation commit; the E4-attributed
   chain is 5a2c7c91c -> f26ddb294 -> 67680ebb1 -> 61df738fe.]").
   Complete.

8. **H5R2-BASELINE "BASELINE-MATCHES" vs H5R2-DECOY
   "DECOY-DISCRIMINATES".** Explicitly recorded as RESOLVED, not
   contradicted ("Interpretation: BASELINE-MATCHES is RESOLVED, not
   contradicted"), so no supersession binding applies. No action.

### Missing or stale (completed below)

9. **TNN3-SUBSTRATE "Unblocks H6R" vs H6R BUILD-FAIL (RECORD-CHECK A2):
   binding MISSING.** WAVE_RECORD.md line 36 still reads, unqualified:
   "Unblocks H2R/H6R/H7R and H4R's construction half". The H6R verdict
   (line 68) BUILD-FAILs on B3/B4 with a substrate design gap (standing
   values live on kind-904 record nodes that are never
   protection-pinned; lbid 0 invisible to the selector; eviction
   destroys standing, so no world can express preferential retention),
   and the H7R line (61) records "the substrate halves are H2R PASS,
   H7R PASS, H6R FAIL". The A2 annotation recommended by RECORD-CHECK
   was never applied. Completed binding entry below (B-9).

10. **Decline-gate retirement via C180 subsumption: binding MISSING in
    the canonical ledger.** The retirement is bound in lane-level
    records ("decline gate retired because dedup subsumed it (ledger
    C180)" in `docs/lab/rsi/runs/wave-20261001-2321pdt/CONSEQ/JUDGE_BRIEF.md`
    lines 10-11 and 37-38; "C180 (DEDUP-DECLINE-INTEGRATION, decline
    gate retired, dedup subsumed decline)" in
    `docs/lab/rsi/runs/wave-20261001-2321pdt/C174/PREREG_C174.md` line
    14 and `.../C174/JUDGE_BRIEF.md` line 12). But the canonical
    ledger's decline entries carry no retirement binding: C161
    (DECLINE-GATE-COMPLETE) ends with "First mechanism to bend DYN-1"
    and its bounded-L2 classification with no retirement note, and
    C179 (DECLINE-ADV-COMPLETE) still reads "Status:
    ADVERSARIAL-SURVIVES (exploratory)" with no note that the gate was
    retired. Note: retirement does not refute the C161/C179 evidence
    (the gate did bend DYN-1; the adversarial battery did survive); it
    retires the mechanism's future use because dedup subsumed it.
    Completed binding entries below (B-10a, B-10b).

11. **H7R "Dispatched ARENA5 as the replacement build" (RECORD-CHECK
    A4):** possible copy error, flagged for the coordinator; not a
    supersession binding issue. No binding entry to complete; left as
    an open coordinator check.

## Completed binding entries (for the coordinator to apply)

### B-9: TNN3-SUBSTRATE line annotation

Location: `docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md`,
line 36 (the TNN3-SUBSTRATE verdict line).

Old bytes (exact current text to annotate):

```
Frozen kill bars KB-H2R/H4R/H6R/H7R for the re-attempts. Unblocks H2R/H6R/H7R and H4R's construction half; H4R's closed loop still gated on Micah's pending EXECUTE placement ruling.
```

New bytes (annotation appended to that sentence, mirroring the
H7R/H6R fix pattern):

```
Frozen kill bars KB-H2R/H4R/H6R/H7R for the re-attempts. Unblocks H2R/H6R/H7R and H4R's construction half; H4R's closed loop still gated on Micah's pending EXECUTE placement ruling. (Supersession note: the "Unblocks H6R" statement predates the H6R BUILD-FAIL verdict recorded below (line 68). H6R's B3/B4 show the package unblocks H6's accumulation and integration bars but leaves a substrate design gap: standing values live on kind-904 record nodes that are never protection-pinned and carry lbid 0 (invisible to the selector), so no world can express preferential retention of high-standing nodes. The substrate halves are H2R PASS, H7R PASS, H6R FAIL, per the H7R line.)
```

### B-10a: C161 decline-gate retirement binding

Location:
`docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`,
C161 entry (ends with the "First mechanism to bend DYN-1." paragraph).

Old bytes (exact current closing text):

```
Counterfactual check passes (same probe behaves differently across histories, mediated by the tally, caused by the miss_inquire write path). Classification: bounded L2; the N=3 criterion is researcher-authored, not learner-internal.
```

New bytes (retirement binding appended; evidence status unchanged):

```
Counterfactual check passes (same probe behaves differently across histories, mediated by the tally, caused by the miss_inquire write path). Classification: bounded L2; the N=3 criterion is researcher-authored, not learner-internal. (Retirement binding: the decline gate was retired after C180 (DEDUP-DECLINE-INTEGRATION) showed dedup subsumes decline (combined run byte-identical to dedup-only); "decline gate retired because dedup subsumed it (ledger C180)" per the 2321pdt CONSEQ judge brief. This retirement concerns future use, not the evidence above, which stands.)
```

### B-10b: C179 decline-gate retirement binding

Location:
`docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`,
C179 entry.

Old bytes (exact current status line):

```
- C179 (DECLINE-ADV-COMPLETE; commit c7f4df907, 2026-10-01): SURVIVES
  with 3 NEEDS-FIX (exploratory adversarial, no frozen prereg).
```

New bytes:

```
- C179 (DECLINE-ADV-COMPLETE; commit c7f4df907, 2026-10-01): SURVIVES
  with 3 NEEDS-FIX (exploratory adversarial, no frozen prereg).
  (Retirement binding: the decline gate was retired after C180 showed
  dedup subsumes decline; see the B-10a binding on C161. The
  adversarial-survival evidence stands; the mechanism is not to be
  continued.)
```

## SHA-256 typo fix (companion bookkeeping item)

Applied separately and committed as 59dc25ece with an explicit
pathspec to
`docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md`
only. Both SHA-256 statements for the frozen TNN-2 core (commit
f4de7ff46) carried a corrupted 79-hex-char string; replaced with the
true 64-hex-char hash verified by
`git show f4de7ff46:tnn2.zag | sha256sum`.

Old bytes (both occurrences, lines 11 and 15):

```
a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
```

(79 hex chars; not a valid SHA-256.)

New bytes (both occurrences):

```
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
```

(64 hex chars; verified true hash. The freeze blob
`b226b223cb3ee0be742af673653fb8ea8605f281` in the same paragraph was
verified correct via `git ls-tree f4de7ff46` and left untouched. The
C186 persistent-connections REPORT.md independently cites the same
true hash, confirming the correction.)
