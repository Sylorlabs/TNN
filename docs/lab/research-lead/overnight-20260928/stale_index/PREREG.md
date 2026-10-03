# PREREG: STALE-INDEX-RECOVERY (frozen)

Non-ledger task. Lane
`docs/lab/research-lead/overnight-20260928/stale_index/`, file prefix
`si_`. Branch `tnn-native-lab`, commits local only, never pushed.

## 1. Task

Follow-up to the HOOK-COMPOSITION Amendment N1 integration finding. The
L-state spec-procedure indexes (ret/vfy/cnt buckets holding fact indices
into the live world) are world-relative. N1 observed: S10E specialized
on drifted world A2, S12A restored world A without re-specializing, so
`ret_spec` read A2 positions against world-A facts (0 subjects for the
(601,621) need). Self-trigger handled it reactively exactly as designed:
bounded retries, coverage contract retired, generic fallback, agree.

Three questions, answered experimentally here:

- Q1 (signal): can the learner detect stale indexes BEFORE they cause a
  0-subject return? Candidate signals: (a) fact count (live nf vs the nf
  recorded at specialization, already stored at L+4240/8488/12736);
  (b) content checksum (order-sensitive hash over fact triples, recorded
  at specialization); (c) world epoch (a counter bumped on every world
  mutation, recorded at specialization).
- Q2 (recovery): should recovery be proactive (detect, re-specialize,
  then query) or reactive (let the query fail; trigger-B retries,
  retires coverage, falls back to generic)?
- Q3 (cost): what does each path cost, honestly counted?

## 2. Frozen design answers (before implementation)

**A1: fact count is provably insufficient for the N1 case.** World A and
world A2 both hold exactly 56 facts; A2 is a REORDERING of A (603-block,
602-block, 601-block, then the 607/609 tail). The nf signal therefore
cannot see the A2 to A restore coming. The prereg predicts the probe
will show nf_stale=0 while the indexes are stale (SI-P1). Fact count is
retained as recorded metadata but EXCLUDED from the recovery predicate.

**A2: checksum and epoch both detect the N1 case before any spec call.**
The checksum is content-derived (no trust in mutation instrumentation);
the epoch is one compare per spec per query (cheap) but requires every
world-mutating path to bump it (a missed bump is a silent false
negative, the same bug class as N1). The hot-path check uses the epoch;
the checksum stays as stage-level instrumentation and as the audit
signal for uninstrumented changes.

**A3: a per-query checksum check would be a net loss.** One world_ck
pass costs 56 fact visits per spec (168 for three); the spec vs generic
saving per 1-need ret query is about 40 visits (16 indexed vs 56
generic). Checking with the checksum every query costs more than the
index saves. The epoch check costs 3 compares. Proactive recovery is
predicted to beat reactive only in the epoch form, after a short
amortization (SI-K1).

**A4: reactive stays the safety net.** If the epoch instrumentation ever
misses a mutation, checksums disagree silently... no: if the epoch
misses a mutation, NEITHER hot-path check fires, and the query fails
exactly as in N1, handled by trigger-B. The reactive path is therefore
not replaced; proactive is a fast path in front of it.

## 3. Implementation (additive deltas over hc_*, frozen)

- si_base.zag, si_module.zag, si_world.zag: byte-copies of hc_*.
- si_learn.zag: hc_learn.zag plus, all additive:
  - `world_ck(L,A)`: order-sensitive i32 hash over the live fact
    triples (h = h*31+s; h = h*31+r; h = h*31+o per fact, wrapping);
    increments the step counter at L+14012 once per fact visited.
  - `specialize_ret/vfy/cnt`: unchanged logic plus three additive
    stores: checksum at L+14000/14004/14008, epoch (sg(S,931)) at
    L+14024/14028/14032, and one L+14012 step-counter increment per
    fact visited in the build loop.
  - `spec_nf_stale(L,A)`: bitmask bit0/1/2 = live nf != recorded nf
    (L+4240/8488/12736) for ret/vfy/cnt.
  - `spec_ck_stale(L,A)`: bitmask from checksum compare.
  - `spec_ver_stale(L,S)`: bitmask from epoch compare.
  - `spec_ensure_fresh(L,S,A)`: mask = spec_ver_stale; re-specializes
    exactly the stale specs (ep 0,0, the N1/S10E precedent); counts
    each re-specialized spec at L+14016; returns mask.
- si_main.zag: hc_main.zag plus:
  - do_query: after the S+7 tick, `if(sg(S,930)==1){
    spec_ensure_fresh(L,S,A) }`, stashing the entry mask at L+14020.
    S+930 is 0 through Acts 1/2, so the regression is untouched.
  - Act 3 (S12 block, hc_main.zag lines 1494-1581) replaced by Act 4
    (S13A-S13F) below; SUMMARY-HOOKGEN replaced by SUMMARY-SISTALE.
- New state cells (all verified free): S+930 proactive flag, S+931
  world epoch, L+14000/14004/14008 checksums, L+14012 step counter,
  L+14016 respec counter, L+14020 entry mask, L+14024/14028/14032
  epochs, L+14036/14040 arm totals.
- si_build.sh: assemble si_full.zag from the five parts, compile with
  the pinned znc. Pure shell + znc.

### S13A STALE-SETUP (disclosed apparatus)

