# SPEC-EPOCHTAG: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_epochtag/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (10/10 frozen kill bars)**

## Summary

Implements the deeper fix recommended by SPEC-RELATIONBLIND: epoch/snapshot
tagging so specs refuse on world change. Each bucket is tagged with the world
epoch at specialization time (world epoch counter at world-arena offset 772;
tags at L+13300/13364/13428 per bucket, all verified free); every spec call
compares the live epoch against the tag and REFUSES on mismatch (increments an
explicit refusal counter, returns a miss, never scans the bucket). Built on the
real `da_base.zag` + `da_module.zag` + `da_learn.zag` (byte-unmodified) plus the
real `rb_fix.zag` variants (unmodified); `da_learn.zag` is NOT modified and the
DA battery is untouched. Results: on the pristine world the et variants behave
byte-identically to the originals (same values, same kb counts, refuse=0); on
relation drift (E2) and deletion drift (E3, the t14 analog) they refuse where
the originals emit phantoms and the fix variants fail silent; on an unrelated
drift (E1) they refuse even though the fix stays correct, documenting the
conservative-refusal cost of per-world epochs. The epoch check adds zero loop
iterations (kb identical on E0) and short-circuits before the bucket scan
(kbs=0 on refused calls). All binaries pure Zag, safebin-built, 3/3
byte-identical.

## What was tested (do not treat the reasoned sections as tested)

The experiment assembles the real `da_base.zag` + `da_module.zag` +
`da_learn.zag` from the disagreement_attribution lane (byte-unmodified) and the
real `rb_world.zag` + `rb_fix.zag` from the spec_relationblind lane
(byte-unmodified) with lane-local `et_world.zag` (epoch counter at A[772],
epoch-bumping drifts), `et_spec.zag` (epoch-tagged variants), `et_main.zag`
(harness). Repro: `./et_build.sh` in this directory.

Tiny world: slots 0..3 = (1,901,10), (2,901,20), (1,902,30), (3,902,40).
Learner state built once via the real `specialize_*` wrapped by
`et_specialize_*` (stamps world epoch 0 into all bucket tags); buckets:
901 -> {0,1}, 902 -> {2,3}.

| Stage | Condition | RET orig / fix / et | CNT orig / fix / et | VFY orig / et |
|-------|-----------|---------------------|---------------------|---------------|
| E0 | pristine (control) | 1 / 1 / 1, refuse=0 | 1 / 1 / 1, refuse=0 | 1 / 1, refuse=0 |
| E1 | slot 2 obj 30->31 (unrelated) | 1 / 1 / REFUSE | 1 / 1 / REFUSE | 1 / REFUSE |
| E2 | slot 0 relation 901->902 | phantom 1 / silent 0 / REFUSE | phantom 1 / silent 0 / REFUSE | 0 / REFUSE |
| E3 | world rebuilt [(1,902,10),(3,902,40)] | phantom 1 / silent 0 / REFUSE | phantom 1 / silent 0 / REFUSE | 0 / REFUSE |

(REFUSE = spec value 0, refuse=1, kbs=0: the bucket was never scanned.)

Kill-bar adjudication: K1 prereg ea055ab0a committed before any implementation
file (verified git log order). K2 safebin, no python3/python, pinned znc. K3
builds clean, exit 0, empty stderr on all 3 runs. K4 E0 et values identical to
originals, refuse=0 everywhere. K5 E2 phantoms reproduced (agree=0), fix
silent (agree=1, spec=0), et refuses (refuse=1, kbs=0). K6 E3 same pattern on
positional drift. K7 3/3 byte-identical (sha256
e478df9869eb41224b8fedc2efe2db94de014aee0db42e9c26a89516a82e03a4).
K8 kb identical between original and et on E0 (kbs=2 / kbs=2). K9 ASCII-only,
no world literals in et_spec.zag/et_main.zag, one fn main. K10 E1 fix correct
(spec=1, agree=1) while et refuses (spec=0, refuse=1). **10/10 PASS.**

## Tested findings

1. **Fail-silent converts to refuse, on every drift type tested.** E2 (relation
   drift): originals fail-wrong (phantom 1 vs 0), fix fails silent (0 vs 0),
   et refuses (0, refuse=1). E3 (deletion drift, t14 analog, positional
   staleness the relation check cannot fix): same triple. H1 confirmed.
2. **Refusal fires before any fact is read.** Refused calls show kbs=0: the
   epoch gate short-circuits ahead of the bucket scan. The refusal is not a
   post-scan miss; it is a pre-scan veto.
3. **Zero behavior change on healthy worlds.** E0: et values, first elements,
   and kb counts are identical to the originals; refuse=0 on all et calls.
   This rules out a degenerate always-refuse transcription and any
   healthy-world regression. H1's control holds.
4. **The epoch check costs zero loop iterations.** K8: kb counts identical
   between original spec and et spec on E0 for RET and CNT. Per-call cost by
   source inspection: two get32 loads (world epoch, tag) plus one compare,
   O(1) per call, no new state machine, no added nesting. H2 confirmed.
5. **The per-world epoch is conservative by design.** E1: a drift that changes
   no query answer (slot 2 object 30->31, relation 902 never queried) leaves
   the fix variants correct (spec=1, agree=1) while et refuses (spec=0,
   refuse=1). Refusal is triggered by world identity, not by
   answer-affecting change. H3 confirmed as documented cost, not mechanism
   failure.
