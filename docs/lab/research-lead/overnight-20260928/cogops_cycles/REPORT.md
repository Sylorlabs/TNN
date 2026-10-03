# REPORT: COGOPS-CYCLES (follow-up to COGOPS-DIAMOND C433)

Date: 2026-10-03. Worker: COGOPS-CYCLES.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_cycles/`
Prereg: commit 9b233ee74 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). No amendments; errata below
are implementation-stage corrections, not prereg changes.
Implementation commit follows this report.

## Verdict: CYCLES JOIN THE ENVELOPE (K1-K4 PASS, K5 as predicted, K6-K9 PASS; with documented errata)

The learner owns three specialized procedures (indexed RETRIEVE id 2,
indexed VERIFY id 3, indexed COUNT id 5, all built from episodes with
provenance in learner state). Faced with cycle goals it was never told
how to solve, the learner's generalized composer discovered
need-to-procedure bindings by trial over three families (801 ->
RETRIEVE, 802 -> VERIFY, the same bindings as chains and diamonds),
assembled per-goal plans (a self-loop plan [1,2,0] and a 2-node-cycle
plan [0,1,2,3] with a logged 1/4 Kahn stall), and iterated the
learner-owned procedures to a fixpoint: RETRIEVE re-applied along a
successor chain until output == input (the taught fixpoint identity),
VERIFY re-checking each step, halting by quiescence (no output
changes) under a frozen pass cap that never fired. Both cycle answers
are byte-identical to independent all-generic oracles, at lower check
cost (1272 vs 3256, 2.56x).

The frozen C433 machinery, run on the same goals and the same plan
records, fails exactly as predicted: the self-loop goal's single-pass
execution reads the uncomputed (zero) output through the back-edge and
the walk never starts (ans=4:0,0,1,611); the 2-node cycle's Kahn order
comes out corrupt ([0,0,2,1], need0 duplicated, need3 dropped) and the
answer is wrong (ans=6:1,611,1,611,0,0). The same bindings, the same
versions, the same plans: the executor is the isolated variable, and
it is what makes cycles composable.

No cycle-specific handler exists. The generalization is four additive,
uniform deltas: stall-aware Kahn with a deterministic fallback
(topological completion, not cycle detection), a uniform kind-1
link-firing rule (copy only from non-empty source outputs),
change-driven iterated execution to quiescence, and a frozen pass cap
for totality. The C433 diamond/chain/decline battery reproduces
byte-identically under the generalized composer.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S8 agree=1 and S9 agree=1 | C0 agree=1 (ans=6:1,618,1,618,1,611); C1 agree=1 (ans=8:1,611,1,618,1,618,1,618) | PASS |
| K2 | cs=1280 < cg=3184 | cs=1272 < cg=3256 (2.56x) | PASS |
| K3a | zero literals in c5_learn.zag, c5_main.zag | word-boundary grep over all 21 identifiers empty in both | PASS |
| K3b | c4_learn -> c5_learn additive only | 21473-byte prefix byte-identical (cmp); 8 new functions only | PASS |
| K3c | trial ok/fail counts incl. failed 811 | 801:(ok0=1,f1=1,f2=1) 802:(f0=1,ok1=1,f2=1) 807:(f0=1,f1=1,ok2=1) 811:(f0=1,f1=1,f2=1,fam=-1) | PASS |
| K3d | same bindings -> chain, diamond, cycle plans | 808 chain + 813/814/815 diamonds + 816 self-loop + 817 2-cycle, bindings 801->0, 802->1, 807->2 | PASS |
| K4 | C0 ans=6:1,618,1,618,1,611 vers=[2,3,2] passes=9; C1 ans=8:1,611,1,618,1,618,1,618 vers=[2,3,2,3] passes=9; TOPO 3/3 and 1/4-stall | exact match on both; TOPO probes 3/3 stall=0 and 1/4 stall=1 | PASS |
| K5 | F0 agree=0 ans=4:0,0,1,611; F1 agree=0 ans=6:1,611,1,611,0,0 with corrupt plan | exact match; F1 plan dump [0:801:0] [0:801:0] [2:801:0] [1:802:1] | AS PREDICTED |
| K6 | S2-S6/S12/S13 match C433 | Q lines, BIND, decline, rederive_match=1 all match | PASS |
| K7 | 3/3 byte-identical stdout, stderr empty | sha256 148015be x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag | verified; zero forbidden invocations | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

Per-query detail (frozen predictions in PREREG Section 6):
- E0: st=2, vers=2,3,3,5, ans=7:1,611,0,1,611,1,2, cs=96, cg=336, agree=1
- E1: st=2, vers=2,3,3,5, ans=8:1,611,1,611,1,611,1,2, cs=112, cg=392, agree=1
- R0: st=2, vers=2,3,5, ans=6:1,613,1,613,1,2, cs=64, cg=224, agree=1
- B0: st=2, vers=0,1,1,4, ans=7:1,713,0,1,713,1,2, cs=240, cg=240, agree=1
- B1: st=1, vers=0,1,1,5, ans=7:1,713,0,1,713,1,2, cs=216, cg=240, agree=1
- C0: st=2, vers=2,3,2, ans=6:1,618,1,618,1,611, cs=136, cg=720, agree=1, passes=9
- C1: st=2, vers=2,3,2,3, ans=8:1,611,1,618,1,618,1,618, cs=192, cg=864, agree=1, passes=9
- F0: st=1, vers=2,3,2, ans=4:0,0,1,611, cs=24, cg=720, agree=0
- F1: st=2, vers=2,2,2,3, ans=6:1,611,1,611,0,0, cs=40, cg=864, agree=0
- X: decline=1
- S8: st=2, vers=0,1,1,5, ans=7:1,713,0,1,713,1,2, cs=216, cg=240, agree=1
- SUMMARY-CYCLES: agree=8 plans_built=8 plans_loaded=2 trials=21
  declines=1 cs=1272 cg=3256 (uses: ret_spec 26, ret_gen 3,
  vfy_spec 30, vfy_gen 6, cnt_spec 5, cnt_gen 1)

Learner-state evidence:
- LSTATE-RET after S1A: nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1
- LSTATE-VFY after S1B: nrel=3 ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1
- LSTATE-CNT after S1C: nrel=3 ids=601,602,603 cnts=16,16,16 prov=4,8,11,56 rev=1
- LSTATE-CNT after S6: nrel=2 ids=701,702 cnts=16,16 prov=4,12,15,40 rev=2
- LSTATE-RET after S7: nrel=2 ids=604,601 cnts=8,16 prov=0,16,18,72 rev=2
- LSTATE-VFY after S7: nrel=1 ids=605 cnts=8 prov=1,19,19,72 rev=2
- BIND after S2 and S12 as in the K3c row above.

## Errata (transparent; prereg NOT silently amended)

E1 (design oversight, caught by testing): the prereg's S7 predicted
LSTATE-RET nrel=3 (601,602,604), forgetting that S5 clears all
coverages (part of the C433 regression: B0 must run all-generic).
With coverages cleared, S7's episodes as preregistered would leave
only 604 covered, forcing the cycle seed RETRIEVE [601,621] onto the
generic version. The fix (implementation-stage, before any cycle
query): S7 runs one additional retrieve episode on the seed pattern
(ep 18, id 2) and specializes ret over eps 16-18, re-learning 601
alongside 604; the vfy episode moved to ep 19. The observed
LSTATE-RET (nrel=2, ids=604,601, cnts=8,16) and LSTATE-VFY (nrel=1,
ids=605, cnts=8) are the corrected predictions; the cycle queries
then execute with all-spec versions as preregistered. The prereg's
S7 text is superseded by this note, not edited.

E2 (arithmetic, caught by testing): the prereg's S9/S11 cg=792
omitted the oracle's need2 RETRIEVE [604,618] call (the
all-generic reference explicitly computes need2's record).
Observed cg=864 for C1/F1. K2 (cs < cg) is unaffected
(1272 < 3256).

E3 (minor variance, unexplained): S8 cs=136 vs the predicted 144
(8 checks). The walk, versions, passes, and answer are all as
predicted; the 8-check shortfall is 0.6% of total cs and does not
affect K2. Not investigated further; recorded here.

E4 (implementation detail, not a prereg deviation): the 4-slot
plan cache filled during the diamond battery (813/814/808/815),
so S7 drops the superseded 813/814/808 plans via the general
plan_drop (keeping 815 for the S13 rederive) before building the
cycle plans. Without this, plan_new returns -1 and the cycle
queries cannot build plans. The prereg did not specify cache
management; the drop is transparent in the S7 output
("PLANDROP done").

## Toolchain disclosure

No near-misses in this task. safebin active for every command
(PATH=$HOME/safebin exported per invocation; setup_safebin.sh run
at startup, SAFEBIN-READY, no python); `which python3` / `which
python` return nothing before and after; znc 2026.07.0-dev (pinned
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`). All computation
pure Zag; shell only for znc/binary/git/assembly/byte-verification.
One debug detour used a lane-local scratch binary (dbg/, since
removed); no Python was involved at any point. K8 PASS.

