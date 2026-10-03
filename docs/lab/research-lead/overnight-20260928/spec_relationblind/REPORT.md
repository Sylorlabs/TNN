# SPEC-RELATIONBLIND: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_relationblind/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (9/9 frozen kill bars)**

## Summary

Investigates DISAGREEMENT-ATTRIBUTION Finding 3: `cnt_spec` and `ret_spec`
verify the queried subject/object at bucketed slots but not the relation id,
while `vfy_spec` checks all three fields. A minimal Zag repro using the REAL
`da_learn.zag` functions (unmodified) confirms the finding in isolation from
positional staleness: changing ONLY the relation field at one bucketed slot
(no index shift, no deletion, same fact count) makes `ret_spec` emit a phantom
subject (1 vs 0) and `cnt_spec` return a phantom count (1 vs 0), while
`vfy_spec` stays correct (0 vs 0). Relation-revalidating variants
(`ret_spec_fix`, `cnt_spec_fix`) restore spec==generic agreement on all
drifted worlds, behave byte-identically to the originals on the pristine
world, and add zero loop iterations. All binaries pure Zag, safebin-built,
3/3 byte-identical.

## What was tested (do not treat the reasoned sections as tested)

The experiment assembles the real `da_base.zag` + `da_module.zag` +
`da_learn.zag` from the disagreement_attribution lane (byte-unmodified) with
lane-local `rb_world.zag` (tiny world + drifts), `rb_fix.zag` (fix variants),
`rb_main.zag` (harness). Repro: `./rb_build.sh` in this directory.

Tiny world: slots 0..3 = (1,901,10), (2,901,20), (1,902,30), (3,902,40).
Learner state built once via the real `specialize_ret`/`specialize_vfy`/
`specialize_cnt`; buckets: 901 -> {0,1}, 902 -> {2,3}.

| Stage | Condition | RET spec vs gen | CNT spec vs gen | VFY spec vs gen |
|-------|-----------|-----------------|-----------------|-----------------|
| D0 | pristine (control) | 1 vs 1, agree | 1 vs 1, agree | 1 vs 1, agree |
| D1 | slot 0 relation 901->902 in place | **1 vs 0, DIVERGE** (phantom subject 1) | **1 vs 0, DIVERGE** (phantom object 10) | 0 vs 0, agree |
| D2 | fix variants on D1 world | 0 vs 0, agree | 0 vs 0, agree | - |
| D3 | world rebuilt as [(1,902,10),(3,902,40)], stale buckets (t14 analog) | unfixed 1 vs 0 DIVERGE; fixed 0 vs 0 agree | unfixed 1 vs 0 DIVERGE; fixed 0 vs 0 agree | - |

Diagnostic (post-freeze addition, not a kill bar): on the pristine world the
fix variants return exactly the originals' outputs (D0RETFIX spec=1 =
D0RET spec=1; D0CNTFIX spec=1 = D0CNT spec=1), ruling out a degenerate
always-zero transcription of the fix.

Kill-bar adjudication: K1 prereg 685f9b57c committed before any
implementation file (verified git log order). K2 safebin, no python3/python,
pinned znc. K3 builds clean, exit 0, empty stderr. K4 D0 all agree=1. K5 D1
ret/cnt agree=0 with vfy agree=1. K6 D2/D3 fix variants agree=1, unfixed D3
diverge. K7 3/3 byte-identical. K8 kb iteration counts identical between spec
and fix (kbs=2 both). K9 ASCII-only, no world literals in rb_fix.zag, one
fn main. **9/9 PASS.**

## Tested findings

1. **The finding is real and isolated.** D1 changes nothing but the relation
   field at one slot. The divergence (ret_spec emits subject 1 from fact
   (1,902,10); cnt_spec counts object 10 from the same fact) is caused solely
   by the missing relation check, not by index-shift staleness. H1 confirmed.
2. **`vfy_spec` is immune because it revalidates the bucket key.**
   It checks fs==s, fr==r, fo==o per slot; on D1 it correctly returns 0.
3. **The fix works and is behavior-preserving on healthy worlds.** H2
   confirmed. D2/D3: fix variants agree with generics everywhere; D0:
   fix == original outputs exactly.
4. **The fix costs zero loop iterations.** kb check-counter deltas are
   identical (kbs=2) for spec vs fix on every stage. Per-slot delta is one
   get32 plus two flag compares by source inspection; nesting depth is
   unchanged from the originals (match flags hoisted, body gated on the
   combined flag).

## Reasoned analysis (not directly tested; argued from the tested results)

### Impact: what failures it causes, what it masks

