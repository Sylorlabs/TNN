# SPEC-PERRELATION-EPOCH: PREREG (frozen)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_perrelation_epoch/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent result:** SPEC-REFUSAL-RECOVERY BUILD-PASS (11/11), 2026-10-03.

## Hypothesis

H1: Per-relation epoch granularity eliminates the E1 rebuild-for-correct-
answers cost. On an unrelated drift (relation 902 changes, relation 901
queries), the per-relation gate hits with refuse=0 and resp=0, while the
coarse per-world scheme in the same run pays refuse=1, resp=1 to restore
answers that were already correct.

H2: The per-relation gate is not degenerate. Queries against the drifted
relation itself still refuse (refuse=1) and recover (resp=1, agree=1).

H3: Answer-changing drifts on the queried relation still refuse and recover
(E2, E3): the finer scheme adds no staleness surface.

H4: Recovery remains repeatable and one-time per drift per family; the
miss/hit decision rule and healthy-world behavior are unchanged.

H5 (complexity): the finer scheme's extra machinery is a bounded per-relation
epoch table (8 bytes per touched relation, capped at 8 entries here) and a
per-call linear scan over at most the table occupancy, versus 1 slot and 1
load for the coarse scheme. It earns this complexity only if H1 holds while
H2/H3 hold.

## Protocol (frozen design)

Per-relation epoch table in the world arena A (offsets verified free; facts
end at 772, the world epoch lives at 772):
- A[776]: entry count (i32)
- A[780+i*8]: relation id; A[784+i*8]: epoch (i32); i in 0..7 (68 bytes max)

Absent relation reads as epoch 0; the first bump creates (rel, 1). The bump
rule (implemented by the drift constructors, which are the world mutators):
bump every relation with at least one fact whose (s,r,o) content changed
(added, removed, or field-modified). This rule is the soundness condition:
a relation whose fact set is untouched keeps its epoch, so its queries hit;
a relation whose fact set changed gets a new epoch, so its queries refuse.

pe_world.zag:
- pe_epoch_get(A, rel): linear scan, return epoch or 0.
- pe_epoch_bump_rel(A, rel): found -> epoch+1; absent and n<8 -> add (rel,1).
- pe_epoch_n(A): entry count.
- pe_drift_unrelated(A): et_drift_unrelated (slot 2 obj 30->31) + bump
  rb_rel_b(). Only the 902 fact set changes: 901 epoch stays 0.
- pe_drift_relswap(A): et_drift_relswap (slot 0 rel 901->902) + bump
  rb_rel_a() + bump rb_rel_b(). A 901 fact leaves, a 902 fact arrives.
- pe_drift_deletion(A): et_drift_deletion (rebuild [(1,902,10),(3,902,40)])
  + bump rb_rel_a() + bump rb_rel_b(). 901 facts are removed; 902's fact
  set changes too ((1,902,31) is gone).

pe_spec.zag (tag slots verified free; et tags end at 13492, L is 16384):
- ret tags at 13500+bi*4, vfy tags at 13564+bi*4, cnt tags at 13628+bi*4.
- pe_specialize_ret/vfy/cnt: call the real specialize_*, then stamp EACH
  bucket's tag with ITS relation's epoch (bucket relation read from the
  da_learn coverage id arrays at L+4 / L+4252 / L+8500).
- pe_ret_spec / pe_cnt_spec: bi=cov_find; bi<0 -> -1; if
  pe_epoch_get(A,rel) != tag -> refuse (refusal counter +1, miss, no scan);
  else the rb_fix variant.
- pe_vfy_spec: per-step pre-scan over chain relations, same gate per step.

pe_rr.zag: recovery wrappers mirroring rr_spec.zag exactly (refuse ->
re-specialize via pe_specialize_* -> single retry; resp counter +1 per
re-specialize; silent misses return as-is).

