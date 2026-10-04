# Shared Substrate Expansion: Design

## Goal

Drive 5 behaviors from ONE shared consequence substrate (build
fa8405a90), with per-behavior ablations proving the same consequence
records matter to multiple behaviors. No new cognitive modules.

## The five behaviors and their substrate reads

| # | Behavior | Substrate read | Write |
|---|----------|----------------|-------|
| 1 | Policy adaptation | STRATEGY(action,0).successes argmax | ev_observe_aw / sb_resolve_aw |
| 2 | Withholding | PURSUIT(s,r).consec_fail >= 3 | every query outcome |
| 3 | Abandonment | PURSUIT(s,r).consec_fail >= 6, then life.state | same writes as (2) |
| 4 | Retention | PURSUIT(s,r).life.state == ABANDONED | se_mark_abandoned |
| 5 | Search-order | STRATEGY(rel,1).successes ranking | credit attribution |

Shared fields (the point of the experiment):
- PURSUIT.consec_fail drives (2) at threshold 3 AND (3) at threshold 6.
- PURSUIT.life.state is written by (3) [decision] and read by (4) [execution].
- STRATEGY.successes drives (1) under key_b=0 AND (5) under key_b=1.

## Ablation method: config bitmask, reads gated, writes free

One binary. A config node (tag 904, f20 bitmask) gates substrate
READS only. Bits: 1 policy, 2 withhold, 4 abandon, 8 retention,
16 order. Arms: full=31, no-policy=30, no-withhold=29, no-abandon=27,
no-retention=23, no-order=15. Every battery runs full vs one ablation.
Because writes are unconditional, an arm can only differ through the
gated read, which is exactly what the battery asserts.

The config node protects itself with a type-9 self-edge (large clock)
so memory pressure cannot evict it. Lesson learned the hard way: an
evicted config node made se_cfg fall back to default 31, silently
re-enabling the ablated behavior mid-battery.

## Discipline change vs prior build (documented)

Withheld queries now write consec_fail+1. A withhold IS a continued
failure to resolve, so the same counter that triggers withholding at 3
triggers abandonment at 6. This supersedes the prior spec 5.1
(withholds do not write), which would have made behaviors 2 and 3
read different fields.

## Behavior details

Abandonment (3): when a withhold pushes consec_fail to 6, the key's
PURSUIT life.state is marked ABANDONED. Later queries return -4 via a
state check placed BEFORE activation, so abandonment survives later
teaching (permanence). Reclaim is deferred to retention.

Retention (4): evict_node first reclaims uncertainty+guide nodes of
ABANDONED keys (found via type-1 guide edges from DEP edges), one per
call, then falls back to the frozen bid scan. Substrate records
themselves are never reclaimed (they are the memory).

Search-order (5): se_mp_run does a substrate pre-pass (try the top
STRATEGY(rel,1) relation's chain first via t2_chain + t2_try_verify)
with full t2_trial fallback. Post-hoc credit attribution re-executes
each relation's chain to find which reproduces the verified answer,
then writes STRATEGY(rel,1) success. The queried relation itself is
skipped (its fact was just taught by promotion, not discovered).
sub_best_action filters key_b==0 so relation records do not pollute
the policy argmax.

## Architecture accounting (One-System Rule)

- Base: 1241 lines frozen sc_base.zag (a29972ca), minus 3 replaced fns.
- Machinery: 79 lines from fa8405a90 (substrate record fns).
- New: ~250 lines in se_behaviors.zag (config, abandonment, pre-pass,
  attribution, ev_query/evict_node modifications).
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
