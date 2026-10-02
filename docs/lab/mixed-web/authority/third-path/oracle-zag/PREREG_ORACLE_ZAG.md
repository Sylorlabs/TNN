# PREREG — TP1 Zag-native oracle (FROZEN 2026-09-22)

**Order:** Micah, 2026-09-22 — the TP1 third-path trial (verdict commit
`c85c9b41770c1878fb00a8dc991a5b4f17f8caaa`, frozen prereg
`44afdbefc168edddcae50e9dd91eac12cd9fa156`) was verified by an independent
PYTHON oracle. Per Micah's standing law ("use zag unless its a script"),
the Python oracle is demoted to build-script status; this frozen prereg
governs the pure-Zag oracle that becomes the verification authority.

**Freeze rule:** this document is committed BEFORE any oracle run. No
oracle result may exist before the freeze commit. Frozen sections are
never edited in place.

## §1. What the oracle recomputes (from frozen data only)

From the frozen corpus
(`docs/lab/mixed-web/authority/third-path/evidence/tp_data.json`,
SHA256SUMS-verified; the upstream 15 round-3 logs re-verified against
`docs/lab/mixed-web/authority/round3/evidence/SHA256SUMS` immediately
before the run), the oracle recomputes, with zero RNG:

1. All **2,640 dispute decisions**: 3 paths (T1/T2/T3) × 220 envelopes
   (180 Block U + 20 S8 + 20 G2) × 4 frozen thresholds (k/(k+1),
   k∈{1,2,3,5} → 500/667/750/833 thousandths), as `P|` lines in
   envelope→threshold→path order.
2. The **3 SHA-256 chained ledger heads** (880 chained entries each):
   - T1 `e17861bac9fca2647669b3ef39e56aeaec3db689a7ce62d2fa6312b3151aa861`
   - T2 `3c030dd4222168014a350f039d43447fd58115b9a656f56e58078c7b2ca212ea`
   - T3 `d2f45295b38d24c8de4c90645a7a204da958854475f1f49f4a74571ed99542a0`
3. **Shape/sequence counts**: `C|1|200|2|20|3|0|0|0` (200 S1_UNCORR /
   20 S8_TIE / 0 CORROB / 0 OTHER) and `S|880|880|880`.
4. **S8 false-confidence**: 0% — zero CONVERGE decisions on the 20 S8
   envelopes across all paths and thresholds (0/80 per path).
5. **Firing behavior**: T1 fire counts per threshold per block
   (T1@500 is the licensed bar: fires exactly where rel ≥ 500 on
   S1_UNCORR, 0 fires on G2); T3 verdict-identical to T1 on all 880
   decisions.

## §2. Decision logic (independently re-derived)

The oracle's classifier and policies are re-derived from the frozen
PREREG-TP1 §3 — NOT copied from the trial program's code structure:

- Shape classifier over envelope rows at max recency: maxy = max year
  over rows; prim = first row's domain; prim_newest = prim's answer at
  maxy. S1_UNCORR (shape 1): 3 distinct answers at maxy, exactly 1
  domain each, prim_newest uncorroborated. S8_TIE (shape 2): 2 distinct
  answers at maxy, exactly 2 domains each. CORROB (shape 3):
  prim_newest has ≥1 corroborator at maxy. OTHER (shape 0): anything
  else → WITHHOLD for all paths.
- T1: shape 1 → CONVERGE prim_newest iff independently-established
  rel ≥ k/(k+1), else WITHHOLD; shapes 2/3/0 → WITHHOLD.
- T2: WITHHOLD on all envelopes (SUSPECT/defer).
- T3: shape 1 → CONVERGE prim_newest iff rel known AND ≥ k/(k+1),
  else WITHHOLD; shape 2 → WITHHOLD with tie-guard marking; shapes
  3/0 → WITHHOLD.
- Reliability in thousandths; unknown rel (−1) → no fire for T1/T3.

## §3. Ledger chain (evidence format)

Per path, chaining `prev = sha256(prev || seq_le8 || path_u8 ||
thou_le4 || qid || 0x00 || dec || 0x00 || ch || 0x00 || rule || 0x00)`,
with `prev` starting at 32 zero bytes and seq counting from 0, over the
same envelope→threshold order as the `P|` lines. This byte layout is the
one recorded in the trial evidence — it is the format under
verification, not trial decision logic. Head = final `prev` as 64 hex
characters, emitted as `H|<path>|<hex>`.

## §4. Match criterion (kill bars)

- **ORACLE-ZAG-MATCH:** every recomputed `P|` line, all 3 `H|` heads,
  the `S|` counts, and the `C|` shape counts must match the committed
  TP1 results (`evidence/run0.log`, sha256 `d57fda22…32d1d9`) with **0
  mismatches**. Any single mismatch FAILs the oracle.
- **ORACLE-ZAG-DET:** ≥3 runs byte-identical (stdout sha256 equal
  across runs), pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Pure Zag, zero RNG.
- TP-CACHE applies: no binaries or `.zagd` cache files in the commit.

## §5. Roles

- The pure-Zag oracle is the verification authority for TP1.
- The Python oracle (`oracle/tp_oracle.py`) is demoted to build-script
  status: it may prepare input data and cross-check, but it no longer
  certifies TP1 results.

**FROZEN 2026-09-22.**
