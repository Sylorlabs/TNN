# Supersession bindings update: wave-20261002-0521pdt RECORDS lane

Worker: RECORDS lane. Date: 2026-10-02. Wave: wave-20261002-0521pdt.
Scope: record bookkeeping item (26) from the 0221pdt backlog: update
the supersession bindings record for the 0221pdt wave's verdicts.
This lane does not edit canonical records (wave records, the ledger);
missing or stale binding entries are completed below as exact old/new
byte citations for the coordinator to apply.

## The bindings record

A "supersession binding" ties a superseded, bounded, or killed claim
to the verdict that changed its status. The record has two parts: (1)
the canonical ledger's status entries
(`docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`,
SUPERSEDED status lines plus the status tally), and (2) supersession
parenthetical notes on verdict lines in the wave records.

## Status of the 0221pdt completed entries

The 0221pdt RECORDS lane completed three binding entries (B-9,
B-10a, B-10b) for the coordinator to apply. Verified this wave: NONE
of the three has been applied.

- B-9 (TNN3-SUBSTRATE "Unblocks H6R" annotation): the
  wave-20261001-2321pdt WAVE_RECORD.md line 36 still reads,
  unqualified, "Unblocks H2R/H6R/H7R and H4R's construction half".
  The H6R BUILD-FAIL annotation is still missing. STILL PENDING.
- B-10a (C161 decline-gate retirement binding): the ledger C161
  entry carries no retirement note. STILL PENDING.
- B-10b (C179 decline-gate retirement binding): the ledger C179
  entry still reads SURVIVES with 3 NEEDS-FIX and no retirement
  note. STILL PENDING.

These three remain open coordinator actions. They are not re-cited
below; the 0221pdt SUPERSESSION_UPDATE.md (commit ac7f14ba6) holds
their exact old/new bytes.

## Survey: 0221pdt verdicts and their binding implications

### Already bound in the wave record (verified, no action)

1. **DDES steps 4+5 BUILD-PASS (reproduction step).** The 0221pdt
   WAVE_RECORD.md DDES line already carries the citation bounds:
   "the three binding caveats still bind every citation", and the
   DDES-ALT line records H1 ATTACK-SUCCEEDS, H2 EVIDENCE-HOLDS, H3
   ATTACK-SUCCEEDS with the explicit restriction that DDES citations
   must not imply DDES "reasons about" or "detects" the t*=0 boundary
   (H3: the p0==p1 alarm is a generic coincidence alarm; H1: FLAG
   unconsumed by downstream decisions), and that the measured
   guidance contribution is narrow and mechanical (bounded L2,
   nothing about L3). Ceiling: bounded L2 with persistence. Complete.

2. **INDEX Part A CONFIRMED.** The 0221pdt WAVE_RECORD.md line 21
   already records the supersession: "The C204 measurements are
   promoted from exploratory to preregistered-confirmed evidence"
   (1393x indexed scan reduction at 1000 MAPs, 693x at 500, 140x at
   100, move-to-front emergent ordering, FACT index reductions, all
   reproduced cleanly in pure Zag under safebin, 3/3 byte-identical).
   This supersedes the earlier contaminated exploratory measurements
   (the 1000-MAP scaling wave that went PROCESS-FAIL after a
   self-disclosed python3 invocation). The red-team caveat stands:
   the claim holds on intact index state (Part B hardens the
   corrupt-state behavior). Complete.

3. **CONTLEARN3 BUILD-PASS.** The 0221pdt WAVE_RECORD.md line already
   carries "BINDING CLAIM BOUND (restated)": proposal CONTENT
   (mech=TRY_CHAIN) is a fixed researcher template; no claim of
   learner authorship of proposal content, learner scheduling of
   initiation, or learner agency; refusal branch structurally
   enforced but empirically unexercised (0 MACHINERY_SKIPPED); no L3,
   no generality; citation stays machinery-enabled per debate Q7
   binding form. Complete.

### New binding entries (completed below for the coordinator)

