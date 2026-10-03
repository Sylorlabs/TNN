# VERDICT — B-T5 split/merge dynamics (R0 redo, 1x)

Crew B-DYNSG · Track R0 · 2026-09-21 · branch `tnn-native-lab`
Prereg: `units/PREREG_FREEZE.md` §2 (Micah signed 2026-09-21). R-9: **1x ONLY**.
Binary: `units/r0/impl/dynamics/dyn_b5.zag` → `dyn_b5 <leg 0|1> <perturb 0..4>`.
Pure Zag. Zero RNG in AI decision paths. Byte-identical reruns (M8 N=5).

## Frozen bar (R0.2 B-T5)

> B-T5 pass requires split fired, merge fired, lineage auditable, no ghost IDs.

Recovered firing conditions (R-8, `r0_init`):
- split iff `use_count>=3 AND conflict>=learned_conflict AND utility<=learned_utility_floor`
  (leg0: conflict 400, floor 0; leg1: conflict 500, floor 0)
- merge iff `pair_seen>=learned_pair_seen AND joint_gain-separate_regret>=learned_gain`
  (leg0: pair_seen 3, gain 0; leg1: pair_seen 4, gain 500)

## Verdict: PASS (both legs)

| Check | Leg 0 | Leg 1 |
|---|---|---|
| SPLIT fired under recovered conditions | ✅ child id 3 | ✅ child id 3 |
| MERGE fired under recovered conditions | ✅ merged id 4 | ✅ merged id 4 |
| Split/merge ledger-audited (ops 196/197) | ✅ | ✅ |
| Lineage (tombstone + successor links) | ✅ | ✅ |
| No ghost IDs (monotonic issuance, ratio<2) | ✅ | ✅ |
| Negative controls (4) | ✅ all `-1` | ✅ all `-1` |
| STORESEQ readback probe (`r0_probe_run`) | 0 fails | 0 fails |
| Battery expected-value self-checks | 0 fails | 0 fails |
| M8 N=5 adversarial perturbations | **PASS** | **PASS** |

## Scenario (harness op order: ingest A, ingest B, split check, recall probe, ingest C, merge check, recall probe)

1. **Ingest A** — recruit 8-span `"splitchk"` with divergent grounded labels
   `{3,3,0,1,2,3}` → purity 500, conflict 500 (both legs). Promoted as id 0.
2. **Ingest C (pair context)** — recruit `"AAAA"` (id 1), `"BBBB"` (id 2),
   uniform labels. Promoted *before* the split so the `"splitchk"` proposal is
   correctly deduped (post-split re-promotion is documented as FINDING B5-F1).
3. **NEGCTRL** `B5_NEGCTRL_SPLIT_EARLY` — `r0_maybe_split` before regret: `-1`
   (utility 5283/… above floor). Proves the utility conjunct is load-bearing.
4. **Ingest B (conflict context)** — 3 greedy segmentations → `use_count=3`;
   delayed regret → utility `5283 → -717` (leg0).
5. **Split check** — `r0_maybe_split(0)` → child id 3. Parent tombstoned,
   `succ=3`, lengths 4/4. Audit entry op 196 (`b1=parent, b2=child, b3=4,
   b4=old_len 8`, stage 9).
6. **Recall probe 1** — re-segmenting `"splitchk"` now yields 4 literals +
   the live suffix child: the old 8-boundary no longer exists on the record.
   Boundaries are mutable.
7. **NEGCTRL** `B5_NEGCTRL_MERGE_EARLY` — `r0_maybe_merge(1,2)` at
   `pair_seen=0`: `-1`. After 6 pair observations, `pair_seen=6`.
8. **Merge check** — `r0_maybe_merge(1,2)` → merged id 4.
   Leg0: `6>=3`, `min((7·6−11)·20,1000)−0 = 620 >= 0`.
   Leg1: `6>=4`, `min(620,500)−0 = 500 >= 500` (exact bar).
   Audit entry op 197 (`b1=1, b2=2, b3=6, b4=8`, stage 9, `d1=620/500`).
9. **Recall probe 2** — merged bytes == `"AAAABBBB"` byte-exact, len 8.
10. **K-R3** — tombstone/live ratio 1500 < 2000; new issuance monotonic
    (ids 5, 6 fresh; tombstoned 0, 1, 2 never reissued live).

Negative-control arenas: **B5C** (uniform labels → conflict 0, use 3, util ≤ 0
→ no split: `-1`) and **B5U** (use 2 < 3, conflict 500, util ≤ 0 → no split:
`-1`) prove the conflict and use_count conjuncts are load-bearing.
**B5T** proves threshold learning is audited, never silent (THRESH op 204,
stage 10; leg0 gain `0→0→50`, leg1 `500→475→525`).

