# PREREG: L2-EXTENDN-2 Revision Mid-Iteration

Status: FROZEN. Committed before any implementation. Any change
requires a fresh preregistration, never an amendment-in-place.

## 1. Hypothesis

A learner running iterative extension (C301, ledger C301) can
survive the world changing mid-iteration. After the learner has
completed 2 extensions toward a 6-link chain, the world kills the
licensing fact on the only remaining frontier path (the learner is
not told). The learner must then, by its own machinery:

- detect the dead frontier plan via a stale check (the fact it
  committed to for the next step is superseded),
- promote NOTHING through the dead fact,
- either re-route through a live alternative frontier fact and
  complete the 6-link chain (R1), or terminate cleanly with
  EXECFAIL, reporting its partial chain honestly (R2).

This fuses the iterative-extension operator with the revision
machinery (commit a plan, observe a violation, revise) and
exercises the EXECFAIL stop that C301 left untested. The number
of extensions, the re-route decision, and the stop are all
learner-decided. No paired training examples. 0 new edge/MAP
types, opcodes, modes, bridges, handlers, semantic cases.

## 2. Operator design (EXTEND-REV)

Frozen sources reused byte-identical (sha256 audited in K7):
cc_base.zag, un_patch.zag, adapt_patch.zag, copied from
docs/lab/research-lead/overnight-20260928/l2_extend_iterative/
(which verified them against composition_integration/).

New cognition file: rv_patch.zag (written fresh for this lane;
same substrate pattern as C301, no blind copying).

