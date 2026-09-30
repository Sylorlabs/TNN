# PREREG H-CAUSAL-UNIFIED7 RED TEAM (FROZEN)

**Date:** 2026-09-29
**Researcher:** H-CAUSAL-UNIFIED7 Red Team (independent adversary)
**Target:** H-CAUSAL-UNIFIED7 SURVIVES (6/6), builder result `b56ed4694`.
The repair under attack is R1..R5 (one-episode-one-vote): carve winners
are marked `EP_COUNTED` and skipped by future adjudication tallies,
while staying live for the guard, routing, prediction, and effects.
**Status:** FROZEN. Committed alone before any attack code, build, or
run. No kill criterion may be weakened after results are observed.
Assumption: the repair claim is false. The adversary wins ties.

## 0. Harness construction (frozen)

`cu7a_adv.zag` = lines 1..2501 of the committed
`causal_unified7/unified_causal7.zag` at builder result `b56ed4694`
(the full mechanism region; `fn main` begins at line 2503),
byte-verified with `cmp` against `git show`, plus an attack-only
`fn main` and attack-only helpers. Zero mechanism bytes altered.
Builds in /tmp only; no binaries committed. Pure Zag: no Python in
prereg, harness, builds, runs, or analysis. Shell only for file
operations; `cmp`/`md5sum` for byte checks.

Driver API reused from the mechanism: `fu_init` (via `intent_init`
plus `set32(W, ST_STR(), STR0())` as in the builder harness),
`fu_learn_ep(W,t,p,l,act,nt,np,nl,seq)`, `fu_predict`,
`handle_caus_learn` for string batches. Episode cap 128 is respected
in fixture design.

## 1. X-CU7-1: double voting (white-box vote-accounting invariant)

**Theory under attack:** every episode votes as a winner at most once;
a retired vote never becomes votable again; no episode is listed twice
in one entry (which would double its tally weight); the carve winner
set never contains a previously counted episode.

**Method:** per-fixture shadow arrays `sh_st[128]` (last observed
`ep_st`) and `winct[128]` (ACT-to-COUNTED transitions per episode).
After EVERY learned episode, `audit(W)` runs:
(a) duplicate-index scan: for each entry, all position pairs; KILL
    `"DUP"` if any episode index appears twice in one entry list.
(b) transition scan: for each episode e below `nep`: if
    `sh_st[e]==EP_ACT` and `ep_st==EP_COUNTED`, `winct[e]++`; if
    `winct[e]>=2`, KILL `"REVOTE"` (one episode, two winner votes).
    If `sh_st[e]==EP_COUNTED` and `ep_st==EP_ACT`, KILL
    `"RESURRECT"` (a retired vote became votable again).
    `COUNTED->SUP` is allowed (honest contest retirement) and
    recorded. Then `sh_st[e]=ep_st`.
(c) carve-winner purity: whenever `nent` grows (a carve), every
    episode in the new entry must have had `winct==0` before this
    learn; KILL `"GHOSTWIN"` otherwise.

**Fixtures:**
F1: builder K-CU7-1 flood replay (20 flood episodes plus the 11
phase A/B/C episodes), audited per episode.
F2: merge-heavy stream: two same-action same-parent ACTIVE siblings
with identical fx, forced through `merge_pass`, then further learns;
audits sharing for duplicates and re-votes.
F3: split-heavy stream: multi-value state variable forcing
`split_attempt`/`apply_split`, then learns into the children.
F4: counted-supersede stream: carve winners (counted), then 3 fresh
contradicting episodes against the carved child to force contest
resolution superseding the counted episodes (`COUNTED->SUP`), then
further learns; verifies no resurrection and audit holds throughout.

**Kill criterion:** any `DUP`, `REVOTE`, `RESURRECT`, or `GHOSTWIN`
emit, or any nonzero exit. Any one kills H-CAUSAL-UNIFIED7 outright.

## 2. X-CU7-2: tally correctness

