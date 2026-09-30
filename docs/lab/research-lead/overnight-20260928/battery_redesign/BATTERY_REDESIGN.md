# Battery v2 Redesign: Restoring Conditional Discrimination After D's MOD Finding

Status: DESIGN DOCUMENT. Not a preregistration. It specifies Battery v2
precisely enough that the frozen prereg can be cut from it with minimal
editing. No implementation or evaluation is authorized by this document.

Date: 2026-09-30.
Trigger: Hypothesis D result `e2ee0964e` (D-TESTED; BUILD-FAIL on K4 purity,
mechanism finding stands).

## 1. What happened (K1 input)

Battery v1 prereg `425f7276d` froze the discrimination matrix on the theory
that abs-like tasks require conditional machinery:

- v1 prediction: T1 abs -> A FAIL, B SOLVE, C SOLVE, D FAIL.
- Review `18be93c3e`: "abs: FAIL. The control has no conditional machinery
  and the P1 op alphabet has no comparison; this matches the straight line
  limit and isolates the discovery question."

D falsified this. D discovered `[IN0 PUSH:-2 IN0 MUL MOD NEG NEG]`, a 7-op
straight-line program computing |x| exactly (17/17 train, 8/8 hidden).
Mechanism: `mod_nonneg(x, -2x)` under the frozen VM semantics
(`genexec2.zag` in `8d5f58b89`):

```
fn mod_nonneg(a:i32, b:i32)i32 {
  let r:i32=a - (a/b)*b;
  if(r<0){ r=r+b; }
  return r;
}
```

- x>0: x/(-2x) = -0.5 truncates to 0, r = x. Result x = |x|.
- x<0: x/(-2x) = -0.5 truncates to 0, r = x < 0, then r += -2x giving -x = |x|.
- x=0: divisor is 0, VM yields 0 = |0|.

The v1 prereg anticipated exactly this event. Falsifier A-F3: "A solves T1
straight line. Investigate before any claim: either the op alphabet secretly
expresses abs without comparison (VM or task flaw) or conditional machinery
was smuggled in." The investigation is now complete: the FIRST disjunct is
confirmed. The op alphabet secretly expresses abs without a dedicated
comparison op. Likewise the review's D-F2 logic ("Either the tasks are
straight line solvable after all (a task design flaw, to be checked by
inspecting the found program)... Invalidate and fix") applies to T1 even
though D-F2 as written only covered T4/T5.

## 2. K1: Compromise analysis

| Task | v1 intent | Status v2 | Evidence |
|------|-----------|-----------|----------|
| T0 2x+1 | basic arithmetic discovery (straight-line OK) | NOT COMPROMISED | intent never required conditionals |
| T1 abs | conditional-structure discriminator | COMPROMISED | D exhibited 7-op straight-line program, 17/17 train, 8/8 hidden (`e2ee0964e`) |
| T2 x mod 3 | MOD discovery (straight-line OK) | NOT COMPROMISED | intent never required conditionals |
| T3 parity(a,b) | two-input basic, all predicted SOLVE | NOT COMPROMISED by the MOD trick; separate MEMORIZATION LOOPHOLE | C's "apparent solve" used 24 splits and a 133-op memorization program (`aae06bac6`), not the predicted repair mechanism |
| T4 \|\|x\|-2\| | nested conditional discriminator | COMPROMISED | composition: \|x\| straight-line in 7 ops implies \|\|x\|-2\| straight-line in ~13 ops (mod_nonneg(u-2,-2(u-2)) after u=\|x\|). D failed to find it in 1M evals, but the task no longer discriminates conditional machinery |
| T5 \|x\|+\|x-2\| | fragment-composition discriminator | COMPROMISED | same composition argument, ~14 ops straight-line on the full VM |
| T6 sealed | adversary capstone | NOT YET DESIGNED; gate updated (sec 4.8) | -- |

Root cause. The review equated "no comparison ops" with "the straight line
limit". That equation is false. Three members of the shortcut class, all
straight-line on the frozen full VM:

1. MOD sign extraction (EXHIBITED by D): `[IN0 PUSH:-2 IN0 MUL MOD NEG NEG]`,
   7 ops (5 without the dead NEG NEG). Computes mod_nonneg(x,-2x) = |x|.
