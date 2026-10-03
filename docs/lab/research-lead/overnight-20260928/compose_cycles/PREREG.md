# PREREG: COMPOSE-CYCLES -- Can the Unified Composition Operation U Compose Cyclic Structure Use?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all implementation.

## 1. Question

Composition has been tested on pipelines (U, COMPOSE-COLLAPSE, verdict
SUBSUMPTION) and diamond/fan-out (GEN; no GEN implementation exists --
see Section 2). Cycles are the next generality frontier: a structure's
output (eventually) feeds back as its own input, with a termination
condition. Test: can U's frozen trial logic compose a MEANINGFUL cycle,
or does the failure boundary show that cycles need a new (general, not
cycle-specific) principle?

Mechanism under test: U = `uni_solve` in `ref_uc_uni.zag` (byte-identical
to the canonical collapse digest, main stripped at build). U's execution
rule is frozen: ordered trial with end-to-end verification over
{single MAPs} then {ordered pairs (x,y), x!=y, each applied exactly once},
then WIDEN=1 (one retry of filter-rejected pairs, triggered solely by
learner-observed exhaustive failure). U has no iteration construct, no
re-application of a structure, and no termination vocabulary.

## 2. Sources under test (frozen digests, verified in NAMECHECK Step 1)

- `ref_uc_uni.zag` -- THE UNIFIED OPERATION U under test. Frozen,
  byte-identical to canonical collapse digest
  `ec36df4a01cb1a2b93043184e6e2c84b07658fe7b0c317f9a489ffd6b7b4562e`.
  Its `main` is stripped at build (`sed '/^fn main/,$d'`); only the
  trial logic ships.
- `ref_uc_base.zag` -- canonical base (arena layout, fact store,
  behaviors, MAP table, teaching). Frozen digest
  `736f12e7452fb0a95c2dbfc8115028a4e1afba9529cb6cd727acb65367799218`.
  Used ONLY as the diff base for `cyc_base.zag` (never built directly).
- GEN: no GEN composition implementation exists in any compose lane
  (domain_blindness lane searched compose_collapse, compose_ops,
  lane-compose-pair6; nothing named GEN implements a composition
  operation). This battery tests U only.

## 3. What makes the cycle "meaningful" (frozen definition)

The workload is fixpoint iteration, stated in domain-neutral mathematical
terms (no domain labels anywhere in code; all identifiers are opaque
integers). It satisfies all five:

- M1 PROGRESS: structure R advances a state strictly along a chain
  (exactly one hop per application). No application is a no-op except
  at the fixpoint.
- M2 DATA-DEPENDENT TERMINATION: the loop stops iff R(x)==x (fixpoint:
  output equals input), a property of the STATE, not an iteration
  count. A max-iteration cap of 8 is a safety bound only, never the
  operative stop in this workload.
- M3 NECESSITY: the fixpoint is 4 applications of R away from the
  start. Section 5 proves by exhaustive enumeration that no single MAP
  application and no ordered pair application reaches it. The cycle
  (re-application with termination check) is the ONLY route to the
  answer with the given structures.
- M4 ADVERSARIAL EVALUATION SIGNAL: structure E measures a property of
  each state; its values along the chain are NON-MONOTONIC
  (2,1,3,1,2), so any naive "stop when the measure stops improving"
  rule fails (it would stop early or never). Only the true fixpoint
  R(x)==x is a sound stop. This blocks trivial early-stopping hacks.
- M5 FAMILY: fixpoint iteration is a mathematically defined cycle
  family (transitive closure by repeated expansion, Newton iteration,
  EM). The test is about the family, not a domain story.

Role mapping to the task brief (prose only, never in code): R is the
refine/advance structure, E is the evaluate structure whose per-state
output feeds back as the termination-relevant observation.

## 4. Termination condition (frozen)

TERMINATE iff R(x)==x (fixpoint: the structure's output equals its
input) OR iterations >= 8 (safety cap). In this workload the fixpoint
is reached at iteration 4; the cap never fires. The cap exists so the
contract is total.

## 5. Workload specification (frozen)

Opaque identifiers. Relations: 201 (chain), 202 (measure), 203
(subject-marker, distractor), 204 (distractor measure). Entities:
1001..1005 (chain nodes), 1101/1102 (measure targets / distractor
subjects), 1201..1203 (distractor entities). All positive, disjoint
from the -2 miss sentinel and from small count values (counts are
1..3; no count value equals any entity id).

