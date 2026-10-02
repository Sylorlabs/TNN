# PREREG: L2-EXTENDN-1 Iterative Extension Operator

Status: FROZEN. Committed before any implementation. Any change
requires a fresh preregistration, never an amendment-in-place.

## 1. Hypothesis

A learner that holds a native MAP m (relation sequence [1,1,1],
plen 3) can reach a 6-link target chain [1,1,1,2,2,2] with NO
paired training example for the target, by ITERATIVELY extending
m: extend once licensed by a real frontier fact, detect the result
still falls short of the predicted terminal, extend again from the
new frontier, and stop by a learner-owned stopping rule. The
number of extensions is decided by the learner loop, never set by
the researcher per problem. This closes the carry-forward from
H-COMPINTEG-1 (ledger C295): frozen EXTEND-ONE extends by exactly
one link and retires trials, so chains never accumulate.

## 2. Operator design (EXTEND-ITER)

Frozen sources reused byte-identical (sha256 audited in K8):
cc_base.zag, un_patch.zag, adapt_patch.zag from
docs/lab/research-lead/overnight-20260928/composition_integration/.

New cognition file: extn_patch.zag.

2.1 Starting MAP selection (learner-owned). extn_best_native(W,s)
scans all live MAP nodes with NO outgoing type-16 edge (native),
extracts each relation sequence with cc_relseq, keeps those fully
satisfiable from s via cc_satisfy, and returns the longest one
(ties: lowest node id). The operator is never told the MAP id.

2.2 One extension step (extn_step). Given the current MAP with
chain description (relse q[0..L-1], values v[0..L], licensing fact
ids f[0..L-1]):
  a. frontier F = v[L].
  b. Scan the fact store for the lowest-id live FACT node with
     subject == F, relation != -999, not superseded. If none,
     return NOFRONTIER.
  c. Skip if a live MAP already carries relseq q ++ [rnew]
     (adapt_relseq_absent, reused from adapt_patch).
  d. Assemble the extended chain with t2_asm_chain over
     v[0..L] ++ [vnext] licensed by f[0..L-1] ++ [fn2].
  e. Execution-verify: t2_exec(root, s) must equal vnext, else
     EXECFAIL.
  f. Promote with adapt_promote (reused; teaches NO fact, per the
     adapt_patch invariant: scaffolding is not a query answer),
     then link_edge(am, 16, parent, 0): each extension links to
     its parent via type-16 adapted-from. No new edge types.

2.3 Iteration loop (extn_extend_iter). No count parameter anywhere.
  - m_cur = extn_best_native(W,s); derive its chain; term = v[L].
  - LOOP:
    - If term == expected: STOP with reason TERM. The query's
      target value is the learner's prediction basis; the learner
      was never told the path, only the goal value.
    - If extensions >= 8: STOP with reason BUDGET (learner safety
      cap, disclosed; never reached in the frozen arms).
    - am = extn_step(...). If it fails: STOP with that reason
      (NOFRONTIER / EXECFAIL / DUP).
    - Else re-derive the chain of am (cc_relseq + cc_satisfy from
      s), term = new terminal, extensions += 1, emit the trace
      line, continue.
  - Answer = best terminal reached (== expected on TERM stops).

2.4 Stopping rules (all learner-owned, evaluated inside the loop):
TERM (extension reached the predicted terminal), NOFRONTIER (no
licensing fact exists at the frontier), EXECFAIL (extended chain
does not execute to the licensed value), BUDGET (safety cap).

2.5 Controls and ablation live in the driver / a separate scaffold
section of extn_patch.zag, clearly labeled, and are NOT part of
the claimed operator:
  - C1 EXTEND-ONE: calls the FROZEN adapt_extend (single pass over
    native MAPs; adapted MAPs are not re-extended), then answers
    the longest satisfiable chain or -3.
  - C2 FRESH: no native MAP taught; the frozen generic miss policy
    t2_trial is the only tool.
  - A1 NO-RULE: extn_extend_iter_norule, identical to the operator
    except the TERM check is removed (NOFRONTIER/EXECFAIL/BUDGET
    remain so it still terminates).

## 3. World spec and hand derivation

World facts, taught in this order via ev_teach (values chosen so
every frontier below is unambiguous; distractors never sit on a
frontier):

  (101,1,102) (102,1,103) (103,1,104)
  (104,2,105) (105,2,106) (106,2,107)
  (107,2,108)   [decoy: licenses overshoot past the E1/E2 goal]
  (201,1,202) (202,1,203) (301,9,309)   [distractors, off-frontier]

E3 world: identical except (105,2,106) is NOT taught.

Native MAP m (taught in every arm except C2): relation sequence
[1,1,1], plen 3, assembled from the first three facts. Hand
derivation of its terminal from s=101:
  101 -1-> 102 -1-> 103 -1-> 104. Terminal = 104.