2. DIV step multiplexing (constructed): with x in -8..8,
   s = (x+9) DIV 9 is 0 iff x<0, else 1 (truncated division; divisor
   nonzero). Then |x| = x*(2s-1):
   `[IN0 DUP PUSH:9 ADD PUSH:9 DIV PUSH:2 MUL PUSH:1 SUB MUL]`, 11 ops.
3. Comparison multiplexing (constructed): LT pops b,a and pushes 1 iff a<b
   (frozen semantics, `genexec2.zag` lines 161-162). s = [x<0] via
   `[IN0 DUP PUSH:0 LT]`, then |x| = x*(1-2s):
   `[IN0 DUP PUSH:0 LT PUSH:2 MUL PUSH:1 SWAP SUB MUL]`, 10 ops.

MOD-with-truncated-division, DIV steps, and comparison multiplexing are all
comparisons in disguise. Any one of them collapses the conditional tasks to
straight-line arithmetic. The battery cannot measure conditional-structure
discovery while all three are available to solution programs.

## 3. K2: Redesign

### 3.1 GENEXEC2-P: the polynomial VM

For the conditional tasks (T1, T4, T5 in v2), solution programs run on
GENEXEC2-P: the frozen GENEXEC2 with `{DIV, MOD, LT, EQ, GT}` removed.

Kept: `PUSH(c)` c in -9..9, `IN0`, `IN1`, `ADD`, `SUB`, `MUL`, `NEG`,
`DUP`, `DROP`, `SWAP`, `OVER`, `JZ(k)`, `JNZ(k)`, `JMP(k)`, `CALL(f)`,
`RET`. All kept ops have exactly their frozen `8d5f58b89` semantics.

Per-op removal rationale:

- MOD: exhibited shortcut (7 ops, D). Must go.
- DIV: step-multiplexing shortcut (11 ops, sec 2 item 2). Must go; removing
  MOD alone is insufficient.
- LT, EQ, GT: comparison-to-0/1 multiplexing (10 ops, sec 2 item 3). Must go.

Per-op retention rationale:

- JZ, JNZ, JMP: genuine branching. A jump-based program IS conditional
  structure, which is the construct under measurement. No current hypothesis
  (A, B, C, C2, D) emits jumps, so predictions stand, and the door stays open
  for a future jump-discovering mechanism. Finite JZ decision chains remain
  expressible (sec 5, exhibit 4).
- CALL, RET: fragment composition, needed for the T5 B-route and for C0-D
  flavor. Called fragments on P-VM tasks must themselves be P-VM-valid
  (audit rule F-SMUG, sec 3.6).

### 3.2 Separation argument

FROZEN TEXT (proposed): "A jump-free GENEXEC2-P program computes a
polynomial in its inputs with integer coefficients."

Lemma 1. By induction on program structure: PUSH k is constant; IN0/IN1 are
variables; ADD, SUB, MUL, NEG preserve polynomiality; DUP, DROP, SWAP, OVER
only route values.

Lemma 2. No polynomial p satisfies p(x) = |x| for all x in {-8,...,8} with
deg(p) <= 8. Proof: q(x) = p(x) - x vanishes at 0,...,8 (9 points), so q is
identically 0, so p(x) = x everywhere, but p(-1) = -1 != 1 = |-1|.
Contradiction. Hence any jump-free P-VM program fitting the T1' train set
(17 points) has degree >= 9, i.e. at least 4 MUL ops (degree at most doubles
per MUL), plus scaffolding: in practice a ~15-op interpolant that oscillates
wildly on held-out episodes (reported separately; Runge-type behavior).

What this buys: the REALISTIC threat model, short arithmetic tricks (MOD 7
ops exhibited; DIV 11; LT 10), is removed by ablation. What remains for
straight-line routes are high-degree interpolants: long, undiscoverable by
the mechanisms within budget in practice, catastrophic on held-out, and
caught by the op cap (sec 3.4) and the mechanism-trace confirmation rule
(sec 3.5). The assumption is fenced by kill-switch falsifier F-TRICK
(sec 3.6): if a short straight-line P-VM solution is ever exhibited, the
affected task is voided, not patched quietly.

