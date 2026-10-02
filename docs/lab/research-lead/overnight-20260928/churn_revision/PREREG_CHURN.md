# PREREG: Newcomer-Churn Revision Experiment
## Does the continuing learner churn useful-but-not-yet-queried knowledge too aggressively?

Worker: Newcomer-Churn Revision Worker
Date: 2026-09-30 PDT
Status: FROZEN. No implementation exists at this commit. Any implementation commit must be a strict descendant of this commit.

## 0. Step 0 name-check (standing rules, LOOP_STATE.md)

Applicable: (1) PURE ZAG ONLY - all implementation, harnesses, and analysis are pure Zag; zero Python anywhere including scratch; authoring Python is a violation even if never executed. (2) Pure-Zag red line scope - fixture provisioning counts as loop work; all fixtures are Zag-generated in-battery, no external data. (3) Shell-only byte checks - em/en dash checks use only worker_snippets/check_no_dash.sh, never python3. Not applicable: image judge (no image work). Fork testing is a wave-level rule, noted as out of scope for this single experiment. These are honored by construction below.

## 1. Relation to prior work

LEARNER-STRESS-PASS (prereg 4ca3a7196, addendum e16897bc9, implementation daa9bf2fc): one persistent learner, 8 phases, retention 8/8, correction uptake 5/5 with 0/12 collateral, interference resistance 8/8, delayed reuse 5/5. Honest mechanism finding from that run: in pressure wave 2, the consequence policy churned 19 of 20 never-queried newcomers rather than displacing anything useful; new knowledge must earn retention through use (the 6 dynamically-useful junk rules all survived both floods).

Open revision hypothesis (adopted from the stress worker): useful-but-not-yet-queried knowledge may be acquired too slowly, because items that WOULD prove useful later are churned before their first query, so the learner can never discover their utility. This experiment tests that hypothesis directly.

## 2. Architecture (frozen, inherited from the stress battery)

One Zag program, one process, one main(), 6 sequential phases. The learner exposes exactly two operations and never receives phase labels, task IDs, or mode flags: learn(subj, rel, obj) and query(subj, rel, expected). Integer-coded episodes. Single store, capacity 36. Rule record: 11 i32 fields, 44 bytes (subj, rel, obj, correct, wrong, dependents, contradictions, last_used_tick, taught_tick, superseded_obj, valid). Importance = 10*(correct - wrong) + 5*dependents - 8*contradictions + 1. Revision in place on contradiction. Retrieval exact-match only (disclosed v1 scope limit, inherited).

Learner core (helpers, learn, query, twohop, storehash) is copied byte-identical from stress_learn.zag at daa9bf2fc (lines 1-220, everything before fn main). Only two changes are permitted: (a) a frozen const POLICY: i32 selecting the eviction tie-break (see section 3); (b) a new main() implementing the 6 phases below. No other learner-code changes.

## 3. The two arms (frozen)

Arm 0 CONTROL (POLICY=0): current consequence policy, ties broken FIFO: among minimum-importance valid slots, evict the LOWEST slot index (replace best only on strictly lower importance).

Arm 1 LIFO-TIE VARIANT (POLICY=1): identical in every respect except the tie-break: among minimum-importance valid slots, evict the HIGHEST slot index (replace best on importance <= best). Rationale: among unproven items, the newest arrival absorbs newcomer-vs-newcomer churn, so pre-existing newcomers keep a window in which to prove useful. This is the cleanest one-line policy change that directly addresses the hypothesis. No importance formula change, no new fields, no grace timers.

The variant source is generated from the control source by changing only the const POLICY line (via sed at build time); both sources are committed. Both arms run the identical 6-phase trajectory.

## 4. Frozen lifetime trajectory (identical for both arms)

Token codes. Foundation (12, queried 2x each in C1, importance 21): (1,10)->4, (1,11)->5, (2,10)->4, (2,12)->1, (3,10)->2, (4,12)->2, (5,11)->2, (6,10)->8, (7,10)->3, (8,12)->5, (9,10)->1, (9,11)->7.

C1 FOUNDATION: teach the 12 foundation rules; query each twice. Probe recall, expect 12/12.

C2 NEWCOMERS: teach 10 Group A earned newcomers (10..19, rel 30)->subj; query each twice (importance 21). Teach 10 Group B sleepers (40..49, rel 20): (40,20)->4, (41,20)->9, (42,20)->2, (43,20)->7, (44,20)->5, (45,20)->1, (46,20)->8, (47,20)->3, (48,20)->6, (49,20)->0. Sleepers are NEVER queried in C2 (importance 1). Store holds 32 rules. Snapshot: count valid slots by rel (20, 30, 99).

C3 PRESSURE WAVE: teach 30 flood items (300..329, rel 99)->subj, never queried (importance 1). 4 fill free slots 32..35; 26 evictions follow. Snapshot by rel after the wave. STATEHASH.

