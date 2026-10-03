# REPORT.md -- Cognitive Operation Invention (COGOP)

Date: 2026-10-02. Worker: COGOP-INVENTION.
Verdict: **COGOP-INVENTION-COMPLETE** (with novelty analysis, section 5).

## 1. What was built

A frozen 4-op ISA (MOVE/INC/DEC/BEQ) plus CALL, the experiment's realization
of the proposed EXECUTE(root,frame) invocation machinery: CALL saves all 8
registers to a value stack, runs a graph from the op inventory, restores
registers, and deposits the result in R0 (depth cap 16, step cap 20000,
fail-closed). No ADD, MUL, or POW semantic case exists anywhere in the
interpreter; the source holds only the 6 generic op forms (build.sh asserts
exactly op==1..6).

On this basis a generic, task-independent learner runs three mechanisms:

- PLANNER: exhaustive search over flat branch-free straight-line bodies,
  lengths 1..3, over synthesis regs R0..R3 and immediates 0..3.
- CONSTRUCTOR: systematic trial over a generic REPEAT form =
  prologue (6 frame setups: save-inputs x accumulator-init {none,0,1}) x
  step (flat body length 1..2) x counter reg (R0..R5), compiled to a
  counter loop with BEQ. First candidate passing all 10 train pairs, then
  all 6 held-out probes, is promoted.
- PROMOTER: appends the graph plus contract {name, arity, domain} to a
  persistent inventory. Later stages use CALL h atomically; the
  constructor never inspects promoted graphs (it emits CALL h by handle
  only), so reuse is opaque.

Invention tower: Stage 1 invents OP_ADD from {MOVE,INC,DEC}; Stage 2 invents
OP_MUL from {basis, CALL OP_ADD}; Stage 3 invents OP_POW (a^b, 0^0=1) from
{basis, CALL OP_ADD, CALL OP_MUL}. The driver computes expected outputs via
world_add/world_mul/world_pow; learner code never calls world_* (asserted).

## 2. Results vs frozen predictions and kill bars

K-COGOP-1 (prereg frozen+committed alone first): PASS. PREREG.md committed
alone as `e9ffbd9f7` before implementation.

K-COGOP-2 (source checks): PASS. build.sh: isa forms exactly 1..6;
mode/bridge/handler 0; `as *i32` 0; `_zag_print` 0; python 0;
`world_` in learner section 0; `as []f64`/`as []i64` 0.

K-COGOP-3 (experimental bar): PASS. All of the following held on the
frozen implementation:

- P1 planner baselines fail with EXACT tried counts: 65640 / 70643 / 75894
  (found=0 at all three stages). The counts match the preregistered
  combinatorics exactly (40^1+40^2+40^3, 41^1+41^2+41^3, 42^1+42^2+42^3),
  confirming the planner ran the full exhaustive space.
- Constructor found=1 at all three stages (tried=2 / 1471 / 58460).
- Ablations report INVENTION-FAIL: A (MUL, basis only) tried=59040
  found=0; B (POW, basis+CALL0) tried=61992 found=0. Both tried counts equal
  the full constructor space (6*(40+1600)*6 and 6*(41+1681)*6), so the
  spaces were exhaustively searched, not merely sampled.
- Grids through the CALL path: 289/289, 289/289, 25/25.
- Post-invention single-CALL planner bodies ([CALL h] alone on train):
  10/10 at all three stages.
- 3/3 deterministic byte-identical
  (sha256 bbf1fd4aa54ca6d50d0850399b8d1dabc69e26660888fc4d010d5d097dbe3be4).
- Inventory holds exactly the 3 invented ops at end.

K-COGOP-4 (novelty analysis present): this section 5.

P5 partial miss (prediction, not a kill bar): the prereg predicted Stage 2
would discover (P4,[MOVE R1 R3; CALL OP_ADD],R1). The learner instead found
(P0,[DEC R0; CALL 0],R0) -- a different, valid multiplication algorithm
(analyzed in section 4). No kill bar pinned the found structure; all bars
still pass. The miss is reported, not patched.

## 3. White-box creation traces

Decoded from the recorded (prologue, step, kreg, graphlen):

OP_ADD, handle 0, (P0,[INC R0],R1), graphlen 6:
```
0: MOVE R5 R1
1: BEQ R5 #0 ->5
2: INC R0
3: DEC R5
4: BEQ R6 #0 ->1
5: RET
```

OP_MUL, handle 1, (P0,[DEC R0; CALL 0],R0), graphlen 7:
```
0: MOVE R5 R0
1: BEQ R5 #0 ->6
2: DEC R0
3: CALL 0
4: DEC R5
5: BEQ R6 #0 ->1
6: RET
```
After iteration k (1..a): R0 = (a-k) + k*b; after a iterations R0 = a*b.
Edge a=0 skips the loop, R0=0. Verified on the full 0..16 grid.

