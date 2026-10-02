# PREREG_OWNED: machinery-disabled integration discrimination (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED. Date: 2026-10-02.
Worker phase: 1 (writing only). Implementation authorized only after the
coordinator commits this prereg alone.

## 0. Commit order (K0)

This prereg is committed alone in
docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/. The implementation
commit must be a strict descendant of the prereg commit. Verified via
`git merge-base --is-ancestor <prereg-sha> <impl-sha>` before any verdict is
reported. UNVERIFIABLE ORDERING voids the prereg. No bar may be altered after
results are seen; amendment requires a transparent re-freeze.

## 1. Question and lineage

The CONTLEARN line stands at INTEGRATION-DEMONSTRATED: the 2021pdt battery
reached REUSE_COUNT 30/30, and the 2321pdt lane reached LEARNOWN-DEMONSTRATED
(unsupervised store 13/13, masked reuse 20/20, ablation-verified dependence
on stored structures). The red-team QUALIFY stands on both: the integration
work is done by researcher machinery, not by the learner. The 2321pdt
verdict states it plainly: "no learner-created state influences any store,
accept, or retrieve decision; the trial search order, the
first-clean-candidate accept rule, and the promotion rule are frozen
researcher code." Attack 6 is carried forward: measured reuse is exact-hit
retrieval of machinery-taught facts via `activate`, not execution of
promoted MAPs at query time.

This probe is a discrimination, not a new integration build. It asks: can
the continuing learner integrate a defined new experience (a fresh chain
fact family, plus a delayed reuse probe across an interference gap) using
ONLY its own mechanisms, with the researcher machinery that performed the
integration in the DEMONSTRATED result DISABLED or ABSENT?

## 2. Exact machinery under test (re-read from the frozen source)

Frozen core: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
commit f4de7ff46, 1591 lines, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.

The machinery that performed the DEMONSTRATED integration, on the query
path of `ev_query` (frozen file lines 813-836):

- `mp_run` (line 668) -> `t2_trial` (line 586): event-triggered trial
  construction of executable graphs over k-hop chains (k=2..4), sums, and
  counts, in a frozen search order. Called only from `ev_query` line 827.
- `t2_try_verify` (line 497): the first-clean-candidate accept rule
  (`v!=-2 && v!=-999999`). Called only from `t2_trial`.
- `promote_graph` (line 533): MAP allocation (tag 20) with alive DEP
  (type 1) edges to every licensing fact on the chain path, plus
  `ev_teach_in` of the computed answer fact. Called only from `t2_trial`
  (lines 605, 628, 644, 659).
- `bootstrap_miss` (line 763): P-INV statistical bootstrap on the query
  path (allocates a MAP and teaches a value when >=k facts on one relation
  share a value). Called only from `ev_query` line 830. It did not fire in
  the DEMONSTRATED battery, but it is the same class of event-triggered
  structure construction on the integration path, so it is disabled too.

Call-site inventory (verified by grep, frozen here): `mp_run(` has one call
site (ev_query:827); `t2_trial(` one (mp_run:670); `t2_try_verify(` four
(t2_trial only); `promote_graph(` four (t2_trial only); `bootstrap_miss(`
one (ev_query:830).

Mechanisms kept (the learner's own, in the only sense the frozen core
supports): `activate` standing retrieval over learner-created edges and
standing; `miss_inquire` (UNCERTAINTY tag-30 node plus a learner-constructed
guide fact linked to POLICY_ROOT); `ev_act` selection over
learner-constructed guides; `ev_teach` experience delivery (the facts ARE
the new experience; the integration work must not come from the disabled
machinery).

Honest boundary statement, frozen: the frozen core contains no
learner-invoked trial/construct machinery. There is no `compose_try`
function in the frozen source (only a comment at line 1217). `t2_trial` is
event-triggered researcher machinery, not a learner-owned operation. So the
learner-owned candidate set for this discrimination is exactly: standing
structures serving queries, UNCERTAINTY/guide construction into POLICY_ROOT,
and guide selection. If those cannot integrate the new experience, the
verdict is MACHINERY-DEPENDENT, reported as an informative discrimination.