Assumptions (frozen): train inputs are bounded as specified; intermediate
values stay within i32 range on the exhibited solution class (no wraparound
exploitation); stack discipline is exactly the frozen interpreter's.

T4/T5 inherit non-polynomiality by the same technique (kinks at -2,0,2 and
0,2 respectively; finite-point interpolation lower bounds apply; a
polynomial matching ||x|-2| on -6..6 needs degree >= 5 by the outer-region
argument, and matching |x|+|x-2| on -4..8 needs degree >= 9 by the Lemma 2
argument on the x<=0 piece).

### 3.3 Probe policy (split classifiers)

C/C2's SPLIT operator partitions episodes with probe programs. v1's
mandatory trace even names the probe `[IN0, PUSH 0, LT]`, which uses an
ablated op. Resolution, FROZEN TEXT (proposed): "Split probes are meta-level
partition classifiers and run on the full GENEXEC2. Region bodies, the main
program, and every CALLed fragment on a P-VM task must be GENEXEC2-P-valid;
this is audited (F-SMUG). A probe may not leak ablated ops into solution
semantics: the region bodies are the solution."

Rationale: the battery measures whether the mechanism discovers case
structure in its SOLUTIONS. The split machinery's internal classifiers are
harness-level tooling, like the repair operator itself. The discrimination
holds because no P-VM region body can harbor the shortcut class.

### 3.4 v2 task specs

FROZEN TEXT (proposed):

| Task | Target | Train episodes | Held-out episodes | VM | Intent |
|------|--------|----------------|-------------------|----|--------|
| T0 | 2x+1 | x in 0..8 (9) | x in -8..-1, 9..16 (16) | full | basic arithmetic discovery |
| T1 | abs(x) | x in -8..8 (17) | x in -12..12 excl -8..8 (8) | P | conditional discovery (kink) |
| T2 | x mod 3 | x in 0..16 (17) | x in 17..33 (17) | full | MOD discovery |
| T3 | 1 if (a+b) even else 0 | a,b in 0..4 (25) | a,b in 0..7 excl 0..4 square (39) | full | two-input basic |
| T4 | \|\|x\|-2\| | x in -6..6 (13) | x in -10..10 excl -6..6 (8) | P | nested conditional (kinks -2,0,2; 4 linear pieces) |
| T5 | \|x\|+\|x-2\| | x in -4..8 (13) | x in -8..12 excl -4..8 (8) | P | fragment composition of conditionals (kinks 0,2; 3 linear pieces) |
| T6 | sealed adversary | per sealed spec (>=9 train) | per sealed spec (>=8, disjoint) | per sealed spec | capstone |

Canonical names stay T0..T6 under the "Battery v2" version. Episodes are
unchanged from v1; only the VM column and the SOLVE definition change.

### 3.5 v2-SOLVE and the anti-memorization bar

FROZEN TEXT (proposed): "v2-SOLVE is defined as exact integer equality of
top of stack with the target on ALL train episodes AND total program ops
(main program plus all called fragment bodies) <= 40."

Rationale: v1 had no complexity bar, so C's T3 "apparent solve" (24 splits,
133 ops, `aae06bac6`) passed the I/O check without the predicted mechanism.
The 40-op envelope matches T6's V3 adequacy bound, so the whole battery
shares one envelope. Every legitimate exhibited solution is under 20 ops;
the JZ decision-chain route (sec 5, exhibit 4) fits under 40; C's 133-op
memorization does not. Partial credit (exact train count) is still reported
but does not count as SOLVE. Hidden accuracy is reported separately, as in
v1.

### 3.6 Confirmation rule and falsifiers

The v1 confirmation rule is carried over verbatim in structure: a prediction
is CONFIRMED iff (a) the observed outcome matches under v2-SOLVE and (b) the
committed construction trace shows the predicted mechanism via the mandatory
events below, verified by independent inspection. Outcome match without
mechanism trace is UNCONFIRMED: it neither confirms nor falsifies.

Updated mandatory trace events (v2):

- C/C2 on T1: split event on a sign-separating probe (probe program logged;
  probe runs on full GENEXEC2 per sec 3.3), each branch repaired; final
  program has 2 regions and 0 CALLs.
