# INT-1 Five-Organ Interface Map (SURVEY — no implementation)

**Date:** 2026-09-20 · **Status:** read-only survey for the implementers. Sources: the organ files listed below; design in `INTEGRATION_DESIGN.md`; prereg in `PREREG_INTEGRATION.md` (V2 does not exist yet).

## O1 — Deliberate memory substrate

**File:** `~/workspace/tnn-lab/wave7/felt-intensity/st_memory_core.zag` (841 lines). `@import("substrate/cl/common.zag")` (relative; build needs `substrate/` alongside).

**Struct:** `StStore` — parallel `[]u8` arrays: `live, pinned, region, tier` (u8 each, per slot), `value/step/st_sclk/pintrainer` (i32 each), `st_str/st_sorg/st_sclk…/st_str` = strength 0..100 (u8), `forcepin` (u8), `cite_n` (u8, ≤ST_CITE_MAX=4), `cite_ep` (i32×4), `justified` (u8), `audit` (i32-packed, 16 words/entry), `audit_n, audit_cap, cap, stage, clock, overflow`.

**Op API** (all `fn st_<op>(s:*StStore, …)i32`, rc=ST_OK or refusal; every path snapshots before/after and appends audit):
- `st_init(cap,audit_cap)StStore` / `st_free` / `st_fingerprint(s,extra)i32` (endpoint fingerprint)
- `st_add(s,value,region,strength,out_slot:*i32)` — needs stage≥ADD; strength 0..100; d1=strength, d2=region
- `st_strengthen/st_weaken(s,slot,strength,code)` — stage≥MANAGE, code∈ST_J_1..7 enum; two of the four legal strength-write paths
- `st_trainer_declare(s,slot,strength,note)` — origin=HUMAN, stage≥MANAGE; reversible by TNN later
- `st_evidence(s,slot,code,cite_ep)` — stage≥KILL; distinct episodes per slot (DUPCITE); citation rides in d2
- `st_justify(s,slot,code)` — stage≥KILL; sets justified flag
- `st_kill_evidenced(s,slot,arm)` — arm==ST_ARM_B **skips** effort/justification; otherwise needs n(s)=⌈s/25⌉ distinct cites + justify; s>50 needs stage≥FULL
- `st_kill(s,slot)` — MA1-verbatim kill (stage≥KILL; ignores strength) = arm-B semantics
- `st_overwrite(s,slot,value,strength,arm)` — pays full erase effort first (Micah's law), then re-adds
- `st_force_pin/st_force_unpin(s,caller,trainer,slot)` — caller MUST be ST_CALLER_TRAINER else ST_REFUSED_EXTERNAL_ONLY; re-pin idempotent, unpin requires original trainer id
- `st_pin/st_unpin/st_promote/st_demote` (stage≥MANAGE); `st_set_stage`; `st_abandon` (recording-only); `st_rollback_last` (restores last mutating op's before-snapshot, skips recording ops)
- Independent checkers: `st_audit_clean_refusals` (refused ⇒ before==after), `st_replay_check` (replay-from-genesis == live), `st_no_pinned_kills`, `st_core_intact` (slots 0,1 live CORE), `st_forcepintag_ok`, `st_evidence_audit` (n(cites)==n(strength-at-kill) at every KILL_EVIDENCED), `st_cite_consistent`

**Refusal codes:** ST_OK=0; 101 CORE / 102 PINNED / 103 NOTLIVE / 104 FULL / 105 STAGE / 106 BADSLOT / 107 AUDITFULL / 108 NOROLLBACK / 120 EFFORT / 121 JUSTIFY / 122 DUPCITE / 123 EXTERNAL_ONLY / 124 OCCUPIED / 125 NOTFORCEDPIN / 126 BADCODE / 127 BADSTRENGTH. Stages: NONE=0 ADD=1 MANAGE=2 KILL=3 FULL=4. Regions: CORE=0 USER=1. Tiers: SHORT=0 LONG=1.

**Audit entry (16 words, i32-packed):** `op@0, slot@4, rc@8, b1@12, b2@16, b3@20, b4@24, b5@28, a1@32, a2@36, a3@40, a4@44, a5@48, stage@52, d1@56, d2@60`. b1=live|pinned<<8|tier<<16|region<<24; b4=strength|origin<<8|forcepin<<16|trainer<<24; b5=strength clock. Audit fail-close: `audit_n>=audit_cap` ⇒ overflow=1, ST_REFUSED_AUDITFULL.

**Arm-B (uniform) configuration:** nothing in the store differs — it is a *call-site* parameter. Arm B = call `st_kill(s,slot)` (or `st_kill_evidenced(s,slot,ST_ARM_B)` with ST_ARM_B=1) so the n(s)=⌈s/25⌉ effort/justification gates are bypassed; strength is still recorded at add-time (judged value) but ignored by the kill gate. All other gates (stage, CORE, pinned/force-pin) still apply. Precedent: `wave5/strength-trial-run/trial/strength_learner.zag:171` — `if(c.*.arm==LR_ARM_B){rc=st_kill(s,vic);}`. The strength trial's own st_memory_core (`wave5/strength-trial-run/trial/st_memory_core.zag`) is the same lineage; the integration copy is the wave7 one above.

## O2 — Eliminative hypothesis logic (minimal core ONLY; HDE v1 excluded)

**Validation source:** `~/workspace/tnn-lab/wave6/attribution-ablation/VERDICT.md` — load-bearing: (a) eliminative hypothesis-state verification, (b) learner-initiated `SIGNAL_DISCONNECT`, (c) deliberative standards (myopic 10× took 21 vs 0 intact). Ledger/checker/provenance are architecture (prove, don't prevent).

**Core mechanics file:** `~/workspace/tnn-lab/wave4/scaffold-release/sr.zag` (287 lines):
- Ops (audited): SR_OP_EPISODE=1, SR_OP_SCAFFOLD=2, SR_OP_ELIMINATE=3, SR_OP_COMMIT=4, SR_OP_DISCONNECT=5, SR_OP_REFUSE=6, SR_OP_PIN=7, SR_OP_UNCOMMIT=8
- `sr_episode(live,committed,next_probe,nctx,nact,connected,*streak,*ctx,action,signal,step,abuf,acount)` — contradiction branch (signal==-1 while connected): ELIMINATE candidate; if sole survivor ⇒ COMMIT; if none survive ⇒ UNCOMMIT (revive all, revoke commitment, restart probes). +1 signal builds `streak` toward SR_STABLE_K=8
- `sr_legal(committed,connected,streak,nctx)` — disconnect allowed iff connected && all contexts committed && streak≥8
- `sr_disconnect(committed,connected,*streak,nctx,step,abuf,acount)` — **learner-initiated**, audit-first, fail-closed (failed append ⇒ channel stays live); refuses SR_ALREADY / SR_UNVERIFIED
- `sr_replay` (re-derive state from audit), `sr_audit_count_op*` helpers; audit 16 bytes/entry, SR_AUDIT_CAP=256
- Return codes: SR_OK=0, SR_BAD=-360101, SR_RANGE=-360102, SR_UNVERIFIED=-360103, SR_ALREADY=-360104, SR_AUDIT_FULL=-360105

**Corroborated-elimination defense:** `~/workspace/tnn-lab/wave5/redteam-rt2/trial/rt2_def.zag` (35/35 vs sustained spoofing): first −1 on a COMMITTED hypothesis audits SR_OP_SUSPECT=9 (held for corroboration, streak reset, hypothesis stands); second consecutive −1 ⇒ ELIMINATE; +1 re-read ⇒ SR_OP_EXONERATE=10. Uncommitted probes still die on a single −1. **Integrate this variant, not base sr.zag.**

**Verdict representation:** HDE's claim-state enum (from `wave3/hypothesis-driven-exploration/impl/hyp_core/learner_core.zag:42-44`): 0 EMPTY, 1 DORMANT, 2 OPEN, 3 TESTING, 4 CONFIRMED, 5 REFUTED, 6 ARCHIVED. The HDE *machinery* (h_surprise, h_arm, cross-context x-states) trialed NEGATIVE — **do not port it**; keep only the state vocabulary and the sr.zag/rt2_def.zag elimination core. The design's CONFIRM/REFUTE/ARCHIVED verdicts = states 4/5/6 above.

**Minimal native re-implementation:** per-context `live[]/committed[]/suspect[]`, `connected`, `streak`; episode rule (contradict→suspect/exonerate→eliminate; commit survivor; uncommit on total refutation); `sr_legal` gate; learner-called `sr_disconnect`; audited op log with replay; deliberative-standard refusal rule from the wave-6 ablation (long-horizon horizon check — extract from `ablate.zag` fire-rule logic).

## O3 — Deliberate consolidation/promotion

**File:** `~/workspace/tnn-lab/wave3/r27-consolidation/impl/psm.zag` (345 lines; imports nothing — isolated by design).

**Struct:** `Psm` with fast tier (`nf` slots × stride 9: FF_USED/ID/OP/PARAM/VER/CTX/UNV/AGE/PROM), slow tier (`ns` × stride 5: FS_USED/ID/OP/PARAM/CONF), history (stride 4: op/id/reason/step; `dropped` counter).

**Ops:**
- CONSOLIDATE (`psm_consolidate`): deliberate mode=1, event-driven, fires when `ver>=V_MIN(=6)` **and** `popcnt(ctxmask)>=CTX_MIN(=2)` — the cross-context corroboration gate. Slow is first-verified-wins per id (conflict ⇒ HR_CONFLICT_KEEP, candidate settles); slow-full ⇒ HR_SLOW_FULL (defers, settles — **never evicts**)
- CONDEMN (`psm_condemn`, HR_UNVERIFIED): ver==0 && unv>=UNV_DISCARD(=8) && age>=AGE_DISCARD(=8); slot becomes tombstone (FF_USED=2), stays matchable
- PREEMPT: in `psm_observe` — if fast full, evicts the **most-discredited never-verified tombstone** (max UNV), audited HR_PREEMPTED
- REVIVE: a condemned form that verifies flips back to candidate, audited HR_REVIVED
- `psm_probe(id,…)` — highest-confidence slow skill answers (tie: lowest index); `psm_digest` — slow-tier digest for determinism gates

**⚠️ CONFIRMED: silent drop.** `psm_observe`, fast full and no tombstone victim:
```zag
} else {
    p.*.dropped=p.*.dropped+1;
    return 1;
}
```
It increments `dropped` and returns 1 — the observation is lost; nothing forces the caller to handle the return. This is the victim-deadlock seam risk: the integrated PREEMPT **must** be pin- and strength-aware (current victim pick ignores both; no organ-1 calls exist in this file at all) and must refuse audibly (ST_refusal-style code) rather than dropping silently. Design §5.3 requires exactly this.

**What the integrator must add:** every tier movement routed through O1 ops (`st_promote/st_demote` for SHORT↔LONG, `st_kill/st_kill_evidenced` for eviction victims, `st_pin` for protected slow entries). psm.zag has no O1 coupling today — it is pure logic to be wired across the seam.

## O4 — Symbolic recall + trace composition

**Recall core:** `~/workspace/tnn-lab/wave3/deliberate-recall/trial/recall_core.zag` (353 lines).
- **⚠️ Import mismatch:** `@import("../../../wave2/memoryagency/trial/memory_core.zag")` — it builds on the **MA1 `MaStore`, not the ST `StStore`**. The integrator must port it to the integrated O1 store (or wrap it); a cross-tree relative import must not survive integration.
- Need declaration: `rc_need_declare(rs,qid,req_ent,req_ops,prov,max_age,compose,just,out_id)` — needs live in a table (RC_NEED_CAP=64); SAFETY_CRITICAL needs force composed? (rc_attach policy: comment at line 102)
- Need-scan: `rc_predmask` computes the **Boolean P1∧P2∧P3∧P4** bitmask (RC_P1=1 entity-match, RC_P2=2 op-coverage, RC_P3=4 provenance-ok, RC_P4=8 age-ok; RC_PALL); `rc_recall(rs,s,need_id,out,cap)` scans live attached slots in index order, every scan decision audited with its mask; compose mode selects by marginal symbolic contribution (no scores)
- ABSTAIN: `rc_act` returns **-1** unless the union of selected ops covers req_ops AND all agree on the action code — audited as RC_KIND_ACT
- Per-slot trace descriptors via `rc_attach(rs,s,slot,ent,ops,src,ver,act)`; `rc_replay_check` rebuilds from its own 6-word ledger (RC_AUDIT_WORDS=6, RC_AUDIT_CAP=2048)

**Trace composition:** `~/workspace/tnn-lab/wave3/trace-composition/comp.zag` (667 lines).
- Trace record (TC_TR_SZ=92 bytes): id@0, verified@4, provenance@8, nops@12, sources@16, sup@20, kind@24, ops@28 (8×8). Capacities: TC_MAX_OPS=8, TC_MAX_TRACES=64, TC_MAX_NAMES=32 (+scratch 32). Opcodes OP_FILTER_GT=1, OP_MAP_MUL=2, OP_NAMED=3; PROV_NONE=0, PROV_SELF_VERIFIED=1, PROV_COMPOSED=2, PROV_TAMPERED=99
- Composition-time verification: `comp_seq(store,a,b,out)` / `comp_branch(store,pred,th,el,out)` / `comp_abstract(store,reg,t,name)` — ALL refuse COMP_UNVERIFIED_LINK=2101 unless every input passes `tc_link_ok` (verified); branch also requires predicate-class (2102 COMP_NOT_PREDICATE); name collision ⇒ 2103; capacity ⇒ 2105; out must not alias inputs
- Blind execution: `comp_apply(store,reg,t,cue,out)` — **"checks NOTHING about verifiedness"** (file's own comment); verification is enforced at composition time only, by design

**Serving-trace pinning:** the phrase does not exist in any implementation file. Recall core reads the store read-only (rc_recall "Read-only on the ma store"); the only pins are O1's `st_pin`. Answer: **no serving-trace pinning exists** — and what does exist (O1 pins) has no expiry (only `st_unpin`/force-unpin clears them). The integrator must design the O4→O1 pin call and its expiry policy; it is not in the organ code.

## O5 — Native structural revision

**File:** `~/workspace/tnn-lab/wave7/reasoning-control/trial/rc_trial.zag` (482 lines). Design: `REASONING_CONTROL.md` (208 lines). Imports the integrity ledger (`il_*.zag` — `il_observe/il_verify/il_claim/il_check/il_refute/il_refused`).

**Op API** (all `fn rc_<op>(s:*RcSys,…)i32`): `rc_init`, `rc_audit(s,op,a,b,c,d)` (RC_WORDS=6, RC_AUDIT_CAP=2048), `rc_episode` (verification episode), `rc_reveal`, `rc_inspect(s,param)` (INSPECT: returns value + provenance audit index), `rc_simulate` (counterfactual: replays recorded episodes under V=2, returns pred_bad), `rc_rcommit(s,param,new_val,pred_bad,j0,j1)` (PROPOSE+COMMIT gate), `rc_rrollback(s,param)` (ROLLBACK to prev), `rc_stage_advance` (evidence-gated: ≥8 consecutive IL_OK → stage FULL), `rc_replay`, `rc_count_bad`. RC op codes: EPISODE=1 … INSPECT=7, PROPOSE=8, RCOMMIT=9, RREFUSE=10, RROLLBACK=11, STAGE=12, REVEAL=13, PARAMINIT=14.

**Gate directions** (class derived from direction, never trusted): V↑ = constructive (no extra gate); R↑ = neutral; V↓/R↓ = **destructive** — needs stage≥FULL **and** two distinct ledger justifications (j0≠j1, valid audit indices) **and** pred_bad ≤ last_bad (non-degrading prediction). Refusals: RC_REF_STAGE=201, RC_REF_JUST=202, RC_REF_PRED=203, RC_REF_CONST=204 (constitution param RC_P_CONST=9 + unknown params ⇒ RC_REF_CONST; every refusal audited).

**Parameters governed:** V (RC_P_V=1, verification bar) and R (RC_P_R=2, calibration R). S (refusal counter, init RC_S0=50, grows by R per refusal, capped RC_SMAX=150) is NOT commit-governable. **Elimination strictness, disconnect criteria, and self-model cadence are in the design (§1) but NOT implemented** — only V and R exist; the parameter register must be extended natively for INT-1.

**Verification-bar mechanics:** `rc_episode`: if V≥2 ⇒ deep path (OBSERVE → DEEPCHECK → VERIFY → claim cites OBSERVE+VERIFY → il_check → CHECKVERDICT → COMMIT; defect ⇒ REFUSE, ROLLBACK-in-effect, S+=R). If V<2 ⇒ thin path (no VERIFY). Post-commit verification is real: `rc_count_bad` over CHECKVERDICT entries; a lying self-change that passed the gate was caught here and rolled back (trial 40/40).

## Curriculum multiplicands (10× base)

**⚠️ Gap:** `wave3/developmental-curriculum/PILOT_RESULTS.md` covers **DC-1 only**:
- DC-1-S1: 64 episodes + 24 settle, 4 partitions, audit cap 2048
- DC-1-S4: 256 + 56 settle, 16 partitions, audit cap 16384 (the largest completed pilot)
- DC-1-S16 (64 cap, 32 regimes, 1024 episodes) was "next step" — **never ran**

`CURRICULUM.md` gives scale-dimension guidance but no pilot multiplicands: DC-0-S10 (80 slots, 640-ledger, 10× op volume), DC-2-S10 (40 traces), DC-3-S10 (10 sequential revisions), DC-4-S10 (20-way hypotheses, 16→160→1600 probes/phase), DC-5-S10 (10× silent episodes, 10 world changes); DC-2 "not yet piloted". **INT-1 needs Micah's amendment on DC-0/2/3/4/5 multiplicands — the prereg's "read verbatim from PILOT_RESULTS.md" works for DC-1 only.** Table-killers (bind every stage): zero RNG in AI decision paths; no pointwise endpoint regression vs stage-entry snapshot; ledger continuity.

## Seven-control battery (EVALUATION_PROTOCOL.md §6; restated verbatim in PREREG_INTEGRATION.md §5)

- Entry gates: **G0** no RNG in decision paths (static grep) · **G1** one-lineage continuity (`newborn_restarts==0`) · **G2** byte-identical paired reruns · **G3** sealed harness (frozen+hashed pre-run) · **G4** trace-machinery soundness (B001 fix) · **G5** novelty floor ≥ L2
- **C1** disabled-agency: freeze O1 add/kill/pin/promote/demote + O5 REASON_*; ±1 probe survival ⇒ agency DEAD
- **C2** disabled-composition: block compose; DC-2/DC-4 gates survive ⇒ composition DEAD
- **C3** scrambled-provenance: permute provenance, keep content; survives ⇒ MEMORIZATION verdict (O4 recall)
- **C4** scrambled-structure: permute op order; survives ⇒ composition-illusion (O4)
- **C5** memory-lesion: accepted-partition-only / candidate-only / killed-traces-only; killed-traces-only above chance ⇒ LEAKAGE alarm (O1 partitions broken)
- **C6** null-system harness check: replay-last/do-nothing must score 0/16 else battery VOID
- **C7** teacher-withdrawal (specified, never run): authorship/lineage break or collapse vs DC-4 ⇒ teacher-dependence, autonomy claim DEAD

## Toolchain constraint checklist (from ~/AGENTS.md)

1. Audit entry = 16 words: op@0, slot@4, rc@8, b1–b5@12..28, a1–a5@32..48, **stage@52, d1@56, d2@60** (NOT d1@52)
2. No single slice > 2^25 bytes (33,554,432) may be indexed — even `a[0]` panics above it → chunk large buffers (audit ledgers); equivalence proven by byte-identical reruns
3. `[]u8` slice `==` is NOT identity (`h==d` false even when aliasing) — use integer selectors, never slice comparison
4. Large-struct indexed field access is mishandled by codegen (`w.*.field[i]`) — alias to a local slice first
5. `st_snap` takes **5 out-pointers** (`&b1..&b5`), no return struct
6. `st_add` takes an **out-slot `*i32`**; `st_evidence(s,slot,code,cite_ep)` takes citation episode; `cl_check` (not cl_check_i32) is the check helper
7. `@import("…")` must be a **bare** directive — `//`-commented imports are silently ignored
8. `_zag_arg(n)` returns a NON-OWNED pointer — never `nio_free` it; `_zag_strcmp(a,b)` returns **1** on equality
9. **`substrate/cl/common.zag` itself imports `../R33_NATIVE_SHA256_V2.zag`** — the trial substrate dir needs `R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` next to `cl/`, or compile fails. Relative `@import("substrate/cl/common.zag")` ⇒ build must place `substrate/` alongside the source/binary

## Missing / unusable — with fallbacks

1. **DC-0/2/3/4/5 curriculum multiplicands missing** (only DC-1 piloted). Fallback: use CURRICULUM.md's S10 scale-test dimensions as provisional multiplicands pending Micah's amendment.
2. **O4's recall core imports MA1's `MaStore`** (wrong store) — port to the integrated O1 store before use; do not keep the cross-tree relative import.
3. **O3's `psm.zag` has no O1 coupling and drops silently on victim deadlock** — wire tier movement through O1 ops and give PREEMPT an audible refusal; victim selection must become pin/strength-aware (currently max-UNV tombstone only).
4. **O5 governs only V and R** — elimination strictness, disconnect criteria, self-model cadence must be added as natively governable params (per the design's parameter list).
5. **"Serving-trace pinning" exists nowhere** — design language; O1 pins have no expiry. The O4→O1 pin seam + expiry policy needs a dated design decision.
6. **PREREG_INTEGRATION_V2.md does not exist** — V1 (`PREREG_INTEGRATION.md`) is current.
