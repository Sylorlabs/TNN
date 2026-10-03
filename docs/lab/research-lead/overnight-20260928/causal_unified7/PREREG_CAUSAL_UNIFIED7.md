# PREREG H-CAUSAL-UNIFIED7 (FROZEN)

**Date:** 2026-09-29
**Researcher:** H-CAUSAL-UNIFIED7 Frontier Researcher
**Target:** H-CAUSAL-UNIFIED6 SURVIVES (builder 5/5, result
`438c3344a`; red team SURVIVES 4/4, result `2cb0b1a6e`).
**Status:** FROZEN. Committed alone before any implementation,
fixture, build, or run. No frozen bar may be weakened or
retroactively changed after results are observed.

## 1. Deferred boundaries under test

From CU5 red team sec 9 and CU6 builder sec 8 (both residual):

(B1) Double voting: carve winners are shared into the new entry
and stay live in the parent tombstone, so they vote in more than
one adjudication over time.
(B2) `find_conflicted` oldest-first tie-break: re-adjudication
routes to the lowest-index equally-specific tombstone.
(B3) Entry capacity 32: explicit refusal (X-CU3 fix).

## 2. Demonstrated defect (white-box, pre-implementation)

`conflict_adjudicate` in `unified_causal6.zag` (lines 1370..1453):

- Tally loop (line 1379): skips only `EP_SUP` episodes.
- Carve loop (lines 1415..1428): winners are `entry_add_ep`ed
  into the new entry and stay `EP_ACT` in the parent tombstone
  (comment at line 1419: "move winners (shared indices, stay
  live)").

Consequence: an episode that voted as a winner in carve N votes
again in carve N+1 at the same state. The winner vote mass is
immortal, so:

(a) the evidence bar for overturning a carved outcome ratchets
upward with each re-adjudication (observed in analysis: required
fresh support grows 2, 3, 6, 7 across flips);
(b) fresh contradicting episodes are absorbed singly, outvoted
by immortal votes, and SUPERSEDED on arrival (evidence
destroyed);
(c) the stale outcome is re-carved from dead votes while live
counterevidence is retired.

This is a genuine architectural failure class: the causal
learner cannot revise a carved law no matter how much fresh
counterevidence arrives. It is independent of the tie-break
(the tie-break only chooses which tombstone hosts the
re-voting).

## 3. Frozen repair R: one-episode-one-vote

New file `causal_unified7/unified_causal7.zag` is byte-verbatim
`causal_unified6/unified_causal6.zag` except exactly:

(R1) New episode state constant after `EP_SUP`:
`fn EP_COUNTED()i32 { return 2; }` meaning "this episode already
voted as a winner in a carve; retired from future tallies but
still live evidence".

(R2) `conflict_adjudicate` tally loop: skip episodes with
`ep_st==EP_SUP` OR `ep_st==EP_COUNTED` (was: skip `EP_SUP`
only).

(R3) `conflict_adjudicate` carve loop: skip `EP_SUP`/`EP_COUNTED`
when selecting winners (winners = uncounted live episodes
matching the winner outcome); each moved winner is marked
`EP_COUNTED` (was: stays `EP_ACT`). Losers go to `EP_SUP`
(unchanged).

(R4) `entry_eps`: include `ep_st==EP_ACT` OR `ep_st==EP_COUNTED`
(was: `EP_ACT` only), so effect induction, prediction, merge,
and split see exactly the same episode set as before.

(R5) All other `ep_st` uses UNCHANGED, so counted episodes stay
live evidence everywhere except the tally:
- `live_contra_at` (CU6 guard): skips `EP_SUP` only; counted
  episodes still count as live outcomes, so the guard still
  fires on a counted-winner vs fresh-evidence contradiction.
- `find_conflicted` covered check: `!=EP_SUP`; absorb routing
  stays durable.
- `learn_episode` ACTIVE contradiction scan: skips `EP_SUP`
  only; counted episodes still serve as entry beliefs.
- `predict` exact-episode: skips `EP_SUP` only.
- `usable()`: skips `EP_SUP` only.
- `contest_feed` loser retirement: skips `EP_SUP` only.

(R6) Carve criterion UNCHANGED: support>=2 and strict majority
over exactly two distinct outcomes (`have_b==0` still returns
0; no single-outcome carve).

## 4. Frozen dispositions (not repaired this wave)

(D1) Tie-break UNCHANGED. Rationale: no demonstrated unsafe
prediction is attributable to the tie-break alone; its worst
observed effect (routing re-adjudication to the tombstone with
the largest immortal voting mass) is neutralized by R, because
counted votes no longer vote anywhere. Residual documented:
evidence stays fragmented across same-mask tombstones; a
re-adjudication is decided by the routing tombstone's uncounted
pool only. Changing the tie-break without a demonstrated defect
would be churn.

