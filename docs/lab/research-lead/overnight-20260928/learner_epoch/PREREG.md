# PREREG: LEARNER-EPOCH (frozen)

Non-ledger task. Lane
`docs/lab/research-lead/overnight-20260928/learner_epoch/`, file prefix
`le_`. Branch `tnn-native-lab`, commits local only, never pushed.

## 1. Task

STALE-INDEX-RECOVERY (SI) left one open follow-up: "the epoch bump
discipline is stage-code instrumentation in this experiment, not
learner-owned mutation tracking. Learner-owned versioning (the world
mutator itself stamping the epoch) is a follow-up." There, the world
epoch (state slot 931) was advanced by harness stage code:
`setup_worldA(A); ss(S2,931,sg(S2,931)+1)` and one manual bump after
the S13D in-place object write. The content checksum was the only
signal the learner computed unilaterally from the world.

This experiment moves epoch stamping into the learner's own
world-mutation operations. `fact_add` and the new `fact_set_obj`
advance the epoch as a side effect of mutating, unilaterally: stage
code that mutates the world performs no bump call of its own. The S13
battery is rerun as S14 with zero stage-code epoch writes, plus a new
read-no-stamp control stage.

## 2. Frozen design answers (before implementation)

**A1: what signal does the learner use to decide when to bump?**
Mutation events at its own world interface. Every successful
`fact_add` (the `n<64` guard: a real add happened) and every
`fact_set_obj` advances the epoch exactly once. Reads never stamp.
The learner does not compare content to decide; the epoch is a
conservative mutation counter, and the checksum remains the precise
content signal. A rebuild of identical content advances the epoch
(spurious re-specialization, still correct); a same-value in-place
write advances it too. This conservatism is frozen, not tuned.

**A2: how does `fact_add` reach the epoch cell?** `sg`/`ss` are defined
in the module file, which assembles after base and world, so the
stamping helpers live in `le_base.zag` and use `get32`/`set32`
directly on byte offset `931*4`: `w_epoch_bump(S)` and the read
accessor `w_epoch_get(S)`. Stage code (`le_main.zag`) never names the
epoch cell at all, not even for reads; it uses `w_epoch_get`.

**A3: which operations stamp?** Exactly two: `fact_add` (append path,
used by all three `setup_world*`) and `fact_set_obj` (in-place object
write, used by the S14D adversarial mutation). `chain_add` does not
stamp (chains are episode structures, not the world). L-state index
builds do not stamp (they do not change the world). The `set32(A,0,0)`
clear at the top of each `setup_world*` does not itself stamp; every
existing rebuild path follows the clear with adds, so the epoch always
advances across a rebuild. A hypothetical clear-without-add path would
not stamp: noted boundary, no such path exists in the battery.

**A4: what is the honest status of "learner-owned"?** Frozen before
implementation: this experiment does NOT show the learner inventing
versioning. The epoch cell, its monotonic semantics, the choice of
mutation events as the signal, and the placement of the bump inside
the two operations are researcher-designed. What the experiment DOES
show is unilateral maintenance: the stamping invariant is now kept by
the learner's world-mutation operations themselves, so deleting every
stage-code bump changes nothing observable (LE-S1 plus LE-B1/B3),
whereas in SI the same deletion would have yielded ver_stale=0 and a
reactive-only recovery. The bug class eliminated is "the harness
forgot to instrument a mutation path" (the N1 class). The bug class
NOT eliminated is "a future mutation path bypasses the two ops with
raw array writes": that stays a discipline issue, auditable by the
LE-S1 style grep, not enforced by the compiler.

## 3. Implementation (additive deltas over si_*, frozen)

- le_base.zag: si_base.zag plus `w_epoch_bump(S)`, `w_epoch_get(S)`,
  `fact_add(S,A,s,r,o)` (signature gains S; bumps inside the `n<64`
  branch only), and `fact_set_obj(S,A,idx,o)` (in-place object write
  plus bump). Nothing else in base changes.
- le_world.zag: si_world.zag with `setup_worldA/B/A2` gaining the S
  parameter and threading it to `fact_add`. World literals stay in
  this file, unchanged.
- le_module.zag: byte-copy of si_module.zag.
- le_learn.zag: byte-copy of si_learn.zag. The three `sg(S,931)`
  recording reads in `specialize_*` are unchanged; `spec_ver_stale`
  and `spec_ensure_fresh` are unchanged.