6. **The refusal counter is load-bearing.** On E2/E3 the et spec value (0) is
   numerically identical to the fix variant's silent miss (0); only
   refuse=1 vs the absent flag distinguishes explicit refusal from silent
   miss. Without the observable refusal signal, the fail-silent to refuse
   conversion would be unmeasurable.

## Reasoned analysis (not directly tested; argued from the tested results)

### Impact: what failures it prevents, what it costs

The tested failure-mode ladder on a changed world is now complete:
fail-wrong (original spec: phantom data, the worst mode for a continuing
learner) -> fail-silent (relation check: miss, better, but the spec still
claims knowledge of a world it cannot see) -> refuse (epoch tag: explicit
"I cannot answer; the world moved"). Each step is strictly more honest than
the last: a miss can trigger re-learning, a refusal can trigger
re-specialization, but a phantom can be learned from, acted on, and
propagated into persistent state before anyone notices.

What it costs: (a) compute: O(1) per call, zero loop iterations, measured;
(b) granularity: any world mutation invalidates every bucket, including
mutations irrelevant to the query (E1). The E1 result quantifies the price of
coarse world-identity tagging. A per-relation epoch would refuse less often
but needs per-relation version tracking: more machinery, more failure modes,
and a new staleness surface (the version table itself). For a continuing
learner, coarse refusal is the safe default; precision can be bought later
with measured evidence, not assumed up front.

### Bug or design limitation (of the baseline)

Design limitation with bug-like symptoms, same family as the relationblind
finding. Under the implicit contract "buckets are valid only for the world
snapshot they were built on", no epoch check is needed. That contract was
nowhere enforced: no epoch, generation counter, or snapshot validation at
query time. The epoch tag enforces the contract mechanically. The general
principle: **a cached structure must carry the identity of the world it was
derived from, and every use must revalidate that identity.** The bucket key
is a candidate filter; the epoch is a validity proof.

Honest scope limit: epoch tagging does NOT restore correctness on drifted
worlds. It converts wrong/silent into refusal; the learner still needs a
re-specialize (or re-learn) protocol to recover answers after refusal. That
protocol is follow-up work, not this lane. Also untested: epoch wraparound
(i32 overflow after 2^31 bumps; irrelevant at any realistic drift rate but
noted), and multi-world (one learner, several arenas) tagging, where the tag
must name the world as well as its epoch.

### Battery cost

Adopting epoch tagging REQUIRES amending the DA battery before merge, for the
same reason the relationblind report gave: t14's staged divergence depends on
the current behavior. With epoch tags, t14 becomes refuse (not a spec/generic
disagreement about content), and t15 likewise. The DA battery's kill bars
count content disagreements; refusal is a different verdict category and the
battery has no bar for it. Do NOT merge into `da_learn.zag` without that
amendment. This lane merges nothing: `da_learn.zag` is byte-unmodified and
the et variants live entirely in lane-local files.

### Honest verdict: benign or serious

- **For the DA BUILD-PASS: benign.** Nothing in this lane changes the DA
  verdict; it is a separate experimental lane by construction.
- **For TNN's continuing-learner direction: serious and worth adopting (with
  the battery amendment).** Worlds that change over time are the point of a
  continuing learner. Silent false positives are the worst failure mode such
  a learner can have, and silent misses are second-worst when they masquerade
  as knowledge. The epoch check is O(1), adds no loop iterations, needs no
  new modes/bridges/handlers, and composes with field revalidation (the et
  variants gate the fix variants, not the originals). The conservative
  granularity is a real cost, honestly measured in E1, and the right default
  until a finer scheme earns its complexity.

## Recommendations

1. Adopt epoch/snapshot tagging as the validity mechanism for all
   learner-built index structures (the et_spec.zag pattern: stamp at build,
   gate at use, refuse with an observable signal), composed with the
   relationblind field revalidation.
2. Amend the DA battery first: t14/t15 need refusal-aware kill bars (refusal
   is a verdict category, not a content disagreement) before any merge into
   `da_learn.zag`.
3. Follow-up lane: the refusal recovery protocol. What does the learner do
   after refuse? Options to test: targeted re-specialize of the refused
   bucket, epoch-scoped re-learn, escalating to full re-specialize. Measure
   recovery cost vs. staleness window.
4. Follow-up experiment (not lane): per-relation vs per-world epoch
   granularity. E1 prices the coarse scheme; a finer scheme must beat it on
   measured refusal precision without adding a new staleness surface.
5. Keep `et_spec.zag` / `et_world.zag` out of `da_learn.zag` until (2) is done.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  `znc_linux_x86_64_abed8aa1`; no Python invoked at any point.
- The REAL `da_learn.zag`, `da_base.zag`, `da_module.zag` were used
  byte-unmodified; the REAL `rb_world.zag`/`rb_fix.zag` from the
  spec_relationblind lane were used byte-unmodified. Only the epoch
  machinery, the et variants, and the harness are new.
- Memory-layout verification before implementation: A[772] free (facts end at
  772); L tag slots at 13300/13364/13428 free (highest da_learn.zag offset is
  13296, telemetry). A colliding first choice (13280) was caught by grep
  before any code was written.
- One hygiene-check iteration during build: a comment in et_main.zag
  mentioned relation literals and tripped the no-literals grep; reworded, no
  frozen bar affected.
- Repro: `et_build.sh` assembles `et_full.zag`, builds with the pinned znc,
  runs 3x, checks byte-identity and all kill bars. All sources and logs are
  in this lane directory.