- C/C2 on T4: at least 2 nested split events with probes and partitions;
  final program has 0 CALLs. This remains the KEY DISCRIMINATOR against B:
  B shows CALLs plus retrieval, C/C2 show splits and zero CALLs.
- C/C2 on T5: split events tracking the 0/2 kink structure; 0 CALLs.
- C/C2 on T0/T2/T3: repair events only, no splits, ops <= 40.
- B on T4/T5 (only if B amends its row per sec 4): at least 2 retrieval
  events for the ABS fragment with behavioral match recorded before each
  CALL, and at least 2 CALLs to the same fragment id; the fragment must be
  P-VM-valid.
- D on T1/T4/T5: predicted FAIL. Any v2-SOLVE fires F-TRICK.

Falsifiers:

- A-F3: RESOLVED and CLOSED. The investigation it demanded is complete: the
  first disjunct (VM/task flaw) is confirmed. A itself remains falsified via
  A-F1 under v1; A is not re-evaluated under v2.
- D-F2: SUPERSEDED by F-TRICK (v2), which generalizes its logic to all P-VM
  conditional tasks and all hypotheses.
- F-TRICK (v2, NEW, kill switch): any hypothesis exhibits a jump-free
  GENEXEC2-P program achieving v2-SOLVE on T1/T4/T5 with ops <= 40. Then the
  sec-3.2 separation assumption is violated: the affected task is VOID
  pending re-investigation, the exhibiting program is preserved as evidence,
  and no quiet patch is permitted.
- F-SMUG (v2, NEW): a P-VM task's final program (main plus all called
  fragment bodies) contains DIV, MOD, LT, EQ, or GT. The result is void:
  full-VM power was smuggled through the persistent fragment library or a
  region body. (The library is carried across tasks per v1 sec 2, so this
  audit is load-bearing for T4/T5.)
- F-MEM (v2, NEW): restates the op cap as a falsifier for clarity; a
  memorization-style solve over the cap is not SOLVE.
- B-F1, B-F2, B-F3, C-F1, C-F2, C-F3, C-F4, D-F1: carried over unchanged.
  C-F2 keeps its role as the B-vs-C mechanism discriminator on T4.
- Review-level (updated): if every hypothesis evaluated under v2 FAILs every
  v2 task within the frozen budget, the review's "discovery is the defect,
  not the VM" assessment is overturned and a VM-level review replaces
  further discovery work.

No L3 claim follows from battery success alone (carried over). After a
CONFIRMED battery, the mandatory Criterion 0 sequence applies: source audit,
persistence, reuse, transfer, revision, adversarial unseen structure.

### 3.7 T6 re-gating

v1: "T6 must not launch until A-D implementations are all frozen in
ancestry." Status: A frozen (`21d838921`, falsified), C frozen (`aae06bac6`,
falsified), D frozen (`e2ee0964e`, K4-dirty rerun pending), B implementing
(not frozen).

v2 gate, FROZEN TEXT (proposed): "T6 evaluation launches only after ALL of:
(i) freeze commits of every hypothesis evaluated under v2 (B, C2, and D's
K4-clean rerun commit) are in ancestry; (ii) the Battery v2 prereg is frozen;
(iii) the sealed T6 spec commit strictly follows (i) and (ii). A and C are
falsified under v1 and do not gate T6."

The v1 seal protocol S1-S4 and validity constraints V1-V5 are carried over;
V2 (exhibited target contains JZ/JNZ/JMP/CALL; materially different from
T0..T5) is re-affirmed. The sealed spec states which VM variant T6 targets.

### 3.8 Transition plan

1. v1 measurements stand as committed. Interpretations of v1-T1/T4/T5 as
   conditional discriminators are SUPERSEDED (measurements are not
   retracted). v1-T0/T2/T3 interpretations stand.
2. D's MOD program is reclassified from "T1 solve" to "exhibited arithmetic
   shortcut": a genuine novel discovery (a 7-op sign-extraction identity the
   programmers did not supply), preserved as evidence, no longer counted as
   conditional-structure discovery.
3. C2 (implementing against v1 tasks): its prereg MUST be transparently
   amended to v2 tasks before any v2 evaluation run. Amendment precedes runs;
   no v1-targeted C2 evaluation counts toward v2.
