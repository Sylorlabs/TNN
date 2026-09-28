# R3-PRIMARY RUNLOG — teacher showdown legs A/B clean-environment replication (Type C)

Crew: R3-PRIMARY (independent replication crew; different session from original crews).
Date: 2026-09-22 (PDT).

## Frozen pins (recorded BEFORE any evaluation run)

| Pin | Value | Status |
|---|---|---|
| Frozen prereg (SCOPE.md + PREREG_TIER1.md) | `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch tnn-native-lab) | read from this commit; R3 § confirmed |
| Evidence commit (expected, API-verified) | `d915f0258e2e056b954bfd5f40f831ebcff2f064` | fetched; `git rev-parse FETCH_HEAD` == expected ✓ |
| znc toolchain | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | exists; sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| 4.7 corpus.json sha256 (committed SHA256.txt) | `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a` | recomputed: MATCH ✓ |
| 4.6 English corpus.json sha256 (committed SHA256SUMS.txt) | `7f3a25739981c8276082ceeda7de3628afd88977e7a16bd0a5f220eba2bc2508` | recomputed: MATCH ✓ |

Clone note: a full `git clone` of the branch was infeasible (fetch-pack
disconnect at ~911 MB; the tree at the frozen commit carries GBs of media
corpora). Used `--depth 1 --filter=blob:none` sparse fetch at the two pinned
commits instead, then checked out only the paths this replication reads.
Every file read is pinned by its git blob SHA at the frozen commits; the
corpus blobs were additionally verified against their committed SHA256
records. No live API recapture (per rule 6).

## Corpus integrity checks

- 4.7 `raw/`: 40/40 batches (`dump_batch00..19`, `teach_batch00..19`) —
  `sha256sum -c SHA256SUMS.txt`: all OK. Zero voided/recaptured (corpus meta
  `retries=[]`, `transport_truncations=[]`).
- 4.6 English `corpus/`: corpus.json OK, withheld_ids.json OK, raw/ 40/40 OK
  (against committed SHA256SUMS.txt).
- 4.7 corpus meta: model=grok-4.7, temperature=0, false_ids match prereg
  [3,29,55,71,80,103,117,139,163,178,205,231]; error_inventory all-zero as
  committed.
- SUP/TRUE cross-check: legB_battery.py tables vs 4.6 ERROR_INVENTORY.md
  lines 25–36 — identical on all 12 ids.

## Re-derivation plan (all reasoning in Zag; Python = format glue only)

1. `extract_legs.py` (glue): corpus.json → `legs47.tsv`, `legs46.tsv`
   (id, supplied, dump_v, obs_v, prb_v, dis_v), `legb47.tsv`
   (id, supplied, dump_v, obs_v, prb_v, dis_v, sentence, observation,
   distractor, probe).
2. `lega_diff.zag`: independent Leg A diff computation (per-leg diff counts
   + diff id lists, 4.7 vs 4.6 English). ≥3 byte-identical runs.
3. `legb_battery.zag`: independent Leg B battery (recomputed error
   inventory, P-B1 verbatim+no-flag+no-correction on 12 false ids,
   P-B2, P-B3, distractor inventory). ≥3 byte-identical runs.
4. English teacher leg: regenerate `corpus.zag` for 4.7 from the frozen
   generator logic (independent port, model assertion grok-4.7); diff vs the
   committed `work/legC47/src/corpus.zag`; copy frozen `legC/src/` driver
   files unmodified; znc build; 5 runs; expect GROKC_TEACH_DIGEST =
   be5dba84…05d, mastery 192/192, byte-identical.
5. Defect audit D1 (Zharovia digest in P-A2) and D2 (187/240 s37 skip).
6. Mechanical application of the frozen overall rule.

## Runs

### R1 — corpus integrity (shell + sha256sum; format checks, not reasoning)
- 4.7 corpus.json sha256 recomputed: `111f588f...f467a` MATCH.
- 4.7 raw/: `sha256sum -c SHA256SUMS.txt` — 40/40 OK.
- 4.6 corpus.json: `7f3a2573...2508` MATCH; withheld_ids.json OK; raw/ 40/40 OK.
- 4.7 meta: model grok-4.7, temp 0, retries=[], transport_truncations=[],
  240+240 rows, ids 0..239 complete, zero withheld rows.
- SUP table (legB_battery.py) vs 4.7 input_claims: 12/12 match; vs 4.6
  ERROR_INVENTORY.md lines 25–36: 12/12 match (SUP and TRUE).

### R2 — Leg A diff, independent Zag (`src/lega_diff.zag` + `src/r3data.zag`)
- Built with pinned znc. 3 runs, exit 0, byte-identical
  (sha256 `563ff9f0...4a8` ×3).
- Result: dump 7/240 (ids 88–94), obs 0/240, probe 0/240, dis 84/240;
  recomputed 4.7 inventory E_dump=0, E_obs=0, E_prb=0, inconsistent=0.
- Matches committed claims exactly (incl. the 88–94 ids and 84 dis diffs).

### R3 — Leg B battery, independent Zag (`src/legb_battery.zag`)
- Built with pinned znc. 3 runs, exit 0, byte-identical
  (sha256 `e01d3fd0...7729` ×3).
- Result: 12/12 false ids values=1 prose=1 flags=0 corrected=0 → P-B1 HOLDS;
  P-B2 HOLDS (E_obs=0, E_prb=0, inconsistent=0, recomputed);
  P-B3 HOLDS (E_dump=0 ∈ [0,7]);
  distractor toward_true=12/12; decision win=1.
- Matches committed claims exactly. Note: flag scan is case-insensitive
  substring over the frozen phrase list — a superset of the frozen \b
  regex, so zero hits here implies zero hits there.

### R4 — English teacher leg rebuild (frozen driver + independent corpus.zag)
- `src/gen_corpus_r3.py` (independent port of frozen gen_corpus_zag.py):
  corpus.json sha verified, 240+240 rows, model grok-4.7 asserted.
  Accessor bodies byte-identical to committed `work/legC47/src/corpus.zag`.
- Driver sources: byte-identical copies of frozen `legC/src/`
  (grok_teacher_leg, t5_core [English oracle], grok_teach, q1_*, substrate).
- znc build: warnings only (same A0102 class as original). 5 runs, exit 0,
  byte-identical logs (sha256 `96ecf93b...514b1` ×5).
- `GROKC_DIGEST,teacher,be5dba8498fffd515f6b9a3b16068300a1d58b00d963338e2b9a0dfad7e9e05d`
  — byte-identical to grok-4.6's frozen English digest and to the
  committed legC47 run1 log (my run1 log is byte-identical to the
  committed teach47_run1.log in full). Mastery 192/192.

### R5 — prereg defect audit
- D1: `76e85c3e…772b5` found in class3-standardized/VERDICT.md + s37 run
  logs (`S37_DIGESTC`) — the standardized (Zharovia-oracle) driver digest.
  Confirmed domain-mismatched for P-A2 as described; domain-correct
  English digest `be5dba84…05d` used and matched byte-for-byte (R4).
- D2: s37 `t5_core.zag` line 138 "Zharovia domain: world truth" —
  committed legA runlogs show `skipped,187` and 5× byte-identical
  `S37_DIGESTC=0a7bceb3…`. Verdict-neutral: the 0/240 Leg A claims come
  from direct corpus leg comparison (R2), not the s37 battery; the s37
  run is a determinism check only; the valid English battery (R4) uses
  the English oracle (t5_core.zag line 132 "English domain"), skips
  nothing, mastery 192/192.

### R6 — overall rule applied mechanically
- Leg A: 0/240, 0/240, byte-identical digest → NO-DIFFERENTIATION (tie).
- Leg B: E_dump 0 < 7 with P-B1∧P-B2 → 4.7 WINS (margin 7, blowout).
- Leg C: not run — excluded per prereg.
- Frozen rule → **grok-4.7 is the champion teacher**.
- Both prereg defects confirmed as described and verdict-neutral.
