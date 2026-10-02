# VALLEY BATTERY Q1 ANALYSIS: VM Scope (GENEXEC2 vs GENEXEC2-P)

Date: 2026-09-30.
Status: ANALYSIS DRAFT. Analysis only. No implementation. No code written.
No instances generated. No evaluation authorized.
Authority: Valley Q1 analyst task; valley design `76c7a887c`; prereg
readiness draft `8d582c080` (section 4, Q1).

## 1. Question restated

The valley design specifies full GENEXEC2 (frozen VM `8d5f58b89`). The
Battery v2 redesign (`611e8fa1f`) ablated {DIV, MOD, LT, EQ, GT} for the
main battery's conditional tasks (GENEXEC2-P, prereg `495878df4`) and
redirected the C2 implementer to GENEXEC2-P. Family K's canonical path
requires DIV, MOD, and EQ. Options: (a) the valley battery stays on full
GENEXEC2, or (b) it is re-scoped to GENEXEC2-P, which requires reworking
Family K. This document analyzes Family K's op usage, assesses rework
feasibility, and recommends (a) with reasoning.

## 2. Family K's DIV/MOD/EQ usage (load bearing, every stage)

Family K (design section 3.1): episodes x in {0, ..., 2^n - 1}, target
f_K(x) = 1 iff x == K. Decoy P0 = [PUSH 0]. Canonical path: [PUSH 1],
then stages j = 0..n-1, each stage

  [IN0, PUSH 2^j, DIV, PUSH 2, MOD, PUSH k_j, EQ, MUL]

where k_j is bit j of K. (For n = 5, stage 4 synthesizes PUSH 16 as
[PUSH 8, PUSH 2, MUL]; the DIV, MOD, EQ around it are unchanged.)

Op-by-op role in each stage:

- DIV: computes truncated x / 2^j, i.e. shifts x right by j bits. Without
  DIV there is no bit-position isolation from the input.
- MOD: computes (x / 2^j) mod 2 under mod_nonneg semantics, i.e. extracts
  bit j of x. Without MOD there is no bit extraction.
- EQ: tests the extracted bit against the key bit k_j, pushing 1 on match
  and 0 on mismatch. Without EQ there is no bit comparison.
- MUL: accumulates the conjunction of bit matches across stages (seeded by
  the initial PUSH 1). Survives ablation, but has nothing to accumulate
  without the DIV/MOD/EQ front end.

The proved score profile (design section 3.2: after j stages,
score = 2^n - 2^{n-j} + 1, with stages 1..n-2 strictly below s0, stage n-1
tying, stage n solving) is a direct consequence of this stage structure:
each stage multiplies in one more bit-match indicator. Remove any of
DIV, MOD, EQ and no stage is expressible; the depth parameterization
d = 1..4 via n = 2..5 and its proof both collapse.

## 3. Family A's DIV/MOD/EQ usage

- A1 (T0 constant-trap escape): canonical path from the C2 design
  walkthrough is arithmetic only ([IN0, PUSH 1] then [IN0, ADD, ADD]
  per `e658766bd`). No DIV/MOD/EQ required. Survives ablation.
- A2 (T2 from identity): canonical path [PUSH 3, MOD] appended to
  P0 = [IN0]. MOD is the entire canonical step. On GENEXEC2-P the
  canonical path is unexpressible.
- A3 (T1 abs from const-0): canonical path targets D's discovered form
  [IN0, PUSH -2, IN0, MUL, MOD, NEG, NEG] or equivalent. MOD is load
  bearing. On GENEXEC2-P the exhibited route is gone; the only surviving
  routes are jump-based decision chains.

So a GENEXEC2-P rework would lose Family K entirely and Family A2/A3 in
their specified forms. Only A1 and CAL-0 survive unchanged.

## 4. What GENEXEC2-P removes and what remains

