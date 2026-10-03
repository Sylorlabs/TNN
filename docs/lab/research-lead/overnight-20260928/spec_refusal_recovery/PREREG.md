# SPEC-REFUSAL-RECOVERY: PREREG (frozen)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_refusal_recovery/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent result:** SPEC-EPOCHTAG BUILD-PASS (10/10), 2026-10-03.

## Hypothesis

H1: A refusal-recovery protocol (refuse -> re-specialize the refused bucket
family from the current world -> retry once) restores spec/gen agreement on
drifted worlds. Correctness after recovery means agree=1 with the generic
spec, NOT spec=1: on answer-changing drift the correct answer changes.

H2: Recovery fires ONLY on explicit refusal (refusal-counter delta), never on
a silent miss. A miss with matching epoch is a legitimate answer, not a
staleness signal, and must not trigger a rebuild.

H3: Recovery is repeatable, not one-shot. After recovery restamps tags to
epoch N, a further drift to epoch N+1 refuses again and recovers again.

H4: Recovery cost is one-time per drift per bucket family. After recovery,
subsequent calls on the same drifted world hit with no new refusal and no
new re-specialize.

## Protocol (frozen design, implemented in rr_spec.zag)

```
rr_ret_spec(L,S,A,rel,obj,kb,ko,out,oo,rkb,rko,spb,spo):
  r0 = get32(rkb,rko)
  v  = et_ret_spec(L,A,rel,obj,kb,ko,out,oo,rkb,rko)
  if get32(rkb,rko) == r0: return v        // hit or silent miss: no recovery
  et_specialize_ret(L,S,A,0,0)             // rebuild buckets, restamp epoch
  set32(spb,spo,get32(spb,spo)+1)          // re-specialize event counter
  return et_ret_spec(L,A,rel,obj,kb,ko,out,oo,rkb,rko)   // single retry
```

Identical shape for rr_cnt_spec (et_specialize_cnt) and rr_vfy_spec
(et_specialize_vfy). Single retry only: a second refusal on retry is returned
as-is (a second-order failure the kill bars would catch, not silently looped).

The wrappers reuse, byte-unmodified: da_base.zag, da_module.zag,
da_learn.zag (NOT modified, DA battery untouched), rb_world.zag, rb_fix.zag,
et_world.zag, et_spec.zag. Only rr_spec.zag (wrappers) and rr_main.zag
(harness) are new.

## World, queries, drifts (identical to SPEC-EPOCHTAG)

Tiny world slots 0..3 = (1,901,10), (2,901,20), (1,902,30), (3,902,40).
Queries: RET (rel 901, obj 10), CNT (rel 901, subs [1]), VFY (chain
[(subj1, rel 901, obj 10)]). Drifts, each bumping the world epoch:
E1 unrelated (slot 2 obj 30->31, epoch 0->1; answers unchanged),
E2 relation swap (slot 0 rel 901->902, epoch 1->2; RET/CNT/VFY gen all 0),
E3 deletion rebuild [(1,902,10),(3,902,40)] (epoch 2->3; RET/CNT/VFY gen 0).

Per-line counters: refuse and resp (re-specialize events) are RESET to 0
before every emitted line, so each line states its own delta.

## Frozen expected values

| Line | spec | gen | agree | refuse | resp | kbs |
|------|------|-----|-------|--------|------|-----|
| E0RET_RR | 1 | 1 | 1 | 0 | 0 | >0 |
| E0CNT_RR | 1 | 1 | 1 | 0 | 0 | >0 |
| E0VFY_RR | 1 | 1 | 1 | 0 | 0 | >0 |
| E0MISS_ET (et_ret 901,99) | 0 | - | - | 0 | - | X>0 |
| E0MISS_RR (rr_ret 901,99) | 0 | - | - | 0 | 0 | =X |
| E1RET_ET | 0 | - | - | 1 | - | 0 |
| E1RET_RR | 1 | 1 | 1 | 1 | 1 | >0 |
| E1RET_RR2 (amort.) | 1 | 1 | 1 | 0 | 0 | >0 |
| E1CNT_RR | 1 | 1 | 1 | 1 | 1 | >0 |
| E1VFY_RR | 1 | 1 | 1 | 1 | 1 | >0 |
| E2RET_ET | 0 | - | - | 1 | - | 0 |
| E2RET_RR | 0 | 0 | 1 | 1 | 1 | >0 |
| E2RET_RR2 (amort.) | 0 | 0 | 1 | 0 | 0 | >0 |
| E2CNT_RR | 0 | 0 | 1 | 1 | 1 | >0 |
| E2VFY_RR | 0 | 0 | 1 | 1 | 1 | >0 |
| E3RET_ET | 0 | - | - | 1 | - | 0 |
| E3RET_RR | 0 | 0 | 1 | 1 | 1 | >0 |
| E3CNT_RR | 0 | 0 | 1 | 1 | 1 | >0 |
| E3VFY_RR | 0 | 0 | 1 | 1 | 1 | >0 |

