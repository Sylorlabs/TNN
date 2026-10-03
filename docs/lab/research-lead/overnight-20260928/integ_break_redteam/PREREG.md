# PREREG: INTEG-BREAK RED TEAM (H-COMPINTEG-1 carry forwards)

Status: FROZEN. Parent mandate: red team the three integration breaks
reported in H-COMPINTEG-1 (ledger C295, verdict
COMPOSITION-INTEGRATION-INCOMPLETE). This prereg freezes the attack
designs, kill bars, guard proposals, and control batteries BEFORE any
attack implementation is written. Commit order: this file plus
NAMECHECK.md (Step 0) committed ALONE first.

Source: docs/lab/research-lead/overnight-20260928/composition_integration/REPORT.md
(C295). Frozen operator sources under test (pristine copies, sha256
recorded in NAMECHECK.md Step 3, matching the C295 report):
cc_base.zag, un_patch.zag, adapt_patch.zag, revise_patch.zag,
ts_patch.zag, lvcomp_patch.zag, integ_patch.zag.

Working directory: docs/lab/research-lead/overnight-20260928/integ_break_redteam/

## 1. Targets (from C295 findings)

T1. SELF-REFERENTIAL FACT SUBSTITUTION (K3). ts_specialize_src treats
learner FACT nodes (field 0 == 1) as alternative-relation candidates:
any live non-superseded fact with field 20 == vj and field 24 != rj.
The learner's own reified predictions (taught via the learner-internal
ev_teach_in channel, e.g. FACT(11,71,14)) are substituted as if they
were world relations, creating self-referential trials ([71] -> 14,
later [74] trials from self-taught FACTs). The observation stream
alternates so the genuine FACT never reaches score 3.

T2. CIRCULAR SELF-VERIFICATION (K5). The stale-revision path was
short-circuited: lv_dfs found a [70] self-referential MAP built from
the learner's own FACT(101,70,105), lv_verify_chain checked the stale
prediction (105) against execution of that same-belief structure
(105 == 105), and promote_graph entrenched it (MAP_Z LINK14, another
learner FACT taught). The learner confirmed its own stale belief
using a structure derived from that same belief.

T3. VALUE-REPLAY VS LIVE-FACT EXECUTION GAP (I5, diagnostic).
t2_exec executes the assembled graph whose 902 literal nodes bake the
construction-time values; it does not re-derive through live facts.
A teach-then-kill fact change is invisible: the stale trial still
executes to the old value. integ_patch.zag documents integ_explore
as executing "through live world facts", which the implementation
does not do.

## 2. Method

Two binaries, both pure Zag via the pinned znc, both built by
rt_build.sh under the safebin PATH:

(a) rt_bin (attack): pristine frozen sources (byte-identical copies)
plus rt_attack.zag driver. Demonstrates each pathology minimally.
Zero source modifications.

(b) rt_guard_bin (guard test): guarded COPIES of three sources
(cc_base_g.zag, ts_patch_g.zag, lvcomp_patch_g.zag; diffs recorded
in REPORT.md) plus rt_guardtest.zag driver. Tests each proposed
learner-side guard and a control battery. Guarded copies live only
in this lane; the composition_integration sources are never modified.

Each binary runs 3x; byte-identical stdout required (RT-K6).
Determinism: the substrate allocates node ids deterministically for
a fixed operation order; all scenarios use fixed orders.

Verdict scale per target: PATHOLOGY-CONFIRMED (all ATTACK bars pass,
3/3 deterministic) or ATTACK-FAILED (any ATTACK bar fails; the trace
is reported, no reinterpretation, no salvage). Guard outcome per
target: GUARD-PASS or GUARD-FAIL against the frozen guard bars.
No global L3-style claim is made.

Hand-derivation risk: if a scenario's hand derivation is wrong, the
arm reports ATTACK-FAILED with its white-box trace. Bars are never
weakened to force a pass.

## 3. T1 attack design

### T1-A1: mechanism repro (minimal)
Fresh workspace W, tnn2_init.
- F1 = ev_teach(W,11,1,12); F2 = ev_teach(W,12,2,99). (world channel)
- FL = ev_teach_in(W,11,71,14). (learner-internal channel; simulates
  the self-taught shortcut of C295 I6)