Frozen in `495878df4`: ablated opcodes {6:DIV, 7:MOD, 13:LT, 14:EQ,
15:GT}. Kept with frozen semantics: PUSH, IN0, IN1, ADD, SUB, MUL, NEG,
DUP, DROP, SWAP, OVER, JZ, JNZ, JMP, CALL, RET.

The v2 redesign's separation argument (section 3.2, Lemmas 1-2): a
jump-free GENEXEC2-P program computes a polynomial in its inputs. No
low-degree polynomial computes comparison-like functions, so on
GENEXEC2-P the only realistic comparison routes are jump-based decision
chains (redesign exhibit 4: finite JZ chains, ~4 ops per distinguished
value, SUB+JZ implementing equality). None of the valley participants
emits jumps in its search alphabet: C2's fix search enumerates
straight-line sequences over the 34-op non-jump alphabet (`e658766bd`,
section 3.2); the redesign states explicitly that no current hypothesis
(A, B, C, C2, D) emits jumps.

## 5. Feasibility assessment of option (b): re-scoping to GENEXEC2-P

A GENEXEC2-P valley family is definable, but Family K as designed is not
reworkable. The reasons are structural, not cosmetic:

1. Bit extraction is impossible. DIV and MOD are the only ops that
   isolate and extract bits. On GENEXEC2-P, bit tests must be done via
   SUB+JZ decision chains. A stage is then a conditional branch, not a
   linear prefix extension. The valley construct (temporarily worse
   intermediate prefixes under concatenation) is defined over linear
   prefix growth; jump-based stages change the trajectory semantics, so
   the depth proof, the score profile, and the op-level prefix acceptance
   (V1) all require a new derivation, not an edit.

2. The depth parameterization is destroyed. Family K's d = 1..4 comes
   from stagewise conjunction of n bit tests. A JZ decision chain for
   the one-key task tests x == K directly (SUB+JZ), collapsing the
   family to a single decision with no stage structure. There is no
   natural P-native parameterization giving provable depths 1..4 with
   the same comparative meaning.

3. The shortcut situation gets worse, not better. On full GENEXEC2 the
   known 5-op shortcut is disclosed and flagged NON_CANONICAL (winner
   length < canonical length - 2), with comparative inference protected
   by identical exposure. On GENEXEC2-P, the SUB+JZ equality test is
   simultaneously the canonical route and the shortcut; the flag has
   nothing to discriminate, and every short solve is jump-based by
   necessity.

4. Participant alphabets confound the construct. B, D, and C2 emit
   straight-line programs. On GENEXEC2-P, straight-line comparison is
   practically infeasible (Lemma 2: high-degree interpolants only,
   long, undiscoverable within budget, held-out fragile). A P-valley
   battery would therefore measure "can the mechanism emit jumps"
   instead of "can the mechanism cross valleys". The triggers
   (T-BUDGET/T-WALL) are supposed to discriminate search mechanisms
   over a shared construction substrate; an alphabet wall is a
   different, uninformative trigger.

5. Acceptance and calibration do not transfer. V1 (score profile),
   V3 (no shallow shortcut; the 2-op neighborhood would need
   re-derivation over jump programs), and V4 (frozen A and C1 must
   fail; established on the full VM, not portable) would all need
   re-validation. V4 in particular would need the falsified mechanisms
   re-run against reworked instances, which is new evaluation of
   frozen artifacts under a changed instrument.

6. New falsifiers would be needed. The v2 falsifiers (F-TRICK for
   jump-free P solves, F-SMUG for ablated-op smuggling) are scoped to
   the main battery's conditional tasks. A P-valley family would need
   its own void conditions for jump-based degenerate solves, a fresh
   design task.

Conclusion on (b): feasible only as a full redesign of the valley
instrument (new family, new depth proof, new acceptance procedure, new
calibration, new falsifiers). It preserves none of the design's proved
content and changes what the battery measures.

## 6. Why the v2 rationale does not transfer to the valley battery