C4 DELAYED FIRST-USE PROBE: query each of the 10 sleepers exactly once with its taught obj as expected. SURV_SLEEP = number answering correctly (a churned sleeper returns -2, counted as not survived). Then 4 two-hop compositions routing through sleeper premises (frozen expected signs): (40,20)=4 vs (3,10)=2 -> 1; (41,20)=9 vs (1,10)=4 -> 1; (42,20)=2 vs (6,10)=8 -> -1; (43,20)=7 vs (9,10)=1 -> 1. COMP_FIRST = score /4. STATEHASH.

C5 RECOVERY: for each sleeper currently absent from the store, re-teach it with learn(). RELEARN_OPS = number of re-learns performed. Record every eviction victim by class (flood rel 99 / earned rel 30 / foundation rel 10-12 / sleeper rel 20). Re-run the 4 compositions: COMP_RECOV /4. (In an arm with zero churn this phase is a deterministic no-op.)

C6 FINAL PROBE: query all 12 foundation rules (FOUND_FINAL /12); query all 10 Group A rules (EARNED_FINAL /10); count flood retained; report FOUND_EVICT flag; STATEHASH.

## 5. Frozen predictions

Control arm: after C3, sleepers 0/10 (FIFO tie-break churns the 10 oldest importance-1 slots, which are the sleepers, before churning flood items among themselves), Group A 10/10, foundation 12/12, flood retained 14/30. C4: SURV_SLEEP 0/10, COMP_FIRST 0/4. C5: RELEARN_OPS 10, all 10 victims flood (0 earned, 0 foundation), COMP_RECOV 4/4. C6: FOUND_FINAL 12/12, EARNED_FINAL 10/10, FOUND_EVICT 0.

LIFO-tie variant: after C3, sleepers 10/10 (each flood evicts the highest-index importance-1 slot, i.e. the previous flood item; sleepers in lower slots are never touched), Group A 10/10, foundation 12/12, flood retained 4/30. C4: SURV_SLEEP 10/10, COMP_FIRST 4/4. C5: RELEARN_OPS 0, COMP_RECOV 4/4. C6: FOUND_FINAL 12/12, EARNED_FINAL 10/10, FOUND_EVICT 0.

## 6. Frozen kill bars

CHURN-REVISION-PASS requires ALL of K1 through K3. Any failure is CHURN-REVISION-FAIL. No partial credit.

- K1 (prereg precedence): this prereg commit strictly precedes the implementation commit, verified with git merge-base --is-ancestor.
- K2 (churn question answered): (a) both arms complete all 6 phases; (b) never-queried vs queried newcomer churn rates measured (SURV_SLEEP, Group A survival) against the frozen predictions; (c) first-probe utility measured (COMP_FIRST /4 both arms); (d) recovery cost measured (RELEARN_OPS, victims by class, COMP_RECOV); (e) the policy-fine falsifier is evaluated: if control SURV_SLEEP >= 5/10, the churn hypothesis is REJECTED for this regime (my FIFO analysis was wrong), the verdict reports "policy is fine", and no variant adoption is recommended regardless of the variant outcome; (f) variant superiority bar: the LIFO variant is recommended for adoption only if variant SURV_SLEEP > control SURV_SLEEP AND variant FOUND_FINAL == 12/12 AND variant EARNED_FINAL == 10/10 (no protection purchased with earned blood) AND the control arm matched its frozen predictions (otherwise the comparison is confounded).
- K3 (purity and determinism): pure Zag, zero Python at every step; 3/3 byte-identical runs per arm (same binary, exit 0, zero stderr); no em dashes in any documentation (byte-verified with check_no_dash.sh).

## 7. Governance

- Pure Zag only: implementation, build, runs, all analysis (grep/cmp/sha256sum only). No Python anywhere including scratch.
- No em dashes in any documentation (byte-verified with check_no_dash.sh).
- Owned paths only: docs/lab/research-lead/overnight-20260928/churn_revision/. Files: PREREG_CHURN.md (this file), churn_learn.zag, churn_learn_lifo.zag, CHURN_RESULT.md, CHURN_RAW_OUTPUT.txt.
- Binaries built only in /tmp, never staged.
- This worker reports CHURN-REVISION-PASS or CHURN-REVISION-FAIL only, with an honest finding (churn too aggressive / policy fine) and a justified recommendation. No promotion claims; those require the full 11-step frontier pipeline.
- Authored infrastructure not claimed as learned: two-hop comparison operator, phase sequencing, integer episode coding, exact-match retrieval, the POLICY tie-break constant itself (a researcher-set build flag, not learned).
- Scope limits disclosed: exact-match retrieval only; integer-coded episodes; synthetic world; the variant is a researcher-authored policy change, not learner-invented.
- Baseline record: this battery runs against the current (pre-DDES) continuing learner.