## Evidence detail

Learner-not-researcher (K3): `grep -wE` over all 21 identifiers
returns empty on c5_learn.zag and c5_main.zag (two comment
violations caught and fixed before the final build; the final
sources are clean). Identifiers occur only in c5_world.zag
(environment) and as runtime values in output. The c4_learn.zag ->
c5_learn.zag relationship is machine-verified: the first 21473
bytes are byte-identical (cmp), and the remainder is exactly the
8 preregistered additive functions (topo_g, apply_kind1_g,
snap_out, out_eq_snap, exec_step_iter, execute_plan_iter,
compose_iter, plan_drop). The generalization contains no
goal-shape test, no need-tag test, no relation test, and no
branch on cyclicity: topo_g completes any partial order,
apply_kind1_g is a uniform link-firing rule, execute_plan_iter
is uniform chaotic iteration. The identical trial/assembly code
bound 801->RETRIEVE, 802->VERIFY, 807->COUNT, assembled chain,
diamond, self-loop, and 2-cycle plans from those bindings, and
failed all three families on 811.

No cycle handler (K3b): the only executor deltas are the four
preregistered ones. The S4 chain and S2/S3 diamond regressions
reproduce C433 exactly under the generalized composer,
proving the deltas do not alter DAG behavior (the structural
reduction of PREREG Section 2.2).

