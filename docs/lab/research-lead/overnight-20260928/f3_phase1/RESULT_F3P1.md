# RESULT_F3P1: F3 Phase 1 -- DNF Representation + State, R-A/R-B Regression

Date: 2026-09-30. Worker: F3 Phase 1 Builder.
Prereg: `2c0d26a4f` (committed alone before implementation; verified
ancestor of this result commit via git merge-base --is-ancestor).
Design: `68aa2f6e8`. Status: PHASE1-TESTED. Pure Zag. No Python.

## 1. Verdict

**PHASE1-TESTED.** K1 PASS, K2 PASS, K3 PASS (with one documented
harness exit-code caveat, section 6). No falsifier fired.

## 2. What was built

`f3_p1.zag` (single file, concatenated BEFORE the frozen world files
at build time; worlds not copied or modified):

- DNF rule sets (design section 2): per effect variable, a set of up
  to 4 conjunctive rules; each literal is (src, polarity, delay).
  Prediction: V(t)=1 iff some rule's literals all hold.
- 7-item persistent state (design section 3): rules[164B],
  effects[48B], verify_buf[16B, quiescent], history[656B, empty],
  doubt[4B, zeroed], varied[4B, tracked], Dcur[i32=4, fixed].
- OP-PROBE: all 16 action codes probed 3x in controlled contexts;
  effects[] classified per the frozen decision procedure, with the
  preregistered SETS(v,val) clarification (post value recorded, so
  CLR is representable). During development the kind=1 setup was
  corrected to SET all vars (prereg said "setup SET all"); the first
  build only set ctrl vars and misclassified CLR on non-ctrl vars.
- OP-PROP: singleton literals, both polarities, delays 1..Dcur,
  fit = ok>0 and never refuted; context guards retained as ordinary
  guard literals (World B: `X@2 + guard !K@2` proposed, ok=2).
- Hypothesis enumeration: Cartesian product, k=1 rule per effect var
  (Phase 1; state and DNF simulation support k<=4).
- Disagreement-driven experiment loop, planning (goal modes 0 and 1),
  and simulation ALL read action semantics from effects[] only.
  Source audit: no kind==0/1/2/3 branches in decision code. The only
  literal-kind uses are F3_probe setup (harness-side initialization,
  prereg section 3) and F3_emit_prim display labels.

## 3. Evidence

| World | md5 (3/3) | NHYP | Exps | Bar | GOAL | stderr |
|---|---|---|---|---|---|---|
| R-A (A-confounded-chain) | e7113382f2c13e02489475ee7abbc515 | 24 | 3 | <=4 (F2=2,+2) | GOAL_REAL=1 | 0 bytes |
| R-B (B-contextual-delay) | 33e55a3a665be700af65124cb93b19ac | 4 | 1 | <=3 (F2=1,+2) | GOAL_REAL_B2=1 | 0 bytes |

R-A trace: SELECT [SX,W,OD], [SD,W,OZ], [SD,W,W,OY]; 3 experiments,
converged by exhaustion to 4 survivors (equivalence class over X's
spurious correlates), PLAN [SX,W,W,W,SX] identical to F2's, goal met
for real. Zero world calls during search (SEARCH_CALLS_OK=1).

R-B trace: candidates `X@2` and `X@2 & !K@2` for Y; single experiment
[SX,SK,W,W,OY] (identical to F2's) killed the unguarded rule;
PLAN_B2 M=[SX,CK,W,SX,W,SX] identical to F2's; triple (Y=1,K=0)
verified for real.

K1: representation and state implemented as preregistered; growth
trace emits PROP (with ok counts) and RULESET lines for every
hypothesis; Dcur=4 logged; effects[] table dumped per code.

K2: R-A 3 <= 4 with GOAL_REAL=1; R-B 1 <= 3 with GOAL_REAL_B2=1.
F-COST, F-GOAL, F-REGRESS: none fired.

K3: pure Zag (znc, sh, grep, git, md5sum only; zero python3
invocations); zero em/en-dash bytes (byte-checked in source and all
logs); 3/3 byte-identical runs per world; zero stderr bytes on all
six runs. Exit code is 1, not 0: see section 6 caveat.

## 4. Falsifiers

None fired. F-COST (exceed F2+2): no. F-GOAL: no. F-PURITY: no.

## 5. Honest scope

Phase 1 is a representation+state migration with no regression, not
a capability advance. Real: DNF machinery, negative-polarity
literals in OP-PROP, learned effect table read by all decision code,
growth trace, 7-item state with quiescent Phase-7 slots. Not yet:
multi-rule hypotheses (k=1), per-rule refutation, OP-GROW/SPLIT/VAR,
EXTEND/STOP, verification stream, REVISE, doubt gating, history use.
No L3 claim. Promotion steps 4-11 remain for any SURVIVES discussion.

## 6. Exit-code caveat (K3)

The frozen F2 world files provide main(), which returns 0 only for
F2's own mask (63). F3 Phase 1 uses its own adjudication per prereg
section 6 and returns 0/1 from L_run; the frozen main therefore
prints "AUTOSCI_A PROGRAM_FAIL mask=0" and exits 1 even on
PHASE1-TESTED. This is a harness artifact of reusing the sealed F2
worlds verbatim (which the prereg requires: worlds concatenated from
their committed paths, unmodified). The authoritative verdict is the
`F3P1 RESULT` line. The learner completed its verdict path cleanly on
all six runs: zero stderr, 3/3 byte-identical. K3 is reported PASS on
substance with this caveat explicit; the exit-code line is F2's
frozen string, not a claim about F3.

## 7. Reproduction

Build (BUILD.sh in this directory):
  cat f3_p1.zag ../autosci2/world_a2.zag > run_p1a.zag
  znc run_p1a.zag -o bin_p1a && ./bin_p1a
Same with world_b2.zag for R-B. Toolchain:
znc 2026.07.0-dev (edition 2026).
