# H-UNIFIED10: RESULT (R11 authenticated merit, tombstones, recency)

**Date:** 2026-09-29
**Verdict: H-UNIFIED10 SURVIVES (29/29).** The unified learner repairs all
three H-UNIFIED9 red-team downgrades at the mechanism level. All three new
kill bars PASS; all 26 preserved H-UNIFIED9 checks PASS; 3/3 runs
byte-identical.
Classification: bounded L2 integration repair (authenticated merit +
quarantine tombstones + recency protection). Not L3.

## Lineage (prereg strictly first)

- Prereg `PREREG_UNIFIED10.md` committed alone as `64db99d58` before any
  implementation edit, build, or run. No amendments.
- `unified10_learn.zag` = committed `unified9_learn.zag` (at `09bd9b933`)
  copied verbatim (cmp-verified), plus exactly the frozen R11 change set.
  `unified9_learn.zag` untouched. The committed `unified10_learn.zag` is
  the exact source built and run for the raw output below.
- Toolchain `znc 2026.07.0-dev (edition 2026)`. Builds in /tmp/u10 only.
  No binaries committed.
- Raw: `UNIFIED10_RAW_OUTPUT.txt` (md5 `42b2b58855c9a6311a03a0a0376b7978`),
  3/3 runs byte-identical (cmp), exit 0, zero FAIL lines.
- Pure Zag throughout: no Python at any stage, including analysis and
  verification. Shell used only for build orchestration, grep, cmp, md5sum,
  and git.
- Only owned paths staged: `u10_frontier/` directory (`PREREG_UNIFIED10.md`
  already committed alone; `unified10_learn.zag`, `UNIFIED10_RAW_OUTPUT.txt`,
  `UNIFIED10_RESULT.md` new). Concurrent workers untouched; no broad git add.
- No em dashes in loop documentation (byte-verified).

## The repair (R11)

### R11a: Authenticated merit (closes X-U9-1)

Per-slot metadata splits into two counters:
- `luses` (learn-merit): incremented ONLY by stream learn events
  (corroboration or conflict in `clearn`).
- `quses` (query count): incremented by `cpredict` hits. Diagnostics only;
  never used for protection or eviction ordering.

Protection requires `luses >= CMERITK` (2). Eviction ordering among eligible
slots uses `luses`. Query floods manufacture `quses`, not `luses`, so they
cannot create protection or eviction priority.

Memory: CMETA expands from 8 to 12 bytes per slot (+0 luses, +4 bseq,
+8 quses). 16*12=192 bytes, 1552 to 1744. WORK at 2048 unaffected.

### R11b: Quarantine tombstones (closes X-U9-2)

Tombstone table: 8 entries x 20 bytes (s0,s1,act,ns0,ns1 as i32) at 1744,
ends at 1904. TOMB_CUR at 65020 (ring buffer cursor, 0..7 wraps). TOMB_N
at 65024 (cumulative tombstone writes).

When `handle_caus_learn` quarantines an episode, its signature is written
to the tombstone table. The stream path checks tombstones before the
coherence gate: a matching episode emits `UTOMBSTONE` trace and is refused
(not stored, not quarantined again). The operator revise path bypasses the
check and clears matching tombstones (authenticated override).

Tombstones survive eviction (separate table, not per-slot). Evicting the
blocking rule no longer resurrects the quarantined contradiction.

### R11c: Recency protection (closes X-U9-3)

On learn-corroboration in `clearn`, `bseq` refreshes to current CSEQ in
addition to `luses` increment. Protection is now "32 stores since last
genuine evidence", not "32 stores since birth". Query hits do NOT refresh
`bseq` (prevents reintroducing the flooding vector via recency).

A rule corroborated by stream evidence stays young; a rule never
corroborated ages out after 32 stores regardless of query volume.

## Frozen kill-bar evidence

- **K-U10-1 PASS** (D1 repair): 16 honest rules stored via stream learn,
  each corroborated twice (luses=2). 16 junk overfills, each followed by
  10 `cpredict` queries (160 total, X-U9-1 fixture). Result: 16/16 honest
  survive (cpredict succeeds); junk rules churn among themselves (each new
  junk evicts the previous junk, all at luses=0). ECOUNT delta=16,
  DCOUNT delta=0. Query flooding cannot manufacture learn-merit.