- MAP_X: root = t2_asm_chain(W, v=[11,12,99], plen=3, f=[F1,F2]);
  node m: tag 20, f4=74, f8=11, f12=-1, f20=root, f36=1 (native: no
  outgoing type-16 edge). cc_relseq(W,m) = [1,2]; cc_satisfy(W,m,11)
  fully satisfied with licensing [F1,F2].
- n = ts_specialize_src(W,m,11,0,m).
- White-box assertions: n >= 1; there exists a live MAP x with
  cc_relseq(W,x) == [71]; x carries an ET_DEP (type-1) edge to FL.
T1-A1 SUCCEEDS iff all three hold, 3/3 runs byte-identical.

Rationale: at link j=0 (vj=11, rj=1), FL satisfies the candidate
filter (live, tag 1, s=11, r=71 != 1, not -999, not superseded), so
the operator builds the [71] trial licensed by the learner's own
fact and adapt_promote keeps it (t2_try_verify: 14 == 14).

### T1-A2: characterization matrix (conditions)
Same harness as T1-A1, five variants (fresh workspace each):
- C1 control: alternative fact via ev_teach(W,11,71,14) (world).
  Expect: [71] trial created.
- C2 attack: alternative fact via ev_teach_in(W,11,71,14) (learner).
  Expect: [71] trial created (indistinguishable from C1: the
  operator has no provenance signal; this IS the pathology).
- C3: learner fact ev_teach_in(W,11,1,50) (same relation as rj).
  Expect: no trial (filter requires r_alt != rj).
- C4: learner fact ev_teach_in(W,11,71,14), then supersede via
  link_edge(W,FL,3,FL,0). Expect: no trial (superseded excluded).
- C5: learner fact ev_teach_in(W,11,71,14), then ns(W,FL,36,0).
  Expect: no trial (dead facts excluded).
T1-A2 SUCCEEDS iff all five outcomes match, 3/3 runs.

### T1-A3: end-to-end pollution (I6 mechanism, minimal)
Fresh W. World: (11,1,12),(12,2,99) via ev_teach; world alternative
(11,3,12) via ev_teach (gives the genuine [3,2] -> 99 trial);
learner shortcut FL = ev_teach_in(W,11,71,14); native MAP_X [1,2]
as in T1-A1. Then 4 cycles of integ_explore(W,11,74,3,0)
(op=3 specialize, retire=0): each cycle adapts, executes kind-3
trials, lv_predict(11,74), lv_observe(11,74,v).
- Assertions: (a) a live [71]-relseq MAP exists whose ET_DEP
  licensing includes FL (self-referential trial created);
  (b) id_fact_score(W,11,74,99) < 3 after 4 cycles (the genuine
  FACT is starved by the alternating 14/99 observation stream);
  (c) trace shows a [74]-relseq trial emerging in a later cycle
  (self-taught FACT(11,74,14) re-substituted; recorded, not gating).
T1-A3 SUCCEEDS iff (a) and (b) hold, 3/3 runs.

T1-ATTACK SUCCEEDS iff T1-A1 and T1-A2 and T1-A3 succeed.

### T1 guard proposal (GUARD-T1)
Learner-side provenance gate in ts_specialize_src (guarded copy
ts_patch_g.zag): skip candidate fact fn2 when it is
learner-originated. Provenance bit: fact field 44.
- cc_base_g.zag: ev_teach_in sets ns(W,n,44,1) (learner-internal
  teach channel); ev_teach leaves 44 = 0 (world channel).
- ts_patch_g.zag: the candidate filter gains
  "and ng(W,fn2,44) != 1".
Channel discipline assumed (documented): in this design the world
teaches through ev_teach and the learner reifies through
ev_teach_in (lv_observe, promote_graph). If a deployment routes
genuine world observations through ev_teach_in, the bit must be
caller-supplied; the assumption is recorded, not smuggled.

Bootstrapping question, answered by design: a learned shortcut is
reusable as an alternative relation ONLY after independent world
confirmation, i.e. when a world-channeled fact (44 == 0) carries the
same (s,r,o). The guard preserves exactly that case.

