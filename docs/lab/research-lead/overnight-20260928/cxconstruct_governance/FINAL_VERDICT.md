# FINAL VERDICT: H-CAUSALEXP-CONSTRUCT (Step 11, Governance Audit)

Date: 2026-09-30.
Auditor: Final Governance Auditor (step 11 of 11-step frontier promotion pipeline).
Scope: Review only. No new implementation. All findings from committed reports.

## Verdict: SURVIVES-AS-L2 (bounded). L3 construction claim KILLED.

The 7/7 BUILD-PASS stands. The mechanism is a real, working, bounded L2
systematic search with a useful disagreement filter. It is not L3. It does
not construct experiments in any learner-authored sense. Two independent
adversaries killed the construction reading on identical grounds.

## Pipeline ledger

| Step | Content | Commit | Status |
|------|---------|--------|--------|
| 1 | Preregistration | 46bdd01c5 | PASS, strict ancestor of step 2 |
| 2 | Implementation, BUILD-PASS 7/7 | 48f2adc15 | PASS |
| 3 | Sealed evaluation (Worlds A, B; 4 configs) | (in 48f2adc15) | PASS |
| 4 | Independent reproduction | G1 report 6b3dd03e8 | REPRODUCED, 3/3 byte-identical, md5 a1b01823aabaf688218de185785c2e6b |
| 5 | Simple-baseline comparison | 48e24c825 (prereg cf83b52be) | BASELINE-LOSES |
| 6 | Alternative-explanation attack (A2) | ae9121f47 (prereg 4f0811349) | 2/3 ATTACK-SUCCEEDS |
| 7 | OOD test | 4c5538a3c (prereg 96cdad502) | OOD-FAIL (0/4) |
| 8 | Ablation | 48cf64979 (prereg e54374f6e) | ABLATION-COMPLETE |
| 9 | Transfer/reuse | 486136c15 (prereg 1a3307b79) | TRANSFER-PARTIAL (3/4) |
| 10 | Independent red team (A1) | cad84f070 (prereg 33769a378) | 3/3 ATTACK-SUCCEEDS |
| 11 | Governance audit | this file | COMPLETE |

## Governance verification (independent, this audit)

1. Prereg lineage: all five prereg/result pairs verified via
   git merge-base --is-ancestor. 46bdd01c5 -> 48f2adc15,
   cf83b52be -> 48e24c825, 4f0811349 -> ae9121f47,
   33769a378 -> cad84f070, e54374f6e -> 48cf64979. ALL PASS.
2. Pure-Zag: no .py files added in any wave commit; no python
   invocations in any committed .zag/.sh (matches are only "No Python"
   declaration comments). PASS.
3. Em-dash audit: zero em-dash bytes in all wave .md/.txt. PASS.
4. Reproduction: G1 independently extracted cxconstruct.zag from
   48f2adc15, built with znc, 3/3 byte-identical, output matches
   committed raw byte-for-byte. PASS.

No governance violations in the H-CAUSALEXP-CONSTRUCT wave. (The wave's
own builder result contains one false descriptive claim, addressed in
section 4 below; it is a documentation error, not a governance breach.)

## What the mechanism does (undisputed)

A learner enumerates sequences of lengths 1..5 over four primitives
{S=set X:=1, W=wait, OY=observe Y, OZ=observe Z} (4+16+64+256+1024 =
1364 total, 1302 with an observe action), simulates each under the live
hypothesis pair, and selects the first sequence (fixed lexicographic
order S<W<OY<OZ) whose predicted outcomes disagree. It then executes
that sequence exactly once against the true world. Zero real-world
actions occur before selection.

World A: selects [S,W,OY] (length 3). World B: selects [S,W,W,OY]
(length 4). All four configs converge with exactly one execution.

## Why the L3 construction claim is dead

Two independent adversaries, from preregistered specs, without builder
code, converge on the same kill:

A2 (ae9121f47):
- A-F2-1 SUCCEEDS: independent pure-Zag reimplementation from the prereg
  spec produces byte-identical SELECT outputs. The learner is a pure
  deterministic function of (hypothesis pair, fixed 1364-sequence
  enumeration, researcher lexicographic order, researcher
  first-disagreement criterion, researcher MAXD=5). No incremental
  construction, no partial-progress guidance. Selection from a disguised
  menu.
- A-F2-2 SUCCEEDS: sealed World C requires depth 6; the MAXD=5 learner
  halts with NO-DISCRIMINATING-SEQUENCE. The prereg's "unbounded in
  length" claim is false.
- A-F2-3 FAILS honestly (single candidate at World A depth 3; order
  irrelevant).

A1 (cad84f070):
- AX-CX1 SUCCEEDS: static source analysis (line 202 hardcodes
  while(d<=5); lines 206-222 base-4 counting in fixed order; lines
  227-228 first-discriminating selection) plus pure-enumeration program
  reproducing raw checked counts exactly ([S,W,OY] is the 3rd
  with-observe sequence at depth 3; [S,W,W,OY] the 15th at depth 4).
  Per Program 3 kill condition, the "invention" maps directly to one
  entry in a finite researcher-enumerated candidate list. The
  "composed, not listed" defense is void: lazy generation by counting
  IS enumeration.
- AX-CX2 SUCCEEDS: sealed World C (H5=[(X,Z,5),(Z,Y,0)],
  H6=[(X,Y,4)]) needs 6 actions; MAXD=5 checks all 1302 with-observe
  sequences and finds nothing; MAXD=6 finds [S,W,W,W,W,OY]. The depth
  bound is load-bearing.
- AX-CX3 SUCCEEDS: generation is hypothesis-blind. The disagreement
  predicate only FILTERS a pre-enumerated stream; no algorithm step
  inspects hypothesis structure to propose candidates. The K-CX4
  BECAUSE criterion rules out random trial-and-error but does not
  distinguish this learner from a zero-understanding exhaustive
  enumerator.

Researcher retains, per both adversaries: the primitive set, the depth
cap (load-bearing), the enumeration order, the selection criterion, and
the hypothesis space (acknowledged authored). The learner contributes
exhaustive enumeration and simulation. It never reasons about delays,
never works backward from what must differ, never targets the
disagreement.

## The false descriptive claim (documentation correction)

The builder result (48f2adc15, CXCONSTRUCT_RESULT.md) states: "No
sequence is pre-authored; the sequence space is unbounded in length."
This is false. The source hardcodes while(d<=5). The space is 1364
sequences, finite and researcher-bounded. Both adversaries proved this
empirically. The BUILD-PASS verdict is unaffected (no kill bar tested
this sentence), but the sentence is RETRACTED as a description of the
mechanism. Future citations must not repeat it.

## What survives: measured value of the bounded L2 mechanism

The downgrade to L2 does not make the mechanism worthless. Three
independent measurements quantify real value:

1. Baseline step 5 (48e24c825, BASELINE-LOSES): random search finds
   discriminating sequences at 0.5-3% density (hopeless); greedy
   real-world trial-and-error needs 17 executions (World A) and 85
   (World B) versus the learner's 1; memorization trained on A,B scores
   0/2 on novel Worlds C,D while the learner scores 4/4. The
   disagreement filter finds needles in 97-99.5% non-needle space at
   zero real-world search cost and generalizes to novel hypothesis
   pairs without retraining.
2. Ablation step 8 (48cf64979): removing the filter drops convergence
   4/4 to 0/4 (filter load-bearing for correctness); removing
   simulation raises real-world actions to 35 (A) and 254 (B), i.e.
   35x-254x efficiency from simulation; depth-5-only still converges 4/4
   but with longer sequences (deepening buys efficiency, not
   correctness); reverse order costs 3.5-4x more checks
   (order is efficiency-relevant); MAXD=3 converges exactly 2/4
   (bound load-bearing for correctness).