## 3. The machinery-disabled condition

A variant core `ow_core_disabled.zag` is derived mechanically from the
recorded nomain derivation of the frozen core
(`lo_core_nomain.zag`, SHA-256
`26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`,
itself a one-line-stripped derivation of the frozen file). The derivation
removes exactly the two call blocks in `ev_query`:

```
  // trial loop first (learner-set miss policy)
  let ans:i32=mp_run(W,s,r,expected,flags);
  if(ans!=-2){log_ev(W,2,s,r,ans,1,0,0); return ans;}
  // fallback: P-INV bootstrap
  let bv:i32=bootstrap_miss(W,s,r);
  if(bv!=-2){log_ev(W,2,s,r,bv,1,0,0); return bv;}
```

Everything else in `ev_query` is kept (exact-hit `activate`, the recent
SUR-edge block, the miss log, `miss_inquire`, return -2). The five
machinery functions remain as unreachable dead code (kept so the diff is
surgical). The variant is a measurement instrument, not a proposed
architecture change; no claim follows about the variant being a better
learner.

Absence verification (CO-5), all frozen here:
- (a) Source diff: `diff` between the variant core and the recorded nomain
  derivation shows exactly the two removed call blocks and nothing else.
- (b) Grep: in the variant source, zero call sites of `mp_run(`, `t2_trial(`,
  `t2_try_verify(`, `promote_graph(`, `bootstrap_miss(` outside their own
  `fn` definition lines; i.e., no path from the event interface
  (`ev_query`/`ev_teach`/`ev_observe`/`ev_act`) can reach them.
- (c) Behavioral: on the 6 family-D masked probes, the variant run writes
  zero new MAP nodes (measured in the run itself).

## 4. Experience sequence (exact, frozen, fresh)

Fresh battery: all subject ids (9001..9106, 9501..9506, 9601..9706,
11001..11130, 12001..12120) and all relations (501, 701, 702, 801, 901,
902) are unused by any prior battery across the wave-20261001 lanes
(verified by grep over the committed lane sources). The script is disclosed
in this prereg (frozen, not adversary-designed); the post-freeze
adversarial battery remains the generality test and is separate. SHA-256 of
the driver source and of the variant diff are recorded before any run.

Two binaries, identical fixture driver, one process per run: TREAT links
the machinery-disabled variant core; CONTROL links the unmodified frozen
core. Event kinds: TEACH (ev_teach), MQUERY (ev_query expected=-2,
flags=1; supervisor disconnected, disclosed; not a task label). PHASE
markers are driver-side prints and never reach cognition.

Full script (104 events), both binaries:

- STORE (30 events):
  - Family D, concept links: for i in 0..5: TEACH(9001+i, 501, 9101+i).
  - Family D, anchor links: for i in 0..5: TEACH(9501+i, 701, 9001+i).
  - Family D, integrate: for i in 0..5: MQUERY(9501+i, 702). Integration
    means: answer 9101+i returned AND MAP(9501+i,702) exists with an alive
    DEP edge to fact(9001+i,501,9101+i). The chain is
    9501+i -> 9001+i -> 9101+i.
  - Family E, standing sanity: for i in 0..5: TEACH(9601+i, 801, 9701+i).
- INTERFERE-1 (30 events): for i in 0..29: TEACH(11001+i, 901, 11101+i).
- REUSE (12 events): for i in 0..5: MQUERY(9501+i, 702) [stored 9101+i];
  for i in 0..5: MQUERY(9601+i, 801) [stored 9701+i].
- INTERFERE-2 (20 events): for i in 0..19: TEACH(12001+i, 902, 12101+i).
- DELAYED (12 events): the same 12 probes as REUSE, same order.

Node/edge budget: TREAT worst case about 110 alive nodes (74 facts, 18
UNCERT, 18 guides); CONTROL about 86 facts plus 6 MAPs; far below the
1024/4096 caps, so no eviction can occur and any missing structure is
evidence, not capacity.