4. **F1 repair-time policy: RETAINED at bounded L2+, followup
   BUILD-FAIL recorded (B-12).** The 0221pdt WAVE_RECORD.md line 23
   records the F1 POLICY-C BUILD-PASS (all 12 decisive frozen bars;
   bounded L2+ ceiling stands). After that wave closed, the
   F1-FOLLOWUP sealed eval (commit db3cc7086) returned VERDICT
   BUILD-FAIL: R = 3/40 below the frozen floor (SENS bar requires
   R >= 4); the bar was not weakened; "F1's BUILD-FAIL is untouched.
   No promotion." The F1 line needs an annotation so the
   bounded-L2+ BUILD-PASS is never cited without the followup
   failure. Completed entry below (B-12).

5. **H5R2-SYNTH: KILLED (B-13).** Commit e847c860d:
   "H5R2-SYNTH implementation + sealed eval (VERDICT BUILD-FAIL)".
   Bar scoreboard (HPI/synth/VERDICT_SYNTH.md): SYN-NR-SEP HOLD;
   SYN-NR-DECOY FAIL, SYN-NR-CHAIN FAIL, SYN-NR-BATT FAIL, SYN-DT
   FAIL; SYN-DET/PURE/ORDER/SCOPE/ARCH HOLD. "The
   newest-live-among-all-live gate is newest-biased in exactly the
   way the decoy family was built to punish: it relabels ties rather
   than resolving them and regresses the frozen battery. The named
   synthesis hypothesis is killed." There is no ledger entry and no
   wave-record line for H5R2-SYNTH (it landed after the wave record
   closed), so the kill exists only in commit-level docs. Completed
   entry below (B-13): a wave-record kill note for the coordinator.

6. **DEVANG4: KILLED for this design iteration (B-14).** Commit
   c68ea3b42: sealed evaluation VERDICT BUILD-FAIL. Killing bars:
   K_SEG 4/12 < 9/12 and K_DISC 2/6 < 5/6. The report's own
   diagnosis distinguishes the two: K_DISC failure with K_AUD passing
   is a mechanism result; K_SEG failure is a test-design result (the
   prereg-frozen B-prime spec generator is flawed, load-bearing for
   the next iteration). No ledger entry; verdict in commit-level
   docs (DEVANG/SEALED_EVAL.md) only. Completed entry below (B-14):
   a kill note that preserves the diagnosis split so the next
   iteration fixes the generator flaw rather than re-running a
   flawed spec.

