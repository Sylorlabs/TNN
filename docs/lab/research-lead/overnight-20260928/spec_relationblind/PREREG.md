# SPEC-RELATIONBLIND: PREREGISTRATION

**Lane:** docs/lab/research-lead/overnight-20260928/spec_relationblind/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent finding:** DISAGREEMENT-ATTRIBUTION REPORT.md Finding 3: `cnt_spec` and
`ret_spec` are relation-blind at bucketed slots (they verify the queried
subject/object but not the relation id); `vfy_spec` correctly checks all three
fields. The DA battery's kind-4 trials (t14/t15) were designed around this.

## Hypotheses

- **H1:** On a world where ONLY the relation field at a bucketed slot changes
  (no index shift, no deletion, same fact count), `ret_spec` and `cnt_spec`
  return wrong-relation facts as false positives while the researcher-supplied
  generics do not; `vfy_spec` agrees with its generic. This isolates
  relation-blindness from positional staleness.
- **H2:** Adding a relation-id revalidation (`fr==rel`) to `ret_spec`/`cnt_spec`
  restores spec==generic agreement on such drifted worlds, with no added loop
  iterations.

## Design

One binary `rb_bin` assembled from the REAL `da_base.zag`, `da_module.zag`,
`da_learn.zag` (unmodified, from the disagreement_attribution lane) plus
lane-local files:

- `rb_world.zag`: tiny world + drift constructors. All world literals live here.
  Tiny world: slots 0..3 = (1,901,10), (2,901,20), (1,902,30), (3,902,40).
- `rb_fix.zag`: `ret_spec_fix` / `cnt_spec_fix`, exact copies of the real spec
  functions with a relation revalidation added. Experimental variants only;
  NOT merged into `da_learn.zag`.
- `rb_main.zag`: harness `main`. Specializes all three families via the real
  `specialize_ret` / `specialize_vfy` / `specialize_cnt` after logging rels
  901, 902, then runs stages:
  - **D0 control** (no drift): RET(901,10), CNT(901, subj 1), VFY((1,901,10)).
    Expect spec==generic on all three.
  - **D1 drift** (in-place relation change at slot 0: 901 to 902; nothing else
    changes): expect RET spec=1 vs gen=0, CNT spec=1 vs gen=0, VFY spec=0 vs
    gen=0.
  - **D2 fix on D1 world**: `ret_spec_fix` / `cnt_spec_fix` expect 0 vs 0.
  - **D3 deletion-shift** (t14 analog): rebuild A as [(1,902,10),(3,902,40)]
    with stale buckets: unfixed RET/CNT expect 1 vs 0; fix variants expect
    0 vs 0.
- The kb check-counter delta is recorded per call for the cost analysis.

## Frozen kill bars

| Bar | Requirement |
|-----|-------------|
| K1 | This prereg (+ NAMECHECK.md) committed alone before any `rb_*.zag` / `rb_build.sh` (git log order). |
| K2 | Toolchain guard: PATH=$HOME/safebin, `which python3`/`which python` empty, pinned znc at $HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1. |
| K3 | `rb_bin` builds with no compiler errors; exit 0; empty stderr on all runs. |
| K4 | D0: RET agree=1, CNT agree=1, VFY agree=1. |
| K5 | D1: RET agree=0, CNT agree=0, VFY agree=1 (core repro of the finding). |
| K6 | D2: RETFIX agree=1, CNTFIX agree=1. D3: unfixed RET agree=0, CNT agree=0; RETFIX agree=1, CNTFIX agree=1. |
| K7 | 3/3 byte-identical stdout across runs. |
| K8 | kb iteration counts identical between spec and fix variants on D1 (the fix adds no loop iterations); per-slot op delta bounded to one get32 plus flag compares, verified by source inspection. |
| K9 | Zero em/en-dash bytes in lane files; `rb_fix.zag` contains no 901/902 literals; exactly one `fn main` in `rb_full.zag`. |

## Verdict rule

BUILD-PASS iff K1..K9 all PASS. A K5 failure falsifies H1 (the DA finding does
not reproduce in isolation from index-shift staleness). A K6 failure falsifies
H2 (relation revalidation is insufficient to restore agreement).

## Out of scope (analytical only, marked as reasoned in REPORT.md)

Impact on the live learner loop, bug-vs-design-limitation judgment, fix cost
beyond the measured kb deltas, and whether the DA battery needs amendment.
These are argued from the tested results, not tested here.