OP_POW, handle 2, (P5,[MOVE R1 R3; CALL 1],R1), graphlen 10:
```
0: MOVE R3 R0
1: MOVE R4 R1
2: MOVE R0 #1
3: MOVE R5 R1
4: BEQ R5 #0 ->9
5: MOVE R1 R3
6: CALL 1
7: DEC R5
8: BEQ R6 #0 ->4
9: RET
```
Repeatedly applies the (opaque) OP_MUL b times starting from 1; 0^0=1 via
the skip path. Verified on the full 0..4 grid.

## 4. The Stage-2 surprise

The researcher hand-derived MUL as "save b, start acc=0, iterate
acc=ADD(acc,a)" (P4). The learner found "counter=a, iterate R0=ADD(R0-1,b)"
(P0): it decrements the accumulator and re-adds b each pass, using R0 as
both counter source and accumulator. This form was not hand-derived in the
prereg; it emerged from the fixed enumeration order (P0 before P4, slen 1
before 2, K=R0... it is the 1471st candidate). It is a genuine
multiplication, not a trick: the invariant R0=(a-k)+k*b holds by induction
and the 289-point grid plus probes confirm it. The binary structurally
verified the found step contains CALL 0 (the reuse check), so N4 holds for
the actual found form.

## 5. Novelty analysis: is the invented operation genuinely new?

T1 (no flat body computes ADD): by induction every register in a
straight-line {MOVE,INC,DEC} body holds a constant or input_i +/- c; a+b
is not of that form. Planner: 65640 bodies, 0 found.

T2 (no fixed composition of {basis, CALL ADD} computes MUL -- the not-a-macro
argument): every register in a straight-line body holds an affine function
alpha*a+beta*b+gamma (MOVE/INC/DEC and CALL ADD(z,w)=z+w preserve affinity).
ab is not affine: (0,0)->0,(1,0)->0,(0,1)->0,(1,1)->1 contradicts
f(1,1)=f(1,0)+f(0,1)-f(0,0). A macro is a fixed finite unfolding; MUL
requires an input-dependent iteration count, which is exactly the semantic
content the invented op adds. Planner: 70643 bodies, 0 found.

T3 (no fixed composition of {basis, CALL ADD, CALL MUL} computes POW): every
register holds a fixed polynomial P(a,b) (CALL MUL multiplies polynomials).
POW forces Q(b)=P(2,b)=2^b on all naturals b, but the (d+1)-th finite
difference of a degree-d polynomial is 0 while for 2^b it is 2^b != 0 --
contradiction. Planner: 75894 bodies, 0 found.

N1 learner-defined semantics: the interpreter has no ADD/MUL/POW cases;
the graphs above were written into learner-state inventory at runtime and
their contracts emitted from that state.
N2 not-a-macro: T1..T3 plus the three exhaustive planner failures.
N3 enabling: each invented op unlocks the next stage; no stage is solvable
in the vocabulary available before its enabling op exists (planner +
ablation exhaustiveness).
N4 opaque reuse: found steps contain CALL h (binary-verified); the
constructor emits CALL by handle and never reads promoted graphs; later
stages treat them atomically.
N5 ablation: removing the enabling op destroys the capability
(INVENTION-FAIL on the FULL space: 59040 and 61992 candidates, all fail).
N6 persistence and use: inventory ends with exactly the 3 ops; each is
exercised through the CALL path on full grids and the single-CALL check.

## 6. Honest limits

1. Finite researcher-enumerated schema. The REPEAT form (6 prologues x step
   odometer x 6 counter regs) is researcher-defined; the learner selects a
   (P,S,K) triple from that finite family rather than assembling loop
   structure itself. Under the strictest bar (open structural form, final
   structure never chosen from a finite researcher-enumerated family) this
   does not clear full L3 representational invention. It demonstrates the
   mechanics of operation invention -- wall, construction, contract,
   opaque reuse, enablement, ablation -- with novelty real relative to the
   plan vocabulary. Open-form structure assembly is the identified next
   frontier.
2. Computability. The 4-op basis is Turing-complete in the idealization,
   so the invented ops add no computability-theoretic power (preregistered).
   The novelty is cognitive: named, contracted, reusable units that
   compress input-dependent iteration into the bounded plan vocabulary.
3. Toy tower: three arithmetic ops, small integer domains, one task tower.
   Transfer across changed surface representations was not tested here.

## 7. Files and hashes

- `cogop.zag` -- single pure-Zag source (learner, then `// === DRIVER ===`, then driver)
- `build.sh` -- guard re-verify, K-COGOP-2 checks, compile, 3 runs, hashes, cmp
- `cogop` -- binary, sha256 d0820db40c1c432d51af23bce5136ebcfb92bac0bdaef645b97172378e62ecdc
- `run1.txt`/`run2.txt`/`run3.txt` -- byte-identical outputs, sha256
  bbf1fd4aa54ca6d50d0850399b8d1dabc69e26660888fc4d010d5d097dbe3be4
- `PREREG.md` (frozen, committed alone as e9ffbd9f7), `NAMECHECK.md`, this file
