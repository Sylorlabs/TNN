# RESULT: L3C protocol v2 (recursive form construction)

Date: 2026-09-30. Builder: L3C Protocol-v2 Builder subagent.
Prereg: PREREG_L3C_V2.md, frozen and committed alone as 9e595301a.
Implementation: l3c_v2.zag (pure Zag, zero Python), built with the pinned
in-repo znc (sha256 prefix 498abcb5ab346f8c).

## Verdict: L3C-V2-PARTIAL

Per the frozen verdict mapping ("C resolves but another family misses" ->
PARTIAL): Family C resolved recursively, Families A, B, E and the v1
regression matched predictions exactly, but Family D's literal prediction
(k=3) did not match the observed k=2. The D gap is a prereg arithmetic
error, not a mechanism failure: the frozen disc2 spec applied to the frozen
D vectors yields exactly 2 separators, provably (derivation below). The
mechanism behaved faithfully; the prediction was miscalculated. No bar was
weakened to reach this verdict; the literal mapping governs.

## Frozen predictions vs observed (mode 1, 3 runs byte-identical)

| Family | Frozen prediction | Observed | Match |
| A (501) | unique conjunction (f1==0 AND f2==0), nested chain depth 2, eval 4/4, D_a1 labeled target is DISP | BUILT natoms=2, eval 4/4, CHK_A_nested=PASS, CHK_A_atoms=PASS | YES |
| B (502) | built delta 0 after clash 1, unique (f1,GE,9) after clash 2, eval 4/4 | defer1 delta=0, defer2 delta=1, eval 4/4, CHK_B_ineq=PASS | YES |
| C (503) | root (f1==1); nested contradiction stashed then refined; D1 labeled target kind==2; eval 6/6 | BUILT natoms=1, REFINE edge=7 natoms=1 a0=(3,0,9), eval 6/6, CHK_C_nested=PASS, CHK_C_D2atom=PASS | YES |
| D (504) | AMBIGUOUS k=3, no dispatch built, heldout 2/4 | AMBIGUOUS k=2 (1,0,1) (2,0,9), rule still TERM, heldout 2/4 | LITERAL MISS (see below) |
| E (505) | unique (f1==1 AND f2==1) over full history, eval 5/5 | BUILT natoms=2, eval 5/5, CHK_E_atoms=PASS | YES |
| Regression 67/131 | (f2==1), 6/6 | 6/6, atom checks PASS | YES |
| Regression 327 | (f3==9), 4/4 | 4/4, atom check PASS | YES |

Determinism: run1/run2/run3 byte-identical
(sha256 13ae08737e4b00276e5923f4454c0523feb3eb9a9cd1d57b3384d5dd160e2d1e).
Ablation (mode 0, construction disabled): built=0, evals at base rates
(A 2/4, B 2/4, C 2/6, E 3/5, reg 4/6 and 2/4); the construction machinery
is what produces the gains.
Anti-widening audit (audit_v2.sh): A1/A2/A5/A6 PASS; A3 (interp one edge
path, recursive) and A4 (all node/edge writes inside the six generic op_*
fns) verified by read. No sig literals outside fn main; op_label_edge has
one definition and is called only from build_chain with variable atom args.

## The Family D discrepancy (prereg arithmetic error, documented not hidden)

Frozen D vectors: train (3,0,5,7)->2, (3,0,6,7)->2; clash (3,1,9,7)->0 twice.
The prereg predicted three separating single equalities: (f1==1), (f2==9),
(f3==9). Hand-derivation under the frozen disc2 spec:
- f0==3: train contains f0=3 -> not separating.
- f1==1: all clash f1=1, no train f1=1 -> SEPARATES.
- f2==9: all clash f2=9, no train f2=9 -> SEPARATES.
- f3: clash f3=7, train f3={7,7} -> no f3 equality separates. (f3==9) does
  not even match the clash vectors (their f3 is 7).
True separator set: {(f1==1), (f2==9)}, k=2. The observed
"AMBIGUOUS sig=504 k=2 (1,0,1) (2,0,9)" is the provably correct output of
the frozen mechanism on the frozen vectors. The prereg's k=3 was a
hand-computation slip. D's essential scientific criterion from the prereg
("the failure mode is converted from silent misresolution to explicit
represented ambiguity: this is the pass criterion for D, not the score")
is met: ambiguity explicitly represented, no dispatch built, rule still
points at TERM(2), no silent misresolution, heldout 2/4 as predicted.

## Implementation bug found and fixed (pre-final, spec-faithful)

amb_push used the AMB count cell as its write cursor, but disc2 only sets
that cell after the search, so every competitor overwrote slot 0 and the
trace printed a phantom (0,0,0). The k count was always correct; only the
competitor naming in the trace was wrong. Fixed by passing an explicit
slot index (nsep, resp. nsep*2/nsep*2+1 for conjunction pairs) and
recording the atom-triple count for the trace. This is an implementation
bug fix toward the frozen spec, not a mechanism change: no frozen bar,
vector, or verdict-relevant number changed (k stayed 2 throughout).

## Was the dispatch form genuinely constructed? (vs template-widening)

Evidence for genuine recursive construction, from the white-box dump:
- Family C: D1 (node 9, DISP) was built by try_construct_root with atom
  (f1==1); edge 7 (D1's labeled edge) initially targeted TERM(0). After
  two corroborated nested contradictions on edge 7, try_refine built D2
  (node 11, DISP) with atom (f3==9) and re-pointed edge 7 at D2 (edge_set_to,
  a generic op). D2's own labeled edge (f3==9) targets TERM(7); its default
  targets the old TERM(0). The final form has a DISP node as a labeled
  edge target, which v1's fixed template could never emit (v1 targets were
  always TERM). CHK_C_nested=PASS and CHK_C_D2atom=PASS assert this
  structurally, not just behaviorally.
- Family A: build_chain emitted a 2-deep DISP chain (natoms=2 from disc2);
  natoms=1 degenerates to the v1 shape, so depth tracks the discovered
  predicate arity, not a template constant.
- The audit shows no per-family semantic cases: one op_label_edge
  definition, called once from build_chain with variable atom arguments;
  interp has a single edge-following path with recursion; all node/edge
  mutation flows through six generic ops.
Honest ceiling (per prereg): bounded L2 at most. The discriminator
vocabulary (equality/inequality atoms, max conjunction arity 2, search
order, EVID_MIN=2) is researcher-authored and disclosed; no L3 or
Criterion-0 claim is made.

## Recommended next step

Transparent amendment of PREREG_L3C_V2.md's Family D prediction (k=3 ->
k=2, with the derivation above; or, alternatively, correcting the clash
vector's f3 to 9 if the three-competitor design was the intent), then
re-freeze and re-run for a clean verdict. The amendment decision is
Micah's; the current verdict stands as PARTIAL under the literal frozen
mapping either way.
