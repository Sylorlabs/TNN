# RESULT_PI_REV2.md

Wave: wave-20260929-2321pdt. Prereg: PREREG_PI_REV2.md (frozen, committed
alone at 7c11ac5af, wave-20260929-1721pdt design lane first act).
Implementation: pi_rev2/proc_revise2.zag (committed at 847a8f10f; pure Zag;
pinned znc 498abcb5).

## What was built

Procedure-invention v2 revision machinery: procedure store (versioned,
ACTIVE/SUBSUMED), example log (CURRENT/SUPERSEDED, never deleted),
monitor loop (predict-vs-actual mismatch detection), diagnosis operator
(position-ascending rank over (p, byte) candidates covering the failing
set; conflicts recorded), primitive-construction kit (mechanical
byte-equality test from a diagnosed (p, b)), SPECIALIZE revision
operator (v_new = IF(P_test, alt, v_old)), conflict rule (newer trusted
evidence overrides; SUPERSEDED provenance), ROLLBACK(v).

The discovery enumeration was ported byte-verbatim from the frozen
H-REVISE source docs/lab/research-lead/overnight-20260928/sem_l3/
proc_revise_test.zag (lines 12-162: z_alloc through print_prog).
cmp-verified at implementation time: the ported block in proc_revise2.zag
(lines 22-172) is byte-identical to the frozen source block (sha
155c4cf1ff075b05a9f809b9704b3ca3b3cece1f3d90ba7ec8f22fc9bdac5bffdcefcdba0f9f4ef66
of the extracted block matched on both sides). The enumeration loop was
wrapped as benum() with identical algorithm; enumeration count 1055
matches the frozen v1 count.

## Evidence

Frozen binary built from the committed source (847a8f10f; working tree
verified identical to the committed blob before building).

P0-P7+P9 run (no argv), 3 executions, byte-identical (sha256 9718685f):
18/18 in-binary checks PASS, zero FAIL. Key lines:

- enumerated 1055 programs
- P0a: PI-1a reverse found; PI-1b identity at index 0 (K-RV2-5)
- P0: discovered index 38 [N C1 SUB]; semantic check n-1 for n=1..6 PASS
- P2: COUNTEREXAMPLE_DETECTED(xab) (v1 predicted "bbb")
- P3: DIAGNOSIS pos=0 byte=120 conflicts=1; K-RV2-1b impossibility
  recheck on the port: no program fits T+F1 (search returned -1)
- P4: PRIMITIVE-CONSTRUCTED pos=0 byte=120
- P5: alt = index 2 (C0 broadcast-first)
- P6: SUPERSEDED rec=1 ("xy"->"yy"); VERSION v2 ACTIVE (parent v1);
  STRUCT base=38 nbranches=1 br0=(0,120)->2
- P7: "abc"->"ccc", "xy"->"xx" (CHANGED per the frozen conflict rule),
  "defg"->"gggg", "xab"->"xxx"; "xqw"->"xxx" with no new revision
  (F1-reuse); R cell 8/8
- P9: ROLLBACK to v1; "xab"->"bbb" (mispredicted again), "xy"->"yy"
  restored, "abc"->"ccc" (K-RV2-2 ablation)

P8 adversary F2: single execution of the frozen binary with argv[1]=i.
The adversary byte was chosen by a declared deterministic rule before
the run: first letter of the frozen allowed set {i,j,k,l,m,n,o,r,t,u,v,w}
in sorted order, removing designer discretion. Result (exit 0,
BUILD-PASS, fails=0):

- COUNTEREXAMPLE_DETECTED(iab); DIAGNOSIS pos=0 byte=105 conflicts=0
- PRIMITIVE-CONSTRUCTED pos=0 byte=105; alt = index 2 (C0)
- VERSION v3 ACTIVE (parent v2)
- "iab"->"iii"; "xab"->"xxx", "abc"->"ccc", "xy"->"xx",
  "defg"->"gggg" all unchanged
- same-class reuse "iqw"->"iii" with no new revision
- R cell 8/8 after P8; P9 rollback re-verified