Arm E1 (need-6, query s=101, goal=107):
  start term 104 != 107.
  ext 1: frontier 104, licensing fact (104,2,105); new chain
    [1,1,1,2], values 101,102,103,104,105; term 105 != 107.
  ext 2: frontier 105, licensing fact (105,2,106); new chain
    [1,1,1,2,2]; term 106 != 107.
  ext 3: frontier 106, licensing fact (106,2,107); new chain
    [1,1,1,2,2,2]; term 107 == 107. STOP TERM.
  Expected: ans=107, extensions=3, stop=TERM,
  final relseq [1,1,1,2,2,2], type-16 hops from final MAP to the
  native m = 3.

Arm E2 (need-5, query s=101, goal=106):
  ext 1 -> [1,1,1,2], term 105 != 106.
  ext 2 -> [1,1,1,2,2], term 106 == 106. STOP TERM.
  Expected: ans=106, extensions=2, stop=TERM,
  final relseq [1,1,1,2,2].

Arm E3 (need-6, missing middle fact, query s=101, goal=107):
  ext 1 -> [1,1,1,2], term 105 != 107. Frontier 105: no live fact
  with subject 105 exists. STOP NOFRONTIER.
  Expected: ans=105, extensions=1, stop=NOFRONTIER,
  final relseq [1,1,1,2].

Arm C1 (EXTEND-ONE control, need-6, query s=101, goal=107):
  Frozen adapt_extend promotes exactly one adapted MAP [1,1,1,2]
  (frontier 104, fact (104,2,105); execution verifies 105==105).
  Adapted MAPs are not re-extended. Longest satisfiable chain
  terminates at 105 != 107. Expected: ans=-3 (fail), exactly 1
  adapted MAP promoted. This reproduces the C295/K1 failure and
  proves iteration did the work in E1.

Arm C2 (fresh learner, need-6, query s=101, goal=107, NO m):
  t2_trial: t2_gather collects paths of at most 4 links from 101
  (101..105); none reaches 107; per-relation count trials yield 3
  (relation 1) and fail; single-link paths fail. Expected: -2.
  The generic frozen miss policy cannot bridge the 6-link gap
  from scratch.

Arm A1 (no-TERM-rule ablation, need-6, query s=101, goal=107):
  ext 1 -> 105, ext 2 -> 106, ext 3 -> 107, then WITHOUT the TERM
  check the loop continues: frontier 107 has the decoy fact
  (107,2,108): ext 4 -> [1,1,1,2,2,2,2], term 108. Frontier 108:
  no fact. STOP NOFRONTIER.
  Expected: ans=108 (WRONG vs goal 107), extensions=4,
  stop=NOFRONTIER, final relseq [1,1,1,2,2,2,2]. Runaway overshoot
  proves the TERM stopping rule is load-bearing.

Stop reason codes: TERM=0, NOFRONTIER=1, EXECFAIL=2, BUDGET=3.

## 4. Kill bars (frozen)

- K1: E1 exact: ans=107, ext=3, stop=TERM, final relseq
  [1,1,1,2,2,2] (cc_relseq white-box), 3 type-16 hops to native m.
- K2: E2 exact: ans=106, ext=2, stop=TERM, final relseq
  [1,1,1,2,2]. K1+K2: extension counts 3 vs 2 are learner-decided;
  no count parameter exists in the operator.
- K3: E3 exact: ans=105, ext=1, stop=NOFRONTIER, final relseq
  [1,1,1,2].
- K4: C1 fails as derived: ans=-3, exactly 1 adapted MAP.
- K5: C2 fails as derived: t2_trial returns -2.
- K6: A1 overshoots as derived: ans=108, ext=4, stop=NOFRONTIER.
- K7: 3/3 runs byte-identical; sha256 digests recorded and
  pairwise cmp clean.
- K8: 0 new machinery: 0 new edge types, 0 new opcodes, 0 modes,
  0 bridges, 0 handlers, 0 new semantic cases; only type-16 reuse.
  Frozen sources sha256-identical to origins; origins unmodified.
- K9: white-box trace: every extension step emits parent id, new
  id, plen, licensing fact (s,r,o), terminal; REPORT reproduces the
  full trace for E1.
- K10: prereg commit strictly precedes implementation; the prereg
  commit contains only PREREG.md and NAMECHECK.md (Step 0).

Verdict rule: BUILD-PASS iff K1-K10 all pass. Any fail is reported
as BUILD-FAIL with the failing bar named. VOID only on toolchain
or commit-order violation.

## 5. Run protocol

Build: cat cc_base.zag un_patch.zag adapt_patch.zag extn_patch.zag
extn_driver.zag > extn_full.zag; compile with the pinned znc to
extn_bin. One binary runs all six arms sequentially, each on a
fresh tnn2_init workspace. Run 3 times; record sha256 of each
output; pairwise cmp. Driver asserts every K1-K6 constant inline
and emits ARM <name> PASS/FAIL lines.

## 6. Cognition accounting

Cognition lines = non-comment non-blank lines of extn_patch.zag
operator section (selection, step, loop, trace helpers). Driver
arms, world teaching, native MAP teaching, and the C1/C2/A1
scaffold are disclosed researcher scaffold, not cognition.
