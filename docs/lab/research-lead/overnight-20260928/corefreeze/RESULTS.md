# CORE-FREEZE RESULTS (charters 59, 60, 216, 61, 62, 63)

Lane `corefreeze/`. Prereg `PREREG.md` committed alone at 2ceaa1748, before
any implementation existed. No bar was moved after seeing results.

## 0. FROZEN CORE: UNCHANGED

```
750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8  c8_learn.zag   1331
fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61  c15_base.zag   174
4200e21fea5fa75d774f8f9785637d2305eccfa3d9b8486f27b7ac287b10b30d  hq_module.zag  326
```
Identical before and after the wave. `cf_base.zag` is `c15_base.zag` modulo
exactly ONE line (the `o_flush` body: `_zag_raw_syscall` is inert on this host,
brief 4.0/4.1), verified by `diff`.

## 1. K0 INFRA: ALL PASS

* `tnn_pure_zag_report` -> `VERDICT: PURE-ZAG-CLEAN`.
* compile rc 0 with `--target macos-arm64`, Mach-O arm64 (not ELF).
* **3/3 BYTE-IDENTICAL stdout**, sha256 `08969d50f51d78c5b7748fcc9e9a2479
  64ac585aa4ea5a077bf07b92f8156da3` over all three runs.
* stdout non-empty, 2 `BAR` lines present.
* **K-A architecture audit PASS.** `cf_engine.zag` contains ZERO world
  relation ids, ZERO goal tags, ZERO need tags in any string literal. Its
  entire literal vocabulary is field names and punctuation (listed by grep in
  the commit message). All 236 data literals live in `cf_data.zag`.
* zero em-dash / en-dash bytes in the lane.
* All runs through `tnnwatch.sh reg cf 900`. No orphans left.

## 2. HEADLINE: THE STUPID BASELINE REMOVES THE COMPETENCE

This is the load-bearing result and it is a NEGATIVE one.

| segment | meaning | MA | MV | MH | MR vs BASE-FULL | fact checks |
|---|---|---|---|---|---|---|
| s=0 | BASE-FULL (episodes+specialize) | 6/14 | 13/14 | 6/6 | (reference) | **1081** |
| s=1 | BASE-NOEP (zero episodes) | 6/14 | 3/14 | 6/6 | **27/27** | **2200** |
| s=2 | BASE-FRESH (zero L per world) | 6/14 | 13/14 | 6/6 | 27/27 | 1070 |
| s=3 | BASE-NOEP-FRESH | 6/14 | 3/14 | 6/6 | 27/27 | 2150 |

**MR = 27/27 means every single goal answer in BASE-NOEP is byte-identical to
BASE-FULL.** Deleting ALL experience changes nothing the core can do. The only
things that change are COST (2200 vs 1081 fact checks, 2.03x) and the reported
version vector (specialized 13/14 -> generic 3/14).

**So the frozen core's competence does not come from learner state. It comes
from the researcher-authored goal record.** Per PREREG section 7 this falsifier
fired, and the report must lead with it.

## 3. CORE-FREEZE ACCOUNTING (charter 216), PER CAPABILITY

Every capability below was obtained with **ZERO cognition-source change**. The
tier records how much researcher authorship was still required.

| id | capability | source change | TIER |
|---|---|---|---|
| CF1-a | 1-step projection, generic interface | ZERO | B (new goal-record bytes) |
| CF1-b | conjunct chain verification + fan-out | ZERO | B |
| CF1-c | union cardinality over a subject set | ZERO | B |
| CF1-d | per-step version selection incl. generic fallback | ZERO | B |
| CF1-e | multi-source kind-3 fan-in (no such goal exists in the c8 lane) | ZERO | B |
| CF1-f | oscillation detected from own trajectory, response invented (how=1, lag 2) | ZERO | **A** |
| CF1-g | convergent control, how=0 (same shape, no oscillation) | ZERO | **A** |
| CF1-h | honest decline on unbindable need shape (rc=0, declines 1->2) | ZERO | **A** |
| CF2-a | plan built in W1, executed in W2, new namespace, 0 new bindings, 0 new plans | ZERO | B |
| CF2-b | uncovered relation with facts, new namespace, generic seed | ZERO | B |
| CF2-c | multi-source fan-in reused in new namespace | ZERO | B |
| CF2-d | self-walk that halts empty, new namespace | ZERO | B |
| CF3-a | typed rewriting: maximal reduct set filtered by type AND grade, plus union cardinality | ZERO | B |
| CF3-b | causal blast radius as union cardinality over multi-source list | ZERO | B |
| CF3-c | generic fallback on uncovered relation, third namespace | ZERO | B |
| CF3-d | same oscillation entry point in W3 returning how=0 | ZERO | **A** |
| B4 | one-shot storage / integration / immediate reuse (OS1) | ZERO | **A** |
| B4 | later reuse stable over 4 repeats (OS1L 4/4) | ZERO | **A** |
| B4 | revision only by re-derivation (OSR2) | ZERO | **A** |
| B5 | early-learned-index ablation does not change competence | ZERO | **A** |

