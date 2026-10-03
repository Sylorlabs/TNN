# SPEC-EPOCHTAG: PREREGISTRATION

**Lane:** docs/lab/research-lead/overnight-20260928/spec_epochtag/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent finding:** SPEC-RELATIONBLIND REPORT.md recommendation 3: "Follow-up
lane: snapshot/epoch tagging for spec validity (refuse on world change) as the
deeper fix for positional staleness; the relation check alone leaves misses."
SPEC-RELATIONBLIND BUILD-PASS (9/9) converted fail-wrong into fail-silent via
relation revalidation. This lane tests whether epoch/snapshot tagging converts
fail-silent into explicit refusal, at what cost, and what it costs when the
world change does not affect the answer.

## Hypotheses

- **H1:** Tagging each bucket with the world epoch at specialization time, and
  refusing (return miss plus an explicit refusal signal) when the live world
  epoch differs at query time, converts fail-silent into explicit refusal on
  every world-change type tested, including the positional staleness (E3, the
  t14 analog) that the relation check cannot fix. No phantom data is ever
  emitted on a changed world.
- **H2 (cost):** The epoch check adds zero loop iterations: kb iteration counts
  are identical between the original spec and the epoch-tagged spec on the
  pristine world. Per-call cost is O(1): two get32 loads plus one compare,
  verified by source inspection.
- **H3 (tradeoff):** The per-world epoch is conservative by design: a world
  change that does not affect the query answer still triggers refusal (E1).
  This is the documented granularity cost of world-identity tagging, not a
  mechanism failure.

## Design

One binary `et_bin` assembled from the REAL `da_base.zag`, `da_module.zag`,
`da_learn.zag` (unmodified, from the disagreement_attribution lane), the REAL
`rb_fix.zag` (unmodified, from the spec_relationblind lane), plus lane-local
files. `da_learn.zag` is NOT modified; this lane does not merge anything into
it.

- `et_world.zag`: world-epoch management. The world arena (4096 bytes) uses
  offsets 0 (nf) and 4..772 (64 facts x 12 bytes); offset 772 is verified free
  (no use in da_base/da_module/da_learn). `et_epoch_get` reads A[772];
  `et_epoch_bump` increments it. `et_drift_unrelated` changes ONLY slot 2's
  object (30 -> 31, a relation-902 fact no query touches) and bumps the epoch.
  `et_drift_relswap` / `et_drift_deletion` wrap the relationblind drifts
  (`rb_drift_relswap`, `rb_drift_deletion` from rb_world.zag, reused
  unmodified) with an epoch bump. All world literals for the new drift live
  here.
- `et_spec.zag`: epoch-tagged variants. NO world literals here. Tag slots in
  L are at 13300+bi*4 (ret), 13364+bi*4 (vfy), 13428+bi*4 (cnt); verified free
  (highest L offset used by da_learn.zag is 13296, telemetry). Each slot holds
  the world epoch at specialization time.
  - `et_specialize_ret/vfy/cnt`: call the real `specialize_*`, then stamp the
    current world epoch into all 16 tag slots of that region.
  - `et_ret_spec` / `et_cnt_spec`: coverage check first (bi<0 returns -1, same
    as the originals); then epoch check. On mismatch: increment the refusal
    counter, write miss (out count 0 / seen reset), return 0 WITHOUT scanning
    the bucket. On match: delegate to `ret_spec_fix` / `cnt_spec_fix` (the
    relationblind variants: epoch gating composes with field revalidation).
  - `et_vfy_spec`: per-chain-step coverage + epoch pre-scan (bi<0 returns -1;
    any tag mismatch refuses with counter increment and return 0), then
    delegates to the real `vfy_spec`.
