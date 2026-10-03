# PREREG-INVENT: H-CONTLIFE-5 follow-up -- Learner-Invented Revision Procedure

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/hcontlife5-invent/`
only. New files: PREREG-INVENT.md (this file), NAMECHECK.md,
src/invent.zag, bin/invent, runs/invent-run{1,2,3}.txt,
REPORT-INVENT.md. The frozen `hcontlife5/` lane (PREREG.md, REPORT.md,
PREREG-REVISE.md, REPORT-REVISE.md, src/selfjudge.zag, src/revise.zag)
is read but never modified; its round-1 and round-2 case tables are
copied verbatim into the new implementation (verified by diff of the
table function bodies at build time).
Worker: H-CONTLIFE-5-INVENT (subagent, 2026-10-02). Replacement for a
completed worker (H-CONTLIFE-5-REVISE).
Parent mandate: close the invention gap. REVISE (REVISION-PASS, R0..R7)
showed the evaluation to action loop works with a researcher specified
revision procedure (leave-one-out plus median); the learner owned the
trigger, the attribution, and the adoption, not the invention of the
procedure. This wave asks whether the learner can INVENT its own
revision procedure: construct it from generic operations in a
combination the researcher did not specify, guided by its own
self-check against observed failures.

## 1. What is being tested

The invention step of the commit to consequence to judge to revise
loop. Everything except the procedure source is held identical to
REVISE: same trigger (self-judged failures only), same attribution
(learner-owned leave-one-out license computed from training values plus
the observed consequence), same adoption gating (persistent learner
state, applied to future commitments with imperfect training fit),
same round-1 set (frozen C337 24 cases), same round-2 fresh set (24
cases), same no-revision control arm. The single change: in P4, instead
of adopting the researcher-specified median-of-LOO procedure, the
learner searches a construction space of generic-operation compositions
and adopts the first composition that passes its own self-check. The
claim under test is learner-constructed revision: the adopted procedure
as a composed unit appears nowhere in this prereg and in no
researcher-written branch of the implementation; it exists in the
binary only as data (an instruction array in learner state) written by
the generic search.

What counts as invention here (not menu selection): the researcher
supplies generic operations (section 2), a composition grammar, a fixed
generic enumeration order, and a self-check protocol. The researcher
does NOT supply candidate procedures, does NOT name or describe any
target composition, and does NOT order the search to land on any
particular answer. The adopted composition is determined by the
learner's search against its own observed failure data. Section 3
states this as an auditable declaration.

Honest scope: the claim sought is L2 structural learning (the learner
constructs a new procedure from generic mechanisms), the same honest
rating as C335 (learner-invented full-store victim selection). The L3
bar (not enumerated as solution space, unforeseen forms, adversary
designed evaluation families) is explicitly not claimed.

## 2. The construction space: exact specification

### 2.1 Instruction inventory (generic operations, fixed order)

Five instructions, listed in the fixed enumeration order used by the
search (index 0 to 4):

0. `fit`: fit an affine line on the current point set S (S starts as
   all three training points) and push the prediction at x*. The
   lane's affine fit primitive: the line through the two retained
   points of smallest x (for the full set this is the frozen commit
   fit, a = y1 - y0, b = y0; after an exclusion it is the standard
   two-point fit, identical to the loo_pred used in REVISE).
1. `exm`: replace S by the full three-point set minus the point with
   largest absolute residual from the full fit. Residuals from the
   lane's fit are r0 = 0, r1 = 0, r2 = |2a + b - y2|; ties go to the
   lowest point index. This is a data-responsive exclusion primitive;
   its exact behavior under the lane's fit is documented here, not
   tuned: with r0 = r1 = 0 it removes point 2 whenever r2 > 0.
2. `loo3`: push the three single-exclusion predictions (exclude point
   0, exclude point 1, exclude point 2; each a two-point fit evaluated
   at x*). A generic jackknife-style primitive. Does not modify S.
3. `med`: replace the prediction stack by its median. Defined for any
   stack depth: sort ascending (insertion order is deterministic),
   take the element at index (n-1)/2 (the lower middle for even n).
4. `avg`: replace the prediction stack by its integer mean
   (truncated sum divided by count).

Each instruction is a generic, domain-neutral operation. None is a
revision procedure by itself.

### 2.2 Program grammar

A revision procedure is a program: a sequence of 1 to 4 instructions.
Validity rules (checked by the search, not by hand):

- (V1) The last instruction must be `fit`, `med`, or `avg` (a program
  must yield exactly one prediction).
- (V2) Every `med`/`avg` must have at least one pushing instruction
  (`fit` or `loo3`) before it.

### 2.3 Enumeration order

Program length 1, then 2, then 3, then 4. Within a length, lexicographic
order over the inventory order of section 2.1 (fit < exm < loo3 < med
< avg), most significant instruction first. This order is fixed,
arbitrary, and generic: it is by program length, then by a pre-fixed
instruction order. It was fixed without reference to any target
composition.

### 2.4 Self-check (the learner's own)

A candidate program is a pure function of (y0, y1, y2, x*). It passes
the self-check iff its prediction equals the observed consequence y*
exactly, on EVERY licensed round-1 failure case (the cases where the
learner's own LOO attribution fired; unlicensed failures are correctly
excluded from construction data, exactly as in REVISE). Inputs to the
check are learner-observable values only: training values, x*, and the
observed consequence. No case id, no flavor label, no hidden standard.

### 2.5 Adoption

The first program in enumeration order that passes the self-check is
adopted: its instruction array and length are written to persistent
learner state and an adoption flag is set. The search stops at the
first pass. If no valid program passes at length 4 or below, nothing
is adopted (flag stays 0) and the round-2 revision arm uses the frozen
procedure; the report then states the learner failed to invent, which
bounds the invention claim per the parent mandate.

Round-2 application (revision arm only): when the adoption flag is set
AND the standard training fit is imperfect (rmax > 0, same gating as
REVISE), the committed prediction p is produced by a GENERIC
interpreter running the adopted instruction array on the training
values. There is no researcher-written branch for any specific
program; the interpreter dispatches on instruction codes. The
tolerance rule is unchanged (t = rmax + 1 from the standard fit).

## 3. Not-specified declaration (auditable)

The following are researcher-specified and frozen above: the five
generic operations, the grammar, the enumeration order, the self-check
protocol, the adoption rule, the rmax > 0 application gating, and the
unchanged tolerance rule.

The following are NOT researcher-specified: no target program is named,
described, or hinted anywhere in this prereg; no expected adopted
composition is stated; the search order was not arranged to land on any
particular composition. Audit: after the runs, the adopted program's
canonical trace name (bracketed comma-joined instruction names, the
exact string emitted by the binary) must be absent from this file
(shell grep, reported with the verdict).

Disclosed tie-break: more than one composition may pass the self-check
(e.g. median-style and mean-style aggregations over the same
prediction set); the fixed enumeration order breaks such ties. This is
a researcher-fixed arbitration, stated here before results.

## 4. Frozen case sets

Round 1: the frozen C337 24-case set, identical to REVISE round 1
(8 AFFINE, 4 QUAD, 8 SHIFT, 2 WOBBLE-G, 2 WOBBLE-B; single-point
corruption at x = 1 for WOBBLE-B). Tables copied verbatim from
`hcontlife5/src/revise.zag` (case_y0, case_y1, case_y2, case_xstar,
world_y); the copy is verified by diff at build time.

Round 2: the 24 fresh frozen cases of PREREG-REVISE.md section 3
(same 5 flavors, new parameters). Tables copied verbatim
(c2_y0, c2_y1, c2_y2, c2_xstar, world_y2); verified by diff.

Exploratory transfer probe (NOT under any kill bar): two new
corruption-locus cases, single-point corruption at x = 0 (a locus the
learner never saw in round 1):

- X0a: true rule 3x, x = 0 point off by +1: train (1, 3, 6), x* = 4,
  y* = 12. Hand analysis: frozen fit predicts 9 (err 3, rmax 1, t 2).
- X0b: true rule 3x + 2, x = 0 point off by +2: train (4, 5, 8),
  x* = 4, y* = 14. Hand analysis: frozen fit predicts 8 (err 6,
  rmax 2, t 3).

Reported for each: invented-procedure err, frozen-procedure err, and a
harness-only reference err (the REVISE median-of-LOO computation,
quarantined in the harness, never callable by learner code). No bar;
this bounds the transfer claim honestly.

## 5. Protocol: two rounds, seven phases, epoch barrier

Identical to REVISE except P4:

- R1-P1 COMMIT (epoch 1): both arms commit (p, t, rmax) on all 24
  round-1 cases with the frozen procedure.
- R1-P2 WORLD (epoch 2): world reveals y* (both arms).
- R1-P3 JUDGE (epoch 3): both arms compute self from sealed (p, t)
  plus observed y*.
- R1-P4 REVISE (epoch 4, revision arm only): for each case with
  self = 0, run the learner-owned LOO attribution (TRG/LIC stamping,
  same as REVISE, but it does NOT set any researcher-specified
  procedure flag); licensed cases are appended to a learner-owned
  buffer. Then the invention search (section 2) runs once over all
  licensed cases, emitting the full white-box trace; on success it
  writes the adopted program and sets the adoption flag in learner
  state. The control arm has no P4.
- R2-P5 COMMIT (epoch 5): both arms commit on the 24 fresh cases.
  Revision arm uses the generic interpreter on the adopted program
  when the flag is set and rmax > 0, else the frozen fit. Control arm
  uses the frozen fit.
- R2-P6 WORLD (epoch 6): world reveals fresh y*.
- R2-P7 JUDGE (epoch 7): both arms compute self.

The exploratory X0a/X0b cases are committed (both procedures plus the
harness reference) and judged after R2-P7; they take no part in any
bar.

## 6. Frozen predictions

- F1 (invention trace): the binary emits a complete white-box trace of
  the search: every valid candidate tried in enumeration order with
  its self-check outcome, then the adopted program (or an explicit
  no-adoption marker). At least one candidate is rejected before any
  adoption.
- F2 (fresh-case performance): on round-2 WOBBLE-B cases, the invented
  procedure's total |err| is below the no-revision control's; it is
  predicted to match the researcher-specified reference performance
  recorded in REVISE (total |err| 0 on that class).
- F3 (ablation): with the invented procedure disabled (frozen fit
  substituted on the revision arm's round-2 cases), the WOBBLE-B total
  |err| returns to the control-arm level.
- F4 (no harm): round-2 agreement stays at ceiling in both arms and
  all 12 genuinely bad round-2 commitments are still rejected.

## 7. Frozen kill bars I0..I8

- I0 TEMPORAL ORDER: per-case records show strict epoch order:
  revision arm round 1: 1 < 2 < 3 < 4; control round 1: 1 < 2 < 3;
  both arms round 2: 5 < 6 < 7. Checked in program. FAIL on any
  violation.
- I1 TRIGGER AND LICENSE: revision-arm TRG count == 14 with per-case
  TRG == (SELF == 0); control-arm TRG == 0 on all cases; LIC count
  == 2 (the WOBBLE-B cases only). Checked in program (reproduces
  REVISE R1/R2). FAIL otherwise.
- I2 INVENTION TRACE: the trace lists at least 2 valid candidates
  tried; at least 1 candidate was rejected before the adopted program;
  the adopted program passes the self-check on all licensed cases
  (re-verified in program from the trace data); the adoption flag is
  set and the program bytes reside in learner state written only by
  the search. Shell audits: (a) the adopted program's canonical trace
  name is absent from this prereg; (b) learner functions never
  reference world_y, world_y2, hidden values, the hidden standard,
  case ids, or the harness-only reference procedure (K2/K6 style
  grep). FAIL otherwise.
- I3 ROUND-2 AGREEMENT: revision-arm agreement on the fresh 24 >=
  14/24. FAIL below.
- I4 NO HARM VS CONTROL: revision-arm round-2 agreement >=
  control-arm round-2 agreement. FAIL if strictly below.
- I5 STILL REJECTS BAD: on the 12 round-2 genuinely bad commitments
  (hidden = 0: 4 QUAD + 8 SHIFT), revision-arm self = 0 on all 12.
  FAIL below 12/12.
- I6 DETERMINISM: 3/3 runs byte identical (sha256 of full stdout).
  FAIL on any divergence.
- I7 INVENTED GAIN: round-2 WOBBLE-B class total |err|, revision arm
  < control arm. (Frozen prediction F2: revision arm equals the
  REVISE reference level of 0; reported alongside.) FAIL otherwise.
- I8 ABLATION: revision-arm round-2 WOBBLE-B total |err| with the
  invented procedure disabled (frozen fit) equals the control-arm
  total |err|. Checked in program. FAIL otherwise.

Verdict rule: INVENTION-PASS iff I0..I8 all pass. Any single FAIL gives
INVENTION-FAIL with the failing bar named. If the search adopts
nothing, the report states the learner failed to invent (I2 FAIL if no
trace/adoption, I7 expected FAIL) and the claim is bounded, not
salvaged. VOID is terminal (prereg violation: e.g. implementation
committed before this prereg, or a bar weakened after results).

## 8. Information flow architecture

Single pure Zag binary, three roles separated by function boundaries:

- LEARNER: learner_commit, learner_judge, learner_attrib (LOO
  license; writes TRG/LIC and appends licensed cases to the
  learner-owned buffer; sets no procedure flag), learner_invent (the
  section-2 search; the ONLY writer of the adoption flag and program
  bytes), learner_interp (generic instruction interpreter),
  learner_commit2 (round-2 commit through the interpreter),
  loo_pred, exm_of, med_of, avg_of. Values only, never a case id,
  never calls world_y / world_y2.
- WORLD: world_y (round 1), world_y2 (round 2), x_world
  (exploratory), called only from the P2/P6/exploratory paths in main.
- HARNESS: agreement counting, bar checks, ablation recomputation,
  exploratory reporting, and the quarantined reference procedure
  (median of LOO, for the exploratory comparison only). Reads sealed
  records only, never writes learner state.

Round-1 and round-2 case tables are readable by main for P1/P5 input
assembly. Audits enforce the boundaries.

## 9. Determinism and build plan

Pure Zag, pinned compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1.
No randomness, no clocks, no environment reads. Output via one
preallocated buffer and a single raw syscall flush (established emit
idiom). Build from the lane dir:
`znc src/invent.zag -o bin/invent`. Run three times, sha256 each
stdout, require identical. Table copies verified by diff against
`hcontlife5/src/revise.zag` before the first build. All scientific
computation in Zag; shell only for znc invocation, runs, sha256sum,
greps, git.

## 10. Honest limitations (pre-registered)

- The claim sought is L2 structural learning, not L3. The operation
  inventory, grammar, enumeration order, and self-check protocol are
  researcher-specified; what is learner-determined is the specific
  adopted composition, found by search against the learner's own
  failure data.
- The fixed enumeration order arbitrates ties between passing
  compositions (disclosed in section 3); the order itself is a
  researcher-fixed choice.
- The construction space is small (5 instructions, length at most 4);
  the correctable class is single-point training corruption at one
  locus. The exploratory X0a/X0b probe (no bar) tests whether the
  invented procedure transfers to a new locus; a failure there bounds
  the claim honestly.
- The `loo3` primitive bundles the three single-exclusion
  predictions; the inventive step is their composition with
  aggregation and the adoption protocol, verified by the rejection
  trace, the fresh-case bars, and the ablation.
- Consequences are exact (no noise). Case sets are small (24 + 24,
  plus 2 exploratory).
- If the learner fails to invent, the report says so plainly per the
  verdict rule; no salvage, no amended re-freeze in this wave.