The ablation was motivated by a specific finding: MOD/DIV/LT secretly
express comparisons in disguise (D's 7-op abs, the 11-op DIV route, the
10-op LT route), which collapsed the main battery's conditional-structure
discrimination for T1/T4/T5. That rationale is task specific:

- The valley battery does not discriminate conditional-structure
  discovery. It measures valley crossing by straight-line construction
  mechanisms. DIV/MOD/EQ in Family K are the valley-building machinery
  (bit tests), not a leak around the measured construct.
- The known shortcut is already handled: disclosed in design section 4,
  flagged per solve by NON_CANONICAL, and comparative inference across
  B/D/C2 is protected by identical VM, instances, and shortcuts.
- The v2 redesign itself keeps T0, T2, and T3 on full GENEXEC2 ("MOD
  discovery", "straight-line OK"). The program therefore treats
  DIV/MOD/EQ as legitimate straight-line machinery, not global taint.
  Family A2 is literally the T2 MOD task; the v2 matrix predicts SOLVE
  for all three mechanisms on it. Removing MOD from the valley battery
  would delete an instance the main battery deliberately retains.

## 7. Recommendation: option (a). Valley stays on full GENEXEC2.

Reasoning:

1. The design's proved content (score profile, depth parameterization,
   acceptance criteria, falsified-mechanism calibration) is built on
   full-GENEXEC2 semantics and survives intact under (a). Under (b) it
   is all discarded and must be rebuilt.
2. The ablation's rationale (conditional discrimination) does not apply
   to a valley-crossing instrument; the shortcut class it targets is
   disclosed and instrumented in the valley design.
3. The participants' search alphabets are straight-line; full GENEXEC2
   keeps the measured construct (valley crossing) separated from
   alphabet emission. GENEXEC2-P would confound them.
4. Precedent: v2 keeps straight-line tasks on full GENEXEC2; the valley
   battery is the pure straight-line valley instrument, so consistency
   favors (a), not (b).

## 8. Cost and conditions of (a)

- C2's main-battery implementation targets GENEXEC2-P (amendment
  `9bc64e4cf`). For valley participation it needs full-GENEXEC2 code:
  either a full-GENEXEC2 build of the same mechanism or a valley
  adapter. This is real but bounded extra work, and the readiness
  draft's Q2 already resolves the freeze definition: the freeze point
  is the commit freezing the code that actually runs on the valley
  battery. B and D are frozen on full GENEXEC2 already (`69730b4ab`,
  `e2ee0964e`), so no extra work falls on them.
- The information barrier (design section 12) is unaffected by the VM
  choice and is arguably simpler under (a): the valley instances are
  generated after the last mechanism code freeze among {B, D, C2},
  verified by ancestry, with no search-logic commits after the
  instance freeze.
- No v2 falsifier (F-TRICK, F-SMUG, F-MEM) applies to the valley
  battery; they are scoped to the main battery's P-VM conditional
  tasks. Valley instances are new instruments with their own
  acceptance (V1-V5) and trigger rules (sections 9-10).
- The prereg (once C2 freezes) records the VM choice explicitly:
  full GENEXEC2, frozen commit `8d5f58b89`, for all valley instances.

## 9. Kill-bar self-check

- K1 (analysis complete): Family K's DIV/MOD/EQ usage analyzed op by
  op in section 2; Family A's usage in section 3; GENEXEC2-P's kept
  and removed sets verified against frozen prereg `495878df4` in
  section 4.
- K2 (recommendation justified): recommendation (a) with four-part
  reasoning in section 7; the (b) feasibility assessment in section 5
  gives six structural reasons rework is a redesign, not an edit;
  section 6 shows the ablation rationale does not transfer.
- K3 (no implementation): no code written, no instances generated,
  no VM modified, no evaluation run. This document is analysis only.

Builder label: Q1-ANALYSIS-COMPLETE.