Facts (setup_cyc, straight-line fact_add calls):
- Chain: (1001,201,1002) (1002,201,1003) (1003,201,1004) (1004,201,1005)
- Measure: (1001,202,1101) (1001,202,1102) -> count 2
            (1002,202,1103) -> count 1
            (1003,202,1104) (1003,202,1105) (1003,202,1106) -> count 3
            (1004,202,1107) -> count 1
            (1005,202,1108) (1005,202,1109) -> count 2
- Subject-marker: (1101,203,1102)  [makes 1101 a subject, kind 1]
- Distractor: (1201,204,1202) (1201,204,1203) -> count 2

MAPs (map_new + teach; teach observes only on exact match):
- MAP 0: class 4 STEP on rel 201. teach: (0,1001,1002) (0,1002,1003)
  (0,1003,1004) (0,1004,1005) (0,1005,1005) [fixpoint teach: at chain
  end STEP returns its input]. Contract: in{1} out{1}.
- MAP 1: class 1 COUNT on rel 202. teach: (1,1001,2) (1,1002,1)
  (1,1003,3) (1,1004,1) (1,1005,2). Contract: in{1} out{2}.
- MAP 2: class 3 IDENT. teach: (2,1101,1101). Contract: in{1} out{1}.
- MAP 3: class 1 COUNT on rel 204. teach: (3,1201,2).
  Contract: in{1} out{2}.

Class 4 STEP semantics (the sole addition to the base, Section 7):
one hop along rel; if no outgoing edge exists, return the input
unchanged (fixpoint identity).

Query (driver main, one call): uni_solve(A,B,c, s=1001, kin=1, kout=1,
exp=1005, nm=4). Then uni_report "UNI"/"QC", uni_census, o_flush.

### 5.1 Predicted U run-through (frozen; the depth-2 bound)

Singles (admitted by kind filter kin=1,kout=1): MAP 0 -> 1002 (!=1005);
MAP 2 -> 1101 (!=1005). MAP 1, MAP 3 rejected (out{2}).
Admitted pairs (x!=y): (0,2): 1002 -> IDENT -> 1002. (2,0): 1001 ->
IDENT -> 1001 -> STEP -> 1002. All other 10 pairs filter-rejected
(kind mismatch: every (1,*) and (3,*) pair fails the middle/out
kind check; (0,1),(0,3),(2,1),(2,3) fail the out-kind check).
WIDEN=1 retries the 10 rejected pairs once:
(0,1)->1; (0,3)->-2; (1,0)->2; (1,2)->2; (1,3)->-2; (2,1)->2;
(2,3)->-2; (3,0)->-2; (3,1)->-2; (3,2)->-2. None equals 1005.
Predicted outcome: found=0, ANS=-2, TRIES=14 (2 admitted singles +
2 admitted pairs + 10 widened pairs). No contract observations are
recorded (observe fires only on success).

## 6. Assembly, build, run (frozen)

- `sed '/^fn main/,$d' ref_uc_uni.zag > uni_nomain.zag`
- `cat cyc_base.zag uni_nomain.zag cyc_new.zag > cyc_full.zag`
- Region audits: each concatenated region must cmp byte-identical to
  its source (head/tail -c by recorded byte sizes).
- Compile with pinned safebin znc (`znc cyc_full.zag -o cyc_bin`);
  run the binary 3x; sha256 each run; outputs to cyc_run1/2/3.txt.
- The driver performs NO iteration: C5 audits this mechanically.

## 7. cyc_base.zag construction (frozen)

`cp ref_uc_base.zag cyc_base.zag`, then exactly three edits:
(a) header class comment gains "4=STEP (one hop; identity at fixpoint)";
(b) new fn stepf after count_rel (single-hop scan; returns input when
no outgoing edge; same break idiom as walkf);
(c) one branch in exec_map: `if(cl==4){ return stepf(A,s,r1); }`
after the cl==3 line.
Arena offsets, fact layout, MAP table, teaching, and classes 0-3 are
untouched. C4 audits the diff.

## 8. Frozen predictions

- P1: `diff ref_uc_base.zag cyc_base.zag` shows exactly the three
  edits of Section 7 (C4).
- P2: 3/3 runs pairwise byte-identical (C2).
- P3: output contains "ANS=-2" on the UNI report line, "WIDEN=1"
  present, TRIES=14 (C3) -- U's trial space contains no cycle
  solution, exactly per the Section 5.1 enumeration.
