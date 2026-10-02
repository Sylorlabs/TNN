# PREREG H-UNIFIED10 (R11): Authenticated merit, quarantine tombstones, recency protection

**Date:** 2026-09-29
**Lane:** H-UNIFIED10 frontier researcher (repair of H-UNIFIED9 after red-team DOWNGRADE)
**Status:** FROZEN. Committed alone before any implementation, build, or run.

## Target

H-UNIFIED9 SURVIVES (26/26), prereg `ecaa78494`, result `09bd9b933`.
Red team DOWNGRADED (3/3 attacks succeed, no kill), prereg `7464cf28c`,
result `411d24bc9`.

## The three downgrades to repair

### D1: X-U9-1 merit flooding (unauthenticated merit)

Red team: 16 honest rules stored; 16 junk overfills each followed by 10
`cpredict` queries (160 total). Result: 16/16 honest evicted, 16/16 junk
retained. Merit is pure exercise-volume: queries increment `uses` at zero
clock cost with no decay.

Root cause: `cpredict` (query path) increments the same `uses` counter as
learn-corroboration. Queries are not evidence; they are exercise. The
mechanism cannot distinguish flooded from earned merit.

### D2: X-U9-2 quarantine resurrection (no tombstone)

Red team: contradiction `(5,0,0)>(0,9)` quarantined against R; after R
evicted by capacity pressure, the byte-identical episode committed as fresh
rule. Quarantine is a property of the (episode, current store) pair; the
store keeps no tombstone.

Root cause: quarantined episodes are counted (QCOUNT) but their signatures
are not recorded. Evicting the blocking rule flips quarantined to admissible
with no record.

### D3: X-U9-3a birth-age inversion (birth-age gate, not recency)

Red team: rule with uses=100 evicted ahead of 15 young uses=2 rules.
Protection is birth-age (bseq+32 window), not recency: 100 queries do not
refresh bseq.

Root cause: `bseq` is set at store time and never refreshed. Protection
measures age since birth, not recency of genuine evidence.

## The repair (R11)

### R11a: Authenticated merit (closes D1)

Split per-slot merit into two counters:
- `luses` (learn-merit): incremented ONLY by learn events (corroboration
  or conflict through the stream learn path in `clearn`).
- `quses` (query count): incremented by query predictions through the rule
  in `cpredict`. Used for diagnostics only; never for protection or
  eviction ordering.

Protection requires `luses >= CMERITK` (2). Eviction ordering among eligible
slots uses `luses`. Query floods cannot manufacture protection or eviction
priority.

Memory: CMETA expands from 8 to 12 bytes per slot (+0 luses, +4 bseq,
+8 quses). 16*12=192 bytes, 1552 to 1744. WORK at 2048 unaffected.

### R11b: Quarantine tombstones (closes D2)

Tombstone table: 8 entries x 20 bytes (s0,s1,act,ns0,ns1 as i32) at 1744
(after expanded CMETA), ends at 1904. TOMB_CUR at 65020 (ring buffer
cursor, 0..7 wraps). TOMB_N at 65024 (cumulative tombstoned episodes).

When `handle_caus_learn` quarantines an episode (coherence gate returns 0),
write its (s0,s1,act,ns0,ns1) signature to the tombstone table at TOMB_CUR,
advance cursor.

In `clearn` (stream path only), before storing a new rule, check the
tombstone table. If the episode (s0,s1,act,ns0,ns1) matches a tombstone
entry, emit `UTOMBSTONE` trace, increment TOMB_N, return 0 (do not store,
do not quarantine again; the episode is already known-bad).

Operator revise path (`handle_caus_revise`) bypasses the tombstone check
(authenticated operator can override) and clears matching tombstone entries
(sets s0=-1 to invalidate).

Tombstones survive eviction (separate table, not per-slot).

### R11c: Recency refresh (closes D3)

On learn-corroboration in `clearn` (the `found>=0` path, non-conflicting),
refresh `bseq` to current CSEQ in addition to incrementing `luses`.
Protection becomes recency-based for genuinely evidenced rules: a rule
corroborated by stream evidence stays young.

Query hits (`cpredict`) do NOT refresh bseq. This prevents reintroducing
the flooding vector via recency.

The youth window CPROB=32 is unchanged. The semantic is now "32 stores
since last genuine evidence" rather than "32 stores since birth".

## Frozen kill bars

### K-U10-1: Merit flooding blocked (D1 repair)

Setup: 16 honest rules stored via stream learn (each with 2 learn-
corroborations, so luses=2). 16 junk overfills, each followed by 10
`cpredict` queries through the junk rule (160 queries total, as in X-U9-1).