- le_main.zag: si_main.zag with (a) every `setup_world*` call site
  threading the in-scope state (`S` in demo_cov_revise, `S2` in main);
  (b) all seven `ss(S2,931,sg(S2,931)+1)` stage bumps deleted; (c) the
  S13D direct write plus manual bump replaced by
  `fact_set_obj(S2,A,mj0,mo1)`; (d) the S13 block replaced by the S14
  battery below; (e) comments updated. Acts 1/2/S11 logic otherwise
  untouched.
- New state cells: none. S+930 (proactive flag), S+931 (epoch),
  L+14020 (entry mask), L+14036/L+14040 (arm totals) are reused.
- le_build.sh: assemble le_full.zag from the five parts, compile with
  the pinned znc. Pure shell + znc.

### S14A LE-STALE-SETUP (no stage bumps)

setup_worldA(S2,A); setup_worldA2(S2,A); specialize_ret/vfy/cnt
(S10E precedent, contracts active, u_induct path); setup_worldA(S2,A)
restore. No bump calls anywhere in stage code. Print
`LE-SETUP specworld=A2 liveworld=A nostagebump`. Derive r601, o601,
r603 from the live world (vocab_scan, first_obj; runtime-derived, no
world literals), tLE = tagC+5, gLE = g_tag(mk_goal813_E0)+7, and build
the 1-need ret goal GSLE via mk_g1need (the S12 G2 shape; oracle_1ret,
okind=2).

### S14B LE-SIGNAL-PROBE

Before any spec procedure runs on the restored world, print one line:
`LE-PROBE nf_stale=<m> ck_stale=<m> ver_stale=<m>` with the three
bitmasks (0-7).

### S14C LE-PROACTIVE (epoch-gated)

Snapshot cs/cg (L2+13244/13248) and steps (L2+14012). Set S+930=1.
do_query LEQ0 (plan miss; the inline version check must fire,
re-specialize all three specs, then the query runs on fresh indexes).
Print `LE-AUTO entry_mask=<m>` (the stashed mask). Eight follow-up
queries LEQ1..LEQ8 (plan hits). Clear S+930=0. Print
`LE-COST arm=proactive q=<q> steps=<s> total=<t>` where q is the
cs+cg delta, s the step-counter delta, t = q+s; stash t at L+14036
(the proactive arm total, as in SI).

### S14D LE-ADVERSARIAL (same-nf content change, learner-op mutation)

Starting from the S14C end state (world A, fresh A indexes, contracts
active): find the first two facts with rel == r603 (runtime-derived
indices mj0, mj1); read fact mj1's object mo1; call
`fact_set_obj(S2,A,mj0,mo1)` (the learner op stamps; no stage bump).
nf stays 56; the LE query's (601,621) answer is untouched. Print
`LE-MUTATE` with the runtime-derived indices. Print the LE-PROBE line
again. Set S+930=1; do_query LEQ0A (plan hit); print LE-AUTO; clear
S+930=0.

### S14E LE-READ-NOSTAMP (discriminating control)

setup_worldA(S2,A); specialize_ret/vfy/cnt (fresh). Sample
e0 = w_epoch_get(S2). Run three queries LEQd1..LEQd3 (plan hits, no
mutation). Sample e1 = w_epoch_get(S2). Derive fact 0's (s,r,o) triple
from the live world and append it via fact_add(S2,A,ds0,dr0,do0) (nf
56 to 57, runtime-derived values). Sample e2 = w_epoch_get(S2).
Print `LE-EPOCH-READ e0=<e0> e1=<e1>` and
`LE-EPOCH-MUT e1=<e1> e2=<e2>`.

### S14F LE-REACTIVE (N1 reproduction, proactive off, no stage bumps)

setup_worldA(S2,A); setup_worldA2(S2,A); specialize x3 (contracts
active, u_induct path); setup_worldA(S2,A) restore. Snapshot cs/cg/
steps AFTER the setup. S+930 stays 0. do_query LEQ0R (plan hit, stale
indexes) plus eight follow-ups LEQ1R..LEQ8R. Print
`LE-COST arm=reactive q=<q> steps=<s> total=<t>`; stash t at L+14040.

### S14G LE-SUMMARY

Print `LE-VERDICT proactive_total=<P> reactive_total=<R>` from the
stashed arm totals, then SUMMARY-LEARNEREPOCH with the SI summary
fields plus `steps=<L+14012>`.

