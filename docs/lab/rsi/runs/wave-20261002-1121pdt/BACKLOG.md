# BACKLOG.md: carryover from wave-20261002-1121pdt to the next wave

Priority order. Each item names the lane branch where evidence lives.

1. SENSORY H5 sealed battery + red team + verdict (NO VERDICT this wave). Evidence preserved on lane-sensory-20261002-1121pdt (prereg c9da6ec2e frozen alone, commit-order PASS; smoke results good; 1024 battery script run_h5.sh ready; red-team T2 tool h5_redteam_t2.zag committed). Two runtime kills (restart-drain); needs a clean worker. If all bars pass: sealed blind A/B + JUDGE_BRIEF.md, READY-FOR-JUDGE.
2. HPIREV2 step-7 clean re-freeze (PROCESS-FAIL this wave). Quarantined reference on lane-hpirev2-20261002-1121pdt (40 world files + SHA256SUMS.txt + draft narrowed prereg). Clean 5-step path: re-verify worlds/hashes with safebin only, re-run validator from fresh pure-Zag staging, commit prereg ALONE, commit worlds + validator, build executor, 24 runs.
3. L2ADAPT B/C battery unblock: debug why (11,70,16) EXTEND fails to promote 5-link MAP (top priority); alternatives: direct MAP construction via workspace manipulation; 4-link B/C batteries with fallback-defeating distractors. Then 3x runs + verdict. Candidate A to canonical promotion (debate ADOPTED as L2).
4. INDEX generalized evict-hook walker (new prereg): fixes the sealed 0521pdt base eviction hook kill (viii) (idx_chain_hits hard-codes 102/101 alternation). Distinct from the operand-encoding defect Micah ruled on 2026-10-02.
5. Micah's 2026-10-02 operand-encoding ruling: implement the invariant fix (NODE vs FRAME operands structurally/tagged distinguishable; no guessed magic numbers; apply to t2_guard/t2_set/t2_mov/t2_inc/t2_dec/t2_jnz/res_op + source audit; 7 governance items). Preserve SCALING-5000-FIXED: FAIL as canonical for old frozen build. Continue L2/L3 research in parallel; do not block swarm on scaling lane.
6. DEVANG: multi-draw K_SEAL calibration study (draws noisy: 12, 14, 9); attack the C-family deficit (learner never beats fixed-3 on novel vocab) without researcher-authored semantic cases; independent-adversary replication of K_SEG/K_SEAL/K_ABL.
7. F2: complete run 1 (K6-R4/R5); runs 2-3 for K6-R7 (3/3 byte-identical).
8. DDES step 9 transfer/reuse (sole promotion blocker; audit otherwise 10/11).
9. TNN-3 T-RECLAIM-1 implementation wave (design frozen at 673f5e9d9 with K1-K10; accounting: ~150 lines, 0 semantic cases, 0 modes/bridges/handlers, 3 learner-state structures).
10. ARENA: (a) re-verify toolchain guard before any arena work (IMPAIRED-CLARITY flag from the python3-probe anomaly; debate ruling on record, Micah may overrule). (b) C8 question-indexed absorption; C12 genuine template revision (L2 adaptive reuse); C15 prompt-intent discrimination as 11-step frontier proposal (needs Micah's boundary ruling); C9 harder structures; procedure/goal/language dedicated lanes.
11. F1: relabel R as greedy-trap rate in future citations (debate-adopted correction); optional 2-step-lookahead ablation (1-step vs buffer myopia).
12. znc toolchain fitness review (GOVERNANCE FLAG for Micah): four independent miscompile patterns now documented (as *i32+q[0..n]; _zag_print name/layout; 7-deep nested ifs E0204; !(A && B) in while). Sealed-evaluation fitness question.
13. CONTLEARN: true MAP-transformation rebind (vs fact-level reuse); learner-authored scheduling/gating policy (caveat 3); integrate (a)+(b)+(c) in one continuing learner.
14. TRADES: per-variable-noise forward model (breaks the collider-covers-chain tie); 5+ variable DAGs; structure-neutral tie-break / abstention-on-tie calibration.
15. HPI: re-teach separator family (queued by hpi lane).
16. BATTERY: T-K5/T-K9/T-K11 standing failures (no regression at tip; still failing).
17. Micah's possible overrule on debate Motion 5 (arena guard distinction: deliberate use vs uncorroborated anomaly).

Standing: fork battery over every branch every wave; prereg commit-order self-check; debate with provenance probe; pure Zag; safebin guard with literal evidence.
