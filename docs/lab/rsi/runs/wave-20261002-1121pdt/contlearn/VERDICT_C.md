# VERDICT_C: cross-kind rebind (exercise c) -- SEALED VERDICT

Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise c).
Date: 2026-10-02. Frozen prereg: PREREG_C.md (committed alone before
any implementation; K0 self-check below). Red team: REDTEAM_C.md
(5 attacks, all executed).

Note: hyphens only in this document; no em or en dashes.

## Governing bars (frozen before implementation)

C-R0 (count capability), C-R1 (rebind with DEP provenance), C-R2
(kind discriminator, KILL bar), C-R3 (control, KILL bar), C-R4
(integrity), C-R5 (determinism/hygiene), K0/K1/K2.

## Numbers (6 frozen runs, 2 binaries x 3 reps)

- C-R0: COUNTMAP_OK 6/6 (MAPs for (95001+i,43) answering 3). All 3 reps.
- C-R1: CHAINMAP_OK 6/6 (MAPs for (95001+i,40) answering 95201+i,
  type-1 DEP edges to phase-A facts). All 3 reps.
- C-R2: SIG_COUNT_OK 6/6 (>=2 tag-103 per count graph); SIG_REBIND_OK
  6/6 (0 tag-103 per rebind graph). All 3 reps.
- C-R3: CONTROL_MISS_OK 6/6 (answers -2); CONTROL_NOMAP 6/6. All 3 reps.
- C-R4: RETENTION_OK 6/6 (answers 3); FACTSTABLE 18/18. All 3 reps.
- C-R5: 3/3 byte-identical SHA-256 per binary (full
  c33a16d4bae8a9b4c80e4a6e5f39e8a4df9283cc19c2312cd9ca3a127842ad87,
  nophase
  563253644b03b9721aeae29a79cafd7f13faaa6420bdf83b60464872c58fb8df);
  FNV stable; rc 0 on all 6; 0-byte stderr; 99/69 events with
  AUDIT_PASS; CAP_GUARD_OK; 1 process/run; empty argv/env; 2 pre-run
  builds, 0 during runs.
- K0: PREREG_C.md (494553776) strictly before any xk_* file. PASS.
- K1/K2: safebin; 0 cognition functions in drivers. PASS.

## Verdict: PASS (scoped claim)

REBIND-CROSS-KIND is adopted in the SCOPED form the red team
forces: within one continuing learner without reset, phase-A chain
content learned and exercised as COUNT (C-R0) is reused as CHAIN
(C-R1), with the kind shift discriminated white-box via t2_sig
(C-R2: 0 vs >=2 INC cells) and the dependence on phase-A structures
proven by the control (C-R3). DEP provenance cites phase-A facts
only; INT3/INT1 facts are not smuggled.

Scope limitation (red-team attack 1, sustained): the COUNT MAPs are
NOT causally upstream of the CHAIN MAPs (probe: CHAIN builds fine
with no COUNT MAPs ever existing). The rebound "learned structure"
is the phase-A chain content, not a MAP-transformation. The
stronger "COUNT MAPs transformed into CHAIN" does not hold and is
not claimed.

What this is: L2 evidence of cross-kind reuse of learned content
within a continuing learner. What this is not: structural
transformation, L3, or invention (the trial's chain assembly is
frozen machinery).

## Keep / discard

- KEEP: cross-kind content reuse as a continuing-learner capability;
  the t2_sig kind discriminator as a reusable white-box tool.
- DISCARD: nothing; no kill bar fired.
- QUEUED NEXT: lane REPORT.md, then final report to parent.

## Commit ids (lane branch lane-contlearn-20261002-1121pdt, local only)

- 494553776 PREREG_C.md frozen (alone).
- (pending) implementation + transcripts + scripts + REDTEAM_C.md +
  VERDICT_C.md commit.