Reused byte-unmodified: da_base.zag, da_module.zag, da_learn.zag (NOT
modified, DA battery untouched), rb_world.zag, rb_fix.zag, et_world.zag,
et_spec.zag, rr_spec.zag. New lane files only: pe_world.zag, pe_spec.zag,
pe_rr.zag, pe_main.zag, pe_build.sh. The coarse et/rr lines in the harness
(E1RET_ETC, E1RET_RRC, E0RET_ETC) reuse et_ret_spec / rr_ret_spec to price
the coarse scheme in the same run.

## World, queries, drifts (identical tiny world to the parent lanes)

Slots 0..3 = (1,901,10), (2,901,20), (1,902,30), (3,902,40). Queries: RET
(rel 901, obj 10), CNT (rel 901, subs [1]), VFY (chain [(subj1, rel 901,
obj 10)]), plus E1B RET (rel 902, obj 30) against the drifted relation.
Per-line counters reset before every emitted line.

## Frozen expected values

| Line | spec | gen | agree | refuse | resp | kbs |
|------|------|-----|-------|--------|------|-----|
| E0RET_ETC (coarse et) | 1 | - | - | 0 | - | 2 |
| E0RET_PERR | 1 | 1 | 1 | 0 | 0 | 2 (=ETC) |
| E0CNT_PERR | 1 | 1 | 1 | 0 | 0 | >0 |
| E0VFY_PERR | 1 | 1 | 1 | 0 | 0 | >0 |
| E0MISS_PEET (pe 901,99) | 0 | - | - | 0 | - | X>0 |
| E0MISS_PERR (pe_rr 901,99) | 0 | - | - | 0 | 0 | =X |
| E1RET_ETC (coarse et) | 0 | - | - | 1 | - | 0 |
| E1RET_RRC (coarse rr) | 1 | 1 | 1 | 1 | 1 | 2 |
| E1RET_PEET (pe 901,10) | 1 | - | - | 0 | - | 2 |
| E1RET_PERR | 1 | 1 | 1 | 0 | 0 | 2 |
| E1CNT_PERR | 1 | 1 | 1 | 0 | 0 | >0 |
| E1VFY_PERR | 1 | 1 | 1 | 0 | 0 | >0 |
| E1B_PEET (pe 902,30) | 0 | - | - | 1 | - | 0 |
| E1B_PERR | 0 | 0 | 1 | 1 | 1 | 2 |
| EPOCHS_E1 | e901=0 e902=1 n=1 | - | - | - | - | - |
| E2RET_PEET | 0 | - | - | 1 | - | 0 |
| E2RET_PERR | 0 | 0 | 1 | 1 | 1 | 1 |
| E2CNT_PERR | 0 | 0 | 1 | 1 | 1 | >0 |
| E2VFY_PERR | 0 | 0 | 1 | 1 | 1 | >0 |
| E2RET_PERR2 (amort.) | 0 | 0 | 1 | 0 | 0 | >0 |
| EPOCHS_E2 | e901=1 e902=2 n=2 | - | - | - | - | - |
| E3RET_PEET | 0 | - | - | 1 | - | 0 |
| E3RET_PERR | 0 | 0 | 1 | 1 | 1 | 0 (A1-analog) |
| E3CNT_PERR | 0 | 0 | 1 | 1 | 1 | 0 (A1-analog) |
| E3VFY_PERR | 0 | 0 | 1 | 1 | 1 | 0 (A1-analog) |
| EPOCHS_E3 | e901=2 e902=3 n=2 | - | - | - | - | - |

Key predictions: E1RET_PERR pays NO rebuild (resp=0) for answers that were
already correct, while E1RET_RRC in the same run pays resp=1: the measured
E1 cost reduction. E1B proves the gate still fires on the drifted relation
(901-hit + 902-refuse on the same drifted world is the discrimination the
coarse scheme cannot express). EPOCHS lines prove the table holds exactly
the touched relations with the right epochs (n=1 after E1, n=2 after E2/E3;
a wrong epoch would mean spurious refusal or staleness). A1-analog: on E3
the rebuilt 901 buckets are empty, so the retry scans 0 slots; real-work
evidence is resp=1 + agree=1 (inherited from the parent amendment).