**TIER-A COUNT = 10. All 10 are "learner state changed behaviour on a
re-presentation of an existing capability" (oscillation invent/replay/converge,
decline, reuse, re-derivation, ablation-invariance). Not one is a new
capability.**

**TIER-C COUNT = 0.** No capability required per-task driver logic. The engine
has one dispatch on episode kind and one on mode; the K-A audit proves there is
no task-type branch.

**HONEST RATIO (charter 216).** delta-capability / delta-cognition-source is
`0 new capabilities / 0 lines changed`. The denominator is zero and the
Tier-A numerator is 10, but Section 2 shows those 10 are *not* new capabilities
-- they are reuse, convergence and decline behaviours on capabilities the
researcher fully specified. Calling this "10 new capabilities from learner
state" would be a faked zero, which the mission forbids. **The honest headline
is: ZERO new capabilities from learner state, and ZERO new capabilities from
new experience.**

## 4. PREREG EXPECTATION ERRORS FOUND (implementation NOT edited to match)

Per PREREG section 6, the expectation is reported wrong and the observed value
is reported. Four frozen expectations are internally inconsistent:

1. **Answer record ORDER.** `topo_g` picks the LAST zero-indegree need, so the
   core emits records in PLAN order, not need order (e.g. `porder=0,2,1` for
   G7002, `1,0,2` for G7003). All PREREG answers are written in need order.
   The engine reorders for the competence check and reports `porder`
   explicitly. This is an arbitrary researcher-frozen tie-break, not a
   capability.
2. **G7003@W2 answer.** PREREG expects `1 1`; observed `1 0`. Relation 9004 has
   exactly one fact `(9101,9004,9401)` and 9101 is not in the fan-in subject
   list, so 0 is correct. The PREREG's `1` corresponds to relation 9003.
3. **G7003@W3 answer + versions.** PREREG expects `1 7201 1 7301 1 1` and CNT
   version 5; observed `1 7001 1 7101 1 1` and version **4**. With the
   PREREG's own goal text ([6001,7101],[6001,7201]) the observed value is
   correct; 6002 is not in the CNT coverage set.
4. **W3 VFY coverage.** PREREG prose says `{5002}`; `vfy_episode` logs EVERY
   chain relation, so 5003 is covered too. The PREREG's own expected version 3
   requires both, so the expectation is right and the prose is wrong.

Net: **13/14 version expectations and 6/6 oscillation expectations are exactly
as preregistered.** The residual MA=6/14 is dominated by prereg answer-order
and the three value errors above, not by core failure.

## 5. DEVELOPMENTAL LEARNING AND EARLY ABLATION (charter 61)

| arm | stage-1 experience | answer | versions |
|---|---|---|---|
| DEV | 3 ret episodes + specialize | `1,1,0,0,0` | `2,1,4` |
| DEV-ABL | same, RET coverage count zeroed | `1,1,0,0,0` | `0,1,4` |
| DEV-NOEP | **stage 1 skipped entirely** | `1,1,0,0,0` | `0,1,4` |

**All three answers are byte-identical. Early learned structures are
prerequisites for EFFICIENCY and for reporting a specialized version, and are
NOT prerequisites for competence.** DEV-NOEP equals DEV on competence, so
stage-2 competence is a SECRETLY INDEPENDENT mechanism with respect to
stage-1 state. This is the prereg's stated conclusion and it fired.