4. D: a K4-clean rerun (zero Python at every stage) on v2 tasks is required
   before D's v2 results are adopted. The rerun does not change D's
   mechanism.
5. B (implementing): preregisters against v2. B may amend its matrix row
   (sec 4) iff its frozen prereg specifies a case-capable base constructor;
   the amendment strictly precedes any v2 evaluation run.
6. GENEXEC2-P: implement as a build variant of the frozen interpreter, with
   a conformance test (ablated opcodes rejected; T0's 2x+1 still runs; D's
   MOD program fails on P-VM), committed and hash-recorded before any v2
   evaluation. This is a separate build task, not part of this design.
7. Budget (1M evals or 300 s per hypothesis-task), determinism (3 runs,
   byte-identical), and the 12 v1 metrics are carried over; add metric 13
   (VM variant) and metric 14 (jump count and split-region count in the
   final program).

## 4. K3: Discrimination matrix v2

FROZEN TEXT (proposed):

```
Task        | B fragments | C2 cex+lookahead | D MAP-Elites
T0 2x+1     | SOLVE       | SOLVE            | SOLVE
T1 abs (P)  | FAIL *      | SOLVE            | FAIL
T2 mod 3    | SOLVE       | SOLVE            | SOLVE
T3 parity   | SOLVE       | SOLVE            | SOLVE **
T4 nabs (P) | FAIL *      | SOLVE            | FAIL
T5 fcomp(P) | FAIL *      | SOLVE            | FAIL
T6 sealed   | conditional | conditional      | conditional
```

A and C were falsified under v1 (A-F1, C-F1) and are not re-evaluated; their
rows are omitted.

- `*` B conditional: B's base constructor as currently understood has no
  case machinery, so B cannot produce the ABS fragment on the P-VM and
  cannot compose it on T4/T5. B's frozen prereg may amend this row
  transparently (SOLVE with the sec-3.6 trace events) iff it specifies a
  case-capable base constructor; the amendment strictly precedes any v2
  evaluation run. An unamended B SOLVE on a P-VM conditional task fires an
  audit for smuggled machinery (F-SMUG/F-TRICK decide which).
- `**` D on T3: v1 observed FAIL (20/32 at 1M evals, `e2ee0964e`) against a
  SOLVE prediction. Theory still predicts SOLVE (7-op straight-line
  solution exists; D found <=11-op solutions on T0/T1/T2). The v1 miss is a
  standing anomaly for D's search adequacy on two-input parity chains; a
  second FAIL on v2-T3 triggers a D-search review instead of a third run.

Cell rationales:

- T1 (P): C2 splits x<0/x>=0 (probe on full VM), repairs each linear piece:
  SOLVE. D is straight-line-only on a polynomial VM: FAIL (Lemma 2). B has
  no case-capable base: FAIL (*).
- T4 (P): C2 nested splits at -2, 0, 2 (4 linear pieces, 0 CALLs): SOLVE.
  D: FAIL. B: FAIL (*), and this is the KEY DISCRIMINATOR cell: if B ever
  solves T4, its trace must show CALLs plus retrieval (B-F1/B-F2 enforced),
  never splits (C-F2 enforced).
- T5 (P): C2 splits at 0, 2 (3 pieces, 0 CALLs): SOLVE. D: FAIL. B: FAIL
  (*); the amended B route would be 2+ CALLs to a P-VM-valid ABS fragment.
- T0/T2/T3: unchanged intents on the full VM; all predicted SOLVE (T3 now
  guarded by the 40-op cap against C-style memorization).

## 5. Exhibits

Exhibit 1 (MOD sign extraction, exhibited by D, `e2ee0964e`):
`[IN0 PUSH:-2 IN0 MUL MOD NEG NEG]`, 7 ops. Stack trace for x=-5:
[ -5 ] -> PUSH -2 -> [ -5, -2 ] -> IN0 -> [ -5, -2, -5 ] -> MUL ->
[ -5, 10 ] -> MOD: mod_nonneg(-5,10): r = -5 - trunc(-0.5)*10 = -5; r<0 so
r += 10 -> 5 -> [ -5, 5 ] -> NEG NEG -> [ -5, 5 ]. Top = 5 = |-5|. The two
NEGs are dead identity. For x=5: MOD: r = 5 - trunc(-0.5)*(-10) = 5 -> top 5.