Key predictions to note: E2/E3 recovery lines have spec=0 (the drifted world
genuinely contains no (901,10) fact); correctness is agree=1. E3RET_ET must
refuse again even though E2's recovery restamped the tags: the stamp is the
live epoch (2), and E3 bumps to 3. E0MISS_RR must NOT re-specialize (resp=0)
because a fix miss with matching epoch is an answer, not staleness.

## Frozen kill bars

- K1: This prereg is committed strictly before any implementation file
  (rr_spec.zag, rr_main.zag, rr_build.sh, outputs). Verified by git log
  order: the prereg commit's hash precedes the implementation commit.
- K2: safebin PATH mandatory; `which python3` and `which python` return
  nothing; pinned znc znc_linux_x86_64_abed8aa1 builds the binary.
- K3: znc builds clean; binary exits 0 on all 3 runs; stderr empty on all 3.
- K4 (E1 recovery restores correctness): E1RET_RR / E1CNT_RR / E1VFY_RR each
  spec=1, agree=1, refuse=1, resp=1.
- K5 (E2 recovery restores agreement after answer-changing drift):
  E2RET_RR / E2CNT_RR / E2VFY_RR each spec=0, gen=0, agree=1, refuse=1,
  resp=1, kbs>0. Fails if re-specialize does not rebuild from the current
  world (stale buckets would phantom: agree=0) or if the retry still
  refuses.
- K6 (decision rule, no recovery on silent miss): E0MISS_RR spec=0,
  refuse=0, resp=0, and kbs(E0MISS_RR) == kbs(E0MISS_ET). Fails if the
  wrapper re-specializes on any miss.
- K7 (repeatability): E3RET_ET refuses again (refuse=1, kbs=0) after E2's
  recovery restamped tags; E3RET_RR / E3CNT_RR / E3VFY_RR each spec=0,
  gen=0, agree=1, refuse=1, resp=1. Fails if recovery is one-shot or the
  restamp corrupts the tag.
- K8 (one-time cost / amortization): E1RET_RR2 and E2RET_RR2 each refuse=0,
  resp=0, with spec/agree identical to the corresponding RR line. Fails if
  the tag does not match after recovery.
- K9 (recovery does real work): kbs>0 on every RR recovery line
  (E1/E2/E3 x RET/CNT/VFY) while the matching ET refuse-only line has
  kbs=0. Fails if recovery is a no-op.
- K10: 3/3 byte-identical stdout (cmp across rr_run1/2/3.txt).
- K11: ASCII-only lane sources; no world literals in rr_spec.zag /
  rr_main.zag (grep for 901/902); exactly one fn main in rr_full.zag.

Verdict rule: BUILD-PASS requires 11/11. Any single bar failure is
BUILD-FAIL with the failing bar named.

## Cost question (to be answered in REPORT, reasoned from measured data)

Does recovery restore correctness, and at what cost? Measured: refuse path
kbs=0 (O(1), no bucket scan) vs recovery retry kbs>0 plus one full bucket
rebuild per family (re-specialize scans the world; counted as resp events,
not kb, since specialize takes no kb counter). Amortization lines show the
rebuild is paid once per drift per family. The E1 stage prices the
conservative-refusal cost carried into recovery: a rebuild paid for answers
that were already correct.