**OSC-DEP = 1, 2, 1** exactly as preregistered: invented (how=1), replayed from
the stored outcome record (how=2), and after zeroing only `L[14500]` invented
again (how=1). The learned artifact does gate the *replay* path but not the
capability.

Caveat: all three DEV arms mismatch the PREREG's expected answer VALUE
(MA=0). The mismatch is identical across arms, so the developmental comparison
is unaffected, but the absolute value discrepancy is unresolved.

## 6. CURRICULUM INDEPENDENCE (charter 62)

| order | FINALans | FINALver | osc how |
|---|---|---|---|
| ABC | 0/9 | 9/9 | 0 |
| BCA | 3/9 | 9/9 | 0 |
| CAB | 0/9 | 9/9 | 0 |
| INTERLEAVED | 0/9 | 9/9 | 0 |

**KILL BAR NOT MET: no order reaches 9/9 answer matches.** However the failure
is order-INDEPENDENT in shape: version selection is 9/9 in every order and the
oscillation probe is correct in every order, so this is NOT catastrophic
interference and shows NO path dependence in the tested range. The 3/9 in BCA
is the three 1-need TA presentations (no permutation); TB and TC mismatch the
PREREG answer in every order, which points at the same class of PREREG
answer-order/value error as Section 4 rather than at fragility. **Reported as
a CURRICULUM FAIL because that is what the prereg specifies; the honest reading
is that the competence metric itself is contaminated and the order comparison is
uninformative rather than negative.**

## 7. ONE-SHOT / FEW-SHOT (charter 63)

| arm | predicted | observed | verdict |
|---|---|---|---|
| OS0 (0 episodes) | ver 0, `1 4001` | ver 0, `1 4001` | PASS |
| OS1 (1 episode) | ver 2, `1 4001` | ver 2, `1 4001` | PASS |
| OS2 (2 episodes) | ver 2, rev 2, nrel 1 | ver 2, rev 2, nrel 1 | PASS |
| OS1-LATER (x4) | stable | 4/4 answers and 4/4 versions | PASS |
| OSR (stale, no re-derive) | STALE WRONG `2 4001 4002` | **fresh correct `1 4009`** | **BOUND-4 FALSIFIED (positive)** |
| OSR2 (re-derive) | `1 4009` | `1 4009` | PASS |

**OSR returned the correct fresh answer, not the predicted stale one.** PREREG
section 7 anticipated exactly this and calls it a genuine positive. Mechanism:
`ret_spec` stores fact INDICES, not values, so "staleness" manifests as reading
a different arena slot, and with a same-slot replacement the answer comes out
right by accident.

To decide whether BOUND-4 is really dead, two clearly-labelled POST-HOC
diagnostics (not kill bars) were added:

* **OSR3**: stale index, replacement arena has NO fact with that relation.
  Truth = empty. Observed = a NON-EMPTY answer naming a subject that does not
  satisfy the queried relation. **Stale index produces a WRONG answer.**
* **OSR4**: identical, but the index is re-derived first. Observed = `0`, i.e.
  **correct.**

So BOUND-4 is CONFIRMED as a real defect (stale index -> wrong answer), while
the PREREG's literal OSR prediction was wrong about how it manifests. There is
**no contradiction trigger anywhere in the core**: revision happens only if the
researcher re-derives.

**SEPARATION, AS REQUIRED.** One-shot *storage* is real and is one i32: one
episode puts one relation id into a coverage table. One-shot *generalisation* is
**NOT claimed and was not found**: `learn_bindings` retries all three families
on every unbound need tag, so one example never reduces the family search space
(`tr` goes 3 -> 6 -> 9 -> 12 across W1 goals, i.e. 3 trials per new need tag,
every time). No new procedure family can be learned from one example.

## 8. BOUNDS FOUND BY READING (reported, not fixed)

* BOUND-1/2/3 confirmed (PLAN 4 slots, BIND 8, coverage 16x64).
* **BOUND-5 is sharper than PREREG stated and it bites.** `plan_find` keys on
  goal tag only, so a SHAPE CHANGE under a live tag is silently executed with
  the old plan. G7004c (2 needs) and G7004 (3 needs) share tag 7004. This wave
  used the frozen core's own generic `plan_drop` to release the slot; that is
  core functionality driven from data, but it IS a driver decision and is
  disclosed. Without it the plan table would also overflow.
