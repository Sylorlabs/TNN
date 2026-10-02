# T6 Sealed Task Specification

Status: SEALED. This is the sealed T6 capstone specification for Battery v2.
It was written by an independent adversary worker per the sealing protocol
(T6_SPEC_DRAFT.md section 7, commit `f26f432dc`). It authorizes T6 evaluation
under the rules in section 9. It contains the exact train and held-out
episode lists, the exhibited target program, and the verification run log.

## 0. Seal metadata

- Sealed by: the T6 Sealer worker, an independent adversary. The sealer is
  independent of the B, C2, and D implementers and of the draft author, and
  has not implemented or debugged any hypothesis evaluated under v2.
- Seal date: 2026-09-30.
- Gate verification (prereg section 3.7): the following commits were each
  verified to be ancestors of this seal commit with
  `git merge-base --is-ancestor` before sealing:
  - `69730b4ab`: B freeze (hyp_b implementation + B-TESTED result)
  - `cdffdcca9`: C2 K4-clean rerun (C2-CLEAN-PASS)
  - `2500fd02b`: D K4-clean rerun (D-V2-FAIL)
  - `d2a69d512`: Battery v2 preregistration (frozen)
  - `9ad539fc2`: T6 gate verdict (T6-GATE-READY)
  - `f26f432dc`: T6 spec draft (prerequisite work product, not a gate item)
  No T6 evaluation commit exists. The seal strictly follows every gate item.
- VM core reference: the verifier embeds lines 1-208 (through `pvm_valid`)
  of the frozen GENEXEC2-P source
  `docs/lab/research-lead/overnight-20260928/genexec2p/genexec2p.zag`,
  sha256 `00c496e3ffb64f40fc0bedca6f158b43e755fd326ed6ba22f379d8af35c599cc`,
  replacing only `main()` with the verification harness in section 11.
- Verification: 3/3 byte-identical runs,
  md5 `d2ec874a67bd18e63ef37b18e77940c1`, zero stderr bytes, PVM_VALID=1,
  22/22 episode matches. Authoring and verification used shell, git, and
  znc only. No Python was used at any stage.
- The sha256 of this file is recorded in the seal commit message per the
  sealing protocol S2.

## 1. VM variant

T6 targets GENEXEC2-P (the restricted VM: jumps, calls, arithmetic, and
stack operations; DIV, MOD, LT, EQ, GT ablated to PVM_TRAP).

Rationale, carried from the draft: (a) the P-VM conditional line T1/T4/T5
is the battery's key discriminator, and the capstone extends that line
rather than opening a new VM axis; (b) on the full VM, DIV and MOD admit
arithmetic shortcuts that bypass intended control flow (the v1 D lesson);
on GENEXEC2-P any non-straight-line target forces jumps, and any jump-free
solve of a conditional T6 fires F-TRICK, so the kill switch acts as a true
anomaly detector; (c) the retained jumps are exactly the machinery T6
probes.

## 2. Task definition

f(a, b) = a*b if a == b, else a + b.

- Diagonal region (a == b): quadratic, nonlinear, via MUL.
- Off-diagonal region (a != b): linear, a + b.
- Integer arithmetic on i32. On all listed episodes |a*b| <= 16, so no
  wraparound behavior is exercised or relied upon.

## 3. Episode lists

Train episodes (12). The harness exposes ONLY these to each hypothesis.

| # | a | b | target | region |
|---|----|----|--------|--------|
| 0 | -2 | -2 | 4 | diagonal |
| 1 | 0 | 0 | 0 | diagonal |
| 2 | 1 | 1 | 1 | diagonal |
| 3 | 3 | 3 | 9 | diagonal |
| 4 | 2 | 2 | 4 | diagonal |
| 5 | -2 | 1 | -1 | off-diagonal |
| 6 | 1 | -2 | -1 | off-diagonal |
| 7 | 0 | 3 | 3 | off-diagonal |
| 8 | 3 | 0 | 3 | off-diagonal |
| 9 | -1 | -2 | -3 | off-diagonal |
| 10 | 2 | -1 | 1 | off-diagonal |
| 11 | -3 | 1 | -2 | off-diagonal |

Held-out episodes (10), disjoint from train. Revealed only after all
hypotheses report on T6.

| # | a | b | target | region |
|---|----|----|--------|--------|
| 12 | -4 | -4 | 16 | diagonal |
| 13 | 4 | 4 | 16 | diagonal |
| 14 | -1 | -1 | 1 | diagonal |
| 15 | -4 | 2 | -2 | off-diagonal |
| 16 | 2 | -4 | -2 | off-diagonal |
| 17 | 4 | -3 | 1 | off-diagonal |
| 18 | -3 | 4 | 1 | off-diagonal |
| 19 | 1 | 2 | 3 | off-diagonal |
| 20 | -2 | -3 | -5 | off-diagonal |
| 21 | 3 | -1 | 2 | off-diagonal |