Read tagC from the live binding directory (pre-existing, runtime
derived). setup_worldA; bump epoch; setup_worldA2; bump epoch;
specialize_ret/vfy/cnt (S10E precedent, contracts active, u_induct
path); setup_worldA (restore WITHOUT re-specialize); bump epoch. The
live world is now A (56 facts) with A2-built indexes: the exact N1
stale condition. Derive r601 = vocab[0], o601 = first_obj(A,r601),
r603 = vocab[2] (all runtime-derived, no world literals), tSI =
tagC+5, gSI = g_tag(mk_goal813_E0)+7, and build the 1-need ret goal GS
via mk_g1need (the S12 G2 shape; oracle_1ret, okind=2).

### S13B SIGNAL-PROBE

Before any spec procedure runs on the restored world, print one line:
`SI-PROBE nf_stale=<m> ck_stale=<m> ver_stale=<m>` with the three
bitmasks (0-7).

### S13C PROACTIVE (epoch-gated)

Snapshot cs/cg (L2+13244/13248) and steps (L2+14012). Set S+930=1.
do_query SIQ0 (plan miss; the inline version check must fire,
re-specialize all three specs, then the query runs on fresh indexes).
Print `SI-AUTO entry_mask=<m>` (the stashed mask). Eight follow-up
queries SIQ1..SIQ8 (plan hits). Clear S+930=0. Print
`SI-COST arm=proactive q=<q> steps=<s> total=<t>` where q is the
cs+cg delta, s the step-counter delta, t = q+s; stash t at L+14036.

### S13D ADVERSARIAL (same-nf content change)

Starting from the S13C end state (world A, fresh A indexes, contracts
active): find the first two facts with rel == r603 (runtime-derived
indices mj0, mj1); copy fact mj1's object over fact mj0's object;
bump epoch. nf stays 56; the SI query's (601,621) answer is untouched.
Print `SI-MUTATE` with the runtime-derived indices. Print the SI-PROBE
line again. Set S+930=1; do_query SIQ0A (plan hit); clear S+930=0.

### S13E REACTIVE (N1 reproduction, proactive off)

setup_worldA; bump; setup_worldA2; bump; specialize x3 (contracts
active, u_induct path); setup_worldA; bump. Snapshot cs/cg/steps AFTER
the setup. S+930 stays 0. do_query SIQ0R (plan hit, stale indexes).
Eight follow-ups SIQ1R..SIQ8R. Print
`SI-COST arm=reactive q=<q> steps=<s> total=<t>`; stash t at L+14040.

### S13F SUMMARY

Print `SI-VERDICT proactive_total=<P> reactive_total=<R>` from the
stashed arm totals, then SUMMARY-SISTALE with the HOOKGEN fields plus
`steps=<L+14012>`.

## 4. Frozen kill bars

- SI-R1 (regression, additive-only): si_run1.txt lines 1-97
  byte-identical to hc_run1.txt lines 1-97 (Acts 1/2/S11).
- SI-P1 (nf falsified, ck+ver confirmed on the N1 reorder): the S13B
  SI-PROBE line is exactly
  `SI-PROBE nf_stale=0 ck_stale=7 ver_stale=7`.
- SI-P2 (same falsification on adversarial same-nf content change):
  the S13D SI-PROBE line is exactly
  `SI-PROBE nf_stale=0 ck_stale=7 ver_stale=7`.
- SI-B1 (reactive reproduces N1): S13E contains exactly 2 RETRY lines;
  SIQ0R appears 3 times with (agree=0,vers=2), (agree=0,vers=2),
  (agree=1,vers=0); RETRY att=1 shows `dc=1,0,0 active=1,1,1`; RETRY
  att=2 shows `dc=2,0,0 active=0,1,1`.
- SI-B2 (proactive recovery): S13C contains zero RETRY lines; SIQ0 is a
  single Q line with st=2 vers=2 agree=1; `SI-AUTO entry_mask=7`.
- SI-B3 (adversarial proactive): S13D contains zero RETRY lines; SIQ0A
  is a single Q line with st=1 vers=2 agree=1.
- SI-K1 (cost): from the two SI-COST lines,
  proactive_total < reactive_total.
- SI-H1 (toolchain/hygiene): safebin from the first command; pure Zag;
  pinned znc; prereg committed alone before implementation; 3/3
  byte-identical runs, stderr empty, exit 0; zero em/en dash bytes; no
  world literals in executable new code (all tags/rels/objs/goals
  runtime-derived).

## 5. Predicted mechanism trace (for the report, not a bar)

- S13C SIQ0: inline check sees epoch 3 vs recorded 2 for all three
  specs (mask 7), re-specializes (3x56 visits), query runs ret_spec on
  fresh A indexes: 16 bucket visits, answer {611}, agree=1 first try.
  Follow-ups: 16 visits each, version check clean.
- S13E SIQ0R: att=1 ret_spec on stale A2 indexes reads A positions
  32..47, 0 subjects, disagree, RETRY att=1 (dc 1,0,0); att=2 same,
  RETRY att=2 (dc 2,0,0, 3000-contract retired); att=3 generic 56
  visits, agree. Follow-ups: 56 visits each, generic, first-try agree.
- Estimated totals: proactive about 168+9x16=312, reactive about
  88+8x56=536. The bar is the inequality, not the estimates.

## 6. What this does NOT claim

- The epoch bump discipline is stage-code instrumentation in this
  experiment, not learner-owned mutation tracking. Learner-owned
  versioning (the world mutator itself stamping the epoch) is a
  follow-up.
- 56 facts is a toy world; the cost inequality is structural
  (per-query check cost vs per-query index saving vs one respec),
  not a scaling result.
- The checksum stays off the hot path here; a periodic checksum audit
  against epoch misses is follow-up work.
