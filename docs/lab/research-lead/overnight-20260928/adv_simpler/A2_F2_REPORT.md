# A2 Attack Report: H-CAUSALEXP-CONSTRUCT (F2)

Date: 2026-09-30.
Prereg: `PREREG_A2.md` (committed as 4f0811349, frozen before implementation).
Result: 2 of 3 attacks SUCCEED. The "construction" is selection from a
disguised menu.

## Method

Independent reimplementation in pure Zag (`a2_f2.zag`) from the prereg
spec. No builder code copied. Simulator written independently from the
frozen semantic description. 3/3 byte-identical runs (md5
508ffe7baa01866b50c0f17ea1a48603). Zero Python. Zero em-dash bytes.

## A-F2-1: Effective menu size: ATTACK-SUCCEEDS

The learner enumerates all sequences of lengths 1 through 5 over 4
primitives: 4+16+64+256+1024 = 1364 total. My independent reimplementation
produces byte-identical SELECT outputs to the builder's committed raw:

- World A: `[S,W,OY]` p0=0 p1=1 (matches builder CXCONSTRUCT_RAW.txt)
- World B: `[S,W,W,OY]` p0=0 p1=1 (matches builder CXCONSTRUCT_RAW.txt)

The learner is a pure deterministic function of (hypothesis pair, fixed
1364-sequence enumeration, researcher-defined lexicographic order
S<W<OY<OZ, researcher-defined first-disagreement criterion,
researcher-defined MAXD=5). There is no incremental construction, no
partial-progress guidance, no structure-sensitive assembly. A trivial
precomputation over the fixed menu reproduces the learner exactly.

This is selection from a disguised menu, not construction.

## A-F2-2: Beyond-menu world: ATTACK-SUCCEEDS

World C (frozen in prereg): H5=[(X,Z,5),(Z,Y,0)], H6=[(X,Y,4)].

Measured discriminating-sequence counts by depth:
- depth 1: 0
- depth 2: 0
- depth 3: 0
- depth 4: 0
- depth 5: 0
- depth 6: 1 (first = [S,W,W,W,W,OY])

The MAXD=5 learner emits NO-DISCRIMINATING-SEQUENCE on World C and halts.
Per its own prereg, this is a BUILD-FAIL outcome.

The prereg (section 8) claims "sequences are composed, unbounded in
length." This is false. The bound MAXD=5 is hardcoded
(`while(d<=5)` in cxconstruct.zag line 202), researcher-imposed, and
load-bearing. A genuine open-ended constructor would extend to depth 6.
The menu is bounded by researcher choice.

## A-F2-3: Researcher-order determinism: ATTACK-FAILS

World A, depth 3: exactly 1 discriminating sequence exists ([S,W,OY]).
The kill criterion required >=2 candidates for the order to matter.
With a single candidate, the lexicographic order is irrelevant.

The attack fails honestly. This does not weaken A-F2-1 or A-F2-2.

## Net assessment

H-CAUSALEXP-CONSTRUCT is systematic exhaustive search over a
researcher-bounded space (1364 sequences, depth cap 5), plus argmin by
researcher-defined order and criterion. The 7/7 BUILD-PASS stands (the
bars do not test authorship). The L3 reading is killed. Classification:
bounded L2 (systematic search), not L3, not genuine construction.

What semantic authority remains with the researcher:
1. The primitive set {S,W,OY,OZ}.
2. The depth cap MAXD=5 (load-bearing; World C defeats it).
3. The enumeration order S<W<OY<OZ.
4. The selection criterion (first disagreeing predictions).
5. The hypothesis space (acknowledged as authored).

The learner contributes exhaustive enumeration and simulation. It does
not incrementally assemble sequences toward a goal, does not use partial
progress to guide construction, and cannot extend beyond the
researcher-fixed bound.

## Targets not attacked this wave

- F1 genexec: no live claim (first wave governance-void). A2 ready.
- F3 DEVINT1: A2 endorses the completed DEVINT1 A2 findings.
- I2 learning-to-learn: no live claim found.

## Files

- `PREREG_A2.md` (frozen prereg)
- `a2_f2.zag` (pure-Zag attack implementation)
- Raw output md5: 508ffe7baa01866b50c0f17ea1a48603 (3/3 identical)