- `et_main.zag`: harness `main`. Builds learner state once via the real
  coverage logging plus `et_specialize_*` on the pristine tiny world
  (slots 0..3 = (1,901,10), (2,901,20), (1,902,30), (3,902,40); buckets
  901 -> {0,1}, 902 -> {2,3}; world epoch 0; tags 0). Then runs stages:
  - **E0 control** (no drift): RET(901,10), CNT(901, subj 1), VFY((1,901,10)).
    Expect et values identical to the originals, agree=1, refuse=0.
  - **E1 unrelated drift** (slot 2 object 30 -> 31; epoch 0 -> 1): the correct
    answers are unchanged. Expect fix variants still correct (spec=1,
    agree=1); et variants REFUSE (spec=0, refuse=1). Documents the
    conservative-refusal cost (H3).
  - **E2 relation drift** (in-place relation change at slot 0: 901 -> 902;
    epoch 1 -> 2): expect originals to show the relationblind phantom
    (RET/CNT spec=1 vs gen=0, agree=0), fix variants to fail silent
    (spec=0, agree=1), et variants to REFUSE (spec=0, refuse=1, kbs=0).
  - **E3 deletion-shift** (t14 analog: rebuild A as [(1,902,10),(3,902,40)]
    with stale buckets; epoch 2 -> 3): expect originals to diverge
    (agree=0), fix variants to fail silent (spec=0, agree=1), et variants to
    REFUSE (spec=0, refuse=1, kbs=0). This is the fail-silent -> refuse
    conversion on positional staleness.
- The kb check-counter delta is recorded per call; a separate refusal counter
  cell records refusal events per et call.

## Frozen kill bars

| Bar | Requirement |
|-----|-------------|
| K1 | This prereg (+ NAMECHECK.md) committed alone before any `et_*.zag` / `et_build.sh` (git log order). |
| K2 | Toolchain guard: PATH=$HOME/safebin, `which python3`/`which python` empty, pinned znc at $HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1. |
| K3 | `et_bin` builds with no compiler errors; exit 0; empty stderr on all runs. |
| K4 | E0: E0RET_ET spec=1 agree=1 refuse=0; E0CNT_ET spec=1 agree=1 refuse=0; E0VFY_ET spec=1 agree=1 refuse=0. et values identical to the originals on the pristine world. |
| K5 | E2: originals reproduce the phantom (E2RET agree=0 spec=1; E2CNT agree=0 spec=1); fix variants fail silent (E2RET_FIX agree=1 spec=0; E2CNT_FIX agree=1 spec=0); et variants REFUSE (E2RET_ET spec=0 refuse=1 kbs=0; E2CNT_ET spec=0 refuse=1 kbs=0; E2VFY_ET spec=0 refuse=1). |
| K6 | E3: originals diverge (E3RET agree=0; E3CNT agree=0); fix variants fail silent (E3RET_FIX agree=1 spec=0; E3CNT_FIX agree=1 spec=0); et variants REFUSE (E3RET_ET spec=0 refuse=1 kbs=0; E3CNT_ET spec=0 refuse=1 kbs=0; E3VFY_ET spec=0 refuse=1). |
| K7 | 3/3 byte-identical stdout across runs. |
| K8 | Cost: kb iteration counts identical between original spec and et spec on E0 (E0RET kbs == E0RET_ET kbs; E0CNT kbs == E0CNT_ET kbs). The epoch check adds zero loop iterations; per-call cost is two get32 plus one compare, verified by source inspection. |
| K9 | Zero em/en-dash bytes in lane files; `et_spec.zag` contains no 901/902 literals; exactly one `fn main` in `et_full.zag`. |
| K10 | E1 conservative cost: fix variants stay correct (E1RET_FIX spec=1 agree=1; E1CNT_FIX spec=1 agree=1) while et variants refuse (E1RET_ET spec=0 refuse=1; E1CNT_ET spec=0 refuse=1), proving refusal is triggered by world identity, not by answer-affecting change. |

## Verdict rule

BUILD-PASS iff K1..K10 all PASS. A K5 failure falsifies H1 on relation drift
(the tag does not gate). A K6 failure falsifies H1 on positional drift (the
deeper-fix claim). A K8 failure falsifies H2 (the check is not free in loop
iterations). K10 documents H3 either way: if et does NOT refuse on E1, the
epoch is not per-world and the design claim is falsified.

## Out of scope (analytical only, marked as reasoned in REPORT.md)

Whether per-relation (finer) epochs would beat per-world epochs, integration
into the live learner loop, DA battery amendment sequencing, and whether
refusal should surface to a caller-visible retry/re-specialize protocol.
These are argued from the tested results, not tested here.
