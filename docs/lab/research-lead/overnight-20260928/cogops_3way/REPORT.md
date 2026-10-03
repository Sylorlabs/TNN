# REPORT: COGOPS-3WAY (follow-up to COGOPS-COMPOSE C417)

Date: 2026-10-03. Worker: COGOPS-3WAY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_3way/`
Prereg: commit 77d949573 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed; the implementation files below
were written after that commit landed). Implementation commit follows
this report.

## Verdict: THREE-WAY COMPOSITION DEMONSTRATED (K1-K6 PASS; with
documented errata, see below)

The learner owns three specialized procedures, a learner-built indexed
RETRIEVE (id 2, from generic id 0), a learner-built indexed VERIFY
(id 3, from generic id 1), and a learner-built indexed COUNT (id 5,
from generic id 4), each with its own working set, inverted index,
and provenance record in learner state. Faced with composite goals it
was never told how to solve, the learner discovered need-to-procedure
bindings by trial over three families (801 -> RETRIEVE, 802 ->
VERIFY, 807 -> COUNT, recorded with per-family ok/fail counts),
assembled per-goal plans from those bindings and each goal's
dependency links (including a new fan-in aggregate link kind),
bound each need to the specialized or generic version from its
learned coverage at execution time, persisted and reused the plans,
re-derived a byte-identical plan after its binding and plan tables
were wiped, and declined a goal whose need no procedure family could
consume.

Three goal types assemble to three distinct orders from the SAME
learned bindings: goal 808 executes [RETRIEVE, VERIFY, COUNT]
(retrieve candidates, verify each, count distinct objects of the
passing set), goal 809 executes [COUNT, RETRIEVE, VERIFY] (count
first on a literal subject, pivot its relation into the retrieve,
verify each candidate), goal 812 executes [VERIFY, RETRIEVE, COUNT]
(verify a chain, pivot its step-0 relation into the retrieve, count
objects of the retrieved subjects). No researcher-supplied pipeline
encodes any of the three orders.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | agree=12/12 | 12/12 (every Q line agree=1) | PASS-WITH-ERRATA (see E1, E3) |
| K2 | cs=1184 < cg=2272 | cs=1184 < cg=2272 | PASS |
| K3a | zero literals in c3_learn.zag, c3_main.zag | word-boundary grep empty in both (after E4 fix) | PASS |
| K3b | three distinct orders from identical bindings | PLAN-808 [RET,VFY,CNT], PLAN-809 [CNT,RET,VFY], PLAN-812 [VFY,RET,CNT] | PASS |
| K3c | trial ok/fail counts incl. failed 811 | 801:(ok0=1,f1=1,f2=1) 802:(f0=1,ok1=1,f2=1) 807:(f0=1,f1=1,ok2=1) 811:(f0=1,f1=1,f2=1,fam=-1) | PASS |
| K3d | 808 plan runs [spec,spec,spec] / [gen,gen,gen] / [gen,gen,spec] | S2 vers=2,3,5; S5 vers=0,1,4; S6 vers=0,1,5 | PASS |
| K4 | S5 vers=[0,1,4]; S6 vers=[0,1,5]; C1 vers=[3,0,5]; B0/B1 vers=[5,2,3] | exact match on all queries | PASS |
| K5 | S8 rebuilt PLAN-808 bytes identical | REDERIVE match=1 | PASS |
| K6 | decline=1, trials=21, no 810 plan | `Q id=X goal=810 decline=1`; trials=21 | PASS |
| K7 | 3/3 byte-identical stdout, stderr empty | sha256 7be6cbbc x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag | verified (see Toolchain) | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

Per-query detail (all match the frozen per-query predictions,
modulo errata E3):
- A0: st=2 (built), vers=2,3,5, ans=6:1,613,1,613,1,2, cs=64, cg=224
- A1/A2: st=1 (loaded), vers=2,3,5, ans 6:1,615,1,615,1,2 / 5:1,611,0,1,0, cs=64/48, cg=224/168
- B0: st=2, vers=5,2,3, ans=6:1,2,1,615,1,615, cs=64, cg=224
- B1: st=1, vers=5,2,3, ans=6:1,2,1,612,1,612, cs=64, cg=224
- C0: st=2, vers=3,2,5, ans=6:1,1,1,616,1,2, cs=64, cg=224
- C1: st=1, vers=3,0,5 (per-need fallback inside one plan: 603 not in ret coverage), ans=6:1,1,1,615,1,2, cs=104, cg=224
- D0/D1: st=1, vers=0,1,4, ans 6:1,713,1,713,1,2 / 6:1,716,1,716,1,2, cs=160, cg=160
- D2/D3: st=1, vers=0,1,5 (mixed plan after count re-specialized), ans 6:1,714,1,714,1,2 / 5:1,718,0,1,0, cs=136/120, cg=160/120
- S8: st=2 (rebuilt), vers=0,1,5, ans=6:1,714,1,714,1,2, cs=136, cg=160
- SUMMARY-3WAY: agree=12 plans_built=4 plans_loaded=8 trials=21 declines=1 cs=1184 cg=2272 (procedure uses: ret_spec 6, ret_gen 6, vfy_spec 7, vfy_gen 5, cnt_spec 10, cnt_gen 2)

Learner-state evidence:
- LSTATE-RET after S1A: nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1
- LSTATE-VFY after S1B: nrel=3 ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1
- LSTATE-CNT after S1C: nrel=3 ids=601,602,603 cnts=16,16,16 prov=4,8,11,56 rev=1
- LSTATE-CNT after S6: nrel=2 ids=701,702 cnts=16,16 prov=4,12,15,40 rev=2 (distractors absent from all dumps: selectivity learned)
- BIND after S2 and after S7 as in the K3c row above.

## Errata (transparent; prereg NOT silently amended)

E1 (K1 oracle defect, same class as C417's E1): the first build
showed agree=0 on C0/C1. The defect was in oracle_812 (the
researcher's reference), not the learner: it passed the retrieve
output buffer to cnt_gen at subject offset 0, but ret_gen writes
[nsubs, subjects...], so subjects start at offset 4. The oracle
counted objects of subject id 1 (the count word) instead of the
retrieved subject. Fixed to offset 4; rebuilt; agree=12/12. The
learner's answers were correct in both builds; only the reference
was wrong.

E2 (driver print defect): the first build printed trailing stale
zeros in vers lines (e.g. `vers=2,3,5,0,0`) because vbuf[8] held
both the third version slot and the need-count word. Moved the
count word to offset 12 (versions at 0,4,8; count at 12). Driver
print machinery only; version selection itself was always
correct, and the first three printed values already matched the
frozen predictions.

E3 (K1 answer-framing shorthand in the prereg): the frozen table
wrote A2/D3 answers as `4:1,611,0,1,0` and B0/B1 answers as
`5:1,2,1,615,1,1`. The preregistered answer-assembly rule (each
need's output record framed as [count, ints...]) yields 5 ints for
A2/D3 ([1,611] + [0] + [1,0]) and 6 ints for B0/B1, where the VFY
fan-out record is [npass, passing-subjects...] = [1,615], not the
standalone [1,verdict] form. The learner and the oracles both
implement the uniform record rule with no goal-specific code, and
agree=1 on every query, so the substance (which subjects pass,
which counts) is exactly as predicted. The corrected forms are
5:1,611,0,1,0 (A2), 5:1,718,0,1,0 (D3), 6:1,2,1,615,1,615 (B0),
6:1,2,1,612,1,612 (B1).

E4 (K3a hygiene): the first implementation's cosmetic stage label
strings contained goal-tag literals ("STAGE S2 COMPOSE-808").
They were renamed to order-descriptive labels (COMPOSE-RVC,
COMPOSE-CRV, COMPOSE-VRC, DECLINE-NOVEL) before final
verification; the word-boundary grep over all 16 identifiers is
empty on the final c3_learn.zag and c3_main.zag. Labels are
output text only; no plan, binding, or version logic changed.

## Evidence detail

Learner-not-researcher (K3): `grep -wE` over all 16 identifiers
(601,602,603,607,609,701,702,707,801,802,807,808,809,810,811,812)
returns empty on c3_learn.zag and c3_main.zag; the identifiers
occur only in c3_world.zag (the environment definitions) and as
runtime values in output. The identical trial/assembly code bound
801->RETRIEVE, 802->VERIFY, 807->COUNT from observed outcomes,
assembled three distinct orders for 808 vs 809 vs 812, and failed
all three families on 811.

Composition without a pipeline (K3b/K4): the 808 plan
`[0:801:0] [1:802:1] [2:807:2]`, the 809 plan
`[0:807:2] [1:801:0] [2:802:1]`, and the 812 plan
`[0:802:1] [1:801:0] [2:807:2]` share bindings but not order;
versions are resolved per need per execution from coverage, so
the same stored 808 plan ran as [spec,spec,spec] on world A,
[gen,gen,gen] after all coverages were cleared on world B, and
[gen,gen,spec] after count was re-specialized on B. C1 shows
fallback inside a single plan: [vfy_spec, ret_gen, cnt_spec]
because the pivoted relation 603 was never in the retrieve
working set. B0/B1 show COUNT executing first and specialized.

Reuse and re-derivation (K5): plans_built=4 (A0, B0, C0, S8
rebuild), plans_loaded=8; after wiping plans AND bindings,
trials re-ran (9) and the rebuilt 808 plan was byte-identical
(REDERIVE match=1).

Principled decline (K6): goal 810's need 811 (3 fields [9,0,0])
was refused by RET (arity 2), by VFY (not chain-shaped), and by
COUNT (aggop 0, not 1); the binding stayed fam=-1 and compose
returned NO_PLAN without crashing.

Generics not strawmen: ret_gen/vfy_gen/cnt_gen are the oracles
for all 12 composite queries and the fallback executors; every
composed answer equals the all-generic composition. The
learner's contribution is binding discovery, assembly, version
selection, and check-cost reduction, never correctness repair.

## What this establishes (and does not)

Establishes: learner-driven composition scales to three
learner-owned specialized procedures: trial-learned bindings
over three families, three distinct per-goal assembled orders
from identical bindings (3 of the 6 possible orders, all forced
by goal link structure), coverage-driven per-need versions
across three families, persisted/reused/re-derivable plans, and
principled decline of unbindable goals, with correctness equal
to the generic oracles at strictly lower check cost (1184 vs
2272, 1.92x). No pipeline, mode, or procedure sequence is
researcher-supplied. The honest boundary from C417
("two-procedure composition only") no longer holds for the
three-procedure chain-with-fan-in case.

Does not establish: general DAG/fan-out/fan-in composition
beyond three procedures in chain-with-fan-in form (no diamond,
no cycles, no multi-input fan-in beyond the count aggregate);
retirement of the generic procedures (they remain fallback and
oracle); learner CREATION of a procedure from scratch (seeds
researcher-supplied by design); learner invention of the
need-tag or aggop ontology itself (tags are environment-defined;
the learner discovers the bindings, not the vocabulary);
behavior on non-chain structures; scaling beyond the tested
sizes.

## Toolchain

- safebin active for every command (PATH=$HOME/safebin exported
  per invocation; setup_safebin.sh run at startup,
  SAFEBIN-READY, 36 tools, no python); `which python3` /
  `which python` return nothing; znc 2026.07.0-dev (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Zero forbidden-executable invocations. All computation pure
  Zag; shell only for znc/binary/git/assembly/byte-verification
  (plus sed for the E4 label rename).
- Git writes via /usr/bin/git absolute path (safebin git symlink
  has the known EPERM-on-write defect). Explicit pathspecs on
  every add/commit; no other lane touched; nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_3way/`:
PREREG.md (frozen, commit 77d949573), NAMECHECK.md (Step 0),
c3_base.zag, c3_world.zag, c3_learn.zag, c3_main.zag,
c3_build.sh, c3_full.zag (assembled; exactly one `fn main`),
c3_bin, c3_compile.txt, c3_run1/2/3.txt (sha256
7be6cbbcdcc9bc43f9e83ae3dad94db853a7d2f417f26222b276e4bada562d23)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Four-procedure composition or a diamond/fan-out-fan-in goal
   (two procedures feeding one), pushing toward general DAG
   assembly.
2. Retirement: conditions for dropping a generic fallback
   (coverage confidence + correctness record), as C408
   follow-up #2 (still open).
3. Learner-invented need ontology: seed with weaker shape cues
   and test whether the learner invents the binding vocabulary
   itself, as C408 follow-up #3 (still open).
4. Interleaved worlds with composition: A/B episodes mixed,
   testing plan stability under coverage union vs revision.