## 4. Exhibited target program

V1 witness. 11 ops, PVM_VALID=1, verified on all 22 episodes (section 10).

```
addr  op    arg   mnemonic
0     1     0     IN0
1     2     0     IN1
2     4     0     SUB
3     17    8     JNZ 8
4     1     0     IN0
5     2     0     IN1
6     5     0     MUL
7     18    11    JMP 11
8     1     0     IN0
9     2     0     IN1
10    3     0     ADD
```

Semantics: push a, push b, SUB gives a-b; JNZ pops it and jumps to 8 iff
a != b. On the diagonal path (a == b): push a, push b, MUL gives a*b, JMP
to end. On the off-diagonal path: push a, push b, ADD gives a+b. Program
length 11, within the 40-op envelope. Contains JNZ (op 17) and JMP
(op 18). No ablated opcodes.

## 5. Validity checklist (V1-V5)

- V1 computability: the section 4 program is exhibited; its exact outputs
  on all train and held-out episodes are logged in section 10 (22/22).
- V2 material difference: the target contains JNZ and JMP, and is
  materially different from T0..T5 (defended in section 6).
- V3 budget adequacy: 11 ops total, within the 40-op envelope shared with
  v2-SOLVE.
- V4 episodes: 12 train, 10 held-out, disjoint, fixed above.
- V5 no reverse engineering: intended discriminations are recorded in
  section 7; T6 satisfies V2 on its own structural merits.

## 6. Family selection and V2 defense

Adversary selection: the equality-gated quadratic/linear two-input task of
section 2. The draft's primary recommendation was the quadratic kink family
(single-input piecewise with a nonlinear region). The adversary selects
this equality-gated form instead, for the following recorded reason.

On GENEXEC2-P the comparison opcodes are ablated, so the only branch
primitives are exact-equality tests (JZ/JNZ on x-k) plus unconditional
jumps. A single-input kink over ranges then forces an unpleasant choice:
either a degenerate single-point task, or an exact-value decision chain at
roughly 4 ops per distinguished value. Covering 22 episodes that way
pressures the 40-op cap and yields a lookup table rather than a structured
piecewise target. The equality-gated design keeps every property the
primary was chosen for: a nonlinear region via MUL (no T0..T5 task has any
nonlinear region), a genuine conditional branch in the exhibited target,
and the C2 discriminator of whether repair synthesizes the nonlinear
region. It is exactly exhibitable in 11 ops and generalizes to all inputs,
not only the listed episodes.

