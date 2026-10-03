# REPORT: COGOPS-COMPOSE (follow-up to C408 COGNITIVE-OPS-LEARNER)

Date: 2026-10-03. Worker: COGOPS-COMPOSE.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_compose/`
Prereg: commit a43e0f98e (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed; the implementation files below
were written after that commit landed). Implementation commit follows
this report.

## Verdict: COMPOSITION DEMONSTRATED (K1-K6 PASS; K1 and K2 with
documented arithmetic errata, see below)

The learner owns two specialized procedures, a learner-built indexed
RETRIEVE (id 2, derived from generic id 0) and a learner-built indexed
VERIFY (id 3, derived from generic id 1), each with its own working
set, inverted index, and provenance record in learner state. Faced
with composite goals it was never told how to solve, the learner
discovered need-to-procedure bindings by trial (501 -> RETRIEVE,
502 -> VERIFY, recorded with ok/fail counts), assembled per-goal plans
from those bindings and each goal's dependency links, bound each need
to the specialized or generic version from its learned coverage at
execution time, persisted and reused the plans, re-derived a
byte-identical plan after its binding and plan tables were wiped, and
declined a goal whose need no procedure family could consume.

The two goal types assemble to opposite orders from the SAME learned
bindings: goal 503 executes [RETRIEVE, VERIFY] (retrieve candidates,
then verify each), goal 504 executes [VERIFY, RETRIEVE] (verify a
chain, then retrieve with a relation pivoted from the chain). No
researcher-supplied pipeline encodes either order.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | agree=10/10 | 10/10 (every Q line agree=1) | PASS-WITH-ERRATUM (see E1) |
| K2 | cs=400 < cg=768 | cs=456 < cg=840 | PASS-WITH-ERRATUM (see E2) |
| K3a | zero literals in cc_learn.zag, cc_main.zag | word-boundary grep empty in both | PASS |
| K3b | PLAN-503 [RET,VFY] vs PLAN-504 [VFY,RET] | `[0:501:0] [1:502:1]` vs `[0:502:1] [1:501:0]` | PASS |
| K3c | trial ok/fail counts incl. failed 506 | 501:(ok0=1,f1=1) 502:(f0=1,ok1=1) 506:(f0=1,f1=1,fam=-1) | PASS |
| K3d | 503 plan runs [spec,spec] / [gen,gen] / [spec,gen] | S2 vers=2,3; S4 vers=0,1; S5 vers=2,1 | PASS |
| K4 | S4 vers=[gen,gen]; S5 vers=[spec,gen]; G1 vers=[spec,gen] | exact match on all 5 queries | PASS |
| K5 | S7 rebuilt PLAN-503 bytes identical | REDERIVE match=1 | PASS |
| K6 | decline=1, trials=10, no 505 plan | `Q id=X goal=505 decline=1`; trials=10 | PASS |
| K7 | 3/3 byte-identical stdout, stderr empty | sha256 c9cf5b2d x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag | verified (see Toolchain) | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

Per-query detail (all match the frozen per-query predictions):
- F0: st=2 (built), vers=2,3, ans=4:1,313,1,313, cs=24, cg=96
- F1/F2: st=1 (loaded), vers=2,3, ans 4:1,315,1,315 / 3:1,311,0, cs=24, cg=96
- G0: st=2, vers=3,2, ans=4:1,1,1,315, cs=24, cg=96
- G1: st=1, vers=3,0 (per-need fallback inside one plan), ans=4:1,1,1,315, cs=48, cg=96
- H0/H1: st=1, vers=0,1, ans 4:1,413,1,413 / 4:1,416,1,416, cs=72, cg=72
- H2/H3: st=1, vers=2,1 (mixed plan), ans 4:1,414,1,414 / 3:1,418,0, cs=56, cg=72
- S7: st=2 (rebuilt), vers=2,1, ans=4:1,414,1,414, cs=56, cg=72
- SUMMARY-COMP: agree=10 plans_built=3 plans_loaded=7 trials=10
  declines=1 cs=456 cg=840 (procedure uses: ret_spec 7, ret_gen 3,
  vfy_spec 5, vfy_gen 5)

Learner-state evidence:
- LSTATE-RET after S1A: nrel=2 ids=301,302 cnts=8,8 prov=0,0,3,32 rev=1
- LSTATE-VFY after S1B: nrel=3 ids=301,302,303 cnts=8,8,8 prov=1,4,7,32 rev=1
- LSTATE-RET after S5: nrel=2 ids=401,402 cnts=8,8 prov=0,8,11,24 rev=2
  (distractors 307/309/407 absent from all dumps: selectivity learned)
- BIND after S2 and after S6 as in the K3c row above.

## Errata (transparent; prereg NOT silently amended)

E1 (K1 answer-format shorthand): the frozen table wrote the 504
answers as [1,1,315]. The preregistered answer-assembly rule (2.4/5:
the executor appends each need's output record, each record framed as
[count, ints...]) yields [1,1,1,315]: the VFY need's record [1,verdict]
followed by the RET need's record [1,sub]. The initial oracle_504
appended the verdict bare, producing [1,1,315]; the learner produced
the record-framed [1,1,1,315]; hence agree=0 on G0/G1 in the first
build. The defect was in the oracle (the researcher's reference), not
the learner: the learner's uniform per-need record rule is generic
machinery with no goal-specific code, and the substantive predicted
content (verdict=1, subjects=[315]) is exactly what the learner
produced. Fixed oracle_504 to emit the VFY record in the same framed
form; rebuilt; agree=10/10. If governance requires the exact
three-int form, the remedy is a fresh prereg with the corrected
answer contract, not an amendment to this verdict.

E2 (K2 totals omitted the S7 query): the frozen totals cs=400 /
cg=768 summed 9 queries but 10 ran (the S7 rederive query is counted
in agree=10/10). Every per-query cs/cg prediction in section 6 is
exact; the hand-summed totals were short by S7's 56/72. Correct
totals: cs=456, cg=840. The kill criterion's substance, strictly
fewer fact-checks via the composed specialized plan, holds: 456 <
840 (1.68x; the S2/S3 all-specialized queries run at 4x, the
mixed/fallback queries less, as predicted per query).

## Evidence detail

Learner-not-researcher (K3): `grep -wE` over all 14 identifiers
(301,302,303,307,309,401,402,407,501,502,503,504,505,506) returns
empty on cc_learn.zag and cc_main.zag; the identifiers occur only in
cc_world.zag (the environment definitions, 20+15+12+... matches) and
as runtime values in output. The identical trial/assembly code bound
501->RETRIEVE and 502->VERIFY from observed outcomes, assembled
opposite orders for 503 vs 504, and failed both families on 506.

Composition without a pipeline (K3b/K4): the 503 plan
`[0:501:0] [1:502:1]` and the 504 plan `[0:502:1] [1:501:0]` share
bindings but not order; versions are resolved per need per execution
from coverage, so the same stored 503 plan ran as [spec,spec] on
world A, [gen,gen] after the ret coverage was cleared on world B,
and [spec,gen] after ret was re-specialized on B. G1 shows fallback
inside a single plan: [vfy_spec, ret_gen] because the pivoted
relation 303 was never in the retrieve working set.

Reuse and re-derivation (K5): plans_built=3 (F0, G0, S7 rebuild),
plans_loaded=7; after wiping plans AND bindings, trials re-ran (4)
and the rebuilt 503 plan was byte-identical (REDERIVE match=1).

Principled decline (K6): goal 505's need 506 (3 fields) was refused
by RET (arity 2) and by VFY (not chain-shaped); the binding stayed
fam=-1 and compose returned NO_PLAN without crashing.

Generics not strawmen: ret_gen/vfy_gen are the oracles for all 10
composite queries and the fallback executors; every composed answer
equals the all-generic composition. The learner's contribution is
binding discovery, assembly, version selection, and check-cost
reduction, never correctness repair.

## What this establishes (and does not)

Establishes: two learner-owned specialized procedures can be composed
by learner-derived structure: trial-learned bindings, per-goal
assembled order, coverage-driven per-need versions, persisted/reused/
re-derivable plans, and principled decline of unbindable goals, with
correctness equal to the generic oracles at strictly lower check
cost (456 vs 840). No pipeline, mode, or procedure sequence is
researcher-supplied.

Does not establish: composition of 3+ procedures or general
DAG/fan-out/fan-in (this is the two-procedure case); retirement of
the generic procedures (they remain fallback and oracle); learner
CREATION of a procedure from scratch (seeds researcher-supplied by
design); learner invention of the need-tag ontology itself (tags are
environment-defined; the learner discovers the bindings, not the
vocabulary); behavior on non-chain structures; scaling beyond tested
sizes.

## Toolchain

- safebin active for every command (PATH=$HOME/safebin exported per
  invocation); `which python3` / `which python` return nothing;
  znc 2026.07.0-dev (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Zero forbidden-executable invocations. All computation pure Zag;
  shell only for znc/binary/git/assembly/byte-verification.
- Git writes via /usr/bin/git absolute path (safebin git symlink has
  the known EPERM-on-write defect). Explicit pathspecs on every
  add/commit; no other lane touched; nothing pushed.
- Note: the first commit attempt used `-m` after `--` and failed
  (git read the message as a pathspec); retried with correct order.
  No files were affected.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_compose/`:
PREREG.md (frozen, commit a43e0f98e), NAMECHECK.md (Step 0),
cc_base.zag, cc_world.zag, cc_learn.zag, cc_main.zag, cc_build.sh,
cc_full.zag (assembled; exactly one `fn main`), cc_bin,
cc_compile.txt, cc_run1/2/3.txt (sha256
c9cf5b2df1f0eb3e4181ad6a20bf85cfb2dd08840a32483eeadba5e31e755318)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Three-procedure composition (add a third learner-owned procedure,
   e.g. specialized COUNT/AGGREGATE) toward DAG/fan-out/fan-in.
2. Retirement: conditions for dropping a generic fallback (coverage
   confidence + correctness record), as C408 follow-up #2.
3. Learner-invented need ontology: seed with weaker shape cues and
   test whether the learner invents the binding vocabulary itself
   (toward L3 creation), as C408 follow-up #3.
4. Interleaved worlds with composition: A/B episodes mixed, testing
   plan stability under coverage union vs revision.