## Frozen kill bars

- K1: This prereg is committed strictly before any implementation file
  (pe_world.zag, pe_spec.zag, pe_rr.zag, pe_main.zag, pe_build.sh,
  outputs). Verified by git log order: the prereg commit's hash precedes
  the implementation commit.
- K2: safebin PATH mandatory; `which python3` and `which python` return
  nothing; pinned znc znc_linux_x86_64_abed8aa1 builds the binary.
- K3: znc builds clean; binary exits 0 on all 3 runs; stderr empty on all 3.
- K4 (E1 rebuild cost eliminated): E1RET_PERR / E1CNT_PERR / E1VFY_PERR
  each spec=1, gen=1, agree=1, refuse=0, resp=0; AND E1RET_RRC (coarse, same
  run) refuse=1, resp=1, spec=1, agree=1. Fails if the per-relation scheme
  refuses on the undrifted relation, or if the coarse baseline does not
  reproduce the priced cost.
- K5 (gate not degenerate): E1B_PEET spec=0, refuse=1, kbs=0; E1B_PERR
  spec=0, gen=0, agree=1, refuse=1, resp=1, kbs>0. Fails if drifted-relation
  queries do not refuse (a never-refuse gate would pass K4 trivially).
- K6 (E2 still refuses and recovers): E2RET_PEET spec=0, refuse=1, kbs=0;
  E2RET_PERR / E2CNT_PERR / E2VFY_PERR each spec=0, gen=0, agree=1,
  refuse=1, resp=1, kbs>0. Fails if an answer-changing drift on the queried
  relation does not refuse (staleness surface).
- K7 (repeatability + one-time cost): E2RET_PERR2 spec=0, agree=1,
  refuse=0, resp=0; E3RET_PEET spec=0, refuse=1, kbs=0; E3RET_PERR /
  E3CNT_PERR / E3VFY_PERR each spec=0, gen=0, agree=1, refuse=1, resp=1.
- K8 (decision rule): E0MISS_PERR spec=0, refuse=0, resp=0, and
  kbs(E0MISS_PERR) == kbs(E0MISS_PEET). Fails if the wrapper re-specializes
  on any miss.
- K9 (healthy-world parity): E0RET_PERR spec=1, gen=1, agree=1, refuse=0,
  resp=0, and kbs(E0RET_PERR) == kbs(E0RET_ETC). Fails if per-relation
  tagging changes healthy-world behavior or adds scan iterations.
- K10 (epoch table bounded and correct): EPOCHS_E1 e901=0 e902=1 n=1;
  EPOCHS_E2 e901=1 e902=2 n=2; EPOCHS_E3 e901=2 e902=3 n=2. Fails on any
  wrong epoch (spurious refusal or staleness) or table growth beyond
  touched relations.
- K11: 3/3 byte-identical stdout (cmp across pe_run1/2/3.txt).
- K12: ASCII-only lane sources; no world literals in pe_world.zag /
  pe_spec.zag / pe_rr.zag / pe_main.zag (grep for 901/902); exactly one fn
  main in pe_full.zag.

Verdict rule: BUILD-PASS requires 12/12. Any single bar failure is
BUILD-FAIL with the failing bar named.

## Cost/complexity question (to be answered in REPORT, reasoned from measured data)

Does per-relation granularity reduce the E1 cost, and what does it cost?
Measured: resp events on E1 901 queries (coarse 1 per family vs fine 0),
refuse events (1 vs 0), table occupancy (n=1 after E1, n=2 after E2/E3),
and the structural gate cost (coarse: 1 get32 + compare per call; fine:
linear scan over at most n entries, n<=8 here). The report must state
whether the measured E1 saving earns the table + scan complexity.