V2 defense: T6 is not a straight-line arithmetic map (the exhibited target
branches; a branch-free program cannot compute the diagonal/off-diagonal
distinction without a comparison or division primitive, both ablated); not
a single-kink absolute value (two inputs, quadratic region); not a
periodic mod; not a two-input parity (T3's target is branch-free parity;
T6's target branches on equality and computes a*b on the diagonal). No
T0..T5 task contains any nonlinear region, and no T0..T5 target requires a
jump. The exhibited target contains JNZ and JMP.

## 7. Intended discriminations (V5)

Hypotheses evaluated under v2: B (fragment retrieval), C2
(counterexample-guided splitting with lookahead and bounded backtracking),
D (MAP-Elites straight-line synthesis). A and C are falsified under v1 and
are not evaluated.

- D: predicted FAIL. D is straight-line only on the polynomial VM; a
  conditional target is out of reach. A D v2-SOLVE on T6 triggers a V2
  audit: either the sealed function admitted a straight-line shortcut
  (adversary error, task void per F-TRICK) or D gained control flow
  (smuggling audit under F-SMUG/F-TRICK).
- B: predicted FAIL unless B's prereg was transparently amended with a
  case-capable base constructor before any v2 evaluation (prereg
  section 4, star condition). If amended, B must show the section 3.6
  trace events: at least 2 retrieval events with behavioral match recorded
  before each CALL, and at least 2 CALLs to the same P-VM-valid fragment
  id. An unamended B SOLVE on a conditional T6 fires an F-SMUG/F-TRICK
  audit.
- C2: conditional SOLVE. Predicted path: split event(s) partitioning the
  diagonal (a == b) from the off-diagonal; each region repaired; 0 CALLs
  in the final program. The key discriminator is whether C2's repair
  synthesizes the nonlinear diagonal region (a*b via MUL). C2 SOLVE with a
  trace showing the partition tracked and the diagonal region synthesized
  is the CONFIRM path. C2 FAIL on the diagonal while solving the
  off-diagonal localizes the repair boundary precisely.

Sharpest signals:

(a) C2 SOLVE with B FAIL and D FAIL confirms split-and-repair beyond
single-input piecewise, and gives B its sharpest signal: no novel
primitive is required, still FAIL.

(b) Any D SOLVE or any jump-free SOLVE on T6 voids or audits per F-TRICK
and V2. No quiet patch is permitted.

## 8. Falsifier application on T6

- F-TRICK: any hypothesis exhibiting a jump-free GENEXEC2-P program
  achieving v2-SOLVE on T6 voids the task pending re-investigation. The
  exhibiting program is preserved as evidence.
- F-SMUG: DIV, MOD, LT, EQ, or GT anywhere in the final program (main
  plus all called fragment bodies) voids the exhibiting result.
- F-MEM: a memorization-style solve over the 40-op cap is not SOLVE.
- Confirmation rule (prereg section 3.6): a prediction is CONFIRMED iff
  the observed outcome matches under v2-SOLVE and the committed
  construction trace shows the predicted mechanism via the mandatory trace
  events. Outcome match without mechanism trace is UNCONFIRMED.

## 9. Harness and void rules (S3/S4)

- At evaluation time the harness exposes ONLY the train episodes of
  section 3 to each frozen hypothesis. Held-out episodes and the target
  program are revealed only after all hypotheses report on T6.
- No hypothesis code changes between seal and reporting; any change voids
  that hypothesis's T6 run. A re-freeze would require a new sealed spec,
  because the old train episodes are then seen.
- Any T6 evaluation run whose ancestry does not show this seal commit
  after all implementation freeze commits is void. Verify with
  `git merge-base --is-ancestor` before accepting results.
- F-TRICK firing on T6 voids the task pending re-investigation. F-SMUG
  voids the exhibiting result. A post-seal contestant change voids the run.
  A broken gate (seal before all freezes) voids the seal itself; the gate
  verification in section 0 shows the gate held.
- No L3 claim follows from battery success alone (prereg section 3.6).
  After a CONFIRMED battery, the mandatory Criterion 0 sequence applies:
  source audit, persistence, reuse, transfer, revision, adversarial unseen
  structure.

## 10. Verification run log

Adversary verifier output, run 1 of 3 (3/3 byte-identical,
md5 `d2ec874a67bd18e63ef37b18e77940c1`, zero stderr bytes):

```
PVM_VALID=1
OPCOUNT=11
TRAIN ep=0 a=-2 b=-2 out=4 exp=4 MATCH
TRAIN ep=1 a=0 b=0 out=0 exp=0 MATCH
TRAIN ep=2 a=1 b=1 out=1 exp=1 MATCH
TRAIN ep=3 a=3 b=3 out=9 exp=9 MATCH
TRAIN ep=4 a=2 b=2 out=4 exp=4 MATCH
TRAIN ep=5 a=-2 b=1 out=-1 exp=-1 MATCH
TRAIN ep=6 a=1 b=-2 out=-1 exp=-1 MATCH
TRAIN ep=7 a=0 b=3 out=3 exp=3 MATCH
TRAIN ep=8 a=3 b=0 out=3 exp=3 MATCH
TRAIN ep=9 a=-1 b=-2 out=-3 exp=-3 MATCH
TRAIN ep=10 a=2 b=-1 out=1 exp=1 MATCH
TRAIN ep=11 a=-3 b=1 out=-2 exp=-2 MATCH
HELD ep=12 a=-4 b=-4 out=16 exp=16 MATCH
HELD ep=13 a=4 b=4 out=16 exp=16 MATCH
HELD ep=14 a=-1 b=-1 out=1 exp=1 MATCH
HELD ep=15 a=-4 b=2 out=-2 exp=-2 MATCH
HELD ep=16 a=2 b=-4 out=-2 exp=-2 MATCH
HELD ep=17 a=4 b=-3 out=1 exp=1 MATCH
HELD ep=18 a=-3 b=4 out=1 exp=1 MATCH
HELD ep=19 a=1 b=2 out=3 exp=3 MATCH
HELD ep=20 a=-2 b=-3 out=-5 exp=-5 MATCH
HELD ep=21 a=3 b=-1 out=2 exp=2 MATCH
MATCHES=22/22
```

## 11. Reproduction appendix

The verifier source is /tmp/t6verify/verify_t6.zag
(sha256 `3e37428008daadcb58dd53b7939f570d275523a441e30fd8566bf52b46e1d360").
It embeds lines 1-208 (through `pvm_valid`) of the frozen GENEXEC2-P source
`docs/lab/research-lead/overnight-20260928/genexec2p/genexec2p.zag`
(sha256 `00c496e3ffb64f40fc0bedca6f158b43e755fd326ed6ba22f379d8af35c599cc\)),
replacing only `main()` with the verification harness below. Build with
`znc verify_t6.zag -o verify_t6_bin` and run `./verify_t6_bin`.
Expected: PVM_VALID=1, 22/22 MATCHES, byte-identical across runs.