* `plans_built` is 6 for the CF1-CF3 lifetime, not the preregistered 4, for
  this reason.
* New: the frozen core passes the goal-time fact-check counter as `K[0]` and
  the episode counter as `K[12]`; a harness that reads `K[8]` silently reports
  zero cost. (Recorded because it nearly invalidated Section 2.)

## 9. HARNESS DEFECTS FOUND AND FIXED (all mine, none in the frozen core)

1. Adjacent string literals are silently dropped by the compiler: only the
   first survives. Data strings must be assembled with `o_app`.
2. Byte/int aliasing: a label's length field at `slot+0` and its packed chars
   at `slot+1` overlap; the corrupted length produced a 774-million-byte slice
   and a segfault. (This is exactly the `get32/set32` byte-offset hazard in the
   mission brief.)
3. `p_case`/`p_seg` started their output cursor at 0 instead of the incoming
   position, overwriting the log buffer from the start.
4. The `ans` answer area starts at byte 4, and appended values are strided by 4
   bytes; three separate off-by-N errors here produced plausible-looking but
   wrong answers.
5. BASE-NOEP initially inherited `L` from segment 0, which made the
   load-bearing baseline look like a large competence effect (MR=13/27). It is
   not; with a zeroed `L` it is 27/27. **This is why the baseline must be
   audited before it is believed.**
6. `bld_labels` reports 85 labels for 84 carets because a trailing caret yields
   one empty label; harmless (index 84 is never referenced).

## 10. VERDICT

**The frozen core is a competent, deterministic, domain-agnostic goal-record
INTERPRETER. It is not a learner of capability, and this wave provides strong
evidence that it is not.**

* It executes 19 novel world/namespace/task combinations with **ZERO cognition
  source change** and **zero domain handlers** (K-A proven by grep). That half
  of the mission is a real, verified success.
* But **removing all experience leaves every answer unchanged** (MR=27/27).
  Learner state buys COST (2.03x) and a version label. Nothing else.
* **Developmental ablation confirms it**: stage-2 competence is identical with
  stage-1 experience, with stage-1 structures ablated, and with no stage-1 at
  all. Later stages are secretly independent mechanisms.
* Consequently the dream trajectory is not supported at this generation.
  **LATE-stage "new capability from new experience only" is FALSE for this
  core**: new experience alone yields zero new capability. What the core has is
  what the researcher wrote into the goal record.

**The long-term target (many new capabilities with ZERO cognition changes) is
not reachable by continuing to add goal records to THIS core.** It requires a
core whose competence boundary depends on learner state, which this one does
not have.

## 11. BOUNDARIES

* Four PREREG expectations are wrong (Section 4); expectations were never edited
  to match the implementation.
* Curriculum competence metric is contaminated; the order comparison is
  uninformative, not negative.
* Absolute DEV stage-2 answer value unresolved (identical across all arms).
* `nlabels=85` off-by-one in the label builder (harmless).
* TOOLCHAIN CONCERN, FLAGGED NOT CONCLUDED: across *different builds* of
  logically identical harness source, the plan order for one goal was observed
  to differ (`1,0` vs `0,1`) in an isolated probe. Run-to-run determinism of a
  fixed binary is 3/3 byte-identical (verified). Build-to-build stability was
  NOT verified and should be treated as open; if real it would qualify the
  brief's section 4.1 reproduction claim (B13), which tested one rebuild, not
  repeated rebuilds. **Replicate before citing.**

## 12. NEXT EXPERIMENT

1. **Replicate or refute the build-to-build plan-order instability** with a
   minimal, dedicated probe. This gates every other result.
2. **Attack the competence boundary directly.** The one lever that DID move
   behaviour without source change was `osc_handle` inventing a response from
   the learner's own trajectory (TIER-A). The next battery should make the
   *oscillation seed* the only input: give the core an arena whose facts make a
   goal oscillate for a reason the researcher did not enumerate, and measure
   whether the invented response transfers to a goal shape never presented.
   That is the only route to a non-zero Tier-A capability count.
3. **Adjudicate TB/TC and the DEV value** with a memory-free oracle goal, then
   re-score curriculum order with a clean metric.
4. Replace `BOUND-4`'s accidental behaviour with an explicit contradiction
   episode type -- but note that requires cognition source change, which is
   precisely what this lane exists to measure.