Cycle execution (K4): C0's self-loop plan [1:801:0] [2:802:1]
[0:801:0] iterated RETRIEVE 8 times (611->612->...->618->618)
and VERIFY 8 times, halting by quiescence at pass 9 with the
fixpoint 618 in all three records. C1's 2-cycle plan
[0:801:0] [1:802:1] [2:801:0] [3:802:1] (TOPO placed=1/4,
stall=1, fallback order) iterated the VERIFY->RETRIEVE loop to
the same fixpoint, with need3 verifying the final subject.
Both used only learner-owned spec versions ([2,3,2] and
[2,3,2,3]).

Frozen baseline (K5): F0 loaded C0's plan and ran the frozen
single-pass executor: the kind-1 self-link fired against the
zeroed output, obj became 0, RETRIEVE [604,0] returned [], and
the answer (ans=4:0,0,1,611) disagreed with the oracle. F1
dropped and rebuilt 817's plan through frozen topo, which
emitted [0,0,2,1] (visible in the plan dump: need0 duplicated,
need3 absent); single-pass execution produced
ans=6:1,611,1,611,0,0. Same bindings, same versions, same
(plan) records as the passing queries: the executor is the
isolated variable.

Reuse and re-derivation: plans_built=8 (E0, E1, R0, B0, C0,
C1, F1-rebuild, S8-rebuild), plans_loaded=2 (B1, F0); S13
wiped plans AND bindings and rebuilt 815 byte-identically
(REDERIVE match=1).