(D2) Capacity eviction CONSIDERED and DEFERRED. Rationale:
entry-capacity exhaustion is already explicit and safe (X-CU3
fix: explicit refusal, never silent). Eviction policy is a
separate failure class needing its own hypothesis, prereg, and
kill bars; bundling it with R would violate
one-repair-per-hypothesis discipline.

## 5. Frozen kill bars

Notation: episodes are 0-indexed by creation order. The flood is
the 20-episode string from K-CU6-1 (indices 0..19, nct=8).
Phase A: `2,0,0,2>0,0,0` (idx 20, carve trigger),
`2,0,0,2>1,1,1` (idx 21, re-conflicts the carved entry).
Phase B: `2,0,0,2>1,1,1` x5 (idx 22..26).
Phase C: `2,0,0,2>0,0,0` x4 (idx 27..30).

### K-CU7-1: double voting closed (entrenchment fixture)

Harness `cu7_adv.zag` runs the fixture above on the CU7
mechanism and asserts white-box:

(a) final `nent(W)==4`: exactly two carves total (phase-A carve
creates entry 2; exactly one phase-B/C carve creates entry 3).
KILL if !=4 (immortal-vote re-carves present).

(b) the phase-B/C carve is entry 3 and `en_neps(W,3)==6`: its
six winner episodes are exactly idx 21..26, each never having
voted before. KILL otherwise.

(c) `EP_SUP` set among idx 21..30 is exactly {idx 27}: the only
retired fresh episode is the honest 6v1 loser of the phase-C
adjudication. KILL if any other of idx 21..30 is superseded
(evidence destruction) or if idx 27 is not (tally dishonest).

(d) final `EP_COUNTED` episode count == 8 (idx 16, 20 from the
phase-A carve; idx 21..26 from the phase-C carve): every vote
was cast exactly once. KILL on mismatch.

(e) final `fu_predict(W,2,0,0,2,out)` returns r=0 (WITHHOLD
live-contradiction) and `adv_live_contra(W,2,2,0,0)==1`: the
guard still sees counted winners as live contradiction against
fresh evidence. KILL if r!=0 or the helper !=1 (stale shadow
or guard regression).

### K-CU7-2: X-CU4-2 stays closed (K-CU6-1 re-derived)

Same fixture and assertions as builder K-CU6-1: after the fresh
`2,0,2,2>7,7,7` general entry, query (2,0,0) r2==0,
`adv_live_contra(W,2,2,0,0)`==1, control query (2,0,2) r2b==1
with out==(7,7,7). KILL on any mismatch.

### K-CU7-3: adjudicated carves still predict (K-CU6-2 re-derived)

Same fixture and assertions as builder K-CU6-2: query (2,0,0)
r==1 out==(0,0,0); query (1,0,0) r==1 out==(0,0,0); query
(0,0,0) r==0. KILL on any mismatch.

### K-CU7-4: no regression

Rebuilt `cu7_test.zag` stdout is byte-identical (cmp) to frozen
`causal_unified6/CU6_TEST_RAW_1.txt` (16/16, MD5
3bde55fe381a7c8ff1cef93d8c038da3). Rebuilt
`unified_causal7.zag` main stdout is byte-identical (cmp) to
frozen `causal_unified6/CU6_MAIN_RAW_1.txt` (28/28, MD5
87f8edc29825802327029f46f045dbe3). KILL on any byte
difference.

### K-CU7-5: determinism

`cu7_adv.zag`, `cu7_test.zag`, and `unified_causal7.zag` main:
3 runs each, stdout byte-identical 3/3 (MD5 recorded). KILL on
any divergence.

### K-CU7-6: change-set purity

`diff unified_causal6.zag unified_causal7.zag` shows exactly
R1..R5 and nothing else: no other function text changed, no
fixture literals in mechanism functions. KILL on any extra
change.

## 6. Verdict rule

SURVIVES iff K-CU7-1 through K-CU7-6 all PASS. Any KILL kills
the hypothesis outright (binary bars; no downgrade path: a
failed vote-accounting invariant is not a partial repair).

## 7. Planned exploratory (not a frozen bar)

Before judging CU7, run the K-CU7-1 fixture against the CU6
mechanism (exploratory defect confirmation): predicted 4
UNCONFLICTs with winner supports 2, 3, 6, 7 (the ratchet) and
EP_SUP swallowing fresh episodes. Reported as exploratory
context only; it constrains no verdict.

## 8. Governance

- This prereg is committed alone before any implementation,
  fixture, build, or run.
- Pure Zag: no Python in prereg, implementation, fixtures,
  builds, runs, analysis, harnesses, or scratch. Shell only for
  file operations; cmp/md5sum for byte checks; a shell byte scan
  for em dashes.
- Only explicitly owned paths staged:
  `docs/lab/research-lead/overnight-20260928/causal_unified7/`.
- No binaries or generated artifacts committed (raw outputs are
  text; binaries and .zag-cache stay in /tmp).
- Commits local; no push attempted or authorized.
- No frozen bar weakened or retroactively changed.
- This document contains no em dashes.