### T1 guard bars (guard binary)
- T1-G1: scenario T1-A1 under guard: ts_specialize_src returns 0
  for the learner-fact substitution (no [71] MAP created).
  Scenario C6: FL = ev_teach_in(W,11,71,14) then world confirmation
  FW = ev_teach(W,11,71,14): [71] trial IS created and its ET_DEP
  licensing is FW (44 == 0), not FL. GUARD-PASS iff both hold.
- T1-G2 control battery: T1-A3 setup MINUS the learner shortcut
  (only the world alternative (11,3,12)): 4 cycles of
  integ_explore(W,11,74,3,0); assert a [3,2]-licensed trial exists
  with world-only licensing AND id_fact_score(W,11,74,99) == 3.
  GUARD-PASS iff both hold (legitimate specialization survives).

## 4. T2 attack design

### T2-A1: confident-wrong via circular verification
Fresh W, tnn2_init.
- World v1: A = ev_teach(W,201,1,202); B = ev_teach(W,202,2,209).
  (world truth for the [1,2] path: 209)
- Native MAP_X: t2_asm_chain(v=[201,202,209], f=[A,B]), tag 20,
  f4=70, live, native.
- Learner belief: F_stale = ev_teach_in(W,201,70,209); then 3
  honest cycles lv_predict(201,70) / lv_observe(201,70,209)
  (world-consistent at the time) raising pred_score to 3.
- Circular MAP via the T1 mechanism (faithful, not hand-built):
  ts_specialize_src(W,MAP_X,201,0,MAP_X) creates the [70] trial at
  link j=0 (vj=201, rj=1; F_stale has s=201, r=70 != 1): m70,
  len-1 [70], ET_DEP -> F_stale, type-16 -> MAP_X, kind 3.
  Assert m70 exists with relseq [70] and DEP -> F_stale.
- World change (teach-then-kill): ns(W,B,36,0);
  C = ev_teach(W,201,1,202); D = ev_teach(W,202,2,205).
  (world truth is now 205; the learner belief 209 is stale)
- q1 = compose_integ(W,201,70,0,st).
  Hand derivation: lv_setup -> p=209, rel=3 (passes the reliability
  gate); lv_dfs finds m70 (un_satisfy via t2_lu_first(201,70) ->
  F_stale -> 209 == pred; MAP_X re-derives to 205, not terminal);
  integ_assemble rebuilds the graph licensed by F_stale;
  lv_verify_chain: 209 == 209 -> promote_graph -> MAP_Z with
  LINK14 -> m70 and a fresh FACT(201,70,209). Returns 209.
- Assertions: q1 == 209; hg(W,36) >= 3 at query time (record pred
  and rel in trace); MAP_Z exists with type-14 edge -> m70;
  live-world-fact derivation of (201,70) via the [1,2] path is 205
  (t2_lu_first(W,202,2) -> D, value 205), so 209 is world-wrong.
T2-A1 SUCCEEDS iff all hold, 3/3 runs byte-identical.

### T2-A2: entrenchment
Continuing the T2-A1 workspace:
- q2 = compose_integ(W,201,70,0,st). Assert q2 == 209 and a second
  promotion occurred whose LINK14 target is m70 (the circular
  structure is re-entrenched, not revised).
- Retire the circular MAP: ns(W,m70,36,0).
- q3 = compose_integ(W,201,70,0,st). Assert q3 == 209 via MAP_Z
  itself (the promoted copy now verifies the belief; entrenchment
  outlives the original circular structure). Record type-15
  edge count workspace-wide for the report (0 on the
  single-segment path: integ_assemble writes co-use only for
  g >= 1; the entrenchment vector here is promotion + LINK14 +
  future-candidate bias, reported honestly).
T2-A2 SUCCEEDS iff q2 == 209 with re-promotion LINK14 -> m70 and
q3 == 209 after m70 is retired, 3/3 runs.

T2-ATTACK SUCCEEDS iff T2-A1 and T2-A2 succeed.

### T2 guard proposal (GUARD-T2): self-license veto
Learner-owned circuit breaker in lv_verify_chain (guarded copy
lvcomp_patch_g.zag):
- lv_setup records the prediction's source struct id in hg(W,40)
  (header slot 40 is unused by all frozen sources; verified by
  grep census in NAMECHECK.md).