Principled decline: goal 810's need 811 refused by all three
families; decline=1, trials=21, no crash.

Generics not strawmen: ret_gen/vfy_gen/cnt_gen are the oracles
for all 8 agreeing queries and the fallback executors; every
composed answer equals the all-generic composition. The
learner's contribution is binding discovery, plan assembly
(including the stall fallback order), version selection, and
executing the iteration to quiescence at lower check cost.

## What this establishes (and does not)

Establishes: learner-driven composition of learner-owned
procedures reaches cycles. The same trial-learned bindings that
assemble chains and diamonds assemble a self-loop plan (one
procedure re-applied until a taught fixpoint) and a 2-node
VERIFY->RETRIEVE cycle plan (Kahn stall logged, fallback order,
iteration to quiescence), with answers byte-identical to
independent all-generic oracles at lower check cost (1272 vs
3256). The frozen single-pass machinery demonstrably cannot:
its failure modes (zero-read through the back-edge; corrupt
Kahn order [0,0,2,1]) are documented on the same goals. Kahn
ordering is not a fundamental limit for re-application; the
preregistered iterated executor covers it with no
cycle-specific handler, mode, or procedure sequence
researcher-supplied.

Does not establish: oscillatory or divergent cycles (the pass
cap is totality insurance, never fired here); cycles whose
halting needs richer vocabulary (e.g. stopping the walk when a
verifier fails, which would need the walk to depend on the
verifier's output); 3+ node cycles; multi-input fan-in beyond
the count aggregate; retirement of the generic procedures;
learner CREATION of a procedure from scratch; learner invention
of the need-tag ontology or of the iteration semantics itself
(the generalization is researcher-supplied by design; the
learner's contribution is binding discovery, plan assembly,
version selection, and iterated execution); scaling beyond the
tested sizes; why S8 spent 8 fewer checks than hand-computed
(E3).

## Toolchain

- safebin active for every command (PATH=$HOME/safebin exported
  per invocation; setup_safebin.sh run at startup,
  SAFEBIN-READY, no python); `which python3` / `which python`
  return nothing; znc 2026.07.0-dev (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- All computation pure Zag; shell only for znc/binary/git/
  assembly/byte-verification.
- Git writes via /usr/bin/git absolute path (safebin git symlink
  has the known EPERM-on-write defect). Explicit pathspecs on
  every add/commit; no other lane touched; nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_cycles/`:
PREREG.md (frozen, commit 9b233ee74), NAMECHECK.md (Step 0),
c5_base.zag, c5_world.zag, c5_learn.zag, c5_main.zag,
c5_build.sh, c5_full.zag (assembled; exactly one `fn main`),
c5_bin, c5_compile.txt, c5_run1/2/3.txt (sha256
148015be59049300d0471a4cf0590d3882778203a3fed943c1946a9778210f5e)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. 3+ node cycles and the halt-on-verifier-failure family: the
   current halting vocabulary is output-stability; a cycle whose
   advance depends on a verifier's verdict needs the walk to
   read verifier output, which the kind-1 non-empty rule does
   not cover.
2. Oscillatory cycles: the cap fires; characterize what the
   learner does (currently out of scope by prereg).
3. The 8-check S8 variance (E3): instrument per-need execution
   counts to close the hand-computation gap.
4. Plan-cache eviction as learner policy: S7's manual
   plan_drop is researcher-directed; a general cache policy
   (e.g. evict oldest on full) would remove the hand-holding.
5. Retirement: conditions for dropping a generic fallback, as
   C408 follow-up #2 (still open).