## 5. White-box measurement oracles

All predicates are structural (tag/field/edge/reachability) over the live
arena, read through the core's own accessors, content-identified, never by
assumed id ranges.

- fact(s,r,o): tag==1, alive, field20==s, field24==r, field28==o.
- map(sbj,rel): tag==20, alive, field8==sbj, field4==rel.
- guide: tag==1, alive, field20==30, field24==-999 (the miss_inquire
  signature).
- serving node of MQUERY(s,r): `activate(s,r)` read-only after the query;
  must be the content-expected live fact, non-superseded.

STORE_OK (end of STORE): for i in 0..5, map(9501+i,702) exists AND has an
alive DEP edge to fact(9001+i,501,9101+i) AND the STORE masked query
returned 9101+i. Bar: 6/6.

REUSE_OK (REUSE phase): the 12 masked probes return the stored values with
the content-expected live fact as serving node: 6x 9101+i on (9501+i,702),
6x 9701+i on (9601+i,801). Bar: 12/12.

DELAYED_OK (DELAYED phase): the same 12 probes again. Bar: 12/12.

SANITY_E (TREAT, REUSE phase): the 6 family-E probes served via activate.
Bar: 6/6. Proves the variant is otherwise functional (standing retrieval
intact) so a TREAT integration failure is a capability gap, not breakage.

Mechanism census per phase (CO-2 evidence): MAPC (alive tag-20 nodes),
DEPC (alive type-1 edges), UNC (alive tag-30 nodes), GUIDEC (guide-signature
nodes), ACTHIT_D (D probes returning 9101+i), MISS_D (D probes returning
-2).

## 6. Frozen kill bars

CO-1 (TREAT integrates to the DEMONSTRATED bar, machinery absent):
STORE_OK_T == 6 AND REUSE_OK_T == 12 AND DELAYED_OK_T == 12.