2.1 Plan commitment (learner-owned). After selecting its starting
MAP and after every successful extension, the learner commits to
the next step's licenser: the lowest-id live FACT with
subject == frontier, relation != -999, not superseded
(rv_lic_fact; same selection rule as C301's extn_lic_fact). This
is ordinary next-step planning from current observations. The
committed plan is emitted (EXTN-PLAN).

2.2 World dynamics (disclosed researcher scaffold, not
cognition). After each successful extension the loop calls
rv_world_step(W, ext, plan): when ext == 2 and plan >= 0, the
world kills the committed plan via a type-3 self-loop edge
(link_edge(W, plan, 3, plan, 0)), which is exactly what the
frozen is_superseded checks. The world kills the fact the
learner planned to use next; the learner is not told. The kill
is emitted as WORLD-KILL (world event, not learner knowledge).

2.3 Stale check and revision (learner-owned). At the top of each
iteration, before any assembly, the learner checks its committed
plan: if is_superseded(plan) == 1, it emits EXTN-REVISION with
the died fact id and its (s,r,o), discards the plan, and
re-scans the frontier:
  - a live fact is found: emit EXTN-REROUTE with the new fact id
    and (s,r,o); proceed to extend through it (the re-route
    decision is the learner's: a live licenser exists).
  - none found: STOP with reason EXECFAIL. The committed
    extension is unexecutable and nothing live replaces it; the
    learner terminates cleanly and reports its best verified
    terminal. Nothing is promoted through the dead fact.

2.4 Guarded step (rv_step). The extension step takes the
committed (or re-routed) plan directly instead of re-scanning,
and asserts is_superseded(plan) == 0 at entry: a dead plan can
never reach assembly or promotion (rc = EXECFAIL). Remaining
logic mirrors C301: DUP check via adapt_relseq_absent, assemble
with t2_asm_chain, execution-verify with t2_exec, promote with
adapt_promote (teaches no fact), link type-16 adapted-from to
the parent. No new edge types.

2.5 Loop (rv_extend_iter). No count parameter anywhere.
out[0] = extensions, out[1] = stop reason (0 TERM, 1
NOFRONTIER, 2 EXECFAIL, 3 BUDGET), out[2] = final MAP id,
out[3] = died fact id or -1, out[4] = replacement fact id or -1.
Stopping rules, all learner-owned: TERM (predicted terminal
reached), NOFRONTIER (no live fact at frontier), EXECFAIL
(committed extension unexecutable; includes the revised
dead-end), BUDGET (safety cap, disclosed, never reached).

2.6 Controls and ablation live in the driver / a labeled scaffold
section of rv_patch.zag, clearly marked, NOT part of the
claimed operator:
  - C1 NO-STALE: rv_extend_iter_nostale, identical loop except
    the stale check (2.3) and the rv_step entry guard are
    removed; the committed plan is used blindly via
    rv_step_blind. Expected to promote the broken extension
    through the dead fact (proving detection did the work).
  - C2 FRESH: no native MAP taught; the frozen generic miss
    policy t2_trial is the only tool.

## 3. World spec and hand derivation

World facts, taught in this order via ev_teach (R1; R2 omits
fact 7):

  1. (101,1,102)  2. (102,1,103)  3. (103,1,104)
  4. (104,2,105)  5. (105,2,106)
  6. (106,2,107)   [kill target: taught before fact 7, lower id]
  7. (106,3,107)   [R1 only: alternative frontier fact]
  8. (201,1,102)... no: distractors (201,1,202) (202,1,203)
     (301,9,309), off-frontier.

Native MAP m (taught in every arm except C2): relation sequence
[1,1,1], plen 3, assembled from facts 1-3. Hand derivation of
its terminal from s=101:
  101 -1-> 102 -1-> 103 -1-> 104. Terminal = 104.

The learner commits its initial plan at frontier 104: lowest-id
live fact with subject 104 is fact 4, (104,2,105).

Arm R1 (revision with re-route; query s=101, goal=107):
  ext 1: plan fact 4 (104,2,105); new chain [1,1,1,2], values
    101,102,103,104,105; term 105 != 107. Commit plan at 105:
    fact 5 (105,2,106). World: ext=1, no kill.
  ext 2: plan fact 5 (105,2,106); new chain [1,1,1,2,2];
    term 106 != 107. Commit plan at 106: lowest-id live fact
    with subject 106 is fact 6 (106,2,107) [fact 7 has higher
    id]. World: ext=2, kills fact 6 (type-3 self-loop).
  ext 3 attempt: stale check on fact 6: superseded == 1.
    EXTN-REVISION died=fact6 (106,2,107). Re-scan frontier 106:
    lowest-id live fact is fact 7 (106,3,107). EXTN-REROUTE
    new=fact7. Extend: rnew=3, vnext=107; new chain
    [1,1,1,2,2,3], values 101..107; term 107 == 107. STOP TERM.
  Expected: ans=107, ext=3, stop=TERM(0), died=fact6 id,
  repl=fact7 id, final relseq [1,1,1,2,2,3], 3 type-16 hops
  from final MAP to native m, ultimate ancestor == m.
  Detection latency: 1 iteration (kill lands inside iteration
  2's post-step world hook; detection fires at the start of
  iteration 3 before any assembly). Promotions through the dead
  fact before detection: 0.

Arm R2 (revision with clean stop; query s=101, goal=107; fact 7
absent):
  ext 1 and ext 2 identical to R1. World kills fact 6 after
  ext 2.
  ext 3 attempt: stale check on fact 6: superseded == 1.
    EXTN-REVISION died=fact6 (106,2,107). Re-scan frontier 106:
    no live fact. STOP EXECFAIL(2). Nothing promoted.
  Expected: ans=106, ext=2, stop=EXECFAIL(2), died=fact6 id,
  repl=-1, final relseq [1,1,1,2,2], 2 type-16 hops to m,
  ultimate ancestor == m, exactly 2 adapted MAPs promoted
  (ext 1, ext 2), every licensing fact of every promoted MAP
  live.

Arm C1 (no-stale control; R1 world; query s=101, goal=107):
  ext 1, ext 2 identical; world kills fact 6 after ext 2. The
  control skips the stale check and the step guard: it uses the
  dead plan fact 6 blindly. Assembly reads rnew=2, vnext=107
  from fact 6's intact fields; t2_exec verifies numerically
  (replay of dead values, the C295/I5 finding); it promotes
  [1,1,1,2,2,2] licensed by the superseded fact 6, links
  type-16, term 107 == 107, STOP TERM.
  Expected: ans=107, ext=3, stop=TERM(0), final relseq
  [1,1,1,2,2,2]; the no-broken-promotion audit FAILS on the
  final MAP (one licensing fact superseded). This is the
  derived behavior: without detection the learner promotes
  through the dead fact.

Arm C2 (fresh learner; R1 world; NO m):
  t2_trial: gather caps at 4-link paths from 101 (101..105);
  none reaches 107; per-relation count trials and single-link
  paths fail. Expected: -2, as in C301 C2 (the extra fact 7
  sits beyond the 4-link gather horizon).

Stop reason codes: TERM=0, NOFRONTIER=1, EXECFAIL=2, BUDGET=3.

## 4. Kill bars (frozen)

- K1: R1 exact: ans=107, ext=3, stop=TERM, final relseq
  [1,1,1,2,2,3] (white-box cc_relseq), 3 type-16 hops to native
  m, ultimate ancestor == m, out[3] is the killed (106,2,107)
  fact and is_superseded(out[3])==1, out[4] is the live
  (106,3,107) fact with is_superseded(out[4])==0. Detection
  latency 1 iteration, 0 promotions through the dead fact.
- K2: R2 exact: ans=106, ext=2, stop=EXECFAIL, final relseq
  [1,1,1,2,2], 2 type-16 hops to m, ultimate ancestor == m,
  out[3] is the killed (106,2,107) fact (superseded), out[4]==-1,
  exactly 2 adapted MAPs promoted, no licensing fact of any
  promoted MAP superseded.
- K3: C1 no-stale control behaves as derived: ans=107, ext=3,
  stop=TERM, final relseq [1,1,1,2,2,2], and the final MAP has
  a superseded licensing fact (broken promotion demonstrated;
  proves the stale check did the work in R1).
- K4: C2 fresh learner: t2_trial returns -2.
- K5: no-broken-promotion audit on R1: every adapted MAP on the
  type-16 provenance chain (final plus ancestors) has all
  licensing facts live (is_superseded==0 on every fid from
  cc_satisfy), and t2_exec of each MAP's root from s=101 equals
  that MAP's terminal (final: 107). Replay of dead values
  would be a FAIL per the C295/I5 finding.
- K6: 3/3 runs byte-identical; sha256 digests recorded and
  pairwise cmp clean; binary exit 0.
- K7: 0 new machinery: 0 new edge types, 0 new opcodes, 0
  modes, 0 bridges, 0 handlers, 0 new semantic cases, 0 new
  node tags. New code issues link_edge only with type 16
  (operator provenance) and type 3 (world-kill self-loop,
  disclosed world scaffold reusing the frozen supersede
  semantic). Frozen sources sha256-identical to origins;
  origins unmodified.
- K8: white-box trace: every extension emits parent id, new
  id, plen, licensing fact (s,r,o), terminal; every plan commit
  emits the fact id and (s,r,o); the world kill emits the fact
  id and (s,r,o); the revision emits died fact id + (s,r,o)
  and replacement id + (s,r,o) or the clean stop. REPORT
  reproduces the full R1 and R2 traces.
- K9: prereg commit strictly precedes implementation; the
  prereg commit contains only PREREG.md and NAMECHECK.md
  (Step 0 guard).
- K10: hand-derived exact chains, terminals, and stop reasons
  for R1/R2/C1/C2 appear in section 3 with the arithmetic
  shown; the driver asserts every constant inline.

Verdict rule: BUILD-PASS iff K1-K10 all pass. Any fail is
reported as BUILD-FAIL with the failing bar named. VOID only
on toolchain or commit-order violation.

## 5. Run protocol

Build: cat cc_base.zag un_patch.zag adapt_patch.zag rv_patch.zag
rv_driver.zag > rv_full.zag; compile with the pinned znc to
rv_bin. One binary runs all four arms sequentially, each on a
fresh tnn2_init workspace. Run 3 times; record sha256 of each
output; pairwise cmp. Driver asserts every K1-K4 constant
inline and emits ARM <name> PASS/FAIL lines plus the K5 audit
lines.

## 6. Cognition accounting

Cognition lines = non-comment non-blank lines of rv_patch.zag
operator section (plan commitment, stale check + revision,
guarded step, loop, trace helpers). The world hook
(rv_world_step), the kill helper, the C1/C2 scaffold, the
audit helpers, and driver arms/world teaching/native MAP
teaching are disclosed researcher scaffold, not cognition.
