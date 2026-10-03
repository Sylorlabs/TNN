# Battery v2 Preregistration (FROZEN)

Status: PREREGISTRATION FROZEN. This document is the frozen Battery v2
preregistration. It is cut verbatim from the Battery v2 design document
(commit `611e8fa1f`,
`docs/lab/research-lead/overnight-20260928/battery_redesign/BATTERY_REDESIGN.md`),
sections 3.4, 3.5, 3.6, 3.7, and the discrimination matrix in section 4.
Text marked "FROZEN TEXT (proposed)" in the design is frozen here verbatim;
the "(proposed)" qualifier is dropped because this commit is the freeze.
No implementation or evaluation is authorized by this document.

Date: 2026-09-30.
Ancestry at freeze: design `611e8fa1f` in ancestry; GENEXEC2-P prereg
`495878df4` and build plus conformance `7c34fe1d1` (BUILD-PASS, C1-C5 all
PASS) in ancestry; C2 prereg transparent amendment `9bc64e4cf` in ancestry.
Authoring: pure text edit, no Python used, byte-grep verified free of
em and en dashes.

---
### 3.4 v2 task specs

FROZEN TEXT:

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

FROZEN TEXT: "v2-SOLVE is defined as exact integer equality of
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

v2 gate, FROZEN TEXT: "T6 evaluation launches only after ALL of:
(i) freeze commits of every hypothesis evaluated under v2 (B, C2, and D's
K4-clean rerun commit) are in ancestry; (ii) the Battery v2 prereg is frozen;
(iii) the sealed T6 spec commit strictly follows (i) and (ii). A and C are
falsified under v1 and do not gate T6."

The v1 seal protocol S1-S4 and validity constraints V1-V5 are carried over;
V2 (exhibited target contains JZ/JNZ/JMP/CALL; materially different from
T0..T5) is re-affirmed. The sealed spec states which VM variant T6 targets.

---

## 4. K3: Discrimination matrix v2

FROZEN TEXT:

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


---

## 5. Prereg freeze kill-bar check

- K1 (prereg frozen): this commit freezes PREREG_BATTERY_V2.md. The freeze
  commit must strictly precede every v2 implementation or evaluation commit.
  Verify with `git merge-base --is-ancestor <prereg-commit> <later-commit>`
  before any v2 evaluation is accepted.
- K2 (checklist): GENEXEC2-P built and conformance PASS (`7c34fe1d1`); C2
  prereg transparently amended to v2 (`9bc64e4cf`, frozen before v2 code);
  D K4-clean rerun still pending: no v2 evaluation launches until D's clean
  rerun commit and B's freeze commit are in ancestry; B prereg `9e2fbd134`
  exists and the section 4 `*` amendment option remains open, but any B
  amendment must strictly precede its first v2 evaluation run.
- K3 (purity): this file is byte-grep verified free of em and en dashes; no
  Python was used in authoring; all downstream v2 work is pure Zag.

T6 remains gated by section 3.7. No L3 claim follows from battery success
alone; after a CONFIRMED battery the mandatory Criterion 0 sequence applies
(source audit, persistence, reuse, transfer, revision, adversarial unseen
structure).

Builder label: V2PREREG-COMPLETE.