Harness main (verbatim):

```zag
// ============ T6 verification main (adversary harness) ============
// Verifies the sealed T6 exhibited target program on all train and
// held-out episodes using the frozen GENEXEC2-P vm_run above.
// This main replaces the conformance main; it is a harness, not a hypothesis.
fn ep_set(ea:[]u8, eb:[]u8, et:[]u8, i:i32, a:i32, b:i32, t:i32)void {
  set32(ea, i*4, a); set32(eb, i*4, b); set32(et, i*4, t);
  return;
}
fn main()void {
  let lib_buf:[]u8=z_alloc(4096);
  let lib_idx:[]u8=z_alloc(8*4);
  let nlib:i32=0;
  let stack:[]u8=z_alloc(256*4);
  let rs:[]u8=z_alloc(64*8);
  // Exhibited target: f(a,b) = a*b if a==b else a+b. 11 ops.
  let p:[]u8=prog_new(16);
  prog_set(p, 0, 1, 0);
  prog_set(p, 1, 2, 0);
  prog_set(p, 2, 4, 0);
  prog_set(p, 3, 17, 8);
  prog_set(p, 4, 1, 0);
  prog_set(p, 5, 2, 0);
  prog_set(p, 6, 5, 0);
  prog_set(p, 7, 18, 11);
  prog_set(p, 8, 1, 0);
  prog_set(p, 9, 2, 0);
  prog_set(p, 10, 3, 0);
  prog_set_len(p, 11);
  emit("PVM_VALID="); e64(pvm_valid(p, 11)); emit("\n");
  emit("OPCOUNT=11\n");
  let ea:[]u8=z_alloc(22*4);
  let eb:[]u8=z_alloc(22*4);
  let et:[]u8=z_alloc(22*4);
  ep_set(ea, eb, et, 0, -2, -2, 4);
  ep_set(ea, eb, et, 1, 0, 0, 0);
  ep_set(ea, eb, et, 2, 1, 1, 1);
  ep_set(ea, eb, et, 3, 3, 3, 9);
  ep_set(ea, eb, et, 4, 2, 2, 4);
  ep_set(ea, eb, et, 5, -2, 1, -1);
  ep_set(ea, eb, et, 6, 1, -2, -1);
  ep_set(ea, eb, et, 7, 0, 3, 3);
  ep_set(ea, eb, et, 8, 3, 0, 3);
  ep_set(ea, eb, et, 9, -1, -2, -3);
  ep_set(ea, eb, et, 10, 2, -1, 1);
  ep_set(ea, eb, et, 11, -3, 1, -2);
  ep_set(ea, eb, et, 12, -4, -4, 16);
  ep_set(ea, eb, et, 13, 4, 4, 16);
  ep_set(ea, eb, et, 14, -1, -1, 1);
  ep_set(ea, eb, et, 15, -4, 2, -2);
  ep_set(ea, eb, et, 16, 2, -4, -2);
  ep_set(ea, eb, et, 17, 4, -3, 1);
  ep_set(ea, eb, et, 18, -3, 4, 1);
  ep_set(ea, eb, et, 19, 1, 2, 3);
  ep_set(ea, eb, et, 20, -2, -3, -5);
  ep_set(ea, eb, et, 21, 3, -1, 2);
  let i:i32=0;
  let ok:i32=0;
  while(i<22){
    let a:i32=get32(ea, i*4);
    let b:i32=get32(eb, i*4);
    let t:i32=get32(et, i*4);
    let o:i32=vm_run(p, 11, a, b, lib_buf, lib_idx, nlib, stack, rs);
    if(i<12){ emit("TRAIN "); } else { emit("HELD "); }
    emit("ep="); e64(i);
    emit(" a="); e64(a); emit(" b="); e64(b);
    emit(" out="); e64(o); emit(" exp="); e64(t);
    if(o==t){ emit(" MATCH\n"); ok=ok+1; } else { emit(" MISMATCH\n"); }
    i=i+1;
  }
  emit("MATCHES="); e64(ok); emit("/22\n");
  return;
}
```