**X-CU7-2(a): honest reversal (KILL-capable).** Fresh world. Replay F1
through the seq-28 carve (entry 3 carved, 6 counted (1,1,1) winners).
Then feed 4 fresh `(2,0,0,2>1,1,1)` episodes. They must
CONFLICTED-ABSORB into entry 2 (oldest same-specificity tombstone)
and the adjudication must carve a new entry 4 whose winner set is
exactly the 4 fresh episodes: total `EP_COUNTED` becomes 12, the new
entry list length is 4, all 4 indices are >=31, all 4 are
`EP_COUNTED`. KILL if: no carve fires (`nent` stays 4); the winner
set includes any previously counted episode; total counted != 12;
or `fu_predict(2,0,0,2)` returns confident (r=1) while the guard
`live_contra_at` reports a live contradiction (guard/predict
disagreement).

**X-CU7-2(b): D1 fragmentation probe (DOWNGRADE-only, never KILL).**
The builder deferred D1 (oldest-tombstone routing strands evidence
in younger tombstones). This probe checks two structural claims on
the F1 end state plus extensions:
(i) append-frozen invariant: once two same-state same-specificity
tombstones exist, the younger never receives further absorbs
(verified by snapshotting younger tombstone lists before/after
extension learns).
(ii) guard coverage: after X-CU7-2(a), feed 4 fresh
`(2,0,0,2>0,0,0)`; the stranded counted (1,1,1) mass in entry 2 must
keep the guard live, so `fu_predict(2,0,0,2)` must withhold (r=0),
never confidently predict against stranded uncounted evidence.
**Downgrade criterion:** if `fu_predict` ever returns r=1 with an
outcome contradicted by stranded uncounted evidence that the routing
never consulted, H-CAUSAL-UNIFIED7 is DOWNGRADED (claim narrowed:
one-episode-one-vote holds, but cross-tombstone routing can strand
decisive evidence). If no such prediction is demonstrated, HOLD with
the residual documented as tested-but-untriggered. This attack
cannot kill: D1 was an explicitly deferred boundary, not a frozen
bar.

**X-CU7-2(c): guard still sees counted winners (KILL-capable).**
On a fixture where counted winners face fresh contradiction below
the carve threshold (single fresh contradicting episode against a
carved child), `live_contra_at` must report 1 (counted winners are
live contradiction) and `fu_predict` must withhold (r=0). KILL on
guard/predict disagreement in either direction.

## 3. X-CU7-3: regression (KILL-capable)

Rebuild `unified_causal7.zag`, `cu7_adv.zag`, and `cu7_test.zag`
from their committed blobs at `b56ed4694`; run each 3 times.
**Kill criterion:** any run whose stdout md5 differs from the
builder frozen hashes (adversary
`36f835f69f41f100675bc385394cf6c3`, battery
`3bde55fe381a7c8ff1cef93d8c038da3`, main
`87f8edc29825802327029f46f045dbe3`); any byte difference versus the
committed raw files; or a `diff` of committed
`unified_causal6.zag` to `unified_causal7.zag` showing any hunk
outside the frozen R1..R5 set. Any mismatch kills.

## 4. X-CU7-4: capacity exhaustion (KILL-capable)

**X-CU7-4(a): entry cap.** Build the F1 carve setup (nent=4), then
call `new_entry` directly 28 times to reach nent=32. Then:
(i) learn at a fresh state: expect the exact emit
`ERROR: entry capacity (32) exhausted; new_entry refused`, nent
stays 32, no episode added for that learn.
(ii) feed the adjudication-triggering absorb that would carve:
`conflict_adjudicate` must return 0 with the same ERROR emit,
nent stays 32, and a full `ep_st` snapshot before/after must be
identical (a refused carve is side-effect free: no winner marked,
no loser superseded).
KILL on: nent>32, missing ERROR emit, any `ep_st` change across
the refused carve, or any confident prediction from a half-built
carve.

**X-CU7-4(b): conflicted-entry episode-list cap.** Replay F1, then
CONFLICTED-ABSORB `(2,0,0,2>0,0,0)` episodes into entry 2 until
`en_neps==64` (single-outcome absorbs never carve), then one more
absorb. Expect the exact emit
`ERROR: conflicted-entry episode list full (64); episode refused`,
`en_neps` stays 64. KILL if the 65th is added or the ERROR is
missing. (Stays within the 128 episode cap: F1 uses 31.)