- lv_verify_chain, after v == hg(W,32): collect the verification
  graph's ET_DEP licensing fact ids by walking SETREG (tag 101)
  cells from the root (guard cells via field 12, set cells via
  ET_SEQ; unknown tags stop the walk, fail-open). VETO (return -2)
  iff the licensing set is non-empty AND every licensing fact id
  equals hg(W,40) AND the source struct is a learner-originated
  FACT (ng(W,hg(W,40),44) == 1).
Rationale: verification is vacuous when the only licensing evidence
is the learner's own reified prediction. The learner-origin
refinement preserves world-grounded degenerate verifications
(source fact 44 == 0): redundant but not vicious. Full lineage
(learner-taught descendants of the source) is future work, recorded
as a limitation; the veto covers the exact K5 degenerate case.

### T2 guard bars (guard binary)
- T2-G1: the T2-A1/A2 scenario under guard: q1 == -2 (clean
  reject), no MAP_Z promoted (newest MAP id unchanged across q1),
  q3 == -2 after m70 retired. GUARD-PASS iff all hold.
- T2-G2 control battery:
  (i) world-grounded degenerate: Wf = ev_teach(W,301,70,314);
  3 honest observe cycles -> score 3; [70] MAP licensed by Wf
  (built via ts_specialize_src on a [1,2] MAP_X as in T2-A1);
  compose_integ(W,301,70) must return 314 with MAP_Z promoted
  (refined guard does not fire: source 44 == 0).
  (ii) non-degenerate: world (401,1,402),(402,2,409); learner
  FACT(401,70,409) score 3 via honest observes; MAP_X [1,2]
  licensed by world facts; compose_integ(W,401,70) must return
  409 with MAP_Z promoted (licensing set != {source}).
  GUARD-PASS iff both controls pass.

## 5. T3 attack design (boundary determination)

### T3-A1: replay vs re-derive divergence, minimal
Fresh W. A = ev_teach(W,201,1,202); B = ev_teach(W,202,2,209).
MAP_X = t2_asm_chain(v=[201,202,209], f=[A,B]), tag 20, live.
Teach-then-kill: ns(W,B,36,0); D = ev_teach(W,202,2,205).
Assertions, all post-kill:
- (a) cc_relseq(W,MAP_X) == -1 (relseq read is DEP-sensitive: the
  killed licensing fact makes it unreadable).
- (b) un_satisfy(W,MAP_X,201,vbuf,fbuf) >= 1 with terminal value
  205 (the contract path re-derives through LIVE facts via
  t2_gather; t2_lu_first(W,202,2) returns D).
- (c) t2_exec(W,ng(W,MAP_X,20),201) == 209 (the assembled graph
  replays construction-time baked literals).
- (d) t2_lu_first(W,202,2) returns D (value 205): the fact store
  itself reflects the kill.
T3-A1 SUCCEEDS iff (a) and (b) and (c) and (d) hold: (b) vs (c) is
the exact execution gap, 3/3 runs byte-identical.

### T3 call-site census (static, part of the verdict)
Classify every t2_exec call site in the frozen integ_full.zag and
every live-fact re-derivation site:
- Replay (executes baked graph, kill-blind): cc_base:412
  (t2_exec def), :500 (t2_try_verify), :732 (ev_query trial),
  :1266 (self-test), integ :2916 (ts construct verify), :3078
  (lv_verify_chain), :3251 (integ_explore). All seven replay.
- Re-derive (consult live facts, kill-sensitive): t2_lu_first,
  cc_satisfy, un_satisfy (contract path), lv_predict (FACT scan),
  activate, cc_relseq (DEP-liveness).
The census is verified by grep during the build and recorded in
REPORT.md.