- P4: driver contains zero `exec_map` calls and zero `while` loops
  (C5) -- the cycle is posed purely as data + one query; the driver
  does not implement iteration.

## 9. Frozen kill bars

- C1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md + NAMECHECK.md
  Steps 0-2 ONLY) strictly precedes all implementation commits
  (git log order self-check).
- C2 DETERMINISM: PASS iff 3/3 runs are pairwise byte-identical (cmp);
  digests recorded.
- C3 U-BOUNDARY: PASS iff the UNI report line shows ANS=-2 (found=0),
  matching the frozen Section 5.1 enumeration. (A finding of ANS=1005
  is NOT a pass of this bar; see verdict mapping.)
- C4 BASE-DIFF: PASS iff `diff ref_uc_base.zag cyc_base.zag` shows
  exactly the Section 7 edits and nothing else.
- C5 NO-CYCLE-HANDLER: PASS iff `grep -c exec_map cyc_new.zag` == 0
  AND `grep -c while cyc_new.zag` == 0.
- C6 OPACITY: PASS iff grep over all built sources
  (`cyc_base.zag`, `cyc_new.zag`, `uni_nomain.zag`) for the banned
  domain-story tokens
  `hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent`
  (case-insensitive) returns empty, AND every exercised identifier is
  a bare integer (no alphabetic entity/relation names).

## 10. Verdict mapping (frozen)

- C1 FAIL -> VOID. Commit order broken; re-freeze, do not hand-tune.
- C2 FAIL -> UNDECIDED. Name the decisive rerun.
- C3/C4/C5/C6 PASS (with C1, C2 PASS) -> verdict INFORMATIVE-FAIL (U):
  U cannot compose cycles. The boundary is precise: U's execution rule
  is a bounded depth-2 pipeline trial with no re-application and no
  termination vocabulary; a 4-deep fixpoint iteration is outside its
  proposal space by construction. REPORT characterizes the boundary
  and states the general-principle direction (Section 11); no new
  principle is implemented in this lane.
- C3 shows ANS=1005 -> verdict PASS (unexpected): U solved the cycle
  workload. REPORT must identify the exact trial that produced it; if
  the Section 5.1 enumeration missed a depth-2 route to 1005, the
  battery is VOID for its intended purpose (disclose the flaw, do not
  claim a cycle result).
- C4/C5/C6 FAIL -> VOID. Implementation deviated from prereg.

## 11. General-principle direction (NOT implemented; preregistered for a follow-up battery)

If C3 holds, the missing principle must be GENERAL, never a cycle
handler. Preregistered shape: generalize U's "ordered trial" from
{singles, ordered pairs, each applied once} to TRIAL OVER
RE-APPLICABLE STRUCTURE SEQUENCES WITH LEARNED HALTING --
a proposed sequence (repetitions allowed) is executed stepwise; after
each step a halting condition is checked; halting is expressed in the
existing contract vocabulary (output-kind includes a HALT signal, or
output==input fixpoint, or a step cap); end-to-end verification is
retained. Pipelines are the special case (halt after one pass); cycles
are sequences with data-dependent halt; this also covers DAG re-use
(revisit a structure after fan-in). It reduces to U exactly when
sequences are restricted to length <= 2 with halt-after-once, so it is
a strict generalization, not a parallel engine. A follow-up worker may
preregister and test this; this lane only establishes the boundary.

## 12. Honest boundaries (pre-declared)

- Tests U only. GEN has no implementation (Section 2).
- One cycle family (fixpoint iteration on a 4-chain, M1-M5). Oscillatory
  cycles, convergent-signal cycles, and multi-structure feedback cycles
  are NOT tested.
- The oracle answer exp is supplied to uni_solve for end-to-end
  verification, exactly as in the P6 battery. The test targets U's
  PROPOSAL space (can it propose a cycle solution?), not discovery of
  exp from scratch.
- STEP-at-fixpoint identity (return input when no outgoing edge) is
  stipulated in the world and taught; it is the termination signal a
  general principle would need to learn to use.
- Section 11 is a direction, not a claim; it is not implemented or
  tested here.
- Behavior classes 0-3 and the -2 sentinel keep their canonical
  semantics; the kind labels 1/2 keep theirs (no polarity swap in this
  battery).