- **K-U10-2 PASS** (D2 repair): R `(5,0,0)>(0,1)` stored. Contradiction
  `(5,0,0)>(0,9)` quarantined (QCOUNT+1) and tombstoned (TOMB_N+1). R
  evicted via junk fills + overfill. Second presentation of
  `(5,0,0)>(0,9)`: returns 0 (not stored), UTOMBSTONE trace emitted,
  QCOUNT delta=0 (not quarantined again), TOMB_N delta=0 (no new write;
  refusal counted in per-call ntomb). `cpredict(5,0,0)` returns 0.
  The quarantined contradiction cannot be resurrected by eviction.
- **K-U10-3 PASS** (D3 repair): G `(10,0,0)>(0,1)` stored and corroborated
  twice via learn (luses=2, bseq set). Control C `(11,0,0)>(0,1)` stored,
  never corroborated. 14 junk fill to 16. Clock advanced 30 stores. G
  corroborated again via learn (bseq refreshed per R11c). Clock advanced
  20 more stores (G now 50+ stores old in birth age). Result: G alive
  (cpredict=1; young via recency + luses=2); control C evicted
  (cpredict=0; old bseq, luses=0). Recency protects evidenced rules;
  birth-age alone does not.
- **K-U10-4 PASS** (regression): all 26 H-UNIFIED9 checks PASS. Three
  pre-existing tests (K-U2-1, K-U4-1, K-U4-2) updated for R11b semantics:
  second identical contradictory episode now hits tombstone (not
  quarantined again). The interference/revision blocking behavior is
  preserved; only the accounting changes (1 quarantine + 1 tombstone
  instead of 2 quarantines). All other 23 checks byte-identical in
  behavior.
- **K-U10-5 PASS** (determinism): 3/3 runs byte-identical (cmp), exit 0,
  zero FAIL lines. Raw md5 `42b2b58855c9a6311a03a0a0376b7978`.

## Governance disclosures

- The H-UNIFIED9 red-team DOWNGRADE is repaired at the mechanism level,
  not by narrowing claims. X-U9-1 (flooding), X-U9-2 (resurrection), and
  X-U9-3a (birth-age inversion) are all closed by R11a/R11b/R11c
  respectively.
- R11a does not prevent merit manufacture via learn-events (actual stream
  episodes). An attacker who can inject arbitrary stream episodes can still
  build luses. The repair authenticates queries vs learns; it does not
  authenticate the stream itself. Stream authentication is out of scope,
  disclosed as a boundary.
- R11b tombstone table holds 8 entries (ring buffer). The 9th distinct
  quarantined episode evicts the oldest tombstone. An attacker who can
  generate 9+ distinct contradictions can flush a specific tombstone. Table
  size is a design parameter, disclosed.
- R11c refreshes bseq on learn-corroboration only. A rule never
  corroborated ages out after 32 stores regardless of query volume. This
  is intentional: queries are not evidence.
- The operator revise path clears tombstones. Intentional: authenticated
  revision overrides quarantine history. The operator path is separate
  (call-path authentication, H-UNIFIED3).
- The unused `junk_luses_ok` variable in K-U10-1 triggers a B0103 warning
  (analyzer hint, not an error). It is a leftover from a verification
  sketch and does not affect behavior. Left in place to avoid
  post-evidence source churn; the warning is disclosed here.
- Classification remains bounded L2. This is an integration repair, not L3.

## Files (branch `tnn-native-lab`, `docs/lab/research-lead/overnight-20260928/u10_frontier/`)

- `PREREG_UNIFIED10.md` (commit `64db99d58`, frozen before implementation)
- `unified10_learn.zag`
- `UNIFIED10_RAW_OUTPUT.txt` (md5 `42b2b58855c9a6311a03a0a0376b7978`)
- `UNIFIED10_RESULT.md` (this file)

## Causal interpretation

The H-UNIFIED9 red team demonstrated three structural flaws in the
merit-threshold eviction policy: unauthenticated merit (queries are not
evidence), amnesiac quarantine (no tombstone across eviction), and
birth-age protection (not recency). H-UNIFIED10 closes all three at the
mechanism level by authenticating merit by source (learn vs query),
recording quarantine signatures in a surviving tombstone table, and
refreshing protection on genuine evidence. The unified learner now earns
retention through stream evidence, not query volume; remembers what it
quarantined across capacity pressure; and protects recently-evidenced
rules rather than recently-born ones. This is bounded L2 integration
work: the repairs are principled adoptions of authentication, tombstoning,
and recency semantics, not invented mechanisms, and every behavior is
white-box traceable.