The designer did not iterate on F2: the F2 phase was executed exactly
once, after all P0-P7+P9 debugging was complete, and no source change
followed the F2 run.

## Kill-bar scorecard

- K-RV2-1 (L3-gate operationalization): (a) PASS. Grep audit over the
  implementation: zero char literal 'x', zero numeric literal 120; the
  strings "xab"/"xxx"/"xqw" occur only in main() as fixture declarations
  and expected-output strings (lines 702-826). The invented primitive
  (0,120) first appears at runtime in the P4 construction line.
  (b) PASS. Impossibility rechecked on the port: dsearch over T+F1
  returns -1. (c) PASS. White-box trace: DIAGNOSIS pos=0 byte=120
  derived from the F-vs-P comparison (conflicts=1 recorded).
  (d) PASS. F1-reuse "xqw"->"xxx" with no revision; F2 revised correctly
  on first execution. (e) PASS. P_x persists as the ACTIVE procedure's
  condition (STRUCT br0=(0,120)->2; v3 adds (0,105)->2).
- K-RV2-2 (not re-search): PASS. v1 (prog 38) structurally contained as
  the else-branch (base=38 with branch list); version history v1->v2->v3
  with provenance; ROLLBACK(v1) restores exactly v1 behavior
  ("xab"->"bbb", "xy"->"yy").
- K-RV2-3 (autonomous detection): PASS. F1 detected via predict-vs-actual
  mismatch; observe() source audited: no branch on input content, only
  predict() arithmetic and predicted-vs-actual byte comparison.
- K-RV2-4 (regression cell R): PASS. 8/8 after P6 and 8/8 after P8.
- K-RV2-5 (discovery regression): PASS. Reverse found; identity at
  index 0. Disclosure: the ported extract_seq returns -1 for
  "hello"->"olleh" (a repeated letter breaks the unique-occurrence
  extraction), and prog_fits treats that pair vacuously; this quirk is
  inherited byte-verbatim from the frozen v1 source and was not altered.
  The reverse program is genuinely constrained by the abc/def/xy pairs.
- K-RV2-6 (determinism): PASS. Full P0-P7+P9 run 3/3 byte-identical.
- K-RV2-7 (generality / anti-tuning): PASS on first execution. Grep
  audit post-disclosure: zero char literal 'i'; zero string literals
  "iab"/"iii"/"iqw" (F2 strings built at runtime from argv bytes); the
  byte 'i' occurs only inside the frozen allowed-set declaration
  "ijklmnortuvw" (fixture declaration in main's F2 phase).

Verdict per the reorientation label rule: BUILD-PASS (bounded revising
mechanism, all frozen bars pass). No promotion: the 11-step pipeline
(independent reproduction, baseline attack, OOD, ablation, transfer,
independent red team, governance audit) is queued next. The L3
criterion-12 claim and Criterion 0 stay open for that pipeline.

## Standing skeptic attacks (status after evidence)

- S1 (researcher-added-primitive): the kit is generic and was frozen
  before F2 was known; the specific primitives (0,120) and (0,105) were
  data-constructed. Whether this satisfies Micah's gate is the debate's
  call; the evidence above is the exhibit.
- S2 (kit boundedness): confirmed bounded; only byte-equality tests at
  positions. Not a general reviser; disclosed.
- S3 (menu at one remove): the diagnosis space is finite (positions x
  256 bytes); the composed conditional was never enumerated as a
  complete candidate. Recorded for the debate.
- S4 (position-ascending bias): frozen and disclosed; F2 (a first-letter
  world) passed on first execution, which constrains gerrymandering
  claims but does not retire the attack.
- S5 (trust): residual; observed examples trusted; not tested.

## Provenance

New this wave: proc_revise2.zag (Section B machinery; Section A ported
byte-verbatim), the frozen binary build, run evidence (3/3 determinism,
single F2 execution), audits, debate records, wave record. Inherited:
PREREG_PI_REV2.md, the H-REVISE fixture set, Family X training set,
RT2-A regression pairs, the 1421pdt M5 banked commitment, reorientation
directives. The "875-regression cell" note remains ungrounded; R is the
8-pair cell defined in the prereg.