7. **INDEX Part B: FIX-VERIFIED (B-15).** Commit 589b34dc5: the
   index-cycle panic (slice out of bounds) reproduced pre-fix with a
   minimal pure-Zag reproducer; fixed walk pattern 6/6;
   index-validation gate matrix 8/8 (rejects corrupt shapes incl.
   OOB pointers, accepts healthy state at full scale); final fixed
   rebuild 3/3 byte-identical to canonical hash. The 0221pdt wave
   record line 22 records this. The binding implication: the earlier
   standing finding ("index cycle crashes the indexer; index
   validation is needed before production") is now closed by the
   fix; production use must route through the validation gate. No
   annotation needed on the wave record (it already records
   FIX-VERIFIED); recorded here so the crash finding is not cited
   as open. No coordinator action.

### No binding change (noted for completeness)

8. **F1 probe-menu equivalence attack: FAILS.** Best single-node f
   32/60 vs S 60/60; oracle 0/30 vs 30/30 on W2; F-B not declarable
   from source alone; F-C vacuous. "F1's C0-B standing is not reduced
   by this attack." No status change; no binding entry.

9. **E3BLIND: IN-S1/S2/S3 CONFIRMED-BLIND.** Blind re-examination
   confirming earlier claims, not a supersession. No binding entry.

10. **HPI sub-task A (H-PI-REV2 step-5): REEXEC-PASS** with debate Q2
    qualifiers carried. No status change; no binding entry.

11. **INTERACTIVE: WORKS.** A runnable interactive TNN exists
    (tnn_chat.zag rebuilt, sha256 matches AUTHORITY_MANIFEST.md,
    5-exchange probe chat byte-captured). Not a cognition claim; no
    binding entry. Process note: the lane commit 9139a579c swept the
    coordinator's in-flight repair staging into a lane commit
    (non-pathspec); bytes verified identical; process incident only.

## Completed binding entries (for the coordinator to apply)

### B-12: F1 line followup annotation

Location: `docs/lab/rsi/runs/wave-20261002-0221pdt/WAVE_RECORD.md`,
line 23 (the F1 repair-time policy verdict line).

Old bytes (exact current closing text of that line):

```
post-freeze sealed family + source audit attacks still queued for any promotion path. Commits c5c9afa3b, 835eebf71 (prereg alone), 97d1ce0db, 409607f81, 73bb0c950, a5e4850a6.
```

New bytes (annotation appended):

```
post-freeze sealed family + source audit attacks still queued for any promotion path. Commits c5c9afa3b, 835eebf71 (prereg alone), 97d1ce0db, 409607f81, 73bb0c950, a5e4850a6. (Followup note: the F1-FOLLOWUP sealed eval (commit db3cc7086) returned VERDICT BUILD-FAIL: R = 3/40 below the frozen SENS floor (R >= 4); the bar was not weakened. The bounded-L2+ BUILD-PASS above stands but is not promoted, and must not be cited without this followup failure.)
```

### B-13: H5R2-SYNTH kill note

Location: coordinator's choice (no existing wave-record line; the
verdict lives in commit e847c860d,
`docs/lab/rsi/runs/wave-20261002-0221pdt/HPI/synth/VERDICT_SYNTH.md`).
Suggested: append to the 0221pdt WAVE_RECORD.md verdicts section or
the H5R2 ledger area when one exists.

New bytes:

```
- H5R2-SYNTH: VERDICT BUILD-FAIL (commit e847c860d). The
  newest-live-among-all-live synth gate failed its sealed bars
  (SYN-NR-DECOY, SYN-NR-CHAIN, SYN-NR-BATT, SYN-DT FAIL;
  SYN-NR-SEP HOLD). The gate relabels ties rather than resolving
  them and regresses the frozen battery. The named synthesis
  hypothesis is killed. H5/H5R must not be cited as viable via this
  gate; queued next is a structurally different discriminator, not
  another tie-breaking rule. Prereg 5b2f8e0f0 frozen alone; 12
  sealed worlds, 3/3 byte-identical.
```

### B-14: DEVANG4 kill note

Location: coordinator's choice (verdict lives in commit c68ea3b42,
`docs/lab/rsi/runs/wave-20261002-0221pdt/DEVANG/SEALED_EVAL.md`).
Suggested: append to the 0221pdt WAVE_RECORD.md verdicts section.

New bytes:

```
- DEVANG4: VERDICT BUILD-FAIL (commit c68ea3b42). Killing bars:
  K_SEG 4/12 < 9/12 and K_DISC 2/6 < 5/6. Diagnosis split per the
  report: K_DISC failure with K_AUD passing is a mechanism result;
  K_SEG failure is a test-design result (the prereg-frozen B-prime
  spec generator is flawed). This design iteration is killed; the
  next iteration must fix the B-prime generator flaw before
  re-testing segmentation, and address the K_DISC mechanism gap.
  DEVANG4 must not be cited as working.
```

## SHA-256 typo fix (companion bookkeeping item 26, second half)

Already applied and verified. Commit 59dc25ece (2026-10-02 09:41:12
UTC) replaced the corrupted 79-hex-char SHA-256 string in
`docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md`
(both occurrences) with the true 64-hex-char hash
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
verified against `git show f4de7ff46:tnn2.zag | sha256sum` and the
freeze blob `b226b223cb3ee0be742af673653fb8ea8605f281` (`git ls-tree
f4de7ff46`). This lane re-verified: the corrupted string occurs zero
times in the current file; the true hash occurs exactly twice. No
further action.

Note: no em-dashes are used in this document.