Exhibit 2 (DIV step multiplexing, constructed): x in -8..8,
`[IN0 DUP PUSH:9 ADD PUSH:9 DIV PUSH:2 MUL PUSH:1 SUB MUL]`, 11 ops.
s = (x+9) DIV 9 is 0 iff x<0 (x=-8 -> 1/9=0; x=-1 -> 8/9=0; x=0 -> 9/9=1;
x=8 -> 17/9=1, truncated). Result x*(2s-1) = |x|.

Exhibit 3 (comparison multiplexing, constructed):
`[IN0 DUP PUSH:0 LT PUSH:2 MUL PUSH:1 SWAP SUB MUL]`, 10 ops. LT pushes 1
iff second-from-top < top, so s = [x<0]; result x*(1-2s) = |x|.

Exhibit 4 (genuine branching route that SURVIVES on the P-VM, sketch): a
finite JZ decision chain distinguishing x+8, x+7, ..., x+1 (JZ pops its test
value and jumps absolute on zero, per frozen semantics), one NEG per
negative value, ~4 ops per value, <= 32 ops total, within the 40-op cap.
No current hypothesis emits jumps, so this route is open territory: a
mechanism discovering it would exhibit genuine conditional discovery, which
is exactly the construct under measurement. (Stack-discipline details per
the frozen interpreter; sketch only, not a verified program.)

## 6. From design to frozen prereg (checklist)

- [ ] Cut PREREG_BATTERY_V2.md from sections 3.4, 3.5, 3.6, 3.7 and the
  matrix in section 4, verbatim where marked FROZEN TEXT.
- [ ] Commit the prereg alone; verify it strictly precedes any v2
  implementation or evaluation commit (git merge-base --is-ancestor).
- [ ] Build GENEXEC2-P with its conformance test; commit and hash-record.
- [ ] Redirect C2's prereg (transparent amendment) to v2 tasks.
- [ ] Schedule D's K4-clean rerun on v2 tasks.
- [ ] Require B's prereg against v2 (with the sec-4 `*` amendment option).
- [ ] Byte-grep the prereg for non-ASCII (no em/en dashes); pure-Zag
  conformance for all downstream work.
- [ ] Do not launch T6 until the sec-3.7 gate is satisfied.

## 7. Honest limitations

1. The separation argument is practical, not absolute: high-degree
   polynomial interpolants are not mathematically impossible, only long,
   undiscoverable-in-practice, and held-out-fragile. F-TRICK is the
   load-bearing fence, not the lemma.
2. Fixed-width integer behavior is assumed unexploited; a wraparound-based
   shortcut would fire F-TRICK rather than being silently absorbed.
3. B's matrix row is conditional by necessity (B unfrozen). If B's prereg
   lands with a case-capable base, the `*` amendment path handles it; if B
   never specifies one, the FAIL predictions stand as the sharp test.
4. C2 is mid-implementation against v1 tasks; the sec-3.8 redirect is a
   real cost (rework), accepted because v1's T1/T4/T5 no longer measure
   what C2 was built to demonstrate.
5. T3's v2 prediction for D carries a known anomaly (v1 FAIL). The matrix
   does not hide it.
6. This design changes no v1 verdict: A and C stay falsified, D's
   measurements stand, D's MOD program is preserved as a discovery. v2 is
   an amendment that ADDS constraints (VM restriction, op cap); it weakens
   no frozen bar and rescues no hypothesis.

## 8. Kill-bar check

- K1 (compromised tasks identified): section 2. T1/T4/T5 COMPROMISED with
  exhibited or constructed programs; T0/T2/T3 not compromised (T3 gets a
  bar fix for the memorization loophole).
- K2 (redesign specified): sections 3.1-3.8. GENEXEC2-P, separation
  argument, probe policy, task specs, v2-SOLVE, confirmation rule,
  falsifiers, T6 re-gating, transition plan.
- K3 (new matrix defined): section 4, frozen text proposed, per-cell
  rationales, B conditional and D anomaly disclosed.

Builder label: DESIGN-COMPLETE.