**X-CU7-4(c): contest cap.** After F1 (nct==8), contradict at a
fresh state on an ACTIVE entry. Expect the exact emit
`ERROR: contest capacity (8) exhausted`, the entry marked
ST_CONFL, and `fu_predict` withholding there. KILL on any silent
untracked contradiction.

## 5. Verdict rule

H-CAUSAL-UNIFIED7 is KILLED if any kill criterion in X-CU7-1,
X-CU7-2(a), X-CU7-2(c), X-CU7-3, or X-CU7-4 fires. X-CU7-2(b) can
only DOWNGRADE, never kill. If all attacks hold, the red team
reports SURVIVES (bounded L2; the repair is a structural
adjudication fix, no invention claimed).

## 6. Governance

Prereg committed alone before any attack code, build, or run.
Pure Zag throughout. Only the owned path
`docs/lab/research-lead/overnight-20260928/cu7_adversary/` is
staged. No binaries committed. Commits local; no push authorized.
This document contains no em dashes.

## AMENDMENT A1 (2026-09-30): X-CU7-2(a) fixture trace correction

Status: TRANSPARENT AMENDMENT, re-frozen. The kill criterion intent
is unchanged; only the fixture's hand-trace is corrected. No bar is
weakened.

Error: the frozen X-CU7-2(a) fixture predicted that 4 fresh
`(2,0,0,2>1,1,1)` episodes would accumulate in conflicted entry 2
and carve with the 4 fresh episodes as winners (counted becomes
12, new entry list length 4). This trace was arithmetically wrong.
After the F1 flood replay, entry 2's uncounted pool contains TWO
`(0,0,0)` episodes (indices 29 and 30, both `EP_ACT`), not zero.
The first fresh `(1,1,1)` makes the adjudication tally
`(0,0,0):2` vs `(1,1,1):1`. The frozen `conflict_adjudicate`
requires `sa>=2 && sa>sb`, so the OLD side correctly wins 2v1 and
carves immediately: winners are exactly indices 29 and 30 (the
pre-existing uncounted episodes, never previously counted), the
fresh episode is superseded as the loser, total counted becomes
10, and the new entry 4 is ACTIVE with list [29,30]. The prereg's
expected outcome (4 fresh winners, counted 12) was impossible
under the frozen mechanism; it reflected an adversary hand-trace
error, not a mechanism defect. Killing on the letter of the
mistaken trace would be a false kill.

Corrected X-CU7-2(a) fixture (two phases, same kill intent):
Phase 1, majority correctness: feed 1x `(2,0,0,2>1,1,1)`.
Expect a carve for the old side: `nent` becomes 5, new entry 4
has exactly 2 winner episodes (indices 29 and 30), both
`EP_COUNTED`, neither previously counted (winct 0 before), the
fresh index 31 is `EP_SUP`, total counted is 10. KILL on any
GHOSTWIN, REVOTE, or wrong winner set.
Phase 2, honest reversal: feed `(2,0,0,2>0,0,0)`,
`(2,0,0,2>1,1,1)`, `(2,0,0,2>0,0,0)`, `(2,0,0,2>1,1,1)`,
`(2,0,0,2>1,1,1)`. The first absorbs into ACTIVE entry 4; the
second contradicts it and the contest cap marks entry 4
ST_CONFL; the remaining three CONFLICTED-ABSORB into entry 2
(oldest tombstone) where the fresh side accumulates to 2v1 and
carves. Expect: `nent` becomes 6, new entry 5 has exactly the 2
fresh winner episodes (indices 35 and 36, both >=31), both
`EP_COUNTED`, total counted is 12, the `(0,0,0)` loser (index
34) is `EP_SUP`. KILL if the winner set includes any previously
counted or non-fresh episode, if counted != 12, or if
`fu_predict(2,0,0,2)` returns confident (r=1) while
`live_contra_at` reports live contradiction.
X-CU7-2(b) runs after the corrected (a); its downgrade criterion
is unchanged, only the starting world state shifts (entry 5 now
exists as the newest tombstone).
