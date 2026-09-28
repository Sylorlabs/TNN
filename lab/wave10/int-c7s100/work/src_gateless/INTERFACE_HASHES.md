# INTERFACE_HASHES.md — INT-1 organ source interfaces

SHA-256 of each organ module's source file as delivered (2026-09-20).
The interface IS the file's public function signatures; hashing the whole
file pins both signatures and their documented refusal codes. Any future
edit changes the hash.

| Organ | File | Lines | SHA-256 |
|---|---|---|---|
| O1 memory | `o1_memory.zag` | 246 | `00876f2c4e9ccc56a4f3401b85af314b7139343b058f7fedd0ce4c8f9f58c780` |
| O2 eliminate | `o2_eliminate.zag` | 219 | `e467cf8369199db090571c88ae3c092a4145902164ac14340dfc8da2b7d7eebf` |
| O3 consolidate | `o3_consolidate.zag` | 184 | `210fcd174eb7ea07a2fab42f01af2d5ba05ead83a0d3a3288b8592373e4116de` |
| O4 recall | `o4_recall.zag` | 402 | `0ca077c8cac8805269d9453b553278c606c208bc256a6d3c96593f58b1c3186e` |
| O5 govern | `o5_govern.zag` | 282 | `0295e8ddcd3553bd177b1931b456600fa05774986a802f1a1b7d0f648e01968a` |

Public signatures (all take the organ state `*O#S` first — imported Zag
modules cannot hold mutable globals):

- O1: `o1_init(cap,audit_cap)→O1S`, `o1_add(o,epi,out_slot)`, `o1_pin(o,slot,force)`, `o1_unpin(o,slot)`, `o1_kill(o,slot)`, `o1_kill_evidenced(o,slot,arm)`, `o1_promote(o,slot)`, `o1_demote(o,slot)`, `o1_evidence(o,slot,code,cite_ep)`, `o1_set_stage(o,stage)`, `o1_new_episode(o)`, `o1_legal_victims(o)`, `o1_victim_candidates(o,exclude_lo,slots_out,str_out,max)`, `o1_snap(o,&w1..&w5)`, `o1_replay_check(o)`
- O2: `o2_init(cap)→O2S`, `o2_open_claim(o,id,gen_ep)`, `o2_observe(o,id,dir)`, `o2_verdict(o,id,&v)`, `o2_disconnect(o)`, `o2_open_count(o)`, `o2_replay_check(o)`
- O3: `o3_init()→O3S`, `o3_consolidate(o,id)`, `o3_condemn(o,id)`, `o3_revive(o,id)`, `o3_preempt(o,candidates,n,strengths,obs,out)`, `o3_replay_check(o)`
- O4: `o4_init()→O4S`, `o4_need(o,qid,req_ent,req_ops,prov,max_age,kind,just,out)`, `o4_scan(o,need_id)`, `o4_compose(o,need_id,out)`, `o4_apply(o,trace_id,cue,out)`, `o4_abstain(o,need_id)`, `o4_replay_check(o)`
- O5: `o5_init()→O5S`, `o5_inspect(o,id,&v)`, `o5_propose(o,id,nv,pred)`, `o5_justify(o,cid)`, `o5_commit(o,id)`, `o5_refuse(o,id)`, `o5_rollback(o,id)`, `o5_replay_check(o)`

Verification: `sha256sum o{1..5}_*.zag` in `impl/` must reproduce the table.