## 4. Frozen kill bars

- LE-R1 (regression, additive-only): le_run1.txt lines 1-97
  byte-identical to si_run1.txt lines 1-97 (Acts 1/2/S11).
- LE-S1 (no stage-code epoch touches): `grep -c 931 le_main.zag`
  is 0. Epoch writes exist only in le_base.zag (`w_epoch_bump`,
  called by `fact_add`/`fact_set_obj`); the only other `931`
  occurrences in the lane are the three pre-existing `sg(S,931)`
  recording reads in le_learn.zag.
- LE-B1 (N1 reorder detected with zero stage bumps): the S14B
  LE-PROBE line is exactly
  `LE-PROBE nf_stale=0 ck_stale=7 ver_stale=7`.
- LE-B2 (proactive recovery on the learner-stamped epoch): S14C has
  zero RETRY lines; LEQ0 is a single Q line with st=2 vers=2 agree=1;
  `LE-AUTO entry_mask=7`.
- LE-B3 (adversarial in-place mutation through the learner op): the
  S14D LE-PROBE line is exactly
  `LE-PROBE nf_stale=0 ck_stale=7 ver_stale=7`; S14D has zero RETRY
  lines; LEQ0A is a single Q line with st=1 vers=2 agree=1;
  `LE-AUTO entry_mask=7`.
- LE-B4 (read-no-stamp control): the LE-EPOCH-READ line shows
  e0 == e1 (queries do not stamp); the LE-EPOCH-MUT line shows
  e2 == e1+1 (one learner-op add stamps exactly once).
- LE-B5 (reactive safety net intact): S14F has exactly 2 RETRY lines;
  LEQ0R appears 3 times with (agree=0,vers=2), (agree=0,vers=2),
  (agree=1,vers=0); RETRY att=1 shows `dc=1,0,0 active=1,1,1`; RETRY
  att=2 shows `dc=2,0,0 active=0,1,1`.
- LE-K1 (cost preserved): from the two LE-COST lines,
  proactive_total < reactive_total.
- LE-H1 (toolchain/hygiene): safebin for all build/run/verify
  commands (recon noted in NAMECHECK); pure Zag; pinned znc; prereg
  committed alone before implementation; 3/3 byte-identical runs,
  stderr empty, exit 0; zero em/en dash bytes in authored files; no
  world literals in new executable code (all tags/rels/objs/goals and
  the S14E triple runtime-derived).

## 5. Predicted mechanism trace (for the report, not a bar)

- S14A: three setup calls stamp 56+56+56 via fact_add; specialize
  records the post-A2 epoch; the restore advances it by 56 more, so
  the S14B probe reads mask 7 with no stage bump anywhere.
- S14C LEQ0: inline check sees live vs recorded mismatch on all three
  specs (mask 7), re-specializes (3x56 build + 3x56 checksum steps),
  query runs ret_spec on fresh A indexes: 16 bucket visits, answer
  {611}, agree=1 first try. Follow-ups: 16 visits each.
- S14D: fact_set_obj stamps once; probe mask 7 on ck and ver;
  LEQ0A plan hit, ensure_fresh re-specializes (mask 7), agree=1.
- S14E: e0 == e1 (no world writes during queries); e2 == e1+1.
- S14F LEQ0R: att=1 ret_spec on stale A2 indexes, 0 subjects,
  disagree, RETRY att=1 (dc 1,0,0); att=2 same, RETRY att=2 (dc 2,0,0,
  3000-contract retired); att=3 generic 56 visits, agree. Follow-ups:
  56 visits each, generic, first-try agree.
- Estimated totals: proactive 984, reactive 1152 (same structure as
  SI; the bar is the inequality, not the estimates).

## 6. What this does NOT claim

- The learner did not invent versioning (see A4). No L2/L3 invention
  evidence is claimed; this is mechanism placement, honestly labeled.
- Raw `set32(A,...)` writes in future stage code would bypass
  stamping exactly as a missed bump did; the mitigation is keeping all
  world mutation behind the two ops, auditable by LE-S1.
- 56 facts is a toy world; the cost inequality is structural
  (per-query check cost vs per-query index saving vs one respec),
  not a scaling result.
- Whether the epoch should advance only on content change (rather
  than on every mutation op call) is left open; the conservative
  choice is frozen here.