3. The filter is order-independent for correctness (AB4) and the
   selections are exactly reproducible by independent reimplementation
   (A2, baseline P-CB1, ablation anchor).

Fair summary: a correctness-critical disagreement filter plus
efficiency-relevant search choices (simulation, deepening, order) over
a researcher-enumerated finite family. Useful machinery. Not invention.

## Classification

SURVIVES as bounded L2 (systematic exhaustive search with a
disagreement filter). The 7/7 BUILD-PASS is valid against its frozen
bars. The L3 construction reading is KILLED by A1 and A2. The
"unbounded in length" descriptive sentence is RETRACTED.

This mechanism may be kept as: a bounded L2+ subsystem, an experimental
baseline for experiment-selection efficiency, a negative/control
reference for future construction claims, and a possible low-level
component (the disagreement filter) inside a genuinely constructive
architecture. It is not: L3, representational invention, or genuine
experiment construction.

## Implications for the next frontier

Per A1's forward guidance, the next causal frontier needs
hypothesis-GUIDED generation, not hypothesis-FILTERED enumeration.
Concretely, a successor must show at least one of:

(a) generation order or extent that depends on hypothesis content
    (e.g., working backward from a predicted disagreement to propose
    a targeted sequence, rather than filtering a fixed stream);
(b) a depth bound set or extended by the learner from evidence,
    not a researcher constant;
(c) construction of a discriminating intervention outside every finite
    family enumerable from researcher-fixed primitives and bounds.

Until then, no L3 claim in the causal-experiment lane.

## Steps 7 and 9 (completed during audit)

Step 7 OOD (4c5538a3c, prereg 96cdad502, lineage verified): OOD-FAIL
(0/4). Three failure modes, all consistent with bounded L2:
- OOD-1 deeper worlds: depths 6, 7, 8 all NO-DISCRIMINATING-SEQUENCE.
  The depth cap is a hard boundary.
- OOD-2 fifth primitive: a world solvable with a 5th observe action is
  invisible to the frozen 4-action menu. Source audit: state layout
  hardcodes 3 variables and action dispatch hardcodes 0-3; no extension
  point exists.
- OOD-3 inhibition law: a non-monotonic true law (Y = NOT X,
  inexpressible as delay rules) yields silent false convergence; truth
  outside the hypothesis class is not detected.
The OOD failures strengthen the "bounded" in bounded L2: the mechanism
fails exactly at the researcher-fixed boundaries (depth cap, primitive
set, hypothesis class).

Step 9 transfer (486136c15, prereg 1a3307b79, lineage verified):
TRANSFER-PARTIAL (3/4). The enumerate-filter-select loop transfers when
the researcher re-parameterizes it: 6-primitive enumeration works (base
parameterized, no hardcoded total=total*4), threshold-rule semantics
work through a swapped simulator, and one concept-transfer test passes.
The loop itself does not invent new primitives, new rule semantics, or
new hypothesis classes; the researcher supplies them. Partial transfer
of a fixed loop, not general construction ability.

Neither step alters the verdict. Both corroborate it.

## Pending items

None. All 11 steps are complete. The classification SURVIVES-AS-L2
with L3 KILLED is final.

## Claim ledger entry

| Claim | Disposition |
|-------|-------------|
| H-CAUSALEXP-CONSTRUCT BUILD-PASS 7/7 | STANDS (frozen bars undisputed) |
| "Learner constructs experiments" (L3 reading) | KILLED (A1 AX-CX1/2/3, A2 A-F2-1/2) |
| "Sequence space unbounded in length" | RETRACTED (false; MAXD=5 hardcoded) |
| Disagreement filter adds measured value | CONFIRMED (baseline 17x-85x, ablation correctness-critical, 4/4 novel generalization) |
| H-CAUSALEXP-CONSTRUCT as L2 mechanism | SURVIVES (bounded) |