## Ledger excerpts (leg 0, canonical run; full table in `b5_ledger_leg{0,1}.csv`)

Columns: `idx,op,slot,rc,b1,b2,b3,b4,b5,stage,d1,d2`.

```
0,192,0,0,8,6,500,0,0,10,2009577897,5283      # PROPOSE "splitchk"
1,193,0,0,8,6,5283,0,0,5,2009577897,0        # COMMIT id 0
7,196,0,0,0,3,4,8,0,9,-358,1                 # CUT_SPLIT parent 0 -> child 3
9,197,4,0,1,2,6,8,0,9,620,0                  # CUT_MERGE 1+2 -> 4 (pair_seen 6, len 8)
12,192,0,0,8,6,500,0,0,10,2009577897,5283    # PROPOSE "splitchk" (re-issue, B5-F1)
13,193,6,0,8,6,5283,0,0,5,2009577897,0       # COMMIT id 6
```

Word map honored: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48,
stage@52, d1@56, d2@60.

## FINDING B5-F1 — same-material split→re-merge is unachievable (frozen core)

Arena E demonstrates the mechanism. `r0_split_at` rewrites the tombstoned
parent's record to the 4-byte prefix (audited: `b3=split_at, b4=old_len`), so:

- (a) re-observing the original 8-span re-promotes it as a **new live chunk**
      (the bank no longer holds any 8-span with those bytes — verified:
      dup id 2, live, byte-identical), while
- (b) the 4-byte prefix can **never** be recruited live again — `r0_promote`'s
      `r0_bank_has_span` dedup matches the tombstoned prefix record and skips
      it (verified: `b5_find_live("spli") == -1`).

Consequences, all verified in-band:
1. The prereg's "later re-merge of the same material" (4+4 → 8) cannot be
   constructed: the merge needs two *live* halves and the prefix half is
   permanently shadowed.
2. The suspected K-R3 "ghost" does **not** materialize as an ID violation:
   lineage is fully audited (SPLIT entry carries parent→child, split_at,
   old_len), issuance is monotonic, tombstoned IDs are never reissued live.
   The wart is semantic (dedup sees tombstones; the bank forgets the whole
   but remembers the prefix), not an identity forgery.
3. The harness's own op order (split check *before* the merge pair's ingest)
   already structures B-T5 as split-fire + merge-fire on separate contexts,
   not as same-material restoration. This battery follows the harness.

**Disposition:** PASS on the frozen bar (split fired, merge fired, lineage
auditable, no ghost IDs). B5-F1 is referred to Micah: either the prereg's
"same material" parenthetical needs amendment, or the core's
split/dedup semantics need a (Micah-approved) change. The battery does not
bend the prereg and does not hide the finding.

## Other flags

- **ZNC-2026-09-21-002** (new, filed in-code): `slice as *u8` does not yield a
  data pointer in this znc build (reads return heap garbage; indexing past the
  header segfaults). Both batteries build the M8 store image by decomposing
  words→bytes instead. Repro captured during this run.
- **API.md imprecision**: the SPLIT entry documents `d1=parent_util`, but the
  core emits the *halved* utility (`b5_ledger`: `d1=-358` = `-717/2`).
  Logged, not treated as failure (frozen core wins over doc).
- **METRICS.md vs ARM_INTERFACE.md**: schema conflict noted per instructions;
  this battery follows `METRICS.md` strings (op names, stage names).
- M8 capture hashes (canonical, perturb 0):
  - leg0: `STORE_IMAGE 4b934b9f2fa70f64dd460505e469a7e62c39c3187daa90828d75893030e2104c`, `LEDGER 1612647514`
  - leg1: `STORE_IMAGE 71abf85952cd0ca34798ffa8313a1509e52968edf7f735fe9ddc544b97ed7cb9`, `LEDGER 370717379`
  (`ALLOC_TRACE` is `e3b0…` empty — this battery routes no bytes through
  `m8_alloc`; perturbations act on the native heap via the in-binary churn.
  Deterministic across all 5 modes.)

## Files

- `units/r0/impl/dynamics/dyn_b5.zag` — battery source (committed)
- `units/r0/evidence/dynamics/b5_leg0.log`, `b5_leg1.log` — canonical outputs
- `units/r0/evidence/dynamics/b5_ledger_leg0.csv`, `b5_ledger_leg1.csv`
- `units/r0/evidence/dynamics/b5_m8.json` — gate verdicts
- `units/r0/evidence/dynamics/VERDICT_B5_DYNAMICS.md` — this file