CO-2 (integration via the learner's own mechanisms): the per-phase
mechanism census is complete and 3/3 consistent across reps, and it
unambiguously identifies which mechanisms produced the outcome. If CO-1
passes, the census must show learner-created structures (MAPs with DEP
edges to licensing facts) that cannot have come from the disabled
machinery (CO-5 verifies the machinery is unreachable). If CO-1 fails, the
census must show the failure signature: zero MAPs, D probes taking the
true miss path (MISS_D counts), UNCERT/guide accumulation.

CO-3 (determinism): 3/3 byte-identical transcripts per binary: SHA-256 of
stdout equal across the three reps, printed FNV-1a arena checksums equal,
exit code 0, zero stderr bytes, no PID/timestamps/paths in transcripts.

CO-4 (control reproduces the DEMONSTRATED result): on the unmodified frozen
core, STORE_OK_C == 6 AND REUSE_OK_C == 12 AND DELAYED_OK_C == 12.

CO-5 (machinery truly absent): the three absence checks of section 3 all
pass (exact two-block diff; zero event-interface call sites by grep;
zero new MAPs on the 6 D probes in the TREAT run).

Governance bars (same standard as the 2321pdt lanes):

K0: prereg committed alone; implementation strictly descendant; verified by
merge-base before verdict.

K1 (one learner, no reset, no recompile, no task labels): K1a: exactly 6
learner processes total (2 binaries x 3 reps), one process per full
104-event run; transcripts contain no PID; harness log records spawns.
K1b: a znc wrapper logs every znc invocation; exactly 2 entries (the two
pre-run builds, one per binary) before the runs; 0 new entries during the
runs. K1c: driver self-audit; every tuple flows through the two choke
points with kind in {1,2} and plain integer operands; MQUERY carries the
frozen parameters expected=-2, flags=1 (disclosed supervisor disconnect,
not a task label); PHASE markers never reach cognition; all runs launch
with empty argv and empty env; expected audited count 104 per run;
prints AUDIT_PASS.

K2 (frozen ISA boundary and architecture accounting): K2a: SHA-256 of the
frozen tnn2.zag equals
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd before
the builds and after the runs; `git diff f4de7ff46` on the frozen path
empty throughout. The CONTROL binary links the recorded byte-identical
nomain derivation read-only; the TREAT binary links the variant, which is
the nomain derivation minus exactly the two removed call blocks (CO-5a).
K2b: driver source audit: 0 cognition functions, 0 structural writes
(`ns(`/`link_edge`/`alloc_node` count 0), 0 new node tags, 0 new edge
types, 0 new opcodes, 0 modes, 0 bridges, 0 routers, 0 task-specific
handlers, 0 semantic cases (switch/match count 0). K2c: cognition-source
delta on the frozen path 0/0/0; the variant is a measurement instrument in
the lane dir, not a change to the frozen architecture; one-system rule
holds (single persistent arena, frozen formats). K2d: pure Zag plus shell
only; `which python3` prints nothing under the safebin PATH (NAMECHECK.md
Step 0).

K3 (no regression): the committed 2321pdt `lo_driver` binary (extracted
read-only from the recorded commit) re-run 3x in TREAT mode; stdout
SHA-256 must equal
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9 on all
3 reps. Kill: any mismatch.

K6 (determinism) is CO-3; listed once.

## 7. Frozen decision rule

- OWNED iff CO-1, CO-2, CO-3, CO-4, CO-5, K0, K1, K2, K3 all pass, and the
  CO-2 white-box evidence shows the integration structures were produced
  via learner-owned paths with the machinery verified absent. Claim:
  integration of the new experience is learner-owned.
- MACHINERY-DEPENDENT iff CO-4, CO-5, K0, K1, K2, K3, CO-3 pass and CO-1
  fails. Claim: the learner does not integrate the new experience without
  the researcher machinery; the red-team QUALIFY stands; integration is
  machinery-dependent. This is an informative discrimination, reported
  honestly, and per the no-patch-treadmill rule it is followed by
  root-cause analysis, not by new handlers, modes, or opcodes.
- VOID iff K0, K1, K2, K3, CO-3, or CO-5 fails: instrument failure, no
  verdict. A CO-4 failure with CO-1 passing is reported as an anomaly with
  root-cause analysis (the control must reproduce the bar).

## 8. Exact claim bound (frozen)

If OWNED: on the fixed disclosed 104-event battery, with the trial /
promotion / P-INV machinery verified absent from the event path, the
continuing learner integrates 6/6 fresh 2-hop chains into MAP structures
with DEP citations using only its standing structures, UNCERTAINTY/guide
machinery, and guide selection, reuses 12/12 integrated values across an
interference gap and 12/12 again after a second gap, 3/3 byte-identical.

If MACHINERY-DEPENDENT: the same battery shows the learner stores the
taught facts and serves them by standing retrieval (family E 6/6 in the
variant), but integrates 0/6 chains without the trial/promotion machinery
(all D probes take the true miss path; zero MAPs; UNCERT/guide
accumulation is the only learner-side response), while the unmodified
frozen core integrates 6/6 on the identical battery. The red-team QUALIFY
is thereby strengthened by a clean discrimination: the integration work
sits on the researcher side of the control-plane line.

Explicitly not shown either way: learner agency in the causal sense
(H2-v2/H3 stand); procedure execution at query time; any L3 or generality
claim; the variant is not a proposed architecture.

## 9. What this prereg does NOT authorize

- No implementation in this commit.
- No new cognitive machinery of any kind: no new Zag subsystems, modes,
  bridges, routers, task-specific handlers, semantic cases, node tags,
  edge types, or ISA opcodes. The variant core is a disabled-machinery
  measurement instrument in the lane directory; it is not a learner design
  and must not be presented as one.
- No tuning of any kind to this battery; K2a/CO-5 forbid edits beyond the
  two frozen call-block removals.
- No sealed adversarial worlds; the script is disclosed. The post-freeze
  adversarial battery remains the generality test and is separate.
- The 2321pdt binary is re-run read-only for K3; it is not rebuilt and not
  modified.