The missing check turns stale buckets from a fail-silent mechanism into a
fail-wrong one. Without the relation check, a drifted world yields FALSE
POSITIVES: wrong-relation facts returned and counted as matches. With the
check, the same drift yields only FALSE NEGATIVES (misses). For a learner,
confident wrong data is strictly worse than detectable absence: a miss can
trigger re-learning, while a phantom fact can be learned from, acted on, and
propagated into persistent state.

Quantified on tested drifts: D1 gives +1 phantom subject and +1 phantom
count against a true 0 (unbounded relative error on a zero base). The DA
battery's t14 is the same phenomenon at scale: spec count 2 vs generic 0.

What it masks: in the DA battery, t14's divergence LOOKS like pure coverage
staleness but is partly an artifact of the missing check. With the fix, t14
becomes spec 0 vs generic 0 (no disagreement; the probe never fires), because
the relation check filters the stale slots. t15 (stale 603-buckets seeing
only deleted-relation facts, spec 0 vs generic 2) is a positional-miss
divergence and is unaffected by the fix. So the DA verdict stands, but t14
conflates two distinct staleness failure modes (wrong-relation pollution vs
positional miss) that the fix separates.

### Bug or design limitation

Design limitation with bug-like symptoms. Under the implicit contract
"buckets are valid only for the world snapshot they were built on", the
relation check is redundant and its absence is a valid optimization. But that
contract is nowhere enforced: there is no epoch, generation counter, or
snapshot validation at query time, and the coverage contracts gate on
relation MEMBERSHIP, which is a strictly weaker condition than world
identity. Code that relies on an unenforced contract will eventually run
outside it; the DA drift battery is the deliberate demonstration.

The general principle the code violates: **a spec function must revalidate
every field the query constrains, using the bucket only as a candidate
filter.** The bucket key (relation) IS a query-constrained field.
`vfy_spec` obeys the principle (the chain constrains all three fields);
`ret_spec`/`cnt_spec` do not.

Honest scope limit: the fix does NOT make specs correct on drifted worlds.
Positional staleness still causes misses (a fact with the right relation
moving out of its bucketed slot is invisible to the spec). The fix converts
fail-wrong into fail-silent; it does not restore correctness. Full
robustness would need snapshot/epoch tagging (refuse when the world changed),
which is a follow-up lane, not this one.

### Fix cost

- Performance (tested): zero added loop iterations; per-slot +1 get32 + 2
  flag compares. Bucket scans remain the optimized path (2 slots vs 4 facts
  here; 16 vs 56 in the DA battery). Negligible.
- Complexity: about 6 lines per function, no new state, no new failure
  modes, nesting depth unchanged.
- Battery cost (reasoned): adopting the fix REQUIRES amending the DA
  battery. t14 must be redesigned to a positional-staleness-only divergence
  (the t15 pattern), because the current t14 depends on the false positive.
  Without the amendment, the DA battery's K5 (16/16) would drop to 15/16,
  not because attribution got worse but because one staged collision stops
  colliding. Do NOT merge the fix into `da_learn.zag` without that amendment.

### Honest verdict: benign or serious

- **For the DA BUILD-PASS: benign.** The attribution (COV) is correct on
  every trial; the divergence is genuine; the verdict stands. The finding
  was correctly scoped as follow-up material.
- **For TNN's continuing-learner direction: moderate, worth fixing.**
  Worlds that change over time are the point of a continuing learner, and
  the coverage contracts cannot detect in-place world change (they check
  relation membership, not world identity). Silent false positives are the
  worst failure mode for such a learner. The fix is cheap, strictly improves
  the failure mode (fail-wrong to fail-silent), and is behavior-preserving on
  healthy worlds (tested). Recommend adoption with the DA amendment above.

## Recommendations

1. Adopt relation revalidation in `ret_spec`/`cnt_spec` (the `rb_fix.zag`
   variants, or the stated general principle) as a learner-code change.
2. Amend the DA battery first: redesign t14 to a t15-style positional-miss
   divergence so K5's 16/16 remains meaningful after the fix.
3. Follow-up lane: snapshot/epoch tagging for spec validity (refuse on world
   change) as the deeper fix for positional staleness; the relation check
   alone leaves misses.
4. Keep `rb_fix.zag` out of `da_learn.zag` until (2) is done.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  `znc_linux_x86_64_abed8aa1`; no Python invoked at any point.
- The REAL `da_learn.zag` was used byte-unmodified; only the harness, world,
  and fix variants are new. The finding is confirmed against the actual code
  under investigation, not a reimplementation.
- One post-freeze diagnostic was added (D0 fix-equivalence lines); no frozen
  kill bar was changed. Documented here transparently.
- Repro: `rb_build.sh` assembles `rb_full.zag`, builds with the pinned znc,
  runs 3x, checks byte-identity and all kill bars. All sources and logs are
  in this lane directory.
