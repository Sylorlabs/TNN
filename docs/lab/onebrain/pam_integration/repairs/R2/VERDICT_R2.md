# VERDICT_R2 — Remove arbitrary exhaustion caps

**Status:** PASS — all frozen kill bars met. Committed 2026-09-25 as
`bb80a0f888d1dfde2e2baf552f21c2b4eff0d5cb` on `sylorlabs/TNN`,
branch `tnn-native-lab` (an earlier draft of this file wrongly claimed a
commit before it happened; this status line records the real one).

## Frozen requirement (PREREG_R2.md)

Replace ledger 1024, disputes 64, quarantine cap, installed index 128,
inbox 256, and text pool 16384 with physically chunked, logically unbounded
storage. Every chunk below znc's genuine 2^25-byte slice ceiling. No silent
drops; physical failure visibly fails closed. Real quarantine and conflict
detection beyond index 128.

## Implementation

Chunked ledger, dispute, quarantine, installed, inbox, and atom-text storage.
Named caps replaced with chunked arenas. Largest configured chunk ~1.31 MB
(well below 33,554,432). Narrow tables use `[]u8` arenas with LE accessors
(per ZNC-2026-09-21-007).

Source identical across build/red-team/long-horizon trees:
`prover.zag` SHA-256 `60063b3e1da5729a5bc2547aaa542b4eef128ed8c94bcbc980bbb2970bed1c87`.

## Performance repairs (2026-09-24/25)

The uncapped design exposed O(n^3) prover slowdowns (800+ verdicts vs ~128).
Six semantically-exact fixes in `prover.zag` (see PERF_FIX_NOTES.md), plus
two associated cleanups (freeing `sp_verdict`'s final closure buffers;
explicit nested conditionals instead of relying on `||` short-circuit):

1. **Leak fix:** `closure_full` frees intermediate `cl_extend` buffers.
2. **Early-break:** skip 2nd/3rd extends once saturated (no bytes added).
3. **Line-offset tables:** `cl_lot_build`/`cl_lot_get` replace O(n) `gline`
   rescans in `cl_extend` (15x) and `closure_base` (2x).
4. **Bloom filter:** 16384-bit, 3×FNV-1a, accelerates `cl_member` O(p)
   find_sub in pair loops. No false negatives; byte-identical output.
5. **Pre-validation bitmap:** `atom_valid` (~600 ops) hoisted from O(na^2)
   loop; inner loop now 80 ops (8.5x).

Combined: R1b 600-withhold probe 46 min → 13m12s (3.5x), matching the
frozen 13-min integrated runtime expectation.

## Kill bars

| Bar | Result |
|---|---|
| K1: 2000 revoke cycles / 4000 ledger rows + 600 withholds, exact totals | PASS — `rx_r1_verdict_rows,2000,2000`, `rx_r1_revoke_rows,2000,2000`, `rx_r1_total,4000,4000`, `r1w_verdict,600,600` |
| K2: 600 real quarantine rows, no phantom | PASS — `r3_quar_index,600,600`, `r1w_quar_index,600,600` |
| K3: conflict detection at installed-index 150, 199 | PASS — `RT_FINDING,R4-INDEX-CAP,repaired-200-indexed-conflict-check-correct-past-128` |
| K4: 200 first-round withholds no false escalation; 3-round escalation works | PASS — `RT_FINDING,R2-DISPUTE-CAP,repaired-200-distinct-no-instant-escalate` |
| K5: long-horizon T1–T5 byte-identical to frozen refs | PASS — bal `cc7e86ed...`, int `356b7873...` match 2026-09-24 |
| K6: every chunk ≤ 33,554,432 bytes | PASS — largest ~1.31 MB |
| K7: zero RNG in decision paths | PASS — grep scan re-run 2026-09-25; only benign hits (FNV hash constants, Bloom-filter `bf_fnv` hash seeds, `sp_seed_store`) |

## Batteries

- **Smoke:** 3/3 byte-identical, `OB_FAILURES,0`, SHA
  `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
  (matches pre-perf-fix SHA — proves semantic exactness).
- **Red-team:** 3/3 byte-identical, `RT_FAILURES,0`, SHA
  `b2658140ad9d645b868bf721f9fff07388f83ba6d3d2608c2cd3a390bfcd115c`.
- **Long-horizon:** bal 3/3 + int 3/3 byte-identical, `OB_FAILURES,0`.

## Files

- `build/src/`, `redteam/src/`, `longhorizon/src/` — full implementation
  sources (the chunked-storage machinery lives in each tree's `prover.zag`,
  SHA-256 `60063b3e1da5729a5bc2547aaa542b4eef128ed8c94bcbc980bbb2970bed1c87`,
  byte-identical across all three trees), battery drivers
  (`ob_test_integration.zag`, `ob_test_redteam.zag`, `ob_lh_bal.zag`,
  `ob_lh_int.zag`), and build/run scripts (`build.sh`, `run_smoke.sh`,
  `build_redteam.sh`, `run_redteam.sh`, `run_lh.sh`)
- `PERF_FIX_NOTES.md` — full investigation record
- `INVESTIGATION_REPORT.md` — pre-repair battery investigation
- `RNG_SCAN.md` — zero-RNG certification (re-scanned 2026-09-25)
- `build/BUILD_REPORT.md`, `build/INTEGRATION_SPEC.md`
- `redteam/ATTACK_LOG.md`, `redteam/RESULTS.md`
- `longhorizon/LONGHORIZON_REPORT.md`
- `evidence/smoke/`, `evidence/redteam/`, `evidence/longhorizon/`
  (3× outputs + SHA-256 each)

No binaries, `.zagd`, `.zag-cache`, probe files, or instrumented/debug
files committed.