Expect: After 16 overfills, at least 15/16 honest rules survive (cpredict
on honest s0 returns 1). Junk rules have quses=10 but luses=0; they are
not protected and are evicted by subsequent junk overfills (churn among
themselves). ECOUNT delta = 16 (16 evictions for 16 overfills). DCOUNT
delta = 0.

Kill if: fewer than 15 honest rules survive, or DCOUNT>0, or any junk rule
achieves luses>0 via queries alone.

### K-U10-2: Quarantine tombstone blocks resurrection (D2 repair)

Setup: Store R `(5,0,0)>(0,1)`. Present `(5,0,0)>(0,9)`; expect quarantine
(QCOUNT delta=1, tombstone written). Evict R via 15 junk fills + overfill
(as in X-U9-2). Present `(5,0,0)>(0,9)` again.

Expect: Second presentation returns 0 (not stored), UTOMBSTONE trace
emitted, TOMB_N delta=1, QCOUNT delta=0 (not quarantined again; already
tombstoned). `cpredict(5,0,0)` returns 0 (no rule).

Kill if: the episode is stored (returns 1), or no UTOMBSTONE trace, or
cpredict succeeds.

### K-U10-3: Recency protection for evidenced rules (D3 repair)

Setup: Store G `(10,0,0)>(0,1)`. Corroborate G via 2 stream learn episodes
(luses=2, bseq refreshed). Store 15 junk rules. Advance clock by 30 stores
(30 overfills with immediate eviction of junk). Corroborate G again via
stream learn (bseq refreshed to current CSEQ). Advance clock by 20 more
stores.

Expect: G survives (cpredict(10,0,0)=1). G's bseq was refreshed by the
second corroboration, so it is young (CSEQ - bseq < 32) despite being
50+ stores old in birth age. A control rule stored at the same time as G
but never corroborated is evicted (birth-age would have protected it;
recency does not).

Kill if: G is evicted, or the uncorroborated control survives while G
is evicted.

### K-U10-4: Preserved H-UNIFIED9 behavior (regression)

All 26 H-UNIFIED9 checks PASS. Specifically:
- K-U9-1..K-U9-4 semantics preserved (eviction still occurs, still loud,
  still merit-ordered within eligible class, now using luses).
- The 22 preserved H-UNIFIED8 checks PASS.
- Output is byte-identical to UNIFIED9_RAW_OUTPUT.txt modulo:
  (a) the R11 banner change,
  (b) ULEARN/UREVISE suffix changes for tombstone counts,
  (c) UEVICT traces now report luses (not total uses),
  (d) new K-U10-1..K-U10-3 sections replacing/augmenting K-U9-1..K-U9-4.

Kill if: any of the 26 checks FAIL, or output diverges beyond the
disclosed deltas.

### K-U10-5: Determinism

3/3 runs byte-identical (cmp), exit 0, zero FAIL lines.

Kill if: any run differs, or exit != 0, or any FAIL line.

## Explicit non-goals (disclosed boundaries)

- R11a does not prevent merit manufacture via learn-events (actual stream
  episodes). An attacker who can inject arbitrary stream episodes can still
  build luses. The repair authenticates queries vs learns; it does not
  authenticate the stream itself. Stream authentication is out of scope.
- R11b tombstone table holds 8 entries (ring buffer). The 9th distinct
  quarantined episode evicts the oldest tombstone. This is a capacity
  boundary, disclosed. An attacker who can generate 9+ distinct
  contradictions can flush a specific tombstone. The table size is a
  design parameter, not a correctness claim.
- R11c refreshes bseq on learn-corroboration only. A rule that is never
  corroborated ages out after 32 stores regardless of query volume. This
  is intentional: queries are not evidence.
- The operator revise path clears tombstones. This is intentional:
  authenticated revision overrides quarantine history. The operator path
  is separate (call-path authentication, H-UNIFIED3).
- Classification remains bounded L2. This is an integration repair
  (authenticated merit + tombstones + recency), not L3.

## Governance

- Prereg committed alone before any implementation, build, or run.
- `unified10_learn.zag` = committed `unified9_learn.zag` copied verbatim
  (cmp-verified), plus exactly the frozen R11 change set.
- Pure Zag throughout. No Python at any stage.
- No em dashes in loop documentation (byte-verified before commit).
- Only owned paths staged: `u10_frontier/` directory.
- 3/3 deterministic runs required.

## Verdict rule

SURVIVES if K-U10-1..K-U10-5 all PASS.
DOWNGRADED if any of K-U10-1..K-U10-3 FAIL but K-U10-4 and K-U10-5 PASS
(mechanism works, repair incomplete).
KILLED if K-U10-4 FAILS (regression: broke H-UNIFIED9) or K-U10-5 FAILS
(non-deterministic) or DCOUNT>0 or silent eviction in any bar.
