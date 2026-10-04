# REPORT-INVENT: H-CONTLIFE-5 follow-up -- Learner-Invented Revision Procedure

Worker: H-CONTLIFE-5-INVENT (subagent, 2026-10-02). Replacement for a
completed worker (H-CONTLIFE-5-REVISE).
Prereg: `hcontlife5-invent/PREREG-INVENT.md`, frozen and committed alone
at 616298c87 before any implementation existed. Implementation:
`src/invent.zag` (pure Zag), built with the pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` to `bin/invent`.
Toolchain guard: Step 0 safebin active whole session (NAMECHECK.md);
`which python3` and `which python` returned nothing; no forbidden
executable invoked. The frozen `hcontlife5/` lane was read but never
modified; its round-1 and round-2 case tables were copied verbatim
(all 12 table functions diff-identical, verified at build).

## What was built

One pure-Zag binary implementing the preregistered invention loop. All
of REVISE is held fixed (trigger, attribution, adoption gating, both
frozen case sets, control arm) except the procedure source: in P4 the
learner runs an invention search instead of adopting a
researcher-specified procedure.

- The construction space (prereg section 2): five generic instructions
  (`fit`, `exm`, `loo3`, `med`, `avg`), programs of 1 to 4
  instructions, validity rules V1/V2, enumeration by length then
  lexicographic instruction order, and a self-check (exact prediction
  of every licensed observed consequence). The prereg names no target
  program (audited: the adopted program's canonical name is absent
  from PREREG-INVENT.md).
- P4 (epoch 4, revision arm only): per-case LOO attribution stamps
  TRG/LIC exactly as in REVISE (no procedure flag is set); licensed
  cases accumulate in a learner-owned buffer; then `learner_invent`
  enumerates candidate programs, emits the full white-box trace, and
  writes the first self-check passer as an instruction array plus an
  adoption flag into learner state. The search stops at the first
  pass; the trace records every candidate tried.
- Round 2 (revision arm): when the flag is set and rmax > 0, the
  committed prediction comes from `learner_interp`, a GENERIC
  instruction interpreter running the adopted array. No
  researcher-written branch for any specific program exists; the
  interpreter dispatches on instruction codes.

## Results (3/3 runs byte-identical, sha256 def24c9547ab8e2b4ea2bae3799f02e4a3924271ff0964fb33ee201d20d26b90)

Round 1: both arms 24/24 agreement (reproduces C337/REVISE). Trigger on
all 14 self-judged failures, license on exactly the 2 WOBBLE-B cases
(cid 22, 23); QUAD and SHIFT correctly unlicensed.

The invention trace (white box, from the run output):

```
INVSEARCH nlic=2
INVTRY prog=[fit] ok=0
INVTRY prog=[fit,fit] ok=0
INVTRY prog=[fit,med] ok=0
INVTRY prog=[fit,avg] ok=0
INVTRY prog=[exm,fit] ok=0
INVTRY prog=[loo3,fit] ok=0
INVTRY prog=[loo3,med] ok=1
INVADOPT prog=[loo3,med]
INVSTAT tried=7 adopted=1
```

The learner tried 7 valid compositions, rejected 6 on its own
self-check, and adopted `[loo3, med]`: push the three
single-exclusion predictions, take their median. This is the same
composition the researcher hand-specified in REVISE, here constructed
by the learner from generic operations against its own failure data,
with no target named in the prereg and no dedicated code branch in the
binary. Convergent invention.

Round 2, revision arm (invented procedure): 24/24 agreement.
WOBBLE-B: 2/2 self=1, predictions exact (err 0). QUAD 4/4 self=0,
SHIFT 8/8 self=0, WOBBLE-G 2/2 self=1, AFFINE 8/8 self=1.
Round 2, control arm: 24/24 agreement, WOBBLE-B err 4 per case.
Commitment quality on round-2 WOBBLE-B, total |err|: invented arm 0
vs control arm 8 (matches the REVISE reference level of 0).
Ablation (invented procedure disabled, frozen fit): WOBBLE-B total
|err| 8, equal to control.

Exploratory transfer probe, new corruption locus x = 0 (no bar):
- X0a: invented err 3, frozen err 3, harness reference err 3.
- X0b: invented err 2, frozen err 6, harness reference err 2.
The invented procedure reproduces the reference procedure's transfer
profile exactly (partial improvement on X0b, none on X0a): the
invention is locus-specific, the same limitation as the
researcher-specified procedure it converged to.

In-program bars: i0=1 i1=1 i2=1 i3=1 i4=1 i5=1 i7=1 i8=1,
"IN-PROGRAM-BARS 8/8 (I6 shell-audited)".

## Kill bar verdicts

- I0 TEMPORAL ORDER: PASS (in-program). Revision arm round 1:
  1<2<3<4; control 1<2<3; both arms round 2: 5<6<7.
- I1 TRIGGER AND LICENSE: PASS (in-program). Revision-arm TRG 14
  with per-case TRG == (SELF==0); control TRG 0; LIC 2 (WOBBLE-B
  only). Reproduces REVISE attribution.
- I2 INVENTION TRACE: PASS (in-program + shell). Trace lists 7 valid
  candidates tried, 6 rejected before adoption; the adopted program
  re-verified in program through the generic interpreter on all
  licensed cases; adoption flag set; program bytes written only by the
  search (single write site in try_candidate). Shell: the adopted
  program's canonical name is absent from PREREG-INVENT.md (grep
  count 0); learner function bodies contain no reference to world_y,
  world_y2, x_world, hidden values, the hidden standard, case ids, or
  the harness-only reference procedure; world functions are called
  only from the P2/P6/exploratory paths in main; the adoption buffer
  is written only by the search.
- I3 ROUND-2 AGREEMENT: PASS. 24/24 >= 14/24.
- I4 NO HARM VS CONTROL: PASS. 24/24 >= 24/24.
- I5 STILL REJECTS BAD: PASS (in-program). 12/12 genuinely bad
  round-2 commitments rejected.
- I6 DETERMINISM: PASS. 3/3 runs byte-identical.
- I7 INVENTED GAIN: PASS. Round-2 WOBBLE-B total |err|: 0 < 8, and
  the frozen prediction (match the REVISE reference level of 0) held.
- I8 ABLATION: PASS (in-program). Disabled-procedure WOBBLE-B total
  |err| 8 equals control-arm 8.

Verdict: INVENTION-PASS (I0..I8 all pass).

## Honest interpretation

What this shows: the learner constructed its own revision procedure.
Given only generic operations, a composition grammar, a fixed generic
enumeration order, and its own observed failures, the search rejected
6 compositions and adopted one that exactly predicts the licensed
failures, generalizes to fresh cases with new parameters (err 8 to 0
on the correctable class), and carries the full gain (ablation
restores control error). The adopted composition was not named in the
prereg, appears in the binary only as learner-state data, and is
applied through a generic interpreter. The trigger, attribution, and
adoption remain learner-owned as in REVISE; this wave adds
learner-owned construction. The claim is L2 structural learning
(constructs a new procedure from generic mechanisms), the same honest
rating as C335, and it directly answers the parent task: invention
extends to revision procedures at L2.

What this does NOT show (pre-registered limits, restated): the L3 bar
is not claimed and not met: the operation inventory, grammar,
enumeration order, and self-check protocol are researcher-specified;
only the specific adopted composition is learner-determined. The
fixed enumeration order arbitrates ties (the mean-style aggregation
over the same prediction set also passes the self-check; the order
picked the median-style one; disclosed in prereg section 3). The
`loo3` primitive bundles the three single-exclusion predictions, so
the inventive step is the composition with aggregation plus the
adoption protocol, not the discovery of leave-one-out itself. The
construction space is small (5 instructions, length at most 4) and the
correctable class is single-point corruption at one locus; the
exploratory probe shows the invented procedure does not transfer to a
new locus, exactly like the reference procedure. Consequences are
exact, case sets are small.

Notable: the learner converged on the exact procedure the researcher
had hand-specified in REVISE. That is evidence the REVISE procedure
choice was a natural attractor of the construction space under the
learner's self-check, not an arbitrary researcher imposition, and it
is evidence the learner can re-derive it without being told.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/hcontlife5-invent
~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/invent.zag -o bin/invent
./bin/invent | sha256sum   # expect def24c9547ab8e2b4ea2bae3799f02e4a3924271ff0964fb33ee201d20d26b90
```

Table fidelity: all 12 round-1/round-2 table functions diff-identical
to `hcontlife5/src/revise.zag` (function-body diff at build time).
Audits: `grep -c "loo3,med" PREREG-INVENT.md` (0); learner-section grep
for `world_y|world_y2|x_world|hidden|ref_medloo|cid` (empty);
`grep -n "set32(prog" src/invent.zag` (writes only in try_candidate
and learner_invent init); world/reference call sites only in main's
P2/P6/exploratory paths.
