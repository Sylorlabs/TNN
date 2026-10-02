# OOD Test Result: H-CAUSALEXP-CONSTRUCT (Step 7 of promotion pipeline)

Date: 2026-09-30. Worker: OOD Test Worker.
Prereg: `PREREG_OOD.md` (frozen at 96cdad502, Amendment 1 at 2550d053c,
committed before any implementation).
Implementation: `ood_cx.zag` (pure Zag, zero Python, zero em-dash bytes).
Raw: `OOD_CX_RAW.txt` (md5 `76028f6d079bee66d1c1f453b57b3196`,
3/3 byte-identical, exit 0, zero stderr).

## K-OOD0: Reimplementation fidelity: GATE PASSES

Independent reimplementation reproduces the builder's committed
`CXCONSTRUCT_RAW.txt` exactly:

- World A: SELECT [S,W,OY], h0pred=0, h1pred=1; checked 2,12,3.
- World B: SELECT [S,W,W,OY], h0pred=0, h1pred=1; checked 2,12,56,15.

All SELECT outputs and checked counts match. The harness is faithful.
OOD verdicts below are drawn from a validated reimplementation.

## OOD-1: Deeper worlds: FAIL

Frozen learner (MAXD=5) on delay-rule worlds requiring deeper experiments:

- D1 (true minimal depth 6): NO-DISCRIMINATING-SEQUENCE.
- D2 (true minimal depth 7): NO-DISCRIMINATING-SEQUENCE.
- D3 (true minimal depth 8): NO-DISCRIMINATING-SEQUENCE.

True minimal depths confirmed by extended-depth exhaustive search
(measurement harness): D1=6, D2=7, D3=8.

The depth cap MAXD=5 is load-bearing. Any world requiring depth >= 6
defeats the frozen learner. The prereg's "unbounded in length" claim is
false (consistent with A2 Attack F2-2).

## OOD-2: Fifth primitive: FAIL

World V with 4th variable V and 5th action OV (observe V).
Hypotheses H31=[(X,V,1)], H32=[(X,V,3)].

- Discriminating sequences in the frozen 4-action menu (depths 1-5): 0.
- Witness in the extended 5-action menu: [S,W,W,OV] gives H31=1, H32=0.
  The world is solvable in principle.

V is unobservable through Y and Z (no rule targets them in H31/H32), so
the frozen menu is blind by construction. The fixed 4-action set is a
hard boundary. Structural fact from source audit: the state layout
hardcodes 3 variables (32 bytes: X,Z,Y,t,tX,tZ,tY) and the action
dispatch hardcodes 0-3; there is no extension point for a 5th primitive.

## OOD-3: Inhibition law: FAIL (silent false convergence)

True law (sealed): Y = NOT X (non-monotonic; inexpressible as delay
rules, which only turn variables on). Hypotheses H25=[(X,Y,1)],
H26=[(X,Y,3)]; both false; truth outside the hypothesis class.

- Frozen learner constructs [S,W,OY] (h0pred=1, h1pred=0).
- EXEC against the sealed inhibition world: real=0.
- H25 eliminated, H26 survives. Survivors: exactly 1.
- Held-out check [S,W,W,W,OY]: true Y=0, H25 predicts 1, H26 predicts 1.
  The survivor is false as a general law.

The mechanism cannot represent inhibition, cannot invent a new
hypothesis form, has no "none of the above" output, and reports success
anyway. This is silent convergence to a false hypothesis.

## OOD-4: Scale: FAIL (combinatorial wall)

Measured checked(d) vs 4^d - 2^d, d=1..10: exact match at all 10 depths
(2, 12, 56, 240, 992, 4032, 16256, 65280, 261632, 1047552).

Zero pruning. The learner enumerates the full unpruned menu. At depth 10,
a single construct call requires 1,047,552 simulations per hypothesis
(2,095,104 for the pair). Growth is 4x per depth with no guidance,
no partial-progress heuristic, no structure-sensitive assembly.

## Overall verdict: OOD-FAIL (0/4)

H-CAUSALEXP-CONSTRUCT generalizes to zero of the four OOD families.
Every boundary is researcher-imposed and load-bearing:

1. Depth cap MAXD=5 (fails at required depth >= 6).
2. Fixed 4-action set (blind to any 5th primitive).
3. Delay-rule hypothesis class (silent false convergence on inhibition).
4. Unpruned 4^d enumeration (combinatorial wall at depth ~10).

## Net assessment

Combined with the A2 alternative-explanation findings (step 6), the
mechanism is now mapped as: systematic exhaustive search over a
researcher-bounded space (1364 sequences at MAXD=5, 4 fixed primitives,
delay-rule hypotheses only), with argmin by researcher-defined order and
criterion. It does not construct, does not generalize beyond its bounds,
does not detect hypothesis-space inadequacy, and does not scale.

The 7/7 BUILD-PASS stands (the bars do not test authorship or OOD).
Classification remains bounded L2. The L3 reading is killed (A2) and the
OOD reading is killed (this report).

What would genuine experiment construction require (design guidance,
not a claim): open-ended action repertoire acquired at runtime,
hypothesis forms invented (not just selected) from evidence, a
"none of the above" signal, and search guided by partial progress rather
than exhaustive enumeration. That is F2's frontier.

## Files

- `PREREG_OOD.md` (frozen prereg + Amendment 1)
- `ood_cx.zag` (pure-Zag implementation)
- `OOD_CX_RAW.txt` (raw output, md5 76028f6d079bee66d1c1f453b57b3196)