### T3 load-bearing analysis
Question: is replay load-bearing for any passing bar (I2/I4)?
Test in the guard binary (T3-G2): I2-equivalent and I4-equivalent
end-to-end runs through compose_integ with the liveness veto
active. If they pass unchanged, replay is incidental to those
bars, not load-bearing. The REPORT verdict then distinguishes:
substrate semantic bug (execute/t2_exec misbehaves) vs integration
modeling error (the layer's documented contract,
"executes ... through live world facts" in integ_patch.zag, is
violated by its implementation). The preregistered leaning, to be
confirmed or overturned by the census: the substrate contract
(compiled graph = frozen plan) is coherent; the error is the
integration layer treating t2_exec as a live belief probe while
never consulting the ET_DEP provenance the base already records.
Verdict recorded in REPORT.md against this bar.

### T3 guard proposal (GUARD-T3): licensing-liveness veto
In t2_exec (guarded copy cc_base_g.zag): before execute(), walk
the graph as in GUARD-T2, collecting ET_DEP licensing facts;
if any licensing fact has field 36 != 1 or is_superseded, return
-999999 (vetoed; all call sites already treat -999999 as
failure/withhold). Unknown graph shapes fail open (walk stops,
no veto) so count/sum graphs and the base self-test are unaffected.

### T3 guard bars (guard binary)
- T3-G1: the T3-A1 scenario under guard: t2_exec on the stale
  MAP_X root returns -999999 (vetoed); a FRESH trial assembled
  post-kill from live facts executes normally to 205.
  GUARD-PASS iff both hold.
- T3-G2 control battery: I2-equivalent (world (11,1,12),
  (12,1,13); native MAP_X [1,1]; relation 72; explore op=2
  truncate; compose_integ(W,11,72) -> 13) and I4-equivalent
  (no prediction basis -> compose_integ returns -3, zero type-16
  edges, live MAP count unchanged) run under all three guards.
  GUARD-PASS iff I2-equiv answers 13 and I4-equiv withholds -3
  with no adaptation side effects.

## 6. Meta bars

- RT-K6 (determinism): each binary runs 3x; stdout sha256
  recorded; pairwise cmp clean. FAIL = any mismatch.
- RT-K7 (hygiene): check_no_dash.sh exit 0 on every lane
  deliverable; the token `expected` appears in no new source
  (grep audit; frozen sources keep their own); guarded copies add
  0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 new semantic cases; exactly one new fact-field
  usage (f44 learner-origin) and one new header slot (hg40
  prediction source), both disclosed here and confined to guarded
  copies.
- RT-K8 (frozen integrity): the six pristine sources are
  byte-identical copies of the C295 origins (sha256 match the
  C295 report values, recorded in NAMECHECK.md Step 3); origins
  untouched (git diff empty on composition_integration/).

## 7. Deliverables

NAMECHECK.md (Steps 0-5), PREREG.md (this file), rt_build.sh,
frozen source copies, cc_base_g.zag / ts_patch_g.zag /
lvcomp_patch_g.zag (guarded copies with marked diffs),
rt_attack.zag, rt_guardtest.zag, rt_bin, rt_guard_bin,
rt_run1/2/3.txt, rtg_run1/2/3.txt with sha256 digests, REPORT.md
with per-target verdicts against the frozen bars, guard diff
line counts, and cognition-lines accounting (guard insertions
count as touched cognition lines; drivers are harness).

## 8. Governance

- Pure Zag for all computation; shell only for znc, binaries,
  git, file moves. Safebin mandatory; any forbidden-interpreter
  invocation = PROCESS-FAIL, results stay exploratory.
- This prereg + NAMECHECK.md committed ALONE before any attack
  implementation. Never weaken frozen bars. VOID is terminal.
- No em/en dashes in lane docs (check_no_dash.sh).
- Sealed worlds are not inspected except through the authorized
  evaluator protocol (not applicable here: all worlds in this
  lane are researcher-constructed minimal scenarios, stated
  above; no sealed assets are used).
- Do not touch TNN_RESEARCH_PAPER_20260929.md. Explicit
  pathspecs. Commits local only, never pushed ("Local only,
  never pushed." appended).
- Compiler lessons honored: no `as *i32` + slice construction in
  functions (u8 cells + get32/set32 helpers); no _zag_print for
  dynamic output (emit/e64 only, as in the frozen drivers);
  no reliance on `.len` of cast slices; if-nesting <= 3 with
  hoisted flags; no `!(A && B)` in while conditions (De Morgan
  form); capacity plan under the 1024-node workspace.
